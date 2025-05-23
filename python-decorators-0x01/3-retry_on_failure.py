#!/usr/bin/env python3
"""Using decorators to retry database queries"""
import time
import sqlite3
import functools

def with_db_connection(func):
    """Handle opening/closing db connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Retries the function if it fails due to transient errors"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
                    last_exception = e
                    if attempt < retries:
                        wait_time = delay * (2 ** (attempt - 1))
                        print(f"Attempt {attempt} failed: {e}. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
            print(f"All {retries} failed")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


users = fetch_users_with_retry()
print(users)
