import sqlite3
import logging
import re

# Configure logging with additional error information
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler('app.log'),  # Log to a file
    logging.StreamHandler()  # Log to console
])

# Maintain a single database connection
connection = sqlite3.connect('database.db')

# Function to get user data securely

def get_user_data(username):
    # Enhanced input validation using regex
    username_pattern = re.compile(r'^[\w_]{1,50}$')  # Compiled regex for username validation
    if not isinstance(username, str) or not username_pattern.match(username):
        logging.error("Invalid username input: %s", username)  # Log error before raising
        raise ValueError("Invalid username input.")  # Validate user input
    
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
        logging.error(f"Database error for user '{username}': {e}")
        raise  # Re-raise the exception for further handling

# SQL injection detection logic

def detect_vulnerabilities(input_string):
    # Expanded whitelist of acceptable patterns to include specific variations and improve accuracy
    acceptable_patterns = [
        r'^[\w_.+-]+@[\w-]+\.[a-zA-Z]{2,}$',  # Valid email format
        r'^[\w_]+$',  # Alphanumeric usernames
        r'^[\d]+$',  # Numeric input
        r'^[\w_]+@[\w]+\.[\w]{2,3}$',  # Shortened email format
        r'^[\d]{1,5}$',  # Numeric input within 1 to 5 digits
        r'^[\w_]+\s*\w*$'  # Two-word usernames
    ]  # Example patterns
    
    # Check against the whitelisted patterns
    if any(re.match(pattern, input_string) for pattern in acceptable_patterns):
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