#!/usr/bin/env python3
""" Manage the API authentication """
from api.v1.auth.auth import Auth


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
