---
name: github
description: "GitHub API, auth, PRs, issues, repos, code review, CI/CD — the full lifecycle via gh CLI or git+curl fallback."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, git, prs, issues, auth, repos, code-review, ci, gh-cli]
    related_skills: [codebase-inspection]
---

# GitHub Workflows

Complete toolkit for working with GitHub. Every section shows `gh` first, then `git` + `curl` fallback for machines without the gh CLI.

## Sections

- [Authentication Setup](#1-authentication-setup) — HTTPS tokens, SSH keys, gh login
- [Repository Management](#2-repository-management) — clone, create, fork, configure, releases
- [Issue Management](#3-issue-management) — create, triage, label, assign, comment, close
- [PR Lifecycle](#4-pr-lifecycle) — branch, commit, open, CI, merge
- [Code Review](#5-code-review) — review local changes, review PRs, inline comments
- [Actions & CI](#6-actions--ci) — workflows, runs, logs, reruns
- [Reference Tables](#7-reference-tables) — quick reference per operation

## Quick Auth Detection

Used by all subsections. Run this once at the start of any GitHub operation:

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\\n\\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\\([^@]*\\)@.*|\\1|')
    fi
  fi
fi

# Get owner/repo from git remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [ -n "$REMOTE_URL" ]; then
  OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\\.com[:/]||; s|\\.git$||')
  OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
  REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
fi
```

---

## 1. Authentication Setup

Two paths: `git` (always available, HTTPS tokens or SSH) and `gh` CLI (richer, simpler).

### Git-Only: HTTPS with Personal Access Token

```bash
git config --global credential.helper store
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Create token at https://github.com/settings/tokens with `repo` + `workflow` scopes.

### Git-Only: SSH Key

```bash
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
# Add to https://github.com/settings/keys
ssh -T git@github.com  # verify
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### gh CLI Login

**Headless/VM servers (preferred):**

```bash
# Create a PAT at https://github.com/settings/tokens (repo + read:org + workflow scopes)
echo "<token>" | gh auth login --hostname github.com --with-token
gh auth setup-git
gh auth status             # verify
```

`--with-token` is the only reliable pattern on headless servers. No interactive prompts, no timeouts.

**Required scopes for `--with-token`:** `repo`, `read:org`, **and** `workflow`. Missing any one produces:
- `error validating token: missing required scope 'read:org'` if `read:org` is missing
- `error validating token: HTTP 401: Bad credentials` if other scopes are missing (even if the token passes `curl -H "Authorization: token $TOKEN" https://api.github.com/user`)

The token must be a **classic** PAT (not fine-grained). Use the "Tokens (classic)" tab at https://github.com/settings/tokens — fine-grained tokens are silently rejected by `gh auth login --with-token` even when they have equivalent permissions.

To verify scopes on an existing token:
```bash
curl -s -I -H "Authorization: token $TOKEN" https://api.github.com/ 2>&1 | grep -i x-oauth-scopes
# If the header is empty or absent, the token has no usable scopes
```

If `--with-token` returns `401: Bad credentials` even though the token works with `curl -H "Authorization: token $TOKEN"`, the token may be a fine-grained PAT or may lack required scopes. Generate a new **classic** PAT (not fine-grained) from the Tokens (classic) tab at https://github.com/settings/tokens with **repo**, **read:org**, and **workflow** scopes.

**Desktop/interactive machines:**

```bash
gh auth login --hostname github.com  # opens browser — device code flow
gh auth setup-git
gh auth status
```

### Device code flow on headless servers (only use when a PAT is unavailable):

The device code flow is fragile on headless servers. Each `gh auth login` call generates a unique code that **invalidates every previous code** immediately. If the user enters a stale code, GitHub silently rejects it — no error message on either end. The command also prompts for SSH key upload and Git credential helper config after the device code is entered; these prompts cannot be answered via stdin injection or PTY input.

When you must use it, run in the **background** from the start so it can wait indefinitely:

```bash
gh auth login --hostname github.com --scopes repo,workflow > /tmp/gh-auth-output.txt 2>&1 &
sleep 3
cat /tmp/gh-auth-output.txt
# Present the ONE one-time code to the user
# Tell them: visit https://github.com/login/device and enter EXACTLY this code
```

CRITICAL RULES for device code flow:
1. Generate the code **once**. Do NOT re-run `gh auth login` to "refresh" the code — it destroys the previous one.
2. Present the code clearly: "Go to https://github.com/login/device and enter: `XXXX-XXXX`"
3. Wait patiently. The command exits silently once the user completes the browser flow.
4. After the user says they've done it, verify with `gh auth status` — do not re-run `gh auth login` until you've confirmed the auth failed.
5. If the user enters a code from a previous run (e.g. from a compacted context or an old terminal session), it will fail silently. Generate a fresh code and have them try again.
6. **"All done" / "Done" from the user does not mean success.** The user may say "done" thinking the code from a previous run is valid. Always verify with `gh auth status` before proceeding. The device code flow only completes when the user enters the CURRENT code at the GitHub device activation page.

For fully automated headless setups, always prefer `--with-token` over device code flow.

### SSH key: gh-independent fallback (when gh auth login fails repeatedly)

If `gh auth login` keeps failing (device codes time out, `--with-token` gets 401, config migration errors), you can bypass `gh` entirely by relying on SSH-key-based git operations combined with direct API calls via `curl`:

1. **Add SSH key to GitHub** via the web UI at `https://github.com/settings/keys`:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # Copy output, paste at https://github.com/settings/keys → New SSH key
   ```
2. **Verify SSH works** (independent of gh):
   ```bash
   ssh -T git@github.com
   # "Hi fiaraz! You've successfully authenticated"
   ```
3. **Use SSH remotes for all git operations**:
   ```bash
   git clone git@github.com:owner/repo.git
   git remote set-url origin git@github.com:fiaraz/repo.git
   git push origin main  # works via SSH even without gh
   ```
4. **Use curl for API calls that gh would handle**:
   ```bash
   # Fork via API (requires token with repo scope) — or just fork via web UI
   # Add upstream remote manually
   git remote add upstream git@github.com:owner/repo.git
   gh repo fork --remote=false  # won't work without gh auth
   ```
5. **What you lose without gh auth**:
   - `gh pr create`, `gh issue list`, `gh repo fork` — all gh CLI commands
   - **But**: clone, push, pull, fetch, branch management all work via SSH git
   - Forks can be created through the web UI, then cloned via SSH

This SSH-priority fallback is faster and more reliable than repeatedly cycling through device codes.

### API Token for curl Calls

```bash
export GITHUB_TOKEN="<token>"
curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

---

## 2. Repository Management

### Clone

```bash
# gh
gh repo clone owner/repo
gh repo clone owner/repo -- --depth 1

# git
git clone https://github.com/owner/repo.git
git clone --depth 1 https://github.com/owner/repo.git
git clone -b develop https://github.com/owner/repo.git
```

### Create

```bash
# gh
gh repo create my-project --public --clone
gh repo create my-org/my-project --private --clone

# curl
GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name": "my-project", "private": false, "auto_init": true, "license_template": "mit"}'
```

### Fork

```bash
# gh
gh repo fork owner/repo --clone

# curl + git
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/owner/repo/forks
sleep 2
git clone https://github.com/$GH_USER/repo.git
cd repo && git remote add upstream https://github.com/owner/repo.git

# Sync fork
git fetch upstream && git checkout main && git merge upstream/main && git push origin main
# gh shortcut: gh repo sync $GH_USER/repo
```

### Repository Settings

```bash
gh repo edit --description "..." --visibility public --enable-wiki=false
curl -s -X PATCH -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{"description": "...", "has_wiki": false}'
```

### Releases

```bash
# gh
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v1.0.0 ./dist/binary --title "v1.0.0"

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name": "v1.0.0", "name": "v1.0.0", "draft": false}'
```

### Secrets (GitHub Actions)

gh is dramatically simpler:
```bash
gh secret set API_KEY --body "your-secret-value"
gh secret list
gh secret delete API_KEY
```

### Branch Protection

```bash
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks": {"strict": true, "contexts": ["ci/test"]}, "required_pull_request_reviews": {"required_approving_review_count": 1}}'
```

---

## 3. Issue Management

### View Issues

```bash
# gh
gh issue list
gh issue list --state open --label "bug" --assignee @me
gh issue view 42

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'pull_request' not in i:
        labels = ', '.join(l['name'] for l in i['labels'])
        print(f'#{i[\"number\"]:5}  {i[\"state\"]:6}  {labels:30}  {i[\"title\"]}')"

# Search
gh issue list --search "authentication error"
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/issues?q=error+repo:$OWNER/$REPO"
```

### Create Issues

```bash
# gh
gh issue create --title "Bug title" --body "## Description..." --label "bug,backend" --assignee "username"

# curl
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{"title": "Bug title", "body": "## Description...", "labels": ["bug"]}'
```

### Manage Labels & Assignees

```bash
gh issue edit 42 --add-label "priority:high,bug" --remove-label "needs-triage" --add-assignee username
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels": ["priority:high", "bug"]}'
```

### Comment, Close, Reopen

```bash
gh issue comment 42 --body "Working on a fix."
gh issue close 42 --reason "completed" / "not planned"
gh issue reopen 42
```

### Triage Workflow

1. List untriaged: `gh issue list --label "needs-triage" --state open`
2. Read each issue, categorize, apply labels and priority
3. Assign if owner is clear, comment with triage notes

---

## 4. PR Lifecycle

### Branch & Commit

```bash
git checkout -b feat/description
# Make changes with file tools...
git add <files>
git commit -m "feat: add feature

Longer description wrapping at 72 chars."
```

Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`, `chore:`, `perf:`

### Push & Open PR

```bash
git push -u origin HEAD

# gh
gh pr create --title "feat: title" --body "## Summary\nChanges..." --label enhancement

# curl
BRANCH=$(git branch --show-current)
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{\"title\": \"feat: title\", \"body\": \"## Summary\", \"head\": \"$BRANCH\", \"base\": \"main\"}"
```

### Monitor CI

```bash
gh pr checks
gh pr checks --watch           # poll until complete

# curl polling
SHA=$(git rev-parse HEAD)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status
```

### Auto-Fix CI Failures Loop

1. Check CI → identify failures
2. Read failed logs: `gh run list --branch $(git branch --show-current) --limit 5` / `gh run view <ID> --log-failed`
3. Fix code with file tools → `git add` + `git commit -m "fix: ..."` + `git push`
4. Re-check CI. Repeat up to 3 attempts, then escalate.

### Merge

```bash
gh pr merge --squash --delete-branch
gh pr merge --auto --squash --delete-branch      # auto-merge when checks pass

# curl
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{\"merge_method\": \"squash\", \"commit_title\": \"feat: title (#$PR_NUMBER)\"}"
git push origin --delete $BRANCH
```

---

## 5. Code Review

### Review Local Changes (Pre-Push)

```bash
# Scope
git diff main...HEAD --stat
git log main..HEAD --oneline

# Full diff
git diff main...HEAD

# Per-file
git diff main...HEAD -- src/auth.py

# Common issues scan
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*="
```

### Review a PR on GitHub

```bash
# gh
gh pr view 123
gh pr diff 123 --name-only

# Check out locally for full review
gh pr checkout 123
# OR plain git:
git fetch origin pull/123/head:pr-123 && git checkout pr-123
git diff main...pr-123
```

### Leave Comments

```bash
# General comment
gh pr comment 123 --body "Overall looks good."

# Inline comment
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')
gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST -f body="Suggestion" -f path="src/auth.py" \
  -f commit_id="$HEAD_SHA" -f line=45 -f side="RIGHT"
```

### Submit Formal Review

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
gh pr review 123 --comment --body "Suggestions, nothing blocking."
```

### Review Checklist

- **Correctness**: edge cases, error paths
- **Security**: no hardcoded secrets, input validation, no SQL injection
- **Code Quality**: naming, single responsibility, DRY
- **Testing**: happy path + error cases covered
- **Performance**: no N+1 queries, appropriate caching
- **Doc**: public APIs documented, README updated

### Review Output Template

```text
## Code Review Summary

### Critical
- **src/auth.py:45** — issue and suggestion

### Warnings
- ...

### Suggestions
- ...

### Looks Good
- ...
```

---

## 6. Actions & CI

```bash
# gh
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main

# curl
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10"
curl -s -L -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs -o /tmp/logs.zip
```

---

## 7. Reference Tables

### Action → gh command → curl endpoint

| Action | gh | curl |
|--------|-----|------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create n --public` | `POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `POST /repos/o/r/forks` + clone |
| List issues | `gh issue list` | `GET /repos/o/r/issues` |
| Create issue | `gh issue create ...` | `POST /repos/o/r/issues` |
| View PR | `gh pr view N` | `GET /repos/o/r/pulls/N` |
| Create PR | `gh pr create ...` | `POST /repos/o/r/pulls` |
| Merge PR | `gh pr merge N` | `PUT /repos/o/r/pulls/N/merge` |
| List workflows | `gh workflow list` | `GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `PUT /repos/o/r/actions/secrets/KEY` |
| Create release | `gh release create v1.0` | `POST /repos/o/r/releases` |
| Add label | `gh issue edit N --add-label X` | `POST /repos/o/r/issues/N/labels` |
| PR review | `gh pr review N --approve` | `POST /repos/o/r/pulls/N/reviews` |
| Branch protection | (via settings) | `PUT /repos/o/r/branches/main/protection` |

### Conventions (absorbed from sub-skills)

- **template: bug-report.md**: See `templates/bug-report.md` for bug report template
- **template: feature-request.md**: See `templates/feature-request.md` for feature request template
- **template: pr-body-feature.md**: See `templates/pr-body-feature.md`
- **template: pr-body-bugfix.md**: See `templates/pr-body-bugfix.md`
- **reference: conventional-commits.md**: See `references/conventional-commits.md`
- **reference: ci-troubleshooting.md**: See `references/ci-troubleshooting.md`
- **reference: gh-auth-troubleshooting.md**: See `references/gh-auth-troubleshooting.md` — diagnostic checklist for failed gh CLI authentication, resolution paths (SSH fallback, PAT, device code), and token type comparison table.

## Pitfalls

1. **`gh auth login` device code flow is fragile on headless servers** — Each invocation generates a unique device code that invalidates all previous ones. If the user enters a stale code, it fails silently. Run in the background once and present the single code. Do NOT regenerate to "refresh." PTY mode doesn't help because SSH key and Git credential prompts appear after the code is entered. The only reliable headless pattern is `echo "<token>" | gh auth login --with-token` with a classic Personal Access Token.
2. **Auth method detection** — always check `gh auth status` first. If unavailable, fall back to `GITHUB_TOKEN` from `.env` or `~/.git-credentials`.
3. **Remote URL parsing** — both HTTPS and SSH remote URLs need the same `owner/repo` extraction logic. Test with both formats.
4. **GitHub API returns PRs in /issues** — always filter by `'pull_request' not in i` when listing issues via API.
5. **Empty diff** — check `git status` before reviewing. If `git diff --cached` is empty, try `git diff` then `git diff HEAD~1 HEAD`.
6. **gh not installed** — all operations can be done with `git` + `curl` + `GITHUB_TOKEN`. No sudo needed.
7. **Secrets via API require encryption** — `gh secret set` is dramatically simpler than the curl encryption workflow. Prefer gh for secrets.
8. **`gh run` vs `gh workflow`** — `gh run` is for individual workflow runs (logs, rerun); `gh workflow` is for workflow files (list, enable, disable, dispatch).
9. **`gh auth login --with-token` 401 even when curl works** — If a classic PAT with `repo`, `read:org`, and `workflow` scopes still returns "Bad credentials" in `gh` but works via `curl -H "Authorization: token $TOKEN"`, the gh version may have incompatibility. Fall back to `git` + `curl` API calls, or add the SSH key to GitHub and use SSH remotes.
10. **Tokens without scopes appear to work for basic GET requests** — A token with zero scopes can still read public profile info (`/users/<name>`, `/repos/public-repo`). This creates a false positive ("token works!") that misleads you into thinking scopes are configured. Always verify scopes explicitly with `curl -s -I -H "Authorization: token $TOKEN" https://api.github.com/ 2>&1 | grep -i x-oauth-scopes` — an empty or absent value means no scopes. Even `curl -s -H "Authorization: Bearer $TOKEN" https://api.github.com/user` returning `{"login": "..."}` is NOT proof the token has scopes — that endpoint returns public data for any unauthenticated user. Test with a private-repo endpoint like `https://api.github.com/user/repos` that truly requires the `repo` scope.

11. **`gh` config migration error** — Writing a malformed `~/.config/gh/hosts.yml` (or any format gh 2.94+ doesn't expect) produces: `failed to migrate config: cowardly refusing to continue with multi account migration: couldn't find oauth token for "github.com": The name org.freedesktop.secrets was not provided by any .service files`. Fix: delete the broken config: `rm -rf ~/.config/gh/` then re-run `gh auth login`.

12. **`Bearer` vs `token` auth scheme matters** — The modern GitHub API v3 accepts both `Authorization: token` and `Authorization: Bearer` with classic PATs, but `gh` CLI (v2.94+) uses Bearer internally. If a token returns data with `curl -H "Authorization: token $TOKEN"` but fails with `curl -H "Authorization: Bearer $TOKEN"`, it is likely a classic PAT where the Bearer scheme is being rejected — but this is rare. More often the token simply lacks the required scopes (see pitfall #10). Verify by checking scopes explicitly, not by switching auth schemes.
