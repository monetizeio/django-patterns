#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.positional_order_test.tests --------===
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

# Django-core, testing
from django.test import TestCase

# Python standard library, unit-testing framework
from django.utils import unittest

# The number of instances which are created in the TestCase's setUp() method.
# Must be a positive integer.
INSTANCE_COUNT = 4

from models import *

def _uuid_list(queryset):
  return map(lambda x: x.uuid, queryset)

def _position_list(queryset):
  return map(lambda x: x._position, queryset)

# Returns an interable containing the keyword arguments necessary to access
# each positional list currently stored in the model.
def _each_position_list(model):
  try:
    order_with_respect_to = list(model._positional_order_with_respect_to)
  except (AttributeError, TypeError):
    return [{}]
  if len(order_with_respect_to) < 1:
    return [{}]
  return map(
    lambda x: model.objects.get(_position=0, **x).get_positional_list_kwargs(),
    map(
      lambda x: dict(zip(order_with_respect_to, x)),
      set(model.objects.values_list(*order_with_respect_to)),
    ),
  ) or [{}]

class PositionalOrderModelTests(TestCase):
  """Tests models which use PositionalOrderMixin to create an automatically
  managed ordering based on an added unique integer `_position` field."""
  _model = SimplePositionalOrderModel

  def setUp(self):
    # Perform setup operations defined by any superclass.
    super(PositionalOrderModelTests, self).setUp()

    # Multiple objects are generated in order to test the auto-generation and
    # uniqueness features of the UUID field.
    for i in xrange(0, INSTANCE_COUNT):
      obj = self._model()
      obj.save()

  def test_objects_created_successfully(self):
    """Tests that instance objects can be successfully created."""
    for kwargs in _each_position_list(self._model):
      self.assertEqual(
        self._model.objects.filter(**kwargs).count(),
        INSTANCE_COUNT,
      )

  def test_default_ordering(self):
    """Tests that the default manager orders objects by `_position`."""
    for kwargs in _each_position_list(self._model):
      # Note: The Django queryset method reverse() has no effect unless a
      #       default ordering exists or an ordering has been specified with
      #       order_by(). We know that our test model does not specify a
      #       default ordering and we don't use order_by(), so reverse() will
      #       have an effect only if PositionSortMixin injected a default
      #       ordering (as it is supposed to).
      forward = _uuid_list(self._model.objects.filter(**kwargs))
      reverse = _uuid_list(self._model.objects.filter(**kwargs).reverse())

      # Undo the reverse ordering, assuming that the queryset reverse() had any
      # effect at all.
      reverse.reverse()

      # Compare the two lists. They should be the same if and only if the
      # queryset reverse() had an effect, which would only be the case if
      # PositionSortMixin injected a default ordering.
      self.assertEqual(forward, reverse)

  def test_position_is_index(self):
    """Tests that the `_position` field is an index into the default ordering
    of all objects."""
    for kwargs in _each_position_list(self._model):
      positions = _position_list(self._model.objects.filter(**kwargs))
      for expected, actual in zip(xrange(0, len(positions)), positions):
        self.assertEqual(expected, actual)

  def test_new_objects_push_to_back(self):
    """Tests that new objects are placed at the end of the list."""
    for kwargs in _each_position_list(self._model):
      obj = self._model(**kwargs)
      obj.save()
      self.assertEqual(
        self._model.objects.filter(**kwargs).order_by('-_position')[0].uuid,
        obj.uuid,
      )

  def test_delete_updates_position(self):
    """Tests that deleting an element updates the position of the elements
    that follow."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Delete the middle element and compare:
      from math import floor
      idx = int(floor(size/2))
      self._model.objects.filter(**kwargs).get(_position=idx).delete()
      oids = oids[:idx] + oids[idx+1:]
      self.assertEqual(oids, _uuid_list(self._model.objects.filter(**kwargs)))

      if len(oids):
        # Delete from the beginning of the list and compare:
        self._model.objects.filter(**kwargs).get(_position=0).delete()
        oids = oids[1:]
        self.assertEqual(oids, _uuid_list(self._model.objects.filter(**kwargs)))

      if len(oids):
        # Delete from the end of the list and compare:
        self._model.objects.filter(**kwargs).order_by('-_position')[0].delete()
        oids = oids[0:len(oids)-1]
        self.assertEqual(oids, _uuid_list(self._model.objects.filter(**kwargs)))

  def test_get_positional_list_kwargs(self):
    """Test that get_positional_list_kwargs() returns a dictionary identifying
    the positional list which includes the passed in instance."""
    for kwargs in _each_position_list(self._model):
      for element in self._model.objects.filter(**kwargs):
        self.assertEqual(kwargs, element.get_positional_list_kwargs())

  def test_get_front(self):
    """Test that get_front() returns the element with `_position` == 0."""
    for kwargs in _each_position_list(self._model):
      self.assertEqual(
        self._model.get_front(**kwargs).uuid,
        self._model.objects.filter(**kwargs).get(_position=0).uuid,
      )

  def test_get_back(self):
    """Test that get_back() returns the last element in the list."""
    for kwargs in _each_position_list(self._model):
      self.assertEqual(
        self._model.get_back(**kwargs).uuid,
        self._model.objects.filter(**kwargs).reverse()[0].uuid,
      )

  def test_get_object_at_offset(self):
    """Tests that get_object_at_offset() retrieves the element at the
    specified offset."""
    from math import floor
    for kwargs in _each_position_list(self._model):
      size = self._model.objects.filter(**kwargs).count()
      idx = int(floor(size/2))
      obj = self._model.objects.filter(**kwargs).get(_position=idx)
      for i in xrange(-idx, size-idx):
        self.assertEqual(
          obj.get_object_at_offset(i).uuid,
          self._model.objects.filter(**kwargs).get(_position=i+idx).uuid,
        )

  def test_get_object_at_offset_invalid(self):
    """Tests that get_object_at_offset() with an invalid index raises a
    DoesNotExist exception."""
    for kwargs in _each_position_list(self._model):
      objs = self._model.objects.filter(**kwargs)
      size = objs.count()
      for obj in objs:
        # Index one too small:
        self.assertRaises(
          self._model.DoesNotExist,
          obj.get_object_at_offset,
          -obj._position - 1,
        )
        # Index one too large:
        self.assertRaises(
          self._model.DoesNotExist,
          obj.get_object_at_offset,
          size - obj._position,
        )

  def test_get_next(self):
    """Tests that get_next() retrieves the element which follows."""
    for kwargs in _each_position_list(self._model):
      size = self._model.objects.filter(**kwargs).count()
      elem = self._model.objects.filter(**kwargs).filter(_position__lt=size-1)
      next = self._model.objects.filter(**kwargs)[1:]
      self.assertEqual(
        map(lambda x: x.get_next().uuid, elem),
        map(lambda x: x.uuid, next),
      )

  def test_get_next_at_back(self):
    """Tests that get_next() on the last element of the list returns None."""
    for kwargs in _each_position_list(self._model):
      last = self._model.objects.filter(**kwargs).reverse()[0]
      self.assertEqual(last.get_next(), None)

  def test_get_prev(self):
    """Tests that get_prev() retrieves the prior element."""
    for kwargs in _each_position_list(self._model):
      size = self._model.objects.filter(**kwargs).count()
      elem = self._model.objects.filter(**kwargs).filter(_position__gt=0)
      prev = self._model.objects.filter(**kwargs)[:size-1]
      self.assertEqual(
        map(lambda x: x.get_prev().uuid, elem),
        map(lambda x: x.uuid, prev),
      )

  def test_get_prev_at_front(self):
    """Tests that get_next() on the first element of the list returns None."""
    for kwargs in _each_position_list(self._model):
      first = self._model.objects.filter(**kwargs)[0]
      self.assertEqual(first.get_prev(), None)

  def test_move_down(self):
    """Tests that move_down() on an element swaps it with the next item in the
    list."""
    for kwargs in _each_position_list(self._model):
      # Create a canonical list of UUIDs, which will be modified alongside the
      # database as a control process.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Test move_down() for each instance the operation would be valid on.
      for i in xrange(0, size-1):
        self._model.objects.filter(**kwargs).get(_position=i).move_down()
        oids[i], oids[i+1] = oids[i+1], oids[i]
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs)),
        )

  def test_move_down_at_back(self):
    """Tests that move_down() on the last element in a list has no effect, but
    doesn't raise any exceptions either."""
    for kwargs in _each_position_list(self._model):
      # Save the ordering pre-move_down().
      oids = _uuid_list(self._model.objects.filter(**kwargs))

      # Attemp a move_down() on the last element.
      self._model.objects.filter(**kwargs).reverse()[0].move_down()

      # Ensure that the list has not changed.
      self.assertEqual(oids,
        _uuid_list(self._model.objects.filter(**kwargs)),
      )

  def test_move_up(self):
    """Tests that move_up() on an element swaps it with the previous item in
    the list."""
    for kwargs in _each_position_list(self._model):
      # Create a canonical list of UUIDs, which will be modified alongside the
      # database as a control process.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Test move_up() for each instance the operation would be valid on.
      for i in xrange(1, size):
        self._model.objects.filter(**kwargs).get(_position=i).move_up()
        oids[i-1], oids[i] = oids[i], oids[i-1]
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs)),
        )

  def test_move_up_at_front(self):
    """Tests that move_up() on the first element in a list has no effect, but
    doesn't raise any exceptions either."""
    for kwargs in _each_position_list(self._model):
      # Save the ordering pre-move_up().
      oids = _uuid_list(self._model.objects.filter(**kwargs))

      # Attemp a move_up() on the first element.
      self._model.objects.filter(**kwargs)[0].move_up()

      # Ensure that the list has not changed.
      self.assertEqual(oids,
        _uuid_list(self._model.objects.filter(**kwargs)),
      )

  def test_move_to_front(self):
    """Tests that move_to_front() moves an element to the front of the
    list."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Test move_to_front() for each instance.
      for i in xrange(0, size):
        self._model.objects.filter(**kwargs).get(_position=i).move_to_front()
        oids = [oids[i]] + oids[:i] + oids[i+1:]
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs)),
        )

  def test_move_to_back(self):
    """Tests that move_to_back() moves an element to the back of the list."""
    # Save the initial ordering.
    for kwargs in _each_position_list(self._model):
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Test move_to_back() for each instance.
      for i in xrange(0, size):
        print (kwargs, oids, i, self._model.objects.filter(**kwargs).values())
        self._model.objects.filter(**kwargs).get(_position=i).move_to_back()
        oids = oids[:i] + oids[i+1:] + [oids[i]]
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs)),
        )

  def test_insert_at(self):
    """Tests that insert_at() moves the element to the position specified,
    shifting all elements in-between up or down one as required."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Try all permunations of insertions.
      from itertools import permutations
      for elem, other in permutations(xrange(0, size), 2):
        # Compute the expected result:
        if elem < other:
          oids = oids[:elem] + oids[elem+1:other+1] + [oids[elem]] + oids[other+1:]
        else:
          oids = oids[:other] + [oids[elem]] + oids[other:elem] + oids[elem+1:]
        # Perform the database update:
        self._model.objects.filter(**kwargs).get(_position=elem).insert_at(other)
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_insert_at_reflexive(self):
    """Tests that insert_at() applied to the position an element is already at
    has no effect."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      for element in xrange(0, size):
        # Perform the database update, with one query:
        obj = self._model.objects.filter(**kwargs).get(_position=element)
        obj.insert_at(element)
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

        # Perform the database update, with two queries:
        self._model.objects.filter(**kwargs).get(_position=element).insert_at(element)
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_insert_before(self):
    """Tests that insert_before() moves the element to the position occupied
    by the element specified, shifting all elements in-between up or down one
    position as required."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Try all permunations of insertions.
      from itertools import permutations
      for elem, other in permutations(xrange(0, size), 2):
        # Compute the expected result:
        if elem < other:
          oids = oids[:elem] + oids[elem+1:other] + [oids[elem]] + oids[other:]
        else:
          oids = oids[:other] + [oids[elem]] + oids[other:elem] + oids[elem+1:]
        # Perform the database update:
        self._model.objects.filter(**kwargs).get(_position=elem).insert_before(
          self._model.objects.filter(**kwargs).get(_position=other),
        )
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_insert_before_reflexive(self):
    """Tests that insert_before() applied itself has no effect."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      for element in xrange(0, size):
        # Perform the database update, with one query:
        obj = self._model.objects.filter(**kwargs).get(_position=element)
        obj.insert_before(obj)
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

        # Perform the database update, with two queries:
        self._model.objects.filter(**kwargs).get(_position=element).insert_before(
          self._model.objects.filter(**kwargs).get(_position=element),
        )
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_insert_after(self):
    """Tests that insert_after() moves the element to the position following
    the element specified, shifting all elements in-between up or down one
    position as required."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # Try all permunations of insertions.
      from itertools import permutations
      for elem, other in permutations(xrange(0, size), 2):
        print (elem, other)
        # Compute the expected result:
        if elem < other:
          oids = oids[:elem] + oids[elem+1:other+1] + [oids[elem]] + oids[other+1:]
        else:
          oids = oids[:other+1] + [oids[elem]] + oids[other+1:elem] + oids[elem+1:]
        # Perform the database update:
        self._model.objects.filter(**kwargs).get(_position=elem).insert_after(
          self._model.objects.filter(**kwargs).get(_position=other),
        )
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_insert_after_reflexive(self):
    """Tests that insert_after() applied at the end of the list moves the
    element to the end of the list, decrementing the position of all elements
    which previously followed the element."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      for element in xrange(0, size):
        # Perform the database update, with one query:
        obj = self._model.objects.filter(**kwargs).get(_position=element)
        obj.insert_after(obj)
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

        # Perform the database update, with two queries:
        self._model.objects.filter(**kwargs).get(_position=element).insert_after(
          self._model.objects.filter(**kwargs).get(_position=element),
        )
        # Compare:
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_swap(self):
    """Tests that swap() exchanges the position of any two elements in the
    list."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # For each permutation of two indices, swap and compare with the
      # expected result.
      from itertools import permutations
      for i in permutations(xrange(0, size), 2):
        # Compute the expected result.
        oids[i[0]], oids[i[1]] = oids[i[1]], oids[i[0]]

        # Swap the elemental positions in the database.
        self._model.objects.filter(**kwargs).get(_position=i[0]).swap(
          self._model.objects.filter(**kwargs).get(_position=i[1])
        )

        # Compare the database with the expected result.
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

  def test_swap_self(self):
    """Tests that swap(self) has no effect, but executes without error."""
    for kwargs in _each_position_list(self._model):
      # Save the initial ordering.
      oids = _uuid_list(self._model.objects.filter(**kwargs))
      size = len(oids)

      # For each index, try swapping it with itself. The result should be the
      # same as the initial ordering.
      for i in xrange(0, size):
        # Swap the elemental positions in the database, using two queries.
        self._model.objects.filter(**kwargs).get(_position=i).swap(
          self._model.objects.filter(**kwargs).get(_position=i)
        )

        # Make sure nothing changed.
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

        # Swap the elemental positions in the database, using one query.
        obj = self._model.objects.filter(**kwargs).get(_position=i)
        obj.swap(obj)

        # Make sure nothing changed.
        self.assertEqual(oids,
          _uuid_list(self._model.objects.filter(**kwargs))
        )

class EmptyPositionalOrderModelTests(TestCase):
  """Tests edge-case behavior when no elements have been created (yet)."""
  _model = SimplePositionalOrderModel
  _args = ()
  _kwargs = {}

  def test_get_front_on_empty(self):
    """Tests that calling get_front() on an empty list raises a DoesNotExist
    exception."""
    self.assertRaises(
      self._model.DoesNotExist,
      self._model.get_front,
      *self._args, **self._kwargs
    )

  def test_get_back_on_empty(self):
    """Tests that calling get_back() on an empty list raises a DoesNotExist
    exception."""
    self.assertRaises(
      self._model.DoesNotExist,
      self._model.get_back,
      *self._args, **self._kwargs
    )

class SimplePositionalOrderWithEmptyTupleTests(PositionalOrderModelTests):
  _model = SimplePositionalOrderWithEmptyTupleModel
class EmptySimplePositionalOrderWithEmptyTupleTests(EmptyPositionalOrderModelTests):
  _model = SimplePositionalOrderWithEmptyTupleModel
class SimplePositionalOrderWithSelfTests(PositionalOrderModelTests):
  _model = SimplePositionalOrderWithSelfModel
class EmptySimplePositionalOrderWithSelfTests(EmptyPositionalOrderModelTests):
  _model = SimplePositionalOrderWithSelfModel
# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
