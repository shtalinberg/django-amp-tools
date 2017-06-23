
from django import template
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.utils.functional import keep_lazy_text
from django.utils.encoding import force_text
from django.template import Library, Node, Variable

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
    def __init__(self, values):
        self.values = values

    def render(self, context):
        req = Variable('request').resolve(context)
        params = req.GET.copy()
        for key, value in self.values.items():
            resolved = value.resolve(context)
            if resolved:
                params[key] = value.resolve(context)
        return '?%s' % params.urlencode()


@register.tag
def amp_link(parser):
    params = ["%s=%s" % (settings.AMP_TOOLS_GET_PARAMETER, settings.AMP_TOOLS_GET_VALUE)]
    return AddGetParameter(params)
