# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssh2_parse_key']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.2.0,<21.0.0']

setup_kwargs = {
    'name': 'ssh2-parse-key',
    'version': '0.7.0',
    'description': 'Parses ssh2 keys and converts to multiple formats.',
    'long_description': '# ssh2_parse_key\n\n[![ci](https://img.shields.io/travis/nigelm/ssh2_parse_key.svg)](https://travis-ci.com/nigelm/ssh2_parse_key)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://nigelm.github.io/ssh2_parse_key/)\n[![pypi version](https://img.shields.io/pypi/v/ssh2_parse_key.svg)](https://pypi.python.org/pypi/ssh2_parse_key)\n\nParses ssh2 public keys in either openssh or RFC4716/Secsh formats and\nconverts to either format.\n\nAt this point any attempt to work with private keys will raise an exception.\n\n----\n\n## Features\n\n- Reads public keys of the following encryption types:-\n    - `ssh-rsa`\n    - `ssh-dss`\n    - `ecdsa-sha2-nistp256`\n    - `ssh-ed25519`\n- Reads either Openssh or RFC4716 format public keys\n- Can read input sets with either or both formats in\n- Can output either format for any key\n\n----\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install ssh2_parse_key\n```\n\n----\n\n## Usage\n\nTo use SSH2 Key Parsing in a project\n\n```python\nfrom ssh2_parse_key import Ssh2Key\n\n# although you can create the object from internal data the normal method\n# would be to use the parse() or parse_file() which return a list of Ssh2Key objects.\n# Ssh2Key objects are immutable.\n# Load one or more keys in either openssh or RFC4716 from a file\nkeys = Ssh2Key.parse_file("/path/to/public_key")\n\n# alternatively\ndata = Path("/path/to/public_key").read_text()\nkeys = Ssh2Key.parse(data)\n\n# now those keys can be dealt with...\nfor public_key in keys:\n    print(f"This is a {key.type} key")\n    print(f"It uses {key.encryption} encryption")\n    print(f"comment = {key.comment}")\n    print(f"subject = {key.subject}")\n\n    print("RFC4716 format representation")\n    print(key.rfc4716())\n\n    print("OpenSSH representation")\n    print(key.openssh())\n```\n\n----\n\n## Credits\n\nThe package is strongly based on the perl [`Parse::SSH2::PublicKey`](https://metacpan.org/pod/Parse::SSH2::PublicKey) module.\n\nDevelopment on the python version was done by [`Nigel Metheringham <nigelm@cpan.org>`](https://github.com/nigelm/)\n\n----\n',
    'author': 'Nigel Metheringham',
    'author_email': 'nigelm@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/ssh2-parse-key/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
