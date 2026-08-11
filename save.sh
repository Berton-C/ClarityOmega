#!/bin/bash
# save.sh -- commit and push your work without thinking about git.
#
#   ./save.sh "what you did"
#
# Runs from the repo root. Works on any branch EXCEPT main (protected).
# Shows you what it will commit, asks once, then commits and pushes.
#
# It deliberately does NOT use `git add .`. It shows you the file list and
# you confirm. That one confirmation is the whole safety net: it is how the
# 9 MB log, the 481 tmp dirs, and the credential files stay out.

set -u

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [ -z "${BRANCH:-}" ]; then
  echo "Not inside a git repository. cd to the repo root first."
  exit 1
fi

# ---------------------------------------------------------------- guard: main
if [ "$BRANCH" = "main" ]; then
  echo "You are on main, which is protected. Direct pushes are rejected."
  echo
  echo "Switch to your working branch first:"
  echo "    git checkout v0.2.0-development"
  exit 1
fi

# ------------------------------------------------------------ guard: message
MESSAGE="${1:-}"
if [ -z "$MESSAGE" ]; then
  echo "Say what you did:"
  echo "    ./save.sh \"wired the startup memory protocol\""
  exit 1
fi

# ------------------------------------------------------- guard: anything new?
if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing to save. Working tree is clean on '$BRANCH'."
  exit 0
fi

# ------------------------------------------------------------- show the plan
echo "Branch:  $BRANCH"
echo "Message: $MESSAGE"
echo
echo "CHANGED (already tracked):"
git status --porcelain | grep -vE '^\?\?' | sed 's/^/  /' || true
echo
echo "NEW (not tracked before -- look at this list):"
git status --porcelain | grep -E '^\?\?' | sed 's/^?? /  /' || true
echo

# Loud warning for things that usually should not be committed.
SUSPECT=$(git status --porcelain | sed 's/^...//' | grep -iE '\.(log|zip|tar|gz|db|sqlite3?|bak|pem|key)$|(^|/)\.env$|__pycache__|\.DS_Store' || true)
if [ -n "$SUSPECT" ]; then
  echo "!! These look like they should NOT be committed:"
  echo "$SUSPECT" | sed 's/^/     /'
  echo "!! If you agree, answer n, then add them to .gitignore."
  echo
fi

printf "Commit and push all of the above? [y/N] "
read -r REPLY
case "$REPLY" in
  y|Y|yes|YES) ;;
  *) echo "Stopped. Nothing committed."; exit 0 ;;
esac

# ------------------------------------------------------------ do the thing
git add -A || { echo "git add failed."; exit 1; }
git commit -m "$MESSAGE" || { echo "Commit failed."; exit 1; }

if ! git push origin "$BRANCH"; then
  echo
  echo "Push failed. Your work IS committed locally and is safe."
  echo "Most likely cause: the branch moved on GitHub. Try:"
  echo "    git pull --rebase origin $BRANCH && git push origin $BRANCH"
  exit 1
fi

echo
echo "Saved and backed up to GitHub."
git log --oneline -1
