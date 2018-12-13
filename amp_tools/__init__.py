# -*- coding: utf-8 -*-

import threading
from amp_tools.settings import settings

__version__ = '0.2.0'

_local = threading.local()


def set_amp_detect(is_amp_detect=False, request=None):
    request = request or getattr(_local, 'request', None)
    if request:
        request.is_amp_detect = is_amp_detect
    _local.is_amp_detect = is_amp_detect


def get_amp_detect(request=None):
    is_amp_detect = False
    request = request or getattr(_local, 'request', None)

    # check if is_amp_detect is set on request
    if not is_amp_detect and hasattr(request, 'is_amp_detect'):
        is_amp_detect = request.is_amp_detect

    # if set out of a request-response cycle its stored on the thread local
    if not is_amp_detect:
        is_amp_detect = getattr(_local, 'is_amp_detect', False)
    return settings.AMP_TOOLS_TEMPLATE_FOLDER if is_amp_detect else u""
