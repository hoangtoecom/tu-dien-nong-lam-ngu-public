#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regen ảnh lỗi (đúng loài VN + đủ màu + không artifact) + gen 30 loài mới (6 nhóm).
Bỏ qua file đã có (đã xoá file lỗi trước khi chạy). python3 scripts/gen-images-fix-and-180.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img'); DET = os.path.join(IMG, 'detail')
os.makedirs(DET, exist_ok=True)
# Style siết chặt: ĐỦ MÀU, không phác thảo, không artifact, đúng loài thật
PT = ("Antique botanical illustration plate of {s}, fully painted in rich natural watercolor color, "
      "finished detailed scientific botanical illustration, 19th century, accurate to the real plant, "
      "clean white background, no text, no labels, no artifacts, not a pencil sketch, not line art, not unfinished")
PD = ("Antique botanical illustration plate of {s}, full plant study showing leaves, flowers, fruit, roots and "
      "cross-sections, fully painted in rich natural watercolor color, finished detailed botanical study, 19th century, "
      "accurate to the real plant, clean white background, no text, no labels, no artifacts, not a sketch")
AT = ("Antique zoological illustration plate of {s}, fully painted in rich natural watercolor color, "
      "finished detailed scientific illustration, 19th century natural history art, accurate to the real species, "
      "single clean specimen, clean white background, no text, no labels, no extra animals, no artifacts, "
      "not a pencil sketch, not line art, not unfinished")
AD = ("Antique zoological illustration plate of {s}, full body together with one or two smaller anatomical detail "
      "studies of the same animal, fully painted in rich natural watercolor color, finished detailed natural history "
      "study, 19th century, accurate to the real species, clean white background, no text, no labels, no extra animals, "
      "no artifacts, not a sketch")

# (kind, subject) — kind: 'p' cây / 'a' động vật
REGEN = {
 "ca-ro-phi":("a","Oreochromis niloticus Nile tilapia, deep oval grey-olive body with faint dark vertical bars, spiny dorsal fin, small head, freshwater food fish, not a perch, not red, not a sunfish"),
 "ca-chep":("a","Cyprinus carpio common wild carp, elongated body with large bronze-olive and brassy brown scales, two pairs of barbels at the mouth, natural muddy-bronze color, not a bright orange goldfish"),
 "ca-chinh":("a","Anguilla marmorata giant mottled eel, long thick snake-like body with brown and olive marbled blotchy pattern, small pectoral fins, Vietnamese freshwater eel"),
 "tom-cang-xanh":("a","Macrobrachium rosenbergii giant freshwater prawn, one single specimen, translucent bluish-grey body, very long slender blue claws, long antennae"),
 "trun-que":("a","Perionyx excavatus earthworm, a single smooth slender reddish-brown segmented worm with no legs, soft moist body on dark compost soil, not a millipede, not a centipede"),
 "luon":("a","Monopterus albus Asian swamp eel, long smooth scaleless yellowish-brown eel-like fish with tapering pointed head and almost no fins, Vietnamese rice-field eel"),
 "oc-buou-den":("a","Pila polita black apple snail, a rounded globular dark olive-black spiral shell with a large body whorl and operculum, freshwater snail"),
 "mun":("p","Diospyros mun ebony, a branch with small glossy oval leaves and small dark fruit, plus a cut piece of jet-black dense ebony heartwood showing wood grain, not black spheres, not black balls"),
 "hau":("a","Crassostrea oyster, a cluster of rough grey oyster shells with one shell open showing pearly white interior, shellfish mollusk only, no bird, no other animals"),
 "ngheu":("a","Meretrix lyrata hard clam, smooth glossy triangular bivalve clam shells one open one closed, shellfish mollusk only, no bird, no other animals"),
}
REGEN_DETAIL_ONLY = {
 "de":("a","Capra hircus domestic goat, full body side profile plus a head close-up study and a detail of the horns and hooves"),
}
# 30 loài mới — 6 nhóm
NEW = {
 # Lâm nghiệp · rừng ngập mặn (cây)
 "duoc":("p","Rhizophora apiculata mangrove tree with arching stilt prop roots, leathery elliptic green leaves, long pencil-like hanging propagule seedlings"),
 "mam":("p","Avicennia marina grey mangrove tree with many pencil-like aerial pneumatophore roots sticking up from mud, grey-green leaves, small round fruit"),
 "ban":("p","Sonneratia caseolaris mangrove apple tree, spreading crown, conical pneumatophore roots, round green fruit, white and pink-red flowers"),
 "vet":("p","Bruguiera gymnorhiza mangrove tree with knee-shaped looping roots, glossy dark leaves, red star-shaped calyx flower, long cigar-shaped propagule"),
 "su":("p","Aegiceras corniculatum river mangrove shrub, small leathery oval leaves, clusters of white flowers, curved horn-shaped fruit"),
 # Lâm nghiệp · cây cảnh & bóng mát (cây)
 "phuong-vi":("p","Delonix regia royal poinciana flame tree, fern-like bipinnate feathery leaves, brilliant red-orange flowers, long flat brown seed pods"),
 "loc-vung":("p","Barringtonia acutangula tree, glossy oval leaves, long hanging racemes of bright red flowers, squarish fruit"),
 "me-tay":("p","Samanea saman rain tree, huge umbrella crown, bipinnate leaves, pink powderpuff flowers, long dark brown pods"),
 "muong-hoang-yen":("p","Cassia fistula golden shower tree, pinnate leaves, long hanging clusters of bright yellow flowers, long cylindrical dark pods"),
 "osaka-do":("p","tropical ornamental flowering tree with long cascading clusters of bright red flowers and pinnate compound green leaves"),
 # Chăn nuôi · thú nuôi đặc sản (động vật)
 "dui":("a","Rhizomys bamboo rat, a stout thick-bodied rodent with grey-brown fur, small ears and eyes, large orange incisor teeth, short tail"),
 "chon-huong":("a","Paradoxurus hermaphroditus common palm civet, slender cat-like mammal, greyish-brown fur with dark dorsal stripes, dark masked face, long tail"),
 "heo-rung":("a","wild boar Sus scrofa, dark coarse bristly coat, elongated snout, small curved tusks, sturdy muscular body"),
 "nai":("a","Rusa unicolor sambar deer, large sturdy brown deer with shaggy dark brown coat and three-tined antlers"),
 "cay-voi-huong":("a","Paguma larvata masked palm civet, plain brownish body, distinctive white facial stripe from nose over the head, long tail"),
 # Chăn nuôi · bò sát nuôi (động vật)
 "ca-sau":("a","Crocodylus siamensis Siamese crocodile, armored scaly olive-grey body, long broad snout, powerful tail, full body"),
 "ran-ho-trau":("a","Ptyas mucosa oriental ratsnake, a long slender olive-brown non-venomous snake with smooth body, loosely coiled"),
 "ky-da":("a","Varanus salvator water monitor lizard, long body with mottled dark grey and yellow scales, forked tongue, long powerful tail"),
 "tran":("a","Python bivittatus Burmese python, thick muscular body with brown saddle blotch pattern on tan background, coiled"),
 "tac-ke":("a","Gekko gecko tokay gecko, plump blue-grey body covered with orange and pale spots, large head, sticky toe pads"),
 # Thủy sản · cá biển nuôi (động vật)
 "ca-mu":("a","Epinephelus grouper, stout heavy body, very large mouth, brown body mottled with darker spots and blotches, marine food fish"),
 "ca-chem":("a","Lates calcarifer barramundi Asian sea bass, elongated silvery body, pointed concave head, large mouth, forked tail"),
 "ca-bop":("a","Rachycentron canadum cobia, long streamlined dark brown body with a pale horizontal lateral stripe, flattened head"),
 "ca-hong-my":("a","Sciaenops ocellatus red drum, reddish-bronze streamlined body with a black spot near the tail base"),
 "ca-mang":("a","Chanos chanos milkfish, streamlined silvery elongated body, small head, deeply forked tail"),
 # Thủy sản · nhuyễn thể & rong
 "so-huyet":("a","Anadara granosa blood cockle, rounded heart-shaped bivalve shells with strong radial ribs, off-white shells"),
 "oc-huong":("a","Babylonia areolata spotted babylon sea snail, smooth conical glossy shell patterned with brown squarish spots"),
 "vem-xanh":("a","Perna viridis Asian green mussel, elongated tapering bivalve shell with bright green and brown coloring"),
 "rong-nho":("p","Caulerpa lentillifera sea grapes seaweed, clusters of tiny round bright green bead-like fronds on slender stems"),
 "rong-sun":("p","Kappaphycus alvarezii seaweed, branching translucent yellowish-green cartilaginous fronds"),
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
    def add(cid, kind, s, thumb=True, detail=True):
        tt = PT if kind=='p' else AT; td = PD if kind=='p' else AD
        if thumb: jobs.append((os.path.join(IMG, cid+".jpg"), "4:3", tt.format(s=s)))
        if detail: jobs.append((os.path.join(DET, cid+".jpg"), "3:4", td.format(s=s)))
    for cid,(k,s) in REGEN.items(): add(cid,k,s)
    for cid,(k,s) in REGEN_DETAIL_ONLY.items(): add(cid,k,s,thumb=False)
    for cid,(k,s) in NEW.items(): add(cid,k,s)
    print(f"Gen {len(jobs)} ảnh...")
    done=0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs={ex.submit(gen,*j):j for j in jobs}
        for fu in cf.as_completed(futs):
            done+=1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")

if __name__=="__main__":
    main()
