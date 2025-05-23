#!/usr/bin/env python3
import sqlite3
import functools


def with_db_connection(func):
    """decorator that automatically handles opening and closing connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # opens a new db connection
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


user = get_user_by_id(user_id=1)
print(user)
