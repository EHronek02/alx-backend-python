from typing import Generator
import mysql.connector
import seed

def stream_user_ages() -> Generator[int, None, None]:
    """
    Generator that streams user ages from the database one by one
    Yields:
        int: User age
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return
    
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if not row:
                break
            yield row[0]
            
    except mysql.connector.Error as e:
        print(f"Error streaming user ages: {e}")
    finally:
        if cursor:
            cursor.close()
        connection.close()

def calculate_average_age() -> float:
    """
    Calculates the average age of users using the stream_user_ages generator
    Returns:
        float: Average age
    """
    total_age = 0
    count = 0
    
    # First loop: iterate through ages from generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0.0
    
    return total_age / count

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
