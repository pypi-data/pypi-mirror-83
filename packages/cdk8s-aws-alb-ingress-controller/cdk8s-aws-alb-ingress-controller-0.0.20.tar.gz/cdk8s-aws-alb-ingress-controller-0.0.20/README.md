[![NPM version](https://badge.fury.io/js/cdk8s-aws-alb-ingress-controller.svg)](https://badge.fury.io/js/cdk8s-aws-alb-ingress-controller)
[![PyPI version](https://badge.fury.io/py/cdk8s-aws-alb-ingress-controller.svg)](https://badge.fury.io/py/cdk8s-aws-alb-ingress-controller)
![Release](https://github.com/guan840912/cdk8s-aws-alb-ingress-controller/workflows/Release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk8s-aws-alb-ingress-controller?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk8s-aws-alb-ingress-controller?label=pypi&color=blue)

# cdk8s-aws-alb-ingress-controller

> [aws alb ingress controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) constructs for cdk8s

Basic implementation of a [aws alb ingress controller](https://github.com/kubernetes-sigs/aws-alb-ingress-controller) construct for cdk8s. Contributions are welcome!

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s import App, Chart
from constructs import Construct
from cdk8s_aws_alb_ingress_controller import AlbIngressController

class MyChart(Chart):
    def __init__(self, scope, name):
        super().__init__(scope, name)
        AlbIngressController(self, "albingresscntroller",
            cluster_name="EKScluster"
        )
app = App()
MyChart(app, "testcdk8s")
app.synth()
```

# Featrue For Add IAM Policy.

* For IRSA add IAM Policy version 1.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# CDK APP like eks_cluster.ts
from cdk8s_aws_alb_ingress_controller import AwsLoadBalancePolicy, VersionsLists
import aws_cdk.aws_eks as eks
cluster = eks.Cluster(self, "MyK8SCluster",
    default_capacity=0,
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_18
)

alb_service_account = cluster.add_service_account("alb-ingress-controller",
    name="alb-ingress-controller",
    namespace="kube-system"
)
# will help you add policy to IAM Role .
AwsLoadBalancePolicy.add_policy(VersionsLists.AWS_LOAD_BALANCER_CONTROLLER_POLICY_V1, alb_service_account)
```

* For IRSA add IAM Policy version 2.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# CDK APP like eks_cluster.ts
from cdk8s_aws_alb_ingress_controller import AwsLoadBalancePolicy, VersionsLists
import aws_cdk.aws_eks as eks
cluster = eks.Cluster(self, "MyK8SCluster",
    default_capacity=0,
    masters_role=cluster_admin,
    version=eks.KubernetesVersion.V1_18
)

alb_service_account = cluster.add_service_account("alb-ingress-controller",
    name="alb-ingress-controller",
    namespace="kube-system"
)
# will help you add policy to IAM Role .
AwsLoadBalancePolicy.add_policy(VersionsLists.AWS_LOAD_BALANCER_CONTROLLER_POLICY_V2, alb_service_account)
```

Also can see [example repo](https://github.com/guan840912/cdk8s-cdk-example)

## License

Distributed under the [Apache 2.0](./LICENSE) license.
