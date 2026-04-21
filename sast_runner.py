import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get user data securely

def get_user_data(username):
    if not isinstance(username, str) or not username:
        raise ValueError("Invalid username input. Must be a non-empty string.")  # Validate user input
    
    # Additional validation: check length and allowed characters
    if len(username) > 30 or not username.isalnum():
        raise ValueError("Invalid username. Must be alphanumeric and less than 30 characters.")
    
    try:
        # Connect to the database using an environment variable for the database path
        db_path = os.getenv('DATABASE_PATH', 'database.db')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            
            # Fetch and return data
            return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")  # Error handling
        return None
    
# Example usage
if __name__ == '__main__':
    user_input = "example_user"  # This should come from a safe input method
    result = get_user_data(user_input)
    print(result)