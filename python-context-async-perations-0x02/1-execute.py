#!/usr/bin/env python3
"""Implements a class based custom context manager ExecuteQuery"""
import sqlite3


class ExecuteQuery:
    """Custom Context manager that executes a parametirized query
    and returns a results"""
    def __init__(self, db_name, query, params=None):
        """Initializes with the db name, query and params(for query)"""
        self.db_name = db_name
        self.query = query
        self.params = params if params is not None else ()
        self.cursor = None
        self.conn = None
        self.results = None

    def __enter__(self):
        """Execute the query when entering context"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

            print(f"Executing query: {self.query} with params {self.params}")
            self.cursor.execute(self.query, self.params)

            self.results = self.cursor.fetchall()
            return self.results

        except sqlite3.Error as e:
            print(f"Query executing failed: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """clean up resources when exiting context"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed")
        return False if exc_type else True


if __name__ == "__main__":
    try:
        with ExecuteQuery(
            db_name="users.db",
            query="SELECT * FROM users WHERE age > ?",
            params=(25,)
        ) as results:
            print("\n Users over 25")
            for user in results:
                print(f"ID: {user[0]}, Name:{user[1]}, Age: {user[3]}")
    except Exception as e:
        print(f"Operation failed: {e}")
