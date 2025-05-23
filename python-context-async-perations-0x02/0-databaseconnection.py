#!/usr/bin/env python3
"""Defines a class based context manager to handle
opening and closing of db connection automatically
"""
import sqlite3


class DatabaseConnection:
    """Custom context manager for db connections"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the db connection when entering the context"""
        print("Opeing the database connection...")
        self.conn = sqlite3.connect(self.db_name)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """close the connection when exiting the context"""
        if self.conn:
            self.conn.close()
            print("Db connection closed")

        if exc_type:
            print(f"An error occured: {exc_val}")
            return False
        return True
    

def query_users():
    try:
        with DatabaseConnection('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")

            print("\n User List:")
            for row in cursor.fetchall():
                print(f"ID: {row[0]}, name: {row[1]}, Email: {row[2]}")
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Errror: {e}")

if __name__ == "__main__":
    query_users()
