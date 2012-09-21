#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.management.commands.discover_unittest_modules -------===
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
Runs the test auto-discover functionality of unittest2 on the applications
specified, and prints to the console a list a modules which need to be added
to INSTALLED_APPS when the test suite is run. If no applications are specified
then the auto-discover is run on all applications in INSTALLED_APPS.
"""

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
