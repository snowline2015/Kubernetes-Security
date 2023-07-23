import os
import json
import yaml
import logging
import base64
import requests
from Entities import Pod
from Logging import Logging
from Trivy import Trivy
from kubernetes import client, config, utils
from kubernetes.client.exceptions import ApiException
from flask import Flask, request, jsonify
from flask_cors import CORS


# Flask API
app = Flask(__name__)
CORS(app)
logging.getLogger('werkzeug').disabled = True


# Kubernetes API
config.load_incluster_config()
v1 = client.CoreV1Api()
k8s_client = client.ApiClient() 
customAPI = client.CustomObjectsApi()





@app.route('/')
def index():
    return jsonify(code=200, data='Kubernetes Security'), 200

    



@app.route('/api/v1/pods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def interact_pods():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    if request.method == 'GET':
        try:
            if pod and namespace:
                res = v1.read_namespaced_pod(name=pod, namespace=namespace, _preload_content=False)
                return jsonify(code=200, data=Pod(data=json.loads(res.data)).attributes()), 200
            else:
                res = v1.list_pod_for_all_namespaces(watch=False,  _preload_content=False)
                return jsonify(code=200, data=[Pod(data=item).attributes() for item in json.loads(res.data)['items']]), 200
            
        except ApiException as e:
            if e.status == 404:
                return jsonify(code=404, data='Not Found'), 404
            else:
                return jsonify(code=500, data='Internal Server Error'), 500
        

    elif request.method == 'POST':
        pass


    elif request.method == 'PUT':
        with open('Policy/block-traffic.yaml', 'r') as f:
            data = yaml.safe_load(f)
        data['metadata']['namespace'] = namespace
        data['spec']['podSelector']['matchLabels']['app.kubernetes.io/name'] = pod
        with open('../Policy/block-traffic.yaml', 'w') as f:
            yaml.dump(data, f)

        try:
            utils.create_from_yaml(k8s_client, '../Policy/block-traffic.yaml')
            return jsonify(code=200, data='OK'), 200
        
        except ApiException as e:
            if e.status == 409:
                return jsonify(code=409, data='Conflict'), 409
            else:
                return jsonify(code=500, data='Internal Server Error'), 500
        

    elif request.method == 'DELETE':
        if not pod or not namespace:
            return jsonify(code=400, data='Bad Request'), 400

        try:
            v1.delete_namespaced_pod(name=pod, namespace=namespace, propagation_policy='Background', grace_period_seconds=0)
            Logging(level='INFO', message=f'{pod}|{namespace}|DELETED BY USER').log()
            return jsonify(code=200, data='OK'), 200
        
        except ApiException as e:
            if e.status == 404:
                return jsonify(code=404, data='Not Found'), 404
            else:
                return jsonify(code=500, data='Internal Server Error'), 500
        

    else:
        return jsonify(code=400, data='Bad Request'), 400





@app.route('/api/v1/scan', methods=['GET', 'POST'])
def scan_image():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        if not pod or not namespace:
            return jsonify(code=400, data='Bad Request'), 400

        try:
            res = v1.read_namespaced_pod(name=pod, namespace=namespace, _preload_content=False)
            pod_info = Pod(data=json.loads(res.data)).attributes()
            trivy = Trivy()
            trivy.scan(pod_info['image_id'])
            return jsonify(code=200, data=trivy.result()), 200

        except ApiException as e:
            if e.status == 404:
                return jsonify(code=404, data='Not Found'), 404
            else:
                return jsonify(code=500, data='Internal Server Error'), 500





@app.route('/api/v1/webhook', methods=['GET', 'POST'])
def webhook_listener():

    if request.method == 'POST':
        try:
            alert = json.loads(request.get_json(force=True))
        except json.JSONDecodeError as e:
            decoder = json.JSONDecoder(object_pairs_hook=dict)
            alert, _ = decoder.raw_decode(request.get_json(force=True))
            
        try:
            alert_handler(alert)
            return jsonify(code=200, data='OK'), 200
        except Exception as e:
            return jsonify(code=500, data='Internal Server Error'), 500
        
    # elif request.method == 'GET':
    #     return jsonify(code=200, data={'temp1': str(temp1), 'temp2': str(temp)}), 200

    else:
        return jsonify(code=400, data='Bad Request'), 400
    


def alert_handler(data: dict):

    pod_info = alert_pod_info(json.loads(data.get('message', '{}')))
    rule = data.get('kibana', {}).get('alert', {}).get('rule', {})

    # To be enhanced, deleting pod for now
    v1.delete_namespaced_pod(name=pod_info['pod'], namespace=pod_info['namespace'], propagation_policy='Background', grace_period_seconds=0)
    Logging(level=rule.get('severity', '').upper(), message=f"{pod_info['pod']}|{pod_info['namespace']}|DELETED BY RULE: {rule.get('name', '')}").log()



def alert_pod_info(log: dict):

    if 'process_exec' in log:
        pod = log.get('process_exec', {}).get('process', {}).get('pod', {})
    elif 'process_kprobe' in log:
        pod = log.get('process_kprobe', {}).get('process', {}).get('pod', {})

    return {
        'namespace': pod.get('namespace', ''),
        'pod': pod.get('name', ''),
        'imageID': pod.get('container', {}).get('image', {}).get('id', '').split('/')[-1],
        'image': pod.get('container', {}).get('image', {}).get('name', ''),
        'labels': pod.get('pod_labels', {})
    }





@app.route('/api/v1/resources', methods=['GET'])
def get_resource_usage():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    res = customAPI.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace=namespace, plural="pods")
    if not pod:
        return jsonify(code=200, data=[{'name': item['metadata']['name'], 'namespace': item['metadata']['namespace'],
                                    'cpu': item['containers'][0]['usage']['cpu'], 'memory': item['containers'][0]['usage']['memory']} 
                                    for item in res['items']]), 200
    else:
        return jsonify(code=200, data=[{'name': item['metadata']['name'], 'namespace': item['metadata']['namespace'],
                                    'cpu': item['containers'][0]['usage']['cpu'], 'memory': item['containers'][0]['usage']['memory']} 
                                    for item in res['items'] if item['metadata']['name'] == pod]), 200
    




@app.route('/api/v1/logs', methods=['GET'])
def get_logs():
    result = -1
    status = request.args.get('status', '')
    raw = request.args.get('raw', default=False, type=bool)

    try:
        result = int(request.args.get('result', '-1'))
    except:
        return jsonify(code=400, data='Bad Request'), 400

    if not os.path.exists('Log/KUBE_SEC.log'):
        return jsonify(code=200, data=[]), 200
    
    logs = open('Log/KUBE_SEC.log', 'r').read().splitlines()

    if raw:
        return jsonify(code=200, data=logs), 200


    def parse_log(log: str):
        return {
            'timestamp': log.split('|')[0],
            'level': log.split('|')[1],
            'pod': log.split('|')[2],
            'namespace': log.split('|')[3],
            'message': log.split('|')[4]
        } 


    if result < -1:
        return jsonify(code=400, data='Bad Request'), 400
    
    elif result == 0:
        return jsonify(code=200, data=[]), 200

    elif result == -1 or result > len(logs):
        if status:
            return jsonify(code=200, data=[parse_log(item) for item in logs if status.lower() in parse_log(item)['message'].lower()]), 200
        else:
            return jsonify(code=200, data=[parse_log(item) for item in logs]), 200
        
    else:
        if status:
            return jsonify(code=200, data=[parse_log(item) for item in logs if status.lower() in parse_log(item)['message'].lower()][-result:]), 200
        else:
            return jsonify(code=200, data=[parse_log(item) for item in logs][-result:]), 200





@app.route('/api/v1/rules', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def interact_security_rules():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    rule_id = request.args.get('rule_id', '')

    if not username:
        username = 'elastic'

    if not password:

        try:
            secret = v1.read_namespaced_secret(name='elasticsearch-master-credentials', namespace='default', watch=False, _preload_content=False)
        except Exception as e:
            return jsonify(code=500, data=e), 500

        password = base64.b64decode(json.loads(secret.data.get('data', {}).get('password',''))).decode('utf-8')

    session = requests.Session()
    session.auth = (username, password)
    session.headers.update({'kbn-xsrf': 'true', 'Content-Type': 'application/json'})
    base_url = 'http://kibana-kibana.default.svc.cluster.local:5601/api/detection_engine'

    if request.method == 'GET':
        if rule_id:
            res = session.get(f'{base_url}/rules/{rule_id}')
            return jsonify(code=res.status_code, data=json.loads(res.text)), res.status_code
        
        else:
            res = session.get(f'{base_url}/rules/_find', params={'per_page': 100}).json()
            while res.get('total', 0) > len(res.get('data', [])):
                temp = session.get(f'{base_url}/rules/_find', params={'per_page': 100, 'page': res.get('page', 1) + 1}).json()
                res['data'].extend(temp.get('data', []))
            return jsonify(code=200, data=res.get('data', [])), 200


    elif request.method == 'POST':
        pass


    elif request.method == 'PATCH':
        pass


    elif request.method == 'DELETE':
        if not rule_id:
            return jsonify(code=400, data='Bad Request'), 400

        res = session.delete(f'{base_url}/rules/{rule_id}')
        return jsonify(code=res.status_code, data=json.loads(res.text)), res.status_code
    

    else:
        return jsonify(code=400, data='Bad Request'), 400
        





def main():
    app.run(host='0.0.0.0', port=50000)



if __name__ == '__main__':
    main()
    
    
        