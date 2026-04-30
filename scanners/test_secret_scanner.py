import unittest
from secret_scanner import SecretScanner

class TestSecretScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SecretScanner()

    def test_detects_valid_secrets(self):
        code_samples = [
            "api_key = '1234567890abcdef'",
            'token: "abcd1234efgh5678ijkl"',
            'password = "mypassword123456"',
            'client_secret = "secretclientkey12345"',
        ]
        for code in code_samples:
            with self.subTest(code=code):
                results = self.scanner.scan_code(code)
                self.assertTrue(results, f"Should detect secret in: {code}")

    def test_ignores_short_non_secrets(self):
        code_samples = [
            'api_key = "abc123"',
            'token: "12345"',
            'password = "pass"',
            'secret = "shrt"',
        ]
        for code in code_samples:
            with self.subTest(code=code):
                results = self.scanner.scan_code(code)
                self.assertFalse(results, f"Should not detect secret in: {code}")

    def test_ignores_non_secret_keywords(self):
        code_samples = [
            'apikeys = "notasecret"',
            'authentication = "none"',
            'accesskey = "123456789012"',  # no underscore or hyphen
            'clientkey = "abcdefghijklmno"',
        ]
        for code in code_samples:
            with self.subTest(code=code):
                results = self.scanner.scan_code(code)
                self.assertFalse(results, f"Should not detect secret in: {code}")

if __name__ == '__main__':
    unittest.main()
