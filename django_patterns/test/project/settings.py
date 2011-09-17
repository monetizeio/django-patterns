#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.test.project.settings -------------------------------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
# as an unpublished work.
#
# RokuSigma Inc. (the “Company”) Confidential
#
# NOTICE: All information contained herein is, and remains the property of the
# Company. The intellectual and technical concepts contained herein are
# proprietary to the Company and may be covered by U.S. and Foreign Patents,
# patents in process, and are protected by trade secret or copyright law.
# Dissemination of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained from the
# Company. Access to the source code contained herein is hereby forbidden to
# anyone except current Company employees, managers or contractors who have
# executed Confidentiality and Non-disclosure agreements explicitly covering
# such access.
#
# The copyright notice above does not evidence any actual or intended
# publication or disclosure of this source code, which includes information
# that is confidential and/or proprietary, and is a trade secret, of the
# Company. ANY REPRODUCTION, MODIFICATION, DISTRIBUTION, PUBLIC PERFORMANCE,
# OR PUBLIC DISPLAY OF OR THROUGH USE OF THIS SOURCE CODE WITHOUT THE EXPRESS
# WRITTEN CONSENT OF THE COMPANY IS STRICTLY PROHIBITED, AND IN VIOLATION OF
# APPLICABLE LAWS AND INTERNATIONAL TREATIES. THE RECEIPT OR POSSESSION OF
# THIS SOURCE CODE AND/OR RELATED INFORMATION DOES NOT CONVEY OR IMPLY ANY
# RIGHTS TO REPRODUCE, DISCLOSE OR DISTRIBUTE ITS CONTENTS, OR TO MANUFACTURE,
# USE, OR SELL ANYTHING THAT IT MAY DESCRIBE, IN WHOLE OR IN PART.
# ===----------------------------------------------------------------------===

"""Settings for the Django test project. This test project exists for the
purpose of being able to run test cases which must be executed from within a
Django environment, and to provide context for an interactive Python shell
with the Django framework for development purposes. It is NOT an example of
how to setup a project's settings to use the django_patterns application."""

##
# During execution of the test suite, DEBUG and associated settings are
# ignored and set to False internally by Django as a convenience so that the
# testing environment more closely matches production. DEBUG=True has been
# kept here so that interactive shells will launch with debugging features
# enabled, as is most useful for development purposes.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

##
# ADMINS and MANAGERS are notified via email when unhandled exceptions are
# raised and when 404 status codes are returned, respectively. These should
# NEVER be set in a testing environment as throwing exceptions and accessing
# invalid URL's are inherently a part of testing. The person running the test
# or the continuous integration system will be notified if a test fails or if
# the test suite is broken for either of these reasons.
ADMINS = ()
MANAGERS = ADMINS

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

##
# Local time zone for this installation. Choices can be found here:
# <http://en.wikipedia.org/wiki/List_of_tz_zones_by_name>, although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

##
# Language code for this installation. All choices can be found here:
# <http://www.i18nguy.com/unicode/language-identifiers.html>.
LANGUAGE_CODE = 'en-us'

##
# Used by the sites framework, SITE_ID specifies which site this settings file
# is for. Multiple sites may be hosted from the same codebase (see the
# django.contrib.sites framework for more information).
SITE_ID = 1

##
# If you set this to False, Django will make some optimizations so as not to
# load the internationalization machinery.
USE_I18N = True

##
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

##
# Absolute filesystem path to the directory that will hold user-uploaded
# files. Example:
#
# MEDIA_ROOT = "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

##
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash. Examples:
#
# MEDIA_URL = "http://media.lawrence.com/media/"
# MEDIA_URL = "http://example.com/media/"
MEDIA_URL = ''

##
# Absolute path to the directory static files should be collected to. Don't
# put anything in this directory yourself; store your static files in apps'
# "static/" subdirectories and in STATICFILES_DIRS. Example:
#
# STATIC_ROOT = "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

##
# URL prefix for static files. Example:
#
# STATIC_URL = "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

##
# URL prefix for admin static files -- CSS, JavaScript and images. Make sure
# to use a trailing slash. Examples:
#
# ADMIN_MEDIA_PREFIX = "http://foo.com/static/admin/"
# ADMIN_MEDIA_PREFIX = "/static/admin/"
ADMIN_MEDIA_PREFIX = '/static/admin/'

##
# Additional locations of static files.
STATICFILES_DIRS = (
  # Put strings here, like "/home/html/static" or "C:/www/django/static".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)

##
# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#  'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

##
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ic_2((w)dg%7c)gd$&u_6$gjpt6swc5z464rgh)-1(euv)d5^_'

##
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
#   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (
  # Put strings here, like "/home/html/django_templates" or
  #   "C:/www/django/templates".
  # Always use forward slashes, even on Windows.
  # Don't forget to use absolute paths, not relative paths.
)

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

##
# The django_nose test runner uses nose under the hood (obviously) and is
# better than the default Django test runner in that it can discover and run
# tests in source files spread throughout the project (this allows tests to be
# written near the code that being tested), generates better reports, and has
# a better framework for extending its functionality through plug-ins.
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

##
# A sample logging configuration. The only tangible logging performed by this
# configuration is to send an email to the site admins on every HTTP 500
# error. See <http://docs.djangoproject.com/en/dev/topics/logging> for more
# details on how to customize your logging configuration.
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'mail_admins': {
      'level': 'ERROR',
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

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
