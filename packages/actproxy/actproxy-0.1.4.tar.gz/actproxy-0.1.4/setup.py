# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['actproxy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-socks>=0.5.5,<0.6.0',
 'aiohttp>=3.6.2,<4.0.0',
 'mo-dots>=3.93.20259,<4.0.0',
 'pytest-aiohttp>=0.3.0,<0.4.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest>=6.1.1,<7.0.0',
 'requests[socks]>=2.24.0,<3.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['setupgen = poetry.command_line:main']}

setup_kwargs = {
    'name': 'actproxy',
    'version': '0.1.4',
    'description': 'Sync & asyncio (Requests & AIOHTTP) proxy rotator + utils for actproxy API & services.',
    'long_description': '# actproxy\n\nPython package providing [actproxy.com](https://actproxy.com/aff.php?aff=30) API access and proxy rotation methods for requests (synchronous) and aiohttp\n(asyncio). Can also be used independently. Supports socks5, http/https, and ipv4/ipv6 as per actproxy\'s services.\n\n[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.org/project/actproxy/)\n\n## Quick-Start (AIOHTTP)\n\n```python\nimport actproxy\nfrom aiohttp import ClientSession\n\n\nasync def main():\n    actproxy_api_keys = [\n        "xxxxxxxxxxxxxxxxxxxxxxxx",\n        "xxxxxxxxxxxxxxxxxxxxxxxx"\n    ]\n    # Initialize API. Also returns your proxies.\n    await actproxy.aioinit(actproxy_api_keys)\n    # Use a new AIOHTTP connector which rotates & uses the next proxy.\n    async with ClientSession(connector=actproxy.aiohttp_rotate()) as session:\n        url = "http://dummy.restapiexample.com/api/v1/employees"\n        async with session.get(url) as resp:\n            if resp.status == 200:\n                resp_json = await resp.json()\n                print(resp_json)\n```\n\n## Quick-Start (Requests)\n\n```python\nimport actproxy\nimport requests\n\nactproxy_api_keys = [\n    "xxxxxxxxxxxxxxxxxxxxxxxx",\n    "xxxxxxxxxxxxxxxxxxxxxxxx"\n]\n# Initialize API. Also returns your proxies.\nactproxy.init(actproxy_api_keys)\nurl = "http://dummy.restapiexample.com/api/v1/employees"\nresp = requests.get(url, proxies=actproxy.rotate())\nif resp.status_code == 200:\n    resp_json = resp.json()\n    print(resp_json)\n```\n\n## Methods\n\n`actproxy.aioinitaioinit(api_keys=[], output_format=\'json\', get_userpass=True)`: Fetches your proxies from ActProxy & returns them. Must be run before the other aiohttp\nfunctions.\n\n`actproxy.initinit(api_keys=[], output_format=\'json\', get_userpass=True)`: Fetches your proxies from ActProxy & returns\nthem. Must be run before the other synchronous functions.\n\n`actproxy.aiohttp_rotate(protocol=\'socks5\')`: Returns an aiohttp connector which uses the next proxy from your list.\n\n`actproxy.rotate(protocol=\'socks5\')`: Returns the next proxy from your list. Return variable is suitable for use with requests[socks].\n\n`actproxy.random_proxy(protocol=\'socks5\')`: Returns a random proxy from your list. Return variable is suitable for use with\nrequests[socks].\n\n`actproxy.aiohttp_random(protocol=\'socks5\')`: Returns an aiohttp connector which uses uses a random proxy from your list.\n\n`actproxy.one_hot_proxy()`: Similar to rotate() but returns a single proxy dict/object for use in places other than\naiohttp or requests.\n\n## Changelog\n\n**0.1.4** - _10/23/2020_ : Support multiple API keys. Unit tests. Fixes.\n\n**0.1.3** - _9/29/2020_ : Minor fixes and addition of docstrings.\n\n**0.1.2** - _9/28/2020_ : Initial release version.',
    'author': 'TensorTom',
    'author_email': '14287229+TensorTom@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://actproxy.com/aff.php?aff=30',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
