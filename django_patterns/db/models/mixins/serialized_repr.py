#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.serialized_repr --------------------===
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

"Mixins providing serialized output by default for `repr()` on Django models."

# Django.core, object-relational mapper
from django.db.models import Model

# Django.core, serialization framework
from django.core.serializers import get_serializer

class SerializedReprMixin(Model):
  """The parent class of all serialized `repr()` mixins, providing the base
  functionality."""
  def __init__(self, serialization_format, *args, **kwargs):
    """Takes a single required parameter `serialization_format`, and sets up
    the instance with a Django serializer to that format."""
    # Perform initialization of superclasses:
    super(SerializedReprMixin, self).__init__(*args, **kwargs)
    # Create and save a Django serializer:
    self._serializer = get_serializer(serialization_format)()

  # Debugging/interactive representation:
  def __repr__(self):
    return self._serializer.serialize((self,))

  # Meta fields:
  class Meta(object):
    abstract = True

class XMLSerializedReprMixin(SerializedReprMixin):
  """Provides XML serialization for `repr()` by default."""
  def __init__(self, *args, **kwargs):
    """Initialize the XML serializer."""
    # Specify XML serialization:
    serialization_format = kwargs.pop('serialization_format', 'xml')
    # SerializedReprMixin will handle the rest:
    super(XMLSerializedReprMixin, self).__init__(serialization_format, *args,
      **kwargs)
  # Meta fields:
  class Meta(object):
    abstract = True

class JSONSerializedReprMixin(SerializedReprMixin):
  """Provides JSON serialization for `repr()` by default."""
  def __init__(self, *args, **kwargs):
    """Initialize the JSON serializer."""
    # Specify JSON serialization:
    serialization_format = kwargs.pop('serialization_format', 'json')
    # SerializedReprMixin will handle the rest:
    super(JSONSerializedReprMixin, self).__init__(serialization_format, *args,
      **kwargs)
  # Meta fields:
  class Meta(object):
    abstract = True

class YAMLSerializedReprMixin(SerializedReprMixin):
  """Provides YAML serialization for `repr()` by default."""
  def __init__(self, *args, **kwargs):
    """Initialize the YAML serializer."""
    # Specify YAML serialization:
    serialization_format = kwargs.pop('serialization_format', 'yaml')
    # SerializedReprMixin will handle the rest:
    super(YAMLSerializedReprMixin, self).__init__(serialization_format, *args,
      **kwargs)
  # Meta fields:
  class Meta(object):
    abstract = True

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
