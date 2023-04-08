import json
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify(code=200, data='Kubernetes Security ')


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


@app.route('/api/pods', methods=['GET'])
def get_pods():
    try:
        res = subprocess.run('kubectl get pods -o json', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res:
            data = json.loads(res.stdout)
            return jsonify(code=200, data=[Pod(item).RAW for item in data.get('items', [])])
        else:
            return jsonify(code=404, data='Pods not found')
    except ValueError as e:
        return jsonify(code=400, data='Bad request: ' + str(e))



@app.route('/api/pods', methods=['GET'])
def get_pod_info():
    pod = request.args.get('pod')
    namespace = request.args.get('namespace')
    try:
        res = subprocess.run(f'kubectl get pods {pod} -n {namespace} -o json',
                             shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res:
            return jsonify(code=200, data=response)
        else:
            return jsonify(code=404, data='Pod not found')
    except ValueError as e:
        return jsonify(code=400, data='Bad request: ' + str(e))



@app.route('/api/report', methods=['POST'])
def generate_report():
    return jsonify(code=201, data='Report created')


def main():
    app.run(debug=True, port=50000)


if __name__ == '__main__':
    main()