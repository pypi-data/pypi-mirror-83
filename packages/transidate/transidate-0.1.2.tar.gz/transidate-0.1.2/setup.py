# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transidate']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'lxml>=4.6.1,<5.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['transidate = transidate.cli:validate']}

setup_kwargs = {
    'name': 'transidate',
    'version': '0.1.2',
    'description': 'Commandline tool for XML transit data validation.',
    'long_description': '# Transidate\n\n## Commadline XML Transit Data Validation\n\n### Installation\n\n```sh\npip install transidate\n\ntransidate /path/to/xml/or/zip/file\n```\n',
    'author': 'Ciaran McCormick',
    'author_email': 'ciaran@ciaranmccormick.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
