# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['catconfig']
setup_kwargs = {
    'name': 'catconfig',
    'version': '0.1.1',
    'description': '🐱Make more easy for reading/validating/updating config for python app',
    'long_description': '# CatConfig\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/catconfig) \n![PyPI - License](https://img.shields.io/pypi/l/catconfig)\n![test](https://github.com/dev-techmoe/python-catconfig/workflows/test/badge.svg)\n\n🐱Make more easy for reading/validating/updating config for python app\n\n## Install \n\n```\npip install catconfig\n```\n\nIf you want to use validation feature, install `cerberus` module for your project to use it normally.  \n\nInstall `toml` or `pyyaml` module for toml/yaml format parsing.\n\n## Quickstart\n\n```python\n# Example.py\nfrom catconfig import CatConfig, ValidationError\n\n# Load\n# Load config from string\nc = CatConfig()\nc.load_from_string("""\n{\n    "foo": "bar"\n}\n""")\n# Load config when initalizing CatConfig object\nc = CatConfig(data={\n    \'foo\': \'bar\'\n})\n# load config from file\nc = CatConfig()\nc.load_from_file(\'./tests/assests/test.json\')\n# Specify config type when initalizing CatConfig object\nc = CatConfig(format=\'json\')\nc.load_from_file(\'./tests/assests/test.json\')\n# Specify config type when loading config file\nc = CatConfig()\nc.load_from_file(\'./tests/assests/test.json\', format=\'json\')\n\n# Get item\nprint(c.foo)\n# Print: bar\nprint(bool(c.some.value.does.nt.exists))\n# Print: False\nprint(str(c.some.value.does.nt.exists))\n# Print: None\nprint(c[\'foo\'])\n# Print: bar\nprint(c.get(\'foo\'))\n# Print: bar\n\n# Validation\n# visit https://docs.python-cerberus.org/en/stable/usage.html for more info of schema\nschema = {\n    \'foo\': {\n        \'type\': \'integer\'\n    },\n    \'some_field\': {\n        \'type\': \'string\'\n    }\n}\nc = CatConfig(validator_schema=schema)\ntry:\n    c.load_from_file(\'./tests/assests/test.json\')\nexcept ValidationError as err:\n    print(err.message)\n    # Print:\n    # arr: unknown field\n    # foo: must be of integer type\n```\n\n## License\nMIT',
    'author': 'dev-techmoe',
    'author_email': 'me@lolicookie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dev-techmoe/python-catconfig',
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
