# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib', 'xontrib.notifypy', 'xontrib.notifypy.os_notifiers']

package_data = \
{'': ['*'],
 'xontrib.notifypy.os_notifiers': ['binaries/Notificator.app/Contents/*',
                                   'binaries/Notificator.app/Contents/MacOS/*',
                                   'binaries/Notificator.app/Contents/Resources/*',
                                   'binaries/Notificator.app/Contents/Resources/Scripts/*']}

install_requires = \
['xonsh>=0.9.20']

setup_kwargs = {
    'name': 'xontrib-cmd-done',
    'version': '0.2.2',
    'description': 'Send notification once long running command is finished. Add duration PROMP_FIELD.',
    'long_description': '<p align="center">\nSend notification once long running command is finished. Add duration PROMP_FIELD.\n</p>\n\n<p align="center">\nIf you like the idea click ⭐ on the repo and stay tuned.\n</p>\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-cmd-done\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-cmd-done\n```\n\n## Usage\n\n``` bash\nxontrib load cmd_done\n```\n\n## Examples\n\n``` bash\n$RIGHT_PROMPT = \'{long_cmd_duration:⌛{}}{user:{{BOLD_RED}}🤖{}}{hostname:{{BOLD_#FA8072}}🖥{}}\'\n```\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja J',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-cmd-done',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
