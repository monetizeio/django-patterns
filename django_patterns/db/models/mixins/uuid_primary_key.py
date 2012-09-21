#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_primary_key -------------------===
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

# Django.core, database
import django.db.models

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

from python_patterns.utils.decorators import Property

from django_patterns.db.fields import UUIDField

class UUIDPrimaryKeyMixin(django.db.models.Model):
  """
  The UUIDPrimaryKeyMixin leverages the database-independent UUIDField
  provided by the Django-patterns library, creating a Django model mixin that
  can be trivially added to the inheritance hierarchy of any abstract or
  concrete Django model, in the following way:

    class MyModel(UUIDPrimaryKeyMixin):
      # That's it! UUIDPrimaryKeyMixin inherits from django.db.models.Model,
      # so that does not need to be listed as a superclass, but you could also
      # (optionally) derive from other python classes as well.
      pass

  A model defined in this way is given a new database-backed, read-only, auto-
  generated, primary-key field, ‘id’, which stores a version 4 (random) UUID
  assigned at creation time for each object instance. This value replaces the
  integer primary-key ‘id’ that is typically added by the Django ORM.

  The UUID value is guaranteed to be unique among all instances of any (non-
  abstract) model that derives from UUIDPrimaryKeyMixin. No guarantees are
  made that the UUID is in fact universally unique, but 2^61 instances are
  required before the likelihood of just a single collision reaches 50%.
  Seeing as just storing that many UUID values would exhaust a 64-bit address
  space, the possibility of collisions due to statistical chance can be
  ignored for all current applications, and nearly all conceivable
  applications, even far into the future.

  NOTE: There is implicit trust in the system's random number generator, both
        that the generated digits are sufficiently random (usually a safe
        assumption, but do your homework and make sure) and that the random
        number generator is properly seeded with real entropy. The latter
        could be a real problem, especially on virtualized infrastructure.
        System administrators: make sure that cloned VM instances are
        immediately seeded with a source of real entropy on first boot, well
        before the web stack is initialized!
  """
  # Please see the documentation accompanying UUIDStampedMixin for an
  # explanation of the UUIDField and the various parameters passed to it.
  id = UUIDField(
    verbose_name = _(u"universally unique identifier"),
    help_text = _(u"""
      An 128-bit identifier with a hard-guarantee of uniqueness among the
      objects of this model, and a reasonable statistical guarantee of
      universal uniqueness. Acts as primary key for the model.
      """.strip()),
    version  = 4,
    null     = False,
    blank    = False,
    editable = False,
    unique   = True,
    auto     = True,

    # This setting tells Django that
    primary_key = True
  )

  @Property
  def uuid():
    """
    An alias for ‘id’, the UUID primary-key. This alias exists so that code
    can work interchangeably with objects that derive from UUIDStampedMixin
    (and therefore have a regular ‘uuid’ field) and those that derive from
    UUIDPrimaryKeyMixin (and therefore have ‘id’ as their UUID value).

    NOTE: fset() and fdel() are set on this property, despite having no real
          semantic value. Django configures the Python class for models in
          such a way that one can assign values to a primary-key and delete
          fields entirely. These operations have no semantic value and cause
          validation errors when one tries to save the now modified instance.
          Defining fset() and fdel() ensures that there is absolutely no
          detectable between UUIDPrimaryKeyMixin.id and
          UUIDPrimaryKeyMixin.uuid.
    """.strip()
    def fget(self):
      return self.id
    def fset(self, value):
      self.id = value
    def fdel(self):
      del self.id
    return locals()

  ##################################
  ## Pythonic Instance Attributes ##
  ##################################

  def __init__(self, *args, **kwargs):
    super(UUIDPrimaryKeyMixin, self).__init__(*args, **kwargs)

    # Pythonic instance attributes go here:
    pass

  ###############
  # Meta Fields #
  ###############

  def __unicode__(self):
    return u"%s" % unicode(self.id)

  class Meta:
    abstract = True

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
