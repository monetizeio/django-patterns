#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === tests/path_hack.py --------------------------------------------------===
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

# PROJECT_DIRECTORY is the directory on the file system which contains the
# Django project this settings file is a part of. It is used so many times
# that it deserves its own variable for efficiency and clarity.
import os
PROJECT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# We need the module django_patterns to be accessible from the Python path. Do
# not use this as an example of what to do in your own projects! Under normal
# circumstances this is most properly done using virtualenv and pip to install
# django_patterns into the site-packages directory of a project-specific
# virtual environment.
import sys
sys.path.insert(0, os.path.abspath(os.path.join(PROJECT_DIRECTORY, '..')))

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
