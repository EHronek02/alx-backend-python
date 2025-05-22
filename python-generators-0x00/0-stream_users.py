#!/usr/bin/python3
import mysql.connector
from seed import connect_to_prodev
import os

def stream_users():
    """Generator that yields one user row at a time
    from the user_data table"""
    
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    except mysql.connector.Error as e:
        print(f"Database Error: {e}")
    finally:
        
        if connection is not None:
            try:
                connection.close()
            except mysql.connector.Error as e:
                print(f"Connection close error: {e}")