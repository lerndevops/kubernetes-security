## [Open Policy Agent (OPA) - OPA Gatekeeper](https://kubernetes.io/blog/2019/08/06/opa-gatekeeper-policy-and-governance-for-kubernetes/)

> **OPA open source, general purpose `policy enforcement` using high-level `declarative language` for microservices,CI/CD pipelines,API gateways, cloud native and `Kubernetes` etc..**

> **OPA Gatekeeper allows you to `enforce custom policies` on any kubernetes `object at creation time`**

#### For Example 
1) All images must be from approved repositories
2) All ingress hostnames must be globally unique 
3) All pods must have resource limits 
4) All namespaces must have annotations that lists a point-of-contact 

> **`Gatekeeper v3.0` - The admission controller is integrated, `declarative policy support`, validating, mutating admission controll and audit controll** 

> **Implement using Policy Templates which uses Rego, CRDs etc..**

## With OPA Gatekeeper we can 

> **Validating Admission Control**

  * Once all the Gatekeeper components have been installed in your cluster, the API server will trigger the Gatekeeper admission webhook to process the admission request whenever a resource in the cluster is created, updated, or deleted.
  * During the validation process, Gatekeeper acts as a bridge between the API server and OPA. The API server will enforce all policies executed by OPA.

> **Policies and Constraints**

  * a Constraint is a declaration that its author wants a system to meet a given set of requirements. 
  * Each Constraint is written with Rego, a declarative query language used by OPA to enumerate instances of data that violate the expected state of the system. 
  * All Constraints are evaluated as a logical AND. If one Constraint is not satisfied, then the whole request is rejected.
  * Before defining a Constraint, you need to create a Constraint Template that allows people to declare new Constraints
  
> **Audit**

  * The audit functionality enables periodic evaluations of replicated resources against the Constraints enforced in the cluster to detect pre-existing misconfigurations. 
  * Gatekeeper stores audit results as violations listed in the status field of the relevant Constraint.

> **Data Replication**

  * Audit requires replication of Kubernetes resources into OPA before they can be evaluated against the enforced Constraints. 
  * Data replication is also required by Constraints that need access to objects in the cluster other than the object under evaluation. 
  * For example, a Constraint that enforces uniqueness of ingress hostname must have access to all other ingresses in the cluster.

## OPA Gatekeeper Implementation 

1) **Install Gatekeeper**

> [Install OPA Gatekeeper in kubernetes cluster](https://open-policy-agent.github.io/gatekeeper/website/docs/install/)

2) **Create Constraint Template (uses Rego)**
3) **Create Constraint resource** 
4) **Create Deployment and Test Contstraint** 

## [OPA Gatekeeper Library](https://open-policy-agent.github.io/gatekeeper-library/website/)

> **A community-owned library of policies for the OPA Gatekeeper project.**

### Validation and Mutation

> **The library consists of two main components: `Validation` and `Mutation`.**

>> **`Validation:` Gatekeeper can validate resources in the cluster against Gatekeeper validation policies, such as these defined in the library.**
  * **The policies are defined as `ConstraintTemplates` and `Constraints`.**
  * **`ConstraintTemplates` can be applied directly to a cluster and then `Constraints` can be applied to customize policy to fit your specific needs.**

>> **`Mutation:` Gatekeeper can mutate resources in the cluster against the Gatekeeper mutation policies, such as these defined in the library. Mutation policies are only examples, they should be customized to meet your needs before being applied.**