import json
import yaml
from kubernetes import client, config, utils
from kubernetes.client.exceptions import ApiException
from flask import Flask, jsonify, request
from flask_cors import CORS


# Flask API
app = Flask(__name__)


# Kubernetes API
config.load_incluster_config()
v1 = client.CoreV1Api()
k8s_client = client.ApiClient() 
customAPI = client.CustomObjectsApi()



class Pod:
    def __init__(self, data: dict = {}):
        self.RAW = data
        self.NAME = data.get('metadata', {}).get('name', '')
        self.NAMESPACE = data.get('metadata', {}).get('namespace', '')
        self.KIND = data.get('metadata', {}).get('ownerReferences', [{}])[0].get('kind', '')
        self.IMAGE = data.get('status', {}).get('containerStatuses', [{}])[0].get('image', '')
        self.IMAGE_ID = data.get('status', {}).get('containerStatuses', [{}])[0].get('imageID', '')
        self.IP = data.get('status', {}).get('podIP', '')
        self.HOST_IP = data.get('status', {}).get('hostIP', '')
        self.STATUS = data.get('status', {}).get('phase', '')


    def attributes(self):
        return {'name': self.NAME, 'namespace': self.NAMESPACE, 'kind': self.KIND, 'image': self.IMAGE, 'image_id': self.IMAGE_ID, 'ip': self.IP, 'host_ip': self.HOST_IP, 'status': self.STATUS}



@app.route('/')
def index():
    return jsonify(code=200, data='Kubernetes Security')

    

@app.route('/api/v1/pods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def interact_pods():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    if request.method == 'GET':
        try:
            if pod and namespace:
                res = v1.read_namespaced_pod(name=pod, namespace=namespace, _preload_content=False)
                return jsonify(code=200, data=Pod(data=json.loads(res.data)).attributes())
            else:
                res = v1.list_pod_for_all_namespaces(watch=False,  _preload_content=False)
                return jsonify(code=200, data=[Pod(data=item).attributes() for item in json.loads(res.data)['items']])
        except ApiException as e:
            if e.status == 404:
                return jsonify(code=404, data='Not Found')
            else:
                return jsonify(code=500, data='Internal Server Error')
        

    elif request.method == 'POST':
        pass


    elif request.method == 'PUT':
        with open('../Policy/block-traffic.yaml', 'r') as f:
            data = yaml.safe_load(f)
        data['metadata']['namespace'] = namespace
        data['spec']['podSelector']['matchLabels']['app.kubernetes.io/name'] = pod
        with open('../Policy/block-traffic.yaml', 'w') as f:
            yaml.dump(data, f)

        try:
            utils.create_from_yaml(k8s_client, '../Policy/block-traffic.yaml')
            return jsonify(code=200, data='OK')
        except ApiException as e:
            if e.status == 409:
                return jsonify(code=409, data='Conflict')
            else:
                return jsonify(code=500, data='Internal Server Error')
        

    elif request.method == 'DELETE':
        try:
            v1.delete_namespaced_pod(name=pod, namespace=namespace)
            return jsonify(code=200, data='OK')
        except ApiException as e:
            if e.status == 404:
                return jsonify(code=404, data='Not Found')
            else:
                return jsonify(code=500, data='Internal Server Error')
        

    else:
        return jsonify(code=400, data='Bad Request')



    


received_data = {}
@app.route('/api/v1/webhook-listener', methods=['GET', 'POST'])
def webhook_listener():
    if request.method == 'GET':
        return jsonify(code=200, data=received_data)
    elif request.method == 'POST':
        received_data = request.get_json()
        return jsonify(code=200, data='OK')
    else:
        return jsonify(code=400, data='Bad Request')
    


def auto_block_traffic():
    pass
    


@app.route('/api/v1/resources', methods=['GET'])
def get_resource_usage():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    res = customAPI.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1", namespace=namespace, plural="pods")
    if not pod:
        return jsonify(code=200, data=[{'name': item['metadata']['name'], 'namespace': item['metadata']['namespace'],
                                    'cpu': item['containers'][0]['usage']['cpu'], 'memory': item['containers'][0]['usage']['memory']} 
                                    for item in res['items']])
    else:
        return jsonify(code=200, data=[{'name': item['metadata']['name'], 'namespace': item['metadata']['namespace'],
                                    'cpu': item['containers'][0]['usage']['cpu'], 'memory': item['containers'][0]['usage']['memory']} 
                                    for item in res['items'] if item['metadata']['name'] == pod])
    
    
        


if __name__ == '__main__':
    app.run(debug=True, port=50000)
    CORS(app)
    