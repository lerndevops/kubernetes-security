## Network Policies 

> **A network policy is a specification of how groups of pods are allowed to communicate with each other and other network endpoints.**

1) **Network policies allow you to specify which pods can talk to other pods. This helps when securing communication between pods, allowing you to identify `ingress` and `egress` rules.**
2) **we can apply a network policy to a pod by using pod or namespace selectors.**
3) **we can even choose a CIDR block range to apply the network policy**

### Prerequisites

>> **Network policies are implemented by the network plugin, so we must be using a networking solution which supports NetworkPolicy. Ex: calico, canal provides these features**

>> **simply creating the resource without a controller to implement it will have no effect**

## Working with Network Policies 

1) [deny-all-ingress-and-egress-in-a-namespace-then-allow-neccessary]