import asyncio
import unittest
from database import connection_pool

class TestConnectionPoolConcurrency(unittest.TestCase):

    def test_concurrent_connection_acquire_release(self):
        async def task():
            conn = connection_pool.get_connection()
            await asyncio.sleep(0.01)  # Simulate work
            connection_pool.return_connection(conn)

        async def run_concurrent_tasks():
            tasks = [task() for _ in range(connection_pool.pool_size)]
            await asyncio.gather(*tasks)

        asyncio.run(run_concurrent_tasks())
        # If no exceptions, test passes

    def test_pool_exhaustion(self):
        conns = []
        # Acquire all connections
        for _ in range(connection_pool.pool_size):
            conns.append(connection_pool.get_connection())
        # Pool should be empty now
        with self.assertRaises(Exception) as context:
            connection_pool.get_connection()
        self.assertEqual(str(context.exception), "No available connections in the pool.")
        # Return all connections
        for conn in conns:
            connection_pool.return_connection(conn)

    def test_connection_reuse(self):
        conn1 = connection_pool.get_connection()
        connection_pool.return_connection(conn1)
        conn2 = connection_pool.get_connection()
        self.assertIs(conn1, conn2, "Connection was not reused from the pool")
        connection_pool.return_connection(conn2)

if __name__ == '__main__':
    unittest.main()
