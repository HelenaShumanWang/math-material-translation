#!/bin/bash
# restore_state.sh [code...]: after a container reset, bring back from the work-state branch what save_state.sh pushed:
# the corrections with their file times (the order they are applied in), the open flags, the pristine stage-1
# segments and QA report, the OCR cache and the afterword texts. The source PDFs come from Google Drive
# (common.DRIVE_IDS) into $BNU_WORK/books/<code>.pdf; the deliveries branch (the checked edition) is checked out at
# $BNU_DELIVERIES. Then apply_corrections.py <code> renders the volume as it stood.
set -e
W=${BNU_WORK:-/tmp/piptest/real}; ST=${BNU_STATE:-/tmp/piptest/state}; DL=${BNU_DELIVERIES:-/tmp/piptest/deliveries}
REPO="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$REPO" fetch -q origin work-state deliveries
[ -d "$ST" ] || git -C "$REPO" worktree add -q "$ST" work-state
[ -d "$DL" ] || git -C "$REPO" worktree add -q "$DL" deliveries
git -C "$ST" pull -q origin work-state || true
codes="$*"; [ -z "$codes" ] && codes="$(ls "$ST/proof")"
for c in $codes; do
  mkdir -p "$W/proof/$c" "$W/books/out_$c"
  cp "$ST"/proof/$c/corr_*.json "$ST"/proof/$c/flags_*.json "$W/proof/$c/" 2>/dev/null || true
  python3 - "$W/proof/$c" "$ST/proof/$c/times.json" <<'PY'
import json, os, sys
for name, t in json.load(open(sys.argv[2])).items():
    f = os.path.join(sys.argv[1], name)
    if os.path.exists(f):
        os.utime(f, (t, t))  # corrections are applied in file-time order
PY
  [ -f "$ST/proof/$c/segments_base.json.gz" ] && gunzip -c "$ST/proof/$c/segments_base.json.gz" > "$W/books/out_$c/segments_base.json"
  if [ -f "$ST/proof/$c/qa_report_base.json" ]; then
    cp "$ST/proof/$c/qa_report_base.json" "$W/books/out_$c/"
    [ -f "$W/books/out_$c/qa_report.json" ] || cp "$ST/proof/$c/qa_report_base.json" "$W/books/out_$c/qa_report.json"
  fi
  echo "$c: $(ls "$W/proof/$c"/corr_*.json 2>/dev/null | wc -l) correction files"
done
[ -d "$ST/ocr_cache" ] && mkdir -p "$W/ocr_cache" && cp -r "$ST/ocr_cache/." "$W/ocr_cache/"
[ -d "$ST/afterword" ] && mkdir -p "$W/afterword" && cp "$ST"/afterword/*.json "$W/afterword/" 2>/dev/null || true
echo "restored into $W; source PDFs: $(ls "$W"/books/*.pdf 2>/dev/null | wc -l) of 12 present"
