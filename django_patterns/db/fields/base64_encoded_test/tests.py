#!/usr/bin/env python
# -*- coding: utf-8 -*-

# === django_patterns.db.fields.base64_encoded_test.tests -----------------===
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

# Python standard library
import uuid
# Django.core
import django.core.exceptions
import django.test
# Django-patterns
import django_patterns.db.fields

from forms import Base64EncodedModelForm
from models import Base64EncodedModel

class Base64EncodedModelTests(django.test.TestCase):
  "Tests models which have a Base64-encoded field with default options."

  def __init__(self, *args, **kwargs):
    super(Base64EncodedModelTests, self).__init__(*args, **kwargs)
    self._model = Base64EncodedModel
    self._form  = Base64EncodedModelForm

  def test_empty(self):
    "Test the empty string."
    s = ''
    obj = self._model()
    obj.base64 = s
    obj.save()
    self.assertTrue(isinstance(obj.base64, basestring))
    self.assertEqual(obj.base64, s)

  def test_zero(self):
    "Test a string containing the zero byte."
    s = '\x00abc\x00123\x00\x00abc123\x00'
    obj = self._model()
    obj.base64 = s
    obj.save()
    self.assertTrue(isinstance(obj.base64, basestring))
    self.assertEqual(obj.base64, s)

  def test_string(self):
    "Test a long, effectively random ASCII string."
    s = '123abc#'*137
    obj = self._model()
    obj.base64 = s
    obj.save()
    self.assertTrue(isinstance(obj.base64, basestring))
    self.assertEqual(obj.base64, s)

  def test_unicode(self):
    "Test a unicode string."
    s = u'elespañol, lefrançais, עברית, & 日本語'
    obj = self._model()
    obj.base64 = s
    obj.save()
    self.assertTrue(isinstance(obj.base64, unicode))
    self.assertEqual(obj.base64, s)

# ===----------------------------------------------------------------------===
# End of File
# ===----------------------------------------------------------------------===
