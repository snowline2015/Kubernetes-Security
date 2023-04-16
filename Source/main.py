import json
import yaml
import subprocess
from kubernetes import client, config, utils
from flask import Flask, jsonify, request, Response


# Flask API
app = Flask(__name__)


# Kubernetes API
config.load_incluster_config()
v1 = client.CoreV1Api()
k8s_client = client.ApiClient() 



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
                # return jsonify(code=200, data=Pod(data=res).RAW)
                return Response(res)
            else:
                res = v1.list_pod_for_all_namespaces(watch=False,  _preload_content=False)
                # return jsonify(code=200, data=[Pod(data=item).RAW for item in res.items])
                return Response(res)
        except Exception as e:
            return jsonify(code=500, data=str(e))
        

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
        except Exception as e:
            return jsonify(code=500, data=str(e))
        

    elif request.method == 'DELETE':
        try:
            v1.delete_namespaced_pod(name=pod, namespace=namespace)
            return jsonify(code=200, data='OK')
        except Exception as e:
            return jsonify(code=500, data=str(e))
        

    else:
        return jsonify(code=400, data='Bad Request')
    




if __name__ == '__main__':
    app.run(debug=True, port=50000)