# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instrumentools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'matplotlib>=3.1.2,<4.0.0',
 'ncempy>=1.5.0,<2.0.0',
 'numpy>=1.17.4,<2.0.0',
 'pandas>=1.0.0,<2.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'seaborn>=0.9.0,<0.10.0',
 'tqdm>=4.40.2,<5.0.0',
 'xlrd>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['cac_analysis = instrumentools.CAC:main',
                     'dsc_analysis = instrumentools.DSC:main',
                     'tem_analysis = instrumentools.TEM:main',
                     'tga_analysis = instrumentools.TGA:main']}

setup_kwargs = {
    'name': 'instrumentools',
    'version': '0.1.3',
    'description': 'Data processing and plotting scripts for chemistry workflows',
    'long_description': None,
    'author': 'Dal Williams',
    'author_email': 'dendrondal@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dendrondal/instrumentools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
