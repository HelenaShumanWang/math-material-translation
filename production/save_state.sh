#!/bin/bash
# save_state.sh [code...]: push what a run cannot rebuild cheaply to the work-state branch (worktree
# $BNU_STATE, default /tmp/piptest/state): every volume's corrections (proof/<code>/corr_*.json, file times kept in
# times.json), its pristine segments (gzip), the OCR cache and the afterword texts.
set -e
W=${BNU_WORK:-/tmp/piptest/real}; ST=${BNU_STATE:-/tmp/piptest/state}
REPO="$(cd "$(dirname "$0")/.." && pwd)"
if [ ! -d "$ST" ]; then
  git -C "$REPO" fetch -q origin work-state 2>/dev/null && git -C "$REPO" worktree add -q "$ST" work-state \
    || { git -C "$REPO" worktree add -q --detach "$ST" && git -C "$ST" checkout -q --orphan work-state && git -C "$ST" rm -rq . 2>/dev/null || true; }
fi
codes="$*"; [ -z "$codes" ] && codes="$(ls "$W/proof" 2>/dev/null)"
for c in $codes; do
  mkdir -p "$ST/proof/$c"
  cp -p "$W"/proof/$c/corr_*.json "$ST/proof/$c/" 2>/dev/null || true
  python3 - "$W/proof/$c" "$ST/proof/$c/times.json" <<'PY'
import json, os, sys, glob
json.dump({os.path.basename(f): os.path.getmtime(f) for f in glob.glob(sys.argv[1] + "/corr_*.json")}, open(sys.argv[2], "w"), indent=0)
PY
  [ -f "$W/books/out_$c/segments_base.json" ] && gzip -c "$W/books/out_$c/segments_base.json" > "$ST/proof/$c/segments_base.json.gz"
  [ -f "$W/books/out_$c/qa_report_base.json" ] && cp "$W/books/out_$c/qa_report_base.json" "$ST/proof/$c/"
done
[ -d "$W/ocr_cache" ] && mkdir -p "$ST/ocr_cache" && cp -r "$W/ocr_cache/." "$ST/ocr_cache/"
[ -d "$W/afterword" ] && mkdir -p "$ST/afterword" && cp "$W"/afterword/*.json "$ST/afterword/" 2>/dev/null || true
cd "$ST"
git add -A
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "Work state: corrections of $codes

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B7Tm5LrnqNnbUvNPjKGh7w" || { echo "nothing new"; exit 0; }
for try in 1 2 3 4; do git push -q -u origin work-state && break; sleep $((2**try)); done
echo "state saved: $(git log --oneline -1 | cut -c1-60)"
