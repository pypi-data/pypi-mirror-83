![](https://img.shields.io/github/issues/adimyth/tf-lambda-resnet)
![](https://img.shields.io/github/forks/adimyth/tf-lambda-resnet)
![](https://img.shields.io/github/stars/adimyth/tf-lambda-resnet)
![](https://img.shields.io/github/license/adimyth/tf-lambda-resnet)
![](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Fadimyth%2Ftf-lambda-resnet
)

## LambdaResNet - TensorFlow

> All credit goes to [lucidrains](https://github.com/lucidrains/) for sharing the initial pytorch implementation. This repo takes majority of contents from his original repo [here](https://github.com/lucidrains/lambda-networks).

<img src="./lambda.png" width="500px"></img>

Implementation of λ-ResNet.

<a href="https://www.youtube.com/watch?v=3qxJ2WD8p4w">Yannic Kilcher's paper review</a>

## Install

```bash
$ pip install tf-lambda-resnet
```

## Usage

LambdaResNet uses localized context as explained in the video.

```python
import tensorflow as tf
from tf_lambda_resnet import LambdaResnet18

model = LambdaResnet18()
out = model(tf.ones([10, 224, 224, 3]))
print(out)
```

## Credits

All the code is taken from the below resources. I have assembled them in a proper manner to make it work for TF2.2

* [tfkeras.py](https://github.com/lucidrains/lambda-networks/blob/main/lambda_networks/tfkeras.py) by [shinel94](https://github.com/shinel94)
* [TensorFlow2.0 ResNet](https://github.com/calmisential/TensorFlow2.0_ResNet) by [calmisential](https://github.com/calmisential)

## References

Thanks to [PistonY](https://gist.github.com/PistonY) for sharing a gist here - [lambda_net.py](https://gist.github.com/PistonY/ad33ab9e3d5f9a6a38345eb184e68cb4)


## Citations

```bibtex
@inproceedings{
    anonymous2021lambdanetworks,
    title={LambdaNetworks: Modeling long-range Interactions without Attention},
    author={Anonymous},
    booktitle={Submitted to International Conference on Learning Representations},
    year={2021},
    url={https://openreview.net/forum?id=xTJEN-ggl1b},
    note={under review}
}
```
