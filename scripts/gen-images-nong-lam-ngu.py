#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen 20 ảnh chăn nuôi + thủy sản (cùng style tranh khắc cổ với 100 cây).
Chạy: python3 scripts/gen-images-nong-lam-ngu.py
Kết quả: img/<id>.jpg (4:3). Dùng credits Higgsfield (không cần API key)."""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img')
os.makedirs(IMG, exist_ok=True)
# style "động vật học cổ" — song song với style botanical của 100 cây
ST = ("Antique zoological illustration plate of {s}, vintage scientific watercolor engraving, "
      "19th century natural history art, clean white background, no text, no letters, no labels")
SUBJ = {
  # === CHĂN NUÔI ===
  "bo-sua": "Bos taurus Holstein Friesian dairy cow, black and white patches, full body side profile, prominent udder, standing pose",
  "trau": "Bubalus bubalis domestic water buffalo, dark grey hide, large curved swept-back horns, sturdy body, side profile",
  "lon": "Sus domesticus domestic pig, pink white body, short legs, curly tail, snout, side profile standing",
  "de": "Capra hircus domestic goat, short coat, curved horns, beard, slender legs, side profile",
  "ga": "Gallus gallus domesticus rooster and hen, red comb and wattles, colorful tail feathers, standing",
  "vit": "Anas platyrhynchos domestic duck, white plumage, orange bill and webbed feet, side profile",
  "ngan": "Cairina moschata Muscovy duck, black and white plumage, red caruncles on face, side profile",
  "chim-cut": "Coturnix japonica Japanese quail, small plump bird, brown speckled plumage, short tail, standing",
  "ong-mat": "Apis cerana honey bee, detailed study of worker bee with wings, plus honeycomb hexagonal cells",
  "tho": "Oryctolagus cuniculus domestic rabbit, long ears, soft fur, sitting pose, side profile",
  # === THỦY SẢN ===
  "ca-tra": "Pangasius hypophthalmus striped catfish, elongated silvery body, barbels, long dorsal fin, side profile",
  "ca-ro-phi": "Oreochromis niloticus Nile tilapia, deep compressed body, spiny dorsal fin, side profile",
  "ca-loc": "Channa striata snakehead fish, elongated cylindrical body, dark mottled pattern, large mouth, side profile",
  "ca-dieu-hong": "Oreochromis red tilapia, reddish pink body, deep shape, dorsal fin, side profile",
  "tom-the": "Litopenaeus vannamei whiteleg shrimp, translucent body, long antennae, legs and tail fan, side view",
  "tom-su": "Penaeus monodon giant tiger prawn, dark body with tiger stripes, long antennae, side view",
  "cua-bien": "Scylla serrata mud crab, broad carapace, large claws, eight legs, top view",
  "ngheu": "Meretrix lyrata hard clam, two ridged oval shells, one open showing inside, on white",
  "hau": "Crassostrea oyster, rough irregular shell, one open showing pearly interior, on white",
  "ech": "Hoplobatrachus rugulosus rice field frog, mottled green brown skin, long hind legs, sitting pose",
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
    jobs = [(os.path.join(IMG, cid+".jpg"), "4:3", ST.format(s=s)) for cid, s in SUBJ.items()]
    print(f"Gen {len(jobs)} ảnh...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")
if __name__ == "__main__":
    main()
