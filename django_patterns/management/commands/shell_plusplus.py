#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.management.commands.shell_plusplus ------------------===
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

"""Extends the shell_plus command provided by django_extensions to include
added features, such as initialization of the database when using an in-memory
SQLite instance."""

# Django-extensions, management commands
from django_extensions.management.commands import shell_plus

class Command(shell_plus.Command):
  def handle_noargs(self, *args, **kwargs):
    # Re-use the SyncDBOnStartupMiddleware code, which envokes ‘syncdb’ and
    # ‘migrate’ if in-memory databases are detected:
    from django.core.exceptions import MiddlewareNotUsed
    from django_patterns.middleware import SyncDBOnStartupMiddleware
    try:
      SyncDBOnStartupMiddleware()
    except MiddlewareNotUsed:
      pass
    # Pass control to Django-extension's shell_plus command:
    super(Command, self).handle_noargs(*args, **kwargs)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
