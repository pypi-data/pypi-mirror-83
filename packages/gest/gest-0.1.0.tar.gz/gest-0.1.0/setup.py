# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gest', 'gest.annotation', 'gest.annotation.gesture', 'gest.examples']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'onnxruntime>=1.4.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0', 'pynput']

setup_kwargs = {
    'name': 'gest',
    'version': '0.1.0',
    'description': 'Hand gestures as an input device',
    'long_description': None,
    'author': 'Bartosz Marcinkowski',
    'author_email': 'b.marcinkowski@leomail.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
