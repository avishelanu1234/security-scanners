import sqlite3
import logging
import threading

# Configure logging with structured format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thread-safe connection pool setup with lifecycle management and monitoring
class ConnectionPool:
    def __init__(self, db_file, pool_size=5, unclosed_threshold=3):
        self.pool_size = pool_size
        self.db_file = db_file
        self.lock = threading.Lock()
        self.pool = [self.create_connection() for _ in range(pool_size)]
        self.checked_out_connections = 0
        self.unclosed_threshold = unclosed_threshold

    def create_connection(self):
        conn = sqlite3.connect(self.db_file)
        return conn

    def get_connection(self):
        with self.lock:
            if self.pool:
                self.checked_out_connections += 1
                if self.checked_out_connections > self.unclosed_threshold:
                    logging.warning(f"Alert: High number of unclosed connections: {self.checked_out_connections}")
                return self.pool.pop()
            else:
                raise Exception("No available connections in the pool.")

    def return_connection(self, conn):
        with self.lock:
            try:
                # Validate connection by executing a lightweight query
                conn.execute('SELECT 1')
                self.pool.append(conn)
                self.checked_out_connections -= 1
            except sqlite3.Error:
                # If connection is invalid, recreate and add
                new_conn = self.create_connection()
                self.pool.append(new_conn)
                self.checked_out_connections -= 1

# Initialize the connection pool
connection_pool = ConnectionPool('database.db')

# Async function to get user data securely
async def get_user_data(username, sanitize_input, get_username_regex, logging):
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
