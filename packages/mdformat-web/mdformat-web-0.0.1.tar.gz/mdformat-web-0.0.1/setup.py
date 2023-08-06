# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_web']

package_data = \
{'': ['*']}

install_requires = \
['cssbeautifier>=1.13.0,<2.0.0',
 'jsbeautifier>=1.13.0,<2.0.0',
 'mdformat>=0.3.5']

entry_points = \
{'mdformat.codeformatter': ['css = mdformat_web:format_css',
                            'javascript = mdformat_web:format_js',
                            'js = mdformat_web:format_js']}

setup_kwargs = {
    'name': 'mdformat-web',
    'version': '0.0.1',
    'description': 'Mdformat plugin to format JS and CSS code blocks',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-web/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-web/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](<https://img.shields.io/pypi/v/mdformat-web>)](<https://pypi.org/project/mdformat-web>)\n\n# mdformat-web\n> Mdformat plugin to format JS and CSS code blocks\n\n## Description\nmdformat-web is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format JavaScript and CSS code blocks with [JS Beautifier](https://github.com/beautify-web/js-beautify).\n\n## Installing\n```bash\npip install mdformat-web\n```\n\n## Usage\n```bash\nmdformat YOUR_MARKDOWN_FILE.md\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-web',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
