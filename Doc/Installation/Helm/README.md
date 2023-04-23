# Deploy with Helm

## Install ElasticSearch

```
helm repo add elastic https://helm.elastic.co
helm repo update
helm install elasticsearch elastic/elasticsearch -f elasticsearch.yaml
```

## Install Kibana

```
helm install kibana elastic/kibana -f kibana.yaml
```

### Generate Kibana encryption key

If you want to use the some features of Kibana, such as **Webhook** connector, you need to generate a new encryption key for Kibana.

```
kubectl exec -it {kibana-pod-name} -- bash
```

You can generate a new encryption key by running the following command:
    
```
bin/kibana-encryption-keys generate -f -q
```

[Generate Kibana encryption key](../../Images/kibana-encryptionKey.png)

## Uninstall Kibana

If you want to uninstall Kibana, you can completely remove it by running the following commands:

```
helm uninstall kibana
kubectl delete configmap kibana-kibana-helm-scripts
kubectl delete serviceaccount pre-install-kibana-kibana
kubectl delete roles pre-install-kibana-kibana
kubectl delete rolebindings pre-install-kibana-kibana
kubectl delete job pre-install-kibana-kibana
kubectl delete secrets kibana-kibana-es-token
```

## Install K8s Agent

You can follow the instructions when adding Elastic Agent from Kubernetes integration in Kibana. You need to modify the manifest file to add the ElasticSearch service IP and the password.

```
    hosts:
        - 'http://{ELASTICSEARCH_SERVICE_IP}:9200'
    username: 'elastic'
    password: '{ELASTICSEARCH_PASSWORD}'
```

Then, apply the manifest file.

```
kubectl apply -f k8s-agent.yaml
```