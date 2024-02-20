#!/usr/bin/env python3
"""Auth model
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Return bytes hash of the input password """
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
