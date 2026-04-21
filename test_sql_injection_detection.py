import unittest
import re

# Assuming the detect_vulnerabilities function is defined in sast_runner.py
from sast_runner import detect_vulnerabilities

class TestSQLInjectionDetection(unittest.TestCase):

    def test_valid_inputs(self):
        valid_inputs = [
            'user_name',
            'user.name',
            'user-name',
            'user123',
            'user@example.com',
            '12345',
            'user name',
            'user name.',
            'user-name 123',
            'user.name@test.com',  # Valid email format
            'user_name123',  # Alphanumeric with underscore
            'user-name-123',  # Hyphenated
            'user name 123',  # Spaces in usernames
        ]
        for input_str in valid_inputs:
            with self.subTest(input=input_str):
                self.assertFalse(detect_vulnerabilities(input_str),
                                 f"{input_str} should not be flagged as a vulnerability.")

    def test_invalid_inputs(self):
        invalid_inputs = [
            "' OR '1'='1",  # Classic SQL injection
            '1; DROP TABLE users;',  # SQL command injection
            'admin --',  # Comment injection
            'user\0',  # Null byte injection
            'user; SELECT * FROM users;',  # Union injection
            '1 OR 1=1',  # Logic injection
            'user/*comment*/name',  # Comment injection with wildcard
            'user; --',  # Comment injection with SQL
            '1; EXEC xp_cmdshell('dir');',  # Command injection
            'user_name; DROP DATABASE;',  # SQL injection with database drop
        ]
        for input_str in invalid_inputs:
            with self.subTest(input=input_str):
                self.assertTrue(detect_vulnerabilities(input_str),
                                f"{input_str} should be flagged as a vulnerability.")

if __name__ == '__main__':
    unittest.main()