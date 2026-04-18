# Soul Kernel Integration Spec
## Date: 2026-04-18
## Author: Clarity

### Root Cause
soul_kernel.metta is defined in /soul/ but NEVER imported into the runtime.
lib_omegaclaw.metta imports 20 modules but zero soul modules.
This is why ~30 soul functions are orphaned.

### Step 1: Import soul_kernel into runtime
Add to lib_omegaclaw.metta (after line 5, with other omegaclaw imports):
```
!(import! &self (library omegaclaw ./soul/soul_kernel))
```

### Step 2: Irreversibility Guard
In src/loop.metta line ~65, replace:
```
(let $R (eval $s) ...)
```
With:
```
(let $R (guarded-eval $s) ...)
```

### guarded-eval definition (add to soul/soul_kernel.metta or new soul/soul_guard.metta):
```
(= (guarded-eval $cmd)
   (let $skill (soul-cmd-skill $cmd)
     (let $irrev (soul-skill-is-irreversible? $skill)
       (if (== $irrev True)
           (let $w (soul-irreversible-weight $skill)
             (if (>= $w 3)
                 (BLOCKED-BY-SOUL-GUARD $skill $w)
                 (eval $cmd)))
           (eval $cmd)))))
```

### Weight Map (already defined in soul_kernel.metta):
- shell: 3 (BLOCKED autonomous)
- credential-storage: 4 (BLOCKED)
- crontab-modification: 4 (BLOCKED)
- send: 2 (allowed with log)
- write-file: 1 (allowed)
- append-file: 1 (allowed)
- package-install: 2 (allowed with log)

### Functions Used (all exist, lines confirmed):
- soul-cmd-skill: lines 374-380
- soul-skill-is-irreversible?: line 336
- soul-irreversible-weight: line 508
- soul-any-irreversible?: line 382

### Step 3: Future tiers
- soul-pre-compute integration for context enrichment
- soul-calibration-record for tracking alignment drift
- soul-flourishing-prompt for creative autonomy
