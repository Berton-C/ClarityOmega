## What this changes

<!-- One or two sentences. What is different after this merge? -->

## Why

<!-- The problem being solved. Link an issue if one exists. -->

## Type of change

- [ ] Bug fix
- [ ] Documentation
- [ ] Cleanup or refactor (no behaviour change)
- [ ] New behaviour (consider whether this belongs in `v0.2.0-development`)

## Verification

<!-- CI checks hygiene only and cannot verify agent behaviour. If this
     changes runtime behaviour, say what you ran and what you observed. -->

- [ ] CI passes
- [ ] For behaviour changes: verified in the live loop (not `run.sh`, which
      starts an empty AtomSpace and is not equivalent)

**What I ran and what I saw:**

<!-- e.g. "docker compose build --no-cache && docker compose up -d, then
     docker logs clarity_omega: the recent-action atoms appear as expected." -->

## Checklist

- [ ] One concern only; unrelated changes are in a separate pull request
- [ ] No em dashes in documents, comments, or commit messages
- [ ] No secrets, credentials, or `.env` content committed
- [ ] Claims about existing behaviour were verified by reading the live source,
      not from memory or documentation
- [ ] If `loop.metta` was touched: the change is a hook calling a named
      function defined elsewhere, not inline logic
- [ ] If a file-modifying script was added: it supports `--apply` and
      `--reverse --apply`, and the reverse path was tested

## Anything the reviewer should know

<!-- Judgment calls, trade-offs, things you were unsure about. Uncertainty
     stated plainly is more useful than false confidence. -->
