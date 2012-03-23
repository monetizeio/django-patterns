#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.fields.base64_encoded ----------------------------===
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

"""Base64-encoded fields provide a method for storing variable-length, format-
unspecified binary objects (“blobs”) in a database-agnostic way (wrapped in
ASCII armor and placed in a `TextField`)."""

# Django-core, variable-length text field
from django.db.models import SubfieldBase, TextField

# Python standard library, RFC-3548 data encodings
from base64 import encodestring, decodestring

class Base64EncodedField(TextField):
  """A Django field suitable for storing binary objects (“blobs”), large or
  small, in an encoded format that is cross-platform/cross-database
  compatible."""
  # Used so to_python() is called:
  __metaclass__ = SubfieldBase

  # Prefix used to identify already-encoded strings:
  _prefix = 'Base64*+-/'

  def to_python(self, value):
    """Convert the Base64-encoded value to a Python string after it has been
    loaded from the database."""
    # For some inane reason `to_python()` is often called with already decoded
    # values. To protect against decoding twice (which may or may not raise an
    # exception), a prefix is added to encoded values and we check for that
    # here:
    if value is not None:
      if value.startswith(self._prefix):
        value = decodestring(value[len(self._prefix):])
    return value

  def get_prep_value(self, value):
    """Encode the passed-in Python string into Base64 in preparation for
    interaction with the database."""
    # `get_db_pref_save()` can (and is) called with values that have already
    # been encoded. We detect that by adding a prefix (which is removed by
    # `to_python()`):
    if value is not None:
      if not value.startswith(self._prefix):
        if isinstance(value, unicode):
          value = value.encode('utf-8')
        value = self._prefix + encodestring(value)
    return value

  def south_field_triple(self):
    """Returns a suitable description of this field for South."""
    # We'll just introspect the _actual_ field:
    from south.modelsinspector import introspector
    field_class = "django.db.models.fields.TextField"
    args, kwargs = introspector(self)
    # That's our definition!
    return (field_class, args, kwargs)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
