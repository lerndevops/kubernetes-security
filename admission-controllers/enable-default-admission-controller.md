## Enable Default Admission Controllers

> **there are admission controllers that are built-in and provided by Kubernetes. `And Not all of them are enabled by default`**

> **Lets Enable a couple of them & see the Behaviour**

## Example 1: NamespaceAutoProvision Admission Controller

> This admission controller examines all incoming requests on namespaced resources and checks if the referenced namespace does exist. It creates a namespace if it cannot be found. This admission controller is useful in deployments that do not want to restrict creation of a namespace prior to its usage

##### **`Step1: Create a Pod in a Namespace "demo"`**
```
kubectl run dmeopod --image=nginx --namespace demo 
```
```       
Note: we can see the Error as Below, as the "demo" namespace doesn't exits 
```
```
root@test-vm:~# kubectl run dmeopod --image=nginx --namespace demo
Error from server (NotFound): namespaces "demo" not found

root@test-vm:~# kubectl get namespace demo
Error from server (NotFound): namespaces "demo" not found
```
##### **`Step2: Enable the admissin controller in api-server config`**
```
vi /etc/kubernetes/manifests/kube-apiserver.yaml

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision
```

  * **Note: after modifying kube-apiserver as above, wait for some until the api-server restart successfully**

##### **`Step3: Validate by Creating a Pod`** 
```
root@test-vm:~# kubectl get ns demo
Error from server (NotFound): namespaces "demo" not found
```
```
root@test-vm:~# kubectl run demopod --image=nginx --namespace demo
pod/demopod created
```
```
root@test-vm:~# kubectl get ns demo
NAME   STATUS   AGE
demo   Active   4s
```
```
root@test-vm:~# kubectl get pod demopod --namespace demo
NAME      READY   STATUS    RESTARTS   AGE
demopod   1/1     Running   0          26s
```