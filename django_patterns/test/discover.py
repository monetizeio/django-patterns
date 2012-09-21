#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.test.discover ---------------------------------------===
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

# In the django_patterns way of doing things, small testing applications
# reside throughout the source tree, close to the code which they are testing.
# In order for models defiend within these test applications to be created by
# the test runner, these apps need to be present in the INSTALLED_APPS. We'll
# take advantage of the new unittest2 discovery feature to find these testing
# applications in the source tree and add them to the end of INSTALLED_APPS.
#
# FIXME: Provide better documentation for this code.
def discover_test_apps(module):
  import os
  import sys
  import subprocess
  argv = []
  for arg in sys.argv:
    if arg.startswith('--settings=') or arg.startswith('--pythonpath'):
      argv.append(arg)
  argv = [
    os.path.abspath(os.path.join(os.getcwd(), sys.argv[0])),
    "discover_unittest_modules",
    ] + argv + [
    module,
  ]
  if argv[0] != os.path.abspath(sys.argv[0]) or argv[1] != sys.argv[1]:
    apps = subprocess.Popen(
      [sys.executable] + argv,
      stdout=subprocess.PIPE).communicate()[0]
    apps = list(set(apps.split('\n')))
    if '' in apps:
      apps.remove('')
    return apps

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
