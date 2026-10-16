from cms.app_base import CMSAppConfig

from .cms_wizards import newscenter_wizard


class NewscenterCMSConfig(CMSAppConfig):
    cms_enabled = True
    cms_wizards = [newscenter_wizard]
