# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eve_panel', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['eve>=1.1.3,<2.0.0',
 'httpx>=0.16.1,<0.17.0',
 'nested_dict>=1.61,<2.0',
 'pandas>=1.1.3,<2.0.0',
 'panel>=0.9.7,<0.10.0']

setup_kwargs = {
    'name': 'eve-panel',
    'version': '0.2.0',
    'description': 'Top-level package for Eve-Panel.',
    'long_description': '=========\nEve-Panel\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/eve_panel.svg\n        :target: https://pypi.python.org/pypi/eve_panel\n\n.. image:: https://img.shields.io/travis/jmosbacher/eve_panel.svg\n        :target: https://travis-ci.com/jmosbacher/eve_panel\n\n.. image:: https://readthedocs.org/projects/eve-panel/badge/?version=latest\n        :target: https://eve-panel.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\nDynamically create an httpx based client for any Eve api that uses Param for type enforcement and Panel for GUIs.\nThis is just a prototype package,features will slowly be added as i need them for my own purposes.\nThe api is expected to change without warning based on my needs but feel free to fork or copy parts and adapt to your own needs.\n\nTo view the widgets in a notebook you will need to install the pyviz plugin. For details, see panel docs.\n.. code-block:: python\n\n        import eve\n        from eve_panel import EveApiClient, EveDomain\n\n        app = eve.Eve()\n\n        client = eve_panel.EveApiClient.from_app_config(app.config, address="http://localhost:5000")\n        client.auth.token = "my-secret-token"\n\n        api = eve_panel.EveDomain.from_domain_def("my_api_name", app.config["DOMAIN"], client=client)\n\n        # show a resources gui\n        api.resource_name \n\n        # get a specific item\n        api.resource_name["item_id"]\n\n        # get current page data\n        api.resource_name.current_page()\n\n        # get next page data\n        api.resource_name.next_page()\n\n        # get previous page data\n        api.resource_name.previous_page()\n\n\n* Free software: MIT\n* Documentation: https://eve-panel.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/eve_panel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
