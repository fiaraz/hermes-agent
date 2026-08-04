#!/usr/bin/env python3
"""
Send GCSE Science promotional image to Business Advertising WhatsApp group.
Runs 1 hour after the A-level (August) ad.
"""

import json
import urllib.request
import urllib.error
import sys

BRIDGE_URL = "http://localhost:3000"
IMAGE_PATH = "/home/ubuntu/.hermes/cache/images/gcse-science-ad.jpg"
GROUP_ID = "120363300623448231@g.us"

CAPTION = """🔬 GCSE Science: Secure Grade 7-9s & Top Sixth Form Entry 🎯
Heading into Year 10 or 11? Get expert preparation for Combined & Triple Science.

🚨 Limited Offer: Save £50
Book a 1-on-1 GCSE Science Diagnostic Assessment & Grade Action Plan (normally £50).

💥 FIRST 5 PARENTS GET IT 100% FREE — No obligation to join classes.
⏳ Offer valid until Friday or until all 5 spots are taken.

👥 Small Group Masterclasses
Max 5 Students: High-intensity practice & personalized feedback.

1 Hour / Week: £25 per week (a fraction of 1-on-1 tuition costs).

Format: 📍 In-Person (Bradford & West Yorkshire) | 💻 Online (UK-Wide).

🏆 Why Choose Fiaraz Iqbal?
Active Examiner & Moderator: Direct insider knowledge on how exam boards grade papers and award top marks.

World-Record Result: Taught the student who scored 269/270 in AQA A-Level Chemistry (World's Highest Score).

30+ Years Experience: Former Headteacher."""


def send_media(chat_id, file_path, caption):
    payload = {
        "chatId": chat_id,
        "filePath": file_path,
        "mediaType": "image",
        "caption": caption,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BRIDGE_URL}/send-media",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode())
        return result
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode()}
    except Exception as e:
        return {"error": str(e)}


def main():
    print(f"Sending GCSE Science image to {GROUP_ID}...")
    result = send_media(GROUP_ID, IMAGE_PATH, CAPTION)
    if "messageId" in result:
        print(f"Success: messageId {result['messageId']}")
        sys.exit(0)
    else:
        print(f"Failed: {json.dumps(result, indent=2)}")
        sys.exit(1)


if __name__ == "__main__":
    main()