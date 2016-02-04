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

    If the setting NEWSCENTER_STORAGES does not exist, this function will return the default 
    storage class (specified under settings.DEFAULT_FILE_STORAGE). If it does exist, it will return 
    an instantiated object with the class being the 'ENGINE' setting in NEWSCENTER_STORAGES, and passing 
    all the arguments in the 'OPTIONS' setting of NEWSCENTER_STORAGES to the constructor.
    """


    if not hasattr(settings, 'NEWSCENTER_STORAGES'):
        return get_storage_class()
    else:
        newscenter_storage_class = get_storage_class(settings.NEWSCENTER_STORAGES['ENGINE'])
        return newscenter_storage_class(**settings.NEWSCENTER_STORAGES['OPTIONS'])


def get_newscenter_upload_to():
    """ Return UPLOAD_TO setting value
    If the setting NEWSCENTER_STORAGES does not exist, this returns 'newscenter/'
    """

    if not hasattr(settings, 'NEWSCENTER_STORAGES'):
        # 'newscenter' was the old UPLOAD_TO location before support for configurable storage
        # was added, this should be kept to ensure backwards compatibility.
        return 'newscenter/' 
    else:
        return settings.NEWSCENTER_STORAGES['UPLOAD_TO']
