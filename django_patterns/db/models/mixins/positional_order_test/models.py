#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order_test.models -------===
# Copyright © 2011, RokuSigma Inc. (Mark Friedenbach <mark@roku-sigma.com>)
# as an unpublished work.
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

# Django-core, object-relational mapper
from django.db.models import Model, CharField, DateTimeField, ForeignKey, \
  IntegerField, ManyToManyField, OneToOneField

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

# Django-patterns, positional-order mixin
from django_patterns.db.models.mixins import PositionalOrderMixin, \
  UUIDPrimaryKeyMixin, UUIDStampedMixin

class SimplePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Implements the simplest positional order model possible--a model that
  simply derives from PositionalOrderMixin. The UUIDStampedMixin is for
  testing purposes, so that each model instance can be uniquely identified."""
  pass

class SimplePositionalOrderWithEmptyTupleModel(PositionalOrderMixin, UUIDStampedMixin):
  """A model nearly identical to SimplePositionalOrderModel, testing that if
  `order_with_respect_to = ()` is specified, the behavior is the same."""
  class Meta(object):
    order_with_respect_to = ()

class SimplePositionalOrderWithSelfModel(PositionalOrderMixin, UUIDStampedMixin):
  """A model nearly identical to SimplePositionalOrderModel, testing that if
  `order_with_respect_to = 'self'` is specified, the behavior is the same."""
  class Meta(object):
    order_with_respect_to = 'self'

class RelatedKeyModel(UUIDPrimaryKeyMixin):
  """The ‘related’ model for OneToOneField, ForeignKey, and ManyToManyField
  tests of PositionalOrderMixin."""
  pass

class OneToOnePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to a OneToOneField (not
  a common occurrence, but officially supported nonetheless)."""
  other = OneToOneField(RelatedKeyModel)
  class Meta(object):
    order_with_respect_to = ('other',)

class ForeignKeyPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to a ForeignKey
  field."""
  other = ForeignKey(RelatedKeyModel)
  class Meta(object):
    order_with_respect_to = ('other',)

class SelfReferentialPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Test a model using positional order with respect to itself."""
  parent = ForeignKey('self', related_name='children', null=True)
  class Meta:
    order_with_respect_to = ('parent',)

class DjangoCompatiblePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to a ForeignKey using
  the field name instead of a tuple (the Django compatibility case)."""
  other = ForeignKey(RelatedKeyModel)
  class Meta(object):
    order_with_respect_to = 'other'

class ManyToManyPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to a
  ManyToManyField."""
  other = ManyToManyField(RelatedKeyModel)
  class Meta(object):
    order_with_respect_to = ('other',)

class ReverseManyToManyPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to a related field.
  Tricky!"""
  class Meta(object):
    order_with_respect_to = ('other',)
class ReverseRelatedModel(Model):
  other = ManyToManyField(ReverseManyToManyPositionalOrderModel,
    related_name='other',
  )

# We obviously cannot test every combination of possible fields to order with
# respect to. So far we have covered the relevant edge cases with the above
# models testing positional order with respect to ForeignKey, OneToOneField,
# and ManyToManyField. We'll conclude this section with a test of ordering
# with respect to an IntegerField (a stand-in for all of the remaining field
# types), before moving on to testing various scenarios (including ordering
# with respect to multiple fields).
class IntegerPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """Tests a model using positional order with respect to just an
  IntegerField."""
  playlist = IntegerField(blank=False, null=False)
  class Meta(object):
    order_with_respect_to = ('playlist',)

class Poll(Model):
  """"""
  question = CharField(help_text=_(u"poll question"), max_length=200)
  pub_date = DateTimeField(help_text=_(u"date published"))
class PollChoicePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  """"""
  poll = ForeignKey(Poll, help_text=_(u"answer choice for a poll"))
  choice = CharField(help_text=_(u"poll choice"), max_length=200)
  votes = IntegerField(help_text=_(u"number of votes"))
  class Meta(object):
    order_with_respect_to = ('poll')

class Writer(Model):
  """"""
  name = CharField(max_length=50, help_text='Use both first and last names.')
class BookPositionalOrderByAuthorModel(PositionalOrderMixin, UUIDStampedMixin):
  """"""
  author = ForeignKey(Writer, blank=True, null=True)
  title = CharField(max_length=80)
  isbn = CharField(max_length=16, unique=True)
  class Meta:
    order_with_respect_to = ('author',)
class BookPositionalOrderByWorkModel(BookPositionalOrderByAuthorModel):
  """"""
  class Meta:
    order_with_respect_to = ('author', 'title')
class ReversedBookPositionalOrderByWorkModel(PositionalOrderMixin, UUIDStampedMixin):
  """"""
  author = ForeignKey(Writer, blank=True, null=True)
  title = CharField(max_length=80)
  isbn = CharField(max_length=16, unique=True)
  class Meta:
    order_with_respect_to = ('author', 'title')
class ReversedBookPositionalOrderByAuthorModel(ReversedBookPositionalOrderByWorkModel):
  """"""
  class Meta:
    order_with_respect_to = ('author',)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
