## OIDC: Simplifying Identity Management

### Understanding OIDC

> OpenID Connect (OIDC) is an open standard authentication protocol built on top of the OAuth 2.0 framework. 

> It provides a secure and flexible way to authenticate and authorize users within applications and systems. 

>OIDC introduces identity-related features to OAuth 2.0, making it ideal for authenticating users in Kubernetes clusters.

### Benefits of OIDC for Kubernetes Authentication

> **Using OIDC for Kubernetes authentication offers several benefits, including:**

1) **`Centralized Identity Management:`** OIDC allows you to leverage an existing identity provider (IdP) infrastructure for user authentication. This enables centralized management of user identities, reducing administrative overhead and ensuring consistency across multiple applications and platforms.

2) **`Single Sign-On (SSO) Experience:`** By integrating Kubernetes with an OIDC provider, users can enjoy a seamless single sign-on experience. Once authenticated, users can access multiple Kubernetes clusters and applications without the need to re-enter their credentials, streamlining the user experience.

3) **`Enhanced Security:`** OIDC leverages industry-standard security mechanisms, such as JSON Web Tokens (JWT), for transmitting identity information. This ensures secure communication between the OIDC provider and Kubernetes, mitigating the risk of unauthorized access or data breaches.

### Best Practices for Kubernetes OIDC Authentication

> **To ensure a secure and efficient OIDC authentication implementation in Kubernetes, consider the following best practices:**

1) **`Use HTTPS:`** Always secure the communication between the OIDC provider, Kubernetes API server, and the client applications by enabling HTTPS.

2) **`Enable RBAC:`** Implement Role-Based Access Control (RBAC) to enforce fine-grained authorization policies based on user groups or claims. RBAC allows you to control which resources and actions users can access within the Kubernetes cluster.

3) **`Token Validation and Rotation:`** Validate the integrity and authenticity of the JWT tokens received from the OIDC provider. Implement token rotation mechanisms to ensure the security of long-lived tokens.

4) **`Monitor and Audit:`** Set up monitoring and auditing mechanisms to track and log authentication events within the Kubernetes cluster. This helps detect and respond to any potential security incidents.

### Setting up Kubernetes Authentication with OIDC

> **To enable OIDC authentication in Kubernetes, you need to follow these general steps:**

1) **`Configure an OIDC Provider:`** First, you need to set up an OIDC provider, which could be an open-source solution like Keycloak or a cloud-based service like Okta or Azure Active Directory. Configure the provider with the necessary client credentials, scopes, and redirect URIs.
  * **Ex: keycloak or okta**
    ```
    Create a new realm in Keycloak or use an existing one.
    Create a new client in the realm for Kubernetes. Set the client protocol to “openid-connect” and the Access Type to “confidential”.
    Configure the Valid Redirect URIs with the URL of your Kubernetes API server’s OAuth2 callback endpoint (e.g., https://kubernetes/api/v1/auth/callback).
    Note down the Client ID and Client Secret of the created client.
    ```  

2) **`Configure Kubernetes API Server:`** Update the Kubernetes API server configuration to enable OIDC authentication. This involves specifying the OIDC provider’s endpoint, client ID, and client secret. Additionally, you can define groups or claims that map to Kubernetes RBAC roles, enabling fine-grained access control.

    ```
    1. Open the Kubernetes API server configuration file (e.g., /etc/kubernetes/manifests/kube-apiserver.yaml) on the master node.

    2. Add the following arguments to the kube-apiserver container spec:
    ```
    ```
        - --oidc-issuer-url=https://keycloak/auth/realms/<realm>
        - --oidc-client-id=<client-id>
        - --oidc-username-claim=preferred_username
        - --oidc-groups-claim=groups
        - --oidc-ca-file=/etc/kubernetes/pki/keycloak-ca.crt
        - --oidc-username-prefix=oidc:
    ```
    ```
    Replace <realm> with the name of your Keycloak realm and <client-id> with the Client ID of the Kubernetes client you created in Keycloak. Make sure to provide the correct path to the OIDC CA file, which contains the certificate of the Keycloak instance.

    3. Save the configuration file and let Kubernetes automatically apply the changes.
    ```
3) **`Configure Kubernetes Cluster Roles:`** Define Kubernetes cluster roles and role bindings based on the OIDC provider’s group or claim mappings. This ensures that users authenticated via OIDC are granted the appropriate permissions within the cluster.

  * **1) Create a ClusterRole in Kubernetes that maps to Keycloak groups. For example:**
    ```
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: keycloak-admins
    rules:
      - apiGroups: [""]
        resources: ["pods", "services"]
        verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
    ```
  * **2) Create a ClusterRoleBinding to assign the ClusterRole to specific Keycloak groups. For example:**
    ```
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: keycloak-admins-binding
    subjects:
      - kind: Group
        name: keycloak-admins
    roleRef:
      kind: ClusterRole
      name: keycloak-admins
      apiGroup: rbac.authorization.k8s.io
    ```
    ```
    Replace keycloak-admins with the name of the Keycloak group you want to map to the ClusterRole.
    ```

4) **`Test and Verify:`** Once the configuration is in place, test the OIDC authentication by logging in with OIDC credentials. Verify that users are successfully authenticated and granted the expected access rights.

   ```
   1) Restart the Kubernetes API server to apply the changes.
   2) Access the Kubernetes API server using the OIDC authentication flow. For example, you can use the kubectl command-line tool:
   ```
   ```
     kubectl config set-credentials oidc-user --auth-provider=oidc \
     --auth-provider-arg=idp-issuer-url=https://keycloak/auth/realms/<realm> \
     --auth-provider-arg=client-id=<client-id> \
     --auth-provider-arg=client-secret=<client-secret> \
     --auth-provider-arg=refresh-token=<refresh-token> \
     --auth-provider-arg=id-token=<id-token>
   ```
   ```
   Replace <realm>, <client-id>, <client-secret>, <refresh-token>, and <id-token> with the appropriate values obtained from Keycloak. Make sure to use the correct URL and authentication parameters for your setup.

   3. Verify that you can access Kubernetes resources based on the assigned roles and group mappings.
   ```
![kube-oidc](https://github.com/lerndevops/kubernetes-security/blob/main/img/kube-oidc.webp)