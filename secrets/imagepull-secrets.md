## ImagePullSecret

> **ImagePullSecret Helps kubernetes pods to pull images from Private registries**

> **create a Pod that uses a `Secret` to pull an image from a `private container image registry` or repository.**


## Create a Secret based on existing credentials

### Log in to Docker Hub

```sh
docker login 
```
> **When prompted, enter your Docker ID, and then the credential you want to use (access token, or the password for your Docker ID).**

> **The login process creates or updates a `config.json` file that holds an authorization token**

```sh
cat $HOME/.docker/config.json
```
```json
# The output contains a section similar to this:
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "c3R...zE2"
        }
    }
}
```
### Create a Kubernetes Secret 

> **A Kubernetes cluster uses the Secret of `kubernetes.io/dockerconfigjson` type to authenticate with a container registry to pull a private image.**

> **create from commandline**

```sh
kubectl create secret generic image-reg-cred \
--from-file=.dockerconfigjson=$HOME/.docker/config.json \
--type=kubernetes.io/dockerconfigjson
```

> **Create using a Yaml definition**

1) Convert the $HOME/.docker/config.json to base64 format 

   ```sh
    cat $HOME/.docker/config.json | base64 -w0 ; echo 
   ```

2) Crate the yaml file as below 
   ```yaml 
    apiVersion: v1
    kind: Secret
    metadata:
      name: image-reg-cred
      namespace: default
    type: kubernetes.io/dockerconfigjson
    data:
      .dockerconfigjson: <base-64-encoded-json-here>
   ```

## Create a Secret by providing credentials on the command line

>>> **`Note:` Typing secrets on the command line may store them in your shell history unprotected, and those secrets might also be visible to other users on your PC during the time that kubectl is running.**

```sh
kubectl create secret docker-registry image-registry-cred \
--docker-server=<your-registry-server> \
--docker-username=<your-name> \
--docker-password=<your-pword> \
--docker-email=<your-email>
```
> where:
* **`**your-registry-server` is your Private Docker Registry FQDN. Use https://index.docker.io/v1/ for DockerHub.**
* **`your-name` is your Docker username.**
* **`your-pword` is your Docker password.**
* **`your-email` is your Docker email.**

## Create a Pod that uses your Secret

```yaml
# vi app1.yaml
kind: Deployment 
apiVersion: apps/v1
metadata:
  name: spring-app
  namespace: default 
  #labels: # are optional 
spec:
  replicas: 1 # the total nummbr of pods to be created
  selector:  # is mandatory # which pods to be managed by controller 
    matchLabels: 
      app: spring
  template: # what pod to be created 
    metadata:  # of the pod 
      labels: 
        app: spring
    spec:      # of the pod
      imagePullSecrets:
        - name: image-reg-cred
      containers:
        - name: webapp 
          image: lerndevops/kube:springboot-app
```