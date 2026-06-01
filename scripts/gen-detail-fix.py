#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sửa ảnh động vật/cá: detail tô màu đủ + nghiên cứu phụ đa dạng (móng/đuôi/vây, không lặp đầu);
sửa loài sai (lươn, cá bớp, sò huyết); thêm cá chạch lấu. python3 scripts/gen-detail-fix.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img'); DET = os.path.join(IMG, 'detail')

# Detail 3:4 — ÉP tô màu đủ, nghiên cứu phụ cũng tô màu (không phác chì), đa dạng chi tiết
DETAIL_T = ("Vintage scientific watercolor illustration of {s}, a natural-history plate: the full animal in full color "
            "together with {extra} — EVERY element fully painted in rich natural color, NO pencil sketch, NO uncolored "
            "line drawing, NO grey outline study, on pure white background, accurate to the real species, no text, no labels")
# Thumb 4:3 — 1 con, nền trắng tinh
THUMB_T = ("Vintage scientific watercolor illustration of {s}, fully painted in rich natural color, single specimen "
           "isolated on a pure flat solid white background, no border, no frame, no text, accurate to the real species, not a sketch")

# id -> (mô tả loài, nghiên cứu phụ tô màu) — regen DETAIL (giữ loài, thumb đang ổn)
DETAIL = {
 "bo-sua":("Holstein Friesian dairy cow, black and white patches, prominent udder", "a small colored close-up of a hoof and the tail"),
 "trau":("Vietnamese water buffalo, dark grey hide, large swept-back curved horns", "a small colored close-up of a hoof and the curved horn"),
 "lon":("domestic pig, pink body", "a small colored close-up of the snout and a trotter"),
 "de":("domestic goat, short coat, curved horns and beard", "a small colored close-up of the horns and a cloven hoof"),
 "bo-thit":("Vietnamese yellow beef cattle, tan-brown coat, short horns", "a small colored close-up of a hoof and the tail tuft"),
 "cuu":("Phan Rang sheep, woolly fleece, curled horns", "a small colored close-up of the curled horn and a hoof"),
 "ga":("rooster and hen, red comb, colorful tail feathers", "a small colored close-up of a clawed foot and a tail feather"),
 "vit":("domestic duck, white plumage, orange bill", "a small colored close-up of the orange webbed foot and the bill"),
 "ngan":("Muscovy duck, black and white plumage, red facial caruncles", "a small colored close-up of the webbed foot and the head"),
 "chim-cut":("Japanese quail, brown speckled plumage", "a small colored close-up of a foot and a speckled egg"),
 "bo-cau":("domestic pigeon, grey plumage, iridescent neck", "a small colored close-up of a foot and a wing feather"),
 "ga-tay":("domestic turkey, fanned tail, red wattled head, bronze plumage", "a small colored close-up of a foot and tail feathers"),
 "da-dieu":("ostrich, black-and-white plumage, long bare neck and legs", "a small colored close-up of a two-toed foot and plumage"),
 "tho":("domestic rabbit, long ears, soft fur", "a small colored close-up of a hind foot and the head"),
 "ca-tra":("Pangasius hypophthalmus striped catfish, silvery elongated body, barbels", "a colored close-up of the head with barbels and the tail fin"),
 "ca-basa":("Pangasius bocourti basa catfish, plump silvery body, barbels", "a colored close-up of the head and the tail fin"),
 "ca-chem":("Lates calcarifer barramundi, elongated silvery body, pointed head", "a colored close-up of the head and the forked tail fin"),
 "ca-mang":("Chanos chanos milkfish, streamlined silvery body, forked tail", "a colored close-up of the head and the deeply forked tail"),
 "ca-hong-my":("Sciaenops ocellatus red drum, reddish-bronze body, black tail spot", "a colored close-up of the head and the black-spotted tail"),
 "ca-ro-phi":("Oreochromis niloticus Nile tilapia, grey-olive body with faint bars", "a colored close-up of the spiny dorsal fin and the tail"),
 "ech":("Hoplobatrachus rugulosus rice-field frog, mottled green-brown", "a small colored close-up of a webbed hind foot"),
}

# id -> mô tả loài (sửa SAI SỰ THẬT) — regen CẢ thumb + detail
SPECIES = {
 "luon":"Monopterus albus Asian swamp eel — a slender SMOOTH scaleless snake-like fish, plain yellowish-brown to olive color, blunt pointed head, very small eyes, NO pectoral fins and almost no visible fins, the rice-field eel of Vietnam",
 "ca-bop":"Rachycentron canadum cobia — a ROBUST elongated marine FISH with a broad flattened head, a row of short stout separate dorsal spines, large pointed pectoral fins and a forked tail, dark chocolate-brown back with a pale silver lateral stripe and white belly; it is a fish with clear fins, NOT an eel",
 "so-huyet":"Anadara granosa blood cockle — a pair of small thick rounded bivalve shells with strong deep RADIAL RIBS like a scallop, off-white to tan, shown as two shells one slightly open",
}
DETAIL_EXTRA = {  # nghiên cứu phụ cho 3 loài sửa
 "luon":"a colored close-up of the blunt head and a cross-section of the body",
 "ca-bop":"a colored close-up of the head and the spiny dorsal fin",
 "so-huyet":"a colored close-up of one ribbed shell showing the hinge",
}

# Cá chạch lấu — thay cá chình (id mới ca-chach)
CHACH = "Mastacembelus favus tire-track spiny eel, the Vietnamese 'cá chạch lấu' — an elongated fish with a long tubular pointed snout, brownish-olive body covered with dark net-like tire-track markings and pale spots, a long low spiny dorsal fin running along the back"

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
    for cid,(s,extra) in DETAIL.items():
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", DETAIL_T.format(s=s, extra=extra)))
    for cid,s in SPECIES.items():
        jobs.append((os.path.join(IMG, cid+".jpg"), "4:3", THUMB_T.format(s=s)))
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", DETAIL_T.format(s=s, extra=DETAIL_EXTRA[cid])))
    jobs.append((os.path.join(IMG, "ca-chach.jpg"), "4:3", THUMB_T.format(s=CHACH)))
    jobs.append((os.path.join(DET, "ca-chach.jpg"), "3:4", DETAIL_T.format(s=CHACH, extra="a colored close-up of the pointed snout and the tail")))
    print(f"Gen {len(jobs)} ảnh...")
    done=0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(gen,*j):j for j in jobs}
        for fu in cf.as_completed(futs):
            done+=1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")

if __name__=="__main__":
    main()
