#!/usr/bin/env python3
"""
Main file
"""

import logging
from filtered_logger import RedactingFormatter, get_db

def test_formatter():
    """Test the RedactingFormatter for log redaction"""
    message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(fields=["email", "ssn", "password"])
    print("Formatted log message:")
    print(formatter.format(log_record))

def query_user_count():
    """Test the get_db function by querying the users table"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    print("\nUser count from database:")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()

if __name__ == "__main__":
    test_formatter()
    query_user_count()
