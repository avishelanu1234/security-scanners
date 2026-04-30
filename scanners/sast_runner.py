import sqlite3
import logging
import re
import json
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Precompile regex patterns once for reuse
SQL_INJECTION_PATTERN = re.compile(r"(?i)(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|EXEC|UNION|AND|OR|NOT|WHERE|FROM|HAVING|--|;|\bOR\b|\bAND\b)\b|--|;|\bUNION\b|\bOR\b|\bAND\b)")
AWS_CREDENTIAL_PATTERN = re.compile(r'\b(AKIA|ASIA)[0-9A-Z]{16}\b')
API_KEY_PATTERN = re.compile(r'\b(?i)([A-Za-z0-9]{32}|[A-Za-z0-9]{40}|[A-F0-9]{40}|(?<=api_key=)[A-Za-z0-9]{32})\b')
AZURE_CREDENTIAL_PATTERN = re.compile(r'\bAZURE[A0-9]{36}\b')
GOOGLE_CLOUD_API_KEY_PATTERN = re.compile(r'\bAIza[0-9A-Za-z-_]{35}\b')
USERNAME_PATTERN = re.compile('^[a-zA-Z0-9]{1,50}$')

# Async function to get user data securely
async def get_user_data(username):
    if not USERNAME_PATTERN.match(username):
        raise ValueError("Invalid username input. Must be alphanumeric and 1-50 characters long.")

    try:
        loop = asyncio.get_event_loop()
        # Run blocking DB call in executor to avoid blocking event loop
        result = await loop.run_in_executor(None, query_user_from_db, username)
        return result
    except Exception as e:
        logging.error(f"Error retrieving user data: {e}")
        return None

# Blocking function to query user from DB
def query_user_from_db(username):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))
            return None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return None

# Function to detect vulnerabilities in user input
async def detect_vulnerabilities(user_input):
    vulnerabilities = []

    if SQL_INJECTION_PATTERN.search(user_input):
        vulnerabilities.append("Potential SQL Injection detected.")

    return vulnerabilities

# Function to detect cloud-specific vulnerabilities
async def detect_cloud_vulnerabilities(user_input):
    vulnerabilities = await detect_vulnerabilities(user_input)

    if AWS_CREDENTIAL_PATTERN.search(user_input):
        vulnerabilities.append("Potential AWS credential exposed.")

    if API_KEY_PATTERN.search(user_input):
        vulnerabilities.append("Potential API key exposed.")

    if AZURE_CREDENTIAL_PATTERN.search(user_input):
        vulnerabilities.append("Potential Azure credential exposed.")

    if GOOGLE_CLOUD_API_KEY_PATTERN.search(user_input):
        vulnerabilities.append("Potential Google Cloud API key exposed.")

    return vulnerabilities

# Function for user feedback on false positives
async def get_user_feedback(vulnerabilities):
    if not vulnerabilities:
        return "No vulnerabilities detected."

    feedback = {}
    feedback['detected_vulnerabilities'] = vulnerabilities
    feedback['false_positives'] = []
    logging.info(f"Detected vulnerabilities: {vulnerabilities}")

    for vulnerability in vulnerabilities:
        if vulnerability.startswith("Potential SQL Injection"):
            feedback['false_positives'].append(vulnerability)

    with open('user_feedback.json', 'w') as f:
        json.dump(feedback, f)

    return feedback['false_positives']

# Main async function
async def main():
    user_input = input("Enter username: ").strip()
    vulnerabilities = await detect_cloud_vulnerabilities(user_input)
    false_positives = await get_user_feedback(vulnerabilities)

    if false_positives:
        logging.info(f"User reported false positives: {false_positives}")
    elif vulnerabilities:
        for vulnerability in vulnerabilities:
            logging.warning(vulnerability)
    else:
        result = await get_user_data(user_input)
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
