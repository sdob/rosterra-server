"""
Django settings for rosterra project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0!&btgbh%^5&e(4uaiy-(*p&szh&$eo09m!rlgk3pwv8+tkwss'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework', # REST API 
        'rest_framework.authtoken', # token-based authentication for DRF
        'sslserver', # SSL-enabled development server
        'corsheaders', # Enable CORS (Cross-Origin Resouce Sharing)
        'custom_auth', # our custom auth app
        'storages', # enable S3 storage
        'main', # main Rosterra app
        'country_utils', # quick and dirty country app
        'timezone_field', # store timezones in the db
        'django_nose', # better tests
        )

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware', # For CORS headers
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        )

ROOT_URLCONF = 'rosterra.urls'

WSGI_APPLICATION = 'rosterra.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Postgres db settings
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'rosterra_db',
            'HOST': 'localhost',
            'PORT': '5432',
            'USER': 'rosterra_user',
            'PASSWORD': 'pass'
            }
        }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
#STATIC_URL = '/static/'

###############################################################################
# Standard Django settings end here; below are very Rosterra-specific
# bits and pieces.
###############################################################################

# Custom user model (using email address as the username)
AUTH_USER_MODEL = 'custom_auth.User'

# Default 'from' email address for things like password resets
DEFAULT_FROM_EMAIL = 'no-reply@rosterra.com'

# Fixtures for test database
FIXTURE_DIRS = (
        'main',
        )

# REST Framework settings
REST_FRAMEWORK = {
        # Render as JSON only (no HTML or browsable API
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            ),
        # Token authentication only
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            )
        }

# CORS header settings. For development, these are whitelisted.
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
        #'localhost',
        #'http://localhost:9000',
        #'54.154.121.74',
        #'52.16.209.241:9000'
        #) 


#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATICFILES_LOCATION = 'static'
#STATICFILES_STORAGE = 'custom_storages.StaticStorage'
#STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

#MEDIAFILES_LOCATION = 'media'
#MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

# Use django-nose to run tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Heroku settings
import dj_database_url
# Set the db configuration to what Heroku wants if there's a DATABASE_URL 
# environment variable defined
if os.environ.has_key('DATABASE_URL'):
    # Parse database configuration from $DATABASE_URL
    DATABASES['default'] = dj_database_url.config()
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration (for Heroku)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
        )
