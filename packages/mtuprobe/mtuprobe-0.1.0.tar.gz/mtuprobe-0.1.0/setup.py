# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtuprobe']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['mtuprobe = mtuprobe.__main__:__main__']}

setup_kwargs = {
    'name': 'mtuprobe',
    'version': '0.1.0',
    'description': 'A tool to find out maximum MTU size on an IPv4 path',
    'long_description': "mtuprobe\n========\n\nA tool to probe the current\n[MTU](https://en.wikipedia.org/wiki/Maximum_transmission_unit) on an IPv4 path.\n\nSo far it's compatible with Linux only however it can very easily be adapted\nto any other operating system.\n\n## Installation\n\n```\npip install mtuprobe\n```\n\n## Usage\n\nThe default options are sane and should give you good results. Suppose that\nyou want to know the current effective MTU towards `wikipedia.org`, in a shell\nyou can try:\n\n```\n% mtuprobe wikipedia.org\nMax packet size:         1464\nExpected ethernet MTU:   1492\n```\n\nYou can check out `mtuprobe -h` to get the complete list of options.\n\nValues are:\n\n- **Max packet size** &mdash; Max packet size specified to `ping`, meaning the\n  size of the data segment of the ICMP packet\n- **Expected ethernet MTU** &mdash; That's what the MTU should be if you're\n  transmitting over Ethernet and the header sizes are what is expected from\n  such a setup. This should apply most of the time but surely some weird\n  network setups could violate this.\n",
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Xowap/mtuprobe',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
