# https://github.com/CHooverShrimp/Mercurial-changelog-webhook
# Actively pinging the revision page for latest changes
# Use when you can't access the hgrc for some reason
import requests
from bs4 import BeautifulSoup
import time

# Read from /hg/repoName/rev
url = "https://your.repos.com/hg/repo/rev/"

webhook_url = "https://your.webhook.com"

def fetch_html_content(url):
    response = requests.get(url)
    return response.text

# Cheaper to compare the title than the whole thing
def extract_title(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    return title_tag.text.strip() if title_tag else ""

def extract_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    changeset_id = title_tag.text.split(': ')[1].strip()
    repo = title_tag.text.split(': ')[0].strip()
    description = soup.find('div', class_='description').text.strip()
    author = soup.find('td', class_='author').text.strip() 
    return description, changeset_id, author, repo

def send_webhook(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Webhook sent successfully")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to send webhook: {e}")
        print("Response status code:", response.status_code)
        print("Response text:", response.text)

print('Running Webhook')

# Initial fetch
previous_title = extract_title(fetch_html_content(url))

while True:
    # Fetch HTML content
    current_title = extract_title(fetch_html_content(url))
    
    # Check for changes in the title
    if current_title != previous_title:
        print('Change detected, preparing payload')
        description, changeset_id, author = extract_content(fetch_html_content(url))
        
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
        
        # Update previous title
        previous_title = current_title
        
    # Wait for a specified interval before checking again (e.g., every 10 seconds)
    time.sleep(10)
