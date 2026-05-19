import os
from flask import Flask, redirect, request, session, url_for
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client
from saml2.config import Config

app = Flask(__name__)
# Secure signing key for Flask session cookies
app.secret_key = "my-key"

# Read the port from the environment, or default to 5000
PORT = os.environ.get("APP_PORT", "5000")
BASE_URL = f"http://localhost:{PORT}"

# Dynamic SAML Configuration
SAML_CONFIG = {
    "entityid": f"{BASE_URL}/saml/metadata",
    "service": {
        "sp": {
            "endpoints": {
                "assertion_consumer_service": [
                    (f"{BASE_URL}/saml/acs", BINDING_HTTP_POST)
                ],
            },
            "required_attributes": ["uid", "mail", "givenName", "sn"],
        }
    },
    "metadata": {"local": ["idp_metadata.xml"]},
}

# Helper function to initialize the SAML Client wrapper
def get_saml_client():
    config = Config()
    config.load(SAML_CONFIG)
    return Saml2Client(config=config)
