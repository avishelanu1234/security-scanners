import sqlite3
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get user data securely

def get_user_data(username):
    # Enhanced input validation using regex
    if not isinstance(username, str) or not username or len(username) > 50 or not re.match(r'^[\w_]+$', username):
        raise ValueError("Invalid username input.")  # Validate user input
    
    try:
        # Connect to the database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
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
        logging.error(f"Database error for user '{username}': {e}")
        raise  # Re-raise the exception for further handling

# SQL injection detection logic

def detect_vulnerabilities(input_string):
    # Whitelist of acceptable patterns (example)
    acceptable_patterns = [r'^[\w_]+$', r'^[\d]+$']  # Example patterns
    
    # Check against the whitelisted patterns
    if any(re.match(pattern, input_string) for pattern in acceptable_patterns):
        logging.info("Input is valid.")
        return False  # No vulnerabilities detected
    else:
        logging.warning("Potential SQL injection detected!")
        return True  # Potential vulnerability

# Example usage of vulnerability detection
if __name__ == '__main__':
    user_input = input("Enter username: ").strip()  # Dynamic input
    if detect_vulnerabilities(user_input):
        print("Potential SQL injection detected!")
    else:
        result = get_user_data(user_input)
        print(result)