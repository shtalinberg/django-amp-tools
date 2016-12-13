#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_tests'

if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.append(os.path.abspath(root))
    execute_from_command_line()
