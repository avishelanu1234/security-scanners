import sqlite3
import logging
import re  # Import regex module
import json
from threading import Lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Compile regex patterns at module level for performance
SQL_INJECTION_PATTERN = re.compile(r"(?i)(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|EXEC|UNION|AND|OR|NOT|WHERE|FROM|HAVING|--|;|\bOR\b|\bAND\b)\b|--|;|\bUNION\b|\bOR\b|\bAND\b)")
AWS_CREDENTIAL_PATTERN = re.compile(r'\b(AKIA|ASIA)[0-9A-Z]{16}\b')
API_KEY_PATTERN = re.compile(r'\b(?i)([A-Za-z0-9]{32}|[A-Za-z0-9]{40}|[A-F0-9]{40}|(?<=api_key=)[A-Za-z0-9]{32})\b')
AZURE_CREDENTIAL_PATTERN = re.compile(r'\bAZURE[A0-9]{36}\b')
GOOGLE_CLOUD_API_KEY_PATTERN = re.compile(r'\bAIza[0-9A-Za-z-_]{35}\b')

# Thread-safe feedback storage
_feedback_lock = Lock()
_feedback_cache = []

# Function to get user data securely
def get_user_data(username):
    # Regex for valid username (alphanumeric, 1-50 characters)
    if not re.match('^[a-zA-Z0-9]{1,50}$', username):
        raise ValueError("Invalid username input. Must be alphanumeric and 1-50 characters long.")  # Validate user input
    
    try:
        # Connect to the database
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            
            # Fetch and return data as a dictionary
            columns = [column[0] for column in cursor.description]
            result = cursor.fetchone()
            if result:
                return dict(zip(columns, result))  # Convert to dictionary
            return None  # No user found
    except sqlite3.IntegrityError as e:
        logging.error(f"Database integrity error: {e}")  # Error handling
        return None
    except sqlite3.OperationalError as e:
        logging.error(f"Database operational error: {e}")  # Error handling
        return None
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")  # Error handling

# Function to detect vulnerabilities in user input
def detect_vulnerabilities(user_input):
    vulnerabilities = []
    if SQL_INJECTION_PATTERN.search(user_input):
        vulnerabilities.append("Potential SQL Injection detected.")
    
    # Additional OWASP pattern detections
    # Detect Cross-Site Scripting (XSS) patterns
    if re.search(r'<script|<img|onerror=|onload=|javascript:', user_input, re.IGNORECASE):
        vulnerabilities.append("Potential Cross-Site Scripting (XSS) detected.")
    
    # Detect Command Injection patterns
    if re.search(r'\b(cat|ls|curl|wget|bash|sh|nc|netcat|python|perl|php|ruby|java|powershell|cmd)\b', user_input, re.IGNORECASE):
        vulnerabilities.append("Potential Command Injection detected.")
    
    # Detect Path Traversal patterns
    if re.search(r'(\.\./|/etc/passwd|/bin/bash)', user_input):
        vulnerabilities.append("Potential Path Traversal detected.")
    
    return vulnerabilities

# Function to detect cloud-specific vulnerabilities
def detect_cloud_vulnerabilities(user_input):
    vulnerabilities = detect_vulnerabilities(user_input)  # Existing SQL injection and new OWASP checks
    
    if AWS_CREDENTIAL_PATTERN.search(user_input):
        vulnerabilities.append("Potential AWS credential exposed.")
    
    if API_KEY_PATTERN.search(user_input):
        vulnerabilities.append("Potential API key exposed.")
    
    if AZURE_CREDENTIAL_PATTERN.search(user_input):
        vulnerabilities.append("Potential Azure credential exposed.")
    
    if GOOGLE_CLOUD_API_KEY_PATTERN.search(user_input):
        vulnerabilities.append("Potential Google Cloud API key exposed.")
    
    return vulnerabilities

# Optimized function for user feedback on false positives
# Uses in-memory cache and thread-safe lock to batch feedback
# Writing to file can be done periodically or at program exit

def get_user_feedback(vulnerabilities):
    if not vulnerabilities:
        return "No vulnerabilities detected."
    feedback = {}
    feedback['detected_vulnerabilities'] = vulnerabilities
    feedback['false_positives'] = []
    
    logging.info(f"Detected vulnerabilities: {vulnerabilities}")
    
    for vulnerability in vulnerabilities:
        if vulnerability.startswith("Potential SQL Injection"):
            feedback['false_positives'].append(vulnerability)
    
    # Use thread-safe cache
    with _feedback_lock:
        _feedback_cache.append(feedback)
        # For demonstration, write to file only if cache size reaches 10
        if len(_feedback_cache) >= 10:
            _write_feedback_to_file()
    return feedback['false_positives']


def _write_feedback_to_file():
    try:
        with open('user_feedback.json', 'w') as f:
            json.dump(_feedback_cache, f)
        _feedback_cache.clear()
    except Exception as e:
        logging.error(f"Error writing user feedback to file: {e}")


# On program exit, ensure feedback is saved
def _save_feedback_on_exit():
    with _feedback_lock:
        if _feedback_cache:
            _write_feedback_to_file()

import atexit
atexit.register(_save_feedback_on_exit)

# Example usage
if __name__ == '__main__':
    user_input = input("Enter username: ").strip()  # Dynamic input
    vulnerabilities = detect_cloud_vulnerabilities(user_input)  # Use new function
    false_positives = get_user_feedback(vulnerabilities)  # Get user feedback
    if false_positives:
        logging.info(f"User reported false positives: {false_positives}")
    elif vulnerabilities:
        for vulnerability in vulnerabilities:
            logging.warning(vulnerability)  # Log vulnerabilities
    else:
        result = get_user_data(user_input)
        print(result)
