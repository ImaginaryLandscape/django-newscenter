from django.core.files.storage import get_storage_class
from django.conf import settings


### AVAILABLE SETTINGS SAMPLE (with defaults)###
#NEWSCENTER_STORAGES = { 
#    'UPLOAD_TO': 'newscenter/',
#    'ENGINE': 'settings.DEFAULT_FILE_STORAGE',
#    'OPTIONS': {
#    }
#}


def get_newscenter_storage_class():
    """ Return either the default storage engine, or an instance of the speficied engine

    This function will either return the default storage class (specified under 
    settings.DEFAULT_FILE_STORAGE). OR, it will return an instatiated object with the class 
    being the 'ENGINE' setting in NEWSCENTER_STORAGES, and passing all the arguments in the 'OPTIONS' 
    setting of NEWSCENTER_STORAGES to the constructor.
    """

    if not hasattr(settings, 'NEWSCENTER_STORAGES'):
        return get_storage_class()()
    else:
        newscenter_storage_class = get_storage_class(settings.NEWSCENTER_STORAGES['ENGINE'])
        return newscenter_storage_class(**settings.NEWSCENTER_STORAGES['OPTIONS'])


def get_newscenter_upload_to():
    """ Return UPLOAD_TO setting value"""

    if not hasattr(settings, 'NEWSCENTER_STORAGES'):
        return 'newscenter/'
    else:
        return settings.NEWSCENTER_STORAGES['UPLOAD_TO']
