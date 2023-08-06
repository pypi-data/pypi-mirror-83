# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seo_cap']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seo-cap',
    'version': '0.1.0',
    'description': 'Utils for websites regarding SEO',
    'long_description': '# SEO Cap\n\n\n## Introduction\n## Installation\n## Usage\n## Code of Conduct\n## History ',
    'author': 'mg santos',
    'author_email': 'mauro.goncalo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mintyPT/seo-cap',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
