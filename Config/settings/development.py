import os

from .base import *

DEBUG = True
# ALLOWED_HOSTS = ['*', ]
ALLOWED_HOSTS = ['.vercel.app', '.now.sh']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        'ATOMIC_REQUESTS': True,
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Static Root is not for here
# pial added this for vercel


# print(STATICFILES_DIRS)
# print("000000000000000000000000000000000000000000")
# static/files
STATIC_ROOT = '/path/to/static/files'
# print(STATIC_ROOT)
# print("000000000000000000000000000000000000000000")
# /path/to/static/files
# STATIC_ROOT = config('STATIC_ROOT')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
