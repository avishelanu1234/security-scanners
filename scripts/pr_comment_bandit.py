import json
import os
import sys
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


def main():
    bandit_report_path = 'bandit-report.json'
    if not os.path.exists(bandit_report_path):
        print(f"Bandit report file '{bandit_report_path}' not found.")
        sys.exit(1)

    with open(bandit_report_path, 'r') as f:
        report = json.load(f)

    high_issues = [issue for issue in report.get('results', []) if issue.get('issue_severity') == 'HIGH']

    if not high_issues:
        print("No high severity issues found in Bandit report.")
        return

    comment_lines = ["### Bandit SAST Scan - High Severity Issues Detected:\n"]
    for issue in high_issues:
        filename = issue.get('filename', 'unknown file')
        line_number = issue.get('line_number', 'unknown line')
        issue_text = issue.get('issue_text', '')
        test_name = issue.get('test_name', '')
        comment_lines.append(f"- **{test_name}** in `{filename}` line {line_number}: {issue_text}")

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
