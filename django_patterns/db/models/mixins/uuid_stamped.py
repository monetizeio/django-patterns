#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_stamped -----------------------===
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

# Django.core, database
import django.db.models

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

from django_patterns.db.fields import UUIDField

class UUIDStampedMixin(django.db.models.Model):
  """
  The UUIDStampedMixin leverages the database-independent UUIDField provided
  by the Django-patterns library, creating a Django model mixin that can be
  trivially added to the inheritance hierarchy of any abstract or concrete
  Django model, in the following way:

    class MyModel(UUIDStampedMixin):
      # That's it! UUIDStampedMixin inherits from django.db.models.Model, so
      # that does not need to be listed as a superclass, but you could also
      # (optionally) derive from other python classes as well.
      pass

  A model defined in this way is given a new database-backed read-only field,
  ‘uuid’, which stores a version 4 (random) UUID automatically assigned at
  creation time for each object instance.

  The UUID value is guaranteed to be unique among all instances of any (non-
  abstract) model that derives from UUIDStampedMixin. No guarantees are made
  that the UUID is in fact universally unique, but 2^61 instances are required
  before the likelihood of just a single collision reaches 50%. Seeing as just
  storing that many UUID values would exhaust a 64-bit address space, the
  possibility of collisions due to statistical chance can be ignored for all
  current applications, and nearly all conceivable applications, even far into
  the future.

  NOTE: There is implicit trust in the system's random number generator, both
        that the generated digits are sufficiently random (usually a safe
        assumption, but do your homework and make sure) and that the random
        number generator is properly seeded with real entropy. The latter
        could be a real problem, especially on virtualized infrastructure.
        System administrators: make sure that cloned VM instances are
        immediately seeded with a source of real entropy on first boot, well
        before the web stack is initialized!
  """
  # The UUIDField is provided by Django-patterns, and handles the details of
  # representing a UUID in various database backends. It is worth noting that
  # some database backends--most notably PostgreSQL--have native support for
  # UUID fields, although at the time of this writing the UUIDField of
  # Django-patterns is represented as a 36-character CharField regardless of
  # the database backend in use.
  uuid = UUIDField(
    verbose_name = _(u"universally unique identifier"),
    help_text = _(u"""
      An 128-bit identifier with a hard-guarantee of uniqueness among the
      objects of this model, and a reasonable statistical guarantee of
      universal uniqueness.
      """.strip()),

    # Version 4 UUID's are 128-bit identifiers with six specified bits and 122
    # randomly generated bits. Other UUID versions are either based on a
    # combined machine identification number and datetime, or a hash of some
    # value that uniquely identifies this asset. Random UUID's have better
    # statistical properties, are presumably faster to generate, and have less
    # likelihood of collision due to programmer or system administrator
    # negligence (conflicting domain spaces, reused initialization vectors,
    # etc.).
    version = 4,

    # The UUID field is automatically assigned at creation time and can never
    # change, so there is no reason to support empty values.
    null  = False,
    blank = False,

    # Once set, the UUID assigned to this object must never change. It is a
    # hard reference which uniquely identifies this object, and this object
    # only, and therefore may be subject to ForeignKey constraints or the
    # equivalent.
    editable = False,

    # The uniqueness constraint ensures that the UUID value remains unique for
    # any model which uses this mixin. It does not, however, ensure universal
    # uniqueness outside of the statistical likelihood of randomly generating
    # the same 122 bits twice. An alternative solution would have been to have
    # a site-wide UUID table using Django's support for generics, but that
    # would have come at the cost of lower performance (an extra JOIN) and far
    # more complicated code for a negligble benefit.
    unique = True,

    # The UUID field is to be automatically generated when the object is first
    # saved.
    auto = True,
  )

  ##################################
  ## Pythonic Instance Attributes ##
  ##################################

  def __init__(self, *args, **kwargs):
    super(UUIDStampedMixin, self).__init__(*args, **kwargs)

    # Pythonic instance attributes go here:
    pass

  ###############
  # Meta Fields #
  ###############

  def __unicode__(self):
    return u"%s" % unicode(self.uuid)

  class Meta:
    abstract = True

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
