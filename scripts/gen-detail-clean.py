#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regen detail động vật/cá BỎ cận cảnh phụ (móng/sừng hay dị dạng) → con vật full-body tô màu đủ.
Sửa loài ốc bươu (tròn globular), chạch lấu, cá chẽm. python3 scripts/gen-detail-clean.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img'); DET = os.path.join(IMG, 'detail')

# DETAIL 3:4 — con vật full-body, KHÔNG cận cảnh bộ phận (tránh dị dạng)
DETAIL_T = ("Vintage scientific watercolor illustration of {s}, the complete animal fully painted in rich natural "
            "color, shown large and detailed in full-body side profile, single species on a pure flat white background, "
            "NO close-up of feet or horns or head, NO anatomical inset, NO deformed body parts, no text, no labels, "
            "not a sketch, accurate to the real species")
# THUMB 4:3 — 1 con, nền trắng tinh
THUMB_T = ("Vintage scientific watercolor illustration of {s}, fully painted in rich natural color, single specimen "
           "isolated on a pure flat solid white background, no border, no frame, no text, accurate to the real species, not a sketch")

# 21 detail (giữ loài) — con vật/cá
DETAIL_SUBJ = {
 "bo-sua":"Holstein Friesian dairy cow, black and white patches, prominent udder",
 "trau":"Vietnamese water buffalo, dark grey hide, large swept-back curved horns",
 "lon":"domestic pig, pink body, short legs, curly tail",
 "de":"domestic goat, short coat, curved horns and beard",
 "bo-thit":"Vietnamese yellow beef cattle, tan-brown coat, short horns",
 "cuu":"Phan Rang sheep, woolly fleece, curled horns",
 "ga":"a rooster and a hen, red comb, colorful tail feathers",
 "vit":"domestic duck, white plumage, orange bill and feet",
 "ngan":"Muscovy duck, black and white plumage, red facial caruncles",
 "chim-cut":"Japanese quail, plump brown speckled bird",
 "bo-cau":"domestic pigeon, grey plumage, iridescent neck",
 "ga-tay":"domestic turkey, fanned tail, red wattled head, bronze plumage",
 "da-dieu":"ostrich, black-and-white plumage, long bare neck and legs",
 "tho":"domestic rabbit, long ears, soft fur, sitting",
 "ca-tra":"Pangasius hypophthalmus striped catfish, silvery elongated body with barbels",
 "ca-basa":"Pangasius bocourti basa catfish, plump silvery body with barbels",
 "ca-mang":"Chanos chanos milkfish, streamlined silvery body, deeply forked tail",
 "ca-hong-my":"Sciaenops ocellatus red drum, reddish-bronze body with a black spot near the tail",
 "ca-ro-phi":"Oreochromis niloticus Nile tilapia, deep grey-olive body with faint vertical bars",
 "ech":"Hoplobatrachus rugulosus rice-field frog, mottled green and brown",
}
# loài SỬA (thumb + detail)
SPECIES = {
 "ca-chem":"Lates calcarifer barramundi / Asian sea bass, a large silvery FISH with a deep elongated body, a concave pointed head with a protruding lower jaw, large mouth, spiny then soft dorsal fins, forked tail, silvery-grey color",
 "oc-buou-den":"Pila polita apple snail — a single large rounded GLOBULAR shell with a low short spire and a very large swollen rounded body whorl, smooth dark olive-green to blackish, an aquatic apple snail, NOT a tall pointed land/garden snail",
 "ca-chach":"Mastacembelus favus tire-track spiny eel (Vietnamese 'cá chạch lấu'), an elongated brown freshwater fish with a long fleshy pointed snout, the body patterned with pale yellow net-like / tire-track markings on dark brown, a long low row of small dorsal spines along the back",
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
    jobs=[]
    for cid,s in DETAIL_SUBJ.items():
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", DETAIL_T.format(s=s)))
    for cid,s in SPECIES.items():
        jobs.append((os.path.join(IMG, cid+".jpg"), "4:3", THUMB_T.format(s=s)))
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", DETAIL_T.format(s=s)))
    print(f"Gen {len(jobs)} ảnh...")
    done=0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(gen,*j):j for j in jobs}
        for fu in cf.as_completed(futs):
            done+=1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")
if __name__=="__main__": main()
