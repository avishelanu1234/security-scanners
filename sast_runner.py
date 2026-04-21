# Updated sast_runner.py to prevent SQL injection vulnerabilities

import sqlite3

# Function to get user data securely

def get_user_data(username):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    
    # Fetch and return data
    return cursor.fetchall()
    
# Example usage
if __name__ == '__main__':
    user_input = "example_user"  # This should come from a safe input method
    result = get_user_data(user_input)
    print(result)
