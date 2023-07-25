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


##  Understanding RBAC in Kubernetes - Role Based Access Control

> **RBAC** is the implementation of Identity and Access Management (Authorization) in Kubernetes. RBAC uses rbac.authorization.k8s.io API to allow admins to dynamically configure policies through API server. 

> Administrator can use RBAC api to grant granular roles to different users or resources. A **Role** represents a set of permissions that are applied to different resources. 

### RBAC defines 4 top-level types

*   **Role**

      A **Role** can be used to grant access to a resource within a single namespace

*   **RoleBinding**

      A **RoleBinding** grants permission defined in a **Role** to a **User** or a **Set of Users**

*   **ClusterRole**

      A **ClusterRole** is similar to a **Role**, however, a ClusterRole extends across the cluster

*   **ClusterRoleBinding**

      A **ClusterRoleBinding** grants permission defined in a **ClusterRole** at cluster level across namespaces


###    Understanding Subjects

> A **RoleBinding** or **ClusterRoleBinding** will bind the permissions defined in a Role to ***Subjects***. A **Subject** is either a ***single user*** or a ***group*** of users or ***ServiceAccounts.***

 Usernames can be any custom string like "alice", "bob", "alice@example.com".

> Kubernetes clusters have two kinds of Users.

*  Normal Users
*  Kubernetes Managed Service Accounts

> A kubernetes managed subject has a special prefix - **system:**. Any username with the prefix **system:** is a kubernetes managed user and is maintained & created by api server or manually through api calls. It is your administrators responsibility to ensure that no external user should be prefixed with **system:**. This may lead to system instability or crashes. 

> The **system:** prefix can be added to either a user , group, serviceaccount, Role, ClusterRole. Few examples of kubernetes managed roles are -

*   system:kube-scheduler - Allows access to resources required by Scheduler
*   system:kube-controller-manager - Allows access to resources required by controller manager
*   system:kube-proxy - Allows access to the resources required by the kube-proxy

> More information about RBAC is provided at - [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

> While creating client certificates for kubernetes core componenets or admin user, its important to note that that internal user for different components are created by Kubernetes itself. Its the certificate issuers responsibility to ensure that the **Common Name (CN)** field is set correctly as **system:kube-\<COMPONENT_NAME\>**.

## Deafult User Facing Roles 

|***Default ClusterRole*** | ***Default ClusterRoleBinding*** | ***Description*** |
|--------------------------|-----------------------------------|-------------------|
| cluster-admin | system:masters group	| Allows super-user access to perform any action on any resource. When used in a ClusterRoleBinding, it gives full control over every resource in the cluster and in all namespaces. When used in a RoleBinding, it gives full control over every resource in the rolebinding's namespace, including the namespace itself.|
| admin | None | Allows admin access, intended to be granted within a namespace using a RoleBinding. If used in a RoleBinding, allows read/write access to most resources in a namespace, including the ability to create roles and rolebindings within the namespace. It does not allow write access to resource quota or to the namespace itself.|
| edit | None | Allows read/write access to most objects in a namespace. It does not allow viewing or modifying roles or rolebindings. |
| view | None | Allows read-only access to see most objects in a namespace. It does not allow viewing roles or rolebindings. It does not allow viewing secrets, since those are escalating. |