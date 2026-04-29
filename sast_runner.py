import sqlite3
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to create a database connection context manager
class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logging.error(f"Database error: {exc_value}")
        self.connection.commit()
        self.connection.close()

# Pre-compile regex patterns for performance
username_pattern = re.compile(r'^[\w_]{1,50}$')
acceptable_patterns = re.compile(
    r'^[\w_.+-]+@[\w-]+\.[a-zA-Z]{2,}$|'
    r'^[\w_]+$|'
    r'^[\d]+$|'
    r'^[\w_]+@[\w]+\.[\w]{2,3}$|'
    r'^[\d]{1,5}$|'
    r'^[\w_]+\s*\w*$|'
    r'^[\-a-zA-Z]+$|'
    r'^[\w\s]+$|'
    r'^[\w\s]+[\.,\'\"\-]+[\w\s]+$'
)

# Function to get user data securely

def get_user_data(username):
    if not isinstance(username, str) or not username_pattern.match(username):
        raise ValueError("Invalid username input.")
    
    with Database('database.db') as cursor:
        query = "SELECT id, username, email FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        
        result = cursor.fetchone()
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None

# SQL injection detection logic

def detect_vulnerabilities(input_string):
    if acceptable_patterns.match(input_string):
        logging.info("Input is valid.")
        return False  # No vulnerabilities detected
    else:
        logging.warning(f"Potential SQL injection detected for input: '{input_string}'!")
        return True  # Potential vulnerability

# Example usage of vulnerability detection
if __name__ == '__main__':
    user_input = input("Enter username: ").strip()  # Dynamic input
    if detect_vulnerabilities(user_input):
        print("Potential SQL injection detected!")
    else:
        result = get_user_data(user_input)
        print(result)