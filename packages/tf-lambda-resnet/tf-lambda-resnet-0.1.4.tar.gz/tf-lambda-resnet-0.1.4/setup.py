# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tf_lambda_resnet']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.3.0,<0.4.0',
 'jupyter>=1.0.0,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'sklearn>=0.0,<0.1',
 'tensorflow==2.2.0']

setup_kwargs = {
    'name': 'tf-lambda-resnet',
    'version': '0.1.4',
    'description': 'LambdaResNet implementation in TensorFlow 2.2',
    'long_description': '![](https://img.shields.io/github/issues/adimyth/tf-lambda-resnet)\n![](https://img.shields.io/github/forks/adimyth/tf-lambda-resnet)\n![](https://img.shields.io/github/stars/adimyth/tf-lambda-resnet)\n![](https://img.shields.io/github/license/adimyth/tf-lambda-resnet)\n![](https://img.shields.io/twitter/url?url=https%3A%2F%2Fgithub.com%2Fadimyth%2Ftf-lambda-resnet\n)\n\n## LambdaResNet - TensorFlow\n\n> All credit goes to [lucidrains](https://github.com/lucidrains/) for sharing the initial pytorch implementation. This repo takes majority of contents from his original repo [here](https://github.com/lucidrains/lambda-networks).\n\n<img src="./lambda.png" width="500px"></img>\n\nImplementation of λ-ResNet.\n\n<a href="https://www.youtube.com/watch?v=3qxJ2WD8p4w">Yannic Kilcher\'s paper review</a>\n\n## Install\n\n```bash\n$ pip install tf-lambda-resnet\n```\n\n## Usage\n\nLambdaResNet uses localized context as explained in the video.\n\n```python\nimport tensorflow as tf\nfrom tf_lambda_resnet import LambdaResnet18\n\nmodel = LambdaResnet18()\nout = model(tf.ones([10, 224, 224, 3]))\nprint(out)\n```\n\n## Credits\n\nAll the code is taken from the below resources. I have assembled them in a proper manner to make it work for TF2.2\n\n* [tfkeras.py](https://github.com/lucidrains/lambda-networks/blob/main/lambda_networks/tfkeras.py) by [shinel94](https://github.com/shinel94)\n* [TensorFlow2.0 ResNet](https://github.com/calmisential/TensorFlow2.0_ResNet) by [calmisential](https://github.com/calmisential)\n\n## References\n\nThanks to [PistonY](https://gist.github.com/PistonY) for sharing a gist here - [lambda_net.py](https://gist.github.com/PistonY/ad33ab9e3d5f9a6a38345eb184e68cb4)\n\n\n## Citations\n\n```bibtex\n@inproceedings{\n    anonymous2021lambdanetworks,\n    title={LambdaNetworks: Modeling long-range Interactions without Attention},\n    author={Anonymous},\n    booktitle={Submitted to International Conference on Learning Representations},\n    year={2021},\n    url={https://openreview.net/forum?id=xTJEN-ggl1b},\n    note={under review}\n}\n```\n',
    'author': 'adimyth',
    'author_email': 'mishraaditya6991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adimyth/tf-lambda-resnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
