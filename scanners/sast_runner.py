import sqlite3
import logging
import re  # Import regex module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to get user data securely

def get_user_data(username):
    # Regex for valid username (alphanumeric, 1-50 characters)
    if not re.match('^[a-zA-Z0-9]{1,50}$', username):
        raise ValueError("Invalid username input. Must be alphanumeric and 1-50 characters long.")  # Validate user input
    
    try:
        # Connect to the database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            
            # Fetch and return data as a dictionary
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))  # Convert to dictionary
            return None  # No user found
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")  # Error handling
        return None
    
# Example usage
if __name__ == '__main__':
    user_input = input("Enter username: ").strip()  # Dynamic input
    result = get_user_data(user_input)
    print(result)