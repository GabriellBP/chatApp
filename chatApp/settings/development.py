from ._base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

ALLOWED_HOSTS = []