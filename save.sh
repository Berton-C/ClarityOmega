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

# Expand to REAL FILE PATHS. `git status --porcelain` collapses an untracked
# directory into one entry, so files inside it are never inspected. That is
# exactly how a 260 MB log slipped through and got rejected by GitHub.
FILES=$(git ls-files --others --exclude-standard; git diff --name-only; git diff --cached --name-only)

# Hard stop: GitHub rejects any file over 100 MB, and the whole push fails.
BIG=""
while IFS= read -r f; do
  [ -f "$f" ] || continue
  sz=$(wc -c < "$f" 2>/dev/null || echo 0)
  if [ "$sz" -gt 52428800 ]; then
    BIG="$BIG  $(du -h "$f" 2>/dev/null | cut -f1)\t$f\n"
  fi
done <<< "$FILES"

if [ -n "$BIG" ]; then
  echo "!! STOPPING: file(s) over 50 MB. GitHub hard-rejects anything over 100 MB"
  echo "!! and the entire push fails, not just that file."
  printf "%b" "$BIG"
  echo "!! Add these to .gitignore, then run this again."
  exit 1
fi

# Warning (not fatal) for things that usually should not be versioned.
SUSPECT=$(printf '%s\n' "$FILES" | grep -iE '\.(log|zip|tar|gz|db|sqlite3?|bak|pem|key)$|(^|/)\.env$|__pycache__|\.DS_Store' || true)
if [ -n "$SUSPECT" ]; then
  echo "!! These look like they should NOT be committed:"
  printf '%s\n' "$SUSPECT" | sed 's/^/     /'
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

PUSH_OUT=$(git push origin "$BRANCH" 2>&1)
PUSH_RC=$?
printf '%s\n' "$PUSH_OUT"

if [ "$PUSH_RC" -ne 0 ]; then
  echo
  echo "Push failed. Your work IS committed locally and is safe."
  echo
  # Read the real error rather than guessing at one cause.
  if printf '%s' "$PUSH_OUT" | grep -q "exceeds GitHub's file size limit\|GH001"; then
    echo "Cause: a file is too large for GitHub (100 MB limit)."
    echo "Fix:   git reset --soft HEAD~1 && git reset"
    echo "       then add the named file to .gitignore and run this again."
  elif printf '%s' "$PUSH_OUT" | grep -q "rule violations\|GH013\|protected branch"; then
    echo "Cause: branch protection. This branch needs a pull request."
    echo "Fix:   you are probably on main. Work on v0.2.0-development instead."
  elif printf '%s' "$PUSH_OUT" | grep -q "workflow.*scope"; then
    echo "Cause: your GitHub token lacks the 'workflow' permission."
    echo "Fix:   enable the 'workflow' scope on your token in GitHub settings."
  elif printf '%s' "$PUSH_OUT" | grep -q "fetch first\|non-fast-forward\|behind"; then
    echo "Cause: the branch moved on GitHub since you last pulled."
    echo "Fix:   git pull --rebase origin $BRANCH && git push origin $BRANCH"
  else
    echo "Read the error above. If it is not obvious, paste it to Claude."
  fi
  exit 1
fi

echo
echo "Saved and backed up to GitHub."
git log --oneline -1
