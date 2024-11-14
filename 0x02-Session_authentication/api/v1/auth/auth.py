#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import TypeVar, List
from os import getenv


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a given path requires authentication"""
        if not excluded_paths or not path:
            return True

        if not path.endswith('/'):
            path += '/'

        for route in excluded_paths:
            if route.endswith('*'):
                if path.startswith(route[:-1]):
                    return False
            elif path == route:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """validate all requests"""
        if not request:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves current user"""
        return None

    def session_cookie(self, request=None):
        """Retrieve cookie value from a request"""
        if not request:
            return None
        cookie_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(cookie_name)