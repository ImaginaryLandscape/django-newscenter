from __future__ import absolute_import
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import NewsFeedPluginModel


class NewsFeedPlugin(CMSPluginBase):
    cache = False
    model = NewsFeedPluginModel
    module = _('Newscenter')
    name = _("News Feed Plugin")
    render_template = "newscenter/newsfeed_plugin.html"

    def render(self, context, instance, placeholder):
        articles = instance.location.articles.get_published()
        if not context['request'].user.is_authenticated():
            articles = articles.filter(private=False)
        context.update({'instance': instance, 'articles': articles[:instance.limit]})
        return context

plugin_pool.register_plugin(NewsFeedPlugin)
