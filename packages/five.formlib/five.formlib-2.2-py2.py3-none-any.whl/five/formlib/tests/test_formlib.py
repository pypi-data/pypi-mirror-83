##############################################################################
#
# Copyright (c) 2004, 2005 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import unittest
from doctest import DocTestSuite
from Testing.ZopeTestCase import FunctionalDocFileSuite
from uuid import uuid4
from Testing.ZopeTestCase.zopedoctest.functional import http


def test_get_widgets_for_schema_fields():
    """
    Test widget lookup for schema fields

    First, load the configuration files:

      >>> from Zope2.App import zcml
      >>> import Products.Five
      >>> zcml.load_config('configure.zcml', Products.Five)
      >>> import zope.app.form.browser
      >>> zcml.load_config('configure.zcml', zope.app.form.browser)

    Now for some actual testing...

      >>> from zope.schema import Choice, TextLine
      >>> salutation = Choice(title=u'Salutation',
      ...                     values=("Mr.", "Mrs.", "Captain", "Don"))
      >>> contactname = TextLine(title=u'Name')

      >>> from zope.publisher.browser import TestRequest
      >>> request = TestRequest()
      >>> salutation = salutation.bind(request)
      >>> contactname = contactname.bind(request)

      >>> from zope.component import getMultiAdapter
      >>> from zope.formlib.interfaces import IInputWidget
      >>> from zope.formlib.textwidgets import TextWidget
      >>> from zope.formlib.itemswidgets import DropdownWidget

      >>> view1 = getMultiAdapter((contactname, request), IInputWidget)
      >>> view1.__class__ == TextWidget
      True

      >>> view2 = getMultiAdapter((salutation, request), IInputWidget)
      >>> view2.__class__ == DropdownWidget
      True

    Clean up:

      >>> from zope.component.testing import tearDown
      >>> tearDown()
    """


def http_request(url, form_parts=None, body=None, auth=None):
    """perform HTTP request from given parameters.

    The primary purpose of this auxiliary function is to compute
    the `Content-Length` header. While Python 2's `cgi` module
    seems resilient to a wrong `Content-Length`, Python 3's `cgi` fails
    badly (at least for a too small value).

    If given, *form_parts* must be an iterable yielding pairs *name*,*value*.
    *body* is then computed as a typical form response from it.
    Otherwise, if *body* is not `None`, it defines the request content.
    Otherwise, a `GET` request is created.
    """
    boundary = None
    if form_parts is not None:
        boundary = str(uuid4())
        body = "".join(
            "--" + boundary + "\n" +
            "Content-Disposition: form-data; name=\"" + name + "\"\n\n" +
            value + "\n"
            for (name, value) in form_parts
            ) + "--" + boundary + "--\n"
    headers = []
    headers.append(("POST" if body is not None else "GET")
                   + " " + url + " HTTP/1.1"
                   )
    if auth:
        headers.append("Authorization: " + auth)
    headers.append("Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7")
    if body is not None:
        if not body.endswith("\n"):
            body += "\n"
        headers.append("Content-Length: " + str(len(body)))
        headers.append(
            "Content-Type: " +
            ("application/x-www-form-urlencoded" if boundary is None
             else "multipart/form-data; boundary=" + boundary)
                      )
        body = "\n\n" + body
    return http("\n".join(headers) + (body or ''))


def test_suite():
    return unittest.TestSuite([
        DocTestSuite(),
        FunctionalDocFileSuite('forms.txt', package="five.formlib.tests",
                               globs=dict(http_request=http_request),
                               ),
        FunctionalDocFileSuite('formlib.txt', package='five.formlib.tests'),
    ])
