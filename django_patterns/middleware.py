#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.middleware ------------------------------------------===
# Copyright © 2011-2012, RokuSigma Inc. and contributors as an unpublished
# work. See AUTHORS for details.
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
