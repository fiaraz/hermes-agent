---
name: daily-education-jobs-scanner
description: "Weekly search for tutoring, teaching, and education job roles working with Chinese or international students in the UK. Focuses on roles similar to JDC Tutoring experience. Sends results via email. Runs Monday 07:00 Europe time."
version: 1.1.0
author: Fiaraz
license: MIT
tags: [jobs, tutoring, education, chinese-students, international-students, uk, jdc-tutoring]
---

# Weekly Education Jobs Scanner

This skill runs every Monday at 07:00 Europe time (06:00 UTC) and finds current job roles and tutoring opportunities for someone with experience teaching Chinese/international students in both China and the UK.

## What it does
- Searches for paid tutoring, teaching, and education roles focused on Chinese and international students in the UK.
- Prioritizes roles that involve Chinese students who have moved to the UK (or international students from China).
- Looks at job boards, education companies, international schools, and tutoring agencies.
- Returns only relevant, paid opportunities (not parent leads).
- Sends a clean list of roles with links, salary/rate where available, and key details via email.

## Cron schedule (07:00 Europe time, weekly Monday)
```
0 6 * * 1
```

## Prompt to use with cron
```
Load and run the daily-education-jobs-scanner skill now.

Search for current paid job roles and tutoring opportunities working with Chinese or international students in the UK, including:
- International student tutoring roles (Chinese students)
- Education companies that support Chinese families in the UK
- Online or in-person tutoring jobs for Chinese students in the UK
- Roles at companies similar to JDC Tutoring

Use the Tavily API key already configured.

Focus on paid employment or contract tutoring roles only (not parent enquiries).

Return a concise list with:
- Job title / role
- Company or platform
- Location (remote / UK / hybrid)
- Rate or salary if shown
- Direct link
- Short description

Exclude general teaching jobs that do not mention Chinese or international students.
Send the final list as an email to fiaraziqbal@googlemail.com
```

## Memory used
This skill reads the following persistent facts:
- User currently works at JDC Tutoring teaching international (especially Chinese) students in China and the UK.
- User wants paid job roles, not parent lead generation.
- User prefers direct opportunities over large agencies where possible.

## Output style
Clean bullet list, no emojis. Include job title, company, location, rate/salary if available, and direct link. Maximum 10-12 roles per day.