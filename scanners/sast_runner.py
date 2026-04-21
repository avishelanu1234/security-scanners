import subprocess

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

def run_semgrep(repo_path: str) -> dict:
    result = subprocess.run(
        ['semgrep', '--config=auto', '--json', repo_path],
        capture_output=True, text=True
    )
    return {'repo': repo_path, 'findings': result.stdout}

# Enhanced SQL string concatenation regex pattern detection
# Updated to prevent SQL injection vulnerabilities
SQL_CONCAT_PATTERN = r"(\w+)\s*\+\s*(\w+|'.*?')"  # Avoid using + for SQL concatenation

# Additional patterns for SQL injection detection
SQL_INJECTION_PATTERNS = [
    r"(?i)(SELECT|INSERT|UPDATE|DELETE)\s+.*?\s+FROM\s+.*?\s+WHERE\s+.*?\s*=\s*.*?",
    r"(?i)(SELECT|INSERT|UPDATE|DELETE)\s+.*?\s+FROM\s+.*?\s+\+\s*.*?",
    r"(?i)(\w+)\.format\(.*?\)",  # Detects .format usage
    r"(?i)(\w+)\s*\%\s*.*?"  # Detects % formatting
]

# Function to check for SQL string concatenation and injection patterns in findings

def check_sql_patterns(findings: str) -> list:
    import re
    matches = []
    # Check for SQL string concatenation
    matches.extend(re.findall(SQL_CONCAT_PATTERN, findings))
    # Check for SQL injection patterns
    for pattern in SQL_INJECTION_PATTERNS:
        matches.extend(re.findall(pattern, findings))
    return matches
