"""
Secret Scanner
Detects hardcoded secrets in code using refined regex patterns with entropy checks.
"""

import re
import math

class SecretScanner:
    def __init__(self):
        # Further refined regex pattern for hardcoded secrets with exclusions for common non-secret keywords
        # Added more exclusions like 'notoken', 'nopassword', 'password123', 'passphrase', 'apikeytest', etc.
        # Increased minimum secret length to 40 characters to further reduce false positives
        # Added patterns for detecting AWS and Azure keys specifically
        # Added negative lookbehind/lookahead to exclude matches in comments
        self.hardcode_pattern = re.compile(
            r"""(?ix)                          # Ignore case, verbose mode
            (?<!#.*?)                         # Negative lookbehind for single-line comment
            (?<!/\*.*?)                      # Negative lookbehind for start of block comment
            \b                                # Word boundary
            (?!                              # Negative lookahead for excluded keywords
                tokenize|passwordless|notoken|nopassword|password123|passphrase|apikeytest|secret123|dummy|example|changeme|default|sample|testkey|placeholder|dummykey|testsecret|dummyvalue|fakekey
            )
            (api[-_ ]?key|apikey|token|secret|password|passwd|auth|access[-_ ]?key|
             secret[-_ ]?key|private[-_ ]?key|client[-_ ]?secret|client[-_ ]?key|aws_access_key_id|aws_secret_access_key|azure_key)
            \b                               # Word boundary
            \s*[:=]\s*                       # Assignment operator with optional whitespace
            (['\"])                          # Opening quote (captured)
            ([a-zA-Z0-9_\-\.\+=\/]{40,})    # Secret value with min length 40
            \1                              # Matching closing quote
            (?!.*\*/)                       # Negative lookahead for end of block comment
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

    def _has_special_chars(self, data: str) -> bool:
        """
        Check if the string contains special characters that are common in secrets.
        """
        special_chars_pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>]')
        return bool(special_chars_pattern.search(data))

    def scan_code(self, code: str) -> list[str]:
        """
        Scans the given code string for hardcoded secret patterns.
        Returns a list of warning messages if violations are found, empty list otherwise.
        Applies entropy and heuristic checks to reduce false positives.
        """
        violations = []
        if not code:
            return violations

        matches = self.hardcode_pattern.finditer(code)
        for match in matches:
            # Extract the secret value inside quotes
            secret_value = re.search(r"['\"]([a-zA-Z0-9_\-\.\+=\/]{40,})['\"]", match.group(0))
            if secret_value:
                secret_str = secret_value.group(1)
                entropy = self._calculate_entropy(secret_str)
                # Increased threshold entropy to consider it a likely secret (e.g., >5.5)
                if entropy > 5.5 and self._has_special_chars(secret_str):
                    violations.append(
                        f"Possible hardcoded secret detected: '{match.group(1)}'. Use secure secret management instead."
                    )

        return violations

# Example usage
if __name__ == '__main__':
    sample_code = """
    api_key = '1234567890abcdef1234567890abcdef1234567890'
    password: 'mypassword1234'
    token = 'tokenvalue12345tokenvalue12345tokenvalue12345tokenvalue12345tokenvalue12345'
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
