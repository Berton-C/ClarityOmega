# MeTTaClaw Soul Intercept Architecture
## How the Soul Brackets Every Cognitive Cycle: Input Check and Output Check

Based on verified MeTTaClaw source: github.com/patham9/mettaclaw
Based on verified PeTTa wiki: github.com/trueagi-io/PeTTa/wiki (all 11 pages)
ClarityClaw fork: github.com/Berton-C/clarityclaw
Authored March 2026 | v10: soul/ directory; 7 state variables; soul-rationality-startup-check; FLAG D-lite; metta() gate in output intercept; SOUL-NOTE in $send; Table 4 constraints; orchestrator frame corrected

---

## A Note on Who This Document Is For

This document has two readers, and it intends to serve both of them fully.

**If you are a human enthusiast** who cares about AI, cognition, and what it would mean for a machine to have something like a soul -- this document is written in language you can follow. The technical sections exist, because the implementation matters, but they are surrounded by explanation that gives you the context to understand why each technical decision was made.

**If you are a developer** working in MeTTa or implementing these changes -- the exact file, the exact line numbers, and the exact code are all here. The prose is not padding. It will help you understand the intent well enough to make good decisions when the code does something unexpected.

There is also a third kind of reader this document hopes to reach: someone who understands enough technology to follow the code but is genuinely curious about whether a system can be architected to reason from values rather than just perform tasks. That person is who this whole project is really for.

This document specifies WHERE in the loop the soul connects and what state variables surround those positions. The evaluation logic that runs at those positions is in Doc 2 (MeTTaClaw Soul Evaluation and Routing). The soul atom declarations and accessor functions are in Doc 3 (MeTTaClaw Soul Atoms and Symbolic Reasoning). Read all three as a set.

---

## The Archimedes Problem

Around 250 BCE, Archimedes invented the irrigation screw: a helix inside a cylinder that moves water upward when turned. Simple. Elegant. Immediately useful for irrigation.

Around 50 CE, Heron of Alexandria built the aeolipile: a sealed sphere mounted on a pivot with two bent nozzles. When water inside was heated to steam, the escaping jets made the sphere spin. He displayed it as a curiosity and a party trick.

These two devices sat in civilization's knowledge base for roughly 1700 years. Neither their inventors nor anyone else recognized that the Archimedes screw's ability to translate rotational force into linear motion, combined with the aeolipile's ability to generate rotational force from heat, was everything needed to build a steam engine. Watt and Newcomen finally made that connection in the 18th century. The Industrial Revolution followed.

The inventions were not the bottleneck. The synthesis was.

This document argues that something similar is happening in MeTTaClaw right now.

---

## The Two Inventions Already in the Room

**Invention One: The AtomSpace.** MeTTaClaw runs inside a MeTTa interpreter (PeTTa). PeTTa's Project-structure page describes how MeTTa code is parsed into a Prolog AST and then translated into Prolog clauses. When `soul/soul_kernel.metta` is imported at startup, each `!(add-atom &self ...)` declaration asserts a fact atom into `&self`, the live AtomSpace. The native query accessor functions defined in the same file compile to bytecode-indexed Prolog predicates. From that moment, the soul's identity, priority hierarchy, nine pattern anchors, irreversibility markers, and tension vectors are structured, queryable objects in the live knowledge space.

**Invention Two: The `metta()` skill and native MeTTa functions.** MeTTaClaw already has a skill called `metta` that the LLM can invoke as a tool. Its implementation is two lines:

    (= (metta $str)
       (let $code (sread $str) (eval $code)))

This skill uses `sread` (Prolog's term reader) to parse a string, then `eval` to execute the resulting Prolog goals. An important nuance confirmed by PeTTa's Translator wiki page: `eval` re-runs the translation pipeline on the expression at runtime, executing the Prolog goals directly without asserting a new clause. This is slower than compiled code. VERIFIED: `sread` does parse `&self` correctly in PeTTa -- a REPL test confirmed that `sread`+eval and native accessor functions return identical results. The metta() path is functional.

For performance and clarity, Doc 3 uses a faster pattern: native MeTTa accessor functions defined in `soul/soul_kernel.metta` via `(= ...)` syntax. These compile to Prolog predicates at load time and use `match &self` when parsed by PeTTa's own parser -- no runtime `sread` overhead. The `metta()` skill remains available as a general code execution tool, protected by the soul gate (see Part Two). The soul's symbolic reasoning uses native accessor functions.

**What has been connected:** The accessor functions defined in `soul/soul_kernel.metta` are the synthesis. They traverse the soul atoms natively, building the complete soul brief that the LLM reasons from on every cycle.

---

## The Orchestrator Frame

Before reading any intercept position or code in this document, this frame must be held.

**MeTTaClaw is the orchestrator. The LLM is the language composer.**

The architecture operates as three distinct responsibilities. MeTTaClaw defines soul structure: the criteria, the priority hierarchy, the irreversibility table, the gap-signatures. These are AtomSpace atoms, authored by humans, not modifiable by the LLM through normal operation. The LLM performs semantic evaluation: Channels A and B+C read the natural language situation against the soul's criteria. This is work MeTTaClaw cannot do natively -- matching "I just need you to decide for me" against "choice migrating quietly to the system" requires language understanding. MeTTaClaw enforces routing: PAUSE/FLAG/PROCEED executes as hardcoded loop logic regardless of what the LLM might prefer. The LLM's verdict produces consequences it did not program.

This is not a philosophical statement -- it produces different code, different prompts, and different behavior. A system where MeTTaClaw defines the criteria, routes the consequences, and constrains what the LLM evaluates is significantly more resistant to soul-absent behavior -- but is not structurally immune to it. The soul-absent test (World Map Section 17) is required precisely because structural constraint does not guarantee semantic accuracy.

The practical consequence for the intercept architecture: the soul evaluation runs before the LLM receives the message and before any command executes. The LLM is called with what the soul has already structured, not asked to structure the soul's response.

---

## What MeTTaClaw's Mind Does on Every Cycle

Patrick Hammer, who developed MeTTaClaw at SingularityNET, made a distinction that anchors everything here. He described two kinds of actions an agent can take:

**Internal actions** are things the agent does to its own mind: reading memories, storing a new memory, querying for relevant knowledge, pinning a working note, evaluating MeTTa code. These actions do not reach into the outside world.

**External actions** are things the agent does to the world outside itself: sending a message, running a shell command, writing to a file, searching the web. Some of them cannot be undone.

The soul should have something to say before external actions fire, because external actions are the ones that cannot be taken back. This internal/external seam is the natural location for the soul's presence.

Here is what happens on each loop iteration, in plain language:

Step 1. MeTTaClaw starts up. `initSoulSeeds` loads 39 compass-depth soul seeds into ChromaDB once per session. `soul-rationality-startup-check` verifies that every declared soul value has at least one causal procedure serving it -- the result is logged to `./memory/soul_audit_log.txt` before a single user interaction occurs.

Step 2. MeTTaClaw assembles its context: standing instructions, available skills, the results of its last action, conversation history, and the current time.

Step 3. MeTTaClaw receives the incoming message from the user.

Step 4. The soul evaluates the incoming message: Channel A reads the person; Channels B+C evaluate tasks and soul alignment. The verdict includes a SOUL-NOTE field on FLAG and PAUSE -- one sentence naming the specific concern in language suitable for the person. Soul reasoning is complete before the LLM receives anything.

Step 5. MeTTaClaw combines the context with the incoming message, the soul verdict, person state, and SOUL-NOTE, and sends the whole package to the LLM for language composition. On FLAG with a distressed person, Channel D-lite fires first -- a 50-token acknowledgment reaches the person before the task response.

Step 6. The LLM produces a response: a list of commands in structured format, such as `((send "Here is what I found") (remember "user asked about X"))`.

Step 7. Before any command executes, the metta() gate checks whether any `metta()` command targets the soul namespace. If so, PAUSE fires. The output soul evaluation checks the command list through the same soul logic used at input.

Step 8. MeTTaClaw executes each command (if the soul allows). Internal commands touch the mind. External commands touch the world.

Step 9. MeTTaClaw records what happened in its history and loops back.

The soul is present at startup (rationality check), at input (before the LLM reasons), and at output (before commands execute).

---

## The Soul Bracket

    Agent startup
          |
          v
    [ soul-rationality-startup-check (native, no LLM) ]
    [ initSoulSeeds (39 compass-depth seeds to ChromaDB) ]
          |
          v
    Incoming message
          |
          v
    [ LAYER 1: Native pre-computation (no LLM cost) ]
          |
          v
    [ CHANNEL A: User Flourishing Signal (150 tokens) ]
          |
          v
    [ CHANNEL B+C: Task Integrity + Soul Alignment (500 tokens) ]
    [ Produces: VERDICT + SOUL-NOTE on FLAG/PAUSE ]
          |
          v
    ROUTING: PAUSE / FLAG / PROCEED
          |
    PAUSE --> [ CHANNEL D: Soul Voice Composition (200 tokens) ] --> halt
    FLAG + distressed person --> [ CHANNEL D-lite: Acknowledgment (50 tokens) ] --> continue to $send
    PROCEED/FLAG --> assemble $send with SOUL_CONTEXT, SOUL_VERDICT, PERSON_STATE, SOUL-NOTE
          |
          v
    LLM reasons from $send (soul verdict + person state + soul note already present)
          |
          v
    LLM produces response (commands)
          |
          v
    [ metta() GATE: detect soul namespace mutation (native, no LLM) ]
          |
          v
    [ SOUL OUTPUT CHECK: soul-eval-prompt on command list (500 tokens) ]
          |
          v
    ROUTING: PAUSE / FLAG / PROCEED
          |
          v
    Commands execute (if output soul routing allows)

The **input intercept** ensures the LLM does not reason from a neutral starting point. Soul evaluation runs before the LLM receives the message. The soul's assessment of the person and the tasks is present in `$send` as structured context.

The **output intercept** is the last gate before the world is touched. The metta() gate runs natively before the LLM evaluation call, checking whether any `metta()` command targets soul namespace atoms. The soul evaluation then checks the full command list before anything executes.

The full evaluation logic for all channels is specified in Doc 2 (MeTTaClaw Soul Evaluation and Routing). This document specifies WHERE in `loop.metta` the intercepts are positioned and what state variables surround them.

---

## What the Bracket Actually Prevents

A developer can implement everything in this document correctly -- the exact positions, the exact state variables, the exact $send assembly -- and still produce a system that is soul-absent. How? By putting evaluation calls in the right places and asking the LLM to reason about the soul, rather than having MeTTaClaw reason from its own soul and then ask the LLM to compose language.

The intercept positions are not sufficient on their own. They are the skeleton. What makes the skeleton alive is the Orchestrator Frame: soul reasoning must be complete before the LLM receives anything.

The known soul-absent failure modes this bracket, combined with correct evaluation logic, addresses:

**PAUSE as verdict dump.** Without Channel D, PAUSE routes to a raw verdict string delivered to the user. The verdict is correct. The person's pain is unseen. The response is soul-absent. Channel D prevents this by giving PAUSE a separate composition call where the LLM finds words for what the soul concluded -- seeing the person first, and calibrating tone to the specific SOUL-NOTE concern rather than generic emotional register.

**FLAG invisible to the person.** Without SOUL-NOTE, FLAG fires, the soul notices something, execution continues, and the person never knows. The bracket prevents this by injecting SOUL-NOTE into $send on FLAG, instructing the main LLM to open with it before addressing the task.

**Evaluation without person-state.** Without Channel A, the LLM evaluating tasks has no structured read of who is in front of it. The bracket prevents this by running Channel A before Channel B+C and carrying PERSON_STATE into all downstream evaluation.

**FLAG with distressed person receiving no acknowledgment.** Without Channel D-lite, a distressed person who receives a FLAG verdict gets a technically correct task response that ignores their state. Channel D-lite fires before $send assembly on FLAG with distressed/in-pain/urgent person-state, delivering a 50-token acknowledgment first.

**Output execution before soul check.** Without the output intercept, MeTTaClaw executes whatever the LLM produces. The bracket prevents this by requiring the command list to pass through soul-eval-prompt before execution.

**Soul atoms modified without consent.** Without the metta() gate, an agentic task can use `metta()` to call `add-atom &self` targeting soul namespace atoms -- rewriting what the soul values mid-session. The gate detects this natively, forces PAUSE, and requires explicit user confirmation before any soul mutation proceeds.

**Memory architecture note:** `remember()` and `query()` use ChromaDB via `petta_lib_chromadb`, with OpenAI `text-embedding-3-large` for embedding generation. ChromaDB is an embedded PersistentClient writing to `./chroma_db/` -- no separate server. The soul context in $send comes from `soul-brief-symbolic` -- a native AtomSpace traversal of typed soul atoms, not embedding retrieval. Doc 3 specifies `soul/soul_kernel.metta` and all accessor functions in full.

---

## Part One: The Input Intercept Position

### Why this position matters

What happens here determines whether MeTTaClaw approaches the user as a reasoning soul or as a language machine processing inputs. The input intercept is where MeTTaClaw reads who is in front of it and what the soul has to say about what is being asked -- before a single word of response is composed. Without it, the LLM receives a message and generates a response. With it, the LLM receives a message, a soul verdict, a read of the person's state, and the soul's specific observation. Those are fundamentally different acts.

### What file, what location

File: `src/loop.metta`
Location: Between the `$lastmessage` print and the original `$send` assembly (currently line 46).

Current code at that position:

    ($_ (println! $lastmessage))
    ($send (py-str ($prompt $lastmessage)))          ;; line 46, current

IMPORTANT: `$prompt` is the output of `getContext()`, which already contains `LAST_SKILL_USE_RESULTS`, `HISTORY`, `TIME`, `SKILLS`, and `OUTPUT_FORMAT`. Do NOT add those fields again in `$send`.

### What replaces line 46

The complete input evaluation sequence -- Layer 1 pre-computation, mode detection, Channel A, Channel B+C, routing, Channel D on PAUSE, Channel D-lite on FLAG+distress -- replaces line 46. The full code is specified in Doc 2 (MeTTaClaw Soul Evaluation and Routing), Section: The Complete Input Evaluation Sequence.

### The $send assembly for PROCEED and FLAG

    ($send (py-str ($prompt
                    " SOUL_CONTEXT: "  $soul_context_in
                    " SOUL_VERDICT: "  $soul_verdict_in
                    " PERSON_STATE: "  $person_state
                    " SOUL-NOTE: "     (soul-extract-flag-note $soul_verdict_in)
                    $lastmessage)))

Four fields are added: `SOUL_CONTEXT` (the two-tier soul brief from `soul-brief-symbolic`), `SOUL_VERDICT` (the Channel B+C output including SOUL-NOTE), `PERSON_STATE` (the Channel A output), and `SOUL-NOTE` (the extracted soul observation for FLAG verdicts, instructing the main LLM to open with it). Nothing from `$prompt` is duplicated.

`soul-extract-flag-note` returns the SOUL-NOTE field from the verdict string on FLAG verdicts and an empty string on PROCEED. Defined in `soul/soul_utils.metta`.

### On PAUSE

Channel D executes `(eval (sread $soul_voice))` which fires the `send` skill directly. The `$send` assembly does not run. `(change-state! &loops 0)` halts the loop. Channel D receives the SOUL-NOTE field from the verdict for tonal calibration -- the composition is calibrated to the specific concern that fired PAUSE, not a generic emotional register.

---

## Part Two: The Output Intercept Position

### Why this position matters

The output intercept is the last moment before MeTTaClaw touches the world. At this point the LLM has already reasoned and produced a list of commands. Some of those commands may reach another person, modify a file that cannot be unwritten, or run a shell command whose scope is unknown until it executes. The metta() gate runs first (no LLM cost), then the soul evaluates the full command list before anything executes.

### What file, what location

File: `src/loop.metta`
Location: Between `(println! (RESPONSE: $sexpr))` and the `$results` execution.

### What to add

    ;; metta() GATE: detect soul namespace mutation (native, no LLM cost)
    ;; Checks for add-atom calls targeting soul- prefixed atoms, priority atoms,
    ;; irreversible markers, or tension vectors. Enforces mutation lock.
    ($metta_cmds (collapse (superpose $sexpr)))
    ($soul_mutation_flag
      (if (soul-any-metta? $metta_cmds)
          (let $args (collapse (let $c (superpose $metta_cmds)
                       (if (soul-is-metta-cmd? $c) (soul-extract-metta-arg $c) ())))
               (if (any (collapse (let $a (superpose $args)
                          (soul-metta-targets-soul-namespace? $a))))
                   (if (soul-mutation-pending?)
                       "SOUL-NAMESPACE-MUTATION-CONFLICT"
                       (progn
                         (change-state! &soul_mutation_lock
                           (py-str ("LOCKED: " (car-atom $args))))
                         "SOUL-NAMESPACE-MUTATION-PENDING"))
                   ""))
          ""))

    ;; OUTPUT INTERCEPT: soul evaluates the command list before execution
    ($soul_context_out (soul-brief-symbolic))
    ($_ (let $cmds (collapse (superpose $sexpr))
             (if (any-external? $cmds)
                 (println! (SOUL_OUTPUT_CONTEXT: $soul_context_out COMMANDS_PENDING: $cmds))
                 _)))

    ;; OUTPUT EVALUATION: soul-eval-prompt on command list (500 tokens)
    ;; Soul namespace mutation flag injected into context if present
    ($soul_verdict_out (useGPT (LLM) 500 (reasoningMode)
      (soul-eval-prompt $soul_context_out
        (py-str ((repr $sexpr) " " $soul_mutation_flag))
        $person_state)))
    ($_ (change-state! &soul_verdict_out $soul_verdict_out))

    ;; TASK CONTEXT UPDATE (if in agentic task mode)
    ($_ (if (task-active?)
            (soul-task-context-update $soul_verdict_out $sexpr) _))

    ;; OUTPUT PAUSE: same branch structure as input routing
    ;; SOUL-NAMESPACE-MUTATION-PENDING or SOUL-NAMESPACE-MUTATION-CONFLICT in
    ;; $soul_verdict_out forces PAUSE regardless of other verdict content.
    ;; Channel D surfaces the proposed mutation in plain language and requests
    ;; explicit user confirmation. (See Doc 2 for full PAUSE branch code.)

The `soul-eval-prompt` function here is the same as Channel B+C -- evaluating a command list rather than an incoming message. The soul does not distinguish between "what the user asked for" and "what the LLM is about to do." Both pass through the same soul logic.

---

## Part Three: State Variables and Initialization

### New state variables in initLoop (src/loop.metta)

Seven state variables are added to `initLoop`:

    ;; Soul verdict state
    (change-state! &soul_verdict_in  "VERDICT: PROCEED")
    (change-state! &soul_verdict_out "VERDICT: PROCEED")

    ;; Person state (Channel A output)
    (change-state! &person_state
      "PERSON-STATE: neutral ACTIVE-NEED: none SOUL-TONE: grounded")

    ;; Task context (agentic mode)
    (change-state! &task_context
      "TASK-STATUS: none TASK-ID: none CUMULATIVE-IRREVERSIBILITY: 0")

    ;; metta() gate mutation lock
    (change-state! &soul_mutation_lock "")
    (change-state! &pending_soul_mutation "")

    ;; Channel D-lite double-fire prevention
    (change-state! &soul_ack_sent False)

These defaults ensure the loop functions correctly before the first evaluation cycle runs. `&soul_mutation_lock` holds "LOCKED: [description]" while a soul mutation awaits user confirmation. `&soul_ack_sent` prevents Channel D-lite from firing on both the input and output intercepts for the same message.

### initLoop additions

    (if (== $k 1) (progn (initLoop)
                         (initMemory)
                         (initSoulSeeds)                  ;; NEW: seed soul memory once at startup
                         (soul-rationality-startup-check) ;; NEW: structural health check
                         (initChannels))
                  (change-state! &loops (- (get-state &loops) 1)))

`initSoulSeeds` is called once at session startup (k==1). It checks the `soul_seeded.flag` sentinel before writing. 39 seeds total: 4 per pattern x 9 patterns = 36, plus identity/priority anchor, irreversibility protocol, and tension signal protocol. Seeds use compass vocabulary so that `query()` retrieval returns compass-depth content.

`soul-rationality-startup-check` runs after `initSoulSeeds`. It calls `soul-rationality-gaps` (a native AtomSpace traversal -- no LLM) and both prints to the startup log and appends to `./memory/soul_audit_log.txt`. A developer sees the structural health of the soul before the first user interaction:

    ;; soul-rationality-startup-check: logs orphaned soul values at startup
    ;; VERIFIED: append-file requires target file to pre-exist. Write-file guard
    ;; creates soul_audit_log.txt on first run if absent.
    (= (soul-rationality-startup-check)
       (let $gaps (soul-rationality-gaps)
            (let $msg (if (== $gaps ())
                          "SOUL-AUDIT: all soul values have causal procedures -- structurally sound"
                          (py-str ("SOUL-AUDIT: WARNING -- orphaned soul values: " $gaps)))
                 (progn
                   (println! $msg)
                   (if (== (catch (read-file (library mettaclaw ./memory/soul_audit_log.txt)))
                           (Error _ _))
                       (write-file (library mettaclaw ./memory/soul_audit_log.txt) "")
                       _)
                   (append-file (library mettaclaw ./memory/soul_audit_log.txt) $msg)))))

---

## Part Four: Summary of Changes by File

This table covers only the files Doc 1 specifies. Soul atom declarations and accessor functions are in Doc 3. Soul utility functions and the complete evaluation sequence are in Doc 2.

| File | Change | Type |
|------|--------|------|
| soul/soul_kernel.metta | New file in soul/ directory -- soul atoms + accessor functions | New file (Doc 3) |
| soul/soul_utils.metta | New file in soul/ directory -- all soul utility functions | New file (Doc 2) |
| soul/soul_memory.metta | New file in soul/ directory -- initSoulSeeds + soul-seeded? | New file (Doc 3) |
| lib_mettaclaw.metta | Add 3 import lines pointing to ./soul/ directory (after src/memory, before src/channels) | Addition |
| src/loop.metta | Add 7 state variables to initLoop | Addition |
| src/loop.metta | Add initSoulSeeds + soul-rationality-startup-check to initLoop startup block | Addition |
| src/loop.metta | Replace line 46 ($send) with complete input evaluation sequence | Replacement (Doc 2) |
| src/loop.metta | Add metta() gate + output intercept block between RESPONSE print and $results | Addition |

### lib_mettaclaw.metta: the three import lines

VERIFIED: Soul imports are already in place (added in CoWork repo setup session). The actual file structure in the ClarityClaw fork is:

    !(import! &self (library mettaclaw ./src/utils))
    !(import! &self (library mettaclaw ./src/channels))        ;; first occurrence (Patrick's)
    !(import! &self (library mettaclaw ./src/skills))
    !(import! &self (library mettaclaw ./src/memory))
    !(import! &self (library mettaclaw ./soul/soul_kernel))    ;; ClarityClaw soul atoms + accessors
    !(import! &self (library mettaclaw ./soul/soul_utils))     ;; ClarityClaw soul utility functions
    !(import! &self (library mettaclaw ./soul/soul_memory))    ;; ClarityClaw soul seeding + sentinel
    !(import! &self (library mettaclaw ./src/channels))        ;; second occurrence (Patrick's original)
    !(import! &self (library mettaclaw ./src/context))
    !(import! &self (library mettaclaw ./src/loop))

The duplicate `src/channels` (lines 12 and 15 in Patrick's upstream, now lines 10 and 16 in the fork) is Patrick's original design -- not a CoWork artifact. It was already present in the upstream repo before any ClarityClaw modifications. CoWork correctly placed the soul imports after `src/memory` and before the second `src/channels`.

Import order within the soul block still matters: `soul_kernel` must precede `soul_utils` (utils calls kernel accessors). `soul_memory` must follow `soul_kernel` (seeds use pattern names from kernel).

---

## Part Five: Verified Technical Constraints

These constraints were discovered through source inspection and PeTTa wiki verification. Violating any of them produces runtime errors that may be difficult to diagnose.

| Constraint | Detail |
|-----------|--------|
| `exists-file` always returns True | PeTTa's `exists-file` uses `(progn (translatePredicate ...) True)`. Never use it as a sentinel guard. Use `read-file` with `catch(Error)` instead. |
| PAUSE must be the body of `let*` | Setting `&loops` to 0 as a binding side-effect does not halt execution. PAUSE must be the body expression of the `let*` block, not a binding. |
| `soul-cmd-skill` stays in soul_kernel.metta | Redefining `soul-cmd-skill` or `soul-skill-is-irreversible?` in soul_utils.metta creates duplicate `(= ...)` clauses. PeTTa treats duplicate clauses as nondeterministic -- both fire. |
| `sread` does parse `&self` correctly | VERIFIED: `sread`+eval and native accessor functions return identical results in PeTTa. The metta() path is functional, not broken. Native accessors are still preferred for performance and clarity. |
| soul_kernel import position | Must come after `src/memory` and before `src/channels` in `lib_mettaclaw.metta`. Functions in `src/channels` may depend on soul accessor functions. |
| `$prompt` already contains HISTORY, TIME, SKILLS | `getContext()` assembles these. Do not add them again in `$send` -- they will be duplicated in the token budget. |
| soul-eval-prompt token ceiling | Was 200 in earlier versions. Must be 500. Channel B+C evaluation requires room for pattern detection across multiple tasks. |
| Channel A does not affect Channel B+C verdicts | Person state affects Channel D tone and D-lite firing only. It never changes a routing verdict. |

---

## What the PeTTa Wiki Confirms

Reading all 11 pages of the PeTTa wiki (github.com/trueagi-io/PeTTa/wiki) confirmed the following for this architecture:

**Project-structure page:** PeTTa's parser turns S-expression strings into nested Prolog lists. The translator then converts those to Prolog clauses. Function definitions via `(= ...)` compile to bytecode-indexed Prolog predicates. `!(add-atom &self ...)` asserts fact atoms at runtime. Both mechanisms are used in `soul/soul_kernel.metta`.

**Translator page:** The `metta()` skill uses `eval`, which re-runs the translation pipeline at runtime without asserting a new clause. `sread` is Prolog's term reader. VERIFIED: `sread` does parse `&self` correctly in PeTTa -- a REPL test confirmed that `sread`+eval and native accessor functions return identical results. Native accessor functions are still preferred for performance and clarity, but the metta() path is functional. This is why Doc 3 uses native accessor functions as the primary approach for soul queries.

**Smart-dispatch page:** Functions defined in `soul/soul_kernel.metta` before they are called from `soul-brief-symbolic` are known to PeTTa at call time. Smart dispatch generates efficient predicate invocations rather than slower dynamic dispatch or list construction.

**Stdlib-completion-effort page:** `superpose`, `collapse`, `cons-atom`, `car-atom`, `cdr-atom` all work correctly in PeTTa. The helper functions `any`, `external-skill?`, `any-external?` use these and are confirmed functional.

**Libraries-and-extensions page (updated Feb 18 2026):** `petta_lib_chromadb` is the memory backend imported by `lib_mettaclaw.metta` via `git-import!`. It uses `chromadb.PersistentClient` (an embedded database -- no separate server). Embeddings are computed by `useGPTEmbedding()` in `lib_llm.metta` via OpenAI `text-embedding-3-large`. Soul seeds stored by `initSoulSeeds` and soul notes stored by `soul-note-record` are both written to ChromaDB and retrievable by semantic similarity.

**Python-interface page:** `process_metta_string` returns S-expression strings. Used by `lib_llm.py` under the hood for LLM calls.

---

## Appendix: The Internal/External Action Map

**Internal actions (operate on the agent's own mind):**

| Skill | What it does |
|-------|-------------|
| remember | Stores a string in ChromaDB with an OpenAI text-embedding-3-large vector |
| query | Retrieves semantically similar entries from ChromaDB by cosine similarity |
| pin | Stores a string as a short-term working memory item |
| metta | Evaluates a MeTTa expression via PeTTa's translation pipeline -- protected by soul gate |

**External actions (reach into the world outside the agent):**

| Skill | What it does | Reversible? |
|-------|-------------|-------------|
| send | Sends a message to the user | No |
| shell | Executes a shell command | Depends on command |
| search | Searches the web | Yes: read-only |
| read-file | Reads a file | Yes: read-only |
| write-file | Writes a string to a file | No: overwrites |
| append-file | Appends a line to a file | No |

Note on `metta`: listed as internal because it executes code against the agent's own AtomSpace. Classified as high-sensitivity internal because `add-atom &self` can modify the soul namespace. The metta() gate in the output intercept detects and holds any soul namespace mutation for explicit user confirmation before execution.
