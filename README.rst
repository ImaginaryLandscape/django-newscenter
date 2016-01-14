=================
Django Newscenter
=================

A Django application for creating news releases which can be associated with unique newsroom objects.

A Django CMS apphook is included as well as a templatetag for rendering news release headlines in non-application templates.

Django 1.5 and up

Installation
============

Add newscenter to your python path:
    $ pip install newscenter

Add the following to the INSTALLED_APPS of your project's settings.py:
    'newscenter',

In your urls.py, add:
    url(r'^newscenter/', include('newscenter.urls')),

For Django <1.6 Run:
    ``manage.py syncdb`` (or ``manage.py migrate`` if you're using south)

For Djanveo >1.7:

   Add or Update the MIGRATION_MODULES dictionary in django settings as follows

     MIGRATION_MODULES = {
         'newscenter': 'newscenter.migrations_django',
     }

   Then Run:
   ``manage.py migrate``

 Collect static media:

   ``manage.py collectstatic``


Dependencies
============

The following will be installed automatically if you use pip to install newscenter:

    Pillow (http://python-pillow.github.io/)

    easy-thumbnails (https://github.com/SmileyChris/easy-thumbnails)

    feedparser (http://pythonhosted.org/feedparser/)

For easy-thumbnails, you'll also need to add it to INSTALLED_APPS and run syncdb or migrate:
    'easy_thumbnails',

Change Log
============
New in 1.5.8:
-Added support for Django 1.7

New in 1.4.1:
-Added title field to Contact model

New in 1.4:
-Switched image plugin from popeye to bxslider


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
