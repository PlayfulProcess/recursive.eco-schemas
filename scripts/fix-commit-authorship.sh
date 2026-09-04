#!/usr/bin/env bash
# fix-commit-authorship.sh
#
# Rewrites all commits in this repository that used the generic
# "noreply@users.github.com" email (which GitHub maps to anderaiprosicks)
# to the correct PlayfulProcess GitHub noreply address.
#
# Safe to run in GitHub Codespaces — no local install required.
#
# Usage:
#   bash scripts/fix-commit-authorship.sh
#
# After the script succeeds you must force-push the rewritten branch:
#   git push --force-with-lease origin main
#
# Prerequisites:
#   - python3 (pre-installed everywhere)
#   - git-filter-repo  (installed automatically below if missing)

set -euo pipefail

OLD_EMAIL="noreply@users.github.com"
NEW_NAME="PlayfulProcess"
NEW_EMAIL="17236172+PlayfulProcess@users.noreply.github.com"

echo "=== fix-commit-authorship ==="
echo "Replacing: <${OLD_EMAIL}>"
echo "     With: ${NEW_NAME} <${NEW_EMAIL}>"
echo ""

# ── install git-filter-repo if needed ────────────────────────────────────────
if ! command -v git-filter-repo &>/dev/null; then
  echo "Installing git-filter-repo …"
  pip install --quiet git-filter-repo
fi

# ── safety check: must be inside a git repo ──────────────────────────────────
if ! git rev-parse --git-dir &>/dev/null; then
  echo "ERROR: not inside a git repository" >&2
  exit 1
fi

# ── require clean working tree ───────────────────────────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: working tree has uncommitted changes. Commit or stash them first." >&2
  exit 1
fi

# ── create a backup branch ───────────────────────────────────────────────────
BACKUP_BRANCH="backup/pre-author-rewrite-$(date +%Y-%m-%d)"
if git show-ref --verify --quiet "refs/heads/${BACKUP_BRANCH}"; then
  echo "Backup branch '${BACKUP_BRANCH}' already exists — skipping creation."
else
  git branch "${BACKUP_BRANCH}"
  echo "Created backup branch: ${BACKUP_BRANCH}"
fi

# ── build a mailmap file for git-filter-repo ─────────────────────────────────
MAILMAP_FILE="$(mktemp fix-authorship-XXXXXX.mailmap)"
echo "${NEW_NAME} <${NEW_EMAIL}> <${OLD_EMAIL}>" > "${MAILMAP_FILE}"

echo ""
echo "Running git-filter-repo …"

git filter-repo \
  --mailmap "${MAILMAP_FILE}" \
  --force

rm -f "${MAILMAP_FILE}"

echo ""
echo "=== Done! ==="
echo ""
echo "Commits with <${OLD_EMAIL}> have been rewritten to:"
echo "  ${NEW_NAME} <${NEW_EMAIL}>"
echo ""
echo "Verification (last 10 commits):"
git log -n 10 --pretty=format:'  %h | %an <%ae> | %s'
printf '\n'
echo ""
echo "─────────────────────────────────────────────────────"
echo "Next step — force-push to update the remote branch:"
echo ""
echo "  git push --force-with-lease origin main"
echo ""
echo "If you also need to push the backup branch:"
echo "  git push origin ${BACKUP_BRANCH}"
echo "─────────────────────────────────────────────────────"
