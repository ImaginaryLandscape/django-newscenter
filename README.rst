=================
Django Newscenter
=================

A Django application for creating news releases which can be associated with unique newsroom objects.

A Django CMS apphook is included as well as a templatetag for rendering news release headlines in non-application templates.

Now compatible with Django 1.5.

Installation
============

Add newscenter to your python path:
    $ pip install newscenter

Add the following to the INSTALLED_APPS of your project's settings.py:
    'newscenter',

In your urls.py, add:
    url(r'^newscenter/', include('newscenter.urls')),

Run:
    ``manage.py syncdb`` (or ``manage.py migrate`` if you're using south) and ``manage.py collectstatic``

Dependencies
============

The following will be installed automatically if you use pip to install newscenter:

    PIL (http://www.pythonware.com/products/pil/)

    easy-thumbnails (https://github.com/SmileyChris/easy-thumbnails)

    feedparser (http://pythonhosted.org/feedparser/)

For easy-thumbnails, you'll also need to syncdb or migrate, then add it to INSTALLED_APPS:
    'easy_thumbnails',

Template Tag
============

The template tag can be used like this::

    {% load newscenter_tags %}
    {% get_news "newsroom-name" %}
    <h1><a href="{{ newsroom.get_absolute_url }}">{{ newsroom.name }}</a></h1>
    {% for release in featured_list %}
    <article>
    <h2>{{ release.title }}</h2>
    <p class="teaser">{{ release.teaser }}</p>
    <p><a href="{{ release.get_absolute_url }}">Read more</a></p>
    </article>
    {% endfor %}
   

