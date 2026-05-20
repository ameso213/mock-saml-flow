import os
from flask import Flask, redirect, request, session
from saml2.client import Saml2Client
from saml2.config import Config
from saml2 import BINDING_HTTP_POST


#Initializing the Web App Runtime
app = Flask(__name__)
app.secret_key = os.urandom(24)


#Defining the Configuration and Identity Contract
XML_METADATA = """<?xml version="1.0"?>
<IDPSSODescriptor protocalSupoortEnummeration="urn:oasis:name:tc:SAML:2.0:protocol">
<SingleSignOnService Binding="urn:oasis:tc:SAML:2.0:bindings:HTTP-Ridirect"
Location="http://localhost:8001/saml/sso"/>

</IDPSSODescriptor>

</EntityDescriptor>

"""

SP_CONFIG={
    "entityid":"http://localhost8000/metadata",
    "service":{
        "sp":{
            "endpoints":{
                "assertion_consumer_service":[
                    ("http://localhost:8000/saml/acs",BINDING_HTTP_POST)
                ]
            },
            "allow_unsolicited":True,
        }
    },
    "metadata":{"inline":[XML_METADATA]},
}


#The Home Page and User Redirection Route
@app.route("/")
def home():
    if "user" in session:
        return f"<hi>Logged In</h1><p>Welcome,{session['user']}<a href='/logout'>Logout</a>"
    return "<h1>Welcome to MOCK SP</h1><a href='/login'></a>"


@app.route('/login')
def login():
    saml_client=Saml2Client(config=Config().load(SP_CONFIG))
    _, _, http_args = saml_client.prepare_for_negotiated_authenticate(
        entity_id="http://idp:8001/metadata", 
        relay_state="/")
    redirect_url=dict(http_args["headers"])["Location"]
    return redirect(redirect_url)


#Processing the Secure SAML Response
@app.route("saml/acs",methods=["POST"])
def acs():
    saml_client = Saml2Client(config=Config().load(SP_CONFIG))
    authn_response = saml_client.parse_authn_request_response(
        request.form["SAMLResponse"], BINDING_HTTP_POST
    )
    identity = authn_response.get_identity() or {}
    mail_list = identity.get("mail",["unknown_user"])
    session["user"] = mail_list if ininstance(mail_list,list) else mail_list

    return redirect("/")


#Logging Out
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

    
