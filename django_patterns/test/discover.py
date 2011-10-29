#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.test.discover ---------------------------------------===
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

##
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
