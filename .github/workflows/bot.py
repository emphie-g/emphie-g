import requests
import os

TOKEN = os.getenv("GITHUB_TOKEN")

OWNER = "nathanbrooks-eng"
REPO = "issue-bot-test"

CRYPTO_KEYWORDS = [
    "wallet",
    "ledger",
    "token",
    "metamask",
    "swap",
    "bridge"
]

AUTO_REPLY = (
    "Thanks for reporting this issue.\n\n"
    "Could you please confirm whether this issue is still occurring?\n\n"
    "- Maintainers"
)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# 1️⃣ build URL
url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

# 2️⃣ make request
response = requests.get(url, headers=headers)

# 3️⃣ check request worked
if response.status_code != 200:
    print("Error:", response.status_code, response.text)
    exit()

# 4️⃣ NOW parse JSON
issues = response.json()

# 5️⃣ loop issues
for issue in issues:
    if "pull_request" in issue:
        continue

    title = (issue["title"] or "").lower()
    body = (issue["body"] or "").lower()

    if any(k in title or k in body for k in CRYPTO_KEYWORDS):
        issue_number = issue["number"]

        comment_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"

        requests.post(
            comment_url,
            headers=headers,
            json={"body": AUTO_REPLY}
        )

        print(f"Replied to issue #{issue_number}")
