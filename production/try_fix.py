"""try_fix.py <code> <page,...> <corrections.json> [tag]: see what corrections would do before writing them. The file
holds {"corrections": [...]}; they are applied after all of the volume's own corrections on a scratch copy (nothing of
the volume is touched) and the pages (1-based) are rendered side by side with the source into
previews/try_<tag>_<code>_<page>.png. Prints what was applied or rejected and why."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import PREVIEWS, out_dir, proof_dir  # noqa: E402

code, pages, corr = sys.argv[1], sys.argv[2], sys.argv[3]
tag = "try_" + (sys.argv[4] if len(sys.argv) > 4 else str(os.getpid()))
work = PREVIEWS / f".{tag}_{code}_{os.getpid()}"  # one scratch folder per run: checkers often share a tag
shutil.rmtree(work, ignore_errors=True)
(work / "out").mkdir(parents=True)
(work / "proof").mkdir(parents=True)
base = out_dir(code) / "segments_base.json"
shutil.copy(base, work / "out" / "segments_base.json")
shutil.copy(out_dir(code) / "segments.json", work / "out" / "segments.json")
for f in proof_dir(code).glob("corr_*.json"):
    shutil.copy2(f, work / "proof" / f.name)  # copy2 keeps the file times: same order
shutil.copy(corr, work / "proof" / "corr_zzzz_try.json")  # newest: applied last
env = dict(os.environ, MT_OUT_DIR=str(work / "out"), MT_PROOF_DIR=str(work / "proof"), MT_PREVIEW_TAG=tag,
           PYTHONPATH=str(HERE.parent))
r = subprocess.run([sys.executable, str(HERE / "apply_corrections.py"), code, "--save-only"], env=env,
                   capture_output=True, text=True)
print("\n".join(line for line in r.stdout.splitlines() if "WARNING" not in line)[-400:],
      r.stderr[-1500:] if r.returncode else "")
a = json.load(open(work / "proof" / "applied.json"))
for x in a["applied"]:
    if x.get("file") == "corr_zzzz_try.json":
        print("applied:", json.dumps(x, ensure_ascii=False)[:200])
for x in a["rejected"]:
    if x.get("file") == "corr_zzzz_try.json":
        print("REJECTED:", json.dumps(x, ensure_ascii=False)[:240])
r = subprocess.run([sys.executable, str(HERE / "preview_pages.py"), code, pages, "--dpi", "110"], env=env,
                   capture_output=True, text=True)
print("\n".join(line for line in r.stdout.splitlines() if line.startswith("page")), r.stderr[-1500:] if r.returncode else "")
shutil.rmtree(work, ignore_errors=True)
