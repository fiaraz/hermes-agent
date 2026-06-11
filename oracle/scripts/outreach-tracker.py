#!/usr/bin/env python3
"""
Gmail reply tracker for school outreach emails.
Checks for replies to: "Chemistry/Biology specialist — my 2024 student scored..."
Reports which schools have replied.
"""

import json, os, base64, datetime, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser('~/.hermes/google_token.json')
OUTPUT_DIR = os.path.expanduser('~/.hermes/cron/output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load credentials
with open(TOKEN_PATH) as f:
    tok = json.load(f)

creds = Credentials.from_authorized_user_info(tok)
service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

# Search for replies to our outreach
query = 'subject:"world\'s highest A Level Chemistry" OR subject:"Chemistry/Biology specialist"'
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])

# Separate sent vs received
sent_count = 0
reply_count = 0
replies = []

for msg_data in messages:
    msg = service.users().messages().get(userId='me', id=msg_data['id'], format='metadata',
                                         metadataHeaders=['From', 'To', 'Subject', 'Date']).execute()
    headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
    subject = headers.get('Subject', '')
    sender = headers.get('From', '')
    recipient = headers.get('To', '')
    date = headers.get('Date', '')

    if sender == 'Fiaraz Iqbal <fiaraziqbal@googlemail.com>' or recipient == 'fiaraziqbal@googlemail.com':
        # It's from me
        sent_count += 1
    else:
        # It's a reply!
        reply_count += 1
        replies.append({
            'from': sender,
            'subject': subject,
            'date': date,
            'id': msg_data['id']
        })

# Also check for replies that don't have the full subject (just "Re:")
query2 = 'in:inbox subject:"highest A Level Chemistry"'
results2 = service.users().messages().list(userId='me', q=query2).execute()
for msg_data in results2.get('messages', []):
    msg = service.users().messages().get(userId='me', id=msg_data['id'], format='metadata',
                                         metadataHeaders=['From', 'Subject', 'Date']).execute()
    headers = {h['name']: h['value'] for h in msg.get('payload', {}).get('headers', [])}
    sender = headers.get('From', '')
    # Only count if sender is not me
    if 'fiaraziqbal' not in sender.lower():
        subject = headers.get('Subject', '')
        date = headers.get('Date', '')
        # Check if already counted
        if not any(r['id'] == msg_data['id'] for r in replies):
            reply_count += 1
            replies.append({
                'from': sender,
                'subject': subject,
                'date': date,
                'id': msg_data['id']
            })

# Save report
report = {
    'checked_at': datetime.datetime.now().isoformat(),
    'emails_sent': sent_count,
    'replies_received': reply_count,
    'replies': replies
}

report_path = os.path.join(OUTPUT_DIR, 'outreach-tracker-report.json')

# Merge with existing report if any
existing = {'seen_ids': []}
if os.path.exists(report_path):
    with open(report_path) as f:
        existing = json.load(f)

seen_ids = existing.get('seen_ids', [])
new_replies = [r for r in replies if r['id'] not in seen_ids]
report['new_replies'] = new_replies
report['total_unique_replies'] = reply_count
report['seen_ids'] = seen_ids + [r['id'] for r in new_replies]

with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)

# Output for cron delivery — silent when no news
if new_replies:
    print(f"OUTREACH TRACKER — {len(new_replies)} new reply/replies")
    for r in new_replies:
        print(f"")
        print(f"From: {r['from']}")
        print(f"Subject: {r['subject']}")
        print(f"Date: {r['date']}")
        print(f"---")
    print(f"")
    print(f"Total sent: {sent_count} | Total replies to date: {reply_count}")