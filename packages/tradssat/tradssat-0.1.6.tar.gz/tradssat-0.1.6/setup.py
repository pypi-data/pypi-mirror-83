# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tradssat',
 'tradssat.exper',
 'tradssat.genotype',
 'tradssat.genotype.vars_',
 'tradssat.mgrs',
 'tradssat.out',
 'tradssat.soil',
 'tradssat.tmpl',
 'tradssat.weather',
 'tradssat.weather.cli',
 'tradssat.weather.mth',
 'tradssat.weather.wth']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=3.0.4,<4.0.0',
 'numpy>=1.19.3,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'pytest-cov>=2.10.1,<3.0.0']

setup_kwargs = {
    'name': 'tradssat',
    'version': '0.1.6',
    'description': 'DSSAT input and output file reader and writer',
    'long_description': None,
    'author': 'Julien Malard',
    'author_email': 'julien.malard@mail.mcgill.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
