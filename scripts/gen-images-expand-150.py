#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gen 30 ảnh mở rộng lên 150 loài. Cây → style thực vật; con vật → style động vật.
Chạy: python3 scripts/gen-images-expand-150.py"""
import os, subprocess, urllib.request, concurrent.futures as cf
BASE = os.path.join(os.path.dirname(__file__), '..'); IMG = os.path.join(BASE, 'img')
os.makedirs(IMG, exist_ok=True)
BOTAN = ("Antique botanical illustration plate of {s}, on clean white background, vintage scientific "
         "watercolor engraving, 19th century botanical art, no text, no letters, no labels")
ZOO = ("Antique zoological illustration plate of {s}, vintage scientific watercolor engraving, "
       "19th century natural history art, clean white background, no text, no letters, no labels")
PLANTS = {
  "mong-toi":"Basella alba Malabar spinach vine, thick heart-shaped fleshy green leaves, small pink-purple flower spikes, dark berries",
  "rau-den":"Amaranthus amaranth plant, upright stem, oval green and red leaves, dense drooping flower spikes",
  "hanh-tim":"Allium ascalonicum shallot, cluster of small purple-red bulbs, long hollow green leaves and roots",
  "hong-xiem":"Manilkara zapota sapodilla branch, glossy oval evergreen leaves, round brown fruit, cross-section showing brown flesh and black seeds",
  "mun":"Diospyros mun ebony tree, slender trunk, small glossy oval leaves, very dark black heartwood cross-section",
  "hoang-dan":"Cupressus cypress conifer branch, scale-like aromatic green foliage, small round brown cones, reddish bark",
  "keo-la-tram":"Acacia auriculiformis tree, curved sickle-shaped phyllodes, yellow flower spikes, twisted curly brown seed pods",
  "tre-gai":"Bambusa thorny bamboo, tall jointed green culms with nodes, lance-shaped leaves, branching thorns",
  "song-may":"Calamus rattan palm, long slender spiny climbing stem, pinnate feathery green leaves",
  "boi-loi-do":"Litsea glutinosa tree branch, oval glossy leaves, small yellow flower clusters, small round fruit, reddish bark",
}
ANIMALS = {
  "bo-thit":"Bos taurus Vietnamese yellow beef cattle, tan brown coat, muscular body, short horns, full body side profile",
  "cuu":"Ovis aries domestic sheep, thick woolly white fleece, curled horns, side profile",
  "huou-sao":"Cervus nippon sika deer, reddish-brown coat with white spots, branching antlers, side profile",
  "bo-cau":"Columba livia domestica pigeon, grey plumage, iridescent green-purple neck, standing",
  "ga-tay":"Meleagris gallopavo domestic turkey, large fanned tail, red wattled head, bronze plumage, side profile",
  "da-dieu":"Struthio camelus ostrich, tall long bare neck, black and white plumage, long powerful legs, full body",
  "tam":"Bombyx mori silkworm, plump white caterpillar on green mulberry leaf, plus a white silk cocoon",
  "trun-que":"Perionyx excavatus red earthworm, reddish segmented worm body on dark compost soil",
  "de-men":"Gryllus field cricket insect, dark brown glossy body, long antennae, large hind legs",
  "nhim":"Hystrix porcupine, body covered with long black and white quills, side profile",
  "ca-chep":"Cyprinus carpio common carp, golden bronze body, large scales, pair of barbels, side profile",
  "ca-tram-co":"Ctenopharyngodon idella grass carp, elongated olive-silver body, large scales, side profile",
  "ca-basa":"Pangasius bocourti basa catfish, plump silvery body, barbels, short dorsal fin, side profile",
  "ca-keo":"Pseudapocryptes goby fish, elongated slender brownish mottled body, side profile",
  "ca-chinh":"Anguilla marbled eel, long snake-like smooth body, small fins, side profile",
  "tom-cang-xanh":"Macrobrachium rosenbergii giant freshwater prawn, long blue-green claws, translucent body, antennae",
  "ghe":"Portunus pelagicus blue swimming crab, blue mottled carapace, paddle-shaped swimming legs, claws, top view",
  "luon":"Monopterus albus Asian swamp eel, long smooth yellowish-brown body, side profile",
  "oc-buou-den":"Pila polita black apple snail, round dark spiral shell with operculum, on white",
  "ba-ba":"Pelodiscus sinensis Chinese softshell turtle, flat olive leathery carapace, long neck, webbed feet, top view",
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
    jobs = [(os.path.join(IMG, k+".jpg"), "4:3", BOTAN.format(s=s)) for k, s in PLANTS.items()]
    jobs += [(os.path.join(IMG, k+".jpg"), "4:3", ZOO.format(s=s)) for k, s in ANIMALS.items()]
    print(f"Gen {len(jobs)} ảnh...")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(gen, *j): j for j in jobs}
        for fu in cf.as_completed(futs):
            done += 1; print(f"[{done}/{len(jobs)}] {fu.result()}", flush=True)
    print("=== DONE ===")
if __name__ == "__main__":
    main()
