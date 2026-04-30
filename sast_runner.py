import sqlite3
import logging
import re
import asyncio
import threading
from html import escape

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-safe connection pool setup
class ConnectionPool:
    def __init__(self, db_file, pool_size=5):
        self.pool_size = pool_size
        self.db_file = db_file
        self.lock = threading.Lock()
        self.pool = [self.create_connection() for _ in range(pool_size)]

    def create_connection(self):
        return sqlite3.connect(self.db_file)

    def get_connection(self):
        with self.lock:
            if self.pool:
                return self.pool.pop()
            else:
                raise Exception("No available connections in the pool.")

    def return_connection(self, conn):
        with self.lock:
            self.pool.append(conn)

# Initialize the connection pool
connection_pool = ConnectionPool('database.db')

# Improved regex for username validation
USERNAME_REGEX = re.compile(r'^[\w\-]{1,50}$')

# Regex patterns for vulnerability detection
ACCEPTABLE_PATTERNS = [
    re.compile(r'^[\w_.+-]+@[\w-]+\.[a-zA-Z]{2,}$'),
    re.compile(r'^[\w\-]+$'),
    re.compile(r'^\d+$'),
    re.compile(r'^[\w\-]+@[\w]+\.[\w]{2,3}$'),
    re.compile(r'^\d{1,5}$'),
    re.compile(r'^[\w\-]+\s?\w*$'),
    re.compile(r'^[a-zA-Z\-]+$'),
]

# Centralized input sanitization

def sanitize_input(user_input: str) -> str:
    return escape(user_input)

# Asynchronous function to get user data securely
async def get_user_data(username):
    sanitized_username = sanitize_input(username)
    if not isinstance(sanitized_username, str) or not USERNAME_REGEX.match(sanitized_username):
        raise ValueError("Invalid username input.")
    
    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
        query = "SELECT id, username, email FROM users WHERE username = ?"
        cursor.execute(query, (sanitized_username,))
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None
    except sqlite3.Error as e:
        logging.error(f"Database error for user '{sanitized_username}': {e}")
        raise
    finally:
        connection_pool.return_connection(connection)

# SQL injection detection

def detect_vulnerabilities(input_string):
    if any(pattern.match(input_string) for pattern in ACCEPTABLE_PATTERNS):
        logging.info("Input is valid.")
        return False
    else:
        logging.warning(f"Potential SQL injection detected for input: '{input_string}'!")
        return True

# Example usage
async def main():
    user_input = input("Enter username: ").strip()
    if detect_vulnerabilities(user_input):
        print("Potential SQL injection detected!")
    else:
        try:
            result = await get_user_data(user_input)
            print(result)
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as ex:
            print(f"Error: {ex}")

if __name__ == '__main__':
    asyncio.run(main())