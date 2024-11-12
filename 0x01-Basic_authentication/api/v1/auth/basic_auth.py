#!/usr/bin/env python3
"""BasicAuth Module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic auth implementation"""
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Extracts the base64 part of the auth_header"""
        if (
            not authorization_header
            or not isinstance(authorization_header, str)
        ):
            return None

        try:
            auth_type, val = authorization_header.split()
        except ValueError:
            return None

        if auth_type == "Basic":
            return val

        return None

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Decode a Base64 string"""
        if (
            not base64_authorization_header
            or not isinstance(base64_authorization_header, str)
        ):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header
            ).decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """Retrieves the user email and password"""
        if (
            not decoded_base64_authorization_header
            or not isinstance(decoded_base64_authorization_header, str)
        ):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
        except ValueError:
            return None, None

        return email, password

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """Retrieves a user instance based on credentials"""
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})

        if users:
            user = users[0]

            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve user instance for a request"""
        encoded_creds = self.authorization_header(request)

        if encoded_creds:
            creds = self.decode_base64_authorization_header(
                self.extract_base64_authorization_header(encoded_creds)
            )
            email, password = self.extract_user_credentials(creds)

            if email and password:
                return self.user_object_from_credentials(email, password)

        return None
