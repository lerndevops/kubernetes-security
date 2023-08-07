## Service Accounts

> **Kubernetes offers distinct ways for clients authenticate to the API server.**

> **As the name suggests, the service accounts are for the services or the non-human users in Kubernetes**

> **When you authenticate to the API server, you identify yourself as a particular user. Kubernetes recognises the concept of a user, however, Kubernetes itself does not have a User API.**

> **A service account provides an identity for processes that run in a Pod's containers, and maps to a ServiceAccount object.** 

> **Kubernetes by default creates a service account in each namespace of a cluster and call it a default service account. These default service accounts are mounted to every pod launched. However, the default service account has no attached permissions, and due to this, it is not of much use until we bind the service account with a role in the K8s RBAC**

> **In addition to the default service accounts, K8s allows us to create as many user-defined service accounts as we want. We can use the below command to create a service account.**



```sh
# Create a Service Account

kubectl create serviceaccount testsa

# Describe Service Account 

root@mnode:~# kubectl describe serviceaccount testsa
Name:                testsa
Namespace:           default
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              <none>
Events:              <none>
```

> ***In the K8s version before 1.24, every time we would create a service account, a non-expiring secret token (Mountable secrets & Tokens) was created by default. However, from version 1.24 onwards, it was disbanded and no secret token is created by default when we create a service account. However, we can create it when need be. Now let us take a look at the service account token in a bit more depth.***

## Service Account Token

##### Kubernetes supports two types of tokens from version 1.22 onwards.

- Long-Lived Token
- Time Bound Token

## Long-Lived Token

> As its name indicates, a long-lived token is one that never expires. Hence, it is less secure and discouraged to use.

#### Creating Long-Lived Token

> Before K8s version 1.24, whenever a service account was created, a secret object was also created that contains the secret token. These token would be long-lived token, which means it has no expiry. However, In Kubernetes version 1.24, it was disbanded due to security and scalability concerns.

> Although not recommended, K8s allows us to create a long-lived token. It is achieved in two different steps:

```sh
## Create a service account

kubectl create serviceaccount testsa
```
```yaml
## Create a secret and specify the name of the service account as annotations within the metadata section.
## vi testsa-token.yaml 
---
apiVersion: v1
kind: Secret
metadata:
  name: testsa-token
  annotations:
    kubernetes.io/service-account.name: testsa
type: kubernetes.io/service-account-token
```
```sh
kubectl apply -f testsa-token.yaml
```

## Time Bound Token

> **From version 1.22 onwards, Kubernetes introduced TokenRequest API. A token generated through this API is a time-bound token that expires after a time. It applies to both — the default service account and the custom-defined service accounts.**

#### Creating a time-bound token

> ***We can create a time-bound token using the below command:***
```sh
kubectl create token my-time-bound-token
```

> **However, it is not required to create a token manually. API credentials are obtained directly by using the TokenRequest API, and are mounted into Pods using a projected volume. The tokens obtained using this method have bounded lifetimes, and are automatically invalidated when the Pod they are mounted into is deleted.**

> **Taking an example of the default service account — when a pod is launched with automountServiceAccountToken set to True, K8s control plane mounts a project volume to the pod. The kubelet agent running on the node provisions the token on this volume.**