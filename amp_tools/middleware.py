
from amp_tools.settings import settings
from amp_tools import set_amp_detect


class AMPDetectionMiddleware(object):

    def process_request(self, request):
        if settings.AMP_TOOLS_GET_PARAMETER in request.GET:
            if request.GET[settings.AMP_TOOLS_GET_PARAMETER] == settings.AMP_TOOLS_GET_VALUE:
                set_amp_detect(is_amp_detect=True, request=request)
