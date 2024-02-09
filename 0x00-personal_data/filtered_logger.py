#!/usr/bin/env python3

""" A function filter_datum that
    returns the log message obfuscated
"""

import logging
from typing import List
import re
import os
from mysql.connector import connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Return: the log message obfuscated """
    return (re.sub(rf"({'|'.join(fields)})=.*?{separator}",
            rf"\1={redaction}{separator}", message))


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format Function """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return (super().format(record))


def get_logger() -> logging.Logger:
    """ Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return (logger)


def get_db() -> connection.MySQLConnection:
    """ Returns a connector to the database
        pip3 install mysql-connector-python
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return (connection.MySQLConnection(
            host=db_host,
            database=db_name,
            username=username,
            password=password))


def main():
    """ Obtain a database connection using get_db
        and retrieve all rows in the users table
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info(row)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
