import sqlite3
import logging
import re
import asyncio
from sqlite3 import pool

# Configure logging with structured format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connection pool setup
class ConnectionPool:
    def __init__(self, db_file, pool_size=5):
        self.pool_size = pool_size
        self.pool = [self.create_connection(db_file) for _ in range(pool_size)]

    def create_connection(self, db_file):
        return sqlite3.connect(db_file)

    def get_connection(self):
        if self.pool:
            return self.pool.pop()
        else:
            raise Exception("No available connections in the pool.")

    def return_connection(self, conn):
        self.pool.append(conn)

# Initialize the connection pool
connection_pool = ConnectionPool('database.db')

# Compiled regex for username validation, cached globally
USERNAME_REGEX = re.compile(r'^[\w_]{1,50}$')

# Compiled regex patterns for vulnerability detection, cached globally
ACCEPTABLE_PATTERNS = [
    re.compile(r'^[\w_.+-]+@[\w-]+\.[a-zA-Z]{2,}$'),  # Valid email format
    re.compile(r'^[\w_]+$'),  # Alphanumeric usernames
    re.compile(r'^[\d]+$'),  # Numeric input
    re.compile(r'^[\w_]+@[\w]+\.[\w]{2,3}$'),  # Shortened email format
    re.compile(r'^[\d]{1,5}$'),  # Numeric input within 1 to 5 digits
    re.compile(r'^[\w_]+\s*\w*$'),  # Two-word usernames
    re.compile(r'^[\-a-zA-Z]+$'),  # Allow hyphenated words
    re.compile(r'^[\w\s]+$'),  # Alphanumeric with spaces
    re.compile(r'^[\w\s]+[\.\,\'\"\-]+[\w\s]+$')  # Allows punctuation between words
]

# Asynchronous function to get user data securely
async def get_user_data(username):
    # Validate user input with length check first
    if not isinstance(username, str) or len(username) > 50 or len(username) == 0:
        raise ValueError("Invalid username input.")
    if not USERNAME_REGEX.match(username):
        raise ValueError("Invalid username input.")

    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
        # Use parameterized query to prevent SQL injection
        query = "SELECT id, username, email FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None  # No user found
    except sqlite3.Error as e:
        logging.error(f"Database error occurred: {e}")
        raise ValueError("An error occurred while retrieving user data. Please try again later.")
    finally:
        connection_pool.return_connection(connection)

# SQL injection detection logic

def detect_vulnerabilities(input_string):
    # Check against the whitelisted patterns
    if any(pattern.match(input_string) for pattern in ACCEPTABLE_PATTERNS):
        logging.info("Input is valid.")
        return False  # No vulnerabilities detected
    else:
        logging.warning(f"Potential SQL injection detected for input: '{input_string}'!")
        return True  # Potential vulnerability

# Example usage of vulnerability detection with asyncio
async def main(user_input):
    user_input = user_input.strip()  # Process passed input
    if detect_vulnerabilities(user_input):
        print("Potential SQL injection detected!")
    else:
        result = await get_user_data(user_input)
        print(result)

if __name__ == '__main__':
    user_input = input("Enter username: ")
    asyncio.run(main(user_input))