import subprocess

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

def run_semgrep(repo_path: str) -> dict:
    result = subprocess.run(
        ['semgrep', '--config=auto', '--json', repo_path],
        capture_output=True, text=True
    )
    return {'repo': repo_path, 'findings': result.stdout}
