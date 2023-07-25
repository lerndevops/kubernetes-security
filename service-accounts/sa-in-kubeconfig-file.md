## using serviceaccount token in kubeconfig file      ** NOT RECOMENDED ** 

> Kubernetes 1.24 removed the automatic creation of secrets for new service accounts. starting 1.24 versions, including Kubernetes v1.27, API credentials are obtained directly by using the [TokenRequest](https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/token-request-v1/) API, and are mounted into Pods using a volume. The tokens obtained using this method have bounded lifetimes, and are automatically invalidated when the Pod they are mounted into is deleted.

> we can still manually create a service account token Secret; for example, if you need a token that never expires. However, using the [TokenRequest](https://kubernetes.io/docs/reference/kubernetes-api/authentication-resources/token-request-v1/) subresource to obtain a token to access the API is recommended instead

> This API simplifies the process and enhances cluster security. Embrace these changes to enjoy a smoother Kubernetes experience with improved access control. 

### create serviceaccount scoped to any namespace 

- kubectl create namespace dev

- kubectl create sa testsa -n dev

#### Creating Long-Lived Token

> **Create a secret and specify the name of the service account as annotations within the metadata section.**

```
vi testsa-secret.yaml 

apiVersion: v1
kind: Secret
metadata:
    name: testsa-secret
    namespace: dev
    annotations:
       kubernetes.io/service-account.name: testsa
type: kubernetes.io/service-account-token

save & close the file

kubectl apply -f testsa-secret.yaml
```

## get the secret associated with serviceaccount 

`kubectl describe serviceaccount testsa -n dev`

```
root@mnode:~# kubectl describe sa testsa
Name:                testsa
Namespace:           dev
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              testsa-secret
Events:              <none>
```

## Token Value is our secrect

`kubectl describe secret testsa-secret -n dev`

```
root@mnode:~# kubectl describe secret testsa-secret
Name:         testsa-token
Namespace:    dev
Labels:       <none>
Annotations:  kubernetes.io/service-account.name: testsa
              kubernetes.io/service-account.uid: 5e3e86bc-f0ef-418d-b115-1c747f26fcbb

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1107 bytes
namespace:  7 bytes
token:   eyJhbGciOiJSUzI1NiIsImtpZCI6IkpoMGpiWFUtVmRUcFhKNFItQ2Y2b3NiUHRFbzJSaEtJbGl0NGFWeFFPV3MifQeyJpc3MiOiJrdWJlcm5ldGV
```

#### as we can see above the screct is associated with ca.crt & a token, we can extract them and use in `config` file to connect to the cluster 

### Follow below to extract the values 
```
kubectl -n dev get secret/testsa-token-bg4xc -o jsonpath='{.data.ca\.crt}' > ca.crt
kubectl -n dev get secret/testsa-token -o jsonpath='{.data.token}' | base64 --decode > testsa.key
kubectl get secret/testsa-token-bg4xc -o jsonpath='{.data.namespace}' | base64 --decode
```

## create kube config file as below 

`replace the ca, token & server with content of ca.crt, testuser.key & server url accordingly`

`vi testuser.conf`

```
apiVersion: v1
kind: Config
clusters:
- name: kube-cluster
  cluster:
    certificate-authority-data: ${ca}
    server: ${server}
contexts:
- name: dev
  context:
    cluster: kube-cluster
    namespace: kube-system
    user: testsa
current-context: dev
users:
- name: testsa
  user:
    token: ${token}
```

#### Example: should look like below after entering the values 

` more testuser.conf `

```
apiVersion: v1
kind: Config
clusters:
- name: kube-cluster
  cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUN5RENDQWJDZ0F3SUJBZ0lCQURBTkJna3Foa2lH
    server: https://192.168.198.147:6443
contexts:
- name: dev
  context:
    cluster: kube-cluster
    namespace: dev
    user: testuser
current-context: dev
users:
- name: testuser
  user:
    token: eyJhbGciOiJSUzI1NiIsImtpZCI6Ik1fZF9rOEJMVmd3NFp2bUotSWVQdHZ6YlpEazk0TnBCOTVnMjJVQmlRTTAifQ.eyJpc3MiOiJ
```

### validate testuser able to authenticate with server 

```
root@kube-master:/home/devops/# kubectl --kubeconfig testuser.conf version --short
Client Version: v1.27.0
Server Version: v1.27.0
```

### validate testuser authorization 
```
root@kube-master:/home/devops/.kube# kubectl --kubeconfig testuser.conf get nodes
Error from server (Forbidden): nodes is forbidden: User "system:serviceaccount:kube-system:testuser" cannot list resource "nodes" in API group "" at the cluster scope
```

`the above Error is expected as we just authenticated with apiserver, but we haven't defined what testuser can perform` 


## Role Based Access Control ( RBAC ) 

### define a Role -- what can be done 

```
vi testsa-role.yaml 

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: readonly-role
rules:
  - apiGroups: ["*"] # "" indicates the core API group
    resources: ["pods","deployments", "replicasets"]
    verbs: ["get", "watch", "list"]
    #verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

save, close the file & apply 

kubectl apply -f testsa-role.yaml

``` 

### define a rolebinding ( bind role to a user/serviceaccount, gives the user set of permmissions )

```
vi testsa-rb.yaml

apiVersion: rbac.authorization.k8s.io/v1
# This role binding allows "testuser" to read pods in the "kube-system" namespace.
kind: RoleBinding
metadata:
  name: readonly-binding
  namespace: dev
subjects:
  - kind: ServiceAccount
    name: testsa # Name is case sensitive
    namespace: dev
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: readonly-role # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io

save,close & apply the file 

kubectl apply -f testsa-rb.yaml
```

## validate able to list deployments, pods replicasets 

```
root@kube-master:/home/devops/.kube# kubectl --kubeconfig testuser.conf get deployment
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
calico-kube-controllers   1/1     1            1           3d19h
coredns                   2/2     2            2           3d19h
```

```
root@kube-master:/home/devops/.kube# kubectl --kubeconfig testuser.conf get replicaset
NAME                                 DESIRED   CURRENT   READY   AGE
calico-kube-controllers-778676476b   1         1         1       3d19h
coredns-6955765f44                   2         2         2       3d19h
```