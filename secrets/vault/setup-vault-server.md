## Setup Vault Server on Kubrnetes Cluster

### Pre Req
1) **Kubernetes Cluster is ready, and the kubectl command-line tool**

    * [Setup a Single Node Kubernetes Cluster](https://github.com/lerndevops/kubernetes/blob/master/1-intall/setup-single-node-kubernetes-cluster.md)

2) **Helm CLI**

    * [Install Helm CLI](https://helm.sh/docs/intro/install/)

## Install vault server with Helm 

> **Helm helps you manage Kubernetes applications with Helm Charts which helps you define, install, and upgrade even the most complex Kubernetes application.**

> **the Vault Helm Chart installs and configures all the necessary components to run Vault in several different modes.**

1) **Add the HashiCorp Helm repository**
   ```
    helm repo add hashicorp https://helm.releases.hashicorp.com
   ```
2) **Update all the repositories to ensure helm is aware of the latest versions.**
   ```
    helm repo update
   ```
3) **Install the latest version of the Vault server running in development mode**
   ```
    helm install vault hashicorp/vault --set "server.dev.enabled=true"

    The Vault pod and Vault Agent Injector pod are deployed in the default namespace.**
   ```
4) **Display all the pods in the default namespace.**
   ```
    kubectl get pods

    NAME                                    READY   STATUS    RESTARTS   AGE
    vault-0                                 1/1     Running   0          80s
    vault-agent-injector-5945fb98b5-tpglz   1/1     Running   0          80s
   ```


## Installation Referece links 

1) https://developer.hashicorp.com/vault/downloads 

2) https://developer.hashicorp.com/vault/docs/install