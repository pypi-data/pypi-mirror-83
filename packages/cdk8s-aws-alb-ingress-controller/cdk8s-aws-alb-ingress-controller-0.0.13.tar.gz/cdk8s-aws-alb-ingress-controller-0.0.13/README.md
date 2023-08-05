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

## License

Distributed under the [Apache 2.0](./LICENSE) license.
