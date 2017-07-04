
from django import template
from django.contrib.sites.models import Site
from django.http import QueryDict
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.template import Library, Node, Variable
from django.template.defaultfilters import stringfilter

register = template.Library()

from amp_tools.settings import settings


@register.simple_tag
def amp_canonical_link(request):
    getvars = request.GET.copy()
    rel = "amphtml"
    if settings.AMP_TOOLS_GET_PARAMETER in getvars:
        del getvars[settings.AMP_TOOLS_GET_PARAMETER]
        rel = "canonical"
    else:
        getvars[settings.AMP_TOOLS_GET_PARAMETER] = settings.AMP_TOOLS_GET_VALUE

    if len(getvars.keys()) > 0:
        getvars = getvars.urlencode()
    else:
        getvars = ''

    href = '%s?%s' % (request.path, getvars) if getvars else request.path

    href = "%s://%s%s" % (request.scheme, Site.objects.get_current().domain, href)

    return mark_safe('<link rel="%s" href="%s" />' % (rel, href))


class AddGetParameter(Node):
    def __init__(self, values, url=None):
        self.url = url
        self.values = values

    def render(self, context):
        if self.url:
            params = QueryDict(self.values)
        else:
            req = Variable('request').resolve(context)
            self.url = req.path
            params = req.GET.copy()

            for key, value in self.values.items():
                resolved = value.resolve(context)
                if resolved:
                    params[key] = value.resolve(context)

        return '%s?%s' % (self.url, params.urlencode())


@register.tag
def amp_link(parser, token):
    url = token.split_contents()[1:][0]
    params = "%s=%s" % (settings.AMP_TOOLS_GET_PARAMETER, settings.AMP_TOOLS_GET_VALUE)
    return AddGetParameter(params, url)


@register.filter
def amp_urlparam(value):
    return "%s?%s=%s" % (value, settings.AMP_TOOLS_GET_PARAMETER, settings.AMP_TOOLS_GET_VALUE)


@register.filter(name='amp_img')
@stringfilter
def amp_img(html_code):
    """Convert <img> to <amp-img>"""
    return html_code.replace("<img", "<amp-img")
