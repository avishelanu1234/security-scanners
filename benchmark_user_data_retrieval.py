import time
import asyncio
from sast_runner import get_user_data

async def benchmark_user_data_retrieval(username, runs=5):
    total_time = 0.0
    for i in range(runs):
        start_time = time.time()
        await get_user_data(username)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Run {i+1} execution time for user '{username}': {execution_time:.4f} seconds")
        total_time += execution_time
    average_time = total_time / runs
    print(f"Average execution time for user '{username}' over {runs} runs: {average_time:.4f} seconds")

if __name__ == '__main__':
    username = input("Enter username to benchmark: ").strip()
    asyncio.run(benchmark_user_data_retrieval(username))
