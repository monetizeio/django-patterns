#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order_test.models -------===
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

# Django-core, object-relational mapper
from django.db import models

# Django-patterns, positional-order mixin
from django_patterns.db.models.mixins import PositionalOrderMixin, \
  UUIDStampedMixin

class SimplePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Implements the simplest positional order model possible--a model that
  simply derives from PositionalOrderMixin. The UUIDStampedMixin is for
  testing purposes, so that each model instance can be uniquely identified."""
  pass

class SimplePositionalOrderWithEmptyTupleModel(PositionalOrderMixin, UUIDStampedMixin):
  """A model nearly identical to SimplePositionalOrderModel, testing that if
  `order_with_respect_to = ()` is specified, the behavior is the same."""
  class Meta(object):
    order_with_respect_to = ()

class SimplePositionalOrderWithSelfModel(PositionalOrderMixin, UUIDStampedMixin):
  """A model nearly identical to SimplePositionalOrderModel, testing that if
  `order_with_respect_to = 'self'` is specified, the behavior is the same."""
  class Meta(object):
    order_with_respect_to = 'self'

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
