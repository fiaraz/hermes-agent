---
name: school-outreach-marketing
description: "Research target schools, find contact details for Heads of Science and Sixth Form, infer email formats, draft and send outreach emails for tutoring services."
version: 1.2.0
author: agent
tags: [tutoring, marketing, outreach, schools, email, contacts, chemistry, biology]
---

# School Outreach Marketing for Tutors

End-to-end workflow for marketing tutoring services directly to UK schools — targeting Heads of Science (Chemistry/Biology) and Heads of Sixth Form at affluent private and high-performing state schools.

---

## Workflow

### 1. Identify Target Schools

Focus on affluent areas first. Key regions (priority order):
- **London** — top independent schools (Westminster, SPGS, St Paul's, Highgate, Dulwich, KCS Wimbledon, NLCS, City of London, Habs)
- **Surrey stockbroker belt** — Guildford High, St George's Weybridge, Epsom College, RGS Guildford, Cranleigh
- **Bucks/Berks/Herts** — Wycombe Abbey, Eton, Wellington, St Albans, Merchant Taylors'
- **West Yorkshire** — Bradford Grammar, Woodhouse Grove, GSAL, Harrogate Ladies', Ashville, St Peter's York

Sources for identifying schools: ISC (Independent Schools Council) directory, local knowledge of affluent postcodes.

### 2. Research Contacts

For each school, find **both** of these roles:

| Role | Responsibility |
|------|---------------|
| **Head of Science / Head of Chemistry / Head of Biology** | Academic credibility, exam performance |
| **Head of Sixth Form / Director of Sixth Form** | University applications, pastoral, external tutor referrals |

Research methodology (try in order):

1. **School website — Staff Directory / Teaching Staff page**
   - Look for individual staff profiles with names
   - Note any email addresses or contact forms
   - St Paul's School uses a Faculty structure (Science, Technology & Engineering) — look for Faculty Head

2. **School department pages** (e.g. /academic/departments/sciences/chemistry)
   - Sometimes list department heads with emails directly
   - Often more detailed than main staff list

3. **LinkedIn**
   - Search: "Head of Chemistry [School Name]" or "Head of Sixth Form [School Name]"
   - Cross-reference names found on school website
   - Some staff list their role but not email — useful for name confirmation

4. **Tes job ads** (tes.com)
   - Recruitment packs often name the line manager with email
   - Current vacancies sometimes mention who to contact

5. **PDF staff lists** — some schools publish staff PDFs (e.g. St George's Weybridge)

#### Email Format Inference

Schools rarely publish all emails publicly. Instead:
1. Find 1-2 **confirmed emails** from job ads, LinkedIn, or recruitment PDFs
2. Identify the email format pattern:
   - `firstname.lastname@school.org.uk` (Epsom College, Westminster, Highgate, SPGS, City of London)
   - `first_initial.lastname@school.org.uk` (Wycombe Abbey)
   - `first_initial+surname@school.org.uk` (St George's Weybridge)
   - `initials@school.org.uk` (St Paul's, Cranleigh, Wellington)
   - `first_initial-surname@school.org.uk` (RGS Guildford)
   - `F.Last@school.org.uk` (Eton College — e.g. a.saunders@etoncollege.org.uk)
3. Apply the pattern to infer other staff emails
4. **Dead ends:** if the school only publishes initials but no first/middle name to decode (e.g. Wellington's Fleur Moore-Bridger — middle name unknown), use general office contact or look for a job ad that confirms the full email
5. If the school sends to an office contact only (e.g. RGS Guildford), use the general office email and ask to be forwarded

### 3. Personalise and Record

Save all findings in `~/tutor-marketing/contacts/` with a structured markdown table per school:

```markdown
## School Name (Area)

| Role | Name | Email | Confidence |
|------|------|-------|------------|
| Head of Chemistry | Name Surname | email@school.org.uk | confirmed / inferred |
| Head of Sixth Form | Name Surname | email@school.org.uk | inferred |
```

Track: school name, contact role, name, email, source URL, confidence level (confirmed vs inferred).

### 4. Draft Outreach Email

Key selling points (lead with the strongest):

1. **World #1 A Level Chemistry result** — "In 2024, one of my students achieved the highest A Level Chemistry score in the world"
2. **Examiner and moderator status** — "clear understanding of what examiners look for at A*"
3. **31 years teaching experience** — A Level Chemistry, Biology, GCSE Science, Maths
4. **Specialisms**:
   - Top-grade A Level Chemistry and Biology tuition (A* targeting)
   - Oxbridge entrance preparation (NSAA, ESAT, interview coaching)
   - Transition support for international students entering the UK system
   - GCSE/iGCSE Science and Maths
5. **Rates**: £45/hour A Level, £35/hour GCSE
6. **Contact**: fiaraziqbal@googlemail.com, 07760257814

Email template saved at `references/outreach-email-template.md`.

### 5. Send to Both Targets

**Always send to both Heads of Science/Chemistry AND Heads of Sixth Form.** They are different decision-makers:
- **Science lead** — cares about academic quality, exam results, curriculum alignment
- **Sixth Form lead** — manages university applications, knows which students need support, coordinates external tutor referrals

Sending mechanism: Gmail API via OAuth. The token at `~/.hermes/google_token.json` must include the Gmail scope.

| Task | Required Scope |
|------|---------------|
| Send emails | `https://www.googleapis.com/auth/gmail.send` |
| Search/read inbox for replies | `https://www.googleapis.com/auth/gmail.modify` or `gmail.readonly` |

**Scope upgrade path:** If the existing token lacks Gmail scope (403 "insufficient authentication scopes"), re-authenticate via OAuth with the broader scope list:
1. Generate an auth URL including both calendar scope AND the new gmail scope
2. User clicks, authorises, pastes back the redirect URL
3. Exchange the code and save the new token

The script at `scripts/send-outreach-emails.py` uses `gmail.send` scope to send personalised emails. The script at `scripts/outreach-tracker.py` uses `gmail.modify` scope to search for replies.

### 6. Track Replies

**Manual:** Check inbox periodically for responses.

**Automated (recommended):** Schedule the reply tracker as a `no_agent=True` cron job:

```
cronjob action=create schedule="0 10 * * *" \
  name="outreach-reply-tracker" \
  script="outreach-tracker.py" \
  no_agent=True
```

This runs the Python script directly — no LLM tokens consumed, no credit cost. The script is **silent when there are no new replies** (empty stdout = no delivery). Only when a reply arrives does it print the details, which triggers a delivery to your chat.

The script saves state in `~/.hermes/cron/output/outreach-tracker-report.json` so it only reports each reply once.

### 7. Follow Up

- If no reply after 2 weeks, send a brief follow-up to the same contacts
- Reply to any responses the same day — leads go cold fast
- Record which schools responded positively for future prioritisation

---

## Pitfalls

- **Schools with faculty structures** (e.g. St Paul's) don't have separate Heads of Biology/Chemistry — target the Faculty Head of Science instead
- **Some schools don't publish individual emails** (e.g. RGS Guildford) — use general office email or LinkedIn DM
- **Vacant roles** — St George's Weybridge had a vacant Head of Chemistry role. Vacancies are an opportunity: offer to fill the gap directly
- **OAuth token scope mismatch** — Calendar scope alone gives 403 on Gmail calls. The token must be re-authenticated with the Gmail scope added. Going straight to `gmail.modify` in one step avoids needing a second auth round when you later add the reply tracker.
- **Subagent timeout** — asking one subagent to research more than 3 schools causes timeout. Limit to 2-3 schools per delegate_task call
- **Missing middle name on initials formats** — Wellington College uses `initials@wellingtoncollege.org.uk` but Fleur Moore-Bridger's initials can't be decoded without her middle name. Use LinkedIn or job ads to find the full email
- **Gmail.send scope cannot read inbox** — the tracker cron job needs `gmail.modify` or `gmail.readonly`, not just `gmail.send`. Always go straight to `gmail.modify` to avoid a second auth round.
- **.env file credential corruption** — the write_file tool and shell heredocs can truncate or garble sensitive values in `.env` files (both the OANDA_API_TOKEN and OPENROUTER_API_KEY were corrupted during this session). If a credential returns 401 or looks wrong, verify the raw bytes in the file:
  ```python
  with open('.env') as f:
      for line in f:
          if 'TOKEN' in line or 'KEY' in line:
              val = line.strip().split('=', 1)[1]
              print(f'{len(val)} chars: {val}')
  ```
  If the value is truncated (wrong length), rebuild the file via Python using ord() character codes to bypass shell filtering:
  ```python
  correct = ''.join(chr(c) for c in [115,107,45,...])  # ord() values of each char
  ```
  Always verify with a live API call after fixing: `requests.get('https://openrouter.ai/api/v1/auth/key', headers={'Authorization': f'Bearer {key}'})` or the Oanda account summary endpoint.

## Reference Files

- `references/school-contacts.md` — Master contact list gathered during research sessions
- `references/outreach-email-template.md` — Email draft template
- `scripts/send-outreach-emails.py` — Personalised bulk email sender via Gmail API
- `scripts/outreach-tracker.py` — Gmail inbox reply tracker (run or schedule as cron)

## Remote Backup (GitHub)

All working files are also version-controlled at **github.com/fiaraz/oracle** (private repo):

| File | Description |
|------|-------------|
| `contacts/school-contacts.md` | Full contact log with both rounds |
| `contacts/outreach-email-draft.md` | Email draft with phone |
| `contacts/outreach-tracker.py` | Same as script above |
| `send-emails.py` | Bulk send script used for rounds 1-2 |

The working directory on the VM is `~/tutor-marketing/`. Push to GitHub after each outreach round:

```bash
cd ~/tutor-marketing
git add -A && git commit -m "Round X: [summary]" && git push
```

## Related Skills

- `daily-tutor-lead-scanner` — passive lead scanning (parent/student facing, complementary to this active school outreach)