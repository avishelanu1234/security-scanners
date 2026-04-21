import sqlite3

# Function to get user data securely

def get_user_data(username):
    if not isinstance(username, str) or not username:
        raise ValueError("Invalid username input.")  # Validate user input
    
    try:
        # Connect to the database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            
            # Fetch and return data
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Error handling
        return None
    
# Example usage
if __name__ == '__main__':
    user_input = "example_user"  # This should come from a safe input method
    result = get_user_data(user_input)
    print(result)
