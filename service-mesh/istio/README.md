## What is Istio?

> **Istio is an open source service mesh that layers transparently onto existing distributed applications.**

> **Istio’s powerful features provide a uniform and more efficient way to secure, connect, and monitor services.**

> **Istio is the path to load balancing, service-to-service authentication, and monitoring – with few or no service code changes. Its powerful control plane brings vital features, including:**

1) Secure service-to-service communication in a cluster with TLS encryption, strong identity-based authentication and authorization
2) Automatic load balancing for HTTP, gRPC, WebSocket, and TCP traffic
3) Fine-grained control of traffic behavior with rich routing rules, retries, failovers, and fault injection
4) A pluggable policy layer and configuration API supporting access controls, rate limits and quotas
5) Automatic metrics, logs, and traces for all traffic within a cluster, including cluster ingress and egress

## How it Works

#### Istio has two components: 

1) **data plane**
2) **control plane.**

> **The `data plane` is the communication between services.** 

>>> **Without a service mesh, the network doesn’t understand the traffic being sent over, and can’t make any decisions based on what type of traffic it is, or who it is from or to.**

>>> **Service mesh uses a proxy to intercept all your network traffic, allowing a broad set of application-aware features based on configuration you set.**

>>> **An Envoy proxy is deployed along with each service that you start in your cluster, or runs alongside services running on VMs**

> **The `control plane` takes your desired configuration, and its view of the services, and dynamically programs the proxy servers, updating them as the rules or the environment changes.**

>>>>>> ![with-without-service-mesh](https://github.com/lerndevops/kubernetes-security/blob/main/img/with-without-service-mesh.png)

## Install istio 

>> https://istio.io/latest/docs/setup/getting-started/

## Istio Profiles 

>> https://istio.io/latest/docs/setup/additional-setup/config-profiles/ 

## Istio Integrations

>> https://istio.io/latest/docs/ops/integrations/

## Inject Istio Envoy Proxy to Pods 

> **Add a namespace label to instruct Istio to automatically inject Envoy sidecar proxies when you deploy your application later:**

```sh
kubectl label namespace default istio-injection=enabled
```

>>> **`Note:` the above we labeled the defualt namespace, choose your namespace accordingly**