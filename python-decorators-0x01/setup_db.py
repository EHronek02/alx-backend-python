#!/usr/bin/env python3
import sqlite3
from contextlib import closing

def setup_db():
    """Setup the database and populate with test users"""
    try:
        with closing(sqlite3.connect('users.db')) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("DROP TABLE IF EXISTS users")

                cursor.execute("""CREATE TABLE users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            age INTEGER,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  )""")
                
                test_users = [
                    ('John Doe', 'john@example.com', 28),
                    ('Jane Smith', 'jane@example.com', 32),
                    ('Bob Johnson', 'bob@example.com', 45),
                    ('Alice Brown', 'alice@example.com', 23),
                    ('Charlie Wilson', 'charlie@example.com', 37)
                ]
                cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", test_users)

                conn.commit()
                print("Database setup complete")
                print(f"Added {len(test_users)} test users")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


def verify_setup():
    """Verify the database was created correctly"""
    try:
        with closing(sqlite3.connect('users.db')) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT COUNT(*) FROM users")
                count = cursor.fetchone()[0]

                cursor.execute("SELECT * from users LIMIT 1")
                sample = cursor.fetchone()

                print("\nVerification:")
                print(f"Total users: {count}")
                print(f"Sample user: {sample}")
    except sqlite3.Error as e:
        print(f"Verification failed: {e}")

if __name__ == '__main__':
    print("Setting up test database...")
    setup_db()
    print()
    print("Verifying...")
    verify_setup
