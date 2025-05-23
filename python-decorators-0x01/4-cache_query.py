#!/usr/bin/env python3
"""Defines a decorate that caches the results of a database queries
inorder to avoid redundant calls"""
import sqlite3
import functools
import pickle
from datetime import datetime, timedelta

query_cache = {}

def cache_query(func):
    """Decorator that caches database query results"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = (query, str(args), str(kwargs))

        if cache_key in query_cache:
            cached_data = query_cache[cache_key]
            if datetime.now() < cached_data['expires']:
                print("serving from the cache")
                return pickle.loads(pickle.dumps(cached_data['result']))
        print("querying db...")
        result = func(conn, query, *args, **kwargs)

        query_cache[cache_key] = {
            'result': result,
            'expires': datetime.now() + timedelta(minutes=5)
        }

        return result
    return wrapper

def with_db_connection(func):
    """Handles  opening/closing database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print("\nCache contents:")
for key in query_cache:
    print(f"Query: {key[0]}")
    print(f"Expires: {query_cache[key]['expires']}")
