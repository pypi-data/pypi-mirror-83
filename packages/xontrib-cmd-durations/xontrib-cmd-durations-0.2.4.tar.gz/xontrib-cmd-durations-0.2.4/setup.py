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
    'name': 'xontrib-cmd-durations',
    'version': '0.2.4',
    'description': 'Send notification once long running command is finished. Add duration PROMP_FIELD.',
    'long_description': '# Overview\n\n<p align="center">\nSend notification once long-running command is finished. Adds `long_cmd_duration` to `$PROMPT_FIELDS` .\n</p>\n\n## Installation\n\nTo install use pip:\n\n``` bash\nxpip install xontrib-cmd-durations\n# or: xpip install -U git+https://github.com/jnoortheen/xontrib-cmd-durations\n```\n\n## Usage\n\n``` bash\nxontrib load cmd_done\n```\n\n## Usage\n\n* makes `long_cmd_duration` available to the `$PROMPT_FIELDS`\n* if the command is taking more than `$LONG_DURATION` seconds\n  + it is `long_cmd_duration` returns the duration in human readable way\n  + a desktop notification is sent if the terminal is not focused.\n    - **Note**: Currently the focusing part requires `xdotool` to be installed.\n\n        So the notification part will not work in Windows/OSX. PRs welcome on that.\n\n``` bash\n$RIGHT_PROMPT = \'{long_cmd_duration:⌛{}}{user:{{BOLD_RED}}🤖{}}{hostname:{{BOLD_#FA8072}}🖥{}}\'\n```\n\n![](./images/2020-10-26-10-59-38.png)\n\n## Credits\n\nThis package was created with [xontrib cookiecutter template](https://github.com/jnoortheen/xontrib-cookiecutter).\n',
    'author': 'Noortheen Raja J',
    'author_email': 'jnoortheen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/xontrib-cmd-durations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
