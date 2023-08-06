# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_web']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4[lxml]>=4.9.3,<5.0.0',
 'cssbeautifier>=1.13.0,<2.0.0',
 'jsbeautifier>=1.13.0,<2.0.0',
 'mdformat>=0.3.5']

entry_points = \
{'mdformat.codeformatter': ['css = mdformat_web:format_css',
                            'html = mdformat_web:format_html',
                            'javascript = mdformat_web:format_js',
                            'js = mdformat_web:format_js',
                            'xml = mdformat_web:format_xml']}

setup_kwargs = {
    'name': 'mdformat-web',
    'version': '0.1.0',
    'description': 'Mdformat plugin to format JS, CSS, HTML and XML code blocks',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-web/workflows/Tests/badge.svg?branch=master)](<https://github.com/hukkinj1/mdformat-web/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush>)\n[![PyPI version](<https://img.shields.io/pypi/v/mdformat-web>)](<https://pypi.org/project/mdformat-web>)\n\n# mdformat-web\n> Mdformat plugin to format JS, CSS, HTML and XML code blocks\n\n## Description\nmdformat-web is an [mdformat](https://github.com/executablebooks/mdformat) plugin\nthat makes mdformat format JavaScript and CSS code blocks with [JS Beautifier](https://github.com/beautify-web/js-beautify),\nand HTML and XML with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).\n\n## Installing\n```bash\npip install mdformat-web\n```\n\n## Usage\n```bash\nmdformat YOUR_MARKDOWN_FILE.md\n```\n',
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
