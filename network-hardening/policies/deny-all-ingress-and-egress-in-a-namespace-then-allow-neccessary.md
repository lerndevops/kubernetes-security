## Deny All Ingress & Egress Policy
```yaml
## vi deny-all-traffic-default-ns.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress-egress-in-default-ns
  namespace: default
spec:
  podSelector: {}
  policyTypes:
   - Ingress
   - Egress
```
```sh
kubectl apply -f deny-all-traffic-default-ns.yaml
```
Deploy Application & test 
---
## Setp1: Deploy Java Application & MongoDB Pods 

```
kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/network-hardening/policies/app.yaml
```

## Step2: access the Spring Java Application from outside Cluster using NodePort

```sh
kubectl get services springboot-app-svc
```
>> **use the NodPort to access the springboot java in the browser** 

>> **you can observe the application not loading, because all Ingress is traffic in default namespace is bloked with network policy we applied above**

## Step3: Now lets allow the request / traffic to springa app

```yaml
# vi allow-ingress-to-springapp-from-all.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-springapp-from-all
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
   - Ingress
  ingress:
   - from:
      - ipBlock:
          cidr: 0.0.0.0/0
      #- namespaceSelecotr:
      #- podSelecotr:
     ports:
      - protocol: TCP
        port: 8080
```
```sh
kubectl apply -f allow-ingress-to-springapp-from-all.yaml
```
>> **use the NodPort to access the springboot java in the browser** 

>> **you can observe the application loading, because all Ingress is traffic now allowed to spring app in default namespace**

>> **also, try entering values in `First Name`, `Last Name` and `Email` then Click on `Submit`**

>> **you will be seeing an error again, As the `Ingress(incoming) to mongo db pods is still not allowed`**

## Step4: Now Lets allow the Ingress to Mongo DB Pod 

```yaml
# vi allow-ingress-to-mongodb-from-spring-app-pods-only.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-mongodb-from-spring-app-pods-only
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: mongodb
  policyTypes:
   - Ingress
  ingress:
   - from:
      #- ipBlock:
      #    cidr: 0.0.0.0/0
      #- namespaceSelecotr:
      - podSelector:
          matchLabels:
            app: myapp
     ports:
      - protocol: TCP
        port: 27017
```
```sh
kubectl apply -f allow-ingress-to-mongodb-from-spring-app-pods-only.yaml
```
>> **Now, again try entering values in `First Name`, `Last Name` and `Email` then Click on `Submit`, from the browser**

>> **you will again see the error, As the Ingress to mongo db pods allowed,**

>> **`but Egress(outgoing) from all pods including springapp/mongodb pods is still blocked`**

## Step5: Now lets allow Egress(outgoing) traffic from spring java app to mongodb  

```yaml
# vi allow-egress-from-spring-app-to-mongodb-pods-only.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-from-spring-app-to-mongodb-pods-only
  namespace: default
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
   - Ingress
  egress:
   - to:
      #- ipBlock:
      #    cidr: 0.0.0.0/0
      #- namespaceSelecotr:
      - podSelector:
          matchLabels:
            app: mongodb
     ports:
      - protocol: TCP
        port: 27017
```
```sh
kubectl apply -f allow-egress-from-spring-app-to-mongodb-pods-only.yaml
```

> **This should allow the egress traffic from Spring java App to mongodb pods**

> **But if you try to submit the data to DB it will not respond, this is because our db url is using "mongo" name to reach db pods and we can see ip are able to connect but name resolution will fail(DNS Lookup fails)**

> **as we restricted all egress traffic all pods can not reach core dns pods in kube-system namespace, hence name resolution fails**

>> ### Exec into one of the app pods to validate
```sh 
kubectl exec -it springboot-app-6487b976bb-qqr2r -- /bin/sh
```

```
# Exec into one of the app pods to validate

root@test-vm:~/netpol# kubectl exec -it springboot-app-6487b976bb-qqr2r -- /bin/sh

/opt/app # curl 192.168.227.80:27017
It looks like you are trying to access MongoDB over HTTP on the native driver port.

/opt/app # curl 10.105.188.12:27017
It looks like you are trying to access MongoDB over HTTP on the native driver port.

/opt/app # curl mongo:27017
curl: (6) Could not resolve host: mongo
```

## Step 6: Lets the Change the default deny all policy as below 
```yaml
## vi deny-all-traffic-default-ns.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress-egress-in-default-ns
  namespace: default
spec:
  podSelector: {}
  policyTypes:
   - Ingress
   - Egress
  egress:
   - to:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: kube-system
      - podSelector:
          matchLabels:
            k8s-app: kube-dns
     ports:
      - protocol: TCP
        port: 53
      - protocol: UDP
        port: 53
```
```sh
kubectl apply -f deny-all-traffic-default-ns.yaml
```
> **Now, we should see all working**