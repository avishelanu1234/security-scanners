import subprocess

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

def run_semgrep(repo_path: str) -> dict:
    result = subprocess.run(
        ['semgrep', '--config=auto', '--json', repo_path],
        capture_output=True, text=True
    )
    return {'repo': repo_path, 'findings': result.stdout}

# Adding SQL string concatenation pattern detection
SQL_CONCAT_PATTERN = "(\w+)\s*\+\s*(\w+)"  # Example pattern for SQL string concatenation detection

# Function to check for SQL string concatenation in findings

def check_sql_concatenation(findings: str) -> list:
    import re
    return re.findall(SQL_CONCAT_PATTERN, findings)