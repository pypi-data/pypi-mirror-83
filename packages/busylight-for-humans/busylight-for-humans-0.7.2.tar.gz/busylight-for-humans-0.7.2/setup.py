# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['busylight', 'busylight.api', 'busylight.effects', 'busylight.lights']

package_data = \
{'': ['*']}

install_requires = \
['bitvector-for-humans>=0.14.0,<0.15.0',
 'hidapi>=0.9.0,<0.10.0',
 'typer>=0,<1',
 'webcolors>=1.11.1,<2.0.0']

extras_require = \
{'webapi': ['uvicorn>=0.12.2,<0.13.0', 'fastapi>=0.61.1,<0.62.0']}

entry_points = \
{'console_scripts': ['busylight = busylight.__main__:cli']}

setup_kwargs = {
    'name': 'busylight-for-humans',
    'version': '0.7.2',
    'description': 'Control USB connected LED lights, like a human.',
    'long_description': '# `busylight`\n\nControl USB attached LED lights like a Human™\n\n![Python 3.7](https://github.com/JnyJny/busylight/workflows/Python%203.7/badge.svg)\n\n![All supported lights](https://github.com/JnyJny/busylight/raw/master/demo/demo.gif)\n\nMake a USB attached LED light turn on, off and blink; all from the\ncomfort of your very own command-line. If your platform supports\nHIDAPI (Linux, MacOS, Windows and probably others), then you can use\n`busylight` with supported lights!\n\n## Usage\n\n\n```console\n$ busylight on\n$ busylight off\n$ busylight on purple\n$ busylight on 0xff00ff   # still purple.\n$ busylight blink yellow  # all hands man your stations.\n$ busylight blink red     # RED ALERT!\n$ busylight off           # all clear.\n```\n\n## Supported Lights\n\n\n```console\n$ busylight supported\nAgile Innovations BlinkStick (†)\nEmbrava Blynclight\nThingM Blink1\nKuando BusyLight (‡)\nLuxafor Flag\n```\n\n \n- † Requires software intervention for `blink` mode\n- ‡ Requires software intervention for all modes\n\nLights that "require software intervention" need software to constantly update\nthe device instead of a one-time configuration of the light. Those devices will\ncause the `busylight` command to not return immediately and the lights will\nturn off when the user interrupts the command. The `busylight serve` mode can\nhelp in this situation.\n\n## Install\n\n\n```console\n$ pip install -U busylight-for-humans\n$ busylight --help\n```\n\n### Install with web API support using FastAPI & Uvicorn\n\n\n```console\n$ pip install -U busylight-for-humans[webapi]\n```\n\n## Source\n\n\n[busylight](https://github.com/JnyJny/busylight.git)\n\n**Usage**:\n\n```console\n$ busylight [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-l, --light-id INTEGER`: Which light to operate on, see list output.  [default: 0]\n* `-a, --all`: Operate on all lights.\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `blink`: Activate the selected light in blink mode.\n* `list`: List available lights (currently connected).\n* `off`: Turn selected lights off.\n* `on`: Turn selected lights on.\n* `serve`: Start a FastAPI-based service to access...\n* `supported`: List supported LED lights.\n* `udev-rules`: Generate a Linux udev rules file.\n\n## `busylight blink`\n\nActivate the selected light in blink mode.\n\nThe light selected will blink with the specified color. The default color is red\nif the user omits the color argument. Colors can be specified with color names and\nhexadecimal values. Both \'0x\' and \'#\' are recognized as hexidecimal number prefixes\nand hexadecimal values may be either three or six digits long.\n\nNote: Ironically, BlinkStick products cannot be configured to blink on and off\n      without software constantly updating the devices. If you need your BlinkStick\n      to blink, you will need to use the `busylight serve` web API.\n\nExamples:\n\n```console\n$ busylight blink          # light is blinking with the color red\n$ busylight blink green    # now it\'s blinking green\n$ busylight blink 0x00f    # now it\'s blinking blue\n$ busylight blink #ffffff  # now it\'s blinking white\n$ busylight --all blink    # now all available lights are blinking red\n$ busylight --all off      # that\'s enough of that!\n```\n\n**Usage**:\n\n```console\n$ busylight blink [OPTIONS] [COLOR] [[slow|medium|fast]]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight list`\n\nList available lights (currently connected).\n    \n\n**Usage**:\n\n```console\n$ busylight list [OPTIONS]\n```\n\n**Options**:\n\n* `-l, --long`\n* `--help`: Show this message and exit.\n\n## `busylight off`\n\nTurn selected lights off.\n\nTo turn off all lights, specify --all:\n\n```console\n$ busylight --all off\n```\n\n**Usage**:\n\n```console\n$ busylight off [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight on`\n\nTurn selected lights on.\n\nThe light selected is turned on with the specified color. The default color is green\nif the user omits the color argument. Colors can be specified with color names and\nhexadecimal values. Both \'0x\' and \'#\' are recognized as hexidecimal number prefixes\nand hexadecimal values may be either three or six digits long. \n\nExamples:\n\n\n```console\n$ busylight on          # light activated with the color green\n$ busylight on red      # now it\'s red\n$ busylight on 0x00f    # now it\'s blue\n$ busylight on #ffffff  # now it\'s white\n$ busylight --all on    # now all available lights are green\n```\n\n**Usage**:\n\n```console\n$ busylight on [OPTIONS] [COLOR]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight serve`\n\nStart a FastAPI-based service to access lights.\n\nAll connected lights are managed by the service, allowing\nlong-running animations and effects that the native device APIs\nmight not support.\n\nOnce the service is started, the API documentation is available\nvia these two URLs:\n\n\n- `http://<hostname>:<port>/docs`\n- `http://<hostname>:<port>/redoc`\n\n## Examples\n\n\n```console\n$ busylight server >& log &\n$ curl http://localhost:8888/1/lights\n$ curl http://localhost:8888/1/lights/on\n$ curl http://localhost:8888/1/lights/off\n$ curl http://localhost:8888/1/light/0/on/purple\n$ curl http://localhost:8888/1/light/0/off\n$ curl http://localhost:8888/1/lights/on\n$ curl http://localhost:8888/1/lights/off\n\n**Usage**:\n\n```console\n$ busylight serve [OPTIONS]\n```\n\n**Options**:\n\n* `-H, --host TEXT`\n* `-p, --port INTEGER`\n* `--help`: Show this message and exit.\n\n## `busylight supported`\n\nList supported LED lights.\n    \n\n**Usage**:\n\n```console\n$ busylight supported [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `busylight udev-rules`\n\nGenerate a Linux udev rules file.\n\nLinux uses the udev subsystem to manage USB devices as they are\nplugged and unplugged. By default, only the root user has read and\nwrite access. The rules generated grant read/write access to all users\nfor all known USB lights by vendor id. Modify the rules to suit your\nparticular environment.\n\n### Example\n\n\n```console\n$ busylight udev-rules -o 99-busylight.rules\n$ sudo cp 99-busylight.rules /etc/udev/rules.d\n```\n\n**Usage**:\n\n```console\n$ busylight udev-rules [OPTIONS]\n```\n\n**Options**:\n\n* `-o, --output PATH`: Save rules to this file.\n* `--help`: Show this message and exit.\n',
    'author': 'JnyJny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/busylight.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
