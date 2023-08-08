## what is Service Mesh? 

> **A service mesh is an `infrastructure layer` that allows you to manage communication between your application’s microservices. As more developers work with microservices, service meshes have evolved to make that work easier and more effective by consolidating common management and administrative tasks in a distributed setup.**

### Why Services Meshes?

> **Service meshes are designed to address some of the challenges inherent to distributed application architectures.**

> **Taking a microservice approach to application architecture involves breaking your application into a collection of loosely-coupled services.**

> **A microservice design avoids some of these issues. Instead of having a large, centralized application codebase, you have a collection of discretely managed services that represent a feature of your application. Benefits of a microservice approach include:**

     1) Greater agility in development and deployment, since teams can work on and deploy different application features independently.
     2) Better options for CI/CD, since individual microservices can be tested and redeployed independently.
     3) More options for languages and tools. Developers can use the best tools for the tasks at hand, rather than being restricted to a given language or toolset.
     4) Ease in scaling.
     5) Improvements in uptime, user experience, and stability.

> **At the same time, microservices have also created challenges:**

    1) Distributed systems require different ways of thinking about latency, routing, asynchronous workflows, and failures.
    2) Microservice setups cannot necessarily meet the same requirements for data consistency as monolithic setups.
    3) Greater levels of distribution necessitate more complex operational designs, particularly when it comes to service-to-service communication.
    4) Distribution of services increases the surface area for security vulnerabilities.

> **`Service meshes are designed to address these issues by offering coordinated and granular control over how services communicate`**

> ***Though it is possible to do these tasks natively with container orchestrators like Kubernetes, this approach involves a greater amount of up-front decision-making and administration when compared to what service mesh solutions like [Istio](https://istio.io/) and [Linkerd](https://linkerd.io/) offer out of the box.***

> ***In this sense, service meshes can streamline and simplify the process of working with common components in a microservice architecture. In some cases they can even extend the functionality of these components.***

## What does a service mesh provide?

#### **Not all of the service meshes out there have all of these capabilities, but in general, these are the features you gain with service mesh:**

1) Service Discovery 
2) Load Balancing 
3) Communication Resiliency (retries, timeouts, circuit-breaking, rate limiting)
4) Security (end-to-end encryption, authorization policies)
5) Observability (Layer 7 metrics, tracing, alerting)
6) Routing Control (traffic shifting and mirroring)
7) API (programmable interface, Kubernetes Custom Resource Definitions (CRD))


## What are the different service mesh implementations?

#### [Istio](https://istio.io/latest/about/service-mesh/)
>> **Istio has a Go control plane and uses Envoy as a proxy data plane. It functions as a complex system that does many things, like tracing, logging, TLS, authentication, etc. A drawback is the resource-hungry control plane, says Stefan. The more services you have the more resources you need to run them on Istio.**

#### [AWS App Mesh](https://aws.amazon.com/app-mesh/)

>> **This is a managed control plane that also uses an Envoy proxy for its data plane. You don’t have to run it yourself on your cluster. It works very similar to Istio. Since it’s fairly new and it still lacks many of the features that Istio has. For example it doesn’t include mTLS or traffic policies.**

#### [Linkerd v2](https://linkerd.io/2.13/overview/)

>> **Similar to Istio, Linkerd v2 also has a Go control plane and a Linkerd proxy data plane that is written in Rust.** 

>> **Linkerd has some distributed tracing capabilities and just recently implemented traffic shifting. The current 2.4 release implements the Service Mesh Interface (SMI) traffic split API, that makes it possible to automate Canary deployments and other progressive delivery strategies with Linkerd and Flagger.**

#### [Consul Connect](https://developer.hashicorp.com/consul/tutorials/get-started-vms/virtual-machine-gs-service-discovery)
>> **This uses a Consul control plane and requires the data plane to be managed inside an app. It does not implement Layer 7 traffic management nor does it support Kubernetes CRDs.**


