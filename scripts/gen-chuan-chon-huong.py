#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regen theo CHUẨN chồn hương: detail gia súc = bản đồ tự nhiên (1 ảnh body tổng thể + 1 ảnh đầu góc khác
+ 1 ảnh chân), tô màu đủ, style editorial. Sửa dúi (chuột tre mặt mập đuôi cụt), chạch đồng (thay chạch lấu),
cá măng (thumb≠detail), cá bớp (bỏ nghiên cứu phụ). python3 scripts/gen-chuan-chon-huong.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img'); DET = os.path.join(IMG, 'detail')

# DETAIL gia súc/dúi 3:4 — bản đồ tự nhiên kiểu chồn hương: full-body + đầu (góc khác) + chân
PLATE_T = ("Vintage editorial scientific watercolor natural-history plate of {s}, on a pure flat white background: "
           "ONE large COMPLETE full-body animal in three-quarter side view showing the whole body with all four legs, "
           "head and tail in their correct natural anatomical positions, with a soft cast shadow; PLUS a smaller boxed "
           "close-up study of the head from a different angle; PLUS a smaller boxed close-up study of one {foot}. "
           "EVERY element fully painted in rich natural color — NO pencil sketch, NO uncolored outline study, "
           "anatomically accurate to the real species, correct proportions, no deformed body parts, the tail in its "
           "proper place at the rear (never on the head), no text, no labels.")
# THUMB 4:3 — 1 con, nền trắng tinh
THUMB_T = ("Vintage scientific watercolor illustration of {s}, fully painted in rich natural color, single specimen "
           "isolated on a pure flat solid white background, no border, no frame, no text, accurate to the real species, not a sketch")
# DETAIL cá 3:4 — full-body sạch, KHÔNG nghiên cứu phụ (khớp thumb)
FISH_DET_T = ("Vintage scientific watercolor illustration of {s}, the complete fish fully painted in rich natural color, "
              "shown large and detailed in full-body side profile, single fish on a pure flat white background, "
              "NO inset, NO close-up study, NO anatomical detail box, no text, no labels, not a sketch, accurate to the real species")

# Gia súc — (mô tả loài, loại bàn chân cho ảnh chân)
GIA_SUC = {
 "bo-sua":("a Holstein Friesian dairy cow with black-and-white patches and a large udder","cloven hoof"),
 "trau":("a Vietnamese water buffalo with dark slate-grey hide and large swept-back curved horns","cloven hoof"),
 "lon":("a domestic pig with a pink body, short legs and a short curly tail at the rear","trotter (cloven hoof)"),
 "de":("a domestic goat with a short coat, curved horns and a beard","cloven hoof"),
 "bo-thit":("a Vietnamese yellow beef bull with a tan-brown coat and short horns","cloven hoof"),
 "cuu":("a Phan Rang sheep with thick woolly fleece and curled horns","cloven hoof"),
}
# Dúi — chuột tre: mặt mập tròn, răng cửa cam, ĐUÔI CỤT
DUI = ("a bamboo rat (Rhizomys), a stout heavy-bodied burrowing rodent with a CHUBBY rounded face, small ears and "
       "small eyes, large orange incisor teeth, dense greyish-brown fur and a VERY SHORT stubby nearly hairless tail "
       "— NOT a long-tailed rat, NOT a slender mouse")
# Cá (thumb + detail sạch)
CA_CHACH = ("an oriental weatherfish / pond loach (Misgurnus anguillicaudatus), a small slender eel-like freshwater fish "
            "with a rounded cylindrical mottled yellow-brown body speckled with darker spots, several pairs of short "
            "barbels around the mouth, small soft fins and a small rounded tail")
CA_MANG = ("a milkfish (Chanos chanos), a streamlined silvery fish with a single dorsal fin and a deeply forked tail")
CA_BOP  = ("a cobia (Rachycentron canadum), a robust elongated marine fish with a broad flattened head, a row of short "
           "stout separate dorsal spines, large pointed pectoral fins and a forked tail, dark chocolate-brown back with "
           "a pale silver lateral stripe and white belly")

def gen(out, ratio, prompt):
    try:
        if os.path.exists(out): os.remove(out)  # overwrite
    except Exception: pass
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
    # Gia súc — detail plate chuẩn chồn hương
    for cid,(s,foot) in GIA_SUC.items():
        jobs.append((os.path.join(DET, cid+".jpg"), "3:4", PLATE_T.format(s=s, foot=foot)))
    # Dúi — thumb + detail plate
    jobs.append((os.path.join(IMG, "dui.jpg"), "4:3", THUMB_T.format(s=DUI)))
    jobs.append((os.path.join(DET, "dui.jpg"), "3:4", PLATE_T.format(s=DUI, foot="clawed forefoot")))
    # Chạch đồng — thumb + detail sạch
    jobs.append((os.path.join(IMG, "ca-chach.jpg"), "4:3", THUMB_T.format(s=CA_CHACH)))
    jobs.append((os.path.join(DET, "ca-chach.jpg"), "3:4", FISH_DET_T.format(s=CA_CHACH)))
    # Cá măng — thumb + detail cùng mô tả (khớp nhau)
    jobs.append((os.path.join(IMG, "ca-mang.jpg"), "4:3", THUMB_T.format(s=CA_MANG)))
    jobs.append((os.path.join(DET, "ca-mang.jpg"), "3:4", FISH_DET_T.format(s=CA_MANG)))
    # Cá bớp — chỉ detail sạch (bỏ nghiên cứu phụ)
    jobs.append((os.path.join(DET, "ca-bop.jpg"), "3:4", FISH_DET_T.format(s=CA_BOP)))
    print(f"Gen {len(jobs)} ảnh...")
    done=0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(gen,*j):j for j in jobs}
        for fu in cf.as_completed(futs):
            done+=1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")

if __name__=="__main__": main()
