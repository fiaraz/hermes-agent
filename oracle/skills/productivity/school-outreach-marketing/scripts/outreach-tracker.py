#!/usr/bin/env python3
"""
Gmail reply tracker for school outreach emails.
Checks for replies matching the outreach subject line.
Silent (empty stdout) when no new replies — designed for no_agent=True cron.
"""

import json, os, base64, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser('~/.hermes/google_token.json')
OUTPUT_DIR = os.path.expanduser('~/.hermes/cron/output')

creds = Credentials.from_authorized_user_info(json.load(open(TOKEN_PATH)))
service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

# Search for messages about our outreach
query = 'subject:"world\'s highest A Level Chemistry" OR subject:"Chemistry/Biology specialist"'
messages = (service.users().messages().list(userId='me', q=query).execute().get('messages', []))

sent_count = 0
reply_count = 0
replies = []

for msg_data in messages:
    msg = service.users().messages().get(
        userId='me', id=msg_data['id'], format='metadata',
        metadataHeaders=['From', 'To', 'Subject', 'Date']
    ).execute()
    headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
    sender = headers.get('From', '')
    if 'fiaraziqbal' in sender.lower():
        sent_count += 1
    else:
        reply_count += 1
        replies.append({'from': sender, 'subject': headers.get('Subject', ''),
                        'date': headers.get('Date', ''), 'id': msg_data['id']})

# Also search inbox for any reply
query2 = 'in:inbox subject:"highest A Level Chemistry"'
for msg_data in (service.users().messages().list(userId='me', q=query2).execute()
                  .get('messages', [])):
    if any(r['id'] == msg_data['id'] for r in replies):
        continue
    msg = service.users().messages().get(
        userId='me', id=msg_data['id'], format='metadata',
        metadataHeaders=['From', 'Subject', 'Date']
    ).execute()
    headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
    sender = headers.get('From', '')
    if 'fiaraziqbal' not in sender.lower():
        reply_count += 1
        replies.append({'from': sender, 'subject': headers.get('Subject', ''),
                        'date': headers.get('Date', ''), 'id': msg_data['id']})

# Persist seen IDs to avoid duplicate notifications
report_path = os.path.join(OUTPUT_DIR, 'outreach-tracker-report.json')
existing = {'seen_ids': []}
if os.path.exists(report_path):
    existing = json.load(open(report_path))

seen_ids = existing.get('seen_ids', [])
new_replies = [r for r in replies if r['id'] not in seen_ids]

# Save state
existing['seen_ids'] = seen_ids + [r['id'] for r in new_replies]
os.makedirs(OUTPUT_DIR, exist_ok=True)
json.dump(existing, open(report_path, 'w'))

# Output for cron — silent when no news
if new_replies:
    print(f"OUTREACH TRACKER — {len(new_replies)} new replies")
    for r in new_replies:
        print(f"")
        print(f"From: {r['from']}")
        print(f"Subject: {r['subject']}")
        print(f"Date: {r['date']}")
        print(f"---")
    print(f"")
    print(f"Total sent: {sent_count} | Replies to date: {reply_count}")