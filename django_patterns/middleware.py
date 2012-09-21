#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.middleware ------------------------------------------===
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

# Django-core, configuration settings
from django.conf import settings

# Django-core, management commands
from django.core.management import call_command

# Django-core, middleware
from django.core.exceptions import MiddlewareNotUsed

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

class SyncDBOnStartupMiddleware(object):
  """This middleware will automagically run syncdb (and migrate if south is
  installed) the first time it is run, if it is detected that the project is
  using an in-memory SQLite database."""
  def __init__(self):
    # The following configuration settings is for Django 1.2+. Django < 1.2
    # would use settings.DATABASE_NAME
    if settings.DATABASES['default']['NAME'] == ':memory:':
      call_command('syncdb', interactive=False)
      if 'south' in settings.INSTALLED_APPS:
        call_command('migrate', interactive=False)
    # Mission accomplished; remove ourselves from MIDDLEWARE_CLASSES:
    raise MiddlewareNotUsed(_(u"Syncdb/migrate on startup complete."))

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
