from typing import Generator, List, Dict, Any
import seed

def paginate_users(page_size: int, offset: int) -> List[Dict[str, Any]]:
    """
    Fetches a page of users from the database
    Args:
        page_size: Number of users to fetch per page
        offset: Starting position for the page
    Returns:
        List of user dictionaries for the requested page
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        return cursor.fetchall()
    except Exception as e:
        print(f"Error paginating users: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def lazy_paginate(page_size: int) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Generator that lazily fetches pages of users
    Args:
        page_size: Number of users to fetch per page
    Yields:
        List of user dictionaries for each page
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # No more users to fetch
            break
        yield page
        offset += page_size
