[![version](https://img.shields.io/pypi/v/hexafid.svg)](https://pypi.org/project/hexafid/) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hexafid.svg)](https://www.python.org/)
[![PyPI - Status](https://img.shields.io/pypi/status/hexafid.svg)](https://gitlab.com/hexafid/hexafid)
[![Gitlab coverage](https://img.shields.io/gitlab/coverage/hexafid/hexafid/master)](https://gitlab.com/hexafid/hexafid)
[![license](https://img.shields.io/pypi/l/hexafid.svg)](https://hexafid.gitlab.io/hexafid/hexafid-license.html)

## Hexafid

Hexafid is an experimental block cipher. [DANGER!](#caveat-emptor) 

The project goals are to produce a cipher that:
- works easily with pen and paper
- secures confidentiality of information
- offers plausible deniability if discovered
- exhibits greater strength in software

### Caveat Emptor

- Hexafid began as a hobby project during the COVID-19 pandemic
- The work has NOT yet been peer reviewed by the academic community
- The algorithms have NOT yet been proven to have strong security
- The software is released under an open source licence (MIT) that:
    - Limits ANY liability, and 
    - Provides NO warranty

### Documentation Home

https://hexafid.gitlab.io/hexafid

### Installation  
<!--- [![PyPI - Downloads](https://img.shields.io/pypi/dm/hexafid)](https://pypi.org/project/hexafid/) --->

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hexafid.

```bash
$ pip install hexafid
```

### Usage

As an end user:
```console
$ hexafid --version
$ hexafid --help
$ hexafid
```

As a developer:
```python
from hexafid import hexafid_core as hexafid
hexafid.encrypt(message, key, mode, iv, period, rounds)  # returns ciphertext string
hexafid.decrypt(message ,key, mode, period, rounds)  # returns plaintext string
```
NOTE: use of these libraries assumes that you understand the cryptographic implications of changing parameters.

### Contributing
Merge Requests are welcome. For all changes, please:
1. open an Issue first to document the activity; 
2. label the Issue (e.g. Bug, Feature, Refactor, Suggestion, Test);
3. update or add any related tests to support your work;  
3. create an associated Merge Request to discuss changes with a maintainer.

We expect team members to have minimum knowledge as found in https://www.coursera.org/learn/crypto.

Key areas of future research and development include:
1. linear and differential cryptanalysis
2. constraint optimized key search algorithm
3. publishable reference implementation in C 

### License
[MIT License](https://hexafid.gitlab.io/hexafid/hexafid-license.html)