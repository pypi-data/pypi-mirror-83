# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydoautomator']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=2.0.0,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pydoautomator',
    'version': '0.8.1',
    'description': 'The Python lib for digital ocean automation',
    'long_description': '# pydoautomator\n\n[![codecov](https://codecov.io/gh/christian-hawk/pydoautomator/branch/master/graph/badge.svg)](https://codecov.io/gh/christian-hawk/pydoautomator)\n\nThe Digital Ocean python automation lib\n\n## Install\n\n`pip install pydoautomator`\n\n## Simple as that\n\n``` python\nfrom pydoautomator import Automator, Droplet\ndigital_ocean_token = \'my-digital-ocean-api-token\'\n\naut = Automator(digital_ocean_token)\n\ndroplet_data = {\n    "name" : "t1.techno24x7.com",\n    "region" : "nyc1",\n    "size" : "s-8vcpu-16gb",\n    "image" : 68259296, # snapshot id\n    "ssh_keys" : [27410347, 27608055, 27590881],\n    "private_networking" : True,\n    "vpc_uuid" : "47e5c00a-2b23-4dac-bed4-0e44659941f3",\n    "monitoring" : True\n    "tags" : ["tests"]\n}\n\ndroplet = Droplet(**droplet_data)\n\naut.create_droplet_from_snapshot(droplet)\n\n```\n\n### Assign floating ip to droplet\n\n```python\ndroplet_id = 152412424\nfloating_ip = \'164.90.252.72\'\naction_status = aut.assign_floating_ip_to_droplet(floating_ip, droplet_id)\n\nif action_status == \'completed\':\n    print(\'floating_ip assigned to droplet!\')\n```\n\n### Create droplet and assign floating ip as soon as droplet created\n\n```python\ndigital_ocean_token = \'my-super-cool-digital-ocean-api-token\'\n\naut = Automator(digital_ocean_token)\n\ndroplet_data = {\n    "name": "t1.techno24x7.com",\n    "region": "nyc1",\n    "size": "s-8vcpu-16gb",\n    "image": 70649304, # snapshot id\n    "ssh_keys": [27410347, 27608055, 27590881],\n    "private_networking": True,\n    "vpc_uuid": "47e5c00a-2b23-4dac-bed4-0e44659941f3",\n    "monitoring": True\n}\n\ndroplet = Droplet(**droplet_data)\n\ndroplet_id = aut.create_droplet_from_snapshot(droplet)\n\n\nfloating_ip = \'164.90.252.72\'\naction_status = aut.assign_floating_ip_to_droplet(floating_ip, droplet_id)\n\nif action_status == \'completed\':\n    print(\'floating_ip assigned to droplet!\')\n```\n\n### Shutdown / turnoff droplet\n\n```python\ndroplet_id = 123456\naut.turnoff_droplet(droplet_id)\n```\n\n### Destroy droplet by id\n\n```python\ndroplet_id = 123456\naut.destroy_droplet(droplet_id)\n```\n\n.\n',
    'author': 'Christian Eland',
    'author_email': 'eland.christian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/christian-hawk/pydoautomator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
