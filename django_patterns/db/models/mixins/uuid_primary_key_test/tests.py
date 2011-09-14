#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.models.mixins.uuid_primary_key_test.tests --------===
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

# Django-core, exceptions
import django.core.exceptions

# Django-core, testing
import django.test

# Python standard library, unit-testing framework
from django.utils import unittest

# Django-extensions, additional model fields
import django_extensions.db.fields

##
# The number of instances which are created in the TestCase's setUp() method.
# Must be a positive integer.
INSTANCE_COUNT = 3

from forms import UUIDPrimaryKeyModelForm
from models import UUIDPrimaryKeyModel

class UUIDPrimaryKeyModelTests(django.test.TestCase):
  """
  Tests models which use UUIDPrimaryKeyMixin to create an automatically
  assigned and randomly generated UUID as the model instance's ‘id’ primary
  key.
  """
  def setUp(self):
    super(UUIDPrimaryKeyModelTests, self).setUp()

    # Multiple objects are generated in order to test the auto-generation and
    # uniqueness features of the UUID field.
    for i in range(0, INSTANCE_COUNT):
      obj = UUIDPrimaryKeyModel()
      obj.save()

  def test_objects_created_successfully(self):
    """
    Tests that UUIDPrimaryKeyModel objects can be successfully created.
    """
    self.assertEqual(UUIDPrimaryKeyModel.objects.filter().count(), INSTANCE_COUNT)

  def test_primary_key_is_uuid(self):
    """
    Tests that the ‘id’ field of UUIDPrimaryKeyModel (and its alias, ‘pk’)
    point to the UUID field.
    """
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    self.assertTrue(isinstance(
      obj._meta._name_map['id'][0],
      django_extensions.db.fields.UUIDField,
    ))
    self.assertEqual(obj.pk, obj.id)

  def test_uuid_is_unique(self):
    """
    Tests that two UUIDPrimaryKeyModel objects cannot be created with the same
    UUID value.
    """
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    new_obj = UUIDPrimaryKeyModel()
    new_obj.id = obj.id
    self.assertRaisesRegexp(
      django.core.exceptions.ValidationError,
      u'with this Universally unique identifier already exists',
      new_obj.validate_unique,
    )

  def test_uuid_is_not_editable(self):
    """
    Tests that ModelForms generated from UUIDPrimaryKeyModel do not contain
    ‘id’ as an editable field.
    """
    objs = UUIDPrimaryKeyModel.objects.filter()
    form = UUIDPrimaryKeyModelForm(objs[0])
    with self.assertRaisesRegexp(KeyError, 'id'):
      form.fields['id'].validate(objs[1].id, objs[0])

  def test_uuid_unicode_representation(self):
    """
    Test that the unicode representation of an UUIDPrimaryKeyModel object is
    in standard form.
    """
    obj = UUIDPrimaryKeyModel.objects.filter()[0]
    self.assertRegexpMatches(unicode(obj), r'[\w]{8}(-[\w]{4}){3}-[\w]{12}')

from django_patterns.db.models.mixins.uuid_stamped_test import tests
class UUIDPrimaryKeyAsStampedModelTests(tests.UUIDStampedModelTests):
  """
  Tests that models which derive from UUIDPrimaryKeyMixin (whose UUID field is
  ‘id’ with a @Property alias at ‘uuid’) work as a stand-in for code expecting
  models derived from UUIDStampedMixin (whose UUID field is ‘uuid’).
  """
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
