import sqlite3
import threading
import logging

# Thread-safe connection pool setup with waiting mechanism
class ConnectionPool:
    def __init__(self, db_file, pool_size=5):
        self.pool_size = pool_size
        self.db_file = db_file
        self.lock = threading.Lock()
        self.pool = [self.create_connection() for _ in range(pool_size)]
        self.condition = threading.Condition(self.lock)

    def create_connection(self):
        return sqlite3.connect(self.db_file)

    def get_connection(self):
        with self.condition:
            while not self.pool:
                self.condition.wait()  # Wait for a connection to be returned
            return self.pool.pop()

    def return_connection(self, conn):
        with self.condition:
            self.pool.append(conn)
            self.condition.notify()

# Improved async-compatible database query function
async def query_user_data(connection_pool, username):
    connection = connection_pool.get_connection()
    try:
        cursor = connection.cursor()
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
    except sqlite3.Error as e:
        logging.error(f"Database error for user '{username}': {e}")
        raise
    finally:
        connection_pool.return_connection(connection)
