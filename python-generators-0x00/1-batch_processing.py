import mysql.connector
from typing import Generator, Dict, Any

def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the ALX_prodev database"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def stream_users_in_batches(batch_size: int) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that fetches users from database in batches
    Args:
        batch_size: Number of users to fetch per batch
    Yields:
        List of user dictionaries for each batch
    """
    connection = connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        offset = 0
        
        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            
            if not batch:
                break
                
            yield batch
            offset += batch_size
            
    except mysql.connector.Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()

def batch_processing(batch_size: int) -> None:
    """
    Processes user batches to filter and print users over age 25
    Args:
        batch_size: Number of users to process per batch
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25
        filtered_users = [user for user in batch if user['age'] > 25]
        
        # Print each filtered user
        for user in filtered_users:
            print(user)
