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

## 7. Advanced SQL Injection Payloads Walkthrough

**Objective:** Demonstrate detection and prevention of advanced SQL injection payloads such as blind and time-based injection.

```python
import time
import re
import logging

logging.basicConfig(level=logging.INFO)

# Simulated function to detect time-based delay injection payloads

def detect_advanced_sql_injection(input_string):
    # Patterns to detect typical blind/time-based injection keywords
    patterns = [r"(sleep\s*\()", r"(benchmark\s*\()", r"(waitfor\s+delay)", r"(or\s+1=1)", r"(union\s+select)"]
    for pattern in patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            logging.warning(f"Advanced SQL injection pattern detected: {pattern}")
            return True
    return False

# Test inputs
inputs = [
    "normalUser",
    "admin' OR '1'='1' --",
    "1; waitfor delay '00:00:05' --",
    "username' UNION SELECT password FROM users --"
]

for inp in inputs:
    print(f"Testing input: {inp}")
    if detect_advanced_sql_injection(inp):
        print("Advanced SQL injection detected.")
    else:
        print("Input passed validation.")
```

**Expected outcome:**
- Injection payloads using time delays, union selects, or tautologies are detected and flagged.

---

## 8. Integration with MySQL Using Prepared Statements Walkthrough

**Objective:** Show how to safely execute queries with MySQL using prepared statements.

```python
import mysql.connector

# Setup connection
conn = mysql.connector.connect(
    host='localhost',
    user='user',
    password='password',
    database='testdb'
)
cursor = conn.cursor()

# Malicious input
malicious_input = "admin'; DROP TABLE users; --"

# Safe query using prepared statements
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (malicious_input,))
results = cursor.fetchall()
print("Query executed safely in MySQL.")

cursor.close()
conn.close()
```

**Expected outcome:**
- Query executes without injection risk.

---

## 9. Integration with PostgreSQL Using Psycopg2 Walkthrough

**Objective:** Demonstrate safe query execution in PostgreSQL using psycopg2 parameterized queries.

```python
import psycopg2

# Setup connection
conn = psycopg2.connect(dbname="testdb", user="user", password="password", host="localhost")
cursor = conn.cursor()

# Malicious input
malicious_input = "admin'; DROP TABLE users; --"

# Safe query
cursor.execute("SELECT * FROM users WHERE username = %s", (malicious_input,))
results = cursor.fetchall()
print("Query executed safely in PostgreSQL.")

cursor.close()
conn.close()
```

**Expected outcome:**
- Query executes safely without injection.

---

## 10. Integration with Django ORM Walkthrough

**Objective:** Show how Django ORM automatically uses parameterized queries to prevent SQL injection.

```python
from django.contrib.auth.models import User

# Malicious input
malicious_input = "admin'; DROP TABLE users; --"

# Safe query using Django ORM
users = User.objects.filter(username=malicious_input)
print(f"Found {users.count()} users with given username.")
```

**Expected outcome:**
- Query safely executed without injection risk.

---

## 11. Integration with Flask and SQLAlchemy Walkthrough

**Objective:** Demonstrate safe query construction with SQLAlchemy in Flask.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

with app.app_context():
    db.create_all()
    db.session.add(User(username='admin'))
    db.session.commit()

    malicious_input = "admin'; DROP TABLE users; --"
    user = User.query.filter_by(username=malicious_input).first()
    if user:
        print(f"User found: {user.username}")
    else:
        print("No user found.")
```

**Expected outcome:**
- Query safely executed with no injection risk.

---

These additional walkthroughs cover advanced SQL injection payloads and demonstrate integration with common database environments and web frameworks, further strengthening detection and prevention capabilities.