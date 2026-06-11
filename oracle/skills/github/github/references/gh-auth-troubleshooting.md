# gh CLI Auth Troubleshooting

## Diagnostic Checklist

Run these in order when `gh auth` fails:

1. **SSH key test** — `ssh -T git@github.com`
   - Working: "Hi USERNAME! You've successfully authenticated"
   - Git operations (clone/push/pull) work regardless of gh CLI state
   - If failing: add key at https://github.com/settings/keys

2. **Token scope test** — `curl -s -H "Authorization: token $TOKEN" https://api.github.com/user/repos?per_page=1`
   - Returns list: token has repo scope
   - Returns 401 or error: token has no scopes or is fine-grained

3. **`gh auth status`** — Is gh logged in at all?

4. **Check for broken config** — `ls ~/.config/gh/`
   - If hosts.yml is malformed, delete it: `rm -rf ~/.config/gh/`

## Resolution Paths (in order)

### Path A: SSH only (fastest, best for git operations)
```
1. Add SSH key to GitHub at https://github.com/settings/keys
2. Verify: ssh -T git@github.com
3. Use git@ remotes for all repos
4. For API operations: curl -H "Authorization: token $TOKEN" with classic PAT
```

### Path B: gh auth login --with-token (full API access)
```
1. Generate CLASSIC PAT at https://github.com/settings/tokens
   - Must be "Tokens (classic)" tab, not fine-grained
   - Scopes: repo, read:org, workflow
2. echo "<token>" | gh auth login --hostname github.com --with-token
3. Verify: gh auth status
```

### Path C: Device code flow (last resort)
```
1. Run in background: gh auth login ... > /tmp/out.txt 2>&1 &
2. Sleep 3s, read /tmp/out.txt for one-time code
3. Present code to user ONCE
4. Do NOT regenerate — each new code invalidates the old one
5. After user says "done", verify with gh auth status
```

## Token types at a glance

| Type | Prefix | Works with `gh auth login --with-token` | Works with `curl -H "Authorization: token"` | Shows scopes in X-OAuth-Scopes |
|------|--------|------------------------------------------|---------------------------------------------|-------------------------------|
| Classic PAT | `ghp_` | Yes (with correct scopes) | Yes | Yes |
| Fine-grained PAT | `github_pat_` | No (silent failure / 401) | Yes | No (empty header) |
| Expired/scope-less | `ghp_` | 401 | Only public data | Empty/absent |