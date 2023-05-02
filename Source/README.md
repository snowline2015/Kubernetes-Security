# API
This is a Flask API that allows interacting with Kubernetes pods and implements an auto-blocking feature for ingress and egress traffic.

&nbsp;

## Installation

### **Requirements**

To use this API, you need to install the following dependencies:

- kubernetes: to interact with the Kubernetes API
- Flask: to implement the API endpoints

You can install these dependencies by running the following command:

```
python3 -m pip install -r requirements.txt
```

### **Metrics Server**

The API requires the Metrics Server to be installed in the Kubernetes cluster. You can install it by running the following command:

```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

If you get an error saying that ***"Readiness probe failed: HTTP probe failed with statuscode: 500"***, you can fix it by running the following command:

```
kubectl patch -n kube-system deployment metrics-server --type=json \
  -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
```

## Usage

To use this API, you need to run the app.py file. You can do this by running the following command:

```
python3 main.py
```

By default, the API will be available at http://localhost:50000/.

&nbsp;

## Endpoints
The API provides the following endpoints:

**GET /**

Returns a JSON response with a message “Kubernetes Security”.

&nbsp;

**GET /api/v1/pods**

**Params**: *pod, namespace*

Returns a JSON response with information about all the pods in all namespaces, or information about a specific pod in a specific namespace if the pod and namespace query parameters are provided.

Example: 
```
curl -X GET "http://localhost:50000/api/v1/pods?pod=nginx&namespace=default"
```

&nbsp;

**POST /api/v1/pods**

**Params**: *pod, namespace*

Not implemented.

&nbsp;

**PUT /api/v1/pods**

**Params**: *pod, namespace*

Applies a traffic blocking policy to a specific pod in a specific namespace. Requires pod and namespace query parameters.

```
curl -X PUT "http://localhost:50000/api/v1/pods?pod=nginx&namespace=default"
```

&nbsp;

**DELETE /api/v1/pods**

Deletes a specific pod in a specific namespace. Requires pod and namespace query parameters.

```
curl -X DELETE "http://localhost:50000/api/v1/pods?pod=nginx&namespace=default"
```

&nbsp;

**GET /api/v1/resources**

**Params**: *pod, namespace*

Returns a JSON response with information about the CPU and memory usage of all the pods in all namespaces, or information about a specific pod in a specific namespace if the pod and namespace query parameters are provided.

Example: 
```
curl -X GET "http://localhost:50000/api/v1/resources?pod=kube-sec-be&namespace=kube-security"
```

> **Note**: This endpoint requires the Metrics Server to be installed in the Kubernetes cluster. See the [Metrics Server](#metrics-server) section for more information.

&nbsp;

**GET /api/v1/logs**

**Params**: *result, status*

Returns a JSON response with information about the lastest logs of all the pods in all namespaces, or number of logs specified in the result query parameter. The status query parameter can be used to filter the logs by status, which can be either "blocked" or "deleted".

Example: 
```
curl -X GET "http://localhost:50000/api/v1/logs?result=10&status=deleted"
```

