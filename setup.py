#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from distutils.core import setup

PROJECT_NAME = 'amp_tools'
ROOT = os.path.abspath(os.path.dirname(__file__))
VENV = os.path.join(ROOT, '.venv')
VENV_LINK = os.path.join(VENV, 'local')

install_requires = [
    'django>=1.11.0',
]


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))


def read(filename):
    return open(os.path.join(ROOT, filename)).read()


class VenvLinkDeleted(object):

    restore_link = False

    def __enter__(self):
        """Remove the link."""
        if os.path.islink(VENV_LINK):
            os.remove(VENV_LINK)
            self.restore_link = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore the link."""
        if self.restore_link:
            os.symlink(VENV, VENV_LINK)

with VenvLinkDeleted():
    setup(
        name='django-amp-tools',
        version=get_version('amp_tools'),
        packages=[
            PROJECT_NAME,
            '{0}.templatetags'.format(PROJECT_NAME),
        ],
        package_data={PROJECT_NAME: data_files},
        include_package_data=True,
        license='MIT License',
        description='Accelerated mobile pages (AMP) in django.',
        keywords='django AMP accelerated',
        long_description=read('README.rst'),
        url='http://github.com/shtalinberg/django-amp-tools',
        author='Oleksandr Shtalinberg',
        author_email='O.Shtalinberg@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',  # example license
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            # Replace these appropriately if you are stuck on Python 2.
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.6',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
        install_requires=install_requires,
        zip_safe=False,
    )
