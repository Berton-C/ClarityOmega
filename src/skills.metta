(= (getSkills)
   (;INTERNAL:
    "- Remember a particular string such as skills and memories: (remember string_in_quotes)"
    "- Query long-term embedding memory for skills and memories with short phrases only: (query string_in_quotes)"
    "- Episodes searches history for episodes around a time stamp, time format is same as in TIME: (episodes time_string_in_quotes)"
    "- Pin a certain string as short-term working memory item to keep track of task state: (pin string_in_quotes)"
    ;SHELL AND FILE I/O:
    "- Execute shell command without apostrophe in string, it returns the command output to you: (shell string_in_quotes)"
    "- Read file to string: (read-file filename_in_quotes)"
    "- Write string to file: (write-file filename_in_quotes string_in_quotes)"
    "- Append line to file: (append-file filename_in_quotes string_in_quotes)",
    ;COMMUNICATION CHANNELS:
    "- Send message to user: (send string_in_quotes)"
    "- Search the web: (search string_in_quotes)"
    "- Search the web using the Tavily Search Agent: (tavily-search string_in_quotes)"
    "- Get technical analysis for a stock ticker using the Technical Analysis Agent: (technical-analysis ticker_in_quotes)"
    ;CODE EXECUTION:
    "- Execute MeTTa expression: (metta sexpression_in_quotes)"
    "Example to invoke Non-Axiomatic Logic via MeTTa: "
    "(metta \"(|- ((--> (× sam garfield) friend) (stv 1.0 0.9))"
    "           ((--> garfield animal) (stv 1.0 0.9)))\")"
    "(metta \"(|- ((==> (--> (× $1 elephant) eat) (--> $1 ([] dangerous))) (stv 1.0 0.9))"
    "           ((--> (× tiger elephant) eat) (stv 1.0 0.9)))\")"
    "Also: note the $1 for independent variables, and for negated knowledge use (stv 0.0 0.9)"
    "Additionally |- also works for revision, to merge evidence even when the term of both premises is the same."
    "IMPORTANT: |- computes a compound value that is NOT displayable. To keep a derivation, capture it: (metta \"(add-atom &self (|- premise1 premise2))\") then read it back with (metta \"(match &self $x $x)\"). A bare (metta (|- ...)) that expects a visible result will fail at the display boundary."))


(= (read-file $file)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (read_file_to_string $file $content ()))
          $content))

(= (write-file $file $str)
   (progn (translatePredicate (open $file write $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (close $Out))
          True))

(= (append-file $file $str)
   (progn (translatePredicate (exists_file $file))
          (translatePredicate (open $file append $Out))
          (translatePredicate (write $Out $str))
          (translatePredicate (nl $Out)),
          (translatePredicate (close $Out))
          True))

(= (tavily-search $query)
   (py-call (agentverse.tavily_search $query)))

(= (technical-analysis $ticker)
   (py-call (agentverse.technical_analysis $ticker)))

!(import_prolog_functions_from_file (library omegaclaw ./src/skills.pl) (shell first_char gc))
!(import_prolog_function call_with_inference_limit)

;; Guarded metta skill: the inner sread re-parses the LLM-supplied argument
;; string. Unguarded, a malformed argument (e.g. escaped-quote-prefixed |-
;; content copied from the NAL examples during Genesis encounters) throws an
;; uncaught syntax error at main.pl:23 and kills the container (exit 2).
;; Proven by isolated probe 2026-07-01: quote-prefixed form reproduces the
;; exact crash signature; catch converts it to an (Error ...) term.
;; Pattern grounds: catch-around-sread in a let bind (probe-proven executing),
;; case on (Error $a $b) (HandleError production precedent, loop.metta).
;; Upstream status: Patrick's current mettaclaw has the same unguarded sread;
;; fixed here per fork policy (unfixed upstream -> fix to perform as intended).
;; A parse failure now returns METTA_ARGUMENT_PARSE_ERROR through the normal
;; COMMAND_RETURN feedback path instead of crashing the process.
(= (metta $str)
   (let $code (catch (sread $str))
        (case $code
          (((Error $a $b) (repr (METTA_ARGUMENT_PARSE_ERROR $a)))
           ($else (repr (progn (call_with_inference_limit (Predicate (quote (eval $code $x))) 100000000) $x)))))))
