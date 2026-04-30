"""
Secret Scanner
Detects hardcoded secrets in code using refined regex patterns.
"""

import re

class SecretScanner:
    def __init__(self):
        # Refined regex pattern for hardcoded secrets
        self.hardcode_pattern = re.compile(
            r"(?i)(api[-_]?key|apikey|token|secret|password|passwd|auth|access[-_]?key|secret[-_]?key|private[-_]?key|client[-_]?secret|client[-_]?key)\s*[:=]\s*['\"]"
            r"[a-zA-Z0-9_\-\.\+=\/]{8,}['\"]"
        )

    def scan_code(self, code: str) -> list[str]:
        """
        Scans the given code string for hardcoded secret patterns.
        Returns a list of warning messages if violations are found, empty list otherwise.
        """
        violations = []
        if not code:
            return violations

        if self.hardcode_pattern.search(code):
            violations.append("Possible hardcoded secret detected. Use secure secret management instead.")

        return violations

# Example usage
if __name__ == '__main__':
    sample_code = """
    api_key = '1234567890abcdef'
    password: 'mypassword1234'
    token = 'tokenvalue12345'
    """
    scanner = SecretScanner()
    results = scanner.scan_code(sample_code)
    if results:
        for msg in results:
            print(msg)
    else:
        print("No hardcoded secrets detected.")
