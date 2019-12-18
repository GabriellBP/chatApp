from ._base import *
import django_heroku

# DEVELOPMENT VARIABLES
SECURE_HSTS_SECONDS = 30
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# HOST
ALLOWED_HOSTS = ['mathema-api.herokuapp.com']

# Activate Django-Heroku.
django_heroku.settings(locals())
