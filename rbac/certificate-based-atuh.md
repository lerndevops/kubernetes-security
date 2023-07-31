## Setting up RBAC with client certificates

> Kubernetes does not have API Objects for User Accounts. Of the available ways to manage authentication. we will use ***OpenSSL certificates*** for their simplicity. 

## step1: create a private/public keypair 

```
mkdir -p /home/certs
cd /home/certs
```

> **Create a private key for your user. In this example, we will name the file user1.key:**

`openssl genrsa -out user1.key 2048 ; ls -l`

```
root@mnode:~# openssl genrsa -out user1.key 2048 ; ls -l 
total 20
-rw-------  1 root root 1704 Jul 25 09:15 user1.key

```
## step2: create a CSR

> **Create a certificate sign request `user1.csr` using the private key we just created (user1.key in this example).** 

> **Make sure you specify your username and group in the -subj section (CN is for the username and O for the group).**

   `openssl req -new -key user1.key -out user1.csr -subj "/CN=user1/O=devops"`

## step3: Generate the Certificate using CSR 

> Locate Kubernetes cluster certificate authority (CA). This will be responsible for approving the request and generating the necessary certificate to access the cluster API. Its location is normally /etc/kubernetes/pki/ca.crt

> **create the final certificate user1.crt by approving the certificate sign request, user1.csr, we made earlier.**
  
  `openssl x509 -req -in user1.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out user1.crt -days 1000 ; ls -ltr`


```
  root@mnode:/home/certs# openssl x509 -req -in user1.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out user1.crt -days 1000 ; ls -ltr
	Signature ok
	subject=CN = user1, O = devops
	Getting CA Private Key
	total 12
	-rw------- 1 root root 1679 Jan  8 01:44 user1.key
	-rw-r--r-- 1 root root  915 Jan  8 01:47 user1.csr
	-rw-r--r-- 1 root root 1017 Jan  8 01:52 user1.crt
```

## step4: Create kubeconfig file using kubectl 

> ***Add cluster details to configuration file:***
 
  `kubectl config --kubeconfig=user1.conf set-cluster dev --server=https://<PLACE-APIServer-IP>:6443 --certificate-authority=/etc/kubernetes/pki/ca.crt`

> ***Add user details to your configuration file:***
 
  `kubectl config --kubeconfig=user1.conf set-credentials user1 --client-certificate=/home/certs/user1.crt --client-key=/home/certs/user1.key`

> ***Add context details to your configuration file:***
 
  `kubectl config --kubeconfig=user1.conf set-context dev --cluster=dev --namespace=dev --user=user1`
  
> ***Set dev context for use:***

  `kubectl config --kubeconfig=user1.conf use-context dev`
  
> ***validate Aceess to API Server:***

  `kubectl --kubeconfig /home/certs/user1.conf version --short`

``` 
  root@kube-master:/home/user1# kubectl --kubeconfig /home/certs/user1.conf version --short
	Client Version: v1.27.0
	Server Version: v1.27.0
```

## step5: Providing the Authorization to user1

* vi rbac-user1.yaml 

```
### define a Role/ClusterRole -- what can be done 
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: readonly
  namespace: dev
rules:
- apiGroups:
   - ""
  resources:
   - pods
   - services
  verbs:
   - get
   - list
   - watch
- apiGroups:
   - apps
  resources:
   - deployments
  verbs:
   - get
   - list
   - watch
---
### define a rolebinding/clusterrolebinding ( bind role to a user, gives the user set of permmissions )
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: user1-access
  namespace: dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: readonly
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: user1
```

> **svae, close & apply the manifest file**

> **kubectl apply -f rbac-user1.yaml**


## validate able to list deployments, pods replicasets 

```
root@kube-master:/home/certs# kubectl --kubeconfig user1.conf get deployment --namespace dev
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
nginx                     1/1     1            1           3d19h
```

```
root@kube-master:/home/user1/# kubectl --kubeconfig user1.conf get pods --namespace dev
NAME                                 DESIRED   CURRENT   READY   AGE
nginx-778676476b                     1         1         1       3d19h
```