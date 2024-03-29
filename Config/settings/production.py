import os
import dj_database_url
from decouple import Csv

from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = config('DEBUG', cast=bool)
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', 'booking-core-demo.vercel.app', ]
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT', cast=int),
#         'ATOMIC_REQUESTS': True,
#     }
# }

DATABASES = {'default': dj_database_url.config(default="postgres://default:gS5WeU2jOxPh@ep-withered-wood-90832038.us-east-1.postgres.vercel-storage.com:5432/verceldb")}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'booking_core'
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'booking_core',
#         'USER': 'booking_user',
#         'PASSWORD': 'booking',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'ATOMIC_REQUESTS': True,
#     }
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# STATIC_URL = '/static/'
STATIC_URL = 'static/'
# STATIC_ROOT = config('STATIC_ROOT')

STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL = 'media/'
# MEDIA_ROOT = config('MEDIA_ROOT')
# /path/to/media/files
# settings.py
MEDIA_ROOT = '/tmp/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# MEDIA_ROOT = '/path/to/media/files'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': config('CACHE_LOCATION'),
#     }
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
}
