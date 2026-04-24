#!/bin/bash
# run_nal.sh - Run NAL inference via MeTTa externally
# Usage: bash run_nal.sh 'premise1' 'premise2'
# This bypasses the outer S-expression parser
echo "!(|- ($1) ($2))" | metta --repl 2>&1 || echo "METTA_NOT_AVAILABLE_AS_CLI"