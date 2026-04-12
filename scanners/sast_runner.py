import subprocess
import logging

REPOS = ['payments-core', 'api-gateway', 'auth-service', 'transaction-engine']

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_semgrep(repo_path: str) -> dict:
    # Input validation
    if not isinstance(repo_path, str) or not repo_path:
        logging.error('Invalid repository path provided.')
        return {'repo': repo_path, 'findings': 'Invalid repository path.'}
    
    try:
        logging.info(f'Running semgrep on {repo_path}')
        result = subprocess.run(
            ['semgrep', '--config=auto', '--json', repo_path],
            capture_output=True, text=True, check=True
        )
        logging.info('Semgrep execution completed successfully.')
        return {'repo': repo_path, 'findings': result.stdout}
    except subprocess.CalledProcessError as e:
        logging.error(f'Semgrep failed with return code {e.returncode}: {e.stderr}')
        return {'repo': repo_path, 'findings': e.stderr}
    except Exception as e:
        logging.error(f'An error occurred: {str(e)}')
        return {'repo': repo_path, 'findings': str(e)}