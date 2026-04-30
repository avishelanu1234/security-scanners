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

def parse_scanner_report(report_path):
    # TODO: Implement parsing logic for the specific scanner report format
    # This function should return a list of significant issues or findings
    # Example: return [{"title": "Issue title", "file": "filename", "line": 123, "description": "details"}, ...]
    return []

def main():
    report_path = 'scanner-report.json'  # Adjust filename and extension as needed
    if not os.path.exists(report_path):
        print(f"Scanner report file '{report_path}' not found.")
        sys.exit(1)

    findings = parse_scanner_report(report_path)

    if not findings:
        print("No significant issues found in scanner report.")
        return

    comment_lines = ["### Security Scanner Report - Significant Issues Detected:\n"]
    for finding in findings:
        # Customize the comment format based on the fields returned by parse_scanner_report
        comment_lines.append(f"- **{finding.get('title', 'No Title')}** in `{finding.get('file', 'unknown file')}` line {finding.get('line', 'unknown line')}: {finding.get('description', '')}")

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
