#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen thumbnail (4:3) + ảnh chi tiết (3:4) cho 38 cây mới qua Higgsfield seedream_v4_5.
Chạy song song, có retry, bỏ qua file đã có. Foreground (in tiến độ).
Chạy: python3 scripts/gen-images-new.py"""
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

# id -> mô tả hình hoạ (đặc điểm thực vật để vẽ)
SUBJ = {
    "du-du": "Carica papaya papaya tree, tall hollow trunk topped with crown of large palmate lobed leaves, cluster of green and orange oblong fruits, small flowers",
    "mang-cut": "Garcinia mangostana mangosteen, dark glossy oval leaves, round deep purple fruit with thick rind, thick green calyx, cross-section showing white segments",
    "oi": "Psidium guajava guava, oval veined leaves, white flowers with many stamens, round guava fruit and cross-section with pink seedy flesh",
    "na": "Annona squamosa sugar apple, round green knobby segmented fruit, oval leaves, cross-section with white pulp and black seeds",
    "bo": "Persea americana avocado, dark green oval leaves, small flowers, pear-shaped green avocado and cross-section with yellow-green flesh and large round seed",
    "dua-thom": "Ananas comosus pineapple plant, rosette of long spiny sword-shaped leaves, single large pineapple fruit with leafy crown",
    "chanh-leo": "Passiflora edulis passion fruit, climbing vine with three-lobed leaves and tendrils, intricate purple and white passion flower, round purple fruit and cross-section with yellow seedy pulp",
    "vu-sua": "Chrysophyllum cainito star apple, leaves green above and coppery below, round purple fruit, cross-section with translucent white flesh",
    "khe": "Averrhoa carambola star fruit, pinnate leaves, small pink flowers, yellow five-ridged fruit and star-shaped cross-section",
    "nho": "Vitis vinifera grapevine, lobed grape leaves, curling tendrils, hanging cluster of round grapes",
    "hong": "Diospyros kaki persimmon, oval leaves, orange-red round persimmon fruit with calyx, cross-section",
    "bap-cai": "Brassica oleracea cabbage, round head of tightly wrapped pale green leaves, spreading outer leaves, roots",
    "ca-rot": "Daucus carota carrot, feathery fern-like green foliage above, long tapering orange root below, small white umbel flowers",
    "ot": "Capsicum annuum chili pepper plant, green leaves, small white flowers, red and green pointed chili peppers, cross-section with seeds",
    "ca-tim": "Solanum melongena eggplant, large leaves, purple star-shaped flowers, glossy deep purple elongated fruit, cross-section",
    "hanh-la": "Allium fistulosum green scallion, clumps of hollow green tubular leaves with white bulbous bases, fibrous roots, spherical flower head",
    "toi": "Allium sativum garlic, flat green leaves, white papery bulb, a bulb split open showing cloves, roots",
    "kho-qua": "Momordica charantia bitter melon, climbing vine with lobed leaves and tendrils, yellow flowers, warty oblong green fruit, cross-section with red seeds",
    "bi-do": "Cucurbita moschata pumpkin, large lobed leaves on creeping vine, yellow trumpet flowers, large ribbed orange pumpkin, cross-section with seeds",
    "su-su": "Sechium edule chayote, climbing vine with lobed leaves and tendrils, single pale green pear-shaped wrinkled fruit",
    "bau": "Lagenaria siceraria bottle gourd, climbing vine with soft leaves and tendrils, white flowers, long pale green bottle gourd fruit",
    "muop": "Luffa aegyptiaca luffa gourd, climbing vine with lobed leaves and tendrils, yellow flowers, long ridged green luffa fruit, fibrous cross-section",
    "xa-lach": "Lactuca sativa lettuce, loose rosette of crinkled soft green leaves, roots",
    "khoai-tay": "Solanum tuberosum potato plant, compound leaves, white and purple star flowers, underground tubers with eyes, roots",
    "khoai-mon": "Colocasia esculenta taro, large heart-shaped peltate leaves on tall stalks, brown corm tuber and roots underground",
    "dau-phong": "Arachis hypogaea peanut plant, low bushy plant with compound leaves, small yellow pea flowers, underground pods, peanut shells and seeds",
    "dau-nanh": "Glycine max soybean plant, trifoliate hairy leaves, small white and purple flowers, hairy green pods, round soybean seeds",
    "bong-vai": "Gossypium hirsutum cotton plant, lobed leaves, cream-yellow hibiscus-like flowers, brown bolls bursting with fluffy white cotton fiber, seeds",
    "giang-huong": "Pterocarpus macrocarpus padauk timber tree, pinnate compound leaves, bright yellow fragrant flower clusters, round winged seed pods, reddish-orange wood",
    "trac": "Dalbergia cochinchinensis Siamese rosewood tree, pinnate compound leaves, small white flowers, flat seed pods, dark reddish-brown heartwood cross-section",
    "sao-den": "Hopea odorata tall timber tree, lance-shaped leaves, small flowers, two-winged samara fruits, straight trunk with bark",
    "po-mu": "Fokienia hodginsii conifer, flattened scale-like foliage sprays, small round woody cones, pale fragrant wood",
    "sen-mat": "Madhuca pasquieri ironwood tree, oval leathery leaves clustered at branch tips, small flowers, oval fruit, very dark heartwood cross-section",
    "dau-rai": "Dipterocarpus alatus giant dipterocarp tree, large oval leaves, two long-winged samara fruits, very tall straight trunk, resin droplets",
    "xoan-ta": "Melia azedarach chinaberry tree, bipinnate compound leaves, clusters of lilac-purple fragrant flowers, round yellow berries",
    "que": "Cinnamomum cassia cinnamon tree, glossy lance leaves with three prominent veins, small flowers, rolled cinnamon bark quills, dried bark pieces",
    "hoi": "Illicium verum star anise, lance-shaped evergreen leaves, eight-pointed star-shaped brown fruit, glossy seeds, small flower",
    "tram-gio": "Melaleuca cajuputi cajuput tree, narrow lance-shaped leaves, white bottlebrush flower spikes, papery layered peeling bark, small woody capsules",
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


def build_jobs():
    jobs = []
    for cid, s in SUBJ.items():
        jobs.append((os.path.join(IMG, cid + ".jpg"), "4:3", STYLE_T.format(s=s)))
        jobs.append((os.path.join(DET, cid + ".jpg"), "3:4", STYLE_D.format(s=s)))
    return jobs


def main():
    jobs = build_jobs()
    todo = [j for j in jobs if not os.path.exists(j[0])]
    print(f"Tổng {len(jobs)} ảnh, cần gen {len(todo)} (bỏ {len(jobs)-len(todo)} đã có).")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1
            print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    # báo cáo thiếu
    missing = [os.path.basename(j[0]) for j in jobs if not os.path.exists(j[0])]
    if missing:
        print("THIẾU:", missing)
    else:
        print("ĐỦ HẾT 76 ảnh.")


if __name__ == "__main__":
    main()
