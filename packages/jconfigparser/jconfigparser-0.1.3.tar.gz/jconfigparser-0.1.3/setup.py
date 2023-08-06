# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jconfigparser']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jconfigparser',
    'version': '0.1.3',
    'description': 'Augmented python configparser',
    'long_description': '\n\njconfigparser\n===\n\n![python](https://img.shields.io/badge/python-3.6--3.8-informational.svg?style=flat)\n[![pypi](https://img.shields.io/pypi/v/jconfigparser.svg?style=flat)](https://pypi.org/project/jconfigparser/)\n![license](https://img.shields.io/pypi/l/jconfigparser.svg?color=red&style=flat)\n[![code style](https://img.shields.io/badge/code%20style-black-202020.svg?style=flat)](https://github.com/ambv/black)\n\n`jconfigparser` is an extension of the `python` `configparser` standard module which adds the following features inspired by [`TOML`](https://github.com/toml-lang/toml):\n\n- Section name depth with dot notation: `[a.b]` \n- Values on right hand side can be everything that is understood by [JSON](https://www.json.org/json-en.html).\n- Values that appear twice or more often are stored as a `list`, see example `output` below (this behavior is configurable).\n\n## Example\n\nSay we have the following configuration file in `test.jconf`:\n\n```\n[atoms]\nfile:                          geometry.in\nformat:                        aims\n\n[calculator.aims]\nxc:                            pbesol\ncharge_mix_param:              0.3\nsc_accuracy_rho:               1e-6\n\noutput: band  0     0     0     0.00  0.25  0.25  50   Gamma  Delta\noutput: band  0.00  0.25  0.25  0     0.5   0.5   50   Delta  X\n\n[calculator.socketio]\nport:                          null\n\n[basissets.aims]\ndefault:                       light\n```\n\n\n\nThis file can be parsed with\n\n```python\nimport jconfigparser as jc\n\nconfig = jc.Config(\'test.jconf\')\n```\n\n`config` will be a modified `dict` that hold the information like\n\n```python\n{\n    "atoms": {"file": "geometry.in", "format": "aims"},\n    "calculator": {\n        "aims": {\n            "xc": "pbesol",\n            "charge_mix_param": 0.3,\n            "sc_accuracy_rho": 1e-06,\n            "output": [\n                "band  0     0     0     0.00  0.25  0.25  50   Gamma  Delta",\n                "band  0.00  0.25  0.25  0     0.5   0.5   50   Delta  X",\n            ],\n        },\n        "socketio": {"port": None},\n    },\n    "basissets": {"aims": {"default": "light"}},\n}\n```\n\n\n\nFurthermore, `config` supports\n\n* Attribute access, e.g., `config.atoms.file`\n* Write itself: `config.write("new.jconf")`\n\n## Changelog\n- v0.1.3: per default, use case-sensitive keys\n',
    'author': 'Florian Knoop',
    'author_email': 'florian_knoop@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/flokno/jconfigparser',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
