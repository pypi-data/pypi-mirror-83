# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearcache', 'clearcache.management', 'clearcache.management.commands']

package_data = \
{'': ['*'], 'clearcache': ['templates/admin/*', 'templates/clearcache/admin/*']}

install_requires = \
['django>=2.2,<3.2']

setup_kwargs = {
    'name': 'django-clearcache',
    'version': '1.1.1',
    'description': 'Allows you to clear Django cache via admin UI or manage.py command',
    'long_description': "# Django ClearCache 🤠🧹💰 ![Build status](https://circleci.com/gh/timonweb/django-clearcache.svg?style=shield)\n\n\nAllows you to clear Django cache via admin UI or manage.py command.\n\n![demo](http://g.recordit.co/qnrHAo66Ny.gif)\n\n## Installation\n\n1. Install using PIP:\n\n    `pip install django-clearcache`\n\n2. Add **clearcache** to INSTALLED_APPS, make sure it's above `django.contrib.admin`:\n\n```\nINSTALLED_APPS += [\n    ...\n    'clearcache',\n    'django.contrib.admin',\n    ...\n]\n```\n\n3. Add url to the main **urls.py** right above root admin url:\n    ```\n    urlpatterns = [\n        url(r'^admin/clearcache/', include('clearcache.urls')),\n        url(r'^admin/', include(admin.site.urls)),\n    ]\n    ```\n\n## Usage\n\n### Via Django admin\n\n1. Go to `/admin/clearcache/`, you should see a form with cache selector\n2. Pick a cache. Usually there's one default cache, but can be more.\n3. Click the button, you're done!\n\n### Via manage.py command\n\n1. Run the following command to clear the default cache\n\n```\npython manage.py clearcache\n```\n\n2. Run the command above with an additional parameter to clear non-default cache (if exists):\n\n```\npython manage.py clearcache cache_name\n```\n\n## Follow me\n\n1. Check my dev blog with Python and JavaScript tutorials at [https://timonweb.com](https://timonweb.com)\n2. Follow me on twitter [@timonweb](https://twitter.com/timonweb)\n",
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://timonweb.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
