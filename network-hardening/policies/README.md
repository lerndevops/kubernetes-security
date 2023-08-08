## Network Policies 

> **A network policy is a specification of how groups of pods are allowed to communicate with each other and other network endpoints.**

1) **Network policies allow you to specify which pods can talk to other pods. This helps when securing communication between pods, allowing you to identify `ingress` and `egress` rules.**
2) **we can apply a network policy to a pod by using pod or namespace selectors.**
3) **we can even choose a CIDR block range to apply the network policy**

### Prerequisites

>> **Network policies are implemented by the network plugin, so we must be using a networking solution which supports NetworkPolicy. Ex: calico, canal provides these features**

>> **simply creating the resource without a controller to implement it will have no effect**

## Ingress vs Egress

#### **Network policies can be used to specify both allowed ingress to pods and allowed egress from pods. These specifications work as one would expect:**

> **traffic to a pod from an external network endpoint outside the cluster is allowed if ingress from that endpoint is allowed to the pod.**

> **traffic from a pod to an external network endpoint outside the cluster is allowed if egress is allowed from the pod to that endpoint.**

> **traffic from one pod (A) to another (B) is allowed if and only if egress is allowed from A to B and ingress is allowed to B from A.**

>>> ***Note that controls are unidirectional – for traffic from B to be allowed to initiate a connection to A, egress must be allowed from B to A and ingress to B& from A.***


## Working with Network Policies 

1) [deny-all-ingress-and-egress-in-a-namespace-then-allow-neccessary]