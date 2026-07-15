# === helper_py_addition.py ===
# DRAFT for Clarity's analysis. Destination: appended to src/helper.py
# (build step B2; the graded variant activates at B3).
#
# ADR-008: these are HANDS. Mechanical formatting of numbers and strings
# only. The framing sentence lives substrate-side in corner_state.metta
# (corner-state-teaching), Clarity's to amend.

def corner_state_block_format(streak, sig_repr, sig_count, window_count):
    """CORNER-STATE basic block (B2). Numbers and strings in, one line out."""
    return ("CORNER-STATE: streak=" + str(streak)
            + " repeated-cmd=" + str(sig_repr)
            + " repeat-count=" + str(sig_count)
            + " window-cmds=" + str(window_count))


def corner_state_block_format_graded(streak, sig_repr, sig_count,
                                     window_count, strength, confidence):
    """CORNER-STATE graded block (B3). Adds quantale strength/confidence."""
    return ("CORNER-STATE: streak=" + str(streak)
            + " repeated-cmd=" + str(sig_repr)
            + " repeat-count=" + str(sig_count)
            + " window-cmds=" + str(window_count)
            + " corner-strength=" + str(strength)
            + " corner-confidence=" + str(confidence))


# === loop_hook_changes (documentation, not code to paste) ===
# Four one-line changes, each a single named call (Discipline 1), each with
# artifact_1 updated in the same commit (Discipline 4). Line numbers per the
# 2026-07-05 full read of src/loop.metta.
#
# CHANGE 1 (B2, Phase 4.3 prompt assembly, getContext line ~53):
#   after:  " " (agency-balance-block)
#   insert: " " (corner-state-block)
#   (B3 commit swaps this call to corner-state-block-graded)
#
# CHANGE 2 (B2, Phase 4.5 output intercept tail, after line 172
#   populate-recent-action):
#   insert hook: ($_ (populate-cycle-trace! $metta_cmds $k))
#   ($metta_cmds is the collapsed ground list bound at line 140)
#
# CHANGE 3 (B4, line 166):
#   from: ($sexpr_gated (apply-corner-gate $sexpr_verdict))
#   to:   ($sexpr_gated (apply-corner-gate-v2 $sexpr_verdict $msgnew))
#
# CHANGE 4 (B4, line 168 and after line 176):
#   from: ($results_final (gate-aware-results $results))
#   to:   ($results_final (gate-aware-results-v2 $results $sexpr_gated $msgnew))
#   and after line 176 (populate-coupling-verdict):
#   insert hook: ($_ (populate-corner-window! $metta_cmds $k))
