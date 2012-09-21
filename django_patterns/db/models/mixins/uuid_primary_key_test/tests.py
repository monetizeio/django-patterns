#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_primary_key_test.tests --------===
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

# Python standard library
from django.utils import unittest
import uuid
# Django.core
import django.core.exceptions
import django.test
# Django-patterns
import django_patterns.db.fields

# The number of instances which are created in the TestCase's setUp() method.
# Must be a positive integer.
INSTANCE_COUNT = 3

from forms import UUIDPrimaryKeyModelForm
from models import UUIDPrimaryKeyModel

class UUIDPrimaryKeyModelTests(django.test.TestCase):
  """Tests models which use UUIDPrimaryKeyMixin to create an automatically
  assigned and randomly generated UUID as the model instance's ‘id’ primary
  key."""

  def setUp(self):
    super(UUIDPrimaryKeyModelTests, self).setUp()

    # Multiple objects are generated in order to test the auto-generation and
    # uniqueness features of the UUID field.
    for i in range(0, INSTANCE_COUNT):
      obj = UUIDPrimaryKeyModel()
      obj.save()

  def test_objects_created_successfully(self):
    """Tests that UUIDPrimaryKeyModel objects can be successfully created."""
    self.assertEqual(UUIDPrimaryKeyModel.objects.filter().count(), INSTANCE_COUNT)

  def test_primary_key_is_uuid(self):
    """Tests that the ‘id’ field of UUIDPrimaryKeyModel (and its alias, ‘pk’)
    point to the UUID field."""
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    self.assertTrue(isinstance(
      obj._meta._name_map['id'][0],
      django_patterns.db.fields.UUIDField,
    ))
    self.assertEqual(obj.pk, obj.id)

  def test_uuid_is_unique(self):
    """Tests that two UUIDPrimaryKeyModel objects cannot be created with the
    same UUID value."""
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    new_obj = UUIDPrimaryKeyModel()
    new_obj.id = obj.id
    self.assertRaisesRegexp(
      django.core.exceptions.ValidationError,
      u'with this Universally unique identifier already exists',
      new_obj.validate_unique,
    )

  def test_uuid_is_not_editable(self):
    """Tests that ModelForms generated from UUIDPrimaryKeyModel do not contain
    ‘id’ as an editable field."""
    objs = UUIDPrimaryKeyModel.objects.filter()
    form = UUIDPrimaryKeyModelForm(objs[0])
    with self.assertRaisesRegexp(KeyError, 'id'):
      form.fields['id'].validate(objs[1].id, objs[0])

  def test_id_is_uuid_instance(self):
    """Test that accessing the `id` field of a `UUIDPrimaryKeyModel` object
    returns a Python standard library UUID instance."""
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    self.assertTrue(isinstance(obj.id, uuid.UUID))

  def test_uuid_unicode_representation(self):
    """Test that the unicode representation of an UUIDPrimaryKeyModel object
    is in standard form."""
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    self.assertRegexpMatches(unicode(obj), r'[\w]{8}(-[\w]{4}){3}-[\w]{12}')

from django_patterns.db.models.mixins.uuid_stamped_test import tests
class UUIDPrimaryKeyAsStampedModelTests(tests.UUIDStampedModelTests):
  """Tests that models which derive from UUIDPrimaryKeyMixin (whose UUID field
  is ‘id’ with a @Property alias at ‘uuid’) work as a stand-in for code
  expecting models derived from UUIDStampedMixin (whose UUID field is
  ‘uuid’)."""
  def __init__(self, *args, **kwargs):
    super(UUIDPrimaryKeyAsStampedModelTests, self).__init__(*args, **kwargs)
    self._model = UUIDPrimaryKeyModel
    self._form  = UUIDPrimaryKeyModelForm

  @unittest.skip(u"UUID field does not exist as a Django field in UUIDPrimaryKeyModel.")
  def test_uuid_field_is_uuid(self):
    pass

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
