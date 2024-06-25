# https://github.com/CHooverShrimp/Mercurial-changelog-webhook
# Gets called by hgrc in the repo to deliver latest changes
# put this in the hgrc file in the repo

# [hooks]
# changegroup =/bin/bash -c '. /yourPythonEnvironment/bin/activate && python3 /yourPathToThisFile/passive_webhook.py https://username:password@your.repos.com/hg/repo/rev/ https://your.repos.com/hg/repo/rev/'

# it basically activates your python environment, then activate this file.

import requests
from bs4 import BeautifulSoup
import sys

if len(sys.argv) != 3:
    print("Usage: python3 webhook.py <local_repo_url> <repo_url>")
    sys.exit(1)

# Local url and reported url
url = sys.argv[1]
repoUrl = sys.argv[2]

# Webhook URL
webhook_url = "https://your.webhook.com"

def fetch_html_content(url):
    response = requests.get(url)
    return response.text

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    changeset_id = title_tag.text.split(': ')[1].strip()  # Extract changeset ID from title
    repo = title_tag.text.split(': ')[0].strip()  
    description = soup.find('div', class_='description').text.strip()
    author = soup.find('td', class_='author').text.strip()
    return description, changeset_id, author, repo

def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for non-2xx status codes
        print("Webhook sent successfully")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to send webhook: {e}")
        print("Response status code:", response.status_code)
        print("Response text:", response.text)


description, changeset_id, author, repo = extract_content(fetch_html_content(url))
        
# Prepare payload
webhook_payload = {
    "embeds": [
        {
            "title": f"Changeset: {changeset_id}",
            "description": description,
            "fields": [
                {"name": "Author", "value": author, "inline": True},
                {"name": "Repository", "value": repo, "inline": True},
                {"name": "Link", "value": repoUrl+changeset_id, "inline": False}
            ],
            "color": 0x36a64f
        }
    ]
}

        
# Send the webhook
send_webhook(webhook_url, webhook_payload)
