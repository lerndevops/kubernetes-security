## Kubernetes Admission Controllers

### What is Kubernetes Admission Controller?
1) **An admission controller is a `piece of code that intercepts requests to the Kubernetes API server prior to persistence of the object, but after the request is authenticated and authorized.`**
2) **Act as gatekeeper and process kubernetes API Server requests before persist in ETCD**
3) **Admission Controllers are compiled with kubernetes API Server binaries**

![adminssion-controller](https://github.com/lerndevops/kubernetes-security/blob/main/img/admission-controller.png)

4) **`Admission Controller` enables DevOps and Security personnel to enforce deployment requirements and restrictions in the cluster upon every workload start and any configuration change.**

> **`An example of admission control` can be a policy that prevents privileged pods from execution in a cluster.**
* **Running a pod in privileged mode means that the pod has access to the host’s resources and kernel capabilities. A hacker will be extra motivated to exploit this pod and access the host’s resources, which causes a significant amount of damage to the cluster.**

### Admission Controller Phases
1) **The admission Controller process proceeds in 2 phases**
    * 1st Phase -- **`mutating`** admission controller will run 
    * 2nd phase -- **`validating`** admission Controllers will run 
2) **if any controller phase rejects, entire request will be rejected with error** 
3) **Admission Controller **`limit`** requests to **`create,delete,modify`** objects only** 
4) **No limitation on `Read` Objects like `get`**  

![Built-in-Admission-Controllers](https://github.com/lerndevops/kubernetes-security/blob/main/img/admission-controller-phases.png)

### Build In Admission Controllers

#### [Built-in-Admission-Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/)

![Built-in-Admission-Controllers](https://github.com/lerndevops/kubernetes-security/blob/main/img/built-in-admission-controllers.png)

### Benefits of Kubernetes Admission Controller

#### Extended Security Controls
#### Company-Wide Guardrails
#### Preventive Capabilities
#### Highly customizable