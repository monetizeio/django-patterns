#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === tests/manage.py -----------------------------------------------------===
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

import os
import sys

try:
  from django.core.management import execute_from_command_line
except ImportError:
  sys.stderr.write(
    # The following is not transalated because in this particular error
    # condition ``sys.path`` is probably not setup correctly, and so we cannot
    # be sure that we'd import the translation machinery correctly. It'd be
    # better to print the correct error in English than to trigger another
    # not-so-helpful ImportError.
    u"Error: Can't find the module 'django.core.management' in the Python "
    u"path. Please execute this script from within the virtual environment "
    u"containing your project.\n")
  sys.exit(1)

if __name__ == '__main__':
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
  execute_from_command_line(sys.argv)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
