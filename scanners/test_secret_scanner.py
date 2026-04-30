import unittest
from scanners.secret_scanner import SecretScanner

class TestSecretScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = SecretScanner()

    def test_detects_valid_secrets(self):
        code_samples = [
            "api_key = '1234567890abcdef12345'",
            'token: "abcd1234efgh5678ijklmnopqrst"',
            'password = "mypassword1234567890abcd"',
            'client_secret = "secretclientkey1234567890"',
            'access_key = "AKIAIOSFODNN7EXAMPLE"',  # AWS access key
            'secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"'  # AWS secret key
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
            'access_key = "AKIAIOS"',  # too short
            'secret_key = "wJalrXUtn"'  # too short
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
            'secretariat = "office"',
            'passwords = "lists"'
        ]
        for code in code_samples:
            with self.subTest(code=code):
                results = self.scanner.scan_code(code)
                self.assertFalse(results, f"Should not detect secret in: {code}")

    def test_edge_cases(self):
        code_samples = [
            'api-key= "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6"',
            'token = "1234567890abcdef1234567890abcdef"',
            'password = "thisisaverylongpasswordthatexceeds20chars"',
            'secret = "!!invalidcharacters$$$"',  # invalid chars, should not match
            'auth = "a"*25',  # not a string literal, should not match
            'client_secret = "short"',  # too short
        ]
        expected_results = [True, True, True, False, False, False]
        for code, expected in zip(code_samples, expected_results):
            with self.subTest(code=code):
                results = self.scanner.scan_code(code)
                if expected:
                    self.assertTrue(results, f"Should detect secret in: {code}")
                else:
                    self.assertFalse(results, f"Should not detect secret in: {code}")

if __name__ == '__main__':
    unittest.main()
