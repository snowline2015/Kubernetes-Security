import json
import yaml
import subprocess
import kubernetes
from flask import Flask, jsonify, request

app = Flask(__name__)


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
    return jsonify(code=200, data='Kubernetes Security ')



@app.route('/api/v1/pods', methods=['GET', 'POST', 'PUT', 'DELETE'])
def interact_pods():
    pod = request.args.get('pod', '')
    namespace = request.args.get('namespace', '')

    if methods == 'GET':
        try:
            res = subprocess.run(f'kubectl get pods {pod} -n "{namespace}" -o json', shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.stdout:
                data = json.loads(res.stdout)
                return jsonify(code=200, data=[Pod(data).RAW for data in data.get('items', [])]) if not pod else jsonify(code=200, data=Pod(data).RAW)
            else:
                return jsonify(code=404, data='Not Found')
        except Exception as e:
            return jsonify(code=500, data='Internal Server Error')
    

    elif methods == 'POST':
        pass
    

    elif methods == 'PUT':
        with open('../Policy/block-traffic.yaml', 'r') as f:
            data = yaml.safe_load(f)
        data['metadata']['namespace'] = namespace
        data['spec']['podSelector']['matchLabels']['app.kubernetes.io/name'] = pod
        with open('../Policy/block-traffic.yaml', 'w') as f:
            yaml.dump(data, f)
        
        try:
            res = subprocess.run(f'kubectl apply -f network-policy.yaml', shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return jsonify(code=200, data='OK')if res.stdout else jsonify(code=404, data='Not Found')
        except Exception as e:
            return jsonify(code=500, data='Internal Server Error')


    elif methods == 'DELETE':
        try:
            res = subprocess.run(f'kubectl delete pod/{pod} -n "{namespace}"', shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return jsonify(code=200, data='OK') if res.stdout else jsonify(code=404, data='Not Found')
        except Exception as e:
            return jsonify(code=500, data='Internal Server Error')




def main():
    app.run(debug=True, port=50000)





if __name__ == '__main__':
    main()