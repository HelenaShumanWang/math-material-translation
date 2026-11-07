#!/bin/bash
# deliver.sh <code>: the English book (final.pdf, page 2 left out, English afterword) and its QA report onto the
# deliveries branch (worktree $BNU_DELIVERIES, default /tmp/piptest/deliveries), committed and pushed; then a compact
# copy (< 29.5 MiB) for chat in $BNU_WORK/deliver/.
set -e -o pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
code=$1
W=${BNU_WORK:-/tmp/piptest/real}; D=${BNU_DELIVERIES:-/tmp/piptest/deliveries}
pdf="$(cd "$HERE" && python3 -c "import common; print(common.pdf_name('$code'))")"
rep="$(cd "$HERE" && python3 -c "import common; print(common.report_name('$code'))")"
zh="$(cd "$HERE" && python3 -c "import common; print(common.TITLES['$code'])")"
python3 "$HERE/strip_page2.py" "$code"
mkdir -p "$W/deliver"
python3 "$HERE/compact_pdf.py" "$W/books/out_$code/final.pdf" "$W/deliver/$pdf" 29.5
[ "${DELIVER_PUSH:-1}" = "0" ] && exit 0
cp "$W/books/out_$code/final.pdf" "$D/$pdf"; mkdir -p "$D/reports"; cp "$W/books/out_$code/qa_report.md" "$D/reports/$rep"
cd "$D"
git add -A && git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -qm "Deliver $zh ($code): translated PDF and QA report

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B7Tm5LrnqNnbUvNPjKGh7w" || true
for try in 1 2 3 4; do git push -q origin deliveries && break; echo "push retry $try"; sleep $((2**try)); done
git log --oneline -1
