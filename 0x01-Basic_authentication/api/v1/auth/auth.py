#!/usr/bin/env python3
""" Manage the API authentication """
from typing import List, TypeVar
from flask import request


class Auth:
    """ Class to manage the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns False - path and excluded_paths """
        if not path or not excluded_paths or not len(excluded_paths):
            return (True)

        path = path[:-1] if path.endswith('/') else path
        excluded_paths = [p[:-1] for p in excluded_paths if p.endswith('/')]

        if path in excluded_paths:
            return (False)

        return (True)

    def authorization_header(self, request=None) -> str:
        """ Returns None - request will be the Flask request object """
        return (None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None - request will be the Flask request object """
        return (None)
