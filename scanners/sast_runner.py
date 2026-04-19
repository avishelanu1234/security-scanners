import subprocess

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

def run_semgrep(repo_path: str) -> dict:
    result = subprocess.run(
        ['semgrep', '--config=auto', '--json', repo_path],
        capture_output=True, text=True
    )
    return {'repo': repo_path, 'findings': result.stdout}

# Updated SQL string concatenation pattern detection
# Enhanced regex pattern, edge case handling, and logging
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SQL_CONCAT_PATTERN = r"(?:\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b).*?\+.*?"  # Enhanced pattern for SQL string concatenation detection

# Function to check for SQL string concatenation in findings

def check_sql_concatenation(findings: str) -> list:
    import re
    matches = re.findall(SQL_CONCAT_PATTERN, findings)
    if matches:
        logging.info(f'Found SQL string concatenation patterns: {matches}')
    else:
        logging.info('No SQL string concatenation patterns found.')
    return matches