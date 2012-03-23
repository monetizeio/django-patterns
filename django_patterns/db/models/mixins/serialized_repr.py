#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.serialized_repr --------------------===
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
