# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Esteban J. Garcia Gabancho.
# Copyright (C) 2020 Mojib Wali.
#
# invenio-shibboleth is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Minimal Flask application example."""

from __future__ import absolute_import, print_function

import os

from flask import Flask, redirect, url_for
from flask_babelex import Babel
from flask_login import current_user
from flask_menu import Menu as FlaskMenu
from invenio_accounts import InvenioAccounts
from invenio_accounts.views import blueprint as blueprint_user
from invenio_db import InvenioDB
from invenio_mail import InvenioMail
from invenio_userprofiles import InvenioUserProfiles
from invenio_userprofiles.views import blueprint_ui_init as blueprint_userprofile_init

from invenio_shibboleth import Invenioshibboleth
from invenio_shibboleth.handlers import acs_handler_factory, default_sls_handler


def account_info(info):
    """Extract user information from IdP response."""
    return dict(
        user=dict(
            email=info["User.email"][0],
            profile=dict(
                username=info["User.FirstName"][0], full_name=info["User.FirstName"][0]
            ),
        ),
        external_id=info["User.email"][0],
        external_method="onelogin",
        active=True,
    )


# Create Flask application
app = Flask(__name__)
app.config.update(
    SSO_SAML_IDPS={
        "onelogin": {
            "settings": {
                "idp": {
                    "entityId": os.environ.get("IDP_ENTITY_ID"),
                    "singleSignOnService": {"url": os.environ.get("IDP_SSO_URL")},
                    "singleLogoutService": {"url": os.environ.get("IDP_SLS_URL")},
                    "x509cert": os.environ.get("IDP_CERT"),
                },
            },
            "acs_handler": acs_handler_factory(account_info),
            "sls_handler": default_sls_handler,
        }
    },
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///instance/app.db"
    ),
    SERVER_NAME="0.0.0.0:5000",
    SECRET_KEY="EXAMPLE_APP",
    DEBUG=True,
    SQLALCHEMY_ECHO=False,
    SECURITY_PASSWORD_SALT="security-password-salt",
    MAIL_SUPPRESS_SEND=True,
    TESTING=True,
    USERPROFILES_EXTEND_SECURITY_FORMS=True,
    SECURITY_CONFIRMABLE=False,
    SECURITY_SEND_REGISTER_EMAIL=False,
)

Babel(app)
FlaskMenu(app)
InvenioDB(app)
InvenioAccounts(app)
InvenioUserProfiles(app)
InvenioMail(app)
Invenioshibboleth(app)

app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_userprofile_init)


@app.route("/")
def index():
    """Homepage."""
    return "Home page (without any restrictions)"


@app.route("/onelogin")
def github():
    """Try to print user email or redirect to login with github."""
    if not current_user.is_authenticated:
        return redirect(url_for("sso_saml.sso", idp="onelogin", next="/onelogin"))
    return "hello {}".format(current_user.email)
