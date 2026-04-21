import sqlite3
import cProfile
import pstats
import io

# Function to get user data securely

def get_user_data(username):
    if not isinstance(username, str) or not username:
        raise ValueError("Invalid username input.")
    
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            return cursor.fetchone()  # Use fetchone() for single user data
    except sqlite3.Error as e:
        print(f"Database error: {e}")  # Error handling
        return None

# Performance testing function

def profile_function():
    user_input = "example_user"  # Example username
    result = get_user_data(user_input)
    print(result)

if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    
    profile_function()
    
    pr.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
