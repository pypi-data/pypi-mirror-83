# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psdtoolsx',
 'psdtoolsx.api',
 'psdtoolsx.composer',
 'psdtoolsx.composite',
 'psdtoolsx.compression',
 'psdtoolsx.psd']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<10', 'attrs>=20.2.0,<22', 'numpy>=1.19.3,<3']

setup_kwargs = {
    'name': 'psdtoolsx',
    'version': '19.5.0',
    'description': 'Python package for working with Adobe Photoshop PSD files',
    'long_description': '[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](../../)\n[![Codacy grade](https://img.shields.io/codacy/grade/[codacy-proj-id].svg?style=for-the-badge)](https://www.codacy.com/manual|gh/FHPythonUtils/PSDToolsX)\n[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](../../)\n[![Issues](https://img.shields.io/github/issues/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](../../issues)\n[![License](https://img.shields.io/github/license/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](/LICENSE.md)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](../../commits/master)\n[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/PSDToolsX.svg?style=for-the-badge)](../../commits/master)\n[![PyPI Downloads](https://img.shields.io/pypi/dm/psdtoolsx.svg?style=for-the-badge)](https://pypi.org/project/psdtoolsx/)\n[![PyPI Version](https://img.shields.io/pypi/v/psdtoolsx.svg?style=for-the-badge)](https://pypi.org/project/psdtoolsx/)\n\n# PSDToolsX\n\n<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">\n\n\n\nPSDToolsX is a Python package for working with Adobe\nPhotoshop PSD files as described in\n[specification](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/).\n\n[![PyPI Version](https://img.shields.io/pypi/v/psd-tools.svg)](https://pypi.python.org/pypi/psd-tools)\n![Test](https://github.com/psd-tools/psd-tools/workflows/Test/badge.svg)\n[![Document Status](https://readthedocs.org/projects/psd-tools/badge/)](http://psd-tools.readthedocs.io/en/latest/)\n\n\n\n## Changes from upstream\n\n1. Use poetry\n2. find and replace `psd_tools` with `psdtoolsx`\n\n\n## Installation\n\nUse `pip` to install the package:\n\n    pip install psd-tools\n\n::: {.note}\n::: {.title}\nNote\n:::\n\nIn order to extract images from 32bit PSD files PIL/Pillow must be built\nwith LITTLECMS or LITTLECMS2 support.\n:::\n\n## Getting started\n\n```python\nfrom psdtoolsx import PSDImage\n\npsd = PSDImage.open(\'example.psd\')\npsd.composite().save(\'example.png\')\n\nfor layer in psd:\n    print(layer)\n    layer_image = layer.composite()\n    layer_image.save(\'%s.png\' % layer.name)\n```\n\nCheck out the [documentation](https://psd-tools.readthedocs.io/) for\nfeatures and details.\n\n## Contributing\n\nSee\n[contributing](https://github.com/psd-tools/psd-tools/blob/master/docs/contributing.rst)\npage.\n',
    'author': 'FredHappyface',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FHPythonUtils/psdtoolsx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
