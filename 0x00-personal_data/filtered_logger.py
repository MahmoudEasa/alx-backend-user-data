#!/usr/bin/env python3
""" A function filter_datum that returns the log message obfuscated
"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return: the log message obfuscated """
    pattern = re.compile(fr"({'|'.join(fields)})=.*?{separator}")
    replacement = fr"\g<1>={redaction}{separator}"
    return(re.sub(pattern, replacement, message))


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Format Function """
        NotImplementedError
