#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.management.commands.discover_unittest_modules -------===
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

"""Runs the test auto-discover functionality of unittest2 on the applications
specified, and prints to the console a list a modules which need to be added
to INSTALLED_APPS when the test suite is run. If no applications are specified
then the auto-discover is run on all applications in INSTALLED_APPS."""

import os
import inspect

# Django-core, management commands
from django.core.management.base import BaseCommand

# Django-core, project settings
from django.conf import settings

# Python standard library, unit-testing framework
from django.utils import unittest

class Command(BaseCommand):
  args = '[app_name another_app ...]'
  help = __doc__.strip()

  # In short, this command uses the unittest2 library (included in the Django
  # distribution) to do autodiscovery of tests. It then builds a list of the
  # modules containing said tests which could possibly be a Django application
  # as well. These candidate appilcations are sorted and printed to stdout.
  #
  # FIXME: Fully document this method.
  def handle(self, *args, **options):
    apps = []
    if not len(args):
      args = settings.INSTALLED_APPS
    for arg in args:
      try:
        module = __import__(arg)
        filename = inspect.getfile(module)
        top_dir = os.path.abspath(os.path.join(os.path.dirname(filename), '..'))
      except:
        continue
      loader = unittest.TestLoader()
      suite = loader.discover(
        start_dir     = arg,
        pattern       = r'*.py',
        top_level_dir = top_dir,
      )
      while len(suite._tests):
        obj = suite._tests.pop(0)
        if isinstance(obj, unittest.TestSuite):
          suite._tests.append(obj._tests)
        elif isinstance(obj, list):
          if len(obj):
            suite._tests.extend(obj)
        else:
          l = obj.__module__.split('.')
          while l:
            app = '.'.join(l)
            del l[-1]
            try:
              __import__('.'.join([app, 'models']))
            except ImportError:
              continue
            apps.append(app)
    apps = list(set(apps))
    for app in settings.INSTALLED_APPS:
      if app in apps:
        apps.remove(app)
    apps.sort()
    print "\n".join(apps)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
