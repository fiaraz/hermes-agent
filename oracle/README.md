# Oracle Customisations for Hermes Agent

This directory contains all the customisations made to turn the stock
Hermes Agent into **Oracle** -- a direct, no-filler AI assistant
configured for Fiaraz Iqbal's tutoring business and personal automation.

## Contents

### `skills/` -- Custom Hermes Agent skills

| Skill | Purpose |
|-------|---------|
| `communication-style/` | Agent persona rules: no emojis, direct tone, called "Oracle" |
| `github/github/` | GitHub workflow helper (auth troubleshooting, PR flow, repo management) |
| `productivity/daily-education-jobs-scanner/` | Weekly scan of education job boards |
| `productivity/daily-exam-schedule/` | Exam schedule lookup (AQA, Edexcel) |
| `productivity/daily-tutor-lead-scanner/` | Weekly scan of tutor request threads on forums |
| `productivity/oracle-knowledge-base/` | Local knowledge base with SQLite vector search |
| `productivity/school-outreach-marketing/` | School outreach email workflow |

### `scripts/` -- Automation scripts

| Script | Purpose |
|--------|---------|
| `gh-auth.sh` | GitHub CLI auth via device code flow |
| `gh-device.sh` | Device-code based gh login helper |
| `outreach-tracker.py` | Daily Gmail inbox scanner for tutoring email replies |

### `config.yaml` -- Base configuration

Key configuration differences from stock Hermes:

- **Model**: DeepSeek V4 Flash via OpenRouter
- **Approvals**: Fully disabled (`mode: false`) -- no confirmation prompts
- **Delegation**: 3 concurrent child agents, 1 level deep
- **Telegram**: Connected via webhook (reactions off)
- **WhatsApp**: Connected via bridge
- **Memory**: 2200 char agent memory, 1375 char user profile
- **Display**: No compact mode, no streaming markdown strip
- **TTS**: Edge TTS with AriaNeural voice

## Cron Jobs

Two weekly jobs run every Monday at 6am:
1. **Tutor lead scanner** -- searches Mumsnet, The Student Room, Facebook groups
2. **Education jobs scanner** -- scans education job boards

A monthly PAYE reminder fires on the 25th at 9am.
Outreach-tracker runs daily at 10am (silent unless a reply is found).

## How to Apply

```bash
# 1. Copy skills into your ~/.hermes/skills/
cp -r oracle/skills/* ~/.hermes/skills/

# 2. Copy scripts into your ~/.hermes/scripts/
cp -r oracle/scripts/* ~/.hermes/scripts/

# 3. Review and apply config (merge with existing config.yaml)
#    - Replace provider API keys in .env
#    - Update Telegram/WhatsApp channel IDs
```

## Environment Variables (required)

```
OPENROUTER_API_KEY=sk-or-v1-...
TAVILY_API_KEY=tvly-...
OPENAI_API_KEY=sk-...
```

## Platforms Connected

- **Telegram**: DMs and Home channel
- **WhatsApp**: "The Maths and Science Tutor" channel
- **Web**: oracle.shunka.org (nginx + Let's Encrypt)