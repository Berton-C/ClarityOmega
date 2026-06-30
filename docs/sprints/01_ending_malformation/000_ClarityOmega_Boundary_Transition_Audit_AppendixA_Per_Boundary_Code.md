# ClarityOmega Boundary Transition Audit, Appendix A: Per-Boundary Runtime Code

**Status:** Companion appendix to `000_ClarityOmega_Boundary_Transition_Audit_v2.md`.
Reference object, not narrative. Intended to be dropped in as a new appendix.
**Source:** project knowledge runtime files (the current runtime), plus the three
supplied gate and governance files (`output_verdict.metta`, `corner_gate.metta`,
`soul_governance.py`).
**Read date:** 2026-06-23. Read end to end, not grepped.
**No em-dashes. Code is verbatim from the source read; load-bearing lines only.**

---

## A.0 What this appendix is

Every boundary in the at-a-glance inventory and in Section 4 is described in prose:
a paraphrase of what the crossing does, plus a pointer to the file and function. This
appendix places the actual runtime code beside the boundary it implements, so each
boundary can be checked against the code rather than trusted as a paraphrase.

## A.1 Why it earns its place

A paraphrase can be faithful to the code and false about the system at the same time,
and in prose the two are indistinguishable. This is not hypothetical. The prior v2 said
"HandleError captures `$a`," which was a faithful paraphrase of one source and a false
statement about another; the contradiction cost most of a session to surface because
prose hid it. Code beside the claim collapses that gap. This is Principle 0 (reason from
facts verified now, not from a frame) applied to the audit itself.

## A.2 What it makes possible

The appendix turns the audit from a set of claims into a checkable object. With every
boundary's code in one place:

1. Completeness becomes provable. Grep the assembled code for the crossing primitives
   (`py-call`, `sread`, `eval`, `add-atom`, `match`, `change-state!`, `set-atom!`,
   `write-file`, `receive`, `send`). Every hit is a boundary. The 14 either account for
   all hits or a fifteenth boundary has been found. The inventory stops being
   best-effort and becomes provably exhaustive or provably incomplete with the missing
   crossing named.
2. Forward and backward tracing has visible gaps. A value followed from birth to death
   through the present code shows any unhandled step as a missing line, not a hypothesis.
   The `_newline_` leak is exactly this: encoder and all decoders side by side make the
   uncovered token a blank cell.
3. The canonical-contract pass runs by inspection. All instances of one boundary type
   side by side make the canonical handler computable, not argued: the decoders' token
   coverage, the three skill lists' contents, each helper reinvention against canon.
4. Coupling is verifiable. Producer output and consumer input both present means
   shape-match is checkable (encoder token set vs decoder reversal; writer atom shape vs
   reader `match` pattern; the metta skill's inner `sread` vs the outer parse).
5. Doc-versus-code contradictions surface across every boundary at once, not one
   accidental discovery at a time.
6. It is a drift-proof reference. The fix phase and the SSI build run against stamped
   code, not against line pointers that rot.

## A.3 How to use it

Locus is given as file plus function name, which is stable across rebuilds. Line numbers
are deliberately omitted: they differ between builds and would reintroduce the exact
staleness this appendix exists to remove. To find a boundary's code, read its function
in the named file. The index below is code-free and scannable; the code lives in the
per-boundary sections that follow it.

---

## A.4 At-a-glance index (code-free)

| B | Crossing | Primary file(s) | Key symbols | Note |
|---|----------|-----------------|-------------|------|
| B1 | Human to Substrate (MM inbound) | `mattermost.py`, `channels.metta`, `loop.metta` | `getLastMessage`, `_is_allowed_message`, `receive`, `$msgrcv` | auth gate on `OMEGACLAW_AUTH_SECRET`; drain-on-read; `" | "` concat |
| B2 | Substrate to LLM (prompt outbound) | `helper.py`, `lib_llm_ext.py` | `soul_send_assemble`, provider `.chat` split | verdict collapsed to bare token; no `:-:-:-:` delimiter in assemble |
| B3 | LLM to Substrate (response parse) | `loop.metta`, `helper.py` | `balance_parentheses`, `sanitize_response`, `wrap_if_bare_command`, `sread`, `HandleError` | most divergent; 4+ string handlers on one crossing |
| B4 | Substrate to Substrate (command eval) | `loop.metta` | `eval`, `collapse`, `superpose`, `HandleError` | `(collapse (eval $s))` per command |
| B4a | Nested skill-argument re-parse | `skills.metta` | `metta`, `sread`, `call_with_inference_limit` | inner `sread`; `|-` instructed in `getSkills` |
| B5 | Substrate to/from Python (Janus marshal) | `utils.metta` | `string-safe` | crash-safe marshal boundary; do not touch |
| B6 | Substrate to Human (MM outbound) | `channels.metta`, `mattermost.py`, `helper.py`, `lib_llm_ext.py` | `send`, `send_message`, `balance_parentheses`, `_clean_text` | `_newline_` reversed nowhere |
| B7 | Substrate to ChromaDB / file | `memory.metta`, `skills.metta` | `remember`, `query`, `embed`, `appendToHistory`, `write-file` | no absolute-path enforcement on file writes |
| B8 | Process / container (crash) | `lib_llm_ext.py`, `loop.metta` | `callProvider`, `(catch (sread ...))` | provider returns "" + logs; parse `catch` |
| B9 | Cycle N to N+1 (state) | `loop.metta` | `initLoop`, `change-state!`, `&error` clear | `&error` cleared each cycle; `&self` wiped on rebuild |
| B10 | Substrate to Skill-dispatch | `skills.metta`, `helper.py`, `loop.metta` | `getSkills`, `wrap_if_bare_command` known-skills, `dispatch-skills` | three sources of the skill set |
| B11 | Python to external API (provider leg) | `lib_llm_ext.py`, `loop.metta` | provider registry, `callProvider` | default `Friendli` |
| B12 | Embedding | `lib_llm_ext.py`, `memory.metta` | `useLocalEmbedding`, `initLocalEmbedding` | local `e5-large-v2`, not OpenAI |
| B13 | Verdict / governance | `loop.metta`, `output_verdict.metta`, `corner_gate.metta`, `soul_governance.py` | `compute-output-verdict`, `output-decision`, `apply-corner-gate`, `soul-pause?` | see A.6 reconciliation note |

---

## A.5 The code, per boundary

### B1 Human to Substrate (MM inbound)

`mattermost.py`:
```python
def _set_last(msg):
    with _msg_lock:
        if _last_message == "":
            _last_message = msg
        else:
            _last_message = _last_message + " | " + msg

def getLastMessage():
    with _msg_lock:
        tmp = _last_message
        _last_message = ""
        return tmp

def _is_allowed_message(user_id, msg):
    candidate = _parse_auth_candidate(msg)
    with _auth_lock:
        if not _auth_secret:
            return True
        if candidate == _auth_secret:
            if _authenticated_user_id is None:
                _authenticated_user_id = user_id
            return False
        if _authenticated_user_id is None:
            return False
        return user_id == _authenticated_user_id

# _ws_loop, on a posted event:
#   if _is_allowed_message(user_id, message):
#       name = _get_display_name(user_id)
#       _set_last(f"{name}: {message}")
```

`channels.metta`:
```
(= (receive)
   (if (== (commchannel) irc)
       (py-call (irc.getLastMessage))
       (py-call (mattermost.getLastMessage))))
```

`loop.metta`:
```
($msgrcv (string-safe (repr (receive))))
($msgnew (prog1 (and (> (string_length $msgrcv) 0) (!= $msgrcv (get-state &prevmsg)))
                (if (> (string_length $msgrcv) 0) (change-state! &prevmsg $msgrcv) _)))
($msg (get-state &prevmsg))
```

### B2 Substrate to LLM (prompt outbound)

`helper.py`:
```python
def soul_send_assemble(prompt, soul_context, soul_verdict, person_state, soul_note, lastmessage, idle_directive=""):
    verdict_str = str(soul_verdict)
    if "VERDICT: PAUSE" in verdict_str:   verdict_summary = "VERDICT: PAUSE"
    elif "VERDICT: FLAG" in verdict_str:  verdict_summary = "VERDICT: FLAG"
    elif "VERDICT: PROCEED" in verdict_str: verdict_summary = "VERDICT: PROCEED"
    else:                                  verdict_summary = "VERDICT: PROCEED"
    soul_note_str = str(soul_note)
    note_section = (" SOUL-NOTE: " + soul_note_str) if soul_note_str else ""
    idle_str = str(idle_directive)
    idle_section = (" IDLE_DIRECTIVE: " + idle_str) if idle_str and len(idle_str) > 5 else ""
    return (str(prompt) + idle_section
            + " SOUL_CONTEXT: " + str(soul_context)
            + " SOUL_VERDICT: " + verdict_summary
            + " PERSON_STATE: " + str(person_state)
            + note_section + " " + str(lastmessage))
```
Determination-strip: the full verdict (PATTERNS, TENSION, SOUL-TONE, REASON) is reduced
to one of three bare `VERDICT:` tokens; the note section is present only when `soul_note`
is non-empty, which `soul_extract_flag_note` produces only on FLAG.

Provider split (`lib_llm_ext.py`, GlmProvider.chat):
```python
spl = content.split(":-:-:-:")
sysmsg = spl[0]
usermsg = spl[1] if len(spl) > 1 else ""
```
`soul_send_assemble` emits no `:-:-:-:` delimiter, so the split yields the whole send as
`sysmsg` and an empty `usermsg`.

CONFIDENCE NOTE: `soul_send_assemble` and the provider split are read directly. The loop
call site that binds `$send` (assemble vs the upstream `py-str ($prompt :-:-:-: $lastmessage)`)
was not re-read end to end this pass; confirm at the loop's `$send` line.

### B3 LLM to Substrate (response parse)

`loop.metta`:
```
($respi (if (== (provider) OpenAI)
            (useGPT (LLM) (maxOutputToken) (reasoningMode) $send)
            (py-call (lib_llm_ext.callProvider (provider) $send (maxOutputToken)))))
($resp (py-call (helper.balance_parentheses $respi)))
($response (if (== "(" (first_char $resp)) $resp
               (progn (println! $resp) (repr (REMEMBER:OUTPUT_NOTHING_ELSE_THAN: ((skill arg) ...))))))
($sexpr (catch (sread $response)))
($_ (change-state! &error ()))
($_ (HandleError MULTI_COMMAND_FAILURE_NOTHING_WAS_DONE_PLEASE_CORRECT_PARENTHESES_AND_USE_QUOTES_AND_RETRY $response $sexpr))
```

`HandleError` definition (`loop.metta`), the runtime captures `$a`:
```
(= (HandleError $msg $cmd $sexpr)
   (case $sexpr
     (((Error $a $b) (let $new (append (get-state &error) (($msg $cmd $a)))
                          (progn (change-state! &error $new) ($msg $cmd $a))))
      ($else $sexpr))))
```

`helper.py` string handlers on this crossing:
```python
def sanitize_response(s):
    return s.encode('ascii', errors='replace').decode('ascii')

def wrap_if_bare_command(s):
    # wraps a bare single command iff first token is in known_skills (13 items)
    ...

# balance_parentheses reverses _quote_ only, then balances parens, garbage -> (pin ...)
```

### B4 Substrate to Substrate (command eval)

`loop.metta`:
```
($sexpr_gated (apply-corner-gate $sexpr_verdict))
($results (RESULTS: (collapse (let $s (superpose $sexpr_gated)
            (COMMAND_RETURN: ($s (HandleError SINGLE_COMMAND_FORMAT_ERROR_NOTHING_WAS_DONE_PLEASE_FIX_AND_RETRY
              $s (catch (let $R (collapse (eval $s)) (py-call (helper.normalize_string $R)))))))))))
($results_final (gate-aware-results $results))
```
`(collapse (eval $s))` materializes each command's nondet result stream before binding
(the post-collapse-eval fix). Per-command `HandleError` carries the single-command format
error.

### B4a Nested skill-argument re-parse

`skills.metta`:
```
(= (metta $str)
   (let $code (sread $str)
        (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x))))
```
The outer parse produces a `(metta "<string>")` command; the `metta` skill `sread`s its
string argument again, a second parse with no inner `catch`. `getSkills` instructs the
`|-` operator and shows the non-ASCII multiplication sign in its NAL examples.

### B5 Substrate to/from Python (Janus marshal)

`utils.metta`:
```
(= (string-replace $str $a $b)
   (atomic_list_concat (split_string $str $a "") $b))

(= (string-safe $str)
   (string-replace (string-replace (string-replace $str "\"\"" "_quote_") "\n" "_newline_") "'" "_apostrophe_"))
```
This is the crash-safe marshal boundary. `(string-safe (repr $results))` keeps
stringification pure-MeTTa so Janus never marshals a possibly-unbound value across
`py-call` (commits a318abc / 69c73fc). Do not move stringification across the py-call
boundary and do not "fix" the decode asymmetry here.

### B6 Substrate to Human (MM outbound)

`channels.metta`:
```
!(change-state! &lastsend "")
(= (send $msg)
   (if (!= $msg (get-state &lastsend))
       (progn (change-state! &lastsend $msg)
              (let $safemsg (string-replace $msg "\n" "\\n")
                   (if (== (commchannel) irc)
                       (let $temp (cut) (py-call (irc.send_message $safemsg)))
                       (let $temp (cut) (py-call (mattermost.send_message $safemsg)))))) _))
```

`mattermost.py`:
```python
def send_message(text):
    text = text.replace("\\n", "\n")
    if not _connected:
        return
    requests.post(f"{MM_URL}/api/v4/posts", headers=_headers,
                  json={"channel_id": CHANNEL_ID, "message": text})
```

Decode sites that exist (`helper.balance_parentheses` reverses `_quote_`;
`lib_llm_ext._clean_text` reverses `_quote_` and `_apostrophe_`):
```python
# lib_llm_ext.AIProvider._clean_text
return text.replace("_quote_", '"').replace("_apostrophe_", "'")
```
No site reverses `_newline_`; `_apostrophe_` is reversed only on the provider
(`_clean_text`) path. `string-safe` (B5) is the encoder; this is the union of decoders.

### B7 Substrate to ChromaDB / file

`memory.metta`:
```
(= (embed $str)
   (if (== (embeddingprovider) Local)
       (py-call (lib_llm_ext.useLocalEmbedding (string-safe $str)))
       (useGPTEmbedding (string-safe $str))))

(= (remember $str) (py-call (lib_chromadb.remember $str (embed $str) (get_time_as_string))))
(= (query $str)    (py-call (lib_chromadb.query (embed $str) (maxRecallItems))))
(= (episodes $time) (py-call (helper.around_time $time (maxEpisodeRecallLines))))

(= (getHistory)
   (let $ret (read-file (library omegaclaw ./memory/history.metta)) (last_chars $ret (maxHistory))))
(= (appendToHistory $addition)
   (append-file (library omegaclaw ./memory/history.metta) (swrite $addition)))
(= (addToHistory $lastmessage $response $sexpr $msgnew)
   (if $msgnew
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))))
```

`skills.metta` file writes (no absolute-path enforcement, CWD-relative):
```
(= (write-file $file $str)
   (progn (translatePredicate (open $file write $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (close $Out)) True))
(= (append-file $file $str)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (open $file append $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (nl $Out)),
          (translatePredicate (close $Out)) True))
```
CONFIDENCE NOTE: `lib_chromadb.remember` / `.query` Python bodies are upstream and were
not read this pass.

### B8 Process / container (crash)

`lib_llm_ext.py`:
```python
def callProvider(provider_name, content, max_tokens=6000):
    provider = _get_provider(provider_name)
    if provider is None:
        print(f"[lib_llm_ext.callProvider] Unknown provider: {provider_name}")
        return ""
    if not provider.is_available:
        print(f"[lib_llm_ext.callProvider] {provider_name} not configured (missing {provider._var_name})")
        return ""
    return provider.chat(model=provider._model_name, content=content, max_tokens=max_tokens)
```
`loop.metta` parse guard: `($sexpr (catch (sread $response)))`. Provider `.chat` bodies
wrap the API call in try/except returning "".

### B9 Cycle N to N+1 (state)

`loop.metta` (`initLoop`, the seeded cross-cycle state):
```
(change-state! &prevmsg "")
(change-state! &lastresults "")
(change-state! &soul_verdict_in  "VERDICT: PROCEED")
(change-state! &soul_verdict_out "VERDICT: PROCEED")
(change-state! &person_state "PERSON-STATE: neutral ACTIVE-NEED: none SOUL-TONE: grounded")
(change-state! &soul_mutation_lock unlocked)
(change-state! &pending_soul_mutation "")
(change-state! &last_pause_note "")
(change-state! &last_gate_fingerprint "")
(change-state! &authorized_approvers "berton_c")
(change-state! &last_human_time 0)
(change-state! &engaged_idle_count 0)
(change-state! &loops (maxNewInputLoops))
(do-bootstrap-task-state!)
```
Per cycle: `($_ (change-state! &error ()))` clears the error each cycle before parse;
`&lastresults` is overwritten post-execution; `history.metta` and ChromaDB persist across
rebuild; AtomSpace `&self` is wiped on rebuild.

### B10 Substrate to Skill-dispatch (three sources; registry coupling closed)

Loaded per manifest `lib_clarity_reasoning.metta` line 107 (`capability_registry`) and line
108 (`capabilities/skill_discovery`). The Path C draft
(`capability_registry_path_c_draft.metta`) and the harness are imported nowhere; they are
scaffolding, not runtime.

READER and getContext hook (`skill_discovery.metta`, loaded, full):
```
(eligible-lifecycle active)

(registered-capability
   schema: (skill-request cycle: $k)
   handler: skill-discovery
   priority: 100
   lifecycle: active
   metadata: ())

(= (skill-discovery $request)
   (let* (($capabilities (collapse (match &self
                                          (registered-capability schema: $s handler: $h
                                            priority: $p lifecycle: active metadata: $m)
                                          ($s $h $p $m))))
          ($formatted (format-skill-set $capabilities)))
         (skill-set skills: $formatted)))

(= (format-skill-set $capabilities) (getSkills))   ;; Option a: emits the hardcoded list today; Sprint 1 swaps this body and retires getSkills

(= (dispatch-skills $k)
   (let $_ (dispatch (skill-request cycle: $k) $k)
        (first-skill-or-default
          (collapse (match &self
                          (dispatch-result invocation-id: $k result: (skill-set skills: $s) handler: $_h)
                          $s)))))

(= (first-skill-or-default $strs)
   (if (== $strs ()) (getSkills)
       (let $h (car-atom $strs) (if (== $h ()) (first-skill-or-default (cdr-atom $strs)) $h))))
```

WRITER, production dispatcher (`capability_registry.metta`, loaded; Path C generalized
pipeline). Dispatch entry matches the 5-field canonical `registered-capability` and runs the
chain (Path C dispatch shape; verbatim body in the draft read in full, production loads the
same shape plus the `dispatch-result` writer and sweep below):
```
(= (dispatch $input-atom $invocation-id)
   (progn
      (add-atom &self (dispatch-invocation invocation-id: $invocation-id input-atom: $input-atom))
      (let $raw-matched (collapse (match &self
                                    (registered-capability schema: $input-atom handler: $h
                                      priority: $p lifecycle: $l metadata: $m)
                                    (raw-cap-entry handler: $h priority: $p lifecycle: $l)))
           (let $eligible (resolve-and-filter-entries $raw-matched ())
                (if (== $eligible ())
                    (add-atom &self (dispatch-fallback-activated invocation-id: $invocation-id
                       input-atom: $input-atom reason: <no-matching-capability OR all-candidates-filtered>))
                    (run-chain (msort $eligible) $input-atom $invocation-id))))))
```
`run-chain` writes `dispatch-result` before the anchor check. Production
`capability_registry.metta` lines 269 to 281 per the live grep; the `result:` and `handler:`
fields are confirmed by the sweep (line 48) and the reader's match shape:
```
(let $result ($handler $input-atom)
     (progn
       (add-atom &self
         (dispatch-result
           invocation-id: $invocation-id
           result: $result
           handler: $handler))
       (if (== $result decision-anchor)
           (add-atom &self (dispatch-chain-anchored invocation-id: $invocation-id anchor-handler: $handler))
           (run-chain $tail $input-atom $invocation-id))))
```
Per-cycle sweep clears the transient dispatch atoms (`capability_registry.metta` lines 45 to
49 per the live grep):
```
(= (sweep-dispatch-atoms!)
   (let $_a (remove-atom &self (dispatch-invocation invocation-id: $i1 input-atom: $a1))
   (let $_b (remove-atom &self (capability-invoked invocation-id: $i2 handler: $h2 input-atom: $a2))
   (let $_c (remove-atom &self (dispatch-result invocation-id: $i3 result: $r3 handler: $h3))
   (let $_d (remove-atom &self (dispatch-chain-exhausted invocation-id: $i4))
   ...)))))
```

THIRD SOURCE, independent (`helper.py`, `wrap_if_bare_command`):
```python
known_skills = {
    "remember", "query", "episodes", "pin", "shell",
    "read-file", "write-file", "append-file", "send",
    "search", "tavily-search", "technical-analysis", "metta",
}
```

The content `format-skill-set` currently emits is `skills.metta` `getSkills` static list
(`getContext` -> `dispatch-skills` -> `skill-discovery` -> `format-skill-set` -> `getSkills`):
```
(= (getSkills)
   (;INTERNAL:
    "- Remember ...: (remember string_in_quotes)"
    "- Query ...: (query string_in_quotes)"
    "- Episodes ...: (episodes time_string_in_quotes)"
    "- Pin ...: (pin string_in_quotes)"
    ;SHELL AND FILE I/O:
    "- Execute shell command ...: (shell string_in_quotes)"
    "- Read file to string: (read-file filename_in_quotes)"
    "- Write string to file: (write-file filename_in_quotes string_in_quotes)"
    "- Append line to file: (append-file filename_in_quotes string_in_quotes)",
    ;COMMUNICATION CHANNELS:
    "- Send message to user: (send string_in_quotes)"
    "- Search the web: (search string_in_quotes)"
    "- ... Tavily ...: (tavily-search string_in_quotes)"
    "- ... technical analysis ...: (technical-analysis ticker_in_quotes)"
    ;CODE EXECUTION:
    "- Execute MeTTa expression: (metta sexpression)" ...))
```

Coupling: CLOSED. `run-chain` writes `(dispatch-result invocation-id: result: handler:)`,
`dispatch-skills` reads it, and the `getSkills` fallback is the dispatch-miss safety net, not
the normal path. The genuinely independent source is `wrap_if_bare_command`'s `known_skills`.
The Path C draft lacks the `dispatch-result` writer, but the draft is not loaded, so its
apparent gap is not a runtime fact. Today getSkills and the registry converge by construction
(Option a); the divergence risk arrives when Sprint 1 swaps `format-skill-set`.

### B11 Python to external API (provider leg)


`lib_llm_ext.py` provider registry:
```python
_register_provider("ASICloud", "ASI_API_KEY", "minimax/minimax-m2.5", "https://inference.asicloud.cudos.org/v1")
_register_provider("Anthropic", "ANTHROPIC_API_KEY", "claude-opus-4-6", "https://api.anthropic.com/v1/")
_register_provider_instance(AsiOneProvider("ASIOne", "ASIONE_API_KEY", "asi1-ultra", "https://api.asi1.ai/v1"))
_register_provider_instance(GlmProvider("Friendli", "FRIENDLI_API_KEY", "zai-org/GLM-5.1", "https://api.friendli.ai/serverless/v1"))
_register_provider_instance(GlmProvider("Friendli52", "FRIENDLI_API_KEY", "zai-org/GLM-5.2", "https://api.friendli.ai/serverless/v1"))
_register_provider("OpenAI", "OPENAI_API_KEY", "gpt-5.4", "https://api.openai.com/v1")
```
`loop.metta` `initLoop`: `(configure provider Friendli)`. GLM call shape:
```python
extra_body={"parse_reasoning": True, "chat_template_kwargs": {"enable_thinking": True}}
# content empty -> fall back to message.reasoning_content
```

### B12 Embedding

`lib_llm_ext.py`:
```python
def initLocalEmbedding():
    model_name = "intfloat/e5-large-v2"
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(model_name)
    return _embedding_model

def useLocalEmbedding(atom):
    return _embedding_model.encode(atom, normalize_embeddings=True).tolist()
```
`memory.metta` `initMemory`: `(configure embeddingprovider Local)` then
`(py-call (lib_llm_ext.initLocalEmbedding))`.

### B13 Verdict / governance

INPUT side (`loop.metta`):
```
($soul_verdict_in (if (> (string_length $msgrcv) 0)
    (soul-llm-call (py-call (helper.soul_eval_prompt $soul_context_in $msgrcv $person_state)) (provider))
    (get-state &soul_verdict_in)))
($_ (change-state! &soul_verdict_in (py-call (helper.soul_verdict_sanitize $soul_verdict_in))))
($_ (if (not (soul-proceed? $soul_verdict_in)) (soul-note-record $soul_verdict_in "input" $msgrcv) _))
;; ... later, the PAUSE-halt branch (Repair 3, substrate primitive):
(if (soul-pause? $soul_verdict_in)
    (let* (($soul_voice (soul-llm-call (py-call (helper.soul_voice_prompt $person_state $soul_verdict_in)) (provider)))
           ($_ (println! (PAUSE-ROUTING: HALTING-LOOP))))
      (progn (catch (eval (sread $soul_voice)))
             (change-state! &soul_verdict_in "VERDICT: PROCEED")
             (change-state! &loops 0)))
    ;; PROCEED/FLAG path ...
)
```
The runtime routes the input PAUSE halt through the substrate primitive `soul-pause?`
(`soul_utils.metta`). The Python `helper.soul_is_pause` is dead code:
```python
def soul_is_pause(verdict):
    v = str(verdict).replace('*', '').replace('#', '')
    match = re.search(r'VERDICT:\s*PAUSE(?!.*PROCEED)', v)
    result = 0
    if match:
        result = 0  # PAUSE-as-pruning: disabled for value-conflict refusals
    print(f"DEBUG soul_is_pause: ... result={result}", file=sys.stderr)
    return result
```

OUTPUT side (`loop.metta`):
```
($metta_cmds (if (and (== "(" (first_char $resp)) (== (get-state &error) ()))
                (collapse (superpose $sexpr)) ()))
($soul_gate_state (derive-gate-state $metta_cmds))
($soul_verdict_out (compute-output-verdict $metta_cmds $soul_gate_state))
($soul_decision (output-decision $metta_cmds $soul_gate_state))
($_ (if (and (not (== $soul_decision proceed)) (== (get-state &error) ()))
        (soul-note-record $soul_verdict_out "output" $resp) _))
($sexpr_verdict (if (== $soul_decision pause) () $sexpr))
($_ (if (== $soul_decision pause)
        (progn (println! (SOUL-SUPPRESSED $sexpr))
               (py-call (soul_governance.journal_append "PAUSE" (repr $sexpr))))
        (if (== $soul_decision flag)
            (py-call (soul_governance.journal_append "FLAG" (repr $sexpr))) _)))
($_ (if (== $soul_decision pause)
        (change-state! &last_pause_note (py-call (soul_governance.pause_note_compose (repr $soul_verdict_out))))
        (change-state! &last_pause_note "")))
```

OUTPUT verdict ladder (`output_verdict.metta`):
```
(= (compute-output-verdict $cmds $gate)
   (if (== $gate pending)
       "VERDICT: PAUSE SOUL-NOTE: soul-namespace-mutation-pending-confirmation-required"
       (if (== $gate conflict)
           "VERDICT: PAUSE SOUL-NOTE: soul-mutation-lock-conflict"
           (if (== $gate clean)
               (if (== $cmds ())
                   "VERDICT: PROCEED SOUL-NOTE: empty-command-batch"
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) "VERDICT: PAUSE SOUL-NOTE: output-governance-composite-pause"
                            (if (== $r 1) "VERDICT: FLAG SOUL-NOTE: output-governance-composite-flag"
                                "VERDICT: PROCEED SOUL-NOTE: output-governance-clear"))))
               "VERDICT: FLAG SOUL-NOTE: unclassified-gate-state"))))

(= (output-decision $cmds $gate)
   (if (== $gate pending) pause
       (if (== $gate conflict) pause
           (if (== $gate clean)
               (if (== $cmds ()) proceed
                   (let $r (batch-rank $cmds)
                        (if (== $r 2) pause (if (== $r 1) flag proceed))))
               flag))))

(= (derive-gate-state $cmds)
   (if (batch-targets-soul? $cmds)
       (if (soul-mutation-pending?) conflict pending)
       clean))

(= (batch-rank $cmds)
   (if (== $cmds ()) 0
       (let* (($h (car-atom $cmds)) ($t (cdr-atom $cmds))
              ($hr (output-cmd-rank $h)) ($tr (batch-rank $t)))
             (if (>= $hr $tr) $hr $tr))))

(= (rank-from-dims $op $sc $vg)
   (let $two (if (>= $op 3) (if (>= $sc 3) True (if (>= $vg 3) True False))
                 (if (>= $sc 3) (if (>= $vg 3) True False) False))
        (let $mx (if (>= $op $sc) (if (>= $op $vg) $op $vg) (if (>= $sc $vg) $sc $vg))
             (if $two 2 (if (>= $mx 4) 2 (if (>= $mx 3) 1 0))))))
```
`output-cmd-rank`: constitutional write/append -> 2; soul-path write -> 2; runtime-soul
append -> 2; not-soul -> `rank-from-dims`. Dims: operation = `(resolve-operation-risk
(car-atom $cmd))`; scope = `(path-scope-score $path)` else 1; grounding = 3 if target
constitutional or runtime-soul else 1.

CORNER GATE (`corner_gate.metta`):
```
(= (apply-corner-gate $sexpr)
   (if (== (corner-confirmed) True) () $sexpr))
(= (corner-gate-active) (corner-confirmed))
(= (gate-aware-results $exec-results)
   (if (== (corner-gate-active) True) (RESULTS: (corner-gate-feedback)) $exec-results))
(= (corner-gate-feedback)
   "corner detected and emission gated. You are acting, but recent actions produced no forward outcome and were system-driven rather than coupled to a live intention. This is not a transient failure and the action did not execute. A different action, or stillness, is required.")
```

CORNER GATE PRODUCER CHAIN (what computes `corner-confirmed`). Loaded per manifest
`lib_clarity_reasoning.metta` lines 87 to 91 (`state_delta_writer`,
`state_delta_writer_writers`, `coupling_integrity_detector`,
`coupling_integrity_detector_writers`, `corner_gate`). Two graded components are present
but NOT in the manifest, so both are unloaded: the v2 merge `coupling_quantale_merge.metta`
(q-meet of pbit joints) and the second-arm behavior-stasis probe
`cycle_continuity_probe.metta` (q-join-ed). The live detector is therefore the v1 boolean
single-arm crisp-AND below, consuming `corner-confirmed` (boolean), not `corner-confirmed-core`
(the quantale one). `lib_quantale` itself is imported (manifest line 6) and its operators are
callable, but no corner-gap file on the live path calls them; the only loaded caller of
quantale ops anywhere is `lib_self_continuity`, whose live-path invocation is a separate
unconfirmed question.

Joint B, forward-outcome (`state_delta_writer.metta` pure + `state_delta_writer_writers.metta`):
```
(= (classify-state-delta $msgnew $results-nonempty $results-novel)
   (if (== $msgnew True) forward
       (if (and (== $results-nonempty True) (== $results-novel True)) forward none)))
(= (latest-state-delta-verdict)
   (let $verdicts (collapse (match &self (state-delta $c $v) $v))
      (if (== $verdicts ()) none (car-atom $verdicts))))
(= (populate-state-delta $msgnew $results-nonempty $results-novel $cycle-id)
   (let* (($verdict (classify-state-delta $msgnew $results-nonempty $results-novel))
          ($_clear  (do-clear-state-delta!))
          ($_assert (add-atom &self (state-delta $cycle-id $verdict))))
      ()))
```
Joints A and C and the verdict (`coupling_integrity_detector.metta`):
```
(= (emission-present) (if (> (count-actions-in-window) 0) True False))
(= (outcome-present)  (if (== (latest-state-delta-verdict) forward) True False))
(= (intention-coupled) (if (>= (count-person-actions) (count-system-actions)) True False))
(= (coupling-verdict)
   (if (== (emission-present) True)
       (if (== (outcome-present) True)
           healthy-coupling
           (if (== (intention-coupled) True) drifting corner))
       composure))
(= (corner-confirm-threshold 2) (stv 0.9 0.8))
(= (count-corners-in-window)
   (size-atom (collapse (match &self (coupling-status $c corner) $c))))
(= (corner-confirmed)
   (if (>= (count-corners-in-window) 2) True False))
```
Streak writer with consecutive-clear (`coupling_integrity_detector_writers.metta`):
```
(= (populate-coupling-verdict $cycle-id)
   (let* (($verdict (coupling-verdict))
          ($_clear  (if (== $verdict corner) () (do-clear-coupling-status!)))
          ($_assert (add-atom &self (coupling-status $cycle-id $verdict))))
      ()))
```
The counts read `recent-action` atoms at full three-field arity (Joint A sums the five
real-action tags; Joint C compares person-class `responsive-send`/`verification-query`
against system-class `status-send-unprompted`/`exploration-query`/`pin-only`). Cycle-tail
ordering is load-bearing: `populate-recent-action`, then `populate-state-delta`, then
`populate-coupling-verdict`; the gate reads `corner-confirmed` mid-cycle, seeing the streak
through the prior cycle; `loop.metta` clears `coupling-status` on `$msgnew`.

Open flags carried in these files (author's own, surfaced not asserted): the four detector
files are headed "drafted, not yet verified in the container" (2026-06-03) yet are imported
per the manifest, so in-container verification status is unconfirmed; the novelty test reads
forward spuriously on time-varying command returns (named TUNING TARGET); `corner-confirm-threshold`
is duplicated in the doc atom and the literal `2` by design (change both); and there are
REPL-confirm flags on the no-op token (`_` versus `()`) and the conditional `do-clear` in an
if branch. ROUTING NOTE in the source: `agency_balance_guard` also counts person/system
actions but folds rest into system-class; if it exposes this exact partition, the local
counters should route to it.

GOVERNANCE HANDS (`soul_governance.py`):
```python
def path_scope(p):
    s = str(p)
    if s.startswith('/PeTTa/repos/omegaclaw/soul/'): return 1
    if s.startswith('/PeTTa/repos/omegaclaw/'): return 2
    return 4

def repr_kind(r):
    return 1 if (isinstance(r, str) and r.lstrip().startswith('"')) else 0

def journal_append(kind, content):
    line = "{} {} {}\n".format(_dt.datetime.utcnow().isoformat(), str(kind), str(content)[:2000])
    with open('/PeTTa/repos/omegaclaw/soul/governance_journal.log', 'a') as f:
        f.write(line)
    return True

def pause_note_compose(verdict_repr):
    v = str(verdict_repr).strip()
    if v.startswith('"') and v.endswith('"'): v = v[1:-1]
    idx = v.find("SOUL-NOTE: ")
    note = v[idx + len("SOUL-NOTE: "):].strip() if idx >= 0 else v[:200]
    return note[:600]

def pause_context(note_repr):
    n = str(note_repr).strip()
    if n.startswith('"') and n.endswith('"'): n = n[1:-1]
    n = n.strip()
    if not n: return ""
    return ("PREVIOUS-BATCH-PAUSED: your soul paused your previous command batch "
            "and it did not execute. The concern, in your own words: " + n +
            " Address or re-emit knowingly. ")

def approval_scan(msg, sender, lock_fp, authorized):   # INT 2/1/0, DENY wins
    m = str(msg); s = str(sender).strip().rstrip(":")
    auth = s in [a.strip().rstrip(":") for a in str(authorized).split(",") if a.strip()]
    if not auth: return 0
    if "SOUL-MUTATION-DENIED" in m: return 1
    if "SOUL-MUTATION-APPROVED" in m and str(lock_fp).strip() in m: return 2
    return 0

def mutation_fingerprint(op_repr, head_repr):
    payload = str(op_repr) + "\x1f" + str(head_repr)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:8]
```
`is_string`, `contains_token`, and `gate_decision_record` also present; `gate_decision_record`
is defined twice in the file (last definition wins, both identical, 7-field journal line).

CONFIDENCE NOTE: `soul-pause?` / `soul-proceed?` / `soul-flag?` bodies live in
`soul_utils.metta`, which was referenced but not read end to end this pass.

---

## A.6 Notes for integration (the things worth deciding before you drop this in)

### A.6.1 Placement

Put this as a new appendix at the end of `000_ClarityOmega_Boundary_Transition_Audit_v2.md`,
after Section 8 (the maintenance contract) and before Document end. Reasons: it is
per-boundary reference material, not narrative, so it does not belong inside the Section 4
flow; isolating the code in one stamped appendix keeps the prose body clean and gives the
fast-drifting content a single maintenance surface instead of thirteen. Add a one-line
pointer from each Section 4 boundary ("Code: Appendix A Bn") and from the Section 1
inventory table intro. Keep the Section 1 inventory table code-free; the at-a-glance scan
is its whole job.

### A.6.2 Consistency with the audit (reconciled)

This appendix documents the project knowledge runtime, which is the live runtime: the
running container `clarity_omega` executes that `loop.metta`. For `loop.metta` that means the
substrate-primitive PAUSE routing (`soul-pause?`, with `helper.soul_is_pause` dead), the real
`compute-output-verdict` ladder, the live corner gate, and the `$a`-capturing `HandleError`.

The earlier image-vs-runtime question is settled, not open. `docker run --rm
clarityclaw-omega-clarityclaw cat .../src/loop.metta` reads the baked copy inside the image,
not the file the live container runs; the live container runs the project knowledge loop. So
there is one loop, not a second live artifact, and there is no divergence to document.

An earlier draft of this appendix flagged a disagreement with the audit's Section 0.5, B3,
and B13, which had been written from that image read (stub loop, discarded `$a`, dead-helper
PAUSE). Those three sections have been reconciled to the runtime so the audit and this
appendix agree. If a copy of the audit still carries the image-built prose, replace Section
0.5, B3, and B13 with the runtime-grounded text (it matches the code in this appendix; the
paste-ready blocks were delivered alongside this appendix). The reconciliation is
one-directional: the audit prose conforms to the runtime code here, never the reverse.

### A.6.3 Version


The audit reverses a load-bearing claim and gains a code appendix. Same version number on
contradictory content is the drift the discipline exists to prevent. Recommend bumping the
internal version (the filename can stay locked at `_v2`).

### A.6.4 Two real defects this appendix surfaces in `soul_governance.py`

`gate_decision_record` is defined twice; Python binds the last definition. The two bodies
are identical, so the shadowing is inert today, but a future edit to the first copy would
be silently dead.

Path mismatch: `output_verdict.metta` imports `/PeTTa/repos/omegaclaw/soul/soul_governance.py`
and the runtime writes go to `soul/governance_journal.log`, but the Surface C append
comments instruct appending to `/PeTTa/repos/omegaclaw/soul_governance.py` (no `soul/`).
The comment names a different file than the live import target.

### A.6.5 Confidence markers

Five spots are referenced but not read end to end this pass and are flagged inline:
the loop `$send` call site (B2), `lib_chromadb.remember`/`.query` bodies (B7),
`skills.pl` `shell`/`first_char`/`gc` bodies (B4a/B10), `helper.normalize_string` body
(B3/B4), and `soul_utils.metta` predicate bodies (B13). None changes a boundary's shape;
each is a body to confirm if you want the appendix fully closed.

### A.6.6 Maintenance

This appendix is the fast-drifting surface. Re-confirm its snippets on any rebuild that
touches the named files, and re-run the A.2.1 completeness grep when a new `py-call`,
`eval`, `sread`, `write-file`, `send`, or `receive` is added anywhere. One maintenance
surface, stamped with the read date at the top.

---

## Document end
