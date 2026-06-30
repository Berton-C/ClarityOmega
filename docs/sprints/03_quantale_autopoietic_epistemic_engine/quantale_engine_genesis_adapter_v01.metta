;; quantale_engine_genesis_adapter_v01.metta
;; Genesis Engine adapter for the surface-general Quantale Autopoietic
;; Epistemic Dynamics Engine.
;;
;; This module is intentionally surface-specific. It translates Genesis
;; cross-domain conjunctions, held tensions, and candidate discoveries into
;; generic qsurface* records. The core engine remains Genesis agnostic.
;;
;; Pure adapter only: no add-atom/remove-atom/set-atom!/write-file.

;; ============================================================
;; 0. Genesis surface declaration
;; ============================================================

(: q-genesis-surface-id Atom)
(= q-genesis-surface-id genesis-surface)

(: q-genesis-surface (-> qsurface))
(= (q-genesis-surface)
   (mk-qsurface genesis-surface genesis-surface layer3))

(: q-genesis-adapter-status Atom)
(= q-genesis-adapter-status adapter-emits-generic-candidate-nexus-surface)

;; ============================================================
;; 1. Genesis-specific candidate shape
;; ============================================================

(: qgenesiscandidate Type)
(: mk-qgenesiscandidate (-> Atom Atom Atom Atom Atom Atom qgenesiscandidate))
;; shape: candidate-id domain-a domain-b connection-kind tension-status quality-status

(: q-genesis-candidate-id (-> qgenesiscandidate Atom))
(= (q-genesis-candidate-id (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $cid)

(: q-genesis-domain-a (-> qgenesiscandidate Atom))
(= (q-genesis-domain-a (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $a)

(: q-genesis-domain-b (-> qgenesiscandidate Atom))
(= (q-genesis-domain-b (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $b)

(: q-genesis-connection-kind (-> qgenesiscandidate Atom))
(= (q-genesis-connection-kind (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $connection)

(: q-genesis-tension-status (-> qgenesiscandidate Atom))
(= (q-genesis-tension-status (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $tension)

(: q-genesis-quality-status (-> qgenesiscandidate Atom))
(= (q-genesis-quality-status (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) $quality)

;; ============================================================
;; 2. Translation into generic surface records
;; ============================================================

(: q-genesis-as-surface-candidate (-> qgenesiscandidate qsurfacecandidate))
(= (q-genesis-as-surface-candidate (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfacecandidate genesis-surface $cid genesis-cross-domain-candidate))

(: q-genesis-lineage-status (-> qgenesiscandidate Atom))
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection held-without-collapse genuine)) lineage-visible)
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection held-without-collapse load-bearing)) lineage-visible)
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection tension-visible humble)) lineage-visible)
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection prematurely-resolved $quality)) lineage-partial)
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection forced-utility $quality)) lineage-partial)
(= (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection tension-opaque $quality)) lineage-missing)

(: q-genesis-as-surface-lineage (-> qgenesiscandidate qsurfacelineage))
(= (q-genesis-as-surface-lineage (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfacelineage $cid genesis-cross-domain-lineage
                       (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))))

(: q-genesis-as-surface-visibility (-> qgenesiscandidate qsurfacevisibility))
(= (q-genesis-as-surface-visibility (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfacevisibility $cid (q-genesis-lineage-status (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))))

(: q-genesis-as-surface-revisability (-> qgenesiscandidate qsurfacerevisability))
(= (q-genesis-as-surface-revisability (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfacerevisability $cid revisable))

(: q-genesis-uptake-status (-> qgenesiscandidate Atom))
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection $tension poetic-only)) insufficient-evidence)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection $tension clever-but-unneeded)) insufficient-evidence)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection $tension overclaimed)) insufficient-evidence)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection tension-opaque $quality)) insufficient-lineage)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection held-without-collapse genuine)) candidate-uptake)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection held-without-collapse load-bearing)) candidate-uptake)
(= (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection tension-visible humble)) candidate-uptake)

(: q-genesis-as-surface-uptake (-> qgenesiscandidate qsurfaceuptake))
(= (q-genesis-as-surface-uptake (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfaceuptake $cid (q-genesis-uptake-status (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))))

(: q-genesis-capacity-delta (-> qgenesiscandidate Atom))
(= (q-genesis-capacity-delta (mk-qgenesiscandidate $cid $a $b convergent-pathway held-without-collapse genuine)) future-capacity-candidate)
(= (q-genesis-capacity-delta (mk-qgenesiscandidate $cid $a $b cross-domain-bridge held-without-collapse load-bearing)) future-capacity-candidate)
(= (q-genesis-capacity-delta (mk-qgenesiscandidate $cid $a $b tension-surfacing tension-visible humble)) future-capacity-candidate)
(= (q-genesis-capacity-delta (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) future-capacity-unknown)

(: q-genesis-as-surface-capacity (-> qgenesiscandidate qsurfacecapacity))
(= (q-genesis-as-surface-capacity (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))
   (mk-qsurfacecapacity $cid (q-genesis-capacity-delta (mk-qgenesiscandidate $cid $a $b $connection $tension $quality))))

;; ============================================================
;; 3. Genesis risk guards
;; ============================================================

(: q-genesis-overclaim-risk (-> qgenesiscandidate Atom))
(= (q-genesis-overclaim-risk (mk-qgenesiscandidate $cid $a $b $connection $tension overclaimed)) overclaim-risk-present)
(= (q-genesis-overclaim-risk (mk-qgenesiscandidate $cid $a $b $connection forced-utility $quality)) overclaim-risk-present)
(= (q-genesis-overclaim-risk (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) risk-not-detected)

(: q-genesis-poetic-only-risk (-> qgenesiscandidate Atom))
(= (q-genesis-poetic-only-risk (mk-qgenesiscandidate $cid $a $b $connection $tension poetic-only)) poetic-only-risk-present)
(= (q-genesis-poetic-only-risk (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) risk-not-detected)

(: q-genesis-connection-addiction-risk (-> qgenesiscandidate Atom))
(= (q-genesis-connection-addiction-risk (mk-qgenesiscandidate $cid $a $b $connection tension-opaque $quality)) connection-addiction-risk-present)
(= (q-genesis-connection-addiction-risk (mk-qgenesiscandidate $cid $a $b $connection $tension clever-but-unneeded)) connection-addiction-risk-present)
(= (q-genesis-connection-addiction-risk (mk-qgenesiscandidate $cid $a $b $connection $tension $quality)) risk-not-detected)

(: q-genesis-shared-assumption-check (-> Atom Atom))
(= (q-genesis-shared-assumption-check shared-weak-premise) shared-assumption-detected)
(= (q-genesis-shared-assumption-check independent-paths) independent-paths-present)
(= (q-genesis-shared-assumption-check unknown-path-relation) insufficient-data)

(: q-genesis-independent-path-check (-> Atom Atom))
(= (q-genesis-independent-path-check independent-paths) independent-paths-present)
(= (q-genesis-independent-path-check shared-weak-premise) shared-assumption-detected)
(= (q-genesis-independent-path-check unknown-path-relation) insufficient-data)

;; ============================================================
;; 4. Process-trace bridge for NAL / Genesis discoveries
;; ============================================================

(: q-genesis-process-knowledge (-> Atom Atom pbit qprocessknowledge))
(= (q-genesis-process-knowledge $trace-id retrieval-empty $p)
   (mk-qprocessknowledge $trace-id genesis-derived-path retrieval-empty $p))
(= (q-genesis-process-knowledge $trace-id fact-persisted $p)
   (mk-qprocessknowledge $trace-id genesis-derived-path fact-persisted $p))
(= (q-genesis-process-knowledge $trace-id process-embedded $p)
   (mk-qprocessknowledge $trace-id genesis-derived-path process-embedded $p))

;; Stable writer schemas for runtime adapters. Comments only.
;;   ((--> (genesis-domain-pair $candidate-id) $domain-pair) (stv 1.0 $conf))
;;   ((--> (genesis-connection-type $candidate-id) $connection-kind) (stv 1.0 $conf))
;;   ((--> (genesis-tension-status $candidate-id) $hold-status) (stv 1.0 $conf))
;;   ((--> (genesis-quality-filter $candidate-id) $quality-status) (stv 1.0 $conf))
;;   ((--> (surface-candidate genesis-surface $candidate-id) genesis-cross-domain-candidate) (stv 1.0 $conf))
