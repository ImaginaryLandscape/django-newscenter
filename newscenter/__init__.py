from django.conf import settings

try:
    import site_config
    class NewscenterSiteConfig(site_config.SiteConfigBase):
        application_short_name = "newscenter"
        application_verbose_name = "News Release Application"
        
        # Optionally override if you want to customize the backend
        # used for a given config.
        def get_backend(self):
            backend = getattr(settings, 'SITECONFIG_BACKEND_DEFAULT',
                'site_config.backends.model_backend.DatabaseBackend')
            return backend
             
        def get_default_configs(self):
            return {
                'NEWSCENTER_IMAGE_HEIGHT':{ 'default':600, 
                    'field':'django.forms.IntegerField', 
                    'help':'Uploaded image height in px.'}, 
                'NEWSCENTER_IMAGE_WIDTH':{ 'default':800, 
                    'field':'django.forms.IntegerField', 
                    'help':'Uploaded image width in px.'},
                'NEWSCENTER_IMAGE_QUALITY':{ 'default':100, 
                    'field':'django.forms.IntegerField', 
                    'help':'Uploaded image quality between 1-100.'}
            }
         
    site_config.registry.config_registry.register(NewscenterSiteConfig)
except:
    pass
