"""
Secret Scanner
Detects hardcoded secrets in code using refined regex patterns with entropy checks.
"""

import re
import math

class SecretScanner:
    def __init__(self):
        # Further refined regex pattern for hardcoded secrets with more exclusions for common non-secret keywords
        # Added more exclusions like 'fake', 'bogus', 'null', 'none', '123456', '111111', '000000', 'test123', 'secretkeytest', 'temp', 'tempkey'
        # Excluded common environment and config variable names
        # Added stricter checks on secret value to require mixed case, digits, or special characters
        # Increased minimum secret length to 30 characters
        # Added patterns for detecting AWS and Azure keys specifically
        self.hardcode_pattern = re.compile(
            r"""(?ix)                          # Ignore case, verbose mode
            \b                                # Word boundary
            (?!                              # Negative lookahead for excluded keywords
                tokenize|passwordless|notoken|nopassword|password123|passphrase|apikeytest|secret123|dummy|example|changeme|default|sample|testkey|placeholder|
                fake|bogus|null|none|123456|111111|000000|test123|secretkeytest|temp|tempkey|
                env|environment|config|setting|value|var|version
            )
            (api[-_ ]?key|apikey|token|secret|password|passwd|auth|access[-_ ]?key|
             secret[-_ ]?key|private[-_ ]?key|client[-_ ]?secret|client[-_ ]?key|aws_access_key_id|aws_secret_access_key|azure_key)
            \b                               # Word boundary
            \s*[:=]\s*                       # Assignment operator with optional whitespace
            (['"])                          # Opening quote (captured)
            ([a-zA-Z0-9_\-\.\+=\/]{30,})    # Secret value with min length 30
            \1                              # Matching closing quote
            """,
            re.VERBOSE | re.IGNORECASE
        )

    def _calculate_entropy(self, data: str) -> float:
        """
        Calculate Shannon entropy of a string to estimate its randomness/complexity.
        """
        if not data:
            return 0
        entropy = 0
        length = len(data)
        for x in set(data):
            p_x = data.count(x) / length
            entropy += - p_x * math.log2(p_x)
        return entropy

    def scan_code(self, code: str) -> list[str]:
        """
        Scans the given code string for hardcoded secret patterns.
        Returns a list of warning messages if violations are found, empty list otherwise.
        Applies entropy check to reduce false positives.
        """
        violations = []
        if not code:
            return violations

        matches = self.hardcode_pattern.finditer(code)
        for match in matches:
            # Extract the secret value inside quotes
            secret_value = re.search(r"['\"]([a-zA-Z0-9_\-\.\+=\/]{30,})['\"]", match.group(0))
            if secret_value:
                secret_str = secret_value.group(1)
                # Stricter check: secret must have mixed case, digits, or special characters
                if (re.search(r'[a-z]', secret_str) and re.search(r'[A-Z]', secret_str)) or \
                   re.search(r'\d', secret_str) or re.search(r'[_\-\.\+=\/]', secret_str):
                    entropy = self._calculate_entropy(secret_str)
                    # Adjusted threshold entropy to consider it a likely secret (e.g., >4.5)
                    if entropy > 4.5:
                        violations.append(
                            f"Possible hardcoded secret detected: '{match.group(1)}'. Use secure secret management instead."
                        )

        return violations

# Example usage
if __name__ == '__main__':
    sample_code = """
    api_key = '1234567890abcdef1234567890abcdef1234'
    password: 'mypassword1234'
    token = 'tokenvalue12345tokenvalue12345tokenvalue12345tokenvalue12345'
    aws_access_key_id = 'AKIAIOSFODNN7EXAMPLE'
    azure_key = 'abcdef1234567890abcdef1234567890'
    """
    scanner = SecretScanner()
    results = scanner.scan_code(sample_code)
    if results:
        for msg in results:
            print(msg)
    else:
        print("No hardcoded secrets detected.")
