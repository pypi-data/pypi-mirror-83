# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jobsbundle']

package_data = \
{'': ['*'], 'jobsbundle': ['_config/*', 'git/*', 'job/*']}

install_requires = \
['console-bundle>=0.2.0,<0.3.0',
 'databricks-api>=0.3.0,<0.4.0',
 'injecta>=0.7',
 'pyfony-bundles>=0.2.0,<0.3.0',
 'pygit2>=1.3.0,<1.4.0']

setup_kwargs = {
    'name': 'jobs-bundle',
    'version': '0.2.3b1',
    'description': 'Databricks jobs management bundle for the Bricksflow Framework',
    'long_description': '# Databricks jobs bundle\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/jobs-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
