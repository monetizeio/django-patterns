#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order -------------------===
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

"""This module provides PositionalOrderMixin, a mixin for Django models which
provides automatic ordering based on an injected `position` integer field."""

# Django.core, object-relational mapper
from django.db import models, transaction
from django.db.models.fields import FieldDoesNotExist

# Django.core, translation
from django.utils.translation import ugettext_lazy as _

class _InjectingModelBase(models.base.ModelBase):
  """This helper metaclass is used by PositionalOrderMixin. It injects a new
  IntegerField named ‘position’, which holds information about the position of
  the element in its list."""

  def __new__(cls, name, bases, attrs):
    """Metaclass constructor calling Django and then modifying the resulting
    class."""

    ##
    # Ask Django nicely for the model class it has built.
    model = super(_InjectingModelBase, cls).__new__(cls, name, bases, attrs)

    ##
    # Try to add the position field.
    try:
      # Create the IntegerField.
      position_field = models.IntegerField(editable=False, unique=True)

      ##
      # Try injecting the position field into the class.
      try:
        # Attempt to get the `position` field
        model._meta.get_field('position')
      except FieldDoesNotExist:
        # It was not found - create it now
        model.add_to_class('position', position_field)

      ##
      # Set position as the first field to order. Of course this gets overridden
      # when using database queries which request another ordering method
      # (order_by).
      if 'position' not in model._meta.ordering:
        model._meta.ordering = ['position'] + list(model._meta.ordering)

    except AttributeError:
      # add_to_class was not yet added to the class. No problem, this is
      # called twice by Django; add_to_class will appear later.
      pass

    ##
    # We're done - output the class, it's ready for use.
    return model

class PositionalOrderMixin(models.Model):
  """This mixin class implements a user defined order in the database. To
  apply this mixin you need to inherit from it before you inherit from
  `models.Model`. It adds an IntegerField called `position` to your model. Be
  careful, it overwrites any existing field that you might have defined.
  Additionally, this mixin changes the default ordering behavior to order by
  the position field.

  Take care: your model needs to have a manager which returns all objects set
  as default manager, that is, the first defined manager. It does not need to
  be named `objects`. Future versions of this mixin may inject its own,
  private manager."""
  # Assign a metaclass which injects the positional field.
  __metaclass__ = _InjectingModelBase

  def __init__(self, *args, **kwargs):
    """Initialize the class and set up some positional magic."""
    # Initialize superclasses first.
    super(PositionalOrderMixin, self).__init__(self, *args, **kwargs)

  @classmethod
  def get_front(cls):
    """Return the first element in the list."""
    return cls._default_manager.get(position=0)

  @classmethod
  def get_back(cls):
    """Return the last element in the list."""
    return cls._default_manager.reverse()[:1].get()

  def get_object_at_offset(self, offset):
    """Get the object whose position is `offset` positions away from my
    own."""
    return self.__class__._default_manager.get(
      position = self.position + offset
    )

  def get_next(self):
    """Return the element immediately following this one."""
    try:
      return self.get_object_at_offset(1)
    except self.DoesNotExist:
      return None

  def get_prev(self):
    """Return the element immediately prior to this one."""
    try:
      return self.get_object_at_offset(-1)
    except self.DoesNotExist:
      return None

  def move_down(self):
    """Move element one position down."""
    # Get the element after this one.
    one_after = self.get_next()
    if one_after is not None:
      # Swap this element with the one that follows.
      self.swap(one_after)

  def move_up(self):
    """Move element one position up."""
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
    # Get the object manager for the class:
    manager = self.__class__._default_manager
    return self.insert_at(self.get_back().position)

  @transaction.commit_on_success
  def insert_at(self, position):
    """Moves the object to a specified position."""
    # Get the object manager for the class:
    manager = self.__class__._default_manager
    # Get the size of the list:
    size = manager.all().count()

    ##
    # Early exits:
    if self.position == position:
      return
    if not position in xrange(0, size):
      raise IndexError, u"invalid position"

    ##
    # Move the element to be inserted out of the way, so we have an empty cell
    # to work with.
    old_position = self.position
    self.position = size
    self.save()

    ##
    # Shift each item in between the two positions over by one, to compensate
    # for the move.
    if position < old_position:
      idx = 1
      qs = manager.filter(
        position__gte = position,
        position__lt = old_position,
      ).order_by('-position')
    else:
      idx = -1
      qs = manager.filter(
        position__gt = old_position,
        position__lte = position,
      ).order_by('position')
    for element in qs:
      element.position += idx
      element.save()

    ##
    # Assign the element to the now-empty cell.
    self.position = position
    self.save()

  def insert_before(self, other):
    """Inserts an object in the database so that it will be ordered just
    before the `other` object - this has to be of the same type, of course."""
    # we only need to call another method and prepare the proper parameters
    if self.position < other.position:
      self.insert_at(other.position - 1)
    else:
      self.insert_at(other.position)

  def insert_after(self, other):
    """Inserts an object in the database so that it will be ordered just
    behind the `other` object - this has to be of the same type, of course."""
    # we only need to call another method and prepare the proper parameters
    if self.position <= other.position:
      self.insert_at(other.position)
    else:
      self.insert_at(other.position + 1)

  @transaction.commit_on_success
  def swap(self, other):
    """Swaps the position with some other class instance"""
    # Save the current position:
    current_position = self.position
    # Set own position to special, temporary position:
    self.position = -1
    self.save()
    # Exchange the two positions:
    self.position, other.position = other.position, current_position
    for obj in (other, self):
      obj.save()

  def save(self, *args, **kwargs):
    """Saves the model to the database. It populates the `position` field of
    the model automatically if there is no such field set. In this case, the
    element will be appended at the end of the list."""
    manager = self.__class__._default_manager
    # is there a position saved? (explicitly testing None because 0 would be false as well)
    if self.position == None:
      # no, it was empty. Find one
      try:
        # Set self's position to be the last element:
        self.position = self.get_back().position + 1
      except self.DoesNotExist:
        # IndexError happened: the query did not return any objects, so this
        # has to be the first
        self.position = 0

    # save the now properly set-up model
    return super(PositionalOrderMixin, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    """Deletes the item from the list."""
    manager = self.__class__._default_manager
    # get all objects with a position greater than this objects position
    objects_after = manager.filter(position__gt=self.position)
    # now we remove this model instance
    # so the `position` is free and other instances can fill this gap
    super(PositionalOrderMixin, self).delete(*args, **kwargs)

    # iterate through all objects which were found
    for element in objects_after:
      # decrease the position in the list (means: move forward)
      element.position -= 1
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
