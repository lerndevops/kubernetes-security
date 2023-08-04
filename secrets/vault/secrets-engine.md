## Secrets engine

## What is a secrets engine?
---
> **Secrets engines are Vault components which store, generate or encrypt secrets/data** 

> **Secrets engines are incredibly flexible, so it is easiest to think about them in terms of their function. Secrets engines are provided some set of data, they take some action on that data, and they return a result.**

> **secrets engines like the `key/value secrets engine` simply store and read data.**

> **Other secrets engines connect to other services and `generate dynamic credentials on demand`. Other secrets engines provide encryption as a service.**

> **Secrets engines are enabled at a path in Vault. When a request comes to Vault, the router automatically routes anything with the route prefix to the secrets engine. In this way, each secrets engine defines its own paths and properties.** 

> **To the user, secrets engines behave similar to a virtual filesystem, supporting operations like read, write, and delete.**

> **There are a number of secrets engines available. You can think of them as a `plugin`. Enable the secrets engine that meets your security needs.**

![scret-engine](https://github.com/lerndevops/kubernetes-security/blob/main/img/vault.png)

## Secrets engines lifecycle
---
> **Most secrets engines can be `enabled`, `disabled`, `tuned`, and moved via the CLI or API.**

1) **[Enable](https://developer.hashicorp.com/vault/docs/commands/secrets/enable) - This enables a secrets engine at a given path. With a few exceptions, secrets engines can be enabled at multiple paths. Each secrets engine is isolated to its path. By default, they are enabled at their "type" (e.g. "aws" enables at aws/).**
   ```
    Note: Case-sensitive: The path where you enable secrets engines is case-sensitive. 

    For example, the KV secrets engine enabled at kv/ and KV/ are treated as two distinct instances of KV secrets engine.
   ```

2) **[Disable](https://developer.hashicorp.com/vault/docs/commands/secrets/disable) - This disables an existing secrets engine. When a secrets engine is disabled, all of its secrets are revoked (if they support it), and all the data stored for that engine in the physical storage layer is deleted.**

3) **[Move](https://developer.hashicorp.com/vault/docs/commands/secrets/move) - This moves the path for an existing secrets engine. This process revokes all secrets, since secret leases are tied to the path where they were created. The configuration data stored for the engine persists through the move.**

4) **[Tune](https://developer.hashicorp.com/vault/docs/commands/secrets/tune) - This tunes global configuration for the secrets engine such as the TTLs.**

> **Once a secrets engine is enabled, you can interact with it directly at its path according to its own API. Use vault path-help to determine the paths it responds to.**