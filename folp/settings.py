"""Local development settings. Not a production deployment configuration."""
from pathlib import Path
import os
import secrets

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = BASE_DIR / '.local-secret'
if not os.environ.get('DJANGO_SECRET_KEY') and not secret_file.exists():
    secret_file.write_text(secrets.token_urlsafe(50))
    secret_file.chmod(0o600)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or secret_file.read_text()
DEBUG = True
ALLOWED_HOSTS = ['*']  # Unrestricted prototype hosts, as requested.
INSTALLED_APPS = [
    'core', 'wagtail.contrib.forms', 'wagtail.contrib.redirects',
    'wagtail.embeds', 'wagtail.sites', 'wagtail.users', 'wagtail.snippets',
    'wagtail.documents', 'wagtail.images', 'wagtail.search', 'wagtail.admin',
    'wagtail', 'modelcluster', 'taggit', 'django.contrib.admin',
    'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]
ROOT_URLCONF = 'folp.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'],
              'APP_DIRS': True, 'OPTIONS': {'context_processors': [
                  'django.template.context_processors.request', 'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages', 'core.context.navigation']}}]
WSGI_APPLICATION = 'folp.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WAGTAIL_SITE_NAME = 'Friends of Larkhall Park'
# Admin navigation uses relative URLs on the current host and port.
# This prototype sends no notification emails requiring an absolute admin URL.
SILENCED_SYSTEM_CHECKS = ['wagtailadmin.W003']
WAGTAILSEARCH_BACKENDS = {'default': {'BACKEND': 'wagtail.search.backends.database'}}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
