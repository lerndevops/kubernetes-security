# Kubernetes Admission Controllers

## What is Kubernetes Admission Controller?
1) **An admission controller is a `piece of code that intercepts requests to the Kubernetes API server prior to persistence of the object, but after the request is authenticated and authorized.`**
2) **Act as gatekeeper and process kubernetes API Server requests before persist in ETCD**
3) **Admission Controllers are compiled with kubernetes API Server binaries**

![adminssion-controller](https://github.com/lerndevops/kubernetes-security/blob/main/img/admission-controller.png)

4) **`Admission Controller` enables DevOps and Security personnel to enforce deployment requirements and restrictions in the cluster upon every workload start and any configuration change.**

## Intent Based API 

> **kubernetes API Server is an intent based API Server**

> **intent based api? Intent is an description of some intended operation. When some Intent is executed, it performs modification/validation before the actual operation.**

> **Intent provide loose coupling between modules that may request an operation and modules that can perform it. They can be easily serialized, so they are suitable for distributed heterogenous systems.**

> **in Kubernetes a USER can perform set of `actions such as "get,list,create,delete,modify,describe"`, on various `API resources such as "pods,deployments,services etc..."`** 

> **once a USER performed an Action using the delcarative definition(manifest file), the intent API can modify/validate the declaravtive definition before it persist in cluster**

> **with RBAC provided in kubernetes we can control only USER Actions such as "`get,list,create,delete,modify,describe`"** 

## WHY Adminssion Controllers? 

1) **RBAC handles the access controll but its limited control because of intent based API.**
2) **Improved Security**
     * Mandating a resonable security baseline (allow only non root, non priviliged)
     * Allow from specific image repositories & deny from unknown repositories 
     * Reject a deployment if doesn't meet security standards (such as must define resource limits)
3) **Easy Governance** 
     * enforce labels, annotations, resource limits etc..
4) **Preventive Capabilities**
     * As opposed to audit log analysis tools and configuration scanning, admission controllers not only detect problems but also prevent them from entering into a cluster.
5) **Highly customizable**
     * Unlike built-in Kubernetes security mechanisms, dynamic admission controllers are adjustable to many different user-specific scenarios and environments
     * There are many open-source and commercial admission controller implementations that customers can choose from and enforce their special constraints.
4) **Configuration & Deployment**
     * prevent obvious misconfigurations 
     * detecting and fixing images deployed without semantic tags 
     * ensureing resonable labels are added to pods 
     * adding resource limits or validating resource limits 
     * enforce not using latest tag for production 

## Admission Controllers

### `Static Admission Controllers` 
> **Static admission controllers are admission controllers that are built-in and provided by Kubernetes itself. Not all of them are enabled by default**

### `Dynamic Admission Controllers`
> **User Configured controllers that can modify or reject API requests based on custom logic**

> **Dynamic admission controllers can be of 3 types** 
     * ImagePolicyWebhook         -- Controls admission for a particular container image
     * MutatingAdmissionWEbhook.  -- Modifies the object received before it persist 
     * ValidatingAdmissionWebhook -- Accepts or Rejects admission requests validation

> **A Webhook is a standard interface that listens to API Server incoming requests and responds with the results**

> **To implement dynamic admission controllers, you must configure the API server first with a change to the `--enable-admission-plugins`.**

```
--enable-admission-plugins=...,MutatingAdmissionWebhook,ValidatingAdmissionWebhook
```
#### [Built-in-Admission-Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

![Built-in-Admission-Controllers](https://github.com/lerndevops/kubernetes-security/blob/main/img/built-in-admission-controllers.png)

### `Admission Controller Phases`

1) **The admission Controller process proceeds in 2 phases**
    * 1st Phase -- **`mutating`** admission controller will run 
    * 2nd phase -- **`validating`** admission Controllers will run 
2) **if any controller phase rejects, entire request will be rejected with error** 
3) **Admission Controller **`limit`** requests to **`create,delete,modify`** objects only** 
4) **No limitation on `Read` Objects like `get`**  

![Admission-Controllers-phases](https://github.com/lerndevops/kubernetes-security/blob/main/img/admission-controller-phases.png)







### Benefits of Kubernetes Admission Controller

#### Extended Security Controls
#### Company-Wide Guardrails
#### Preventive Capabilities
#### Highly customizable