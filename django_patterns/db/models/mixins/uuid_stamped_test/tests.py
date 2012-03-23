#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_stamped_test.tests ------------===
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
