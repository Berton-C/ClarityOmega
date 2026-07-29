#!/usr/bin/env python3
"""
Corner-Gate v3 A.5 / B.3 disposable candidate-import closure.

This validator:
  1. Creates a temporary repository containing only the installer targets.
  2. Applies the candidate installer inside that temporary repository.
  3. Mounts the resulting candidate soul, manifest, helper, and loop files
     over the existing production image.
  4. Runs a one-shot production import probe.
  5. Never changes the live repository or live container.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


PURE_HASH = "0665131e1491bced69a8ab3e5870637a6a9757b45375fee3095d17ade540cc81"
WRITERS_HASH = "50662dc45167fa044bec280d4da47f6f67dafaf8c10f7e6ce9c8a7a65ecfc940"
HELPER_HASH = "de3183e1f3504e2201d6ef80ec6e6650534b80d491e4df7efa38a099f1e87e54"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    capture: bool = True,
) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command))
    return subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        check=False,
    )


def require(condition: bool, message: str, detail: str = "") -> None:
    if condition:
        print(f"PASS  {message}")
        return

    print(f"FAIL  {message}")
    if detail:
        print(detail)
    raise SystemExit(1)


def copy_file(root: Path, temp_root: Path, relative: str) -> None:
    source = root / relative
    destination = temp_root / relative

    require(source.is_file(), f"source exists: {relative}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_tree(root: Path, temp_root: Path, relative: str) -> None:
    source = root / relative
    destination = temp_root / relative

    require(source.is_dir(), f"source directory exists: {relative}")

    shutil.copytree(source, destination, dirs_exist_ok=True)


def final_values(output: str) -> list[str]:
    """Return non-transpiler result lines from the tail of one-shot output."""
    values: list[str] = []

    for raw in output.splitlines():
        line = raw.strip()

        if not line:
            continue

        if line.startswith((
            "-->",
            ":- ",
            "^^^^^^^^",
            "Not specialized ",
        )):
            continue

        values.append(line)

    return values[-30:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--image",
        default="clarityomega-clarityclaw:latest",
    )
    parser.add_argument("--platform", default="linux/amd64")
    parser.add_argument(
        "--evidence-log",
        default="/tmp/cg-v3-a5-b3/evidence/v3_candidate_import_closure.log",
    )
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()

    require(
        sha256(root / "docs/sprints/01_corner_gate_v3/coupling_legibility.metta")
        == PURE_HASH,
        "A.5 pure payload identity",
    )
    require(
        sha256(
            root
            / "docs/sprints/01_corner_gate_v3/"
              "coupling_legibility_writers.metta"
        )
        == WRITERS_HASH,
        "writers payload identity",
    )
    require(
        sha256(
            root
            / "docs/sprints/01_corner_gate_v3/"
              "coupling_legibility_helper_payload.py"
        )
        == HELPER_HASH,
        "helper payload identity",
    )

    with tempfile.TemporaryDirectory(prefix="cg3-a5-candidate-") as temp:
        candidate = Path(temp) / "repo"
        candidate.mkdir(parents=True)

        # Mirror the complete repository areas used by the installer and
        # production import chain. The disposable repository must preserve
        # the real layout and all installer preflight dependencies.
        for relative in (
            "docs",
            "lib_clarity_reasoning",
            "src",
            "staging",
            "soul",
        ):
            copy_tree(root, candidate, relative)

        apply = run(
            [
                sys.executable,
                "staging/apply_corner_gate_v3_monolith.py",
                "--repo-root",
                ".",
                "--apply",
            ],
            cwd=candidate,
        )

        require(
            apply.returncode == 0,
            "candidate installer applies in disposable repository",
            apply.stdout or "",
        )

        probe = candidate / "probe-candidate-import.metta"
        probe.write_text(
            """!(import! &self (library lib_import))
!(git-import! "https://github.com/asi-alliance/omegaClaw-Core.git")
!(import! &self (library omegaclaw lib_omegaclaw))

!(coupling-legibility-schema-version)
!(coupling-known-heads)
!(surface-for-head-total write-file)
!(command-class-of-total write-file)
!(surface-for-head-total unknown-head)
!(command-class-of-total unknown-head)
!(coupling-legibility-line)
!(gate-aware-results (RESULTS: (probe-result)))
"""
        )

        command = [
            "docker",
            "run",
            "--rm",
            "--platform",
            args.platform,
            "--entrypoint",
            "sh",
            "-v",
            f"{candidate / 'soul'}:/PeTTa/repos/omegaclaw/soul:ro",
            "-v",
            (
                f"{candidate / 'lib_clarity_reasoning/lib_clarity_reasoning.metta'}:"
                "/PeTTa/repos/omegaclaw/lib_clarity_reasoning/"
                "lib_clarity_reasoning.metta:ro"
            ),
            "-v",
            (
                f"{candidate / 'src/helper.py'}:"
                "/PeTTa/repos/omegaclaw/src/helper.py:ro"
            ),
            "-v",
            (
                f"{probe}:"
                "/PeTTa/probe-candidate-import.metta:ro"
            ),
            args.image,
            "/PeTTa/run.sh",
            "/PeTTa/probe-candidate-import.metta",
        ]

        result = run(command)
        output = result.stdout or ""

        evidence = Path(args.evidence_log).expanduser().resolve()
        evidence.parent.mkdir(parents=True, exist_ok=True)
        evidence.write_text(output)

        require(
            result.returncode == 0,
            "disposable one-shot process exits cleanly",
            output[-1200:],
        )

        forbidden = (
            "Unknown procedure",
            "not_less_than_zero",
            "Domain error",
            "Syntax error",
            "syntax error",
            "Parse error",
            "parse error",
        )

        require(
            not any(token in output for token in forbidden),
            "no unresolved/compiler failure",
            output[-1200:],
        )

        tail = final_values(output)
        joined = "\n".join(tail)

        expected_list = (
            "(write-file append-file shell remember read-file query "
            "episodes metta send pin search tavily-search "
            "technical-analysis)"
        )

        require("v3-18-field" in tail, "schema version result")
        require(expected_list in tail, "exact known-head list result")
        require("runtime-output" in tail, "write-file surface result")
        require("action-class" in tail, "write-file class result")
        require("no-contact" in tail, "unknown-head surface result")
        require("neutral" in tail, "unknown-head class result")

        coupling_lines = [
            value for value in tail
            if value.startswith("COUPLING-STATE: contact ")
        ]

        require(
            len(coupling_lines) == 1,
            "one ground COUPLING-STATE result",
            joined,
        )
        require(
            "$" not in coupling_lines[0]
            and "(Error" not in coupling_lines[0]
            and "unreduced" not in coupling_lines[0],
            "COUPLING-STATE result is ground",
            coupling_lines[0],
        )

        result_lines = [
            value for value in tail
            if value.startswith("(RESULTS:")
        ]

        require(
            len(result_lines) == 1
            and "(COUPLING-STATE-LINE " in result_lines[0]
            and "probe-result" in result_lines[0],
            "gate appends coupling line and preserves probe-result",
            joined,
        )

        print("=" * 72)
        print("A.5/B.3 DISPOSABLE CANDIDATE CLOSURE: PASS")
        print(f"Evidence: {evidence}")


if __name__ == "__main__":
    main()
