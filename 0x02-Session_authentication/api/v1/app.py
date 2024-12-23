#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if getenv('AUTH_TYPE') == 'auth':
    auth = Auth()

elif getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()

elif getenv('AUTH_TYPE') == 'session_auth':
    auth = SessionAuth()

elif getenv('AUTH_TYPE') == 'session_exp_auth':
    auth = SessionExpAuth()

elif getenv('AUTH_TYPE') == 'session_db_auth':
    auth = SessionDBAuth()


@app.before_request
def filter() -> None:
    """Determines if a request require authentication"""
    if auth:
        ex = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, ex):
            cur_user = auth.current_user(request)
            if (
                not auth.authorization_header(request)
                and not auth.session_cookie(request)
            ):
                abort(401)
            if not cur_user:
                abort(403)
            request.current_user = cur_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ forbidden access handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
