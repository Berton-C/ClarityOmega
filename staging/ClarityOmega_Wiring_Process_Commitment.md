# ClarityOmega Wiring Process Commitment

## The Rule

One change at a time. Each change has a hypothesis stated before execution. We verify the hypothesis before moving to the next change. If a change breaks something, we revert it and diagnose before trying again. We build on proven ground -- every change is either a test we can revert or a fix based on something we proved.

## The Pattern for Each Wiring Step

1. **State the hypothesis.** What we expect to happen and what we expect to learn. Written down before we touch anything.

2. **Make one change.** Not two. Not "while we are in there." One file, one modification, one purpose.

3. **Rebuild.** `docker compose build --no-cache mettaclaw` for any file change inside the repo. This is mandatory because Docker caching serves stale code otherwise.

4. **Restart.** `docker compose up -d` to launch with the new build.

5. **Verify baseline.** Confirm the container iterates normally. If iterations stop, the change broke something. Revert immediately and diagnose.

6. **Verify the new thing.** Test that the specific change works as expected. grep for the new function, check the import loaded, confirm the file exists at the expected path.

7. **Document what we learned.** Update the wiring knowledge with proven facts. Note any surprises.

8. **Then next change.** Only after steps 1-7 are complete for the current change.

## What We Do Not Do

- We do not make multiple changes between rebuilds.
- We do not assume a change worked without verifying.
- We do not jump to fixing a problem without understanding it first.
- We do not skip the rebuild step because "it is just a small change."
- We do not modify Patrick's original logic unless we understand why it is the way it is.

## Revert Protocol

If a change breaks the container (iterations stop, crash on boot, APIConnectionError):
1. Identify which change caused the break.
2. Revert that single change.
3. Rebuild and verify iterations resume.
4. Diagnose what went wrong before attempting the change again.
5. Document the failure and what we learned.

## Documentation

Every step produces a one-line entry in the wiring log:
```
Step N: [what we changed] -- RESULT: [what happened] -- LEARNED: [what we now know]
```

This log is the ground truth of the wiring session. If we need to backtrack, it tells us exactly which steps succeeded and which did not.
