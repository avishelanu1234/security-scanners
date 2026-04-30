import os
import sys
from bs4 import BeautifulSoup
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

def parse_zap_report(report_path):
    with open(report_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    alerts = []
    # Parse the ZAP report HTML to extract alerts with High risk
    for alertitem in soup.find_all('alertitem'):
        riskdesc = alertitem.find('riskdesc')
        if riskdesc and 'High' in riskdesc.text:
            alertname = alertitem.find('alert').text if alertitem.find('alert') else 'Unknown Alert'
            description = alertitem.find('desc').text if alertitem.find('desc') else ''
            url = alertitem.find('uri').text if alertitem.find('uri') else ''
            alerts.append((alertname, description, url))
    return alerts

def main():
    zap_report_path = 'zap-report.html'
    if not os.path.exists(zap_report_path):
        print(f"ZAP report file '{zap_report_path}' not found.")
        sys.exit(1)

    alerts = parse_zap_report(zap_report_path)

    if not alerts:
        print("No high risk alerts found in ZAP report.")
        return

    comment_lines = ["### OWASP ZAP DAST Scan - High Risk Alerts Detected:\n"]
    for alertname, description, url in alerts:
        comment_lines.append(f"- **{alertname}** at {url}\n  Description: {description}")

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
