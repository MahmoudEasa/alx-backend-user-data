#!/usr/bin/env python3
""" Manage the API authentication """
from os import getenv
from typing import List, TypeVar
from flask import request


class Auth:
    """ Class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False if path in excluded_paths else True """
        if not path or not excluded_paths or not len(excluded_paths):
            return (True)

        path = path[:-1] if path.endswith('/') else path
        for p in excluded_paths:
            p_copy = p
            if p.endswith('/'):
                p_copy = p[:-1]

            if path == p_copy:
                return (False)

            if p.endswith('*'):
                if path.startswith(p[:-1]):
                    return (False)

        return (True)

    def authorization_header(self, request=None) -> str:
        """ Returns None - request will be the Flask request object """
        if not request or 'Authorization' not in request.headers:
            return (None)
        return (request.headers['Authorization'])

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - request will be the Flask request object """
        return (None)
    
    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if not request:
            return (None)
        return (request.cookies.get(getenv("SESSION_NAME")))
