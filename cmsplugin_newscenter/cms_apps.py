from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class NewsCenter(CMSApp):
    app_name = "newscenter"
    name = _("News Center")
    
    def get_urls(self, page=None, language=None, **kwargs):
        return ["newscenter.urls"]

apphook_pool.register(NewsCenter)
