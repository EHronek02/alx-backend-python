# Python Generators for Efficient Data Processing

This project demonstrates advanced usage of Python generators to handle large datasets efficiently, with practical implementations for database operations, batch processing, pagination, and aggregate calculations.

## Table of Contents
1. [Database Setup](#1-database-setup)
2. [Streaming Users One-by-One](#2-streaming-users-one-by-one)
3. [Batch Processing](#3-batch-processing)
4. [Lazy Pagination](#4-lazy-pagination)
5. [Memory-Efficient Aggregates](#5-memory-efficient-aggregates)

---

## 1. Database Setup
### `seed.py`
Sets up a MySQL database and populates it with user data.

**Features:**
- Creates `ALX_prodev` database
- Defines `user_data` table with proper schema
- Imports data from CSV file
- Handles duplicate entries

**Usage:**
```python
from seed import connect_db, create_database, connect_to_prodev, create_table, insert_data

# Initialize database
connection = connect_db()
create_database(connection)
connection.close()

# Setup table and data
connection = connect_to_prodev()
create_table(connection)
insert_data(connection, 'user_data.csv')
