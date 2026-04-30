import logging
import re
import asyncio
from html import escape
from typing import List, Optional
from database import get_user_data

# Configure logging with verbosity setting
VERBOSE = True
log_level = logging.INFO if VERBOSE else logging.WARNING
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Cached compiled regex patterns for vulnerability detection
CACHED_USERNAME_REGEX = re.compile(r'^[\w\-]+$')

ACCEPTABLE_PATTERNS = [
    re.compile(r'^[\w_.+-]+@[\w-]+\.[a-zA-Z]{2,}$'),
    CACHED_USERNAME_REGEX,
    re.compile(r'^\d+$'),
    re.compile(r'^[\w\-]+@[\w]+\.[\w]{2,3}$'),
    re.compile(r'^\d{1,5}$'),
    re.compile(r'^[\w\-]+\s?\w*$'),
    re.compile(r'^[a-zA-Z\-]+$'),
]

# SQL injection detection

def detect_vulnerabilities(input_string):
    # Perform a simple length check before regex matching
    if len(input_string) == 0 or len(input_string) > 100:
        logging.warning(f"Input length invalid for potential SQL injection: '{input_string}'")
        return True

    # Use cached compiled regex specifically for username validation
    if CACHED_USERNAME_REGEX.match(input_string):
        logging.info("Input is valid.")
        return False

    if any(pattern.match(input_string) for pattern in ACCEPTABLE_PATTERNS):
        logging.info("Input is valid.")
        return False
    else:
        logging.warning(f"Potential SQL injection detected for input: '{input_string}'!")
        return True

# Batch processing for user data retrieval
async def process_usernames(usernames: List[str]):
    tasks = []
    for username in usernames:
        if detect_vulnerabilities(username):
            logging.warning(f"Potential SQL injection detected for username: {username}")
            continue
        tasks.append(get_user_data(username))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Example usage with batch input handling
async def main(usernames: Optional[List[str]] = None):
    if usernames is None:
        # Single input mode
        user_input = input("Enter username: ").strip()
        usernames = [user_input]
    results = await process_usernames(usernames)
    for result in results:
        if isinstance(result, Exception):
            print(f"Error: {result}")
        else:
            print(result)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Batch mode from command line arguments
        asyncio.run(main(sys.argv[1:]))
    else:
        asyncio.run(main())
