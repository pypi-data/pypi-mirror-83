# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_splunk_addon',
 'pytest_splunk_addon.standard_lib',
 'pytest_splunk_addon.standard_lib.addon_parser',
 'pytest_splunk_addon.standard_lib.cim_compliance',
 'pytest_splunk_addon.standard_lib.cim_tests',
 'pytest_splunk_addon.standard_lib.event_ingestors',
 'pytest_splunk_addon.standard_lib.fields_tests',
 'pytest_splunk_addon.standard_lib.index_tests',
 'pytest_splunk_addon.standard_lib.sample_generation',
 'pytest_splunk_addon.standard_lib.utilities']

package_data = \
{'': ['*'], 'pytest_splunk_addon.standard_lib': ['data_models/*']}

install_requires = \
['faker>=4.1,<5.0',
 'filelock>=3.0,<4.0',
 'httplib2',
 'jsonschema>=3.2,<4.0',
 'junitparser',
 'pytest',
 'pytest-splunk-env>=v0.1.3-a.2',
 'pytest-xdist',
 'requests>=2,<3',
 'splunk-sdk>=1.6,<2.0',
 'splunk_appinspect>=2,<3']

extras_require = \
{'docker': ['lovely-pytest-docker>=0,<1']}

entry_points = \
{'console_scripts': ['cim-report = '
                     'pytest_splunk_addon.standard_lib.cim_compliance.junit_parser:main',
                     'generate-indextime-conf = '
                     'pytest_splunk_addon.standard_lib.utilities.create_new_eventgen:main'],
 'pytest11': ['plugin = pytest_splunk_addon.plugin',
              'splunk = pytest_splunk_addon.splunk']}

setup_kwargs = {
    'name': 'pytest-splunk-addon',
    'version': '1.3.11a2',
    'description': 'A Dynamic test tool for Splunk Apps and Add-ons',
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
