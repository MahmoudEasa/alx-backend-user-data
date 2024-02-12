#!/usr/bin/env python3
""" Manage the API authentication """
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """ Empty Class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """ Returns the Base64 part of the Authorization header
            for a Basic Authentication
        """
        if not isinstance(authorization_header, str):
            return (None)
        if not authorization_header.startswith("Basic "):
            return (None)
        return (authorization_header[6:])

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ returns the decoded value
            of a Base64 string base64_authorization_header
        """
        if not isinstance(base64_authorization_header, str):
            return (None)
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return (decoded_bytes.decode("utf-8"))
        except Exception as e:
            return (None)

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ Returns the user email and password from
            the Base64 decoded value
        """
        input = decoded_base64_authorization_header
        if not isinstance(input, str):
            return ((None, None))

        index = input.find(":")
        if index == -1:
            return ((None, None))

        return ((input[:index], input[index + 1:]))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return (None)

        user = User.search({'email': user_email})
        if not len(user):
            return (None)
        if not user[0].is_valid_password(user_pwd):
            return (None)
        return (user[0])
