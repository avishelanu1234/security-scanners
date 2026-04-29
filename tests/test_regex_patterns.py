import re
import unittest

class TestRegexPatterns(unittest.TestCase):

    def setUp(self):
        # Define regex patterns
        self.regex_patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@(?!.*(example|test|dev|tempmail|mailinator|10minutemail|dev\.example\.com|test\.example\.com)$)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'api_key': r'\b(API_KEY|SECRET|TOKEN|ACCESS_TOKEN|sk_|pk_)\b[:;=]\s*[a-zA-Z0-9._-]{32,64}',
            'numeric_string': r'(?<![a-zA-Z])\d{8,12}(?![a-zA-Z])',
            'valid_email': r'^[a-zA-Z0-9._%+-]+@(test|dev|staging)\.(example|test)\.[a-zA-Z]{2,}$',
            'complex_api_key': r'\b(API_KEY|SECRET|TOKEN)\s*[:=;\s]+\s*(?=.*[!@#$%^&*()_+]).{20,64}',
            'general_secret': r'(?<!#|//|/\*|\s)(API_KEY|SECRET|TOKEN|PASSWORD|PASS)\s*[=:;\s]+\s*[^\"\s]+',
            'hash': r'\b[0-9a-f]{40}\b|\b[0-9a-f]{64}\b'
        }

    def test_email_patterns(self):
        valid_emails = [
            'test@example.com',
            'user.name+tag+sorting@example.com',
            'user@example.co.uk'
        ]
        invalid_emails = [
            'plainaddress',
            '@missingusername.com',
            'username@.com'
        ]
        for email in valid_emails:
            self.assertRegex(email, self.regex_patterns['email'])
        for email in invalid_emails:
            self.assertNotRegex(email, self.regex_patterns['email'])

    def test_api_key_patterns(self):
        valid_keys = [
            'API_KEY=12345678901234567890123456789012',
            'TOKEN:abcde1234567890abcdef1234567890abcdef'
        ]
        invalid_keys = [
            'API_KEY=shortkey',
            'TOKEN=12345'
        ]
        for key in valid_keys:
            self.assertRegex(key, self.regex_patterns['api_key'])
        for key in invalid_keys:
            self.assertNotRegex(key, self.regex_patterns['api_key'])

    def test_numeric_string_patterns(self):
        valid_numbers = ['1234567890', '987654321012']
        invalid_numbers = ['abc123', '12345abc']
        for number in valid_numbers:
            self.assertRegex(number, self.regex_patterns['numeric_string'])
        for number in invalid_numbers:
            self.assertNotRegex(number, self.regex_patterns['numeric_string'])

if __name__ == '__main__':
    unittest.main()