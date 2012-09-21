#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_stamped_test.tests ------------===
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
import uuid
# Django.core
import django.core.exceptions
import django.test
# Django-patterns
import django_patterns.db.fields

# The number of instances which are created in the TestCase's setUp() method.
# Must be a positive integer.
INSTANCE_COUNT = 3

from forms import UUIDStampedModelForm
from models import UUIDStampedModel

class UUIDStampedModelTests(django.test.TestCase):
  """Tests models which use UUIDStampedMixin to create an automatically
  assigned ‘uuid’ which in this mixin is in addition to the primary key."""

  def __init__(self, *args, **kwargs):
    super(UUIDStampedModelTests, self).__init__(*args, **kwargs)
    self._model = UUIDStampedModel
    self._form  = UUIDStampedModelForm

  def setUp(self):
    super(UUIDStampedModelTests, self).setUp()
    # Multiple objects are generated in order to test the auto-generation and
    # uniqueness features of the UUID field.
    for i in range(0, INSTANCE_COUNT):
      obj = self._model()
      obj.save()

  def test_objects_created_successfully(self):
    """Tests that UUIDStampedModel objects can be successfully created."""
    self.assertEqual(self._model.objects.filter().count(), INSTANCE_COUNT)

  def test_uuid_exists_as_field(self):
    """Tests that the ‘uuid’ attribute exists on UUIDStampedModel
    instances."""
    obj = self._model.objects.filter()[0]
    try:
      obj.uuid
    except AttributeError:
      self.assertTrue(False)

  def test_uuid_field_is_uuid(self):
    """Tests that the ‘uuid’ attribute on UUIDStampedModel instances is in
    fact a UUID field."""
    obj = self._model.objects.filter()[0]
    self.assertTrue(isinstance(
      obj._meta._name_map['uuid'][0],
      django_patterns.db.fields.UUIDField,
    ))

  def test_uuid_is_unique(self):
    """Tests that two UUIDStampedModel objects cannot be created with the same
    UUID value."""
    obj = self._model.objects.filter()[0]
    new_obj = self._model()
    new_obj.uuid = obj.uuid
    self.assertRaisesRegexp(
      django.core.exceptions.ValidationError,
      u'with this Universally unique identifier already exists',
      new_obj.validate_unique,
    )

  def test_uuid_is_not_editable(self):
    """Tests that ModelForms generated from UUIDStampedModel do not contain
    ‘uuid’ as an editable field."""
    objs = self._model.objects.filter()
    form = self._form(objs[0])
    with self.assertRaisesRegexp(KeyError, 'uuid'):
      form.fields['uuid'].validate(objs[1].uuid, objs[0])

  def test_uuid_is_uuid_instance(self):
    """Test that accessing the `uuid` field of a `UUIDStampedModel` object
    returns a Python standard library UUID instance."""
    obj = self._model.objects.filter()[0]
    self.assertTrue(isinstance(obj.uuid, uuid.UUID))

  def test_uuid_unicode_representation(self):
    """Test that the unicode representation of an UUIDStampedModel object is in
    standard form."""
    obj = self._model.objects.filter()[0]
    self.assertRegexpMatches(unicode(obj), r'[\w]{8}(-[\w]{4}){3}-[\w]{12}')

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
