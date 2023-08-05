# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pkgdownloader']

package_data = \
{'': ['*'], 'pkgdownloader': ['docker/*', 'templates/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'docker>=4.3.1,<5.0.0']

entry_points = \
{'console_scripts': ['pkg-downloader = pkgdownloader.pkgdownloader:run']}

setup_kwargs = {
    'name': 'pkg-downloader',
    'version': '0.1.4',
    'description': 'A streamlined way to download packages for offline installation.',
    'long_description': '# pkg-downloader\n\nA package downloader for Ubuntu, Debian, and CentOS that downloads the .deb or .rpm packages and their dependencies.\n\n## Installation & Requirements\n---\n\n### Prerequisites\n\n- Python 3.7.2+\n- [Docker](https://docs.docker.com/engine/install/)\n\n\n### Install pkg-downloader\n```\npip3 install pkg-downloader\n```\n\n## Exaple Usage\n---\nTo download packages for centos 8: \n```\npkg-downloader --os centos --version 8 --packages nginx postgresql\n```\n\nTo download packages for ubuntu 20.04 to a specific directory: \n```\npkg-downloader --os ubuntu --version 20.04 --location ~/Desktop --packages nginx postgresql \n```',
    'author': 'TheComputerDan',
    'author_email': 'thedoctordan@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TheComputerDan/pkg-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
