#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.fields.uuid_field --------------------------------===
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

# ===----------------------------------------------------------------------===
# Copyright (c) 2007 Michael Trier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ===----------------------------------------------------------------------===

import uuid

from django.db.models import SubfieldBase, CharField

class UUIDVersionError(Exception):
  pass

try:
  import psycopg2.extras
  psycopg2.extras.register_uuid()
except ImportError:
  pass

class UUIDField(CharField):
  """UUIDField

  By default uses UUID version 1 (generate from host ID, sequence number and
  current time).

  The field support all uuid versions which are natively supported by the uuid
  python module. For more information see:
  
  <http://docs.python.org/lib/module-uuid.html>.
  """
  # Used so to_python() is called:
  __metaclass__ = SubfieldBase

  def __init__(self,
    verbose_name = None,
    name         = None,
    auto         = True,
    version      = 1,
    node         = None,
    clock_seq    = None,
    namespace    = None, **kwargs):
    kwargs['max_length'] = 36
    if auto:
      kwargs['blank'] = True
      kwargs.setdefault('editable', False)
    self.auto = auto
    self.version = version
    if version == 1:
      self.node, self.clock_seq = node, clock_seq
    elif version == 3 or version == 5:
      self.namespace, self.name = namespace, name
    super(UUIDField, self).__init__(verbose_name, name, **kwargs)

  def db_type(self, connection, *args, **kwargs):
    if 'postgres' in connection.settings_dict['ENGINE']:
      return 'uuid'
    return super(UUIDField, self).db_type(connection, *args, **kwargs)

  def get_internal_type(self):
    return "CharField"

  def contribute_to_class(self, cls, name):
    if self.primary_key:
      assert not cls._meta.has_auto_field, \
        "A model can't have more than one AutoField: %s %s %s; have %s" % \
         (self, cls, name, cls._meta.auto_field)
    super(UUIDField, self).contribute_to_class(cls, name)
    if self.primary_key:
      cls._meta.has_auto_field = True
      cls._meta.auto_field = self

  def create_uuid(self):
    if not self.version or self.version == 4:
      return uuid.uuid4()
    elif self.version == 1:
      return uuid.uuid1(self.node, self.clock_seq)
    elif self.version == 2:
      raise UUIDVersionError("UUID version 2 is not supported.")
    elif self.version == 3:
      return uuid.uuid3(self.namespace, self.name)
    elif self.version == 5:
      return uuid.uuid5(self.namespace, self.name)
    else:
      raise UUIDVersionError("UUID version %s is not valid." % self.version)

  def pre_save(self, model_instance, add):
    if self.auto and add and not getattr(model_instance, self.attname, None):
      value = self.create_uuid()
      setattr(model_instance, self.attname, value)
      return value
    else:
      value = super(UUIDField, self).pre_save(model_instance, add)
      if self.auto and not value:
        value = self.create_uuid()
        setattr(model_instance, self.attname, value)
    return value

  def db_type(self, connection):
    if 'postgres' in connection.settings_dict['ENGINE']:
      return 'uuid'
    return super(UUIDField, self).db_type(connection)

  def to_python(self, value):
    # For some inane reason `to_python()` is often called with already decoded
    # values. We protect against this by first checking if the passed in value
    # is an instance of `uuid.UUID`.
    if value and not isinstance(value, uuid.UUID):
      value = uuid.UUID(value)
    return value

  def get_db_prep_value(self, value, connection, prepared=False):
    # `get_db_prep_save()` can (and is) called with values that have already
    # been prepared. So we only prepare values which are instances of
    # `uuid.UUID`:
    if 'postgres' in connection.settings_dict['ENGINE']:
      return self.to_python(value) or None
    if isinstance(value, uuid.UUID):
      value = unicode(value)
    return value

  def south_field_triple(self):
    "Returns a suitable description of this field for South."
    # We'll just introspect the _actual_ field.
    from south.modelsinspector import introspector
    field_class = "django.db.models.fields.CharField"
    args, kwargs = introspector(self)
    # That's our definition!
    return (field_class, args, kwargs)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
