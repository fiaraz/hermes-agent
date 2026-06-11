---
name: daily-exam-schedule
description: "Sends a clean, concise daily message listing all GCSE and A-level Chemistry, Biology, Physics and Maths exams scheduled for that day across AQA, Edexcel and OCR (Summer 2026)."
version: 1.3.0
author: Oracle
license: MIT
tags: [exams, timetable, a-level, gcse, chemistry, biology, physics, maths, aqa, edexcel, ocr]
---

# Daily Exam Schedule -- Summer 2026

This skill produces a short daily message (06:00 UTC on weekdays) showing which Chemistry, Biology, Physics and Maths exams are happening that day for AQA, Edexcel and OCR.

## Output rules
- Only list the four subjects: Chemistry, Biology, Physics, Maths
- Show board + qualification + paper + time
- Keep the message short and scannable
- If no exams that day, send a brief "No exams today" message

## Session times
- am = 09:00 start
- pm = 13:30 start
- All sessions follow JCQ common exam slots

## Timetable sources (Summer 2026)
- Primary: embedded hardcoded date table below
- Verification: Tavily web search, **once per week only (Mondays)** -- stick to the embedded table on other days

## Known key dates (Chemistry, Biology, Physics, Maths)

### GCSE (AQA & Edexcel -- JCQ common slots)

#### Maths
- Paper 1 (Non-Calc): 14 May 2026 am (1h30m)
- Paper 2 (Calc): 3 June 2026 am (1h30m)
- Paper 3 (Calc): 10 June 2026 am (1h30m)

#### Biology
- Paper 1: 12 May 2026 pm (1h45m)
- Paper 2: 8 June 2026 am (1h45m)

#### Chemistry
- Paper 1: 18 May 2026 am (1h45m)
- Paper 2: 12 June 2026 am (1h45m)

#### Physics
- Paper 1: 2 June 2026 am (1h45m)
- Paper 2: 15 June 2026 am (1h45m)

#### Combined Science
- Biology 1: 12 May 2026 pm
- Biology 2: 8 June 2026 am
- Chemistry 1: 18 May 2026 am
- Chemistry 2: 12 June 2026 am
- Physics 1: 2 June 2026 am
- Physics 2: 15 June 2026 am

### AQA A-level
- Chemistry Paper 1 (7405/1): 2 June 2026 am
- Chemistry Paper 2 (7405/2): 9 June 2026 am
- Chemistry Paper 3 (7405/3): 15 June 2026 am
- Biology Paper 1 (7402/1): 4 June 2026 pm
- Biology Paper 2 (7402/2): 12 June 2026 am
- Biology Paper 3 (7402/3): 16 June 2026 am
- Physics Paper 1 (7408/1): 21 May 2026 pm
- Physics Paper 2 (7408/2): 11 June 2026 am
- Physics Paper 3 (7408/3): 22 June 2026 am
- Maths Paper 1 (7357/1): 3 June 2026 pm
- Maths Paper 2 (7357/2): 11 June 2026 pm
- Maths Paper 3 (7357/3): 18 June 2026 pm

### Edexcel A-level
- Chemistry Paper 1 (9CH0/01): 2 June 2026 am
- Chemistry Paper 2 (9CH0/02): 9 June 2026 am
- Chemistry Paper 3 (9CH0/03): 15 June 2026 am
- Biology A Paper 1 (9BN0/01): 4 June 2026 pm
- Biology A Paper 2 (9BN0/02): 15 June 2026 am
- Biology A Paper 3 (9BN0/03): 22 June 2026 pm
- Physics Paper 1 (9PH0/01): 23 May 2026 am
- Physics Paper 2 (9PH0/02): 9 June 2026 am
- Physics Paper 3 (9PH0/03): 8 June 2026 am
- Maths Paper 1 (9MA0/01): 3 June 2026 pm
- Maths Paper 2 (9MA0/02): 11 June 2026 pm
- Maths Paper 3 (9MA0/03): 18 June 2026 pm

## Contingency day
Wednesday 24 June 2026 (all day) -- students must remain available.

## Cron schedule
PAUSED. Will resume April 2027.
- Previous: 0 6 * * 1-5 (weekdays at 06:00 UTC)
- Paused 8 June 2026 -- exam season complete
- Resume: April 2027 for Summer 2027 exam series

## Delivery
Telegram (origin).

## Execution rules
1. Confirm today's date with `date`
2. Use the embedded date table above as the primary source
3. Tavily verification: **only on Mondays** -- other days skip web search entirely
4. Send the matched exams for today
5. If no exams match, send "No exams today."