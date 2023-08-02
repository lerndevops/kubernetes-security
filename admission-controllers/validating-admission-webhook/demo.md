## Step1: Enbale Validation Admission Webhook 
```
vi /etc/kubernetes/manifests/kube-apiserver.yaml

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision,ValidatingAdmissionWebhook
```

## Step2: Genereate SSL Certs required to Deploy Webhook Server 

> **Admission Webhooks need to be on SSL**

`wget https://raw.githubusercontent.com/lerndevops/kubernetes-security/main/admission-controllers/validating-admission-webhook/gencerts.sh -P $HOME`

`bash $HOME/gencerts.sh`

`ls -l $HOME/ssl`

## Step3: Create secret with generated SSL Certs 

> **this is requred to start webhook server**

`kubectl create secret tls validating-webhook-tls --cert $HOME/ssl/server.crt --key $HOME/ssl/server.key`

## Step4: Deploy the Webhook Server 

`kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/validating-admission-webhook/validating-webhook-server.yaml`

## Step5: Deploy the Webhook Config 

#### Download the file to local server 

`wget https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/validating-admission-webhook/validating-webhook-config.yaml -P $HOME`

#### convert the ca.crt created in Step2 in to base64 format 

`cat $HOME/ssl/ca.crt | base64 | tr -d "\n"`

#### copy the output & append in the validating-webhook-config.yaml 

`vi $HOME/validating-webhook-config.yaml`

`modify below section in file` 

`caBundle: <PLACE-YOUR-WEBHOOK-SERVER_CA-HERE><MUST BE base64 encoded data>`

#### deploy the webhook configuration 

`kubectl apply -f $HOME/validating-webhook-config.yaml`

## Test the Webhook Working 

> **Note that webhook server/config deployed will mandate that every deployment has an annotation with a key "author"**

> **if no annotation with "author" in deployment definition it will be rejected**

#### deployment 

`kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/validating-admission-webhook/test-webhook.yaml`

#### Expected Output
```
root@test-vm:~# kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/validating-admission-webhook/test-webhook.yaml

deployment.apps/deployment-with-annotation created

Error from server: error when creating "https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/validating-admission-webhook/test-webhook.yaml": admission webhook "validating-webhook-demo.default.svc" denied the request: Not allowed without author annotations
```