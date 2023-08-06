![Build](https://github.com/radon-h2020/radon-defect-predictor/workflows/Build/badge.svg)
![Documentation](https://github.com/radon-h2020/radon-defect-predictor/workflows/Documentation/badge.svg)
![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/radon-h2020/radon-defect-predictor)
![LGTM Alerts](https://img.shields.io/lgtm/alerts/github/radon-h2020/radon-defect-predictor)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# radon-defect-prediction
The RADON command-line client for Infrastructure-as-Code Defect Prediction.


## How to Install

From source code:
```
git clone https://github.com/radon-h2020/radon-defect-prediction.git
cd radon-defect-predictor
pip install .
```

## Quick Start

```radon-defect-predictor --help```

```prompt
usage: radon-defect-predictor [-h] [-v] {train,predict,model} ...

A Python library to train machine learning models for defect prediction of infrastructure code

positional arguments:
  {train,predict,model}
    train               train a brand new model from scratch
    model               get a pre-trained model to test unseen instances
    predict             predict unseen instances

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

See the [Docs](https://radon-h2020.github.io/radon-defect-predictor/) for details and examples of usage.
