# Deploy ECK in Kubernetes cluster
Please follow the instructions from [here](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html)

&nbsp;

## Install CRD
```
kubectl create -f https://download.elastic.co/downloads/eck/2.7.0/crds.yaml
```

## Install operators RBAC
```
kubectl apply -f https://download.elastic.co/downloads/eck/2.7.0/operator.yaml
```

## Install ElasticSearch
```
kubectl apply -f elasticsearch.yaml
```

## Get ElasticSearch password
```
kubectl get secret elasticsearch-es-elastic-user -o go-template='{{.data.elastic | base64decode}}'
```

## Install Kibana
```
kubectl apply -f kibana.yaml
```

## Install K8s Agent
You can follow the instructions when adding Elastic Agent from Kubernetes integration in Kibana.
You need to modify the manifest file to add the ElasticSearch service IP and the password.

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

> **Warning**: This is ECK so you need your subscription to be ***platinum*** to use some features. For example, you can't use **webhook** connector to send alerts.
> 
> Therefore, it is recommended to install by [Helm](Kubernetes-Security/tree/main/Doc/Installation/Helm) instead.


