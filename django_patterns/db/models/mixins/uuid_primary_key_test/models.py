#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_primary_key_test.models -------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
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

# Django-core, object relational mapper
import django.db.models

# Django-patterns, object relational mapper mixins
from django_patterns.db.models.mixins import UUIDPrimaryKeyMixin

class UUIDPrimaryKeyModel(UUIDPrimaryKeyMixin):
  """
  A more complex sample model which inherits from UUIDPrimaryKeyMixin and uses
  the inherited ‘uuid’ field as the model's primary key. The auto-assigned and
  randomly generated ‘uuid’ will be its only database-backed field.

  NOTE: Although this behavior is supported, it is generally not recommended
        unless its use is absolutely required. As of the time of this writing
        UUIDField (which UUIDPrimaryKeyMixin is built upon) is still
        represented as a CharField even on databases which support a native
        UUID type. Using a CharField as a primary key can have atrocious
        performance consequences.
  """
  class Meta(object):
    ordering     = ['id']
    verbose_name = u"UUID primary-key model"

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
