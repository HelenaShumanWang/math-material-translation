#!/bin/bash
# cycle.sh <code>: apply all corrections and re-render, then the English book and its compact copy (pushed to the
# deliveries branch unless DELIVER_PUSH=0), then a fresh proof pack, then save the corrections (save_state.sh).
set -e -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
code=$1
export PYTHONPATH="$(dirname "$HERE")"
python3 "$HERE/apply_corrections.py" "$code" 2>&1 | grep -v WARNING | tail -3
bash "$HERE/deliver.sh" "$code"
python3 "$HERE/make_proof_pack.py" "$code"
bash "$HERE/save_state.sh" "$code" || echo "state not saved"
