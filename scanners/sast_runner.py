import subprocess
import re

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

def run_semgrep(repo_path: str) -> dict:
    try:
        result = subprocess.run(
            ['semgrep', '--config=auto', '--json', repo_path],
            capture_output=True, text=True, check=True
        )
        return {'repo': repo_path, 'findings': result.stdout}
    except subprocess.CalledProcessError as e:
        print(f"Error running semgrep on {repo_path}: {e}")
        return {'repo': repo_path, 'findings': []}

# Enhanced SQL string concatenation pattern detection
SQL_CONCAT_PATTERN = r'(\w+|\'[^"]*\'|\"[^"]*\")\s*\+\s*(\w+|\'[^"]*\'|\"[^"]*\")'

# Function to check for SQL string concatenation in findings
def check_sql_concatenation(findings: str) -> list:
    return re.findall(SQL_CONCAT_PATTERN, findings)