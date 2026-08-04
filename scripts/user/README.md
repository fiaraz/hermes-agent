# WhatsApp Ad Scripts

Scripts for sending promotional ads to WhatsApp groups via the Hermes WhatsApp bridge.

## Scripts

- `send-ad-business-advertising.py` – August A-level offer to Business Advertising group
- `send-ad-business-network-uk.py` – August A-level offer to Business Network UK group
- `send-west-yorkshire-ad.py` – August A-level offer to West Yorkshire Marketplace group (currently paused)
- `send-gcse-business-advertising.py` – GCSE Science ad to Business Advertising group
- `send-gcse-business-network-uk.py` – GCSE Science ad to Business Network UK group
- `send-gcse-west-yorkshire.py` – GCSE Science ad to West Yorkshire Marketplace group (currently paused)

## Schedule

Configured via Hermes cron jobs:

- **August A-level ad**: Monday/Wednesday/Friday at 20:00 UTC to Business Advertising & Business Network UK
- **GCSE Science ad**: Tuesday/Thursday/Saturday at 20:00 UTC to Business Advertising & Business Network UK

West Yorkshire group ads paused per user request.

## Images

Ads reference cached images:

- August offer: `~/.hermes/cache/images/august-offer-ad.jpg`
- GCSE Science: `~/.hermes/cache/images/gcse-science-ad.jpg`

Ensure these images exist before running scripts.

## Bridge

Scripts POST to `http://localhost:3000/send` with `chatId` and `message` payload.

Cron jobs are set with `no_agent=true` and `script` pointing to these files.