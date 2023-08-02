## Step1: Enbale Validation Admission Webhook 
```
vi /etc/kubernetes/manifests/kube-apiserver.yaml

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision,ValidatingAdmissionWebhook
```

## Step2: deploy the webhook server 
``