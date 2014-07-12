"""
Django settings for iTeam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

#############################
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
#############################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

################################
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
################################

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR' #en-us'

TIME_ZONE = 'Europe/Paris' # default : 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


##################################
# Files location
##################################
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(SITE_ROOT, 'static') # dont uncomment, the css are not found anymore

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'static'),
)

# Absolute path to template directory (/Library/Python/2.7/site-packages/django)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Should Django serve the static and media files ? This should not be set to
# True in a production environment
SERVE = True


###############################
# Dev options for debug
###############################

# Make this unique, and don't share it with anybody.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z3rte+c4hikqi-csxbs2&j#+5%nwwbe=ki0j957a^i1%k-hs^^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


##################################
# Stuff divers
##################################

# Application definition

INSTALLED_APPS = (
    'iTeam.pages',
    'iTeam.member',
    'iTeam.publications',
    'iTeam.medias',
    'iTeam.events',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'email_obfuscator',
    'schedule',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'iTeam.urls'

WSGI_APPLICATION = 'iTeam.wsgi.application'

############################################
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
############################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


##########################################
# iTeam settings
##########################################

NB_PUBLICATIONS_PER_PAGE = 10
NB_MEMBERS_PER_PAGE = 10

SIZE_MAX_IMG = 10*1024*1024
SIZE_MAX_TITLE = 100

LOGIN_URL = '/membres/connexion/'


#####################################
# schedule (django-scheduler)
#####################################
FIRST_DAY_OF_WEEK = 1 # default : 0 = Sunday


#############################################
#
# LOGGING
#
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#
# Levels :
# DEBUG: Low level system information for debugging purposes
# INFO: General system information
# WARNING: Information describing a minor problem that has occurred.
# ERROR: Information describing a major problem that has occurred.
# CRITICAL: Information describing a critical problem that has occurred.
##############################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            'format': '\tDefault : %(levelname)s %(asctime)s %(message)s'
        },
        'request': {
            'format': '\tRequest : %(levelname)s %(status_code)d %(message)s'
        },
        'backends_simple': {
            'format': '\tBackends : %(levelname)s %(asctime)s %(duration)s'
        },
        'backends_verbose': {
            'format': '\tBackends : %(levelname)s %(asctime)s %(duration)s %(sql)s %(params)s'
        },
    },

    'handlers': {
        'default':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'request':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'request'
        },
        'backends':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'backends_simple'
        },
        #'db':{
        #    'level': 'INFO',
        #    'class': 'iTeam.utils.MyDbLogHandler',
        #    'formatter': 'verbose'
        #}
    },

    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['backends'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


######################################
# Production settings
#
# Load the production settings from the settings_prod.py file. This will
# override some settings from this file as needed, like the SECRET_KEY and
# other production stuff.
#######################################

try:
    from iTeam.settings_prod import *
except ImportError:
    pass
