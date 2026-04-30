import os
import sys
import json
import requests

def post_pr_comment(owner, repo, pr_number, comment, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print("Comment posted successfully.")
    else:
        print(f"Failed to post comment: {response.status_code} - {response.text}")

def parse_secrets_baseline(filepath):
    secrets = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                secrets.append(line.strip())
    return secrets

def main():
    baseline_path = '.secrets.baseline'
    if not os.path.exists(baseline_path):
        print(f"Secrets baseline file '{baseline_path}' not found.")
        sys.exit(1)

    secrets = parse_secrets_baseline(baseline_path)

    if not secrets:
        print("No secrets detected in baseline.")
        return

    comment_lines = ["### Secrets Scan - Potential Secrets Detected:\n"]
    for secret in secrets:
        comment_lines.append(f"- {secret}")

    comment = "\n".join(comment_lines)

    # Read environment variables for repo owner, repo name, PR number and token
    owner = os.getenv('GITHUB_REPOSITORY_OWNER')
    repo = os.getenv('GITHUB_REPOSITORY_NAME')
    pr_number = os.getenv('PR_NUMBER')
    token = os.getenv('GITHUB_TOKEN')

    if not all([owner, repo, pr_number, token]):
        print("Missing environment variables for GitHub API access or PR details.")
        sys.exit(1)

    post_pr_comment(owner, repo, int(pr_number), comment, token)

if __name__ == '__main__':
    main()
