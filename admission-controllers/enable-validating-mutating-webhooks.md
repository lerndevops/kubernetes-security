## dynamic Admission Webhooks

> **Admission webhooks are HTTP callbacks that receive admission requests and do something with them. You can define two types of admission webhooks,**

1) [validating admission webhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#validatingadmissionwebhook) 
2) [mutating admission webhook](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook)


> **Admission webhooks are essentially part of the cluster control-plane.** 

> **You should write and deploy them with great caution. Please read the [user guides](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#write-an-admission-webhook-server) for instructions if you intend to write/deploy production-grade admission webhooks**

> **these webhooks are not enabled by default**

## Enable Admission Webhooks
```
vi /etc/kubernetes/manifests/kube-apiserver.yaml

    - --enable-admission-plugins=NodeRestriction,NamespaceAutoProvision,ValidatingAdmissionWebhook,MutatingAdmissionWebhook
```

