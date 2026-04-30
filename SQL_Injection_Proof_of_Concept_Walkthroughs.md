# SQL Injection Proof-of-Concept Walkthroughs

This document provides detailed proof-of-concept (PoC) walkthroughs based on the SQL injection detection rules and improvements defined in the SQL_Injection_Detection_Rules.md file.

---

## 1. Input Validation Walkthrough

**Objective:** Demonstrate how input validation using regex and input constraints prevents SQL injection.

```python
import re

# Function to validate username input
 def validate_username(username):
     if not isinstance(username, str) or not username or len(username) > 50 or not re.match(r'^[\w_]+$', username):
         raise ValueError("Invalid username input.")
     return True

# Test with safe input
try:
    validate_username("valid_user_123")
    print("Safe input passed validation.")
except ValueError as e:
    print(f"Validation failed: {e}")

# Test with malicious input
try:
    validate_username("admin'; DROP TABLE users; --")
except ValueError as e:
    print(f"Validation failed: {e}")
```

**Expected outcome:**
- Safe input passes validation.
- Malicious input triggers ValueError, preventing SQL injection.

---

## 2. Parameterized Queries Walkthrough

**Objective:** Show how parameterized queries protect against injection even if input is malicious.

```python
import sqlite3

# Setup in-memory database and table
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()
cursor.execute('CREATE TABLE users (username TEXT)')
cursor.execute('INSERT INTO users VALUES ("admin")')
conn.commit()

# Malicious input that would cause injection if concatenated directly
malicious_input = "admin'; DROP TABLE users; --"

# Safe parameterized query
try:
    cursor.execute('SELECT * FROM users WHERE username = ?', (malicious_input,))
    result = cursor.fetchall()
    print("Query executed safely, no injection occurred.")
except sqlite3.Error as e:
    print(f"Database error: {e}")

# Verify table still exists
cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users"')
if cursor.fetchone():
    print("Table 'users' still exists.")
else:
    print("Table 'users' was dropped - injection succeeded.")

conn.close()
```

**Expected outcome:**
- Query executes without error.
- Table 'users' remains intact, proving injection was prevented.

---

## 3. Vulnerability Detection Logic Walkthrough

**Objective:** Demonstrate how the whitelist approach detects potential SQL injection attempts.

```python
import re
import logging

logging.basicConfig(level=logging.INFO)

acceptable_patterns = [r'^[\w_]+$', r'^[\d]+$', r'^[\s\w.-]+@[\w.-]+\.\w+$']  # username, digits, email

def detect_sql_injection(input_string):
    if any(re.match(pattern, input_string) for pattern in acceptable_patterns):
        logging.info("Input is valid.")
        return False
    else:
        logging.warning("Potential SQL injection detected!")
        return True

# Test inputs
inputs = [
    "normalUser",
    "123456",
    "user@example.com",
    "admin' OR '1'='1",
    "DROP TABLE users;--"
]

for inp in inputs:
    print(f"Testing input: {inp}")
    if detect_sql_injection(inp):
        print("Potential SQL injection detected.")
    else:
        print("Input passed validation.")
```

**Expected outcome:**
- Valid inputs pass.
- Injection-like inputs are flagged with warnings.

---

## 4. Suggested Improvement: Rate Limiting Walkthrough

**Objective:** Illustrate how rate limiting can be applied to protect from brute force or repeated injection attempts.

```python
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/submit', methods=['POST'])
@limiter.limit("5 per minute")  # Limit to 5 requests per minute per IP
 def submit_form():
     return "Form submitted successfully."

if __name__ == '__main__':
    app.run()
```

**Expected outcome:**
- User can submit form up to 5 times per minute.
- Further requests are rate-limited, reducing attack surface.

---

## 5. Suggested Improvement: Enhanced Logging Walkthrough

**Objective:** Show improved logging capturing IP address and context for injection attempts.

```python
import logging
from flask import request

logging.basicConfig(level=logging.WARNING)

def log_injection_attempt():
    ip = request.remote_addr
    logging.warning(f"Potential SQL injection detected from {ip}!")

# This function would be called when injection is detected
```

**Expected outcome:**
- Logs include IP address, aiding in incident response.

---

## 6. Suggested Improvement: Input Sanitization Walkthrough

**Objective:** Demonstrate additional sanitization of inputs to escape special characters.

```python
import cgi

def sanitize_input(user_input):
    return cgi.escape(user_input)

# Test
raw_input = "admin'; DROP TABLE users; --"
sanitized = sanitize_input(raw_input)
print(f"Sanitized input: {sanitized}")
```

**Expected outcome:**
- Special characters are escaped, reducing injection risk.

---

These walkthroughs provide practical demonstrations of how the detection rules and improvements work to prevent and detect SQL injection vulnerabilities.