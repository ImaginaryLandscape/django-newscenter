from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NewsCenter(CMSApp):
    name = _("News Center")
    urls = ["newscenter.urls"]

apphook_pool.register(NewsCenter)
