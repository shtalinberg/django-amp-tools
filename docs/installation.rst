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
