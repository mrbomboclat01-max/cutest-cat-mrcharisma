"""Kawaii tabby kitten — cutest-cat-01 entry. Copies the pre-rendered PNG to output."""
import os, shutil

src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
dst = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy2(src, dst)
