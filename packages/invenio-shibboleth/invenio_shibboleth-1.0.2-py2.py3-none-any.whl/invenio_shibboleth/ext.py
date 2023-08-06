# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. Garcia Gabancho.
# Copyright (C) 2020 Mojib Wali.
#
# invenio-shibboleth is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module that provides SAML integration."""

from __future__ import absolute_import, print_function

from . import config
from .flask_sso_saml import FlaskSSOSAML


class Invenioshibboleth(object):
    """invenio-shibboleth extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        if "flask-sso-saml" not in app.extensions:
            FlaskSSOSAML(app)
        app.extensions["invenio-shibboleth"] = self
