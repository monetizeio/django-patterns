#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.fields.uuid_field --------------------------------===
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

""""""

from django.db.models import SubfieldBase, CharField

import uuid

class UUIDVersionError(Exception):
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
    """"""
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
    CharField.__init__(self, verbose_name, name, **kwargs)

  def get_internal_type(self):
    """"""
    # FIXME: Should later expand to include UUID types if the database
    #        supports it.
    return CharField.__name__

  def contribute_to_class(self, cls, name):
    """"""
    if self.primary_key:
      assert not cls._meta.has_auto_field, \
        "A model can't have more than one AutoField: %s %s %s; have %s" % \
         (self, cls, name, cls._meta.auto_field)
    super(UUIDField, self).contribute_to_class(cls, name)
    if self.primary_key:
      cls._meta.has_auto_field = True
      cls._meta.auto_field = self

  def create_uuid(self):
    """"""
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
    """"""
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

  def to_python(self, value):
    """"""
    # For some inane reason `to_python()` is often called with already decoded
    # values. We protect against this by first checking if the passed in value
    # is an instance of `uuid.UUID`.
    if value and not isinstance(value, uuid.UUID):
      value = uuid.UUID(value)
    return value

  def get_prep_value(self, value):
    """"""
    # `get_db_pref_save()` can (and is) called with values that have already
    # been prepared. So we only prepare values which are instances of
    # `uuid.UUID`:
    if isinstance(value, uuid.UUID):
      value = unicode(value)
    return value

  def south_field_triple(self):
    """"""
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
