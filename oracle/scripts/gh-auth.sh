#!/bin/bash
# Run gh auth login, capture output to a file, timeout after 300s
timeout 300 gh auth login --hostname github.com --scopes repo,workflow > /tmp/gh-auth-output.txt 2>&1
echo "EXIT_CODE=$?" >> /tmp/gh-auth-output.txt