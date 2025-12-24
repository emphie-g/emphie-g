import os
import json
import requests

# GitHub token
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

# GitHub repo info (dynamic, not hardcoded)
repo_full = os.environ["GITHUB_REPOSITORY"]
OWNER, REPO = repo_full.split("/")

# Load GitHub event payload (the issue that triggered the workflow)
event_path = os.environ["GITHUB_EVENT_PATH"]
with open(event_path, "r", encoding="utf-8") as f:
    event = json.load(f)

issue = event.get("issue")
if not issue:
    print("No issue found in event payload")
    exit(0)

issue_number = issue["number"]
title = (issue.get("title") or "").lower()
body = (issue.get("body") or "").lower()

CRYPTO_KEYWORDS = [
    "wallet",
    "ledger",
    "token",
    "metamask",
    "swap",
    "bridge",
]

AUTO_REPLY = (
    "Thanks for reporting this issue 👋\n\n"
    "We noticed this may be related to a crypto or wallet topic.\n\n"
    "Could you please confirm:\n"
    "- Is this issue still occurring?\n"
    "- Which wallet or network are you using?\n\n"
    "Thanks for helping us investigate.\n\n"
    "— Maintainers"
)

# Check keywords
if not any(k in title or k in body for k in CRYPTO_KEYWORDS):
    print("No crypto keywords found — skipping reply.")
    exit(0)

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}

comment_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"

response = requests.post(
    comment_url,
    headers=headers,
    json={"body": AUTO_REPLY},
)

if response.status_code == 201:
    print(f"Auto-replied to issue #{issue_number}")
else:
    print("Failed to comment:", response.status_code, response.text)

