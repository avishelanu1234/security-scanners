import sqlite3
import logging
import re
import asyncio
import threading
from html import escape
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-safe connection pool setup with configurability
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
                # Wait and retry mechanism
                raise Exception("No available connections in the pool.")

    def return_connection(self, conn):
        with self.lock:
            self.pool.append(conn)

# Initialize the connection pool with configurable size
DB_POOL_SIZE = 10  # Configurable pool size
connection_pool = ConnectionPool('database.db', pool_size=DB_POOL_SIZE)

# Improved regex for username validation (cached)
_cached_username_regex = None

def get_username_regex():
    global _cached_username_regex
    if _cached_username_regex is None:
        _cached_username_regex = re.compile(r'^[\w\-]{1,50}$')
    return _cached_username_regex

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

# Language-specific parsers for vulnerability detection (placeholder implementation)
class LanguageParser:
    def __init__(self, language: str):
        self.language = language

    def parse(self, code: str) -> bool:
        # Placeholder: Implement language-specific parsing logic here
        # Return True if vulnerability detected, False otherwise
        return False

# Registry of parsers
language_parsers = {
    'python': LanguageParser('python'),
    'javascript': LanguageParser('javascript'),
    # Add more language parsers as needed
}

# Asynchronous function to get user data securely
async def get_user_data(username):
    sanitized_username = sanitize_input(username)
    regex = get_username_regex()
    if not isinstance(sanitized_username, str) or not regex.match(sanitized_username):
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

# Batch processing for user data retrieval
async def process_usernames(usernames: List[str]):
    tasks = []
    for username in usernames:
        if detect_vulnerabilities(username):
            logging.warning(f"Potential SQL injection detected for username: {username}")
            continue
        tasks.append(get_user_data(username))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Example usage with batch input handling
async def main(usernames: Optional[List[str]] = None):
    if usernames is None:
        # Single input mode
        user_input = input("Enter username: ").strip()
        usernames = [user_input]
    results = await process_usernames(usernames)
    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(result)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Batch mode from command line arguments
        asyncio.run(main(sys.argv[1:]))
    else:
        asyncio.run(main())
