#!/usr/bin/env python3
"""
Authentication module
"""
from flask import request
from typing import TypeVar, List


class Auth():
    """Authentication class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a given path requires authentication"""
        if not excluded_paths or not path:
            return True

        if not path.endswith('/'):
            path += '/'

        for route in excluded_paths:
            print(path, route)
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
        return None
