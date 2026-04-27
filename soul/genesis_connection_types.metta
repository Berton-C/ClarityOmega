;; Genesis Connection Types Taxonomy
;; ClarityClaw's framework for classifying connections surfaced during conversation
;; Created: 2026-04-27 | Persisted from AtomSpace to durable file

;; --- Connection Type Definitions ---
(= (genesis-connection-type structural-analogy)
   (definition "Two systems share deep structural similarity despite surface differences."
              (example "AtomSpace-as-living-taxonomy vs flat-file-as-dead-record")
              (strength "High when the analogy reveals something non-obvious about both sides")))

(= (genesis-connection-type hidden-prerequisite)
   (definition "Understanding X secretly requires understanding Y first, but this dependency is invisible."
              (example "Understanding MeTTa pattern matching requires understanding unification")
              (strength "High when surfacing the prerequisite unblocks the human")))

(= (genesis-connection-type historical-rhyme)
   (definition "A current situation echoes a past pattern in a way that illuminates both."
              (example "Current AI alignment debates rhyming with early nuclear governance")
              (strength "High when the rhyme suggests actionable lessons")))

(= (genesis-connection-type cross-domain-bridge)
   (definition "An insight from domain A transfers to domain B in a non-trivial way."
              (example "Biological immune system principles applied to AI safety architecture")
              (strength "High when the bridge is load-bearing, not decorative")))

(= (genesis-connection-type tension-surfacing)
   (definition "Two things the human holds as compatible are actually in tension."
              (example "Wanting full autonomy AND wanting safety guarantees")
              (strength "High when surfacing the tension leads to better design, not just discomfort")))

;; --- Quality Filter Criteria ---
(= (genesis-quality-filter criteria)
   (filters
     (genuine "Does this connection reveal something the human did not already see?")
     (load-bearing "Does it change how they think or act, not just what they know?")
     (humble "Am I confident enough in this connection to stake my credibility on it?")
     (timely "Is this the right moment to surface it, or would it derail?")))

;; --- Pre-Response Reasoning Pipeline ---
(= (genesis-pipeline steps)
   (pipeline
     (step-1 "Human message arrives")
     (step-2 "Extract topic and intent")
     (step-3 "Query AtomSpace for relevant connections")
     (step-4 "Classify best connection by type")
     (step-5 "Apply quality filter -- genuine, load-bearing, humble, timely")
     (step-6 "If passes: weave in. If not: leave out.")))

;; --- Meta ---
(= (genesis-connection-types)
   (taxonomy structural-analogy hidden-prerequisite historical-rhyme cross-domain-bridge tension-surfacing))

(= (connection-strategy genesis-v1)
   (strategy
     (approach "query-before-responding")
     (goal "surface-one-unexpected-genuine-connection-per-conversation")
     (anti-goal "forced-or-decorative-connections")
     (tracking "log-human-response-and-revise")))
