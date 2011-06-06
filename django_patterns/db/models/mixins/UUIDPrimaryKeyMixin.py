#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.UUIDPrimaryKeyMixin ----------------===
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

# Django.core, database
import django.db.models

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

# Django-extensions, additional model fields
import django_extensions.db.fields

class UUIDPrimaryKeyMixin(django.db.models.Model):
  """
  The UUIDPrimaryKeyMixin leverages the database-independent UUIDField
  provided by the Django-extensions library, creating a Django model mixin
  that can be trivially added to the inheritance hierarchy of any abstract or
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
  id = django_extensions.db.fields.UUIDField(
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
    return u"{%s}" % unicode(self.id)

  class Meta:
    abstract = True

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
