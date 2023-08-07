## TLS secrets
> **Kubernetes provides a builtin Secret type kubernetes.io/tls for storing a certificate and its associated key that are typically used for TLS.**

> **One common use for TLS secrets is to configure encryption in transit for an Ingress** 

> **we can also use it with other resources or directly in your workload. 

> **When using this type of Secret, the `tls.key` and the `tls.crt` key must be provided in the data (or stringData) field of the Secret configuration, although the API server doesn't actually validate the values for each key.**

### covnert your tls.key and tls.crt file to base64 encoding string 
```sh
cat /path/to/tls.key | base64 -w0 ; echo 
```
```sh
cat /path/to/tls.crt | base64 -w0 ; echo 
```
```yaml 
apiVersion: v1
kind: Secret
metadata:
  name: secret-tls
type: kubernetes.io/tls
data:
  # the data is abbreviated in this example
  tls.crt: MIIC2DCCAcCgAwIBAgIBATANBgkqh ...    
  tls.key: MIIEpgIBAAKCAQEA7yn3bRHQ5FHMQ ...  

```
> **The TLS Secret type is provided for user's convenience.**

> **You can create an `Opaque` for credentials used for TLS server and/or client. However, using the builtin Secret type helps ensure the consistency of Secret format in your project; the API server does verify if the required keys are provided in a Secret configuration.**

### When creating a TLS Secret using `kubectl`, you can use the `tls` subcommand as below:
```sh
kubectl create secret tls tls-secret \
--cert=path/to/cert/file \
--key=path/to/key/file
```

### [You-can-find-More-Info-here](https://kubernetes.io/docs/concepts/configuration/secret/#tls-secrets)