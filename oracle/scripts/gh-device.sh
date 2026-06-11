#!/bin/bash
OUTFILE=/tmp/gh-device-code.txt
gh auth login --hostname github.com --git-protocol ssh --skip-ssh-key --scopes repo,workflow > "$OUTFILE" 2>&1
echo "EXIT=$?" >> "$OUTFILE"