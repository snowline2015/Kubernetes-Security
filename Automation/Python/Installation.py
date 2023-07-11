import requests
import subprocess
import yaml


# Tetragon
# subprocess.run('helm repo add cilium https://helm.cilium.io && '
#                'helm repo update && '
#                'helm install tetragon cilium/tetragon -n kube-system --set tetragon.enableProcessCred=true --set tetragon.enableProcessNs=true && '
#                'kubectl rollout status -n kube-system ds/tetragon -w', shell=True)


# # ElasticSearch
# subprocess.run('helm repo add elastic https://helm.elastic.co && '
#                 'helm repo update && '
#                 'helm install elasticsearch elastic/elasticsearch -f https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/elasticsearch.yaml',
#                 shell=True)


# # Kibana
# subprocess.run('helm install kibana elastic/kibana -f https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/kibana.yaml',
#                 shell=True)


# Elastic Agent
## Get Secret
secret = subprocess.run("kubectl get secrets --namespace=default elasticsearch-master-credentials -ojsonpath='{.data.password}' | base64 -d", shell=True)

## Edit
manifest = requests.get('https://raw.githubusercontent.com/snowline2015/Kubernetes-Security/main/Doc/Installation/Helm/elastic-agent.yaml').text
manifest = yaml.load(manifest, Loader=yaml.FullLoader)




