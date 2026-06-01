#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen ảnh cho 20 cây mới (gia vị + lâm nghiệp đợt 2). Như gen-images-new.py.
Chạy: python3 scripts/gen-images-3.py"""
import os, subprocess, urllib.request, concurrent.futures as cf

BASE = os.path.join(os.path.dirname(__file__), '..')
IMG = os.path.join(BASE, 'img')
DET = os.path.join(IMG, 'detail')
os.makedirs(DET, exist_ok=True)

STYLE_T = ("Antique botanical illustration plate of {s}, on clean white background, "
           "vintage scientific watercolor engraving, 19th century botanical art, no text, no letters, no labels")
STYLE_D = ("Antique botanical illustration plate of {s}, full plant study showing roots, stem, leaves, "
           "flowers, fruit and cross-sections, detailed botanical study, vintage scientific watercolor and ink, "
           "19th century, clean white background, no text, no letters, no labels")

SUBJ = {
    "gung": "Zingiber officinale ginger, green lance-shaped leaves on reed-like stems, knobby beige rhizome with a cut section, small pale flower spike, roots",
    "nghe": "Curcuma longa turmeric, large oblong green leaves, cluster of pale flowers, bright orange rhizome cut open showing vivid color, roots",
    "sa": "Cymbopogon citratus lemongrass, dense clump of long narrow arching green blades with swollen pale stem bases, roots",
    "rieng": "Alpinia officinarum galangal, tall reed-like leafy stems, white flower spike, reddish-brown hard rhizome with a cut section, roots",
    "tia-to": "Perilla frutescens perilla, square stems, broad serrated leaves green above and purple beneath, small flower spikes",
    "hung-que": "Ocimum basilicum sweet basil, square stems, oval aromatic green leaves, spikes of small white flowers",
    "lim-xanh": "Erythrophleum fordii lim ironwood tree, bipinnate compound leaves, small flower spikes, flat woody seed pods, dense dark heartwood",
    "dinh": "Markhamia stipulata tree, pinnate compound leaves, large bell-shaped cream-yellow flowers, very long slender seed pods, hardwood",
    "tau": "Vatica odorata tau hardwood tree, leathery lance-shaped leaves, small flowers, winged nut fruit, hard yellow-brown heartwood",
    "sua": "Dalbergia tonkinensis rosewood tree, pinnate compound leaves, fragrant white flower clusters, flat pods, reddish fragrant heartwood cross-section",
    "cam-lai": "Dalbergia oliveri rosewood tree, pinnate compound leaves, small pale flowers, flat seed pods, pinkish-brown patterned heartwood cross-section",
    "go-do": "Afzelia xylocarpa tree, pinnate compound leaves, flower clusters, large woody pods with black seeds capped orange, reddish-brown heartwood",
    "vu-huong": "Cinnamomum balansae aromatic tree, glossy oval veined leaves, small flowers, small dark berries, fragrant pale wood",
    "mo": "Manglietia conifera tree, glossy lance-shaped leaves, magnolia-like cream flower, cone-like aggregate fruit, straight pale trunk",
    "bo-de": "Styrax tonkinensis tree, oval pointed leaves, drooping clusters of white bell-shaped flowers, round drupes, resin droplets on bark",
    "phi-lao": "Casuarina equisetifolia she-oak tree, drooping fine needle-like green branchlets, tiny cone-like woody fruits, rough bark, straight trunk",
    "luong": "Dendrocalamus barbatus giant bamboo, tall hollow jointed culms in a clump, long narrow leaves, a young bamboo shoot at the base",
    "xa-cu": "Khaya senegalensis African mahogany tree, pinnate compound glossy leaves, small flowers, round woody capsules splitting open, broad buttressed trunk",
    "muong-den": "Senna siamea cassia tree, pinnate compound leaves, clusters of bright yellow flowers, flat long seed pods, spreading crown",
    "thong-ba-la": "Pinus kesiya pine tree, slender needles in bundles of three, brown ovoid cones, straight trunk with furrowed bark",
}


def gen(out, ratio, prompt):
    if os.path.exists(out):
        return f"SKIP {os.path.basename(out)}"
    for attempt in (1, 2):
        try:
            r = subprocess.run(
                ["higgsfield", "generate", "create", "seedream_v4_5",
                 "--aspect_ratio", ratio, "--prompt", prompt, "--wait"],
                capture_output=True, text=True, timeout=300)
            url = (r.stdout or "").strip().splitlines()[-1].strip() if r.stdout.strip() else ""
            if url.startswith("http"):
                urllib.request.urlretrieve(url, out); subprocess.run(["sips","-s","format","jpeg","-s","formatOptions",("82" if "/detail/" in out else "80"),"-Z",("1100" if "/detail/" in out else "760"),out,"--out",out],capture_output=True)
                return f"OK   {os.path.basename(out)}"
        except Exception as e:
            if attempt == 2:
                return f"ERR  {os.path.basename(out)} :: {e}"
    return f"FAIL {os.path.basename(out)} :: {(r.stdout or r.stderr).strip()[:80]}"


def main():
    jobs = []
    for cid, s in SUBJ.items():
        jobs.append((os.path.join(IMG, cid + ".jpg"), "4:3", STYLE_T.format(s=s)))
        jobs.append((os.path.join(DET, cid + ".jpg"), "3:4", STYLE_D.format(s=s)))
    todo = [j for j in jobs if not os.path.exists(j[0])]
    print(f"Tổng {len(jobs)} ảnh, cần gen {len(todo)} (bỏ {len(jobs)-len(todo)} đã có).")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1
            print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    missing = [os.path.basename(j[0]) for j in jobs if not os.path.exists(j[0])]
    print("THIẾU:", missing) if missing else print("ĐỦ HẾT 40 ảnh.")


if __name__ == "__main__":
    main()
