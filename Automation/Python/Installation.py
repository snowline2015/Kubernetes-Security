import os
import requests
import subprocess


# Tetragon
subprocess.run(
    'helm repo add cilium https://helm.cilium.io && helm repo update && '
    'helm install tetragon cilium/tetragon -n kube-system --set tetragon.enableProcessCred=true --set tetragon.enableProcessNs=true && '
    'kubectl rollout status -n kube-system ds/tetragon -w', shell=True)



# ElasticSearch
subprocess.run(
    'helm repo add elastic https://helm.elastic.co && helm repo update && '
    'helm install elasticsearch elastic/elasticsearch -f '
    'https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/elasticsearch.yaml', shell=True)



# Kibana
subprocess.run('helm install kibana elastic/kibana -f '
               'https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/kibana.yaml', shell=True)



# Elastic Agent
## Get ElasticSearch Info
secret = subprocess.run("kubectl get secrets --namespace=default elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d", 
                        shell=True, capture_output=True, text=True).stdout
ip = subprocess.run("kubectl get service --namespace=default elasticsearch-master -o jsonpath='{.spec.clusterIP}'", 
                    shell=True, capture_output=True, text=True).stdout

## Edit
manifest = requests.get('https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/elastic-agent-standalone-kubernetes.yaml').text
manifest = manifest.replace('https://elasticsearch-master:9200', f'https://{ip}:9200')
manifest = manifest.replace('changeme', secret)

## Apply
with open(f'{os.path.dirname(__file__)}/manifest.yaml', 'w') as f:
    f.write(manifest)

subprocess.run(f'kubectl apply -f {os.path.dirname(__file__)}/manifest.yaml', shell=True)



# Metrics Server
subprocess.run('kubectl apply -f '
               'https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml', shell=True)

subprocess.run('kubectl patch -n kube-system deployment metrics-server --type=json -p \'[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]\'', shell=True)



# Frontend & Backend
subprocess.run('kubectl apply -f https://raw.githubusercontent.com/huyvdq2/tetragon_fe/main/k8s.yaml && '
               'kubectl apply -f https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Security/backend.yaml', shell=True)