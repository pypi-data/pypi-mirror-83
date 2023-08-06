# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docs',
 'docs._themes',
 'example',
 'example.contrib.experiment-client',
 'sanic_oauthlib',
 'sanic_oauthlib.contrib',
 'sanic_oauthlib.provider',
 'tests',
 'tests.oauth1',
 'tests.oauth2',
 'tests.test_contrib',
 'tests.test_oauth2']

package_data = \
{'': ['*'],
 'docs': ['_static/*', '_templates/*'],
 'docs._themes': ['flask/*',
                  'flask/static/*',
                  'flask_small/*',
                  'flask_small/static/*'],
 'example': ['static/*', 'templates/*'],
 'tests.oauth1': ['templates/*'],
 'tests.oauth2': ['templates/*']}

install_requires = \
['aiohttp==3.6.3',
 'oauthlib==3.1.0',
 'sanic-plugins-framework>=0.9.4,<1.0',
 'sanic>=19.12.3,<20.12.0',
 'sanic_jinja2_spf>=0.8.0',
 'sanic_session_spf>=0.5.1']

entry_points = \
{'sanic_plugins': ['OAuth1Provider = sanic_oauthlib.provider.oauth1:instance',
                   'OAuth2Provider = sanic_oauthlib.provider.oauth2:instance',
                   'OAuthClient = sanic_oauthlib.client:instance']}

setup_kwargs = {
    'name': 'sanic-oauthlib',
    'version': '0.2.2',
    'description': 'OAuthLib for Sanic, ported from Flask-OAuthLib',
    'long_description': "Sanic-OAuthlib\n==============\n\n.. image:: https://img.shields.io/pypi/wheel/sanic-oauthlib.svg\n   :target: https://pypi.python.org/pypi/sanic-OAuthlib/\n   :alt: Wheel Status\n.. image:: https://img.shields.io/pypi/v/sanic-oauthlib.svg\n   :target: https://pypi.python.org/pypi/sanic-oauthlib/\n   :alt: Latest Version\n.. image:: https://travis-ci.org/ashleysommer/sanic-oauthlib.svg?branch=master\n   :target: https://travis-ci.org/ashleysommer/sanic-oauthlib\n   :alt: Travis CI Status\n.. image:: https://coveralls.io/repos/ashleysommer/sanic-oauthlib/badge.svg?branch=master\n   :target: https://coveralls.io/r/ashleysommer/sanic-oauthlib\n   :alt: Coverage Status\n\n=====\n\nSanic-OAuthlib is an extension to Sanic that allows you to interact with\nremote OAuth enabled applications. On the client site, it is a replacement\nfor Sanic-OAuth. But it does more than that, it also helps you to create\nOAuth providers.\n\nSanic-OAuthlib is a fork of Flask-OAuthlib, ported to sanic using the\nSanicPluginsFramework.\n\nSanic-OAuthlib relies on oauthlib_.\n\n.. _oauthlib: https://github.com/idan/oauthlib\n\n\nFeatures\n--------\n(These features are directly ported from Flask-OAuthLib)\n\n- Support for OAuth 1.0a, 1.0, 1.1, OAuth2 client\n- Friendly API (same as Sanic-OAuth)\n- Direct integration with Sanic using SanicPluginsFramework\n- Basic support for remote method invocation of RESTful APIs\n- Support OAuth1 provider with HMAC and RSA signature\n- Support OAuth2 provider with Bearer token\n\nAnd request more features at `github issues`_.\n\n.. _`github issues`: https://github.com/ashleysommer/sanic-oauthlib/issues\n\n\nSecurity Reporting\n------------------\n\nIf you found security bugs which can not be public, send me email at `ashleysommer@gmail.com`.\nAttachment with patch is welcome.\n\n\nInstallation\n------------\n\nInstalling sanic-oauthlib is simple with pip_::\n\n    $ pip install Sanic-OAuthlib\n\nIf you don't have pip installed, try with easy_install::\n\n    $ easy_install Sanic-OAuthlib\n\n.. _pip: http://www.pip-installer.org/\n\n\nAdditional Notes\n----------------\n\nSee the original documentation for Flask-OAuthlib here: `flask-oauthlib@readthedocs`_.\n\n.. _`flask-oauthlib@readthedocs`: https://flask-oauthlib.readthedocs.io\n\nIf you are only interested in the client part, you can find some examples\nin the ``example`` directory.\n\nThere is also a `development version <https://github.com/lepture/flask-oauthlib/archive/master.zip#egg=Flask-OAuthlib-dev>`_ on GitHub.\n",
    'author': 'Ashley Sommer',
    'author_email': 'ashleysommer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ashleysommer/sanic_oauthlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
