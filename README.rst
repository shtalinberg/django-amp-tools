================
django-amp-tools
================

.. image:: https://travis-ci.org/shtalinberg/django-amp-tools.svg?branch=develop
    :target: https://travis-ci.org/shtalinberg/django-amp-tools

.. image:: https://img.shields.io/pypi/v/django-amp-tools.svg
    :target:  https://pypi.python.org/pypi/django-amp-tools/

.. image:: https://img.shields.io/pypi/pyversions/django-amp-tools.svg

.. image:: https://img.shields.io/badge/django-1.8%20or%20newer-green.svg

.. image:: https://img.shields.io/pypi/dm/django-amp-tools.svg
    :target:  https://pypi.python.org/pypi/django-amp-tools/


.. _introduction:

**django-amp-tools** ( amp_tools ) provides a simple way to work with Accelerated mobile pages (AMP)
in django and gives you tools at your hand to render some different templates
to deliver an AMP version of your site to the user.

The idea (from django-mobile app) is to keep your views exactly the same but to transparently
interchange the templates used to render a response. This is done in two steps:

1. A middleware determines the client's preference to view your site. E.g. if
   he wants to use the AMP or the standart version.
2. The template loader takes then care of choosing the correct templates based
   on the GET param detected in the middleware.


Installation
============

.. _installation:

*Pre-Requirements:* ``django-amp-tools`` depends on django's sites framework. So
before you try to use ``django-amp-tools`` make sure that the sites framework
is enabled and working.

1. Install ``django-amp-tools`` with your favourite python tool, e.g. with
   ``easy_install django-amp-tools`` or ``pip install django-amp-tools``.
2. Add ``amp_tools`` to your ``INSTALLED_APPS`` setting in the
   ``settings.py``.
3. Add ``amp_tools.middleware.AMPDetectionMiddleware`` to end of your
   ``MIDDLEWARE_CLASSES`` setting.
4. Add ``amp_tools.loader.Loader`` as first item to your
   ``loaders`` list for ``TEMPLATES`` setting in ``settings.py``.


Pull requests are welcome.
