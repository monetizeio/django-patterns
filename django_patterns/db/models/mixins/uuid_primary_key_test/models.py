#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_primary_key_test.models -------===
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
