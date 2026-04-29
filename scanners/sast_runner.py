import sqlite3
import logging
import re  # Import regex module
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        return None
    
# Function to detect vulnerabilities in user input

def detect_vulnerabilities(user_input):
    vulnerabilities = []
    # Refined rule: Check for SQL injection patterns in the input
    if re.search(r'((?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b)', user_input):
        vulnerabilities.append("Potential SQL Injection detected.")
    return vulnerabilities

# Function to detect cloud-specific vulnerabilities

def detect_cloud_vulnerabilities(user_input):
    vulnerabilities = detect_vulnerabilities(user_input)  # Existing SQL injection check
    # Add cloud-specific checks

    # Check for exposed AWS credentials using refined pattern
    if re.search(r'AKIA[0-9A-Z]{16}', user_input):
        vulnerabilities.append("Potential AWS credential exposed.")
    
    # Check for exposed API keys (generic pattern)
    if re.search(r'(?i)(?:[A-Za-z0-9]{32}|[A-Za-z0-9]{40}|[A-F0-9]{40})', user_input):
        vulnerabilities.append("Potential API key exposed.")
    
    # Check for Azure credentials with refined regex
    if re.search(r'AZURE[A-Z0-9]{40}', user_input):
        vulnerabilities.append("Potential Azure credential exposed.")
    
    # Check for Google Cloud credentials with refined regex
    if re.search(r'AIza[0-9A-Za-z-_]{35}', user_input):
        vulnerabilities.append("Potential Google Cloud API key exposed.")
    
    return vulnerabilities

# Function for user feedback on false positives

def get_user_feedback(vulnerabilities):
    if not vulnerabilities:
        return "No vulnerabilities detected."
    feedback = {}
    feedback['detected_vulnerabilities'] = vulnerabilities
    feedback['false_positives'] = []
    # Log the detected vulnerabilities
    logging.info(f"Detected vulnerabilities: {vulnerabilities}")
    
    # In a non-interactive environment, simulate user response
    # Here, we mock user feedback for CI/CD integration
    # In production, this should be replaced with actual feedback handling
    for index, vulnerability in enumerate(vulnerabilities):
        # Simulating user feedback (mock response)
        if vulnerability.startswith("Potential SQL Injection"):  # Example of a false positive
            feedback['false_positives'].append(vulnerability)
    
    # Save feedback to a file for later analysis
    with open('user_feedback.json', 'w') as f:
        json.dump(feedback, f)
    return feedback['false_positives']

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