import re

from amp_tools.settings import settings
from amp_tools import set_amp_detect


class AMPDetectionMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_request(self, request):
        if settings.AMP_TOOLS_GET_PARAMETER in request.GET:
            if request.GET[settings.AMP_TOOLS_GET_PARAMETER] == settings.AMP_TOOLS_GET_VALUE:
                if settings.AMP_TOOLS_ACTIVE_URLS:
                    for url in settings.AMP_TOOLS_ACTIVE_URLS:
                        if not isinstance(url, re._pattern_type):
                            url = str(url)
                        url_re = re.compile(url)

                        if url_re.match(request.path_info):
                            set_amp_detect(is_amp_detect=True, request=request)
                else:
                    set_amp_detect(is_amp_detect=True, request=request)
        else:
            set_amp_detect(is_amp_detect=False, request=request)
