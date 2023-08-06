# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_doh']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'async_dns>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'async-doh',
    'version': '0.2.1',
    'description': 'DNS over HTTPS based on aiohttp and async_dns',
    'long_description': "# async-doh\n\n[![PyPI](https://img.shields.io/pypi/v/async-doh.svg)]()\n\nDNS over HTTPS based on aiohttp and [async_dns](https://github.com/gera2ld/async_dns).\n\n## Installation\n\n```sh\n$ pip install async-doh\n```\n\n## Usage\n\n### Command-line\n\n```\nusage: python3 -m async_doh [-h] [-n NAMESERVERS [NAMESERVERS ...]] [-t TYPES [TYPES ...]] hostnames [hostnames ...]\n\nAsync DNS resolver with DoH\n\npositional arguments:\n  hostnames             the hostnames to query\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -n NAMESERVERS [NAMESERVERS ...], --nameservers NAMESERVERS [NAMESERVERS ...]\n                        name servers\n  -t TYPES [TYPES ...], --types TYPES [TYPES ...]\n                        query types, default as `any`\n```\n\nExamples:\n\n```sh\n$ python3 -m async_doh -n https://223.5.5.5/dns-query -t ANY -- www.google.com\n```\n\n### Client\n\n```py\nimport asyncio\nimport aiohttp\nfrom async_doh.client import DoHClient\n\nasync def main():\n    async with DoHClient() as client:\n        result = await client.query('https://1.1.1.1/dns-query', 'www.google.com', 'A')\n        print('query:', result)\n        result = await client.query_json('https://1.1.1.1/dns-query', 'www.google.com', 'A')\n        print('query_json:', result)\n\nasyncio.run(main())\n```\n\n### Server\n\n```py\nfrom aiohttp import web\nfrom async_doh.server import application\n\nweb.run(application)\n```\n\nNow you have `http://localhost:8080/dns-query` as an endpoint.\n\n### Patching async_dns\n\nBy importing the patch, async_dns will support queries throught HTTPS (aka DNS over HTTPS):\n\n```py\nimport asyncio\nfrom async_dns import types\nfrom async_dns.resolver import ProxyResolver\nfrom async_doh.resolver_patch import patch\n\nasync def main():\n  revoke = await patch()\n  resolver = ProxyResolver(proxies=['https://dns.alidns.com/dns-query'])\n  print(resolver.query('www.google.com', types.A))\n  await revoke()\n\nasyncio.run(main())\n```\n\n## References\n\n- <https://tools.ietf.org/html/rfc8484>\n",
    'author': 'Gerald',
    'author_email': 'gera2ld@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/async-doh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
