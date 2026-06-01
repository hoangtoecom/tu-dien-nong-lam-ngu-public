#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen 50 ảnh CHI TIẾT (3:4) cho các loài mới — ngang chất với ảnh detail của cây cũ.
Cây = bản nghiên cứu bộ phận; con vật = bản đa góc nhìn; côn trùng = vòng đời.
Tái dùng mô tả loài từ 2 script gen trước. python3 scripts/gen-images-detail-50.py"""
import os, subprocess, urllib.request, importlib.util, concurrent.futures as cf
SC = os.path.dirname(__file__); BASE = os.path.join(SC, '..')
DET = os.path.join(BASE, 'img', 'detail'); os.makedirs(DET, exist_ok=True)

def load(fname):
    spec = importlib.util.spec_from_file_location('m_'+fname.replace('-','_').replace('.py',''), os.path.join(SC, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
r1 = load('gen-images-nong-lam-ngu.py')   # SUBJ: 20 con vật/thủy sản (đợt 1)
r2 = load('gen-images-expand-150.py')      # PLANTS: 10 cây | ANIMALS: 20 con vật/thủy sản (đợt 2)

PLANTS = dict(r2.PLANTS)                       # 10 cây
ANIMALS = {**r1.SUBJ, **r2.ANIMALS}            # 40 con vật/thủy sản
LIFECYCLE = {"ong-mat", "tam", "de-men", "trun-que"}  # côn trùng/giun → vòng đời

P_DETAIL = ("Antique botanical illustration plate of {s}, full plant study showing roots, stem, leaves, "
            "flowers, fruit and cross-sections, detailed botanical study, vintage scientific watercolor and ink, "
            "19th century, clean white background, no text, no letters, no labels")
A_DETAIL = ("Antique zoological illustration plate of {s}, detailed natural history study showing the full animal "
            "together with smaller secondary studies of the head and distinctive features, vintage scientific "
            "watercolor and ink engraving, 19th century, clean white background, no text, no letters, no labels")
L_DETAIL = ("Antique zoological illustration plate of {s}, life-cycle and anatomy study showing several stages "
            "and body details, vintage scientific watercolor and ink, 19th century, clean white background, "
            "no text, no letters, no labels")

def gen(out, prompt):
    if os.path.exists(out): return f"SKIP {os.path.basename(out)}"
    for a in (1, 2):
        try:
            r = subprocess.run(["higgsfield","generate","create","seedream_v4_5","--aspect_ratio","3:4","--prompt",prompt,"--wait"],
                               capture_output=True, text=True, timeout=300)
            url = (r.stdout or "").strip().splitlines()[-1].strip() if r.stdout.strip() else ""
            if url.startswith("http"): urllib.request.urlretrieve(url, out); subprocess.run(["sips","-s","format","jpeg","-s","formatOptions",("82" if "/detail/" in out else "80"),"-Z",("1100" if "/detail/" in out else "760"),out,"--out",out],capture_output=True); return f"OK   {os.path.basename(out)}"
        except Exception as e:
            if a == 2: return f"ERR  {os.path.basename(out)} :: {e}"
    return f"FAIL {os.path.basename(out)}"

def main():
    jobs = []
    for cid, s in PLANTS.items():
        jobs.append((os.path.join(DET, cid+".jpg"), P_DETAIL.format(s=s)))
    for cid, s in ANIMALS.items():
        tpl = L_DETAIL if cid in LIFECYCLE else A_DETAIL
        jobs.append((os.path.join(DET, cid+".jpg"), tpl.format(s=s)))
    print(f"Gen {len(jobs)} ảnh chi tiết (3:4)...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")

if __name__ == "__main__":
    main()
