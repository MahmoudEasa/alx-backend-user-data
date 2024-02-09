#!/usr/bin/env python3
""" Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Returns a salted, hashed password, which is a byte string """
    return (bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
