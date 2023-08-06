# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import sys

import pytest
import django
from webtest import TestApp

from contrast.test.apptest.base_test import BaseContrastTest


@pytest.mark.django_db
class BaseDjangoTest(BaseContrastTest):
    @property
    def middleware_name(self):
        # TODO: PYT-1102
        if os.environ.get("USE_DJANGO_WSGI"):
            return "wsgi_middleware"
        return (
            "django_middleware"
            if django.VERSION >= (1, 10)
            else "legacy_django_middleware"
        )

    def setup_method(self):
        super(BaseDjangoTest, self).setup_method()

        self.build_test_app()

    def teardown_method(self):
        del sys.modules["app.wsgi"]
        super(BaseDjangoTest, self).teardown_method()

    def build_test_app(self):
        # app must be imported here and not top of module to avoid app from
        # getting initialized before setup_method patching - just like for Flask
        from app.wsgi import application

        # we call this thing a "client" because it's comfortable for us, but
        # it's really a test app
        self.client = TestApp(application, lint=False)
