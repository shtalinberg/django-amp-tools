
import threading

from amp_tools.settings import settings as amp_setting
from django.test import TestCase

from mock import MagicMock, Mock, patch, call

from amp_tools import get_amp_detect
from amp_tools.middleware import AMPDetectionMiddleware
from amp_tools.templatetags.amp_tags import amp_link


def _reset():
    '''
    Reset the thread local.
    '''
    import amp_tools
    del amp_tools._local
    amp_tools._local = threading.local()


class BaseTestCase(TestCase):
    def setUp(self):
        _reset()

    def tearDown(self):
        _reset()


class DetectAMPMiddlewareTests(BaseTestCase):

    def setUp(self):
        self.amp_get_parameter = amp_setting.AMP_TOOLS_GET_PARAMETER
        self.amp_get_value = amp_setting.AMP_TOOLS_GET_VALUE

    def test_default_page(self):
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        # default flavour is set
        self.assertEqual(get_amp_detect(), '')

    @patch('amp_tools.middleware.set_amp_detect')
    def test_set_amp_detect_through_get_parameter(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    def test_tamplate_tags(self):
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        middleware = AMPDetectionMiddleware()

        middleware.process_request(request)

        self.assertEqual(
            amp_link('/path/'),
            "/path/%s=%s" % (self.amp_get_parameter, self.amp_get_value)
        )
