import subprocess
import os

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

# Make sure the repo_path exists and is a directory

def run_semgrep(repo_path: str) -> dict:
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        return {'error': 'Invalid repository path'}
    
    result = subprocess.run(
        ['semgrep', '--config=auto', '--json', repo_path],
        capture_output=True, text=True
    )
    return {'repo': repo_path, 'findings': result.stdout}