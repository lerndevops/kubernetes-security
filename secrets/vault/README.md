## What is Vault 

> **Vault is an identity-based secret and encryption management system**

> **A secret is anything that you want to tightly control access to, such as API encryption keys, passwords, and certificates**

> **A modern system requires access to a multitude of secrets, like** 

1) database credentials, 
2) API keys for external services, 
3) credentials for service-oriented architecture communication, etc. 

> **Vault comes with various pluggable components called secrets engines and authentication methods allowing you to integrate with external systems.**

![vault](https://github.com/lerndevops/kubernetes-security/blob/main/img/vault.png)

## Why Vault? 

> **Centrally store, access, and deploy secrets across applications, systems, and infrastructure.**

> **Vault provides encryption services that are gated by authentication and authorization methods.**

> **Using Vault’s UI, CLI, or HTTP API, access to secrets and other sensitive data can be securely stored and managed, tightly controlled (restricted), and auditable.**

> **Vault validates and authorizes clients (users, machines, apps) before providing them access to secrets or stored sensitive data.**

> **It can be difficult to understand who is accessing which secrets, especially since this can be platform-specific. Adding on key rolling, secure storage, and detailed audit logs is almost impossible without a custom solution. This is where Vault steps in.**

### the key features of Vault

1) **`Secure Secret Storage:` Arbitrary key/value secrets can be stored in Vault. Vault encrypts these secrets prior to writing them to persistent storage, so gaining access to the raw storage isn't enough to access your secrets. Vault can write to disk, Consul, and more.**

2) **`Dynamic Secrets:` Vault can generate secrets on-demand for some systems, such as AWS or SQL databases. For example, when an application needs to access an S3 bucket, it asks Vault for credentials, and Vault will generate an AWS keypair with valid permissions on demand. After creating these dynamic secrets, Vault will also automatically revoke them after the lease is up.**

3) **`Data Encryption:` Vault can encrypt and decrypt data without storing it. This allows security teams to define encryption parameters and developers to store encrypted data in a location such as a SQL database without having to design their own encryption methods.**

4) **`Leasing and Renewal:` All secrets in Vault have a lease associated with them. At the end of the lease, Vault will automatically revoke that secret. Clients are able to renew leases via built-in renew APIs.**`

5) **`Revocation:` Vault has built-in support for secret revocation. Vault can revoke not only single secrets, but a tree of secrets, for example all secrets read by a specific user, or all secrets of a particular type. Revocation assists in key rolling as well as locking down systems in the case of an intrusion.**

## How does vault work? 

> **Vault works primarily with tokens and a token is associated to the client's policy.**

> **Each policy is path-based and policy rules constrains the actions and accessibility to the paths for each client.**

> **With Vault, you can create tokens manually and assign them to your clients, or the clients can log in and obtain a token.**

![How does vault work](https://github.com/lerndevops/kubernetes-security/blob/main/img/vault-flow.png)