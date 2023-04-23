# Kind
[kind](https://sigs.k8s.io/kind) is a tool for running local Kubernetes clusters using Docker container “nodes”.
kind was primarily designed for testing Kubernetes itself, but may be used for local development or CI.

If you have [go](https://golang.org/) ([1.17+](https://golang.org/doc/devel/release.html#policy)) and [docker](https://www.docker.com/) installed, all you need is to run:

```
go install sigs.k8s.io/kind@v0.18.0 && kind create cluster
```

# Tetragon

Cilium’s new [Tetragon](https://github.com/cilium/tetragon) component enables powerful realtime, eBPF-based Security Observability and Runtime Enforcement.

Tetragon detects and is able to react to security-significant events, such as

* Process execution events
* System call activity
* I/O activity including network & file access

When used in a Kubernetes environment, Tetragon is Kubernetes-aware - that is, it understands Kubernetes identities such as namespaces, pods and so-on - so that security event detection can be configured in relation to individual workloads.

## Deploy Tetragon

To install and deploy Tetragon, run the following commands:

```
helm repo add cilium https://helm.cilium.io
helm repo update
helm install tetragon cilium/tetragon -n kube-system
kubectl rollout status -n kube-system ds/tetragon -w
```

## Watch Tetragon logs
```
kubectl logs -n kube-system -l app.kubernetes.io/name=tetragon -c export-stdout -f | tetra getevents -o compact
```

Please follow this [link](https://github.com/cilium/tetragon#tetra-cli) for more information about the Tetra CLI.
