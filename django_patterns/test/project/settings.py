#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.test.project.settings -------------------------------===
# Copyright © 2011-2012, RokuSigma Inc. and contributors. See AUTHORS for more
# details.
#
# Some rights reserved.
#
# Redistribution and use in source and binary forms of the software as well as
# documentation, with or without modification, are permitted provided that the
# following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  * The names of the copyright holders or contributors may not be used to
#    endorse or promote products derived from this software without specific
#    prior written permission.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE AND
# DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ===----------------------------------------------------------------------===

"""
Settings for the Django test project. This test project exists for the purpose
of being able to run test cases which must be executed from within a Django
environment, and to provide context for an interactive Python shell with the
Django framework for development purposes. It is NOT an example of how to
setup a project's settings to use the django_patterns application.
"""

###############
# Environment #
###############

# PROJECT_DIRECTORY is the directory on the file system which contains the
# Django project this settings file is a part of. It is used so many times
# that it deserves its own variable for efficiency and clarity.
import os
PROJECT_DIRECTORY = os.path.abspath(
  os.path.join(os.path.dirname(__file__), '..'))

##################
# Debug Settings #
##################

# During execution of the test suite, DEBUG and associated settings are
# ignored and set to False internally by Django as a convenience so that the
# testing environment more closely matches production. DEBUG=True has been
# kept here so that interactive shells will launch with debugging features
# enabled, as is most useful for development purposes.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

##########################
# Administrative Contact #
##########################

# ADMINS and MANAGERS are notified via email when unhandled exceptions are
# raised and when 404 status codes are returned, respectively. These should
# NEVER be set in a testing environment as throwing exceptions and accessing
# invalid URL's are inherently a part of testing. The person running the test
# or the continuous integration system will be notified if a test fails or if
# the test suite is broken for either of these reasons.
ADMINS = ()
MANAGERS = ADMINS

#########################
# Session Configuration #
#########################

from random import choice
SECRET_KEY = ''.join(choice('0123456789abcdef') for x in xrange(64)).decode('hex')

##########################
# Database Configuration #
##########################

DATABASES = {
  'default': {
    # An in-memory SQLite database is sufficient for testing purposes in a
    # local development environment. On a continuous integration server, the
    # production database server should be used instead. The build scripts can
    # adjust these settings by specifing their own settings file.
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
}

#############
# Timezones #
#############

# Local time zone for this installation. Choices can be found here:
# <http://en.wikipedia.org/wiki/List_of_tz_zones_by_name>, although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#########################################
# Internationalization and Localization #
#########################################

# Language code for this installation. All choices can be found here:
# <http://www.i18nguy.com/unicode/language-identifiers.html>.
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not to
# load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

##########################
# Template Configuration #
##########################

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or
  #   "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
  os.path.abspath(os.path.join(PROJECT_DIRECTORY, 'templates')),
)

TEMPLATE_CONTEXT_PROCESSORS = (
  "django.contrib.auth.context_processors.auth",
  "django.core.context_processors.csrf",
  "django.core.context_processors.debug",
  "django.core.context_processors.i18n",
  "django.core.context_processors.media",
  "django.core.context_processors.static",
  "django.contrib.messages.context_processors.messages",
)

############################
# Middleware Configuration #
############################

MIDDLEWARE_CLASSES = (
  # Run syncdb and migrate on first run if an in-memory database is used.
  'django_patterns.middleware.SyncDBOnStartupMiddleware',

  # Standard Django middlewares:
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#####################
# URL Configuration #
#####################

ROOT_URLCONF = 'tests.urls'

#########################
# Logging Configuration #
#########################

# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500 error
# when DEBUG=False. See <http://docs.djangoproject.com/en/dev/topics/logging>
# for more details on how to customize your logging configuration.
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

#############################
# Application Configuration #
#############################

INSTALLED_APPS = (
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # Uncomment the next line to enable the admin:
  # 'django.contrib.admin',
  # Uncomment the next line to enable admin documentation:
  # 'django.contrib.admindocs',

  # Django-extensions is a dependency of Django-patterns, and provides the
  # ever-useful shell_plus command for launching an ipython interactive
  # development shell.
  'django_extensions',

  # Our Django application, which provides setup and utilities for assisting
  # test discovery.
  'django_patterns',

  # Replaces the default Django test runner with nose's, which is much more
  # capable at auto-discovery of tests and provides a better framework for
  # report generation and plug-in functionality.
  'django_nose',
)

#=--------------------=#
# django.contrib.sites #
#=--------------------=#

# Used by the sites framework, SITE_ID specifies which site this settings file
# is for. Multiple sites may be hosted from the same codebase (see the
# django.contrib.sites framework for more information).
SITE_ID = 1

#=--------------------------=#
# django.contrib.staticfiles #
#=--------------------------=#

# Absolute filesystem path to the directory that will hold user-uploaded
# files. Example:
#
# MEDIA_ROOT = "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash. Examples:
#
# MEDIA_URL = "http://media.lawrence.com/media/"
# MEDIA_URL = "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to. Don't
# put anything in this directory yourself; store your static files in apps'
# "static/" subdirectories and in STATICFILES_DIRS. Example:
#
# STATIC_ROOT = "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files. Example:
#
# STATIC_URL = "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files.
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#  'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

#=-----------=#
# django_nose #
#=-----------=#

# The django_nose test runner uses nose under the hood (obviously) and is
# better than the default Django test runner in that it can discover and run
# tests in source files spread throughout the project (this allows tests to be
# written near the code that being tested), generates better reports, and has
# a better framework for extending its functionality through plug-ins.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
