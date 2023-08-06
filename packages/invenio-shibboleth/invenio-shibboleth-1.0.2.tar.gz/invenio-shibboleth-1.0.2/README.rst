..
    Copyright (C) 2020 CERN.
    Copyright (C) 2020 TU Graz.

    invenio-shibboleth is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

====================
 invenio-shibboleth
====================

.. image:: https://travis-ci.com/mb-wali/invenio-shibboleth.svg
        :target: https://travis-ci.com/github/mb-wali/invenio-shibboleth

.. image:: https://img.shields.io/coveralls/mb-wali/invenio-shibboleth.svg
        :target: https://coveralls.io/r/mb-wali/invenio-shibboleth

.. image:: https://img.shields.io/github/tag/mb-wali/invenio-shibboleth.svg
        :target: https://github.com/mb-wali/invenio-shibboleth/releases

.. image:: https://img.shields.io/pypi/dm/invenio-shibboleth.svg
        :target: https://pypi.python.org/pypi/invenio-shibboleth

.. image:: https://img.shields.io/github/license/mb-wali/invenio-shibboleth.svg
        :target: https://github.com/mb-wali/invenio-shibboleth/blob/master/LICENSE

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Invenio module that provides SAML integration.

These two modules has been merged into one:

* ``invenio-saml`` Further documentation is available on https://invenio-saml.readthedocs.io/
* ``flask-sso-saml`` Further documentation is available on https://flask-sso-saml.readthedocs.io/

====================
 Installation
====================
``pip install invenio-shibboleth``

====================
Configuration
====================

``from invenio_shibboleth.handlers import acs_handler_factory``

.. code:: python

   SSO_SAML_IDPS = {
    'onelogin': {
                # settings_file_path can be either json or xml.
		"settings_file_path": "./saml/onelogin/onelogin.json",
		"sp_cert_file": "./saml/onelogin/cert/sp.crt",
		"sp_key_file": "./saml/onelogin/cert/sp.key",

        'settings': {
            'sp': {
                'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
            },
            'security': {
                'authnRequestsSigned': False,
                'failOnAuthnContextMismatch': False,
                'logoutRequestSigned': False,
                'logoutResponseSigned': False,
                'metadataCacheDuration': None,
                'metadataValidUntil': None,
                'nameIdEncrypted': False,
                'requestedAuthnContext': False,
                'requestedAuthnContextComparison': 'exact',
                'signMetadata': False,
                'signatureAlgorithm':
                    'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
                'wantAssertionsEncrypted': False,
                'wantAssertionsSigned': False,
                'wantAttributeStatement': False,
                'wantMessagesSigned': False,
                'wantNameId': True,
                'wantNameIdEncrypted': False,
                'digestAlgorithm':
                    'http://www.w3.org/2001/04/xmlenc#sha256'
            },
        },
 
          "mappings": {
            # invenio  #origin
            "email": "email",
            "name": "username",
            "surname": "full_name",
            "external_id": "external_id",
        },

        'acs_handler': acs_handler_factory('onelogin'),

          },

           }

Further documentation is available on
https://invenio-shibboleth.readthedocs.io/
