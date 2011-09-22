#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order -------------------===
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
    # Ask Django nicely for the model class it has built.
    model = super(_InjectingModelBase, cls).__new__(cls, name, bases, attrs)

    # Try to add the _position field:
    try:
      # Create the IntegerField:
      position_field = models.IntegerField(editable=False, unique=True)
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

  @classmethod
  def get_front(cls):
    """Return the first element in the list."""
    manager = cls._positional_order_manager
    return manager.get(_position=0)

  @classmethod
  def get_back(cls):
    """Return the last element in the list."""
    manager = cls._positional_order_manager
    return manager.reverse()[:1].get()

  def get_object_at_offset(self, offset):
    """Get the object whose position is `offset` positions away from my
    own."""
    manager = self.__class__._positional_order_manager
    return manager.get(_position = self._position + offset)

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
    """Move element down one position."""
    # Get the element after this one.
    one_after = self.get_next()
    if one_after is not None:
      # Swap this element with the one that follows.
      self.swap(one_after)

  def move_up(self):
    """Move element up one position."""
    # Get the element before this one.
    one_before = self.get_prev()
    if one_before is not None:
      # Swap this element with the one prior.
      self.swap(one_before)

  def move_to_front(self):
    """Move element to the front of the list."""
    return self.insert_at(0)

  def move_to_back(self):
    """Move element to the end of the list."""
    return self.insert_at(self.get_back()._position)

  @transaction.commit_on_success
  def insert_at(self, position):
    """Moves the object to a specified position."""
    manager = self.__class__._positional_order_manager
    # Get the size of the list:
    size = manager.all().count()

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
      qs = manager.filter(
        _position__gte = position,
        _position__lt = old_position,
      ).order_by('-_position')
    else:
      idx = -1
      qs = manager.filter(
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
    """Swaps the position with some other class instance"""
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
    manager = self.__class__._positional_order_manager
    # Is there a position saved? (Explicitly testing None because 0 would be
    # False as well.)
    if self._position == None:
      # No, it was empty. Find one:
      try:
        # Set self's position to be the last element:
        self._position = self.get_back()._position + 1
      except self.DoesNotExist:
        # IndexError happened: the query did not return any objects, so this
        # has to be the first
        self._position = 0
    # Save the now properly set-up model:
    return super(PositionalOrderMixin, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    """Deletes the item from the list."""
    manager = self.__class__._positional_order_manager
    # get all objects with a position greater than this objects position
    objects_after = manager.filter(_position__gt=self._position)
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
