#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regen ảnh SAI theo audit (AUDIT-IMAGES.md). Backup ảnh cũ rồi gen lại theo nhóm A/B/C.
   Chạy: python3 scripts/gen-fix.py
   - Cat A (gỗ lớn): detail = BRANCH STUDY, không cây tí hon, không rễ lộ.
   - Cat B (cao thân mảnh): detail = STALK STUDY.
   - Cat C (thấp/củ/leo): cây nguyên có rễ OK, sửa lát cắt/màu cho đúng.
   - Bỏ lát cắt 'cam có múi' lạc loài ở mọi cây.
"""
import os, time, subprocess, urllib.request, concurrent.futures as cf

BASE = os.path.join(os.path.dirname(__file__), '..')
IMG  = os.path.join(BASE, 'img')
DET  = os.path.join(IMG, 'detail')
TS   = time.strftime('%Y%m%d-%H%M%S')
BK_D = os.path.join(DET, f'_old-{TS}')
BK_M = os.path.join(IMG, f'_old-{TS}')
BK_U = os.path.join(IMG, 'ui', f'_old-{TS}')

STYLE = ("Antique botanical illustration plate, 19th century scientific watercolor and ink engraving, "
         "natural true-to-life colors, on a clean white background, no text, no letters, no labels, no numbers")
NO_TREE = ("Compose it as a CUT BRANCH specimen study only — a branch with leaves, flowers and fruit, plus small "
           "separate details. Do NOT draw the whole tree, do NOT show a tiny bonsai tree, do NOT show exposed roots. "
           "Do NOT add any unrelated round citrus-like cross-section with segments.")
NO_TINY = ("Show only a stalk/stem segment study with leaves, flower and fruit. Do NOT draw a tiny whole plant with roots. "
           "Do NOT add any unrelated citrus-like segmented cross-section.")
NO_CIT  = "Do NOT add any unrelated round citrus-like cross-section with segments."

# id -> (aspect, prompt)  ; cat A/B uses branch/stalk, cat C whole-plant + corrected cross-section
A = {  # Cat A gỗ lớn -> branch study
 "vu-sua":  "Chrysophyllum cainito star apple: branch with oval leaves green above and coppery-golden velvety beneath, small pinkish flowers, a round purple fruit, and a cross-section showing the white pulp in a star pattern. No carambola star fruit anywhere.",
 "khe":     "Averrhoa carambola star fruit: branch with compound leaves, small pink-purple flowers, a ribbed yellow-green star fruit, and ONE cross-section showing the 5-point star shape. Only the star cross-section, no other cross-section.",
 "ca-phe":  "Coffea arabica coffee: branch with glossy deep-GREEN leaves (not dark/black), white star flowers, clusters of green and red cherries, and a cross-section of a cherry showing two beans.",
 "dieu":    "Anacardium occidentale cashew: branch with smooth oval leaves, panicle of small pink-striped flowers, a red-yellow cashew apple with the curved grey nut hanging below, and a cross-section of the nut.",
 "sau-rieng":"Durio zibethinus durian: branch with simple elliptic leaves bronze beneath (NOT compound feathery leaves), a large spiky green fruit, and a cross-section showing creamy segments with large seeds.",
 "bo":      "Persea americana avocado: branch with glossy leaves, small greenish flowers, a pear-shaped green fruit, and a cross-section showing yellow flesh and one large round single seed.",
 "hong":    "Diospyros kaki persimmon: branch with broad leaves, an orange fruit with a four-lobed green calyx, and a cross-section of the orange flesh.",
 "tech":    "Tectona grandis teak: large rough oval leaves, panicle of small white flowers, papery winged fruits, and a small section of pale-brown wood.",
 "thong":   "Pinus merkusii pine: a branch with long needle leaves in pairs, a brown woody cone, and a piece of resinous bark. No flowers.",
 "sao-den": "Hopea odorata: leathery lanceolate leaves, small flowers, and the characteristic two-winged samara fruit. No citrus cross-section.",
 "po-mu":   "Fokienia hodginsii: flattened scale-like aromatic foliage sprays, small round woody cones, and a piece of fragrant pale wood. No flowers, no citrus cross-section.",
 "sen-mat": "Madhuca pasquieri: branch with leathery leaves clustered at tips, fleshy cream flowers, a small berry, and a section of wood.",
 "dau-rai": "Dipterocarpus alatus: large leathery leaves with full natural GREEN color (not grey), and the large two-winged samara fruit, with a piece of resinous bark. No citrus cross-section.",
 "xoan-ta": "Melia azedarach chinaberry: bipinnate leaves, clusters of small lilac flowers, and small round yellow drupes with a cross-section showing the hard stone. No citrus segments.",
 "hoi":     "Illicium verum star anise: branch with glossy leaves, a star-shaped fruit of 8 woody points (the correct fruit), and small flowers. No round citrus cross-section.",
 "tram-gio":"Melaleuca cajuputi: narrow leaves, white bottlebrush flower spikes, and papery peeling pale bark. No citrus cross-section.",
 "lim-xanh":"Erythrophleum fordii: bipinnate compound leaves, small flower spikes, flat seed pods, and a section of dark wood.",
 "dinh":    "Markhamia stipulata: large pinnate leaves, yellow bell-shaped flowers, very long slender seed pods, and a piece of wood.",
 "tau":     "Vatica odorata: leathery leaves, small flowers, a winged fruit, and a piece of pale-yellow wood. No citrus cross-section.",
 "sua":     "Dalbergia tonkinensis rosewood: pinnate compound leaves, small white pea flowers, flat seed pods, and a section of fragrant reddish heartwood.",
 "cam-lai": "Dalbergia oliveri: pinnate compound leaves, small pale flowers, flat seed pods, and a section of pink-brown heartwood.",
 "go-do":   "Afzelia xylocarpa: pinnate leaves, small flowers, a thick woody pod with black seeds capped in orange aril, and a section of red-brown wood.",
 "vu-huong":"Cinnamomum balansae: aromatic leaves with three veins, small flowers, small dark berries, and a section of fragrant wood. No citrus cross-section.",
 "mo":      "Manglietia conifera: glossy leaves, a large white magnolia flower, an upright cone-like aggregate fruit, and a piece of wood. No citrus cross-section.",
 "bo-de":   "Styrax tonkinensis: oval leaves, hanging white bell flowers, small round fruits, and resin droplets on a branch. No citrus cross-section.",
 "phi-lao": "Casuarina equisetifolia: drooping needle-like green branchlets, small cone-like fruits, and a piece of bark. No citrus cross-section.",
 "xa-cu":   "Khaya senegalensis mahogany: pinnate leaves, small white flowers, round woody capsules splitting open with winged seeds, and a section of red-brown wood. No citrus cross-section.",
 "muong-den":"Senna siamea: pinnate compound leaves, yellow flower clusters, flat seed pods, and a piece of wood. No citrus cross-section.",
 "thong-ba-la":"Pinus kesiya three-needle pine: needle leaves in groups of three, brown woody cones, and resinous bark. No flowers, no citrus cross-section.",
 "do-bau":  "Aquilaria crassna agarwood: glossy leaves, small white flowers, and a section of pale wood streaked with dark fragrant resin. No citrus cross-section.",
 "ko-nia":  "Irvingia malayana wild almond: oblong glossy leaves, small flowers, a green ovoid fruit, and a cross-section showing ONE large hard almond-like seed. No citrus segments.",
 "bang-lang":"Lagerstroemia speciosa: oblong leaves, large clusters of crinkled purple flowers, round woody seed capsules, and smooth bark. No citrus cross-section.",
 "long-nao":"Cinnamomum camphora camphor: glossy aromatic leaves with three veins, small flowers, small dark berries, and a section of pale aromatic wood. No citrus cross-section.",
 "oi":      "Psidium guajava guava: branch with smooth bark, oval veined leaves, white flowers with many stamens, a round fruit, and a cross-section of pink flesh with many tiny seeds. No exposed roots.",
 "giang-huong":"Pterocarpus macrocarpus: pinnate compound leaves, fragrant yellow pea flowers, round winged pods, and a section of yellow-brown heartwood.",
 "trac":    "Dalbergia cochinchinensis Siamese rosewood: pinnate compound leaves, small pale flowers, flat seed pods, and a section of dark red-brown heartwood.",
 "que":     "Cinnamomum cassia cinnamon: leaves with three veins, small flowers, and rolled quills of fragrant brown bark with a piece of bark and wood. No citrus cross-section.",
 "dau-tam": "Morus alba mulberry: branch with serrated heart-shaped leaves, small catkin flowers, and clusters of dark purple-black aggregate berries. No round citrus cross-section.",
}
PALM = {
 "dua": ("4:3" if False else "3:4",
   "Cocos nucifera coconut palm: a few large pinnate fronds and a CLUSTER of green coconuts on the crown, a halved coconut showing white flesh and water cavity, a fibrous husk piece, and a flower spadix. Tall single columnar palm — do NOT draw a tiny tree, do NOT make it look like a slender areca/cau palm. "+NO_CIT),
}
B = {  # Cat B cao thân mảnh -> stalk study
 "chuoi":  "Musa banana: a section of the pseudostem with a large paddle leaf, a hanging bunch of green-yellow bananas, the purple flower bud, and a cross-section of a banana. Full natural color, no dark/black render artifact.",
 "du-du":  "Carica papaya: the top of the hollow trunk with palmate lobed leaves, clusters of round-oval fruit on the stem, and a cross-section showing orange flesh and black seeds in the cavity.",
 "luong":  "Dendrocalamus giant bamboo: a segment of thick jointed culm with a node and branch of lance leaves, a shoot, and a cross-section of the hollow culm wall. Full natural green color, no grey/black-and-white areas.",
}
C = {  # Cat C: whole plant ok, fix defect
 "nho":     "Vitis vinifera grape: a section of woody vine with tendrils and lobed leaves, a hanging cluster of grapes, and a cross-section of one grape showing translucent flesh with 2 to 4 small seeds. "+NO_CIT,
 "bap-cai": "Brassica oleracea cabbage: a SHORT-stemmed plant sitting at ground level with a tight round head of wrapped leaves and spreading outer leaves and roots, plus a halved cabbage showing tightly packed concentric leaf layers. Stem is very short — head sits near the ground. "+NO_CIT,
 "muop":    "Luffa aegyptiaca sponge gourd: climbing vine with lobed leaves and tendrils, bright yellow flowers, a LONG SMOOTH cylindrical green gourd with faint ridges (NOT a bumpy warty bitter melon), and a cross-section with white flesh and flat black seeds. "+NO_CIT,
 "khoai-tay":"Solanum tuberosum potato: GREEN compound leaves with full watercolor color (not grey), white-purple star flowers, several brown tubers below ground with roots, and a tuber cut showing solid pale creamy flesh with no seeds. Do NOT draw eggplant berries. "+NO_CIT,
 "ca-rot":  "Daucus carota carrot: a long tapering orange taproot with fine rootlets, feathery finely-divided leaves, a white umbel flower, and a root cross-section showing CONCENTRIC core and outer rings (no seeds, no citrus segments).",
 "cai-xanh":"Brassica juncea mustard greens: an upright rosette of broad GREEN leaves (not purple, not curly kale) with pale midribs, roots, small yellow flowers, and slender seed pods. "+NO_CIT,
 "xa-lach": "Lactuca sativa lettuce: a low loose head/rosette of soft green leaves with roots at the base — NOT a tall bolted flowering stem, NO bean pods. A small leaf cross-section is fine. "+NO_CIT,
 "dau-phong":"Arachis hypogaea peanut: a low bushy plant with compound leaves and yellow pea flowers, underground pods on pegs, and a pod cross-section showing 2 peanut seeds in papery shell. "+NO_CIT,
 "gung":    "Zingiber officinale ginger: upright leafy shoots, a knobby pale-yellow rhizome with roots, a flower spike, and a rhizome cross-section showing pale fibrous flesh. "+NO_CIT,
 "nghe":    "Curcuma longa turmeric: broad leaves, a knobby rhizome with bright orange flesh and roots, a flower spike, and a rhizome cross-section showing deep orange flesh. "+NO_CIT,
 "rieng":   "Alpinia officinarum galangal: tall leafy stems, a hard reddish-brown rhizome with roots, a flower spike, and a rhizome cross-section showing firm pale flesh. "+NO_CIT,
 "hung-que":"Ocimum basilicum basil: a bushy plant with square stems, green-and-purple oval leaves, and spikes of small white-purple flowers with tiny seeds. NO bean pods, NO citrus cross-section.",
 "cu-den":  "Beta vulgaris beetroot: a round deep red-purple swollen root with rootlets, dark green leaves with red veins, and a root cross-section showing CONCENTRIC red-purple rings (no seeds, no citrus segments).",
}

def build_jobs():
    jobs = []  # (out_path, aspect, prompt)
    for cid, feat in A.items():
        jobs.append((os.path.join(DET, cid+'.jpg'), "3:4", f"{STYLE}. {feat} {NO_TREE}"))
    for cid, (asp, p) in PALM.items():
        jobs.append((os.path.join(DET, cid+'.jpg'), asp, f"{STYLE}. {p}"))
    for cid, feat in B.items():
        jobs.append((os.path.join(DET, cid+'.jpg'), "3:4", f"{STYLE}. {feat} {NO_TINY}"))
    for cid, feat in C.items():
        jobs.append((os.path.join(DET, cid+'.jpg'), "3:4", f"{STYLE}. {feat} Show the whole low plant with roots."))
    # MAIN (4:3) cần regen
    jobs.append((os.path.join(IMG, 'muop.jpg'), "4:3",
        f"{STYLE}. Luffa aegyptiaca sponge gourd on the vine: lobed leaves, yellow flower, a LONG SMOOTH cylindrical green gourd with faint ridges (NOT a warty bitter melon), and a cut showing white flesh. {NO_CIT}"))
    jobs.append((os.path.join(IMG, 'khoai-tay.jpg'), "4:3",
        f"{STYLE}. Solanum tuberosum potato: green leaves, white-purple flowers, and several clean brown potato tubers (no text or markings on the tubers), with a tuber cut showing pale creamy flesh. {NO_CIT}"))
    # HERO (16:9) — bỏ quả xoài lạc trên cành cà phê
    jobs.append((os.path.join(IMG, 'ui', 'hero.jpg'), "16:9",
        "Antique watercolor landscape with gold-leaf accents, Vietnamese highlands: misty pine hills, terraced green tea/fields, golden ripe rice in the foreground, and on the right a coffee branch bearing ONLY red and green coffee cherries with glossy leaves (no other fruit, no mango). 19th century botanical atlas style, no text, no letters."))
    return jobs

def backup(out):
    if not os.path.exists(out): return
    if '/ui/' in out.replace('\\','/'): bk = BK_U
    elif '/detail/' in out.replace('\\','/'): bk = BK_D
    else: bk = BK_M
    os.makedirs(bk, exist_ok=True)
    os.replace(out, os.path.join(bk, os.path.basename(out)))

def gen(out, ratio, prompt):
    tmp = out + '.new'
    for a in (1, 2):
        try:
            r = subprocess.run(["higgsfield","generate","create","seedream_v4_5","--aspect_ratio",ratio,"--prompt",prompt,"--wait"],
                               capture_output=True, text=True, timeout=360)
            url = (r.stdout or "").strip().splitlines()[-1].strip() if r.stdout.strip() else ""
            if url.startswith("http"):
                urllib.request.urlretrieve(url, tmp)
                if os.path.getsize(tmp) > 1000:
                    backup(out)                 # chỉ backup+thay khi ảnh mới tải OK
                    os.replace(tmp, out)
                    return f"OK   {os.path.basename(out)}"
        except Exception as e:
            if a == 2: return f"ERR  {os.path.basename(out)} :: {e} (giữ ảnh cũ)"
    if os.path.exists(tmp): os.remove(tmp)
    return f"FAIL {os.path.basename(out)} (giữ ảnh cũ)"

def main():
    jobs = build_jobs()
    print(f"Regen {len(jobs)} ảnh (backup -> _old-{TS})...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    miss = [os.path.basename(j[0]) for j in jobs if not os.path.exists(j[0])]
    print("THIẾU:", miss) if miss else print(f"ĐỦ {len(jobs)} ảnh.")

if __name__ == "__main__": main()
