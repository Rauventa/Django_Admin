from .settings_default import *

SECRET_KEY = '123'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'files', 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'files', 'static')
