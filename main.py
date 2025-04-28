import requests
import csv
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = os.getenv('OWNER')
REPO = os.getenv('REPO')

headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

issues_url = f'https://api.github.com/repos/{OWNER}/{REPO}/issues'

params = {
    'state': 'all',
    'per_page': 100
}

def format_date(date_str):
    if not date_str:
        return 'Not Available'
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return date_obj.strftime("%b %d, %Y")


all_issues = []
page = 1

while True:
    print(f'Fetching page {page}...')
    params['page'] = page
    response = requests.get(issues_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Error fetching issues: {response.status_code}')
        break
    issues = response.json()
    if not issues:
        break
    all_issues.extend(issues)
    page += 1

with open('repo_issues.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Issue Number', 'Title', 'Body', 'Assignee', 'State', 'Created At', 'Updated At', 'Labels', 'Author', "Closed At"])
    for issue in all_issues:
        if 'pull_request' in issue:
            continue  # Skip pull requests, only issues
        issue_number = issue.get('number', '')
        title = issue.get('title', '')
        body = issue.get('body', '')
        assignee = issue.get('assignee', {}).get('login') if issue.get('assignee') else 'None'
        state = issue.get('state', '')
        created_at = format_date(issue.get('created_at', ''))
        updated_at = format_date(issue.get('updated_at', ''))
        labels = [label['name'] for label in issue.get('labels', [])]
        author = issue.get('user', {}).get('login', '')
        closed_at = format_date(issue.get('closed_at', ''))
        writer.writerow([issue_number, title, body, assignee, state, created_at, updated_at, ', '.join(labels), author, closed_at])


print('Finished writing issues to repo_issues.csv!')
