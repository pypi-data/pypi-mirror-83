# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['webpub_manifest_parser',
 'webpub_manifest_parser.core',
 'webpub_manifest_parser.epub',
 'webpub_manifest_parser.opds2',
 'webpub_manifest_parser.rwpm']

package_data = \
{'': ['*']}

install_requires = \
['enum34>=1.1.10,<2.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'pyrsistent==0.16.1',
 'rfc3987>=1.3.8,<2.0.0',
 'strict-rfc3339>=0.7,<0.8',
 'uritemplate>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'webpub-manifest-parser',
    'version': '0.0.2',
    'description': 'A parser for the Readium Web Publication Manifest and OPDS 2.0 formats.',
    'long_description': '# python-webpub-manifest-parser\n\n[![Build Status](https://travis-ci.com/vbessonov/python-webpub-manifest-parser.svg?branch=master)](https://travis-ci.com/vbessonov/python-webpub-manifest-parser)\n\nA parser for the [Readium Web Publication Manifest (RWPM)](https://github.com/readium/webpub-manifest) and [Open Publication Distribution System 2.0 (OPDS 2.0)](https://drafts.opds.io/opds-2.0) formats.\n\n## Usage\n1. Install [pyenv](https://github.com/pyenv/pyenv#installation)\n\n3. Install one of the supported Python versions mentioned in [.python-version](.python-version) or other PATCH versions of the same MINOR versions:\n```bash\npyenv install <python-version>\n```\n\n4. Install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation) plugin\n\n5. Create a virtual environment:\n```bash\npyenv virtualenv <virtual-env-name>\npyenv activate <virtual-env-name>\n```\n\n6. Install the library\n```bash\npip install webpub-manifest-parser\n``` \n\n\n# Setting up a development environment\n\n## Running tests using tox\n1. Make sure that a virtual environment is not activated and deactivate it if needed:\n```bash\ndeactivate\n```\n\n2. Install `tox` and `tox-pyenv` globally:\n```bash\npip install tox tox-pyenv\n```\n\n3. Make your code prettier using isort and black:\n```bash\nmake reformat\n``` \n\n4. Run the linters:\n```bash\nmake lint\n```\n\n5. To run the unit tests use the following command:\n```bash\nmake test-<python-version>\n```\nwhere `<python-version>` is one of supported python versions:\n- py27\n- py36\n- py37\n- py38\n\nFor example, to run the unit test using Python 2.7 run the following command:\n```bash\nmake test-py27\n```',
    'author': 'Leonard Richardson',
    'author_email': 'leonardr@segfault.org',
    'maintainer': 'Viacheslav Bessonov',
    'maintainer_email': 'viacheslav.bessonov@hilbertteam.com',
    'url': 'https://github.com/NYPL-Simplified/python-webpub-manifest-parser',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
