## Step1: Enbale Validation Admission Webhook 
```
vi /etc/kubernetes/manifests/kube-apiserver.yaml

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision,ValidatingAdmissionWebhook,MutatingAdmissionWebhook
```

## Step2: Genereate SSL Certs required to Deploy Webhook Server 

> **Admission Webhooks need to be on SSL**

**`wget https://raw.githubusercontent.com/lerndevops/kubernetes-security/main/admission-controllers/mutating-admission-webhook/gencerts.sh -P $HOME`**

**`bash $HOME/gencerts.sh`**

**`ls -l $HOME/ssl`**

## Step3: Create secret with generated SSL Certs 

> **this is requred to start webhook server**

**`kubectl create secret tls mutating-webhook-tls --cert $HOME/ssl/server.crt --key $HOME/ssl/server.key`**

## Step4: Deploy the Webhook Server 

**`kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/mutating-admission-webhook/mutating-webhook-server.yaml`**

## Step5: Deploy the Webhook Config 

#### Download the file to local server 

**`wget https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/mutating-admission-webhook/mutating-webhook-config.yaml -P $HOME`**

#### convert the ca.crt created in Step2 in to base64 format 

**`cat $HOME/ssl/ca.crt | base64 | tr -d "\n"`**

#### copy the output & append in the mutating-webhook-config.yaml 

**`vi $HOME/mutating-webhook-config.yaml`**

**`modify below section in file`**

**`caBundle: <PLACE-YOUR-WEBHOOK-SERVER_CA-HERE><MUST BE base64 encoded data>`**

#### deploy the webhook configuration 

**`kubectl apply -f $HOME/mutating-webhook-config.yaml`**

## Test the Webhook Working 

> **Note that webhook server/config deployed will update the labels as project: chandrayan for every deployment created**

#### deployment 

**`kubectl apply -f https://github.com/lerndevops/kubernetes-security/raw/main/admission-controllers/mutating-admission-webhook/test-webhook.yaml`**

#### validate Output

**`kubectl get deployment mutation-test-deployment -o yaml | grep -v apiVersion | egrep -A 2 labels`**
```
root@test-vm:~/# kubectl get deployment mutation-test-deployment -o yaml | grep -v apiVersion | egrep -A 2 labels
  labels:
    app: mutation
    project: chandrayan
```