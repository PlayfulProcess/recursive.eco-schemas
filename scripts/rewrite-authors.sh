#!/usr/bin/env bash
# ============================================================
# rewrite-authors.sh
#
# Rewrites ALL commit authors in this repository so every
# commit is attributed to:
#   PlayfulProcess <17236172+PlayfulProcess@users.noreply.github.com>
#
# This uses git-filter-repo to permanently change stored commit
# metadata. The .mailmap file already handles display-level
# normalization (git log, GitHub contributor graph), but
# running THIS script changes the underlying commit hashes.
#
# PREREQUISITES:
#   pip install git-filter-repo
#
# HOW TO USE (run from your local clone of main, not a PR):
#   1. Make a fresh clone to be safe:
#        git clone https://github.com/PlayfulProcess/recursive.eco-schemas.git /tmp/eco-rewrite
#        cd /tmp/eco-rewrite
#   2. Install git-filter-repo:
#        pip install git-filter-repo
#   3. Run this script:
#        bash scripts/rewrite-authors.sh
#   4. Force-push all branches (destructive — rewrites GitHub history):
#        git push --force --all origin
#        git push --force --tags origin
#   5. Tell any collaborators to re-clone (old clones are now invalid).
#
# NOTE: This rewrites ALL branches and ALL tags.
#       You CANNOT undo a force-push without a backup.
# ============================================================

set -euo pipefail

TARGET_NAME="PlayfulProcess"
TARGET_EMAIL="17236172+PlayfulProcess@users.noreply.github.com"

# Write a mailmap for filter-repo (maps ALL known emails to the target)
MAILMAP_FILE=$(mktemp)
cat > "$MAILMAP_FILE" <<EOF
${TARGET_NAME} <${TARGET_EMAIL}> copilot-swe-agent[bot] <198982749+Copilot@users.noreply.github.com>
${TARGET_NAME} <${TARGET_EMAIL}> <REDACTED>
${TARGET_NAME} <${TARGET_EMAIL}> <noreply@users.github.com>
EOF

echo "Rewriting authors using mailmap:"
cat "$MAILMAP_FILE"
echo ""

# --force is needed because the repo has a remote configured
git filter-repo --mailmap "$MAILMAP_FILE" --force

rm -f "$MAILMAP_FILE"

echo ""
echo "✅ History rewritten locally."
echo ""
echo "To push to GitHub:"
echo "  git push --force --all origin"
echo "  git push --force --tags origin"
echo ""
echo "After force-pushing, any existing clones must be re-cloned."
