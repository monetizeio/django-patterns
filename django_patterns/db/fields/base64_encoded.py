#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.fields.base64_encoded ----------------------------===
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
