"""
Secret Scanner
Detects hardcoded secrets in code using refined regex patterns with entropy checks.
"""

import re
import math

class SecretScanner:
    def __init__(self):
        # Refined regex pattern for hardcoded secrets with exclusions for common non-secret keywords and patterns
        # Added exclusions for environment variable patterns, common placeholders, test code, and inline comments
        # Added negative lookaheads for common file paths, URLs, and config keys to reduce false positives
        # Adjusted length and entropy thresholds based on secret type
        self.hardcode_pattern = re.compile(
            r"""(?ix)                          # Ignore case, verbose mode
            (?<!#.*?)                         # Negative lookbehind for single-line comment
            (?<!/\*.*?)                      # Negative lookbehind for start of block comment
            \b                                # Word boundary
            (?!                              # Negative lookahead for excluded keywords and placeholders
                tokenize|passwordless|notoken|nopassword|password123|passphrase|apikeytest|secret123|dummy|example|changeme|default|sample|testkey|placeholder|dummykey|testsecret|dummyvalue|fakekey|
                your_api_key|your_secret_here|replace_me|<your_api_key>|<your_secret>|<replace_me>|
                oauth_token|csrf_token|session_token|
                config|config_path|filepath|filename|url|endpoint|host|domain|port|path
            )
            (api[-_ ]?key|apikey|token|secret|password|passwd|auth|access[-_ ]?key|
             secret[-_ ]?key|private[-_ ]?key|client[-_ ]?secret|client[-_ ]?key|aws_access_key_id|aws_secret_access_key|azure_key)
            \b                               # Word boundary
            \s*[:=]\s*                       # Assignment operator with optional whitespace
            (['\"])                          # Opening quote (captured)
            ([a-zA-Z0-9_\-\.\+=\/]{20,})  # Secret value with min length 20
            \1                              # Matching closing quote
            (?!.*\*/)                       # Negative lookahead for end of block comment
            """,
            re.VERBOSE | re.IGNORECASE
        )

        # Pattern to exclude environment variable references
        self.env_var_pattern = re.compile(r"\$\{?[A-Za-z0-9_]+\}?")

        # Pattern to detect base64 encoded strings
        self.base64_pattern = re.compile(r"^[A-Za-z0-9+/=\n\r]{20,}$")

        # Pattern to detect comments and docstrings
        self.comment_pattern = re.compile(r"(?m)^\s*#|""""""|'''''')

        # Pattern to detect test code lines
        self.test_code_pattern = re.compile(r"(?i)test|dummy|example|sample|mock|fake")

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

    def _is_in_comment_or_test(self, code: str, match_start: int) -> bool:
        """
        Check if the matched secret is within a comment, docstring, or test code context.
        """
        # Check if line containing match is a comment or docstring
        lines = code[:match_start].splitlines()
        if lines:
            last_line = lines[-1].strip()
            if last_line.startswith('#') or '"""' in last_line or "'''" in last_line:
                return True
        # Check for test code indications in surrounding lines
        surrounding_code = code[max(0, match_start-50):match_start+50].lower()
        if self.test_code_pattern.search(surrounding_code):
            return True
        return False

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
            # Skip if match is in comment, docstring or test code context
            if self._is_in_comment_or_test(code, match.start()):
                continue

            # Extract the secret value inside quotes
            secret_value = re.search(r"['\"]([a-zA-Z0-9_\-\.\+=\/]{20,})['\"]", match.group(0))
            if secret_value:
                secret_str = secret_value.group(1)

                # Exclude if secret looks like environment variable reference
                if self.env_var_pattern.search(secret_str):
                    continue

                entropy = self._calculate_entropy(secret_str)

                # Check for base64 encoded strings and adjust entropy threshold
                is_base64 = bool(self.base64_pattern.match(secret_str))

                # Adjusted entropy threshold: 5.5 for base64 and 4.5 for others
                entropy_threshold = 5.5 if is_base64 else 4.5

                if entropy > entropy_threshold and self._has_special_chars(secret_str):
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
    env_var = "$API_KEY"
    placeholder = '<your_api_key>'
    """
    scanner = SecretScanner()
    results = scanner.scan_code(sample_code)
    if results:
        for msg in results:
            print(msg)
    else:
        print("No hardcoded secrets detected.")
