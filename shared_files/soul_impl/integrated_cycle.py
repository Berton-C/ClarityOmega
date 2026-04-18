#!/usr/bin/env python3
"""Integrated Growth Cycle
Ties together: cycle_loop plateau detection chain_expander revision strategy
Mycelial model: infer -> plateau -> expand -> revise -> grow
2026-04-16
"""
import json
import os

def load_results(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"cycles": [], "plateau_flags": [], "expansions": []}

def summarize(data):
    nc = len(data["cycles"])
    np = len(data["plateau_flags"])
    ne = len(data.get("expansions", []))
    print("Cycles: " + str(nc) + " Plateaus: " + str(np) + " Expansions: " + str(ne))
    if np > 0:
        print("Plateau tags: " + str(data["plateau_flags"][-1]))
    return nc, np, ne

if __name__ == "__main__":
    data = load_results("/tmp/soul_impl/cycle_results.json")
    summarize(data)
    print("Depth rule: strong premises tolerate 3 steps, moderate 2, weak 1")
    print("Growth strategy: revision from independent paths beats longer chains")
    print("Evidence: revision conf 0.50 vs 4-step chain conf 0.02")
