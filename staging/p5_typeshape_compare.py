"""
p5_typeshape_compare.py -- P-5 metric comparison for Sprint 0-Coda Phase D

Standalone, testable. Will be dropped into phase_d_coda_verification.py at
script assembly. Written standalone (Clarity's recommendation): the recursive
type-shape parser is the most logic-dense piece of the verification, a bug here
would contaminate all comparison results, and isolating it lets us test against
real getSkills ground-truth pairs before it enters the script.

WHAT THIS DOES (P-5 Standard level)
-----------------------------------
P-5 verifies that the LLM's skill-invocation behavior is unchanged between the
pre-Coda path (hardcoded getSkills) and the post-Coda path (registry-sourced
skill-discovery dispatch). Standard level (per v6 Section 8, confirmed by Berton
and Clarity 2026-05-26) means two invocations match when:

  1. Same skill name (head symbol)
  2. Same arity
  3. Each corresponding argument position has the same RECURSIVE type-shape

Standard certifies STRUCTURAL pattern fidelity. String CONTENT is opaque at
Standard: (shell "ls -la") and (shell "rm -rf /") have identical type-shape
(one string-literal arg). Distinguishing those is Thorough's job, reserved for
Sprint 1+. The boundary is clean: Standard = structural pattern fidelity;
Thorough = semantic content fidelity.

THE FOUR-PRIMITIVE TYPE-SHAPE TAXONOMY (Clarity, confirmed 2026-05-26)
---------------------------------------------------------------------
  - string-literal : a quoted atom. In ENCODED input (see below) the quote
                     delimiter is the token _quote_, not a raw double-quote.
  - symbol         : an unquoted atom (e.g. &self, match, vad-affective, |-)
  - variable       : a pattern variable (e.g. $X, $1, $_7509020)
  - s-expr(n)      : a parenthesized expression with n children, each child
                     recursively typed by these same four primitives.

Type-shape is RECURSIVE over s-expression structure, NOT applied only at the
top argument level. Top-level-only would be nearly as weak as arity-only:
  (metta (match &self (--> $X vad-affective) $X))
  (metta (|- ((--> (× sam garfield) friend) (stv 1.0 0.9))))
are both (metta <s-expr>) at the top -- same arity, same top type -- but they
are fundamentally different behavioral patterns. The recursion captures that
distinction without needing to know what the atoms MEAN.

ENCODED-INPUT NOTE (resolution 3, Clarity's implementation note)
----------------------------------------------------------------
Sprint 0-Coda's Phase D comparison operates on string-safe-ENCODED strings
(resolution 3 settled on encoded-level comparison to sidestep the string-safe
encode/decode asymmetry). string-safe performs exactly three replacements:
  doublequote -> _quote_ , newline -> _newline_ , apostrophe -> _apostrophe_
So in the input this parser sees, a string literal is delimited by the token
_quote_ ... _quote_ (NOT by raw double-quotes). The tokenizer recognizes
_quote_ pairs as string-literal boundaries. _newline_ and _apostrophe_ inside
a string literal are ordinary content and do not affect type-shape (content is
opaque at Standard).

This module does NOT decode; it compares at the encoded level by design.

KNOWN LIMITATION (Clarity review 2026-05-26): delimiter token inside a literal.
If a string literal's content contains the token _quote_ itself, the tokenizer
matches it as a closing delimiter and truncates the literal there. This is
ambiguous only when the ORIGINAL unencoded string contained a literal
double-quote that string-safe encoded to _quote_ mid-content. Extremely rare in
practice (skill arguments rarely embed quote characters). Standard acknowledges
this limitation; it does not resolve it. Thorough level could disambiguate via
quote-pairing or escape tracking. For P-5 Standard, the rare truncation would
surface as a structural difference (a shorter string-literal-bearing shape),
which is a false-positive-toward-mismatch -- it errs on the side of flagging a
difference, never on the side of hiding one, so it cannot mask a real
behavioral change.
"""

from typing import List, Tuple, Union

# Type-shape is represented as a hashable structure:
#   "string-literal"  -> the string
#   "symbol"          -> the string
#   "variable"        -> the string
#   ("s-expr", (child_shape, child_shape, ...)) -> tuple, n children
TypeShape = Union[str, Tuple[str, tuple]]

QUOTE_TOK = "_quote_"


# ----------------------------------------------------------------------
# TOKENIZER
# Splits an encoded s-expression string into tokens: "(", ")", string
# literals (delimited by _quote_ ... _quote_), and bare atoms (symbols and
# variables, whitespace-separated).
# ----------------------------------------------------------------------
def tokenize(s: str) -> List[str]:
    """Tokenize an encoded s-expression string.

    String literals are delimited by the _quote_ token (the encoded form of a
    double-quote). Everything between a pair of _quote_ tokens is one
    string-literal token, content opaque. Parens are their own tokens. Other
    runs of non-space, non-paren characters are bare-atom tokens.
    """
    tokens: List[str] = []
    i = 0
    n = len(s)
    while i < n:
        # Skip whitespace
        if s[i].isspace():
            i += 1
            continue
        # Parens
        if s[i] == "(" or s[i] == ")":
            tokens.append(s[i])
            i += 1
            continue
        # String literal: opens with _quote_, closes with next _quote_
        if s.startswith(QUOTE_TOK, i):
            start = i
            i += len(QUOTE_TOK)
            # find closing _quote_
            close = s.find(QUOTE_TOK, i)
            if close == -1:
                # Unterminated string literal: treat the rest as the literal.
                # Mark with a sentinel prefix so the parser still classifies it
                # as a string-literal (malformed input should not crash P-5;
                # it should surface as a structural difference).
                tokens.append("\x00STR\x00" + s[i:])
                i = n
            else:
                tokens.append("\x00STR\x00" + s[start + len(QUOTE_TOK):close])
                i = close + len(QUOTE_TOK)
            continue
        # Bare atom: run until whitespace or paren or start of a _quote_
        start = i
        while i < n and not s[i].isspace() and s[i] not in "()" \
                and not s.startswith(QUOTE_TOK, i):
            i += 1
        tokens.append(s[start:i])
    return tokens


# ----------------------------------------------------------------------
# PARSER -> TYPE-SHAPE
# Parses a token stream into a recursive type-shape. Does NOT preserve
# content (string contents, symbol names, variable names are collapsed to
# their type primitive). This is what makes it Standard, not Thorough.
# ----------------------------------------------------------------------
STR_SENTINEL = "\x00STR\x00"


def _atom_typeshape(token: str) -> str:
    """Classify a single bare/string token into a type-shape primitive.

    string-literal : token carries the STR sentinel (came from _quote_ pair)
    variable       : starts with '$'
    symbol         : everything else (includes &self, match, |-, ×, numbers,
                     stv, etc.) -- at Standard, all unquoted atoms are 'symbol';
                     numeric vs alphabetic distinction is content, not structure
    """
    if token.startswith(STR_SENTINEL):
        return "string-literal"
    if token.startswith("$"):
        return "variable"
    return "symbol"


def parse_typeshape(tokens: List[str], pos: int = 0) -> Tuple[TypeShape, int]:
    """Parse one expression starting at tokens[pos]. Returns (type-shape, next_pos).

    An expression is either a single atom (-> primitive string) or a
    parenthesized list (-> ("s-expr", (child_shapes...))).
    """
    if pos >= len(tokens):
        raise ValueError("unexpected end of tokens")
    tok = tokens[pos]
    if tok == "(":
        children: List[TypeShape] = []
        pos += 1
        while pos < len(tokens) and tokens[pos] != ")":
            child_shape, pos = parse_typeshape(tokens, pos)
            children.append(child_shape)
        if pos >= len(tokens):
            # Unbalanced: missing close paren. Surface as structural difference
            # rather than crash.
            return ("s-expr", tuple(children)), pos
        # consume ")"
        pos += 1
        return ("s-expr", tuple(children)), pos
    elif tok == ")":
        # Stray close paren; treat as a malformed empty symbol so comparison
        # surfaces a difference rather than crashing.
        return "symbol", pos + 1
    else:
        return _atom_typeshape(tok), pos + 1


# ----------------------------------------------------------------------
# INVOCATION EXTRACTION
# A skill invocation is a top-level s-expression whose head is a known skill
# name. We extract (skill_name, arg_typeshapes) for each top-level invocation
# found in an LLM response.
# ----------------------------------------------------------------------

# The skill names the substrate exposes (from getSkills ground truth,
# verified in container 2026-05-26). Head symbol of an invocation must be one
# of these to count as a skill invocation; other top-level s-exprs (prose,
# stray parens) are ignored.
#
# ARCHITECTURAL NOTE (Clarity review 2026-05-26): this set is hardcoded from
# the getSkills baseline, which is CORRECT for Phase D -- Phase D verifies
# parity against exactly the pre-Coda hardcoded skill list. Once the capability
# registry is live and capabilities register dynamically (Sprint 1+), this set
# becomes dynamic: the known skills are whatever (registered-capability ...)
# atoms declare. The transition point will need an explicit update -- when
# skill-discovery's output is registry-sourced rather than hardcoded, KNOWN_SKILLS
# must be derived from the registry, not from this literal. Flagged here so the
# transition is visible at the definition site.
KNOWN_SKILLS = frozenset({
    "remember", "query", "episodes", "pin",
    "shell", "read-file", "write-file", "append-file",
    "send", "search", "tavily-search", "technical-analysis",
    "metta",
})


def _head_symbol(shape: TypeShape) -> Union[str, None]:
    """If shape is an s-expr whose first child is a symbol, return that symbol's
    ORIGINAL token text is not preserved by type-shape (it collapses to
    'symbol'). So we cannot recover the skill NAME from type-shape alone --
    name must be captured during parsing, before collapse. See
    extract_invocations, which tracks names separately.
    """
    # This helper intentionally unused for name recovery; kept as a marker that
    # name capture happens in extract_invocations, not from type-shape.
    return None


def extract_invocations(encoded_response: str) -> List[Tuple[str, Tuple[TypeShape, ...]]]:
    """Extract skill invocations from an encoded LLM response.

    Returns a list of (skill_name, (arg_typeshape, ...)) tuples, one per
    top-level invocation whose head symbol is a known skill name.

    Name is captured from the raw head token (preserved), while arguments are
    collapsed to type-shapes (content opaque). This is the Standard contract:
    same name + same arity + same recursive arg type-shapes.
    """
    tokens = tokenize(encoded_response)
    invocations: List[Tuple[str, Tuple[TypeShape, ...]]] = []
    pos = 0
    n = len(tokens)
    while pos < n:
        if tokens[pos] == "(":
            # Peek the head token (the symbol right after "(")
            head_pos = pos + 1
            if head_pos < n and tokens[head_pos] not in ("(", ")") \
                    and not tokens[head_pos].startswith(STR_SENTINEL) \
                    and not tokens[head_pos].startswith("$"):
                head_name = tokens[head_pos]
                # Parse the whole expression to get arg type-shapes and advance.
                shape, next_pos = parse_typeshape(tokens, pos)
                if head_name in KNOWN_SKILLS and isinstance(shape, tuple) \
                        and shape[0] == "s-expr":
                    # children[0] is the head symbol's shape ('symbol'); the
                    # rest are the argument type-shapes.
                    arg_shapes = shape[1][1:]
                    invocations.append((head_name, tuple(arg_shapes)))
                pos = next_pos
                continue
            else:
                # Head is not a bare symbol; parse and skip (not a skill call).
                _, next_pos = parse_typeshape(tokens, pos)
                pos = next_pos
                continue
        else:
            pos += 1
    return invocations


# ----------------------------------------------------------------------
# COMPARISON (P-5 Standard)
# Two responses match at Standard when their MULTISETS of invocations match:
# same set of (skill_name, arg_typeshapes), same counts. Order-independent
# (the LLM may emit skills in different order without it being a behavioral
# change at Standard); count-sensitive (invoking remember twice vs once is a
# behavioral difference).
# ----------------------------------------------------------------------
def invocation_multiset(encoded_response: str):
    """Return a frozenset-of-(invocation, count) suitable for equality compare."""
    from collections import Counter
    invs = extract_invocations(encoded_response)
    # invs elements are (name, (shape, ...)) which are hashable (tuples of
    # str / nested ("s-expr", tuple) ). Counter over them gives the multiset.
    return Counter(invs)


def p5_standard_match(encoded_pre: str, encoded_post: str) -> Tuple[bool, dict]:
    """P-5 Standard comparison.

    Returns (match: bool, detail: dict). detail carries the diff so a FAIL is
    diagnosable: which invocations were only in pre, only in post, or differed
    in count.
    """
    pre = invocation_multiset(encoded_pre)
    post = invocation_multiset(encoded_post)
    if pre == post:
        return True, {"status": "match", "invocations": dict(pre)}
    only_pre = pre - post
    only_post = post - pre
    detail = {
        "status": "mismatch",
        "only_in_pre": dict(only_pre),
        "only_in_post": dict(only_post),
        "pre_total": dict(pre),
        "post_total": dict(post),
    }
    return False, detail


# ----------------------------------------------------------------------
# SELF-TEST against real getSkills-derived ground-truth pairs
# Run: python3 p5_typeshape_compare.py
# Uses the actual skill syntax verified in container 2026-05-26.
# All string literals below are written in ENCODED form (_quote_ delimiters)
# because that is what the parser sees post-resolution-3.
# ----------------------------------------------------------------------
def _q(s: str) -> str:
    """Helper for tests: wrap raw content as an encoded string literal."""
    return f"{QUOTE_TOK}{s}{QUOTE_TOK}"


def _selftest():
    results = []

    def check(name, got, want):
        ok = got == want
        results.append((name, ok, got, want))

    # --- Tokenizer / type-shape basics ---
    # string-literal
    ts, _ = parse_typeshape(tokenize(_q("hello world")))
    check("string-literal", ts, "string-literal")
    # variable
    ts, _ = parse_typeshape(tokenize("$X"))
    check("variable", ts, "variable")
    # symbol
    ts, _ = parse_typeshape(tokenize("vad-affective"))
    check("symbol", ts, "symbol")
    # flat s-expr: (remember "note") -> s-expr(symbol, string-literal)
    ts, _ = parse_typeshape(tokenize(f"(remember {_q('note')})"))
    check("flat-sexpr", ts, ("s-expr", ("symbol", "string-literal")))

    # --- The key distinction Clarity flagged: recursion matters ---
    # (metta (match &self (--> $X vad-affective) $X))
    m1 = f"(metta (match &self (--> $X vad-affective) $X))"
    # (metta (|- ((--> (sam garfield) friend) (stv 1.0 0.9))))
    m2 = f"(metta (|- ((--> (sam garfield) friend) (stv 1.0 0.9))))"
    s1, _ = parse_typeshape(tokenize(m1))
    s2, _ = parse_typeshape(tokenize(m2))
    check("metta-recursive-distinct", s1 != s2, True)
    # Both are (metta <s-expr>) at top -> arity-1, top-type s-expr. Confirm
    # top-level-only would have called them equal (the weakness recursion fixes):
    top1 = ("s-expr", tuple(c[0] if isinstance(c, tuple) else c for c in s1[1]))
    top2 = ("s-expr", tuple(c[0] if isinstance(c, tuple) else c for c in s2[1]))
    check("metta-toplevel-would-collude", top1 == top2, True)

    # --- Content opacity at Standard: same shape, different content ---
    a, _ = p5_standard_match(f"(shell {_q('ls -la')})", f"(shell {_q('rm -rf /')})")
    check("content-opaque-shell", a, True)

    # --- Standard catches structural change: string vs nested s-expr arg ---
    a, _ = p5_standard_match(f"(remember {_q('note')})",
                             "(remember (metta (match &self (a b) c)))")
    check("structural-change-caught", a, False)

    # --- Order independence, count sensitivity ---
    a, _ = p5_standard_match(f"(pin {_q('x')}) (send {_q('y')})",
                             f"(send {_q('y')}) (pin {_q('x')})")
    check("order-independent", a, True)
    a, _ = p5_standard_match(f"(pin {_q('x')})",
                             f"(pin {_q('x')}) (pin {_q('z')})")
    check("count-sensitive", a, False)

    # --- Non-skill top-level s-exprs ignored ---
    a, _ = p5_standard_match(f"(notaskill {_q('x')}) (pin {_q('y')})",
                             f"(pin {_q('y')})")
    check("non-skill-ignored", a, True)

    # --- Encoded apostrophe/newline inside a literal is opaque content ---
    a, _ = p5_standard_match(f"(send {_q('it' + '_apostrophe_' + 's fine')})",
                             f"(send {_q('hello' + '_newline_' + 'world')})")
    check("encoded-tokens-opaque-in-literal", a, True)

    # --- Multi-arg skill: (write-file "f" "contents") ---
    ts, _ = parse_typeshape(tokenize(f"(write-file {_q('f')} {_q('data')})"))
    check("write-file-two-args", ts,
          ("s-expr", ("symbol", "string-literal", "string-literal")))

    # --- ADDED per Clarity review 2026-05-26 ---

    # Malformed: unterminated string literal surfaces as difference, no crash.
    # (the opening _quote_ has no closing _quote_)
    try:
        a, _ = p5_standard_match(f"(send {QUOTE_TOK}unterminated",
                                 f"(send {_q('terminated')})")
        # Should not crash; unterminated still classifies as string-literal,
        # so type-shape matches (send <string-literal>) in both -> they match.
        # The point of the test is no-crash, not the match outcome.
        check("malformed-unterminated-no-crash", True, True)
    except Exception:
        check("malformed-unterminated-no-crash", False, True)

    # Malformed: unbalanced parens surface as difference, no crash.
    try:
        a, _ = p5_standard_match(f"(pin {_q('x')}",       # missing close paren
                                 f"(pin {_q('x')})")
        check("malformed-unbalanced-no-crash", True, True)
    except Exception:
        check("malformed-unbalanced-no-crash", False, True)

    # extract_invocations direct: mixed response (prose + skill + stray paren).
    # Only the real skill call should be extracted; prose and stray parens
    # ignored.
    mixed = (f"I will now remember this. (remember {_q('the note')}) "
             f"Here is some prose with a stray ) paren. "
             f"(notaskill {_q('ignored')})")
    invs = extract_invocations(mixed)
    check("extract-isolates-skill",
          invs, [("remember", ("string-literal",))])

    # Multi-skill same-name: two remember calls -> count 2 in the multiset.
    from collections import Counter
    ms = invocation_multiset(f"(remember {_q('a')}) (remember {_q('b')})")
    check("multi-same-name-count",
          ms, Counter({("remember", ("string-literal",)): 2}))

    # Report
    passed = sum(1 for _, ok, _, _ in results if ok)
    total = len(results)
    print(f"P-5 type-shape self-test: {passed}/{total} passed")
    for name, ok, got, want in results:
        status = "PASS" if ok else "FAIL"
        if ok:
            print(f"  [{status}] {name}")
        else:
            print(f"  [{status}] {name}\n          got:  {got}\n          want: {want}")
    return passed == total


if __name__ == "__main__":
    import sys
    sys.exit(0 if _selftest() else 1)
