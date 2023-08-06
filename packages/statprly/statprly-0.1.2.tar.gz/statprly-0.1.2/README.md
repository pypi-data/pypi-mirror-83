## STATPRLY

[![Release](https://img.shields.io/github/release/alladin9393/statprly.svg)](https://github.com/alladin9393/statprly/releases)
[![PyPI version shields.io](https://img.shields.io/pypi/v/statprly.svg)](https://pypi.python.org/pypi/statprly/)
[![Build Status](https://travis-ci.com/Alladin9393/statprly.svg?branch=develop)](https://travis-ci.com/Alladin9393/statprly)
[![CodeFactor](https://www.codefactor.io/repository/github/alladin9393/statprly/badge)](https://www.codefactor.io/repository/github/alladin9393/statprly)

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/statprly.svg)](https://pypi.python.org/pypi/statprly/)

`STATPRLY` - is a python package with recognition tools.

Set of tools:

    * Bayesian recognition digit based on standards
    
  * [Getting started](#getting-started)
    * [Requirements](#getting-started-requirements)
      * [Ubuntu 16.04 & 18.04](#ubuntu-1604--1804)
      * [MacOS](#macos)
    * [Installation](#installation)
  * [Usage](#usage)
    * [Bayesian Recognition Digit](#bayesian-recognition-digit-usage)
  * [Development](#development)
  * [Production](#production)
  * [Contributing](#contributing)
    * [Request pull request's review](#request-pull-requests-review)

## Getting started

<h3 id="getting-started-requirements">Requirements</h4>

#### Ubuntu 16.04 & 18.04

If you have 16.04 version, install system requirements with the following terminal commands:

```bash
$ sudo apt update && sudo apt install -y software-properties-common build-essential
```

#### MacOS

Install Python 3.7 (also, we support 3.6):
```bash
$ brew install python3
```

## Installation

Install the package from the [PyPi](https://pypi.org/project/statprly) through pip:

```bash
$ pip3 install statprly
```

## Usage

#### Bayesian Recognition Digit
<a name="bayesian-recognition-digit-usage"></a>

Recognize random digit with noise:

```python
import numpy

from statprly import MonoDigitRecognizer

if __name__ == '__main__':
    recognizer = MonoDigitRecognizer()
    noise = 0.1
    with open('path_to_digit_to_recognize') as f:
        digit_to_predict = f.read()
    
    digit_to_predict = numpy.array(digit_to_predict)
    recognized_digit = recognizer.recognize(
        digit_to_predict_data=digit_to_predict,
        noise_probability=noise,
    )

    print(recognized_digit)    
```

Recognize random digit with noise with data from `Pattern Recognition Server`:

Install requirements to interact with server:
```bash
$ pip3 install websockets
```

Example code can be found here:
[Link to github gist](https://gist.github.com/Alladin9393/52c22ac263684d878ce8819642a07f1a).

## Development

Clone the project and move to project folder:

```bash
$ git clone https://github.com/Alladin9393/statprly.git && cd statprly
```

Create virtualenv and install requirements:

```bash
$ virtualenv venv -p python3 && source venv/bin/activate
$ pip3 install -r requirements/development.txt
```

To run tests use:

```bash
$ coverage run -m pytest -vv tests
```

When you have developed new functionality, check it with the following command. This command creates the Python 
package from source code instead of installing it from the PyPi:

```bash
$ pip3 uninstall -y statprly && rm -rf dist/ statprly.egg-info && \
      python3 setup.py sdist && pip3 install dist/*.tar.gz
```
## Production

To build the package and upload it to [PypI](https://pypi.org/) to be accessible through 
[pip](https://github.com/pypa/pip), use the following commands. [Twine](https://twine.readthedocs.io/en/latest/) 
requires the username and password of the account package is going to be uploaded to.

```bash
$ python3 setup.py sdist
$ twine upload dist/*
username: alladin9393
password: ******
```

## Contributing

#### Request pull request's review

If you want to your pull request to be review, ensure you:

If you want to your pull request to be review, ensure you:
1. [Branch isn't out-of-date with the base branch](https://habrastorage.org/webt/ux/gi/wm/uxgiwmnft08fubvjfd6d-8pw2wq.png).
2. [Have written the description of the pull request and have added at least 2 reviewers](https://camo.githubusercontent.com/55c309334a8b61a4848a6ef25f9b0fb3751ae5e9/68747470733a2f2f686162726173746f726167652e6f72672f776562742f74312f70792f63752f7431707963753162786a736c796f6a6c707935306d7862357969652e706e67).
3. [Continuous integration has been passed](https://habrastorage.org/webt/oz/fl/-n/ozfl-nl-jynrh7ofz8yuz9_gapy.png).
