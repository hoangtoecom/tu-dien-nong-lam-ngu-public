#!/usr/bin/env bash
# Gen ảnh cây: thumbnail lâm nghiệp + detail cho tất cả 32 cây
# Chạy: bash scripts/gen-images.sh
# Kết quả: img/<id>.jpg và img/detail/<id>.jpg

set -e
IMG_DIR="$(cd "$(dirname "$0")/.." && pwd)/img"
DETAIL_DIR="$IMG_DIR/detail"
mkdir -p "$DETAIL_DIR"

gen() {
  local OUT="$1"; local RATIO="$2"; local PROMPT="$3"
  if [ -f "$OUT" ]; then echo "SKIP (exists): $OUT"; return; fi
  local URL
  URL=$(higgsfield generate create seedream_v4_5 --aspect_ratio "$RATIO" --prompt "$PROMPT" --wait 2>&1)
  if echo "$URL" | grep -q "https://"; then
    curl -sL "$URL" -o "$OUT" && echo "SAVED: $OUT"
  else
    echo "ERROR for $OUT: $URL"
  fi
}

# === LÂM NGHIỆP THUMBNAILS (4:3) ===
gen "$IMG_DIR/keo.jpg" "4:3" \
  "Antique botanical illustration plate of Acacia mangium, wattle tree, showing phyllodes flattened leaves, cylindrical cream flower spikes, twisted seed pods, detailed stem and bark, clean white background, vintage scientific watercolor engraving, 19th century botanical art, no text, no letters" &

gen "$IMG_DIR/bach-dan.jpg" "4:3" \
  "Antique botanical illustration plate of Eucalyptus camaldulensis, river red gum, showing lance-shaped leaves, white flower clusters with fluffy stamens, gum nuts, fibrous brown bark strips, clean white background, vintage scientific watercolor engraving, 19th century botanical art, no text, no letters" &

gen "$IMG_DIR/thong.jpg" "4:3" \
  "Antique botanical illustration plate of Pinus merkusii, Merkus pine, showing paired pine needles, brown pine cones, resin-covered branch, bark texture detail, clean white background, vintage scientific watercolor engraving, 19th century botanical art, no text, no letters" &

gen "$IMG_DIR/lat-hoa.jpg" "4:3" \
  "Antique botanical illustration plate of Chukrasia tabularis, Indian redwood, showing pinnate compound leaves, small white flowers in panicles, round woody capsule fruit, dark red-brown heartwood cross-section, clean white background, vintage scientific watercolor engraving, 19th century botanical art, no text, no letters" &

gen "$IMG_DIR/tram-trang.jpg" "4:3" \
  "Antique botanical illustration plate of Canarium album, white canarium olive tree, showing pinnate compound leaves, small white flowers, green oval drupe fruit, resin droplets on branch, clean white background, vintage scientific watercolor engraving, 19th century botanical art, no text, no letters" &

wait
echo "=== THUMBNAIL LÂM NGHIỆP DONE ==="

# === DETAIL IMAGES (3:4 portrait, full plant) ===
gen "$DETAIL_DIR/lua.jpg" "3:4" \
  "Antique botanical illustration plate of Oryza sativa rice plant, full plant from roots to grain panicle, showing root system, hollow jointed stems, long narrow leaves, drooping seed panicle with rice grains, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/ngo.jpg" "3:4" \
  "Antique botanical illustration plate of Zea mays maize corn plant, full plant from roots to tassel, showing root system, thick jointed stalk, broad leaves with parallel veins, ear of corn with husk and exposed kernels, male tassel flowers, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/san.jpg" "3:4" \
  "Antique botanical illustration plate of Manihot esculenta cassava plant, full plant from tuberous roots to crown, showing large starchy roots, green palmate leaves, thin stems, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/khoai-lang.jpg" "3:4" \
  "Antique botanical illustration plate of Ipomoea batatas sweet potato plant, full plant showing trailing vines, heart-shaped leaves, purple funnel-shaped flowers, swollen storage roots cross-section, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/ca-phe.jpg" "3:4" \
  "Antique botanical illustration plate of Coffea arabica coffee plant, full branch study showing dark glossy leaves, white jasmine-like flowers, green and red coffee cherries, coffee beans cross-section, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/cao-su.jpg" "3:4" \
  "Antique botanical illustration plate of Hevea brasiliensis rubber tree, full plant study showing compound trifoliate leaves, small flowers, three-lobed capsule fruits, latex oozing from scored bark, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/ho-tieu.jpg" "3:4" \
  "Antique botanical illustration plate of Piper nigrum black pepper vine, full plant showing climbing vine, heart-shaped leaves with veins, long slender flower spike, green and red peppercorns, root and stem details, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/dieu.jpg" "3:4" \
  "Antique botanical illustration plate of Anacardium occidentale cashew tree, full plant from roots to crown, showing oval leathery leaves, pink-white flowers, cashew apple with hanging kidney-shaped nut, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

wait
echo "=== DETAIL BATCH 1 DONE ==="

gen "$DETAIL_DIR/che.jpg" "3:4" \
  "Antique botanical illustration plate of Camellia sinensis tea plant, full plant showing oval serrated leaves, white five-petal flowers with yellow stamens, small round fruits, root system, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/mia.jpg" "3:4" \
  "Antique botanical illustration plate of Saccharum officinarum sugarcane plant, full tall plant from roots to plume, showing fibrous root system, thick jointed cane stems, long ribbon-like leaves, silky plume flower head, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/ca-cao.jpg" "3:4" \
  "Antique botanical illustration plate of Theobroma cacao cacao tree, showing cauliflorous fruits growing directly on trunk, large oval pod cross-section revealing white pulp and cacao seeds, waxy leaves, small pink flowers, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/thanh-long.jpg" "3:4" \
  "Antique botanical illustration plate of Selenicereus undatus dragon fruit cactus, full plant showing climbing jointed cactus stems with aerial roots, large white night-blooming flower, pink scaly fruit and cross-section revealing white flesh with black seeds, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/sau-rieng.jpg" "3:4" \
  "Antique botanical illustration plate of Durio zibethinus durian tree, full study showing large pinnate leaves, cauliflorous flower clusters on trunk, massive spiky fruit with opened section revealing yellow arils and seeds, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/xoai.jpg" "3:4" \
  "Antique botanical illustration plate of Mangifera indica mango tree, full branch study showing long lance-shaped leaves at various growth stages, panicle of small flowers, ripe golden mango fruit and cross-section, seed, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/chuoi.jpg" "3:4" \
  "Antique botanical illustration plate of Musa paradisiaca banana plant, full plant showing pseudostem formed by leaf sheaths, large paddle-shaped leaves, hanging bunch of bananas with purple flower bract, root system, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/cam.jpg" "3:4" \
  "Antique botanical illustration plate of Citrus sinensis orange tree, full branch study showing glossy dark green leaves, white fragrant flowers, cross-section of ripe orange showing segments and seeds, whole fruit, leaf oil glands, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

wait
echo "=== DETAIL BATCH 2 DONE ==="

gen "$DETAIL_DIR/buoi.jpg" "3:4" \
  "Antique botanical illustration plate of Citrus maxima pomelo tree, full branch study showing large round fruit, white flowers, large glossy leaves, fruit cross-section showing thick pith and segments, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/nhan.jpg" "3:4" \
  "Antique botanical illustration plate of Dimocarpus longan longan tree, full branch study showing pinnate compound leaves, small yellow flowers in panicles, cluster of round fruits with papery brown skin, flesh surrounding seed, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/vai.jpg" "3:4" \
  "Antique botanical illustration plate of Litchi chinensis lychee tree, full branch study showing pinnate compound leaves, panicle of small flowers, cluster of red warty fruits, peeled fruit showing white translucent flesh and seed, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/chom-chom.jpg" "3:4" \
  "Antique botanical illustration plate of Nephelium lappaceum rambutan tree, full branch study showing compound leaves, small flowers, cluster of red hairy rambutan fruits, peeled fruit showing white flesh and seed, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/mit.jpg" "3:4" \
  "Antique botanical illustration plate of Artocarpus heterophyllus jackfruit tree, full study showing large oblong fruit directly on trunk, opened fruit with yellow arils and seeds, large dark green leaves, small male and female flower spikes, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/dua.jpg" "3:4" \
  "Antique botanical illustration plate of Cocos nucifera coconut palm, full palm from roots to crown, showing tall smooth trunk, feathery compound fronds, coconut flower spike, green and brown coconuts, coconut cross-section with husk, shell, white flesh and liquid, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/rau-muong.jpg" "3:4" \
  "Antique botanical illustration plate of Ipomoea aquatica water spinach, full plant study showing hollow floating stems, heart-shaped to arrow-shaped leaves, purple funnel-shaped morning glory flowers, root and growing tips, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/cai-xanh.jpg" "3:4" \
  "Antique botanical illustration plate of Brassica juncea mustard greens plant, full plant showing rosette of large frilly dark green leaves with purple tinge, yellow four-petal flowers, seed pods, root system, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

wait
echo "=== DETAIL BATCH 3 DONE ==="

gen "$DETAIL_DIR/ca-chua.jpg" "3:4" \
  "Antique botanical illustration plate of Solanum lycopersicum tomato plant, full plant from roots to fruit, showing pinnate compound leaves, yellow star-shaped flowers, cluster of green ripening and red ripe tomatoes, fruit cross-section showing chambers and seeds, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/dua-leo.jpg" "3:4" \
  "Antique botanical illustration plate of Cucumis sativus cucumber vine, full plant showing climbing vine with tendrils, three-lobed leaves, yellow flowers, cylindrical fruit with bumpy skin, fruit cross-section showing watery flesh and seeds, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/tech.jpg" "3:4" \
  "Antique botanical illustration plate of Tectona grandis teak tree, full plant study from roots to crown, showing massive oval leaves up to 60cm, clusters of white tubular flowers, woody drupe fruits, deeply grooved bark, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/keo.jpg" "3:4" \
  "Antique botanical illustration plate of Acacia mangium wattle tree, full plant study showing phyllodes flattened leaf-like structures, long cylindrical cream-yellow flower spikes, coiled seed pods releasing shiny seeds, grey fibrous bark, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/bach-dan.jpg" "3:4" \
  "Antique botanical illustration plate of Eucalyptus camaldulensis river red gum tree, full plant study showing juvenile round leaves and mature lance-shaped leaves, white fluffy flower clusters, woody gum nut capsules, fibrous red-brown bark strips peeling, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/thong.jpg" "3:4" \
  "Antique botanical illustration plate of Pinus merkusii Merkus pine tree, full plant from roots to crown, showing paired long slender needles in bundles, brown oval pine cones at various stages, resin canals in bark cross-section, root system, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/lat-hoa.jpg" "3:4" \
  "Antique botanical illustration plate of Chukrasia tabularis Indian redwood tree, full plant study showing pinnate compound leaves, panicles of small white flowers, round woody fruit capsule splitting open to release winged seeds, dark red-brown heartwood cross-section, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

gen "$DETAIL_DIR/tram-trang.jpg" "3:4" \
  "Antique botanical illustration plate of Canarium album white canarium tree, full plant study showing large pinnate compound leaves, panicles of small white flowers, clusters of green oval drupe fruits, resin droplets, stone fruit cross-section, detailed botanical study, vintage scientific watercolor and ink, 19th century, clean white background, no text, no letters" &

wait
echo "=== ALL IMAGES DONE ==="
