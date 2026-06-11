---
name: daily-tutor-lead-scanner
description: "Weekly search for A-level Chemistry & Biology tutor leads on Mumsnet, The Student Room, Facebook groups, and web. Sends results via Telegram. Runs Monday 07:00 Europe time."
version: 1.1.0
author: Fiaraz
license: MIT
tags: [tutoring, leads, mumsnet, studentroom, facebook, chemistry, biology, a-level]
---

# Weekly A-level Tutor Lead Scanner

This skill runs every Monday at 07:00 Europe time (06:00 UTC) and delivers fresh, high-intent leads for A-level Chemistry and Biology tutoring.

## What it does
- Searches Mumsnet, The Student Room, Facebook groups, and general web for parents/students actively looking for A-level Chemistry or Biology tutors.
- Filters for recent activity only (posted or last replied within the last 4 weeks, or explicitly mentioning ASAP, "this month", "June/July 2026", "next 4 weeks", "urgent", "this summer").
- Returns only direct, actionable leads with links.
- Sends a clean formatted message to the current Telegram chat.
- Avoids agencies and platforms that take large cuts.

## Cron schedule (07:00 Europe time, weekly Monday)
```
0 6 * * 1
```

## Prompt to use with cron
```
Run the daily-tutor-lead-scanner skill now.

Search for recent parent requests for A-level Chemistry and Biology tutors on:
- Mumsnet
- The Student Room
- Facebook groups
- General web (high-intent keywords)

Use the Tavily API key already configured.

Return a concise list of the best current leads with:
- Thread title
- Direct URL
- Short context (when last active or what parent said)

Do not include platform jobs or agency postings.
Deliver the final list in this chat.
```

## Memory used
This skill reads the following persistent facts:
- User only wants direct platforms / parent enquiries (no agencies)
- Current best sources are Mumsnet, The Student Room, and specific Facebook groups

## Output style
Clean bullet list, no emojis, maximum 12 leads.
Focus on quality over quantity.

## Related Skills
- `school-outreach-marketing` — active outreach to schools (Heads of Science, Heads of Sixth Form). This skill is passive (scanning for existing leads); that skill is active (prospecting schools directly). Use both in parallel for maximum coverage.