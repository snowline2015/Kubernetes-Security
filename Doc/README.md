# Kubernetes Security API
This is a Flask API that allows interacting with Kubernetes pods and implements an auto-blocking feature for incoming traffic based on certain policies.

&nbsp;

## Installation

To use this API, you need to install the following dependencies:

- kubernetes: to interact with the Kubernetes API
- Flask: to implement the API endpoints

You can install these dependencies by running the following command:

```
pip install kubernetes Flask
```

&nbsp;

## Usage

To use this API, you need to run the app.py file. You can do this by running the following command:

```
python app.py
```

By default, the API will be available at http://localhost:50000/.

&nbsp;

## Endpoints
The API provides the following endpoints:

**GET /**

Returns a JSON response with a message “Kubernetes Security”.

&nbsp;

**GET /api/v1/pods**

Returns a JSON response with information about all the pods in all namespaces, or information about a specific pod in a specific namespace if the pod and namespace query parameters are provided.

&nbsp;

**POST /api/v1/pods**

Not implemented.

&nbsp;

**PUT /api/v1/pods**

Creates a policy to block incoming traffic to a specific pod in a specific namespace. Requires pod and namespace query parameters. The policy is defined in a YAML file located at *Policy/block-traffic.yaml*.

&nbsp;

**DELETE /api/v1/pods**

Deletes a specific pod in a specific namespace. Requires pod and namespace query parameters.

&nbsp;

**GET /api/v1/webhook-listener**

Returns a JSON response with the data received from a webhook listener. This endpoint is deplayed.

&nbsp;

**POST /api/v1/webhook-listener**

Receives data from a webhook listener and stores it in memory. This endpoint is deplayed.