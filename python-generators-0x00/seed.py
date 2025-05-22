import csv
import uuid
import mysql.connector
from mysql.connector import Error
from typing import Generator, Tuple, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the database ALX_prodev if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def insert_data(connection: mysql.connector.connection.MySQLConnection, csv_file: str) -> None:
    """Insert data from CSV file into the database"""
    try:
        cursor = connection.cursor()
        
        # Read CSV file
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                user_id = str(uuid.uuid4())

                # Check if user with same email already exists
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (row['email'],))
                if not cursor.fetchone():
                    # Insert a new record
                    cursor.execute("""
                                   INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)""",
                                   (user_id, row["name"], row["email"], int(row["age"])))
        
        connection.commit()
        print(f"Data inserted successfully from {csv_file}")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    except FileNotFoundError:
        print(f"Error: CSV file {csv_file} not found")
    finally:
        if cursor:
            cursor.close()

def stream_users(connection: mysql.connector.connection.MySQLConnection) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that streams rows from user_data table one by one
    Args:
        connection: MySQL database connection
    Yields:
        Dictionary containing user data for one row at a time
    """
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if not row:
                break
            yield row
            
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
