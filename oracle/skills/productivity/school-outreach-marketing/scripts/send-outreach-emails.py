#!/usr/bin/env python3
"""
Send personalised outreach emails via Gmail API.
Reads credentials from ~/.hermes/google_token.json (needs gmail.send scope).
Personalises the greeting for each contact.
"""

import json, os, base64, time
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = os.path.expanduser('~/.hermes/google_token.json')

with open(TOKEN_PATH) as f:
    tok = json.load(f)

creds = Credentials.from_authorized_user_info(tok)
service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

BODY_TEMPLATE = """Dear {name},

I wanted to introduce myself directly. I am a qualified teacher and examiner with 31 years' experience teaching A Level Chemistry, A Level Biology, GCSE Science, and GCSE Maths.

In 2024, one of my A Level Chemistry students achieved the highest score in the world.

I also serve as an examiner and moderator, which gives me a clear understanding of exactly what examiners look for at each grade boundary — particularly at A*.

My areas of focus:

- Top-grade A Level Chemistry and Biology tuition (A* targeting)
- Oxbridge entrance preparation (including NSAA, ESAT, and interview coaching)
- Transition support for international students entering the UK system
- GCSE/iGCSE Science and Maths for students targeting selective schools

I am writing to offer my services as an external specialist who can support your sixth-form students — particularly those aiming for competitive university places in medicine, dentistry, veterinary science, and the natural sciences.

I charge £45/hour for A Level and £35/hour for GCSE, and I am available online during school hours, evenings, and weekends.

I would be very happy to send you my full CV and exam results data, or to arrange a brief call to discuss how I might support your students.

Best regards

Fiaraz Iqbal
BSc (Hons), PGCE
31 years' teaching experience | A Level examiner and moderator
fiaraziqbal@googlemail.com
07760257814"""

SUBJECT = "Chemistry/Biology specialist — my 2024 student scored the world's highest A Level Chemistry result"

# Each recipient: (first_name, email, description)
recipients = [
    ("Jack", "jack.chapman@westminster.org.uk", "Jack Chapman, Head of Chemistry, Westminster"),
    # ... add your recipients here
]

sent, failed = 0, 0
for first_name, email_addr, desc in recipients:
    try:
        msg = MIMEText(BODY_TEMPLATE.format(name=first_name))
        msg['To'] = email_addr
        msg['Subject'] = SUBJECT
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        result = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        sent += 1
        print(f"  SENT: {desc} -> {email_addr}")
        time.sleep(0.5)
    except Exception as e:
        failed += 1
        print(f"  FAIL: {desc}: {e}")

print(f"\nSent: {sent}  Failed: {failed}")