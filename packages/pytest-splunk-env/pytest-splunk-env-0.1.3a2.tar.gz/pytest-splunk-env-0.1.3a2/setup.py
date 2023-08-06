# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_splunk_env',
 'pytest_splunk_env.sc4s',
 'pytest_splunk_env.splunk',
 'pytest_splunk_env.splunk.helmut',
 'pytest_splunk_env.splunk.helmut.app',
 'pytest_splunk_env.splunk.helmut.connector',
 'pytest_splunk_env.splunk.helmut.exceptions',
 'pytest_splunk_env.splunk.helmut.log',
 'pytest_splunk_env.splunk.helmut.manager',
 'pytest_splunk_env.splunk.helmut.manager.confs',
 'pytest_splunk_env.splunk.helmut.manager.confs.rest',
 'pytest_splunk_env.splunk.helmut.manager.confs.sdk',
 'pytest_splunk_env.splunk.helmut.manager.indexes',
 'pytest_splunk_env.splunk.helmut.manager.indexes.rest',
 'pytest_splunk_env.splunk.helmut.manager.indexes.sdk',
 'pytest_splunk_env.splunk.helmut.manager.jobs',
 'pytest_splunk_env.splunk.helmut.manager.jobs.rest',
 'pytest_splunk_env.splunk.helmut.manager.jobs.sdk',
 'pytest_splunk_env.splunk.helmut.manager.roles',
 'pytest_splunk_env.splunk.helmut.manager.roles.sdk',
 'pytest_splunk_env.splunk.helmut.manager.saved_searches',
 'pytest_splunk_env.splunk.helmut.manager.saved_searches.sdk',
 'pytest_splunk_env.splunk.helmut.manager.users',
 'pytest_splunk_env.splunk.helmut.manager.users.sdk',
 'pytest_splunk_env.splunk.helmut.misc',
 'pytest_splunk_env.splunk.helmut.splunk',
 'pytest_splunk_env.splunk.helmut.util',
 'pytest_splunk_env.splunk.helmut_lib']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.0,<4.0',
 'future',
 'httplib2',
 'pytest-xdist',
 'pytest>=6.1.1,<7.0.0',
 'requests',
 'splunk-sdk']

extras_require = \
{'docker': ['lovely-pytest-docker>=0,<1']}

entry_points = \
{'pytest11': ['pytest_splunk_env_base = pytest_splunk_env.splunk.base',
              'pytest_splunk_env_sc4s = pytest_splunk_env.sc4s',
              'pytest_splunk_env_splunk = pytest_splunk_env.splunk',
              'pytest_splunk_env_splunk_docker = '
              'pytest_splunk_env.splunk.docker',
              'pytest_splunk_env_splunk_external = '
              'pytest_splunk_env.splunk.external',
              'pytest_splunk_env_splunk_local = '
              'pytest_splunk_env.splunk.local']}

setup_kwargs = {
    'name': 'pytest-splunk-env',
    'version': '0.1.3a2',
    'description': 'pytest fixtures for interaction with Splunk Enterprise and Splunk Cloud',
    'long_description': None,
    'author': 'rfaircloth-splunk',
    'author_email': 'rfaircloth@splunk.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
