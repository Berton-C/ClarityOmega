#!/usr/bin/env python3
"""
Patch Corner-Gate v3 from failed A.4/B.2 to corrected A.5/B.3.

Run from the ClarityOmega repository root:

    python3 staging/patch_corner_gate_v3_a5_b3.py

This script:
- applies the proven tagged-list correction to coupling-known-heads;
- updates the installer and validator frozen pure-payload identity;
- verifies the frozen writers/helper payload identities;
- syntax-checks the Python tooling;
- creates or refreshes the authoritative A.5/B.3 payload manifest;
- creates timestamped backups outside the repository under /tmp.

It does NOT:
- apply v3 to the live repository;
- rebuild an image;
- start or restart a container;
- stage or commit files.

The script is idempotent and fail-closed.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
from pathlib import Path
import py_compile
import shutil


OLD_PURE_HASH = (
    "3a2764428e43c9a96ec1a90066e442e0f9af8f03b450c46271f46c5742852347"
)
NEW_PURE_HASH = (
    "0665131e1491bced69a8ab3e5870637a6a9757b45375fee3095d17ade540cc81"
)
WRITERS_HASH = (
    "50662dc45167fa044bec280d4da47f6f67dafaf8c10f7e6ce9c8a7a65ecfc940"
)
HELPER_HASH = (
    "de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54"
)

OLD_DEFINITION = """(= (coupling-known-heads)
   (write-file append-file shell remember read-file query episodes metta
    send pin search tavily-search technical-analysis))"""

NEW_DEFINITION = """(= (coupling-known-heads)
   (let $tagged
        (coupling-known-heads-data
          write-file append-file shell remember read-file query episodes metta
          send pin search tavily-search technical-analysis)
     (cdr-atom $tagged)))"""


def refuse(message: str) -> None:
    raise SystemExit(f"REFUSE: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_file(root: Path, path: Path) -> None:
    if not path.is_file():
        refuse(f"missing required file: {path.relative_to(root)}")


def backup_files(root: Path, paths: list[Path]) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path("/tmp/cg-v3-a5-b3") / f"patch-backup-{stamp}"
    backup_root.mkdir(parents=True, exist_ok=False)

    for path in paths:
        if not path.exists():
            continue
        relative = path.relative_to(root)
        destination = backup_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

    print(f"BACKUP  {backup_root}")
    return backup_root


def patch_payload(root: Path, pure: Path) -> None:
    text = pure.read_text()

    old_count = text.count(OLD_DEFINITION)
    new_count = text.count(NEW_DEFINITION)

    if old_count == 1 and new_count == 0:
        pure.write_text(text.replace(OLD_DEFINITION, NEW_DEFINITION))
        print(f"PATCHED {pure.relative_to(root)}")
    elif old_count == 0 and new_count == 1:
        print(f"PRESENT {pure.relative_to(root)}")
    else:
        refuse(
            "ambiguous coupling-known-heads state: "
            f"old_definition_count={old_count}, "
            f"new_definition_count={new_count}"
        )

    actual = sha256(pure)
    if actual != NEW_PURE_HASH:
        refuse(
            "corrected pure payload hash mismatch:\n"
            f"expected {NEW_PURE_HASH}\n"
            f"actual   {actual}"
        )

    print(f"PASS    pure payload identity {actual}")


def patch_hash_reference(root: Path, path: Path) -> None:
    text = path.read_text()
    old_count = text.count(OLD_PURE_HASH)
    new_count = text.count(NEW_PURE_HASH)

    if old_count == 1 and new_count == 0:
        text = text.replace(OLD_PURE_HASH, NEW_PURE_HASH)
        print(f"PATCHED {path.relative_to(root)} payload identity")
    elif old_count == 0 and new_count >= 1:
        print(f"PRESENT {path.relative_to(root)} A.5 identity")
    else:
        refuse(
            f"ambiguous payload identity state in {path.relative_to(root)}: "
            f"old_hash_count={old_count}, new_hash_count={new_count}"
        )

    replacements = {
        "FROZEN A.4 PAYLOAD IDENTITY":
            "FROZEN A.5 CANDIDATE PAYLOAD IDENTITY",
        "Payload A.4": "Payload A.5",
        "PAYLOAD A.4": "PAYLOAD A.5",
        "Step B.2": "Step B.3",
        "STEP B.2": "STEP B.3",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    path.write_text(text)

    if OLD_PURE_HASH in text:
        refuse(f"old A.4 identity remains in {path.relative_to(root)}")
    if NEW_PURE_HASH not in text:
        refuse(f"A.5 identity missing from {path.relative_to(root)}")


def verify_frozen_payloads(writers: Path, helper: Path) -> None:
    writers_actual = sha256(writers)
    helper_actual = sha256(helper)

    if writers_actual != WRITERS_HASH:
        refuse(
            "writers payload changed unexpectedly:\n"
            f"expected {WRITERS_HASH}\n"
            f"actual   {writers_actual}"
        )

    if helper_actual != HELPER_HASH:
        refuse(
            "helper payload changed unexpectedly:\n"
            f"expected {HELPER_HASH}\n"
            f"actual   {helper_actual}"
        )

    print(f"PASS    writers payload identity {writers_actual}")
    print(f"PASS    helper payload identity  {helper_actual}")


def syntax_check(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_file():
            continue
        py_compile.compile(str(path), doraise=True)
        print(f"PASS    Python syntax {path}")


def write_manifest(
    root: Path,
    manifest: Path,
    artifacts: dict[str, Path],
) -> None:
    identities = {
        name: sha256(path)
        for name, path in artifacts.items()
        if path.is_file()
    }

    identity_lines = "\n".join(
        f"{digest}  {name}"
        for name, digest in identities.items()
    )

    manifest_text = f"""# Corner-Gate v3 Coupling-Legibility Payload Manifest

**Payload revision:** A.5  
**Installation revision:** B.3  
**Status:** RATIFICATION CANDIDATE  
**Date:** 2026-07-12

## Corrective change

A.4 placed the callable symbol `write-file` in the head position of an
expression intended as list data. The production transpiler interpreted the
expression as a function invocation and aborted payload compilation.

A.5 uses an inert tag and removes it with `cdr-atom`:

```metta
{NEW_DEFINITION}
```

This returns the exact original known-command list while preventing callable
head interpretation.

## Frozen artifact identities

```text
{identity_lines}
```

## Required pre-apply commands

```bash
python3 staging/apply_corner_gate_v3_monolith.py \\
  --repo-root . \\
  --dry-run

python3 staging/validate_corner_gate_v3_candidate_closure.py \\
  --repo-root . \\
  --image clarityomega-clarityclaw:latest \\
  --platform linux/amd64 \\
  --evidence-log /tmp/cg-v3-a5-b3/evidence/v3_candidate_import_closure.log
```

## Apply command

```bash
python3 staging/apply_corner_gate_v3_monolith.py \\
  --repo-root . \\
  --apply
```

## Reverse command

```bash
python3 staging/apply_corner_gate_v3_monolith.py \\
  --repo-root . \\
  --reverse \\
  --apply
```

## Required semantic results

```text
schema                     v3-18-field
write-file surface         runtime-output
write-file command class   action-class
unknown-head surface       no-contact
unknown-head class         neutral
```

The exact known-head list remains:

```text
(write-file append-file shell remember read-file query episodes metta
 send pin search tavily-search technical-analysis)
```

The candidate validator must also prove that `gate-aware-results` appends a
ground `COUPLING-STATE-LINE` while preserving `probe-result`.

## Evidence basis

See:

```text
CG3_RUNTIME_CRASH_INVESTIGATION.md
evidence/
```
"""

    manifest.write_text(manifest_text)
    print(f"WROTE   {manifest.relative_to(root)}")

    written = manifest.read_text()
    for name, digest in identities.items():
        expected = f"{digest}  {name}"
        if expected not in written:
            refuse(f"manifest missing exact identity: {expected}")
        print(f"PASS    manifest identity {name}")


def main() -> None:
    root = Path.cwd().resolve()

    if not (root / ".git").is_dir():
        refuse("run this script from the ClarityOmega repository root")

    pure = root / "docs/sprints/01_corner_gate_v3/coupling_legibility.metta"
    writers = (
        root
        / "docs/sprints/01_corner_gate_v3/"
          "coupling_legibility_writers.metta"
    )
    helper = (
        root
        / "docs/sprints/01_corner_gate_v3/"
          "coupling_legibility_helper_payload.py"
    )
    manifest = (
        root
        / "docs/sprints/01_corner_gate_v3/"
          "coupling_legibility_payload_manifest.md"
    )
    installer = root / "staging/apply_corner_gate_v3_monolith.py"
    validator = root / "staging/validate_corner_gate_v3_monolith.py"
    candidate_validator = (
        root / "staging/validate_corner_gate_v3_candidate_closure.py"
    )
    patcher = root / "staging/patch_corner_gate_v3_a5_b3.py"

    for path in [pure, writers, helper, installer, validator]:
        require_file(root, path)

    backup_files(root, [pure, installer, validator, manifest])

    patch_payload(root, pure)
    verify_frozen_payloads(writers, helper)
    patch_hash_reference(root, installer)
    patch_hash_reference(root, validator)

    syntax_check([installer, validator, candidate_validator, patcher])

    artifacts = {
        "coupling_legibility.metta": pure,
        "coupling_legibility_writers.metta": writers,
        "coupling_legibility_helper_payload.py": helper,
        "apply_corner_gate_v3_monolith.py": installer,
        "validate_corner_gate_v3_monolith.py": validator,
        "validate_corner_gate_v3_candidate_closure.py":
            candidate_validator,
        "patch_corner_gate_v3_a5_b3.py": patcher,
    }

    write_manifest(root, manifest, artifacts)

    print("=" * 72)
    print("A.5/B.3 PATCH COMPLETE")
    print("No live apply, rebuild, restart, staging, or commit was performed.")
    print()
    print("NEXT:")
    print(
        "  python3 staging/apply_corner_gate_v3_monolith.py "
        "--repo-root . --dry-run"
    )
    print(
        "  python3 staging/validate_corner_gate_v3_candidate_closure.py "
        "--repo-root . --image clarityomega-clarityclaw:latest "
        "--platform linux/amd64 "
        "--evidence-log "
        "/tmp/cg-v3-a5-b3/evidence/v3_candidate_import_closure.log"
    )
    print(
        "  python3 staging/apply_corner_gate_v3_monolith.py "
        "--repo-root . --apply"
    )


if __name__ == "__main__":
    main()
