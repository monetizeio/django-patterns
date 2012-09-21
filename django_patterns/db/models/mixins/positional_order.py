#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order -------------------===
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

"""This module provides PositionalOrderMixin, a mixin for Django models which
provides automatic ordering based on an injected `_position` integer field.
This pattern provides a superset of the functionality of Django's built-in
`order_with_respect_to` Meta option, and is based on the following Django
snippet (heavily modified):

<http://djangosnippets.org/snippets/259/>"""

# Django.core, object-relational mapper
from django.db import models, transaction
from django.db.models.fields import FieldDoesNotExist

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

class _InjectingModelBase(models.base.ModelBase):
  """This helper metaclass is used by PositionalOrderMixin. It inspects the
  Meta option `order_with_respect_to` and in most cases injects into the model
  a new IntegerField named `_position`, which holds information about the
  position of the element relative to other elements with the same ordering
  key.

  If `order_with_respect_to` specifies a single ForeignKey field (or a
  OneToOneField), the methods `get_RELATED_order()` and `set_RELATED_order()`
  are added to the related model (with the same semantics as the default
  Django behavior)."""

  def __new__(cls, name, bases, attrs):
    """Metaclass constructor calling Django and then modifying the resulting
    class."""

    # Extract the `order_with_respect_to`, and do some preprocessing to get it
    # in standard form.
    try:
      # Extract the `order_with_respect_to` configuration option from the Meta
      # attribute. This will raise a `KeyError` if there is no Meta attribute,
      # or an `AttributeError` if order_with_respect_to is not specified.
      owrt = attrs['Meta'].order_with_respect_to
      del attrs['Meta'].order_with_respect_to

      # For compatibility with existing Django functionality, it is possible
      # to specify `order_with_respect_to` as a string specifying a single
      # attribute. Note that in Python 2.x `isinstance(obj,str)` is not the
      # same as `isinstance(obj,unicode)`.
      if isinstance(owrt, basestring):
        owrt = (owrt,)
      else:
        owrt = tuple(owrt)

      # Specifying `'self'` or `('self',)` is the same as `()`. We'll
      # explicitly unify these cases.
      if 'self' in owrt:
        if len(owrt) is not 1:
          raise ValueError, _(u"‘self’ cannot be combined with other fields in order_with_respect_to expression.")
        else:
          owrt = ()

    # See the first two lines of the try block for the source of these
    # exceptions:
    except (KeyError, AttributeError):
      owrt = ()

    # Save the `order_with_respect_to` configuration parameter to our own
    # attribute. While doing so, we check to see if a subclass has provided a
    # different `order_with_respect_to`, in which case we use that.
    try:
      owrt = attrs['_positional_order_with_respect_to']
    except KeyError:
      attrs['_positional_order_with_respect_to'] = owrt

    # Ask Django nicely for the model class it has built.
    model = super(_InjectingModelBase, cls).__new__(cls, name, bases, attrs)

    # Try to add the _position field:
    try:
      # Create the IntegerField:
      position_field = models.IntegerField(editable=False, unique=False)
      # Try injecting the _position field into the class:
      try:
        # Attempt to get the `_position` field:
        model._meta.get_field('_position')
      except FieldDoesNotExist:
        # It was not found--create it now:
        model.add_to_class('_position', position_field)

      # Set _position as the first field to order by. Of course this gets
      # overridden when using database queries which request another ordering
      # method vis the order_by method.
      if '_position' not in model._meta.ordering:
        model._meta.ordering = ['_position'] + list(model._meta.ordering)

      # Inject the default manager if one was never provided.
      try:
        # Attempt to get the `objects` field:
        model._meta.get_field('objects')
      except FieldDoesNotExist:
        # It was not found--create it now:
        model.add_to_class(
          'objects',
          models.Manager()
        )

    except AttributeError:
      # add_to_class was not yet added to the class. No problem, this is
      # called twice by Django; add_to_class will appear later.
      pass

    # We're done--output the class, it's ready for use:
    return model

class _PositionalOrderManager(models.Manager):
  def get_query_set(self):
    return super(_PositionalOrderManager, self).get_query_set()

def _match_args(params, *args, **kwargs):
  args = dict(zip(params, args))

  # Check for duplicates
  argkeys = args.keys()
  kwakeys = kwargs.keys()
  for key in argkeys:
    if key in kwakeys:
      if args['key'] is not kwargs['key']:
        raise ValueError, _(u"parameter %s given different values in args and kwargs")

  # Combine dictionaries and return:
  kwargs.update(args)
  return kwargs

class PositionalOrderMixin(models.Model):
  """This mixin class implements a user defined order in the database. To
  apply this mixin you need to inherit from it, as follows:

    from django_patterns.db.models.mixins import PositionalOrderMixin
    class MyOrderedModel(PositionalOrderMixin):
      # That's it! Because `PositionalOrderMixin` inherits from
      # `django.db.models.Model`, you don't need to explicitly include it as a
      # superclass.
      pass

  PositionalOrderMixin adds an IntegerField called `_position` to your model.
  Additionally, this mixin adds its own manager, and modifies the default
  manager (creating one if necessary) to have the default ordering behavior of
  ordering by the _position field."""
  # Assign a metaclass which injects the `_position` field.
  __metaclass__ = _InjectingModelBase

  _positional_order_manager = _PositionalOrderManager()

  def get_positional_list_kwargs(self):
    """Returns a dictionary specifying the instance values for the fields this
    model has an `order_with_respect_to` constraint. This dictionary is
    suitable for use as kwargs to a queryset filter, for which the results are
    guaranteed to have unique `_position` fields."""
    def getattr_or_None(obj, attr):
      try:
        return getattr(obj, attr)
      except ValueError:
        return None
    return dict(zip(
      self._positional_order_with_respect_to,
      map(
        lambda x: getattr_or_None(self, x),
        self._positional_order_with_respect_to,
      ),
    ))

  @classmethod
  def get_front(cls, *args, **kwargs):
    "Return the first element in the list."
    # Combine args and kwargs based on `order_with_respect_to`:
    kwargs = _match_args(cls._positional_order_with_respect_to, *args, **kwargs)
    manager = cls._positional_order_manager
    return manager.get(_position=0, **kwargs)

  @classmethod
  def get_back(cls, *args, **kwargs):
    "Return the last element in the list."
    # Combine args and kwargs based on `order_with_respect_to`:
    kwargs = _match_args(cls._positional_order_with_respect_to, *args, **kwargs)
    manager = cls._positional_order_manager
    return manager.filter(**kwargs).reverse()[:1].get()

  def get_object_at_offset(self, offset):
    "Get the object whose position is `offset` positions away from my own."
    kwargs = self.get_positional_list_kwargs()
    manager = self.__class__._positional_order_manager
    return manager.get(_position = self._position + offset, **kwargs)

  def get_next(self):
    """Return the element immediately following this one, or None at the end
    of the list."""
    try:
      return self.get_object_at_offset(1)
    except self.DoesNotExist:
      return None

  def get_prev(self):
    """Return the element immediately prior to this one, or None at the start
    of the list."""
    try:
      return self.get_object_at_offset(-1)
    except self.DoesNotExist:
      return None

  def move_down(self):
    "Move element down one position."
    # Get the element after this one.
    one_after = self.get_next()
    if one_after is not None:
      # Swap this element with the one that follows.
      self.swap(one_after)

  def move_up(self):
    "Move element up one position."
    # Get the element before this one.
    one_before = self.get_prev()
    if one_before is not None:
      # Swap this element with the one prior.
      self.swap(one_before)

  def move_to_front(self):
    "Move element to the front of the list."
    return self.insert_at(0)

  def move_to_back(self):
    "Move element to the end of the list."
    kwargs = self.get_positional_list_kwargs()
    return self.insert_at(self.get_back(**kwargs)._position)

  @transaction.commit_on_success
  def insert_at(self, position):
    "Moves the object to a specified position."
    kwargs = self.get_positional_list_kwargs()
    manager = self.__class__._positional_order_manager
    # Get the size of the list:
    size = manager.filter(**kwargs).count()

    # Early exits:
    if self._position == position:
      return
    if not position in xrange(0, size):
      raise IndexError, _(u"invalid position")

    # Move the element to be inserted out of the way, so we have an empty cell
    # to work with.
    old_position = self._position
    self._position = size
    self.save()

    # Shift each item in between the two positions over by one, to compensate
    # for the move.
    if position < old_position:
      idx = 1
      qs = manager.filter(**kwargs).filter(
        _position__gte = position,
        _position__lt = old_position,
      ).order_by('-_position')
    else:
      idx = -1
      qs = manager.filter(**kwargs).filter(
        _position__gt = old_position,
        _position__lte = position,
      ).order_by('_position')
    for element in qs:
      element._position += idx
      element.save()

    # Assign the element to the now-empty cell.
    self._position = position
    self.save()

  def insert_before(self, other):
    """Inserts an object in the database so that it will be ordered just
    before the `other` object - this has to be of the same type, of course."""
    # we only need to call another method and prepare the proper parameters
    if self._position < other._position:
      self.insert_at(other._position - 1)
    else:
      self.insert_at(other._position)

  def insert_after(self, other):
    """Inserts an object in the database so that it will be ordered just
    behind the `other` object - this has to be of the same type, of course."""
    # we only need to call another method and prepare the proper parameters
    if self._position <= other._position:
      self.insert_at(other._position)
    else:
      self.insert_at(other._position + 1)

  @transaction.commit_on_success
  def swap(self, other):
    "Swaps the position with some other class instance"
    # Save the current position:
    current_position = self._position
    # Set own position to special, temporary position:
    self._position = -1
    self.save()
    # Exchange the two positions:
    self._position, other._position = other._position, current_position
    for obj in (other, self):
      obj.save()

  def save(self, *args, **kwargs):
    """Saves the model to the database. It populates the `position` field of
    the model automatically if there is no such field set. In this case, the
    element will be appended at the end of the list."""
    # Is there a position saved? (Explicitly testing None because 0 would be
    # False as well.)
    if self._position == None:
      # No, it was empty. Find one:
      try:
        # Set self's position to be the last element:
        last = self.get_back(**self.get_positional_list_kwargs())
        self._position = last._position + 1
      except self.DoesNotExist:
        # IndexError happened: the query did not return any objects, so this
        # has to be the first
        self._position = 0
    # Save the now properly set-up model:
    return super(PositionalOrderMixin, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    "Deletes the item from the list."
    manager = self.__class__._positional_order_manager
    # get all objects with a position greater than this objects position
    objects_after = manager.filter(_position__gt=self._position,
      **self.get_positional_list_kwargs())
    # now we remove this model instance
    # so the `position` is free and other instances can fill this gap
    super(PositionalOrderMixin, self).delete(*args, **kwargs)

    # iterate through all objects which were found
    for element in objects_after:
      # decrease the position in the list (means: move forward)
      element._position -= 1
      element.save()

  ##################################
  ## Pythonic Instance Attributes ##
  ##################################

  def __init__(self, *args, **kwargs):
    super(PositionalOrderMixin, self).__init__(*args, **kwargs)

    # Pythonic instance attributes go here:
    pass

  ###############
  # Meta Fields #
  ###############

  class Meta:
    abstract = True

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
