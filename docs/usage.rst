Usage
=====

Usage app
~~~~~~~~~

The concept of **django-amp-tools** is render *amp* for your site from save view as desktop version.

This makes it possible to provide many possible designs instead of just
differentiating between a full desktop experience and one AMP version.


After the correct version is somehow chosen by the middlewares, it's
assigned to the ``request.is_amp_detect`` attribute. You can use this in your views
to provide separate logic.


.. code-block:: html+django

    <html>
    <head>
        <title>My site {% if request.is_amp_detect %}(amp version){% endif %}</title>
    </head>
    <body>
        ...
    </body>
    </html>

You can create own AMP base.html.

My example base_amp.html

.. code-block:: html+django

    <!doctype html>{% load i18n amp_tags %}{% load static from staticfiles %}
    <html amp lang="{{ LANGUAGE_CODE }}">
      <head>
        <meta charset="utf-8">
        <script async src="https://cdn.ampproject.org/v0.js"></script>
        <title>BERGSOFT+</title>
        {% block amp-link %}{% amp_canonical_link request %}{% endblock %}
        <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
        <style amp-custom>
        {% block amp-custom %}
            {% include "amp/includes/style_amp_custom.css" %}
        {% endblock %}
        </style>
        {% block amp-ld-json %}{% endblock %}
        <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
      </head>
      <body>
        <header id="#top" class="amp-site-header">
            <div>
                <a href="{% url 'home_page' %}">
                    <amp-img src="{% static "images/v-2/logo.png" %}" width="145" height="35" class="amp-site-icon"></amp-img>
                    {% trans 'Web site development' %}
                </a>
            </div>
        </header>
        {% block content %}
        <h1>{% trans "Bergsoft+ company" %}</h1>
        {% endblock %}

        <footer class="amp-site-footer">
            <div>
                <h2>{% trans 'Web Development' %}</h2>
                <p>
                    &copy;&nbsp;{% now "Y" %} {{ site.name }}. {% trans "All rights reserved" %}.
                </p>
                <a href="#top" class="back-to-top">{% trans "Back to top" %}</a>
            </div>
        </footer>
      </body>
    </html>


In your app template folder (`blog`, for example) create folder `amp`

for blog detail page ``blog/tempplates/blog/post_detail.html``
create AMP version ``blog/tempplates/blog/amp/post_detail.html`` with content

.. code-block:: html+django

    {% extends "base_amp.html" %}
    {% load i18n blog_tags amp_tags %}
    {% load thumbnail staticfiles %}

    {% block content %}
    <article class="amp-post-article">
        <header class="amp-post-article-header">
            <h1 class="amp-post-title">{{ object.title|safe }}</h1>
            <div class="amp-post-meta amp-post-byline">
                {% if post.author.avatar %}
                    <amp-img src="{{ post.author.avatar.url }}" width="24" height="24" layout="fixed"></amp-img>
                {% endif %}
                <span class="amp-post-author author vcard"><i class="fa fa-user-o"></i>  {% trans "Posted by" %} {{ post.author }}</span>
            </div>

            <div class="amp-post-meta amp-post-posted-on">
                <i class="fa fa-calendar"></i> {{ post.published_at|date:"Y-m-d" }}
            </div>
        </header>
        {% if object.picture %}
        <figure class="amp-post-article-featured-image amp-caption">
            <amp-img src="{{ object.picture.url }}" width="738" height="430" alt="{{ object.title|striptags }}"></amp-img>
            {#<p class="amp-caption-text">{{ object.picture_caption|striptags }}</p>#}
        </figure>
        {% endif %}

        <div class="amp-post-article-content">
            {{ post.body_html|amp_safe }}
        </div>
        <footer class="amp-post-article-footer">
            <div class="amp-post-meta amp-post-tax-category">
                <i class="fa fa-folder-o"></i>
                <a href="{{ post.categories.all.0.get_absolute_url }}"> {{ post.categories.all.0 }}</a>
            </div>
            {% if post.tags %}
            <div class="amp-wp-meta amp-wp-tax-tag">
                <i class="fa fa-tags"></i>
                {% for tag in post.tags %}
                    <a href="{{ tag.get_absolute_url }}"> {{ tag }}</a>
                {% endfor %}
            </div>
            {% endif %}
        </footer>

    </article>
    {% endblock %}

we use filter `amp_safe` to convert all <img> into <amp-img> from {% load amp_tags %}
See result of this code here::
http://bergsoftplus.com/weblog/2016/11/28/internet-bezopasnost-pri-onlajn-pokupkah-20/?amp-content=amp


Settings
--------

.. _settings:

Here is a list of settings that are used by **django-amp-tools** and can be
changed in your own ``settings.py``:

``AMP_TOOLS_GET_PARAMETER``
    The name of GET parameter which check in ``AMPDetectionMiddleware``.

    **Default:** ``'amp-content'``

``AMP_TOOLS_GET_VALUE``
    The value of GET parameter which check in ``AMPDetectionMiddleware``.
    select AMP version.

    **Default:** ``'amp'``

``AMP_TOOLS_TEMPLATE_PREFIX``
    This string will be prefixed to the template names when searching for
    AMP templates. This is useful if you have many flavours and want to
    store them in a common subdirectory. Example:

    .. code-block:: python

        from django.template.loader import render_to_string
        from amp_tools import set_amp_detect

        set_amp_detect(is_amp_detect=True, request=request)
        render_to_string('index.html') # will render 'amp/index.html'

        # now add this to settings.py
        AMP_TOOLS_TEMPLATE_PREFIX = 'amp-new/'

        # and try again

        set_amp_detect(is_amp_detect=True, request=request)
        render_to_string('index.html') # will render 'amp-new/amp/index.html'

    **Default:** ``''`` (empty string)

``AMP_TOOLS_TEMPLATE_LOADERS``
    **django-mobile**'s template loader can load templates prefixed with the
    current flavour. Specify with this setting which loaders are used to load
    flavoured templates.

    **Default:** same as ``TEMPLATE_LOADERS`` setting but without
    ``'amp_tools.loader.Loader'``.

