from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import NewsFeedPluginModel


class NewsFeedPlugin(CMSPluginBase):
    model = NewsFeedPluginModel
    module = _('Newscenter')
    name = _("News Feed Plugin")
    render_template = "newscenter/newsfeed_plugin.html"

    def render(self, context, instance, placeholder):
        articles = instance.location.articles.get_published()[:instance.limit]
        context.update({'instance': instance, 'articles': articles})
        return context

plugin_pool.register_plugin(NewsFeedPlugin)
