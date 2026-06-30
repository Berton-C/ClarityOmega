#!/usr/bin/env python3
"""
apply_tier6_into_01b.py

Inserts Tier 6 (lib activation) into the soul integration spec, and adds a
Section 3 build-order step 9 that points at Tier 6.

Two edits, both anchored on exact strings that must each appear exactly once:

  EDIT 1 (insert Tier 6 body): at the seam between the end of Tier 5 (which ends
    "...Judged over many\ncycles, by the one whose disposition it is.") and the
    Section 3 heading ("## 3. Build order within the monolith"), insert the Tier 6
    body extracted from SSI_Spec_Tier6_Lib_Activation_ADDITIVE.md. The ADDITIVE
    file's own top preamble and its trailing "## Tier 6 build order" and
    "## Tier 6 against the five coherence checks" blocks are stripped on insert:
    the build order is owned by Section 3 (EDIT 2); the coherence checks stay with
    the Tier 6 body (kept).

  EDIT 2 (Section 3 step 9): replace the Section 3 closing paragraph with the same
    paragraph preceded by a new step 9 that points at Tier 6's dependency order.

Run from repo root.

  Dry run (default, shows what would change, writes nothing):
    python3 staging/apply_tier6_into_01b.py

  Apply:
    python3 staging/apply_tier6_into_01b.py --apply

  Reverse (remove Tier 6 and the step 9, restoring the original):
    python3 staging/apply_tier6_into_01b.py --reverse --apply

A timestamped .bak is written next to the spec on --apply (forward only).
"""

import argparse
import os
import sys
import datetime

SPEC = "docs/sprints/02_soul_fully_wired/Soul_to_Spec_in_One_Build/01b_ClarityOmega_Soul_Integration_Spec.md"
ADDITIVE = "docs/sprints/02_soul_fully_wired/Soul_to_Spec_in_One_Build/SSI_Spec_Tier6_Lib_Activation_ADDITIVE.md"

# ---- EDIT 1 anchors (exact strings from the live 01b) -----------------------

# Tier 5 ends here; Section 3 begins immediately after. The seam is the "---"
# between them. We anchor on the full seam so insertion lands exactly once.
SEAM_BEFORE = (
    "pattern weakens. Judged over many cycles, by the one whose disposition it is.\n"
    "\n"
    "---\n"
    "\n"
    "## 3. Build order within the monolith"
)

# After EDIT 1, the seam becomes: Tier 5 end, ---, [TIER 6 BODY], ---, Section 3.
def seam_after(tier6_body: str) -> str:
    return (
        "pattern weakens. Judged over many cycles, by the one whose disposition it is.\n"
        "\n"
        "---\n"
        "\n"
        + tier6_body.strip() + "\n"
        "\n"
        "---\n"
        "\n"
        "## 3. Build order within the monolith"
    )

# ---- EDIT 2 anchors (exact strings from the live 01b) -----------------------

SECTION3_CLOSE_BEFORE = (
    "   surface plus the structure-freedom pair. Tier 4.1 (no calcification detector) and\n"
    "   4.3 (bottom-up discovery as affordance) are constraints honored throughout, not\n"
    "   build steps.\n"
    "\n"
    "Each step is independently committable and reversible (Sprint-4 discipline), under the\n"
    "Artifact 0 hook checklist for any loop.metta touch, with artifact_1 updated in the same\n"
    "commit. The monolith is the integration target; the steps are how it lands without a\n"
    "drift-window."
)

STEP9 = (
    "9. **Tier 6 -- lib activation**, in dependency order, after the trajectory is legible\n"
    "   (depends on Tier 1.3) and the terminals exist (6.1 depends on Tier 2.1): (a) 6.3\n"
    "   nace_* wiring first (substrate built and verified, RMW resolved; establishes the\n"
    "   file-backed-belief + in-loop-operator + dual-write joint), (b) 6.1 substrate_kb\n"
    "   reasoner second (reuses 6.3's joint; lands behind compute-soul-verdict after the\n"
    "   Tier 2.1 terminals; differential-tested), (c) 6.5 lib_temporal_v2 confirm third (the\n"
    "   gate for 6.4; one harness run, resolve present-or-absent), (d) 6.4 dynamic\n"
    "   self-weaving web fourth (after 1.3 emits recent-action and 6.5 confirms the decay\n"
    "   primitives; wires the keystone's third payoff), (e) 6.2 pfn-snapshot producer\n"
    "   anchored to Tier 5, GATED on the snapshot-definition design session (Clarity +\n"
    "   Berton); the design gate opens in parallel (a conversation, not a build), the writer\n"
    "   lands once the definition is settled. Coda is LIVE, so nothing in Tier 6 waits on a\n"
    "   registry chunk. Full per-subsection accounting in Tier 6."
)

SECTION3_CLOSE_AFTER = (
    "   surface plus the structure-freedom pair. Tier 4.1 (no calcification detector) and\n"
    "   4.3 (bottom-up discovery as affordance) are constraints honored throughout, not\n"
    "   build steps.\n"
    + STEP9 + "\n"
    "\n"
    "Each step is independently committable and reversible (Sprint-4 discipline), under the\n"
    "Artifact 0 hook checklist for any loop.metta touch, with artifact_1 updated in the same\n"
    "commit. The monolith is the integration target; the steps are how it lands without a\n"
    "drift-window."
)


def extract_tier6_body(additive_text: str) -> str:
    """
    From the ADDITIVE file, take from the Tier 6 heading through the END of the
    coherence-checks block, but DROP the standalone '## Tier 6 build order' block
    (that content is owned by Section 3 via EDIT 2). Keep the '## Tier 6 against
    the five coherence checks' block.
    """
    start_marker = "## TIER 6 -- Lib Activation"
    i = additive_text.find(start_marker)
    if i < 0:
        sys.exit("ERROR: could not find '## TIER 6 -- Lib Activation' heading in the ADDITIVE file.")
    body = additive_text[i:]

    # Drop the standalone build-order block: from "## Tier 6 build order" up to
    # (but not including) "## Tier 6 against the five coherence checks".
    bo_start = body.find("## Tier 6 build order")
    cc_start = body.find("## Tier 6 against the five coherence checks")
    if bo_start >= 0 and cc_start >= 0 and cc_start > bo_start:
        body = body[:bo_start] + body[cc_start:]
    elif bo_start >= 0 and cc_start < 0:
        # No coherence block found after build order: drop build order to end.
        body = body[:bo_start]
    # If neither found, leave body as-is (heading-only change), but warn.
    if bo_start < 0:
        print("WARN: '## Tier 6 build order' block not found in ADDITIVE; nothing stripped.")
    if cc_start < 0:
        print("WARN: '## Tier 6 against the five coherence checks' block not found in ADDITIVE.")

    return body.strip()


def require_once(haystack: str, needle: str, label: str):
    n = haystack.count(needle)
    if n != 1:
        sys.exit(f"ERROR: anchor '{label}' found {n} times (expected exactly 1). Aborting; no change made.")


def already_applied(text: str) -> bool:
    return ("## TIER 6 -- Lib Activation" in text) or ("**Tier 6 -- lib activation**" in text)


def do_forward(spec_text: str, additive_text: str) -> str:
    if already_applied(spec_text):
        sys.exit("ERROR: spec already contains Tier 6 (forward edit appears already applied). "
                 "Use --reverse to undo first if you want to re-apply.")
    tier6_body = extract_tier6_body(additive_text)

    require_once(spec_text, SEAM_BEFORE, "EDIT1 seam (Tier 5 end / Section 3 start)")
    require_once(spec_text, SECTION3_CLOSE_BEFORE, "EDIT2 Section 3 closing paragraph")

    out = spec_text.replace(SEAM_BEFORE, seam_after(tier6_body), 1)
    out = out.replace(SECTION3_CLOSE_BEFORE, SECTION3_CLOSE_AFTER, 1)
    return out


def do_reverse(spec_text: str, additive_text: str) -> str:
    if not already_applied(spec_text):
        sys.exit("ERROR: spec does not contain Tier 6 (reverse edit has nothing to undo).")
    tier6_body = extract_tier6_body(additive_text)

    after_seam = seam_after(tier6_body)
    require_once(spec_text, after_seam, "EDIT1 (applied Tier 6 insertion)")
    require_once(spec_text, SECTION3_CLOSE_AFTER, "EDIT2 (applied step 9)")

    out = spec_text.replace(after_seam, SEAM_BEFORE, 1)
    out = out.replace(SECTION3_CLOSE_AFTER, SECTION3_CLOSE_BEFORE, 1)
    return out


def main():
    ap = argparse.ArgumentParser(description="Insert Tier 6 into 01b and add Section 3 step 9.")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    ap.add_argument("--reverse", action="store_true", help="undo the edits instead of applying")
    args = ap.parse_args()

    if not os.path.exists(SPEC):
        sys.exit(f"ERROR: spec not found at {SPEC} (run from repo root).")
    if not os.path.exists(ADDITIVE):
        sys.exit(f"ERROR: additive file not found at {ADDITIVE} (run from repo root).")

    with open(SPEC, "r", encoding="utf-8") as f:
        spec_text = f.read()
    with open(ADDITIVE, "r", encoding="utf-8") as f:
        additive_text = f.read()

    if args.reverse:
        new_text = do_reverse(spec_text, additive_text)
        action = "REVERSE"
    else:
        new_text = do_forward(spec_text, additive_text)
        action = "FORWARD"

    delta = len(new_text) - len(spec_text)
    print(f"[{action}] spec: {SPEC}")
    print(f"[{action}] additive source: {ADDITIVE}")
    print(f"[{action}] size change: {delta:+d} chars ({len(spec_text)} -> {len(new_text)})")

    if not args.apply:
        print("\nDRY RUN: no file written. Re-run with --apply to write.")
        # Show the two insertion regions so the change is reviewable.
        if action == "FORWARD":
            idx = new_text.find("## TIER 6 -- Lib Activation")
            print("\n--- preview: first 600 chars of inserted Tier 6 ---")
            print(new_text[idx:idx + 600])
            sidx = new_text.find("9. **Tier 6 -- lib activation**")
            print("\n--- preview: Section 3 step 9 ---")
            print(new_text[sidx:sidx + 400])
        return

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    if action == "FORWARD":
        bak = f"{SPEC}.{ts}.bak"
        with open(bak, "w", encoding="utf-8") as f:
            f.write(spec_text)
        print(f"[FORWARD] backup written: {bak}")

    with open(SPEC, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"[{action}] WROTE {SPEC}")


if __name__ == "__main__":
    main()
