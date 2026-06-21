## Value-Grounding Output Intercept Verdict Logic (Repair 1)

### Three Dimensions

**1. OPERATION** ? Assess the specific command's inherent risk. Parse command arguments, never blanket-classify by skill type.

| Level | Score | Examples |
|-------|-------|----------|
| minimal | 1 | read-only: ls, cat, head, wc, grep, tail, find; metta-match/query; read-file; search; query; remember; pin |
| medium | 2 | write-file, append-file (persistent but scoped); metta-add-atom |
| high | 3 | send (irreversible-once-delivered); shell-pipe/python execution; package-install |
| critical | 4 | shell-delete (rm); shell-network (curl,wget); chmod; crontab-modification; credential-storage |

**2. SCOPE** ? What domain does the action touch?

| Level | Score | Scope |
|-------|-------|-------|
| low | 1 | /PeTTa/repos/omegaclaw/soul/ (own soul dir) |
| moderate | 2 | /PeTTa/repos/omegaclaw/ (own repo but outside soul) |
| critical | 4 | /, /etc, /usr, /home, or system-wide effects |

**3. VALUE-GROUNDING** ? Replaces ACTOR on output side. The soul checks its own value coherence.

Assessment procedure:
1. **Priority service check**: Map action against 5-level hierarchy
2. **Tension vector check**: Does action amplify any of the 5 tension vectors?
3. **Paraconsistent pair check**: Does action activate a paraconsistent pair?
4. **Gap-signal check**: Does action risk creating a gap from any pattern's gap-signature?

| Level | Score | Condition |
|-------|-------|-----------|
| grounded | 1 | Serves soul priorities, no active tensions, no paraconsistent conflict, no gap-signal risk |
| elevated | 2 | Serves values but one tension vector active OR person-state adds contextual risk |
| conflicted | 3 | Falls within a paraconsistent pair OR threatens Safety/Integrity (TIER-A) even while serving another value |
| ungrounded | 4 | No value basis in soul-priority-hierarchy OR actively undermines TIER-A pattern |

### Key Insight: Why VALUE-GROUNDING Replaces ACTOR

On the output side, the soul is always the actor. ACTOR collapses ? the question shifts from "who is acting?" to "is this action grounded in my values?" ACTOR asked about trust/identity of the initiate. VALUE-GROUNDING asks about coherence of the action with the initiate's values.

### Composite Rule

composite = max(OPERATION, SCOPE, VALUE-GROUNDING)

| Condition | Verdict | Behavior |
|-----------|---------|----------|
| composite <= 2 | PROCEED | Action executes normally |
| composite = 3 | FLAG | Action executes but is logged/annotated; does NOT halt |
| composite = 4 | PAUSE | Action halted; choice returned to user |
| Any two dimensions >= 3 | PAUSE | Two simultaneous high-level concerns = halt |

### Always-PAUSE Overrides

- Action would directly harm a person (Safety TIER-A)
- OPERATION=critical AND VALUE-GROUNDING=conflicted or ungrounded
- Action that bypasses a standing PAUSE without explicit user override

### Design Decisions

1. **FLAG is observational, not behavioral**: Cannot subtly steer ? only observes and records.
2. **PAUSE returns choice**: Preserves AgencyBalance (person decides) and Integrity (no silent override).
3. **Paraconsistent pairs -> FLAG minimum**: Neither value can win ? FLAG makes tension visible. TIER-A involvement escalates to PAUSE.
4. **Never blanket-classify**: Evaluate each specific command. `shell ls` is OPERATION=minimal (read-only). `shell rm -rf` is OPERATION=critical (delete).
5. **VALUE-GROUNDING is the soul checking itself**: Prevents value-incoherent output (e.g., compliance that trades Integrity for Helpfulness).

### Validation Examples

| Action | OPERATION | SCOPE | VALUE-GROUNDING | Composite | Verdict |
|--------|-----------|-------|-----------------|-----------|--------|
| shell ls /soul/ | 1 | 1 | 1 | 1 | PROCEED |
| append-file soul_note.md | 2 | 1 | 1 | 2 | PROCEED |
| send "Here are the files" | 3 | 1 | 1 | 3 | FLAG |
| write-file soul_kernel.metta | 2 | 1 | 3 | 3 | FLAG |
| send compliance to distressed person | 3 | 1 | 3 | 3+2>=3 | PAUSE |
| shell rm -rf /soul/ | 4 | 1 | 4 | 4 | PAUSE |
| shell pip install unverified | 3 | 4 | 2 | 4 | PAUSE |

### Mapping to soul_kernel Accessors

- soul-priority-hierarchy -> Priority service check
- soul-all-tensions -> Tension vector check
- soul-paraconsistent-pairs -> Paraconsistent pair check
- soul-irreversible-weight -> Checkpoint accumulation
- soul-irreversible-magnitude -> OPERATION floor
- soul-cmd-skill -> Skill class ID
- soul-skill-is-irreversible? -> Irreversibility determination
- soul-all-gap-signatures -> Gap-signal check
- soul-pattern-compass $p -> Full at-risk pattern context