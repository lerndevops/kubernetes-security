## Secrets

> **A Secret is an object that contains a small amount of sensitive data such as a `password,` a `token,` or a `key`.**

> **Such information might otherwise be put in a Pod specification or in a container image.**

> **`Using a Secret means that you don't need to include confidential data in your application code.`**

> **Because Secrets can be created independently of the Pods that use them, there is less risk of the Secret (and its data) being exposed during the workflow of creating, viewing, and editing Pods.**

> Kubernetes, and applications that run in your cluster, can also take additional precautions with Secrets, such as avoiding writing secret data to nonvolatile storage.

> **There are multiple ways of creating secrets in Kubernetes**

1) **Creating from txt files from CLI using kubectl create**
   ```
   kubectl create secret generic tomcat-passwd --from-file =./username.txt --from-file =./password.txt
   ```

2) **Creating using manifest yaml file with `kind: Secret` resource type.**
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: tomcat-pass
   type: Opaque
   data:
     password: <User Password - must be base64 encoded>
     username: <User Name - must be base64 encoded> 
   ```

How to Inject Secrets into the pod
---
> **Once we have created the secrets, it can be consumed in a pod as**

1) **Volume**
2) **Environment Variable**

### As Volume data 

> **inside your `pod.spec` filed use volumes**

```yaml 
spec:
  volumes:
   - name: secretstest
     secret:
       secretName: tomcat-pass
  containers:
   - image: tomcat:7.0
     name: awebserver
     volumeMounts:
      - mountPath: "/tmp/mysec"
        name: secretstest
```

### As Environment Variable 

> **inside your `pod.spec.containers` filed use volumes**

```yaml
## getting the data from a specific key & storing into a key defined 
containers:
  name: cont1
  image: nginx
  env:
   - name: SECRET_USERNAME # key
     valueFrom:
      secretKeyRef:
        name: tomcat-pass
        key: username # value from key from secret created 
```

OR

```yaml 
## getting all the data from the secret & register into environment of container
containers:
  name: cont1
  image: nginx
  envFrom: 
   - secretRef: 
       name: tomcat-pass
```

## Types of Secret {#secret-types}

| Built-in Type                         | Usage                                   |
| ------------------------------------- | --------------------------------------- |
| `Opaque`                              | arbitrary user-defined data             |
| `kubernetes.io/service-account-token` | ServiceAccount token                    |
| `kubernetes.io/dockercfg`             | serialized `~/.dockercfg` file          |
| `kubernetes.io/dockerconfigjson`      | serialized `~/.docker/config.json` file |
| `kubernetes.io/basic-auth`            | credentials for basic authentication    |
| `kubernetes.io/ssh-auth`              | credentials for SSH authentication      |
| `kubernetes.io/tls`                   | data for a TLS client or server         |
| `bootstrap.kubernetes.io/token`       | bootstrap token data                    |



### [Distribute Credentials Securely Using Secrets](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)

### [MORE INFO](https://kubernetes.io/docs/concepts/configuration/secret/)