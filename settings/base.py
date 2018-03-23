from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

SECRET_KEY = 'NeNZCQ4tr97(RnNb^($E.qB;(Qr234fQp7;.Mx*7k6DwKz7GKW'

DJANGO_APPS = (
    )

THIRD_PARTY_APPS = (
    'django_extensions',
    )

MY_APPS = (
    'parse',
    )

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MY_APPS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

USE_TZ = True
