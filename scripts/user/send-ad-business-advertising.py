#!/usr/bin/env python3
"""
Send August promotional image to Business Advertising WhatsApp group.
Run via cron with no_agent=True.
"""

import json
import urllib.request
import urllib.error
import sys

BRIDGE_URL = "http://localhost:3000"
IMAGE_PATH = "/home/ubuntu/.hermes/cache/images/august-offer-ad.jpg"
GROUP_ID = "120363300623448231@g.us"

CAPTION = """🚨 Limited August Offer: Save £60 Before Committing!

Before you join masterclasses, every student requires a Diagnostic Assessment & Target Grade Blueprint (normally valued at £60).

💥 SPECIAL OFFER: We are waiving the assessment fee for the first 5 parents who book this week. Get a full 1‑on‑1 diagnostic review 100% FREE — no obligation to continue.

⏳ Offer expires Friday, 15th August or as soon as all 5 free spots are claimed.

👥 Masterclass Details
Group Size: Max 5 Students Per Class for high‑intensity, personalised feedback.
Tuition: £30 per week (a fraction of the cost of standard 1‑on‑1 private tutoring).
💻 Online (UK‑Wide).

🏆 Why Choose Fiaraz Iqbal?
• World‑Record Result: Taught the student who scored 269/270 in AQA A‑Level Chemistry (World's Highest Score, 2024).
• 30+ Years Experience: Former Headteacher & Active AQA Examiner.

Reply NOW to secure your FREE spot!

📲 Message @FiarazIqbal to book."""


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
    print(f"Sending August offer image to {GROUP_ID}...")
    result = send_media(GROUP_ID, IMAGE_PATH, CAPTION)
    if "messageId" in result:
        print(f"Success: messageId {result['messageId']}")
        sys.exit(0)
    else:
        print(f"Failed: {json.dumps(result, indent=2)}")
        sys.exit(1)


if __name__ == "__main__":
    main()