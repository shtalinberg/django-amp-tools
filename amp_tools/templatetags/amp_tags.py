from __future__ import unicode_literals

import re

from django import template
from django.contrib.sites.models import Site
from django.http import QueryDict
from django.utils.safestring import mark_safe
# from django.utils.encoding import force_text
from django.template import Node, Variable
from django.template.defaultfilters import stringfilter

register = template.Library()

from amp_tools.settings import settings

# For the full HTML element - <img src="image.jpg">
RE_IMG = re.compile('(<img.+?src=["\'].+?["\'].+?>)')

# For the image url itself - "image.jpg"
RE_IMG_SRC = re.compile('src=["\'](.+?)["\']')



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

        return "{}?{}".format(self.url, params.urlencode())


@register.tag
def amp_link(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )
    if not (url[0] == url[-1] and url[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    params = "{}={}".format(
        settings.AMP_TOOLS_GET_PARAMETER,
        settings.AMP_TOOLS_GET_VALUE
    )
    return AddGetParameter(params, url[1:-1])


@register.filter
def amp_urlparam(value):
    return "%s?%s=%s" % (value, settings.AMP_TOOLS_GET_PARAMETER, settings.AMP_TOOLS_GET_VALUE)


@register.filter(name='amp_img')
@stringfilter
def amp_img(html_code):
    """Convert <img> to <amp-img>"""
    img_elements = RE_IMG.findall(html_code)
    for img_el in img_elements:
        replace_str = img_el.replace('/>','>')

        if not 'width=' in replace_str or not 'height=' in replace_str:
            replace_str = replace_str.replace('>', ' layout="responsive" width="1.33" height="1"></amp-img>')
        else:
            replace_str = replace_str.replace('>', ' layout="responsive"></amp-img>')

        html_code = html_code.replace(img_el, replace_str)
    html_code = html_code.replace("</img>", "</amp-img>")
    return html_code.replace('<img', '<amp-img')


@register.filter(name='amp_safe')
@stringfilter
def amp_safe(html_body):
    html_body = re.sub(
        r'<img (alt="[^"]*") (class="[^"]*") (src="[^"]*") style="height:(\d+)px;.*width:(\d+)px" />',
        r'<img \1 \2 \3 style="height:\4px; width:\5px" width="\5" height="\4" />',
        html_body
    )
    html_body = re.sub(
        r'<img (alt="[^"]*") (class="[^"]*") (src="[^"]*") style=".*width:(\d+)%" />',
        r'<img \1 \2 \3 style="width:\4%" />',
        html_body
    )

    html_body = re.sub(r'style="[^"]+"', '', html_body)
    html_body= amp_img(html_body)
    return mark_safe(html_body)


