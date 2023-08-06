# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysizer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['pysizer = pysizer:main']}

setup_kwargs = {
    'name': 'pysizer',
    'version': '0.1.0',
    'description': 'Quick & Efficient Command Line picture resizer!',
    'long_description': '# PySizer\n\n![](https://travis-ci.com/kumaraditya303/PySizer.svg?token=Tp128txvcHsePdipY3xq&branch=master)\n\n![](https://img.shields.io/codecov/c/github/kumaraditya303/PySizer?style=flat-square)\n\n# Introduction\n\n### PySizer is a simple python command line program to resize images efficiently using Threads. This program uses click as a command line argument parser. It can also be used to pyinstaller to create a executable.\n\n# Quick Start\n\n- Install the project with pip\n\n```bash\npip install git+https://github.com/kumaraditya303/PySizer.git\n```\n\n- Project will now be available as a command line utility\n\n- Get Help\n\n```text\n$ pysizer.exe --help\nUsage: pysizer [OPTIONS]\n\n  Main PySizer function which with ThreadPoolExecutor creates threads for\n  resizing pictures.\n\n  Checks for correct file extension, creates threads for each picture with\n  thread limitation as given by threads argument.\n\n  Creates progress bar with the click for resizing progress.\n\nOptions:\n  --source PATH      Pictures source  [default: .]\n  --dest PATH        Destination for resized pictures  [default: resized]\n  --height INTEGER   Image height  [default: 1280]\n  --width INTEGER    Image weight  [default: 1920]\n  --threads INTEGER  number of threads to use  [default: 40]\n  --help             Show this message and exit.\n\n```\n\n# Project Made and Maintained By Kumar Aditya\n',
    'author': 'Kumar Aditya',
    'author_email': 'rahuladitya303@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kumaraditya303/PySizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
