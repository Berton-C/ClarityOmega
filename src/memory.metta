;Configured at runtime memory and history in amount of characters:
(= (maxFeedback) (empty))
(= (maxRecallItems) (empty))
(= (maxSimilarityRecall) (empty))
(= (maxEpisodeRecallLines) (empty))
(= (maxHistory) (empty))
(= (embeddingprovider) (empty))
(= (promotionInflationFactor) (empty))
(= (mostPromotedMemories) (empty))

(= (initMemory)
   (progn (println! "Initializing memory")
          (configure maxFeedback 50000)
          (configure maxRecallItems 20)
          (configure maxSimilarityRecall 10)
          (configure maxEpisodeRecallLines 20)
          (configure maxHistory 30000)
          (configure embeddingprovider Local) ;OpenAI or Local
          (configure promotionInflationFactor 10)
          (configure mostPromotedMemories 10)
          (py-call (helper.promotion_open_map))
          (reconcile-promotion-atoms)
          (if (== (embeddingprovider) Local)
              (py-call (lib_llm_ext.initLocalEmbedding)) _)))

(= (getPrompt)
   (read-file (library omegaclaw ./memory/prompt.txt)))

(= (getHistory)
   (let $ret (read-file (library omegaclaw ./memory/history.metta))
        (last_chars $ret (maxHistory))))

(= (addToHistory $lastmessage $response $sexpr $msgnew)
   (if $msgnew
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) "HUMAN_MESSAGE: " $lastmessage (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))
       (if (== (get-state &error) ())
           (appendToHistory ((get_time_as_string) (newline) $response (newline)))
           (appendToHistory ((get_time_as_string) (newline) $response (newline) ERROR_FEEDBACK: (get-state &error))))))

(= (embed $str)
   (if (== (embeddingprovider) Local)
       (py-call (lib_llm_ext.useLocalEmbedding (string-safe $str)))
       (useGPTEmbedding (string-safe $str))))

(= (appendToHistory $addition)
   (append-file (library omegaclaw ./memory/history.metta) (swrite $addition)))

(= (remember $str)
   (py-call (lib_chromadb.remember $str (embed $str) (get_time_as_string))))

(= (query $str)
   (py-call (lib_chromadb.query (embed $str) (maxRecallItems))))

(= (episodes $time)
   (py-call (helper.around_time $time (maxEpisodeRecallLines))))

;; ============================================================
;; PROMOTION INFRASTRUCTURE (additive, from upstream memory.metta)
;; Adopted per memory-layer merge design v1 Section 4.1.
;; Adapted for omegaclaw paths.
;; ============================================================

;; Compute current promotion salience for a uuid given current time.
;; Includes time-decay factor (half-life-ish based on day-scale exponential decay).
(= (get-promotion $current_time $uuid)
   (let* (($promotion (py-call (helper.promotion_get_value $uuid 0.0)))
          ($last_time (py-call (helper.promotion_get_lasttime $uuid 0.0)))
          ($t (- $current_time $last_time)))
         (* $promotion (pow-math (+ 1.0 (/ $t 86400.0)) (- 0.0 0.7)))))

;; Return the top-K promoted memory uuids ranked by current salience.
(= (best-promoted-memory-ids)
   (let* (($current_time (get_time))
          ($uuids (py-call (helper.promotion_get_all_keys)))
          ($ranked (takeK (mostPromotedMemories)
                          (msort (collapse (let* (($uuid (superpose $uuids))
                                                  ($promotion (get-promotion $current_time $uuid)))
                                                 (if (> $promotion 0.0) ((- 0.0 $promotion) $uuid))))))))
         (collapse (let ($p $uuid) (superpose $ranked) $uuid))))

;; Return the actual memory contents for the top-K promoted ids.
(= (best-promoted-memories)
   (let $uuids (best-promoted-memory-ids)
        (let $ret (py-call (lib_chromadb.query_by_ids $uuids))
             (progn (write-file ./repos/omegaclaw/memory/promoted_memories.metta "")
                    (repr (collapse (let ($uuid $t $c) (superpose $ret)
                                         (progn (append-file ./repos/omegaclaw/memory/promoted_memories.metta (repr ($t $c)))
                                                ($t $c)))))))))

;; T-3 Config B: promotion-weighted query as separate function from `query`.
;; Our existing `query` (lines 45-46) stays unchanged. Consumers explicitly
;; opt in to promotion-weighted ranking by calling this function.
(= (query-promoted $str)
   (let* (($embedding (embed $str))
          ($queryresults (py-call (lib_chromadb.query_with_ids_and_dists $embedding (* (promotionInflationFactor) (maxRecallItems)))))
          ($candidates (collapse (let* (($current_time (get_time))
                                        (($uuid $time $message $distance) (superpose $queryresults))
                                        ($promotion (get-promotion $current_time $uuid)))
                                       (if (> $promotion 0.0)
                                           ((- 0.0 $promotion) $distance $uuid $time $message))))))
         (let* (($best (takeK (maxRecallItems) (msort $candidates)))
                ($bestpromoted (collapse (let ($_ $_ $uuid $time $message) (superpose $best)
                                              ($time $message))))
                ($closest (collapse (let ($uuid $time $message $distance) (superpose $queryresults)
                                          ($time $message)))))
               (takeK (+ (maxRecallItems) (maxSimilarityRecall)) (unique-atom (append $bestpromoted $closest))))))

;; Promote: bump salience for memories at $time. Includes bridge to atomspace.
;; Section 7 (memory-layer merge design v1): dual-write to atomspace as
;; (promoted memory-id $uuid salience $newv). SQLite is source of truth;
;; atomspace is queryable derived view. add-atom call uses alpha (clean)
;; style per Q7 decision. Durability via reconcile-promotion-atoms at startup.
(= (promote $time)
   (let* (($current_time (get_time))
          ($uuids (py-call (lib_chromadb.ids_by_time $time))))
         (progn (collapse (let* (($uuid (superpose $uuids))
                                 ($v (get-promotion $current_time $uuid))
                                 ($newv (min 10.0 (+ 1.0 $v))))
                                (progn (py-call (helper.promotion_set_value $uuid $newv))
                                       (py-call (helper.promotion_set_lasttime $uuid $current_time))
                                       (add-atom &self (promoted memory-id $uuid salience $newv)))))
                (py-call (helper.promotion_commit))
                PROMOTE-SUCCESS)))

;; Demote: reduce salience for memories at $time. Same bridge pattern.
(= (demote $time)
   (let* (($current_time (get_time))
          ($uuids (py-call (lib_chromadb.ids_by_time $time))))
         (progn (collapse (let* (($uuid (superpose $uuids))
                                 ($v (get-promotion $current_time $uuid))
                                 ($newv (max 0.0 (- $v 1.0))))
                                (progn (py-call (helper.promotion_set_value $uuid $newv))
                                       (py-call (helper.promotion_set_lasttime $uuid $current_time))
                                       (add-atom &self (promoted memory-id $uuid salience $newv)))))
                (py-call (helper.promotion_commit))
                DEMOTE-SUCCESS)))

;; Startup reconciliation: read all promotion uuids from SQLite, compute
;; current salience, and write atomspace atoms. Called from initMemory after
;; promotion_open_map. Idempotent by design: re-running emits the same atoms.
;; MeTTa add-atom on identical atoms is the runtime's responsibility; this
;; function should be tested for idempotency during --dry-run verification.
;; Durability guarantee for the bridge: if SQLite has a promotion that
;; atomspace lacks (because of crash or restart), this function recovers it.
(= (reconcile-promotion-atoms)
   (let* (($current_time (get_time))
          ($uuids (py-call (helper.promotion_get_all_keys))))
         (collapse (let* (($uuid (superpose $uuids))
                          ($salience (get-promotion $current_time $uuid)))
                         (if (> $salience 0.0)
                             (add-atom &self (promoted memory-id $uuid salience $salience))
                             _)))))
