from __future__ import unicode_literals

import threading

from django.test import TestCase, override_settings
from django.template import Template, RequestContext


from mock import MagicMock, Mock, patch, call

from amp_tools import get_amp_detect
from amp_tools.middleware import AMPDetectionMiddleware
from amp_tools.settings import settings as amp_setting
from amp_tools.templatetags.amp_tags import amp_img



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
        request.GET = {'amp-content': 'amp'}
        template = Template(
            '{% load amp_tags %}{% amp_link "/path/" %}'
        )
        context = RequestContext(request, {},)

        rendered = template.render(context)

        self.assertEqual(
            rendered,
            "/path/?%s=%s" % (self.amp_get_parameter, self.amp_get_value)
        )

        html_content = """
            <html><body>
                <img alt="alternate text" src="/media/uploads/img.png" style="width: 100%;">
                <img alt="alternate text2" src="/media/uploads/img2.png" style="width: 100%;" />
            </body></html>
        """
        amp_content = amp_img(html_content)
        self.assertNotEqual(amp_content, html_content)
        self.assertEqual(amp_content, """
            <html><body>
                <amp-img alt="alternate text" src="/media/uploads/img.png" style="width: 100%;" layout="responsive"></amp-img>
                <amp-img alt="alternate text2" src="/media/uploads/img2.png" style="width: 100%;"  layout="responsive"></amp-img>
            </body></html>
        """)


    @patch('amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=['^/$'])
    def test_set_amp_not_set_url_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        request.path_info = '/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(set_amp_detect.call_args, call(is_amp_detect=True, request=request))

    @patch('amp_tools.middleware.set_amp_detect')
    @override_settings(AMP_TOOLS_ACTIVE_URLS=['^/$'])
    def test_set_amp_not_set_url_not_allowed(self, set_amp_detect):
        request = Mock()
        request.META = MagicMock()
        request.GET = {'amp-content': 'amp'}
        request.path_info = '/not-amp-url/'
        middleware = AMPDetectionMiddleware()
        middleware.process_request(request)
        self.assertEqual(0, len(set_amp_detect.call_args_list))

