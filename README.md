# Kubernetes Secutiry 

## Controlling access to the Kubernetes API

> As Kubernetes is entirely API driven, controlling and limiting who can access the cluster and what actions they are allowed to perform is the first line of defense.

### Use Transport Layer Security (TLS/SSL) for all API traffic

> Kubernetes expects that all API communication in the cluster is encrypted by default with TLS, and the majority of installation methods will allow the necessary certificates to be created and distributed to the cluster components. 


### API Authentication

> Choose an authentication mechanism for the API servers to use that matches the common access patterns when you install a cluster. For instance, small single user clusters may wish to use a simple certificate or static Bearer token approach. Larger clusters may wish to integrate an existing OIDC or LDAP server that allow users to be subdivided into groups.

> All API clients must be authenticated, even those that are part of the infrastructure like nodes, proxies, the scheduler, and volume plugins. These clients are typically service accounts or use x509 client certificates, and they are created automatically at cluster startup or are setup as part of the cluster installation.

[More Info about Authentication here](https://kubernetes.io/docs/reference/access-authn-authz/authentication/) 


### API Authorization

> Once authenticated, every API call is also expected to pass an authorization check. Kubernetes ships an integrated ***Role-Based Access Control (RBAC)*** component that matches an incoming user or group to a set of permissions bundled into roles. 

> These permissions combine verbs (get, create, delete) with resources (pods, services, nodes) and can be namespace or cluster scoped.

[More Info about Authorization here](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)