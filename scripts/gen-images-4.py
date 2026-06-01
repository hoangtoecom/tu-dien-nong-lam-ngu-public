#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen ảnh cho 10 cây mới (đợt 100 loài). python3 scripts/gen-images-4.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img'); DET = os.path.join(IMG, 'detail')
os.makedirs(DET, exist_ok=True)
ST = ("Antique botanical illustration plate of {s}, on clean white background, vintage scientific "
      "watercolor engraving, 19th century botanical art, no text, no letters, no labels")
SD = ("Antique botanical illustration plate of {s}, full plant study showing roots, stem, leaves, flowers, "
      "fruit and cross-sections, detailed botanical study, vintage scientific watercolor and ink, 19th century, "
      "clean white background, no text, no letters, no labels")
SUBJ = {
  "dua-hau": "Citrullus lanatus watermelon, sprawling vine with lobed leaves and tendrils, yellow flowers, large round green striped melon, cross-section with red flesh and black seeds",
  "dua-gang": "Cucumis melo Vietnamese melon, trailing vine with lobed leaves and tendrils, yellow flowers, elongated pale yellow-green melon, cross-section",
  "dau-tay": "Fragaria ananassa strawberry plant, low rosette of trifoliate serrated leaves, white five-petal flowers, red strawberries with tiny seeds, runners and roots",
  "dau-tam": "Morus alba mulberry branch, serrated heart-shaped leaves, small flowers, clusters of dark purple-black mulberry fruits",
  "bi-xanh": "Benincasa hispida wax gourd winter melon, climbing vine with large lobed leaves and tendrils, yellow flowers, long pale green waxy fruit with white bloom, cross-section",
  "cu-den": "Beta vulgaris beetroot, rosette of dark green leaves with red veins, deep red-purple round root below ground, fine roots",
  "do-bau": "Aquilaria crassna agarwood tree, slender trunk, oval glossy leaves, small white flowers, dark resin-soaked agarwood heartwood pieces",
  "ko-nia": "Irvingia malayana wild almond tree, large rounded crown, oblong glossy leaves, small flowers, green ovoid fruit with a hard nut kernel, sturdy trunk",
  "bang-lang": "Lagerstroemia speciosa pride of India tree, oblong leaves, large clusters of crinkled purple flowers, round woody seed capsules, smooth bark",
  "long-nao": "Cinnamomum camphora camphor tree, glossy oval aromatic leaves with three veins, small flowers, small dark berries, broad trunk with pale aromatic wood",
}
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
    jobs = []
    for cid, s in SUBJ.items():
        jobs.append((os.path.join(IMG, cid+".jpg"), "4:3", ST.format(s=s)))
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", SD.format(s=s)))
    print(f"Gen {len(jobs)} ảnh...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    miss = [os.path.basename(j[0]) for j in jobs if not os.path.exists(j[0])]
    print("THIẾU:", miss) if miss else print("ĐỦ 20 ảnh.")
if __name__ == "__main__": main()
