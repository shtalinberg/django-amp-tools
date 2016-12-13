==========================================
Django AMP(Accelerated Mobile Pages) Tools
==========================================

**django-amp-tools** ( amp_tools ) provides a simple way to work with Accelerated mobile pages (AMP)
in django and gives you tools at your hand to render some different templates
to deliver an AMP version of your site to the user.

The idea (from django-mobile app) is to keep your views exactly the same but to transparently
interchange the templates used to render a response. This is done in two steps:

1. A middleware determines the client's preference to view your site. E.g. if
   he wants to use the AMP or the standart version.
2. The template loader takes then care of choosing the correct templates based
   on the GET param detected in the middleware.

The **source code** for this app is hosted at
https://github.com/shtalinberg/django-amp-tools.

Contents:

.. toctree::
   :maxdepth: 2

   installation
   contributing
   contacts
