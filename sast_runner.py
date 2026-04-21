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
    
# Example usage
if __name__ == '__main__':
    user_input = input("Enter username: ").strip()  # Dynamic input
    result = get_user_data(user_input)
    print(result)