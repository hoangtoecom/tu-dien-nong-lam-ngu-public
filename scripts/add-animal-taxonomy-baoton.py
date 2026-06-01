#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bổ sung phanLoai (Bộ/Họ/Chi·Loài) + baoTon cho 60 loài chăn nuôi/thủy sản.
Phân hạng bảo tồn tra theo IUCN / CITES / Nghị định 84-2021 / Sách Đỏ VN.
Chạy: python3 scripts/add-animal-taxonomy-baoton.py"""
import json, os

BASE = os.path.join(os.path.dirname(__file__), '..')
F = os.path.join(BASE, 'data', 'tu-dien-nong-lam-ngu.json')

# baoTonCap: '' = không xếp hạng / phổ biến; LC/NT/VU/EN/CR theo IUCN.
# Loài nuôi thuần hóa → coi là phổ biến (không thuộc diện bảo tồn).
COMMON = "Vật nuôi phổ biến — không thuộc diện bảo tồn."
FARMED = "Loài nuôi phổ biến — không bị đe dọa."

# id -> (bo, ho, chi, loai, baoTon, baoTonCap)
TX = {
 # ----- GIA SÚC -----
 "bo-sua": ("Guốc chẵn (Artiodactyla)", "Trâu bò (Bovidae)", "Bos", "B. taurus", COMMON, ""),
 "bo-thit": ("Guốc chẵn (Artiodactyla)", "Trâu bò (Bovidae)", "Bos", "B. taurus", COMMON, ""),
 "trau": ("Guốc chẵn (Artiodactyla)", "Trâu bò (Bovidae)", "Bubalus", "B. bubalis", COMMON, ""),
 "lon": ("Guốc chẵn (Artiodactyla)", "Lợn (Suidae)", "Sus", "S. domesticus", COMMON, ""),
 "de": ("Guốc chẵn (Artiodactyla)", "Trâu bò (Bovidae)", "Capra", "C. hircus", COMMON, ""),
 "cuu": ("Guốc chẵn (Artiodactyla)", "Trâu bò (Bovidae)", "Ovis", "O. aries", COMMON, ""),
 # ----- GIA CẦM -----
 "ga": ("Gà (Galliformes)", "Trĩ (Phasianidae)", "Gallus", "G. gallus", COMMON, ""),
 "vit": ("Ngỗng (Anseriformes)", "Vịt (Anatidae)", "Anas", "A. platyrhynchos", COMMON, ""),
 "ngan": ("Ngỗng (Anseriformes)", "Vịt (Anatidae)", "Cairina", "C. moschata", COMMON, ""),
 "chim-cut": ("Gà (Galliformes)", "Trĩ (Phasianidae)", "Coturnix", "C. japonica", COMMON, ""),
 "bo-cau": ("Bồ câu (Columbiformes)", "Bồ câu (Columbidae)", "Columba", "C. livia", COMMON, ""),
 "ga-tay": ("Gà (Galliformes)", "Trĩ (Phasianidae)", "Meleagris", "M. gallopavo", COMMON, ""),
 "da-dieu": ("Đà điểu (Struthioniformes)", "Đà điểu (Struthionidae)", "Struthio", "S. camelus", COMMON, ""),
 # ----- VẬT NUÔI KHÁC -----
 "ong-mat": ("Cánh màng (Hymenoptera)", "Ong mật (Apidae)", "Apis", "A. cerana / A. mellifera", "Loài nuôi phổ biến — không bị đe dọa; có vai trò thụ phấn quan trọng cho nông nghiệp.", ""),
 "tho": ("Thỏ (Lagomorpha)", "Thỏ (Leporidae)", "Oryctolagus", "O. cuniculus", COMMON, ""),
 "tam": ("Cánh vảy (Lepidoptera)", "Ngài tằm (Bombycidae)", "Bombyx", "B. mori", "Loài thuần hóa hoàn toàn — không tồn tại ngoài tự nhiên, không thuộc diện bảo tồn.", ""),
 "trun-que": ("Haplotaxida", "Megascolecidae", "Perionyx", "P. excavatus", FARMED, ""),
 "de-men": ("Cánh thẳng (Orthoptera)", "Dế (Gryllidae)", "Gryllus", "G. bimaculatus", FARMED, ""),
 "nhim": ("Gặm nhấm (Rodentia)", "Nhím (Hystricidae)", "Hystrix", "H. brachyura", "IUCN Ít lo ngại (LC); bị săn bắt ngoài tự nhiên nên việc gây nuôi cần tuân thủ quy định về động vật hoang dã.", ""),
 # ----- THÚ ĐẶC SẢN (nhiều loài hoang dã) -----
 "huou-sao": ("Guốc chẵn (Artiodactyla)", "Hươu nai (Cervidae)", "Cervus", "C. nippon", "Toàn cầu Ít lo ngại (LC); riêng quần thể hoang dã ở Việt Nam gần như tuyệt chủng ngoài tự nhiên — đàn nuôi hiện là nguồn bảo tồn nguồn gen.", "NT"),
 "nai": ("Guốc chẵn (Artiodactyla)", "Hươu nai (Cervidae)", "Rusa", "R. unicolor", "Sắp nguy cấp (VU) theo IUCN; suy giảm ngoài tự nhiên ở Việt Nam do săn bắt và mất sinh cảnh. Gây nuôi cần nguồn gốc hợp pháp.", "VU"),
 "dui": ("Gặm nhấm (Rodentia)", "Dúi (Spalacidae)", "Rhizomys", "Rhizomys sp.", "IUCN Ít lo ngại (LC); là động vật hoang dã, gây nuôi thương mại phải đăng ký theo quy định.", ""),
 "chon-huong": ("Ăn thịt (Carnivora)", "Cầy (Viverridae)", "Paradoxurus", "P. hermaphroditus", "IUCN Ít lo ngại (LC); thuộc nhóm động vật rừng được quản lý, gây nuôi cần đăng ký trại nuôi.", ""),
 "cay-voi-huong": ("Ăn thịt (Carnivora)", "Cầy (Viverridae)", "Paguma", "P. larvata", "IUCN Ít lo ngại (LC); là động vật hoang dã, gây nuôi cần tuân thủ quy định và đăng ký.", ""),
 "heo-rung": ("Guốc chẵn (Artiodactyla)", "Lợn (Suidae)", "Sus", "S. scrofa", "IUCN Ít lo ngại (LC); heo rừng nuôi/lai phổ biến, gây nuôi cần nguồn gốc rõ ràng.", ""),
 # ----- BÒ SÁT NUÔI (CITES / Nghị định 84) -----
 "ca-sau": ("Cá sấu (Crocodilia)", "Cá sấu (Crocodylidae)", "Crocodylus", "C. siamensis", "Cực kỳ nguy cấp (CR) theo IUCN; CITES Phụ lục I với quần thể hoang dã (trại nuôi đăng ký thuộc Phụ lục II); Sách Đỏ Việt Nam. Cá thể nuôi thương mại phải có nguồn gốc hợp pháp.", "CR"),
 "ran-ho-trau": ("Có vảy (Squamata)", "Rắn nước (Colubridae)", "Ptyas", "P. mucosa", "CITES Phụ lục II; Việt Nam liệt kê trong danh mục động vật rừng nguy cấp, quý, hiếm (nhóm IIB). Bị khai thác mạnh, gây nuôi cần đăng ký.", "NT"),
 "ky-da": ("Có vảy (Squamata)", "Kỳ đà (Varanidae)", "Varanus", "V. salvator", "CITES Phụ lục II; Việt Nam nhóm IIB (Nghị định 84/2021). IUCN Ít lo ngại nhưng bị săn bắt nhiều — gây nuôi phải đăng ký.", "NT"),
 "tran": ("Có vảy (Squamata)", "Trăn (Pythonidae)", "Python", "P. bivittatus", "Sắp nguy cấp (VU) theo IUCN; CITES Phụ lục II; Việt Nam nhóm IIB (Nghị định 84/2021). Nuôi thương mại cần đăng ký trại nuôi.", "VU"),
 "tac-ke": ("Có vảy (Squamata)", "Tắc kè (Gekkonidae)", "Gekko", "G. gecko", "CITES Phụ lục II (từ 2019); bị khai thác mạnh làm dược liệu nên quần thể tự nhiên suy giảm. Gây nuôi cần tuân thủ quy định.", "NT"),
 # ----- CÁ NUÔI -----
 "ca-tra": ("Cá da trơn (Siluriformes)", "Cá tra (Pangasiidae)", "Pangasius", "P. hypophthalmus", "Loài nuôi xuất khẩu chủ lực — không bị đe dọa trong nuôi trồng (IUCN Ít lo ngại).", ""),
 "ca-basa": ("Cá da trơn (Siluriformes)", "Cá tra (Pangasiidae)", "Pangasius", "P. bocourti", FARMED, ""),
 "ca-ro-phi": ("Cá vược (Cichliformes)", "Cá rô phi (Cichlidae)", "Oreochromis", "O. niloticus", FARMED, ""),
 "ca-dieu-hong": ("Cá vược (Cichliformes)", "Cá rô phi (Cichlidae)", "Oreochromis", "Oreochromis sp.", "Giống lai chọn tạo từ cá rô phi — loài nuôi phổ biến, không bị đe dọa.", ""),
 "ca-loc": ("Cá rô đồng (Anabantiformes)", "Cá quả (Channidae)", "Channa", "C. striata", FARMED, ""),
 "ca-chep": ("Cá chép (Cypriniformes)", "Cá chép (Cyprinidae)", "Cyprinus", "C. carpio", FARMED, ""),
 "ca-tram-co": ("Cá chép (Cypriniformes)", "Cá chép (Cyprinidae)", "Ctenopharyngodon", "C. idella", FARMED, ""),
 "ca-keo": ("Cá bống (Gobiiformes)", "Cá bống trắng (Gobiidae)", "Pseudapocryptes", "P. elongatus", FARMED, ""),
 "ca-chach": ("Cá chép (Cypriniformes)", "Cá chạch (Cobitidae)", "Misgurnus", "M. anguillicaudatus", FARMED, ""),
 # ----- GIÁP XÁC -----
 "tom-the": ("Mười chân (Decapoda)", "Tôm he (Penaeidae)", "Litopenaeus", "L. vannamei", "Loài nuôi xuất khẩu chủ lực — không bị đe dọa.", ""),
 "tom-su": ("Mười chân (Decapoda)", "Tôm he (Penaeidae)", "Penaeus", "P. monodon", FARMED, ""),
 "cua-bien": ("Mười chân (Decapoda)", "Cua bơi (Portunidae)", "Scylla", "S. serrata", FARMED, ""),
 "tom-cang-xanh": ("Mười chân (Decapoda)", "Tôm càng (Palaemonidae)", "Macrobrachium", "M. rosenbergii", FARMED, ""),
 "ghe": ("Mười chân (Decapoda)", "Cua bơi (Portunidae)", "Portunus", "P. pelagicus", "Khai thác & nuôi phổ biến — không bị đe dọa; cần quản lý đánh bắt để tránh suy giảm.", ""),
 # ----- THỦY SẢN KHÁC -----
 "ngheu": ("Venerida", "Ngao (Veneridae)", "Meretrix", "M. lyrata", FARMED, ""),
 "hau": ("Ostreida", "Hàu (Ostreidae)", "Crassostrea", "Crassostrea sp.", FARMED, ""),
 "ech": ("Không đuôi (Anura)", "Ếch nhái chính thức (Dicroglossidae)", "Hoplobatrachus", "H. rugulosus", "IUCN Ít lo ngại (LC); nuôi thương mại phổ biến.", ""),
 "luon": ("Mang liền (Synbranchiformes)", "Lươn (Synbranchidae)", "Monopterus", "M. albus", FARMED, ""),
 "oc-buou-den": ("Architaenioglossa", "Ốc bươu (Ampullariidae)", "Pila", "P. polita", "Loài bản địa được nuôi phổ biến — không bị đe dọa (phân biệt với ốc bươu vàng xâm hại).", ""),
 "ba-ba": ("Rùa (Testudines)", "Ba ba (Trionychidae)", "Pelodiscus", "P. sinensis", "Sắp nguy cấp (VU) theo IUCN do khai thác quá mức ngoài tự nhiên; nuôi thương mại phổ biến tại Việt Nam.", "VU"),
 # ----- CÁ BIỂN -----
 "ca-mu": ("Cá vược (Perciformes)", "Cá mú (Serranidae)", "Epinephelus", "Epinephelus sp.", "Phần lớn loài cá mú nuôi không bị đe dọa; một số loài tự nhiên bị khai thác quá mức — nên ưu tiên con giống sinh sản nhân tạo.", ""),
 "ca-chem": ("Cá vược (Perciformes)", "Cá chẽm (Latidae)", "Lates", "L. calcarifer", FARMED, ""),
 "ca-bop": ("Cá khế (Carangiformes)", "Cá bớp (Rachycentridae)", "Rachycentron", "R. canadum", FARMED, ""),
 "ca-hong-my": ("Cá vược (Perciformes)", "Cá đù (Sciaenidae)", "Sciaenops", "S. ocellatus", FARMED, ""),
 "ca-mang": ("Cá măng (Gonorynchiformes)", "Cá măng (Chanidae)", "Chanos", "C. chanos", FARMED, ""),
 # ----- NHUYỄN THỂ / RONG -----
 "so-huyet": ("Arcida", "Sò (Arcidae)", "Anadara", "A. granosa", FARMED, ""),
 "oc-huong": ("Neogastropoda", "Babyloniidae", "Babylonia", "B. areolata", "Loài nuôi giá trị cao — không bị đe dọa; quần thể tự nhiên cần quản lý khai thác.", ""),
 "vem-xanh": ("Mytilida", "Vẹm (Mytilidae)", "Perna", "P. viridis", FARMED, ""),
 "rong-nho": ("Bryopsidales", "Rong cầu lục (Caulerpaceae)", "Caulerpa", "C. lentillifera", "Rong biển nuôi trồng phổ biến — không bị đe dọa.", ""),
 "rong-sun": ("Gigartinales", "Rong sụn (Solieriaceae)", "Kappaphycus", "K. alvarezii", "Rong biển nuôi trồng phổ biến — không bị đe dọa.", ""),
}

def main():
    d = json.load(open(F, encoding='utf-8'))
    items = d['cay']
    done = 0; missing = []
    for x in items:
        if str(x.get('linhVuc')) not in ('chan-nuoi', 'thuy-san'):
            continue
        t = TX.get(x['id'])
        if not t:
            missing.append(x['id']); continue
        bo, ho, chi, loai, baoTon, cap = t
        x['phanLoai'] = {"bo": bo, "ho": ho, "chi": chi, "loai": loai}
        if not str(x.get('ho', '')).strip():
            x['ho'] = ho
        x['baoTon'] = baoTon
        # Vật nuôi thương mại KHÔNG gắn cờ bảo tồn: cờ IUCN theo quần thể HOANG DÃ
        # gây hiểu nhầm trong từ điển chăn nuôi/thủy sản (loài nuôi vốn phổ biến).
        # Phần text baoTon vẫn giữ (nêu rõ tình trạng hoang dã vs nuôi thương mại).
        x['baoTonCap'] = ''
        done += 1
    d['_meta']['capNhat'] = '2026-05-30'
    json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"DONE: enriched {done}/60 animal items. missing={missing}")

if __name__ == '__main__':
    main()
