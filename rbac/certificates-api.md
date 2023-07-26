## Setting up RBAC with client certificates

> Kubernetes does not have API Objects for User Accounts. Of the available ways to manage authentication. we will use ***OpenSSL certificates*** for their simplicity. 

## step1: create a private/public keypair 

> **Create a directory to place certificates**

```
mkdir -p /home/certs
cd /home/certs
```

> **Create a private key for your user. In this example, we will name the file user007.key:**

`openssl genrsa -out user007.key 2048 ; ls -l`

```
root@mnode:~# openssl genrsa -out user007.key 2048 ; ls -l 
total 20
-rw-------  1 root root 1704 Jul 25 09:15 user007.key

```

## step2: create a CSR

> **Create a certificate sign request `user007.csr` using the private key we just created (user007.key in this example).** 

> **Make sure you specify your username and group in the -subj section (CN is for the username and O for the group).**

   `openssl req -new -key user007.key -out user007.csr -subj "/CN=user007/O=devops"`


## step3: Send CSR to API Server using Certificates API & get it approved with kubernetes CA 

##### use the below file to send the CSR to API, ensure to convert the CSR file to base64 encoding before palcing in to file 
```
# convert csr to base64  

    cat user007.csr | base64 | tr -d "\n"

vi user007-csr.yaml 

kind: CertificateSigningRequest
apiVersion: certificates.k8s.io/v1
metadata:
   name: user007
spec:
  signerName: kubernetes.io/kube-apiserver-client
  #expirationSeconds: 86400
  #groups:
  request: <place the CSR content in base64 format here>
  usages:
   - client auth
   #- digital signature
   #- key encipherment
   #- server auth
```

> **kubectl apply -f user007-csr.yml**

> **kubectl get csr**
```
root@test-vm:~# kubectl get csr
NAME      AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
user007   25s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Pending
```

> **kubectl certificate approve user007**

```
root@test-vm:~# kubectl certificate approve user007
certificatesigningrequest.certificates.k8s.io/user007 approved

root@test-vm:~# kubectl get csr
NAME      AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
user007   96s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Approved,Issued
```

## step4: obtain the issued certificate from API 

> **kubectl get csr user007 -o json** 

> **kubectl get csr user007 -o jsonpath="{.status.certificate}" | base64 --decode > user007.crt**

## step5: Create kubeconfig file using kubectl 

> ***Add cluster details to configuration file:***
 
  `kubectl config --kubeconfig=user007.conf set-cluster dev --server=https://<PLACE-APIServer-IP>:6443 --certificate-authority=/etc/kubernetes/pki/ca.crt`

> ***Add user details to your configuration file:***
 
  `kubectl config --kubeconfig=user007.conf set-credentials user007 --client-certificate=/home/certs/user007.crt --client-key=/home/certs/user007.key`

> ***Add context details to your configuration file:***
 
  `kubectl config --kubeconfig=user007.conf set-context dev --cluster=dev --namespace=dev --user=user007`
  
> ***Set dev context for use:***

  `kubectl config --kubeconfig=user007.conf use-context dev`
  
> ***validate Aceess to API Server:***

  `kubectl --kubeconfig /home/certs/user007.conf version --short`

``` 
  root@kube-master:/home/certs# kubectl --kubeconfig /home/certs/user007.conf version --short
	Client Version: v1.27.0
	Server Version: v1.27.0
```

## step6: Providing the Authorization to user007

#### define a Role/Rolebinding -- what can be done by user007

* vi rbac-user007.yaml 

```
# Role Definition starts here 
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
# Rolebinding definition Starts here 
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: user007-access
  namespace: dev
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: readonly
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: user007
```

> **save, close & apply the manifest file**

> **kubectl apply -f rbac-user007.yaml**


## validate able to list deployments, pods replicasets 

```
root@kube-master:/home/certs# kubectl --kubeconfig user007.conf get deployment --namespace dev
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
nginx                     1/1     1            1           3d19h
```

```
root@kube-master:/home/user007/# kubectl --kubeconfig user007.conf get pods --namespace dev
NAME                                 DESIRED   CURRENT   READY   AGE
nginx-778676476b                     1         1         1       3d19h
```