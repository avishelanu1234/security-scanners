"""
Secret Scanner
Detects hardcoded secrets in code using refined regex patterns with entropy checks.
"""

import re
import math

class SecretScanner:
    def __init__(self):
        # Refined regex pattern for hardcoded secrets with exclusions for common non-secret keywords
        # Added more exclusions like 'notoken', 'nopassword', 'password123', 'passphrase', 'apikeytest', etc.
        # Increased minimum secret length to 25 characters to reduce false positives
        self.hardcode_pattern = re.compile(
            r"(?i)\b(?!tokenize|passwordless|notoken|nopassword|password123|passphrase|apikeytest|secret123|dummy|example|changeme|default|sample|testkey|placeholder)"
            r"(api[-_] ?key|apikey|token|secret|password|passwd|auth|access[-_] ?key|secret[-_] ?key|private[-_] ?key|client[-_] ?secret|client[-_] ?key)\b\s*[:=]\s*['"]"
            r"[a-zA-Z0-9_\-\.\+=\/]{25,}['"]"
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
            secret_value = re.search(r"['\"]([a-zA-Z0-9_\-\.\+=\/]{25,})['\"]", match.group(0))
            if secret_value:
                secret_str = secret_value.group(1)
                entropy = self._calculate_entropy(secret_str)
                # Adjusted threshold entropy to consider it a likely secret (e.g., >4.0)
                if entropy > 4.0:
                    violations.append(
                        f"Possible hardcoded secret detected: '{match.group(1)}'. Use secure secret management instead."
                    )

        return violations

# Example usage
if __name__ == '__main__':
    sample_code = """
    api_key = '1234567890abcdef1234567890abcdef'
    password: 'mypassword1234'
    token = 'tokenvalue12345tokenvalue12345tokenvalue12345'
    """
    scanner = SecretScanner()
    results = scanner.scan_code(sample_code)
    if results:
        for msg in results:
            print(msg)
    else:
        print("No hardcoded secrets detected.")
