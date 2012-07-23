# -*- coding: utf-8 -*-

"""
Project: BugEx Online
Authors: Amir Baradaran
         Tim Krones
         Frederik Leonhardt
         Christos Monogios
         Akmal Qodirov
         Iliana Simova
         Peter Stahl
"""

from os import getcwd

# The current working directory,
# used for creating file paths which are
# independent of a particular computer.
ROOT_PATH = getcwd()

# A boolean that turns on/off debug mode.
# One of the main features of debug mode is
# the display of detailed error pages.
DEBUG = False

# A boolean that turns on/off template debug mode.
# If this is True, the fancy error page will display
# a detailed report for any exception raised during template rendering.
TEMPLATE_DEBUG = DEBUG

# The backend to use for sending emails.
# Only for debugging; prints emails to the console
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# A tuple that lists people who get code error notifications.
# When DEBUG=False and a view raises an exception, Django will
# email these people with the full exception information.
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

# A tuple in the same format as ADMINS that specifies
# who should get broken-link notifications when SEND_BROKEN_LINK_EMAILS=True.
MANAGERS = ADMINS

# A dictionary containing the settings for all databases
# to be used with Django. It is a nested dictionary whose contents
# maps database aliases to a dictionary containing the options
# for an individual database.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{0}/bugex_online_database.db'.format(ROOT_PATH),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and
# a single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '{0}/uploads'.format(ROOT_PATH)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '{0}/static'.format(ROOT_PATH)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '{0}/static_media'.format(ROOT_PATH),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3e96pdk2pclfz%ogoc50*d$w86b9k60ov_o(1djn3bq2)b1plj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# A string representing the full Python import path to your root URLconf.
# Can be overridden on a per-request basis by setting the attribute urlconf
# on the incoming HttpRequest object.
ROOT_URLCONF = 'bugex_online.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bugex_online.wsgi.application'

# List of locations of the template source files searched by
# django.template.loaders.filesystem.Loader, in search order.
TEMPLATE_DIRS = (
    '{0}/templates'.format(ROOT_PATH),
)

# A tuple of strings designating all applications that are
# enabled in this Django installation.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'bugex_webapp',
    #'captcha'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

APPLICATION_BASE_URL = 'http://localhost:8000'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bugexonline@gmail.com'
EMAIL_HOST_PASSWORD = 'eniln0xeguB'
#Admin variable.
#Here sees man the emails that are going to get emails when
#1)an HTTP error occurs
#2)a user submits the contact form
ADMINS = (('Admin', 'pemistahl@gmail.com'))
