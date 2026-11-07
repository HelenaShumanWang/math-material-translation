"""Generate sample textbooks: python scripts/make_sample_pdf.py examples/sample_zh.pdf --lang zh"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mathtrans.samples import make_sample_pdf

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--lang", default="zh")
    a = ap.parse_args()
    print(make_sample_pdf(a.out, a.lang))
