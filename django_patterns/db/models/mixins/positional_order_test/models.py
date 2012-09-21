#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order_test.models -------===
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
  "Tests a model using positional order with respect to a ForeignKey field."
  other = ForeignKey(RelatedKeyModel)
  class Meta(object):
    order_with_respect_to = ('other',)

class SelfReferentialPositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  "Test a model using positional order with respect to itself."
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
  question = CharField(help_text=_(u"poll question"), max_length=200)
  pub_date = DateTimeField(help_text=_(u"date published"))
class PollChoicePositionalOrderModel(PositionalOrderMixin, UUIDStampedMixin):
  poll = ForeignKey(Poll, help_text=_(u"answer choice for a poll"))
  choice = CharField(help_text=_(u"poll choice"), max_length=200)
  votes = IntegerField(help_text=_(u"number of votes"))
  class Meta(object):
    order_with_respect_to = ('poll')

class Writer(Model):
  name = CharField(max_length=50, help_text='Use both first and last names.')
class BookPositionalOrderByAuthorModel(PositionalOrderMixin, UUIDStampedMixin):
  author = ForeignKey(Writer, blank=True, null=True)
  title = CharField(max_length=80)
  isbn = CharField(max_length=16, unique=True)
  class Meta:
    order_with_respect_to = ('author',)
class BookPositionalOrderByWorkModel(BookPositionalOrderByAuthorModel):
  class Meta:
    order_with_respect_to = ('author', 'title')
class ReversedBookPositionalOrderByWorkModel(PositionalOrderMixin, UUIDStampedMixin):
  author = ForeignKey(Writer, blank=True, null=True)
  title = CharField(max_length=80)
  isbn = CharField(max_length=16, unique=True)
  class Meta:
    order_with_respect_to = ('author', 'title')
class ReversedBookPositionalOrderByAuthorModel(ReversedBookPositionalOrderByWorkModel):
  class Meta:
    order_with_respect_to = ('author',)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
