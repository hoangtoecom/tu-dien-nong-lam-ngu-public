#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen visual editorial cho UI: hero lớn + 4 feature + 2 lĩnh vực.
Style: botanical encyclopedia, watercolor & ink, warm cream. python3 scripts/gen-visuals.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); UI = os.path.join(BASE, 'img', 'ui')
os.makedirs(UI, exist_ok=True)
BASE_STYLE = ("vintage botanical encyclopedia editorial illustration, watercolor and ink, "
              "warm cream paper background, muted forest green and brass gold palette, soft shadows, "
              "elegant and detailed, no text, no letters, no labels, no words")
JOBS = [
  ("hero.jpg", "16:9",
   "A grand frontispiece scene of Vietnamese flora: in the foreground lush rice stalks, a coffee branch with red cherries and a ripe fruit, midground terraced green fields, background forested hills with tall trees and soft mist, "+BASE_STYLE),
  ("feature-1.jpg", "4:3",
   "An open botanical herbarium journal showing a pressed plant specimen, a magnifying glass and a small branching taxonomy diagram, study desk still life, "+BASE_STYLE),
  ("feature-2.jpg", "4:3",
   "A healthy young potted plant with a glowing sun, a water droplet and visible soil layers with roots around it, illustrating growing conditions, "+BASE_STYLE),
  ("feature-3.jpg", "4:3",
   "A left-to-right growth sequence of a seed sprouting into a seedling then a mature flowering plant, with a small calendar and simple farming tools, "+BASE_STYLE),
  ("feature-4.jpg", "4:3",
   "A woven harvest basket full of fruits and grains beside two apothecary jars and an open book, abundance and knowledge still life, "+BASE_STYLE),
  ("linhvuc-nong.jpg", "16:9",
   "A serene Vietnamese farmland panorama: rice paddies, vegetable plots and fruit trees under a soft sky, a conical hat resting on a fence, agriculture, "+BASE_STYLE),
  ("linhvuc-lam.jpg", "16:9",
   "A lush Vietnamese forest panorama: tall hardwood and pine trees on layered hills, ferns below, soft mist between trunks, forestry, "+BASE_STYLE),
]
def gen(out, ratio, prompt):
    if os.path.exists(out): return f"SKIP {os.path.basename(out)}"
    for a in (1, 2):
        try:
            r = subprocess.run(["higgsfield","generate","create","seedream_v4_5","--aspect_ratio",ratio,"--prompt",prompt,"--wait"],
                               capture_output=True, text=True, timeout=300)
            url = (r.stdout or "").strip().splitlines()[-1].strip() if r.stdout.strip() else ""
            if url.startswith("http"): urllib.request.urlretrieve(url, out); subprocess.run(["sips","-s","format","jpeg","-s","formatOptions",("82" if "/detail/" in out else "80"),"-Z",("1100" if "/detail/" in out else "760"),out,"--out",out],capture_output=True); return f"OK   {os.path.basename(out)}"
        except Exception as e:
            if a == 2: return f"ERR  {os.path.basename(out)} :: {e}"
    return f"FAIL {os.path.basename(out)}"
def main():
    print(f"Gen {len(JOBS)} visual...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=7) as ex:
        futs = {ex.submit(gen, os.path.join(UI, n), r, p): n for n, r, p in JOBS}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(JOBS)}] {fu.result()}", flush=True)
    miss = [n for n, r, p in JOBS if not os.path.exists(os.path.join(UI, n))]
    print("THIẾU:", miss) if miss else print("ĐỦ visual.")
if __name__ == "__main__": main()
