import time
import asyncio
from sast_runner import get_user_data

async def benchmark_user_data_retrieval(username):
    start_time = time.time()
    await get_user_data(username)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for user '{username}': {execution_time:.4f} seconds")

if __name__ == '__main__':
    username = input("Enter username to benchmark: ").strip()
    asyncio.run(benchmark_user_data_retrieval(username))