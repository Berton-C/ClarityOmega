# Git, the short version

Everything you need. Nothing you do not.

---

## The one thing to know

**Your daily work happens on `v0.2.0-development`. It is not protected.
Commit and push to it freely, exactly as you always have.**

`main` is protected and frozen at the v0.1.0 release. You only touch it when
you deliberately want to change the stable release, which will be rare.

---

## Daily: save your work

```bash
./save.sh "what you did"
```

That is it. It shows you what it will commit, warns if something looks like
junk, asks once, then commits and pushes to GitHub.

Answer `n` if the file list contains something that should not be versioned,
then add that thing to `.gitignore` and run it again.

**Run it often.** Every hour of real work, at minimum. The one thing git
cannot protect you from is work that was never committed.

---

## Start of a work session

```bash
git checkout v0.2.0-development && git pull origin v0.2.0-development
```

Only strictly necessary if you work from more than one machine, but it is
harmless and it is a good habit.

---

## When something is wrong

**"I want to throw away everything since my last save."**
```bash
git reset --hard HEAD
```
Destroys uncommitted changes. Anything you saved with `./save.sh` is safe.

**"What have I changed since the last save?"**
```bash
git status --short
```

**"Push failed."**
Your work is committed and safe locally. The branch moved on GitHub:
```bash
git pull --rebase origin v0.2.0-development && git push origin v0.2.0-development
```

**"I am lost."**
```bash
git status -sb | head -1 && git log --oneline -3
```
That tells you which branch you are on and your last three saves.

---

## Rare: getting a fix into `main`

`main` rejects direct pushes. It needs a pull request. Only do this when a fix
genuinely belongs in the stable v0.1.0 release.

```bash
git checkout main && git pull origin main
git checkout -b fix/short-description
```

Make the fix, then:

```bash
./save.sh "fix: what you fixed"
```

Then open a pull request in the browser at:
`https://github.com/Berton-C/ClarityOmega/compare/main...fix/short-description`

Wait for the green check, then Merge. Afterwards, bring the fix into your
working branch too:

```bash
git checkout v0.2.0-development && git merge main && git push origin v0.2.0-development
```

---

## Why `main` is locked

It requires a pull request and a passing CI check, and it refuses force pushes
and deletion. That means the published v0.1.0 cannot be silently changed or
destroyed, by you on a tired evening or by anyone else. The lock is the point.

You can always change or remove the rule yourself at
`Settings → Rules → Rulesets`. Nothing here can lock you out permanently.

---

## What CI checks when you open a pull request

MeTTa parenthesis balance, Python syntax, no committed credentials, and
`.env.example` staying in sync with `docker-compose.yml`.

It does **not** verify that the agent behaves correctly. That still needs the
live loop. A green check means structurally sound, not working.
