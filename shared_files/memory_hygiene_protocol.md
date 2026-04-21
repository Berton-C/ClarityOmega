# Memory Hygiene Protocol

## Problem
Duplicate memories degrade retrieval by flooding results with identical entries.

## Prevention Rules
1. Before any remember call, query for the core phrase first
2. Only remember if the new entry adds genuine novelty
3. Never remember inside a retry loop without dedup check

## Remediation
- Store CANONICAL SUPERSEDES marker entries
- Old duplicates persist but lose relevance as canonical entries accumulate
- No delete skill exists so pollution is permanent but dilutable
