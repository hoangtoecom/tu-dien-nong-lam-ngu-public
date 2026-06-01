#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restructure từ điển sang 2 cấp + thêm nhóm gia vị + 20 cây mới.
- Thêm field `linhVuc` (nong-nghiep / lam-nghiep) cho mọi cây.
- Tách 'lam-nghiep' → nhóm con: go-quy / trong-rung / lam-san.
- Tạo nhóm 'gia-vi' (chuyển tỏi+ớt sang, thêm 6 cây gia vị).
- Thêm 14 cây lâm nghiệp phổ biến.
Chạy: python3 scripts/restructure-plants.py (idempotent — chạy lại an toàn)"""
import json, os

base = os.path.join(os.path.dirname(__file__), '..')
path = os.path.join(base, 'data', 'tu-dien-nong-lam-ngu.json')

# Map cây lâm nghiệp hiện có -> nhóm con
LAM_SUB = {
    "tech": "go-quy", "lat-hoa": "go-quy", "giang-huong": "go-quy", "trac": "go-quy",
    "sao-den": "go-quy", "po-mu": "go-quy", "sen-mat": "go-quy", "dau-rai": "go-quy",
    "keo": "trong-rung", "bach-dan": "trong-rung", "thong": "trong-rung", "xoan-ta": "trong-rung",
    "tram-trang": "lam-san", "que": "lam-san", "hoi": "lam-san", "tram-gio": "lam-san",
}


def ls(*pairs):
    return [{"giaiDoan": g, "thoiGian": t} for g, t in pairs]


def P(id, ten, sci, khac, ho, linhVuc, nhom, bo, chi, loai, xuatXu, moTa, loaiThan,
      chieuCao, chuKy, anhSang, nuoc, loaiDat, vungTrong, muaVu, dieuKien,
      nhanGiong, thuHoach, nangSuat, lich, sauBenh, giaTri, dinhDuong,
      huongVi, yhct, thiTruong, thuVi, mau, nguon):
    return {
        "id": id, "ten": ten, "tenKhoaHoc": sci, "tenKhac": khac, "ho": ho,
        "linhVuc": linhVuc, "nhom": nhom,
        "anh": f"img/{id}.jpg", "anhChiTiet": f"img/detail/{id}.jpg",
        "xuatXu": xuatXu,
        "phanLoai": {"bo": bo, "ho": ho, "chi": chi, "loai": loai},
        "moTa": moTa, "loaiThan": loaiThan, "chieuCao": chieuCao, "chuKy": chuKy,
        "anhSang": anhSang, "nuoc": nuoc, "loaiDat": loaiDat, "vungTrong": vungTrong,
        "muaVu": muaVu, "dieuKien": dieuKien, "nhanGiong": nhanGiong,
        "thoiGianThuHoach": thuHoach, "nangSuat": nangSuat, "lichSinhTruong": lich,
        "sauBenh": sauBenh, "giaTri": giaTri, "dinhDuong": dinhDuong,
        "huongVi": huongVi, "yHocCoTruyen": yhct, "thiTruong": thiTruong,
        "suThatThuVi": thuVi, "mauDacTrung": mau, "nguon": nguon,
    }


NEW = [
    # ===== GIA VỊ – DƯỢC LIỆU (6 mới) =====
    P("gung", "Gừng", "Zingiber officinale", "Ginger · sinh khương", "Gừng (Zingiberaceae)",
      "nong-nghiep", "gia-vi", "Gừng (Zingiberales)", "Zingiber", "Z. officinale",
      "Có nguồn gốc Đông Nam Á; gia vị & dược liệu lâu đời, trồng khắp Việt Nam.",
      "Gừng là cây lấy củ (thân rễ) cay ấm; vừa là gia vị thiết yếu vừa là vị thuốc quen thuộc.",
      "Cây thân thảo, thân rễ (củ) phình ngầm", "0,5–1 m", "Cây hàng năm (8–10 tháng)",
      "Ưa nắng, chịu bóng nhẹ", "Trung bình — ẩm đều, sợ úng", "Đất tơi xốp, giàu mùn, thoát nước",
      "Khắp cả nước, nhiều ở trung du & miền núi", "Trồng xuân (2–4), thu củ sau 8–10 tháng",
      "Ưa ẩm, đất tơi cho củ to; tránh úng gây thối củ",
      "Trồng bằng củ giống (hom)", "8–10 tháng sau trồng", "15–25 tấn củ/ha",
      ls(("Trồng hom củ", "Tháng 0"), ("Mọc mầm & ra lá", "Tháng 1–3"),
         ("Phình củ", "Tháng 3–8"), ("Thu hoạch", "Tháng 8–10")),
      "Sâu đục thân, bệnh thối củ, cháy lá",
      "Gia vị thiết yếu; mứt gừng, trà gừng, tinh dầu; dược liệu",
      "Chứa gingerol, tinh dầu; ít calo", "Cay nồng, ấm, thơm",
      "Gừng ấm bụng, trị cảm lạnh, say tàu xe, buồn nôn (Đông y)",
      "Gừng tươi, gừng khô & tinh dầu tiêu thụ rộng, có xuất khẩu",
      "Bộ phận dùng của gừng là thân rễ mọc ngầm, không phải rễ — nên gọi đúng là 'củ thân rễ'",
      ["#E3C16F", "#C8794A"], "https://vi.wikipedia.org/wiki/G%E1%BB%ABng"),

    P("nghe", "Nghệ", "Curcuma longa", "Turmeric · khương hoàng", "Gừng (Zingiberaceae)",
      "nong-nghiep", "gia-vi", "Gừng (Zingiberales)", "Curcuma", "C. longa",
      "Có nguồn gốc Nam & Đông Nam Á; gia vị, phẩm màu & dược liệu trồng khắp Việt Nam.",
      "Nghệ là cây lấy củ (thân rễ) vàng cam; tạo màu & hương cho món ăn, đồng thời là dược liệu quý (curcumin).",
      "Cây thân thảo, thân rễ vàng ngầm", "0,8–1,2 m", "Cây hàng năm (8–10 tháng)",
      "Ưa nắng, chịu bóng nhẹ", "Trung bình — ẩm đều, sợ úng", "Đất tơi xốp, giàu mùn, thoát nước",
      "Khắp cả nước, nhiều ở miền Trung & Tây Bắc", "Trồng xuân (2–4), thu củ sau 8–10 tháng",
      "Ưa ẩm, đất tơi; thu khi lá úa vàng cuối chu kỳ",
      "Trồng bằng củ giống (hom)", "8–10 tháng sau trồng", "20–30 tấn củ/ha",
      ls(("Trồng hom củ", "Tháng 0"), ("Mọc mầm & ra lá", "Tháng 1–3"),
         ("Phình củ", "Tháng 3–8"), ("Thu hoạch", "Tháng 8–10")),
      "Bệnh thối củ, cháy lá, rệp",
      "Gia vị & tạo màu vàng; tinh bột nghệ, viên curcumin; dược liệu giá trị cao",
      "Chứa curcumin chống viêm, chống oxy hóa", "Hơi đắng, thơm ấm, màu vàng cam",
      "Nghệ trị đau dạ dày, làm lành vết thương, đẹp da (curcumin)",
      "Tinh bột nghệ & curcumin chế biến giá trị gia tăng, xuất khẩu",
      "Màu vàng của nghệ đến từ curcumin — chất đang được nghiên cứu nhiều về kháng viêm",
      ["#E8A33D", "#C8521E"], "https://vi.wikipedia.org/wiki/Ngh%E1%BB%87"),

    P("sa", "Sả", "Cymbopogon citratus", "Lemongrass · sả chanh", "Hòa thảo (Poaceae)",
      "nong-nghiep", "gia-vi", "Hòa thảo (Poales)", "Cymbopogon", "C. citratus",
      "Có nguồn gốc nhiệt đới châu Á; cây gia vị & tinh dầu trồng khắp Việt Nam, dễ tính.",
      "Sả là cây cỏ bụi thơm mùi chanh; gia vị quen thuộc, đuổi muỗi và cho tinh dầu thơm.",
      "Cây cỏ lâu năm, mọc bụi, thân giả", "0,8–1,5 m", "Cây lâu năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn tốt", "Đất tơi xốp, thoát nước, thích nghi rộng",
      "Khắp cả nước, vườn nhà & trồng tinh dầu", "Trồng quanh năm, thu nhiều đợt",
      "Dễ trồng, chịu hạn, ít sâu bệnh; tách bụi nhân giống nhanh",
      "Tách bụi (nhánh sả)", "Thu sau 3–4 tháng, cắt nhiều đợt", "20–40 tấn/ha/năm (lá+thân)",
      ls(("Trồng nhánh", "Tháng 0"), ("Đẻ nhánh thành bụi", "Tháng 1–3"),
         ("Thu cắt", "Tháng 3+"), ("Tái sinh liên tục", "Quanh năm")),
      "Ít sâu bệnh; đôi khi rệp, cháy lá",
      "Gia vị (kho, nướng, lẩu); tinh dầu sả đuổi muỗi, hương liệu, mỹ phẩm",
      "Chứa citral (tinh dầu); ít calo", "Thơm mùi chanh, cay nhẹ",
      "Sả giải cảm, kích thích tiêu hóa; tinh dầu sả đuổi muỗi, thư giãn",
      "Tinh dầu sả & sả tươi tiêu thụ rộng, có xuất khẩu",
      "Mùi chanh đặc trưng của sả đến từ citral — cũng là chất khiến muỗi tránh xa",
      ["#9CB04A", "#E3C16F"], "https://vi.wikipedia.org/wiki/S%E1%BA%A3_chanh"),

    P("rieng", "Riềng", "Alpinia officinarum", "Galangal · cao lương khương", "Gừng (Zingiberaceae)",
      "nong-nghiep", "gia-vi", "Gừng (Zingiberales)", "Alpinia", "A. officinarum",
      "Có nguồn gốc Đông Nam Á & Nam Trung Quốc; gia vị & dược liệu quen thuộc, nhất là miền Bắc.",
      "Riềng là cây lấy củ (thân rễ) cay thơm; gia vị đặc trưng món kho, giả cầy, mẻ; cũng là vị thuốc.",
      "Cây thân thảo, thân rễ ngầm cứng", "1–1,5 m", "Cây lâu năm",
      "Ưa nắng, chịu bóng nhẹ", "Trung bình — ẩm đều", "Đất tơi xốp, giàu mùn, thoát nước",
      "Khắp cả nước, nhiều ở nông thôn miền Bắc", "Trồng xuân, thu củ sau 10–12 tháng",
      "Dễ tính, chịu bóng; củ già càng cay thơm",
      "Trồng bằng củ giống (hom)", "10–12 tháng sau trồng", "15–25 tấn củ/ha",
      ls(("Trồng hom củ", "Tháng 0"), ("Đẻ nhánh & ra lá", "Tháng 1–4"),
         ("Phình củ", "Tháng 4–10"), ("Thu hoạch", "Tháng 10–12")),
      "Bệnh thối củ, cháy lá",
      "Gia vị đặc trưng (kho cá, giả cầy, mắm tép); dược liệu ấm bụng",
      "Chứa tinh dầu, galangin", "Cay nồng, thơm, hắc nhẹ",
      "Riềng ấm tỳ vị, trị đầy bụng, đau dạ dày, kích thích tiêu hóa (Đông y)",
      "Riềng tươi & bột riềng tiêu thụ nội địa",
      "Riềng cay và xơ hơn gừng nhiều — thường giã hoặc thái lát mỏng khi nấu",
      ["#C8794A", "#9C6B30"], "https://vi.wikipedia.org/wiki/Ri%E1%BB%81ng"),

    P("tia-to", "Tía tô", "Perilla frutescens", "Perilla · tử tô", "Bạc hà (Lamiaceae)",
      "nong-nghiep", "gia-vi", "Hoa môi (Lamiales)", "Perilla", "P. frutescens",
      "Có nguồn gốc Đông Á; rau gia vị & dược liệu trồng khắp vườn nhà Việt Nam.",
      "Tía tô là rau gia vị lá tím-xanh thơm; ăn kèm, nấu cháo giải cảm, đồng thời là vị thuốc.",
      "Cây thân thảo, thân vuông có lông", "0,5–1 m", "Cây hàng năm",
      "Ưa nắng, chịu bóng nhẹ", "Nhiều — cần ẩm đều", "Đất thịt nhẹ, giàu mùn, thoát nước",
      "Khắp cả nước, vườn nhà", "Trồng quanh năm, thu lá nhiều đợt",
      "Dễ trồng, ưa ẩm; ngắt ngọn cho ra nhiều lá",
      "Gieo hạt", "Thu lá sau 40–60 ngày", "15–25 tấn lá/ha/vụ",
      ls(("Gieo hạt", "Ngày 0–10"), ("Cây con", "Ngày 10–30"),
         ("Vươn lá", "Ngày 30–50"), ("Thu hái nhiều đợt", "Ngày 50+")),
      "Sâu ăn lá, rệp, bệnh đốm lá",
      "Rau gia vị ăn kèm; cháo tía tô giải cảm; tinh dầu & dược liệu",
      "Giàu tinh dầu, vitamin A, C, chất chống oxy hóa", "Thơm nồng đặc trưng, hơi the",
      "Tía tô giải cảm, hạ sốt, trị dị ứng, an thai (Đông y)",
      "Lá & hạt tía tô tiêu thụ nội địa; tinh dầu perilla có xuất khẩu",
      "Lá tía tô hai màu — mặt trên xanh, mặt dưới tím — do sắc tố anthocyanin",
      ["#7D5BA6", "#6A994E"], "https://vi.wikipedia.org/wiki/T%C3%ADa_t%C3%B4"),

    P("hung-que", "Húng quế", "Ocimum basilicum", "Basil · rau quế · é quế", "Bạc hà (Lamiaceae)",
      "nong-nghiep", "gia-vi", "Hoa môi (Lamiales)", "Ocimum", "O. basilicum",
      "Có nguồn gốc nhiệt đới châu Á–châu Phi; rau gia vị thơm trồng khắp Việt Nam.",
      "Húng quế là rau gia vị lá thơm nồng; ăn kèm phở, bún, gỏi cuốn; cũng cho tinh dầu.",
      "Cây thân thảo, thân vuông, phân nhánh", "30–60 cm", "Cây hàng năm",
      "Ưa nắng hoàn toàn", "Trung bình — cần ẩm đều", "Đất thịt nhẹ, giàu mùn, thoát nước",
      "Khắp cả nước, vườn nhà & chuyên canh rau thơm", "Trồng quanh năm, thu lá nhiều đợt",
      "Ưa nóng ẩm; ngắt ngọn & hái thường xuyên cho ra nhánh",
      "Gieo hạt, giâm cành", "Thu lá sau 40–55 ngày", "15–25 tấn lá/ha/vụ",
      ls(("Gieo hạt", "Ngày 0–10"), ("Cây con", "Ngày 10–28"),
         ("Vươn nhánh", "Ngày 28–45"), ("Thu hái nhiều đợt", "Ngày 45+")),
      "Sâu ăn lá, rệp, bệnh sương mai",
      "Rau gia vị ăn sống ăn kèm; tinh dầu húng quế hương liệu",
      "Giàu tinh dầu (eugenol), vitamin K, A", "Thơm nồng, cay ấm đặc trưng",
      "Húng quế kích thích tiêu hóa, giải cảm; hạt é làm thức uống mát",
      "Rau thơm tiêu thụ rộng; hạt é (é quế) làm đồ uống giải nhiệt",
      "Hạt húng quế (hạt é) khi ngâm nước nở thành lớp gel — làm thức uống giải nhiệt mùa hè",
      ["#4F7A34", "#A7C957"], "https://vi.wikipedia.org/wiki/H%C3%BAng_qu%E1%BA%BF"),

    # ===== LÂM NGHIỆP — GỖ QUÝ (7 mới) =====
    P("lim-xanh", "Lim xanh", "Erythrophleum fordii", "Lim · iron wood", "Đậu (Fabaceae)",
      "lam-nghiep", "go-quy", "Đậu (Fabales)", "Erythrophleum", "E. fordii",
      "Loài gỗ quý 'tứ thiết' bản địa; phân bố rừng Đông Bắc & Bắc Trung Bộ Việt Nam.",
      "Lim xanh là một trong 'tứ thiết' (đinh–lim–sến–táu) — gỗ cực cứng, bền, từng dùng dựng đình chùa, cầu cống.",
      "Cây gỗ lớn, thân thẳng tròn", "20–30 m", "Cây lâu năm, khai thác sau 50–80 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm đều", "Đất feralit sâu, thoát nước",
      "Đông Bắc, Bắc Trung Bộ (Quảng Ninh, Nghệ An, Hà Tĩnh)", "Trồng đầu mùa mưa, sinh trưởng chậm",
      "Ưa khí hậu nhiệt đới ẩm; sinh trưởng chậm, gỗ rất cứng nặng",
      "Gieo hạt (xử lý), trồng cây con", "50–80 năm (gỗ quý)", "~2 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng chậm", "Năm 3–15"),
         ("Tích lũy gỗ tâm", "Năm 15–40"), ("Khai thác", "Năm 50–80")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ 'tứ thiết' cực bền — đình chùa, cột, cầu, đồ gỗ cao cấp, tà vẹt",
      "—", "—", "—",
      "Gỗ lim quý hiếm, giá cao; thuộc nhóm gỗ được bảo vệ",
      "Gỗ lim cứng tới mức 'lim đanh như sắt' — nhiều đình chùa cổ Việt Nam dựng bằng cột lim còn nguyên vẹn sau hàng trăm năm",
      ["#3A2E22", "#6B4A2E"], "https://vi.wikipedia.org/wiki/Lim_xanh"),

    P("dinh", "Đinh", "Markhamia stipulata", "Dinh · iron wood", "Quao (Bignoniaceae)",
      "lam-nghiep", "go-quy", "Hoa môi (Lamiales)", "Markhamia", "M. stipulata",
      "Loài gỗ quý 'tứ thiết' bản địa; phân bố rừng tự nhiên miền Bắc & Bắc Trung Bộ.",
      "Đinh là một trong 'tứ thiết' (đinh–lim–sến–táu) — gỗ cứng bền đẹp, thớ mịn, dùng đồ gỗ và xây dựng cao cấp.",
      "Cây gỗ lớn, thân thẳng", "15–25 m", "Cây lâu năm, khai thác sau 50–70 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất thịt sâu, ẩm, thoát nước",
      "Miền núi phía Bắc, Bắc Trung Bộ", "Trồng đầu mùa mưa, ra hoa lớn",
      "Ưa khí hậu nhiệt đới ẩm; sinh trưởng chậm",
      "Gieo hạt, trồng cây con", "50–70 năm (gỗ quý)", "~2 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng chậm", "Năm 3–15"),
         ("Tích lũy gỗ tâm", "Năm 15–40"), ("Khai thác", "Năm 50–70")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ 'tứ thiết' cứng bền thớ mịn — đồ gỗ cao cấp, xây dựng, chạm khắc",
      "—", "—", "Vỏ & quả dùng trong y học dân gian",
      "Gỗ đinh quý hiếm, giá cao; được bảo vệ",
      "Đinh có hoa lớn hình chuông đẹp — ít ai ngờ cây gỗ 'tứ thiết' cứng rắn lại nở hoa rực rỡ như vậy",
      ["#5A4A2E", "#9C6B30"], "https://vi.wikipedia.org/wiki/%C4%90inh_(c%C3%A2y)"),

    P("tau", "Táu", "Vatica odorata", "Tau · makha", "Dầu (Dipterocarpaceae)",
      "lam-nghiep", "go-quy", "Bông (Malvales)", "Vatica", "V. odorata",
      "Loài gỗ quý 'tứ thiết' bản địa; phân bố rừng tự nhiên Bắc Bộ & Bắc Trung Bộ.",
      "Táu là một trong 'tứ thiết' (đinh–lim–sến–táu) — gỗ vàng nâu rất cứng, chịu nước, bền với mối mọt.",
      "Cây gỗ lớn, thân thẳng tròn", "20–30 m", "Cây lâu năm, khai thác sau 50–80 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất feralit, thịt sâu, thoát nước",
      "Bắc Bộ, Bắc Trung Bộ (rừng tự nhiên)", "Trồng đầu mùa mưa, sinh trưởng chậm",
      "Ưa khí hậu nhiệt đới ẩm; gỗ rất cứng nặng",
      "Gieo hạt, trồng cây con", "50–80 năm (gỗ quý)", "~1,5–2 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng chậm", "Năm 3–15"),
         ("Tích lũy gỗ tâm", "Năm 15–40"), ("Khai thác", "Năm 50–80")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ 'tứ thiết' cứng bền chịu nước — cầu cống, cột, tà vẹt, đồ gỗ ngoài trời",
      "—", "—", "—",
      "Gỗ táu quý hiếm, giá cao; được bảo vệ",
      "Táu chịu nước cực tốt — từng được dùng làm cọc móng cầu và công trình ngâm nước lâu năm",
      ["#8B6B3A", "#C9A227"], "https://vi.wikipedia.org/wiki/T%C3%A1u_m%E1%BA%ADt"),

    P("sua", "Sưa (Sưa đỏ)", "Dalbergia tonkinensis", "Sưa đỏ · trắc thối · huỳnh đàn", "Đậu (Fabaceae)",
      "lam-nghiep", "go-quy", "Đậu (Fabales)", "Dalbergia", "D. tonkinensis",
      "Loài gỗ cực quý bản địa miền Bắc; nổi tiếng với những vụ gỗ sưa đỏ giá kỷ lục.",
      "Sưa đỏ là loài gỗ quý hiếm bậc nhất, lõi đỏ thơm; từng có giá kỷ lục, được bảo vệ nghiêm ngặt.",
      "Cây gỗ vừa, thân thẳng", "10–18 m", "Cây lâu năm, khai thác sau 30–50 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn khá", "Đất thịt, thoát nước tốt",
      "Đồng bằng & trung du Bắc Bộ (Hà Nội, Bắc Ninh...)", "Trồng đầu mùa mưa, ra hoa trắng thơm",
      "Dễ trồng nhưng gỗ tích lũy lõi quý rất chậm",
      "Gieo hạt, giâm hom", "30–50 năm (lõi quý)", "~1,5 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–2"), ("Sinh trưởng", "Năm 2–15"),
         ("Tích lũy lõi đỏ", "Năm 15–30"), ("Khai thác", "Năm 30–50")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ lõi đỏ thơm cực quý — đồ thờ, tượng, mỹ nghệ cao cấp; giá trị sưu tầm",
      "—", "—", "—",
      "Gỗ sưa đỏ từng có giá hàng chục tỷ đồng/cây; thuộc nhóm IA cấm khai thác, được bảo vệ nghiêm ngặt",
      "Có thời điểm 1 cây sưa đỏ cổ thụ được trả giá tới hàng chục tỷ đồng — đắt bậc nhất trong các loài cây ở Việt Nam",
      ["#8B2E22", "#C8521E"], "https://vi.wikipedia.org/wiki/S%C6%B0a"),

    P("cam-lai", "Cẩm lai", "Dalbergia oliveri", "Cẩm lai · rosewood", "Đậu (Fabaceae)",
      "lam-nghiep", "go-quy", "Đậu (Fabales)", "Dalbergia", "D. oliveri",
      "Loài gỗ quý bản địa; phân bố rừng Tây Nguyên & Đông Nam Bộ.",
      "Cẩm lai là gỗ quý nhóm I, lõi nâu hồng vân đẹp, cứng nặng; đồ nội thất & mỹ nghệ cao cấp.",
      "Cây gỗ lớn, thân thẳng tròn", "20–25 m", "Cây lâu năm, khai thác sau 50–70 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất đỏ bazan, thịt sâu, thoát nước",
      "Tây Nguyên (Đắk Lắk, Gia Lai, Kon Tum), Đông Nam Bộ", "Trồng đầu mùa mưa, sinh trưởng chậm",
      "Ưa khí hậu nhiệt đới ẩm có mùa khô; gỗ tích lũy chậm",
      "Gieo hạt, giâm hom", "50–70 năm (gỗ quý)", "~2 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng chậm", "Năm 3–15"),
         ("Tích lũy lõi", "Năm 15–40"), ("Khai thác", "Năm 50–70")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ quý nhóm I, vân đẹp — bàn ghế, sập gụ, tượng, mỹ nghệ cao cấp",
      "—", "—", "—",
      "Gỗ cẩm lai giá rất cao; thuộc nhóm gỗ quý hiếm được bảo vệ",
      "Cẩm lai cùng chi Dalbergia với trắc và sưa — chi này quy tụ những loài gỗ quý đắt giá nhất Việt Nam",
      ["#7A3A2E", "#C9925A"], "https://vi.wikipedia.org/wiki/C%E1%BA%A9m_lai"),

    P("go-do", "Gõ đỏ (Cà te)", "Afzelia xylocarpa", "Cà te · gõ đỏ · doussie", "Đậu (Fabaceae)",
      "lam-nghiep", "go-quy", "Đậu (Fabales)", "Afzelia", "A. xylocarpa",
      "Loài gỗ quý bản địa; phân bố rừng Tây Nguyên & Đông Nam Bộ.",
      "Gõ đỏ là gỗ quý nhóm I, lõi đỏ nâu cứng bền, vân đẹp; gỗ làm sập, bàn ghế, tượng cao cấp.",
      "Cây gỗ lớn, thân thẳng tròn", "20–30 m", "Cây lâu năm, khai thác sau 50–80 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — chịu hạn khá", "Đất đỏ bazan, thịt sâu, thoát nước",
      "Tây Nguyên, Đông Nam Bộ", "Trồng đầu mùa mưa, sinh trưởng chậm",
      "Ưa khí hậu nhiệt đới có mùa khô; gỗ rất bền, ít cong vênh",
      "Gieo hạt (hạt to), trồng cây con", "50–80 năm (gỗ quý)", "~2 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng chậm", "Năm 3–15"),
         ("Tích lũy lõi", "Năm 15–40"), ("Khai thác", "Năm 50–80")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ quý nhóm I, đỏ nâu bền đẹp — sập gụ, bàn ghế, tượng, đồ thờ cao cấp",
      "—", "—", "Hạt và vỏ dùng trong y học dân gian",
      "Gỗ gõ đỏ giá cao, ít cong vênh nứt nẻ; thuộc nhóm gỗ quý được bảo vệ",
      "Hạt gõ đỏ có 'mũ' màu cam đỏ bắt mắt — từng được dùng làm hạt trang sức và đồ chơi dân gian",
      ["#8B3A2A", "#C8794A"], "https://vi.wikipedia.org/wiki/G%C3%B5_%C4%91%E1%BB%8F"),

    P("vu-huong", "Vù hương", "Cinnamomum balansae", "Re hương · gù hương · xá xị", "Long não (Lauraceae)",
      "lam-nghiep", "go-quy", "Long não (Laurales)", "Cinnamomum", "C. balansae",
      "Loài gỗ quý thơm bản địa; phân bố rừng miền Bắc & Bắc Trung Bộ, có tên trong Sách Đỏ.",
      "Vù hương là cây gỗ lớn thơm mùi xá xị; gỗ và rễ chứa tinh dầu safrole, vừa cho gỗ vừa cho tinh dầu.",
      "Cây gỗ lớn thường xanh", "20–30 m", "Cây lâu năm, khai thác sau 40–60 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất thịt sâu, ẩm, thoát nước",
      "Miền núi phía Bắc, Bắc Trung Bộ", "Trồng đầu mùa mưa, sinh trưởng trung bình",
      "Ưa khí hậu nhiệt đới ẩm; cả cây thơm mùi xá xị",
      "Gieo hạt, giâm hom", "40–60 năm (gỗ); tinh dầu sớm hơn", "~2–3 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng", "Năm 3–15"),
         ("Tích lũy gỗ & tinh dầu", "Năm 15–40"), ("Khai thác", "Năm 40–60")),
      "Sâu đục thân, nấm gỗ",
      "Gỗ thơm bền chống mối — đồ gỗ, tủ; tinh dầu (safrole) hương liệu, công nghiệp",
      "—", "—", "Rễ & gỗ nấu nước xá xị; tinh dầu sát khuẩn",
      "Gỗ & tinh dầu vù hương giá trị; loài quý được bảo vệ (Sách Đỏ)",
      "Cả thân, rễ và lá vù hương đều thơm mùi xá xị — nguồn safrole tự nhiên dùng trong hương liệu",
      ["#6B4A2E", "#A98D5B"], "https://vi.wikipedia.org/wiki/V%C3%B9_h%C6%B0%C6%A1ng"),

    # ===== LÂM NGHIỆP — TRỒNG RỪNG (7 mới) =====
    P("mo", "Mỡ", "Manglietia conifera", "Mo · manglietia", "Mộc lan (Magnoliaceae)",
      "lam-nghiep", "trong-rung", "Mộc lan (Magnoliales)", "Manglietia", "M. conifera",
      "Loài cây trồng rừng bản địa mọc nhanh; phổ biến ở miền núi phía Bắc & Bắc Trung Bộ.",
      "Mỡ là cây gỗ bản địa mọc nhanh, thân thẳng đẹp; gỗ trắng mềm làm bút chì, ván, bao bì, nguyên liệu giấy.",
      "Cây gỗ thường xanh, thân thẳng tròn", "20–30 m", "Cây lâu năm, khai thác sau 12–20 năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Nhiều — ưa ẩm", "Đất feralit sâu, ẩm, thoát nước",
      "Yên Bái, Phú Thọ, Hà Giang, Nghệ An", "Trồng đầu mùa mưa",
      "Ưa khí hậu mát ẩm vùng đồi núi; thân thẳng ít cành",
      "Gieo hạt, trồng cây con", "12–20 năm (gỗ)", "10–15 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–2"), ("Sinh trưởng nhanh", "Năm 2–8"),
         ("Phát triển đường kính", "Năm 8–15"), ("Khai thác", "Năm 12–20")),
      "Sâu ăn lá, sâu đục ngọn, nấm bệnh",
      "Gỗ trắng mềm thớ mịn — bút chì, ván ghép, bao bì, nguyên liệu giấy, đồ mộc",
      "—", "—", "—",
      "Gỗ mỡ là nguyên liệu truyền thống làm ruột bút chì và ván ghép thanh",
      "Gỗ mỡ thớ mịn, mềm đều — lý do nó được chọn làm thân bút chì gỗ ở Việt Nam",
      ["#9CA877", "#C9B97A"], "https://vi.wikipedia.org/wiki/M%E1%BB%A1_(c%C3%A2y)"),

    P("bo-de", "Bồ đề (trồng rừng)", "Styrax tonkinensis", "Bồ đề trắng · cánh kiến trắng", "Bồ đề (Styracaceae)",
      "lam-nghiep", "trong-rung", "Thạch nam (Ericales)", "Styrax", "S. tonkinensis",
      "Loài cây trồng rừng bản địa mọc nhanh; phổ biến ở miền núi phía Bắc, cho nhựa benzoin.",
      "Bồ đề là cây gỗ mọc nhanh, gỗ trắng nhẹ làm giấy & diêm; vỏ cho nhựa cánh kiến trắng (benzoin) thơm quý.",
      "Cây gỗ rụng lá, thân thẳng", "15–20 m", "Cây lâu năm, khai thác sau 8–12 năm",
      "Ưa nắng hoàn toàn", "Trung bình — cần ẩm", "Đất feralit, ẩm, thoát nước",
      "Yên Bái, Phú Thọ, Hà Giang, Lào Cai", "Trồng đầu mùa mưa",
      "Mọc nhanh, ưa sáng; tái sinh hạt tự nhiên tốt",
      "Gieo hạt, tái sinh tự nhiên", "8–12 năm (gỗ); nhựa khi trưởng thành", "10–15 m³ gỗ/ha/năm",
      ls(("Gieo / tái sinh", "Năm 1–2"), ("Sinh trưởng nhanh", "Năm 2–6"),
         ("Lấy nhựa & phát triển gỗ", "Năm 6–10"), ("Khai thác", "Năm 8–12")),
      "Sâu ăn lá, sâu đục thân",
      "Gỗ trắng nhẹ — bột giấy, diêm, que kem; nhựa benzoin (cánh kiến trắng) làm hương liệu, dược phẩm",
      "—", "—", "Nhựa benzoin sát khuẩn, làm hương trầm, định hương nước hoa",
      "Gỗ bồ đề & nhựa benzoin có giá trị; benzoin Việt Nam (Lào Cai, Yên Bái) xuất khẩu",
      "Nhựa bồ đề (benzoin) là một trong những hương liệu định hương cổ xưa nhất, dùng trong nước hoa và hương trầm",
      ["#C9B97A", "#E9EDC9"], "https://vi.wikipedia.org/wiki/B%E1%BB%93_%C4%91%E1%BB%81_(chi_B%E1%BB%93_%C4%91%E1%BB%81)"),

    P("phi-lao", "Phi lao", "Casuarina equisetifolia", "Dương · phi lao · whistling pine", "Phi lao (Casuarinaceae)",
      "lam-nghiep", "trong-rung", "Dẻ (Fagales)", "Casuarina", "C. equisetifolia",
      "Loài cây chắn gió ven biển; trồng dày khắp dải cát ven biển miền Trung & Nam Bộ.",
      "Phi lao là cây mọc nhanh chịu mặn, lá kim nhỏ; trồng chắn gió, chắn cát, cố định đụn cát ven biển.",
      "Cây gỗ thường xanh, cành rủ như lá kim", "15–25 m", "Cây lâu năm, khai thác sau 8–15 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn & mặn tốt", "Đất cát ven biển, chịu mặn",
      "Dải cát ven biển miền Trung, Nam Bộ", "Trồng đầu mùa mưa",
      "Chịu gió bão, cát bay, đất mặn nghèo; cố định đạm cải tạo đất cát",
      "Gieo hạt, trồng cây con", "8–15 năm (gỗ, củi)", "8–12 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–2"), ("Sinh trưởng nhanh", "Năm 2–6"),
         ("Khép tán chắn gió", "Năm 4–10"), ("Khai thác / tỉa", "Năm 8–15")),
      "Sâu ăn lá, sâu đục thân, nấm rễ",
      "Cây phòng hộ chắn gió chắn cát ven biển; gỗ làm củi, cọc, bột giấy; cố định đụn cát",
      "—", "—", "—",
      "Giá trị phòng hộ là chính; gỗ phi lao làm củi đun & cọc xây dựng",
      "Cái 'lá kim' của phi lao thực ra là cành nhỏ — lá thật tiêu giảm thành vảy li ti để chống mất nước nơi gió cát",
      ["#5A6B4A", "#9C8B5A"], "https://vi.wikipedia.org/wiki/Phi_lao"),

    P("luong", "Luồng", "Dendrocalamus barbatus", "Luồng · tre luồng · bamboo", "Hòa thảo (Poaceae)",
      "lam-nghiep", "trong-rung", "Hòa thảo (Poales)", "Dendrocalamus", "D. barbatus",
      "Loài tre lớn trồng rừng chủ lực; nổi tiếng ở Thanh Hóa, Hòa Bình, Phú Thọ.",
      "Luồng là loài tre thân lớn mọc cụm, sinh trưởng cực nhanh; nguyên liệu xây dựng, giấy, đũa, măng ăn.",
      "Tre thân lớn mọc cụm, thân rỗng có đốt", "15–20 m", "Cây lâu năm; khai thác cây ≥3 tuổi",
      "Ưa nắng hoàn toàn", "Nhiều — ưa ẩm", "Đất feralit ẩm, ven đồi, thoát nước",
      "Thanh Hóa (Quan Hóa, Lang Chánh), Hòa Bình, Phú Thọ", "Măng mọc mùa mưa; khai thác cây quanh năm",
      "Mọc cực nhanh; một bụi cho cây thu hoạch hằng năm, tái sinh liên tục",
      "Trồng bằng gốc / hom thân, chiết cành", "Cây ≥3 tuổi mới khai thác", "10–20 tấn/ha/năm",
      ls(("Trồng gốc/hom", "Năm 0–1"), ("Phát triển bụi", "Năm 1–3"),
         ("Khai thác cây ≥3 tuổi", "Năm 3+"), ("Tái sinh măng hằng năm", "Mùa mưa")),
      "Sâu vòi voi măng, bệnh chổi sể, mọt thân",
      "Nguyên liệu xây dựng, giàn giáo, đũa, tăm, ván ép tre, bột giấy; măng luồng ăn được",
      "Măng giàu chất xơ, ít calo", "Măng giòn, ngọt nhẹ (khi luộc kỹ)",
      "Măng luồng là thực phẩm; cây luồng gắn sinh kế vùng cao",
      "Tre luồng & măng tiêu thụ rộng; ván ép tre, đũa luồng xuất khẩu",
      "Luồng mọc nhanh bậc nhất giới thực vật — măng có thể vươn cao cả mét chỉ trong một ngày",
      ["#6A994E", "#C9B97A"], "https://vi.wikipedia.org/wiki/Lu%E1%BB%93ng"),

    P("xa-cu", "Xà cừ", "Khaya senegalensis", "Sọ khỉ · African mahogany", "Xoan (Meliaceae)",
      "lam-nghiep", "trong-rung", "Bồ hòn (Sapindales)", "Khaya", "K. senegalensis",
      "Loài gỗ nhập từ châu Phi; trồng rộng làm cây xanh đô thị & lấy gỗ khắp Việt Nam.",
      "Xà cừ là cây gỗ lớn tán rộng, rễ bạnh; vừa là cây bóng mát đường phố quen thuộc vừa cho gỗ đỏ làm đồ mộc.",
      "Cây gỗ lớn, tán rộng, gốc bạnh", "20–30 m", "Cây lâu năm, khai thác sau 25–40 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn tốt", "Thích nghi nhiều loại đất, thoát nước",
      "Khắp cả nước, phổ biến cây đường phố đô thị", "Trồng đầu mùa mưa",
      "Dễ trồng, chịu khói bụi & hạn; rễ bạnh khỏe nhưng dễ nổi gây hỏng vỉa hè",
      "Gieo hạt, trồng cây con", "25–40 năm (gỗ)", "5–8 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–2"), ("Sinh trưởng nhanh", "Năm 2–10"),
         ("Khép tán / phát triển gỗ", "Năm 10–25"), ("Khai thác", "Năm 25–40")),
      "Sâu đục thân, sâu ăn lá, nấm bệnh",
      "Cây bóng mát đường phố; gỗ đỏ nâu (mahogany) làm đồ mộc, ván, nội thất",
      "—", "—", "Vỏ cây dùng làm thuốc dân gian (sốt rét) ở châu Phi",
      "Gỗ xà cừ tiêu thụ nội địa; giá trị cảnh quan đô thị lớn",
      "Hàng xà cừ cổ thụ là hình ảnh quen thuộc của nhiều con phố Hà Nội — có cây hơn trăm tuổi",
      ["#7A3A2E", "#5A6B4A"], "https://vi.wikipedia.org/wiki/X%C3%A0_c%E1%BB%AB"),

    P("muong-den", "Muồng đen", "Senna siamea", "Muồng xiêm · cassia", "Đậu (Fabaceae)",
      "lam-nghiep", "trong-rung", "Đậu (Fabales)", "Senna", "S. siamea",
      "Loài cây trồng rừng & bóng mát mọc nhanh; trồng phổ biến làm cây đường phố và rừng phòng hộ.",
      "Muồng đen là cây gỗ mọc nhanh, hoa vàng; trồng làm bóng mát, củi, gỗ và cải tạo đất.",
      "Cây gỗ thường xanh, tán rộng", "10–20 m", "Cây lâu năm, khai thác sau 10–20 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn tốt", "Thích nghi nhiều loại đất, thoát nước",
      "Khắp cả nước, cây đường phố & rừng phòng hộ", "Trồng đầu mùa mưa, hoa vàng mùa hè",
      "Dễ tính, mọc nhanh, chịu hạn; cố định đạm cải tạo đất",
      "Gieo hạt, trồng cây con", "10–20 năm (gỗ, củi)", "8–12 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1"), ("Sinh trưởng nhanh", "Năm 1–6"),
         ("Khép tán / phát triển gỗ", "Năm 6–12"), ("Khai thác / tỉa", "Năm 10–20")),
      "Sâu ăn lá, sâu đục thân",
      "Cây bóng mát đường phố; gỗ lõi đen làm đồ mộc; củi tốt; cải tạo đất",
      "—", "—", "Lá non & hoa ăn được (sau chế biến) ở một số vùng",
      "Gỗ & củi muồng đen tiêu thụ nội địa; giá trị cảnh quan & phòng hộ",
      "Muồng đen nở vàng rực cả tán vào mùa hè — là cây bóng mát đường phố quen thuộc khắp Việt Nam",
      ["#2E2A22", "#E3C16F"], "https://vi.wikipedia.org/wiki/Mu%E1%BB%93ng_%C4%91en"),

    P("thong-ba-la", "Thông ba lá", "Pinus kesiya", "Khasi pine · thông ba lá", "Thông (Pinaceae)",
      "lam-nghiep", "trong-rung", "Thông (Pinales)", "Pinus", "P. kesiya",
      "Loài thông lá kim phổ biến Tây Nguyên; rừng thông Đà Lạt, Lâm Đồng chủ yếu là thông ba lá.",
      "Thông ba lá là loài thông lá kim (3 lá/bó) trồng rừng chủ lực Tây Nguyên; cho gỗ, nhựa và cảnh quan.",
      "Cây gỗ lá kim thường xanh, thân thẳng", "20–35 m", "Cây lâu năm, khai thác sau 25–40 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn tốt", "Đất feralit, đất đỏ, thoát nước, pH 5–6",
      "Lâm Đồng (Đà Lạt), Kon Tum, Gia Lai, Lào Cai", "Thường xanh; trích nhựa mùa khô",
      "Ưa khí hậu mát cao nguyên 800–1800 m; chịu đất nghèo",
      "Gieo hạt (từ nón), trồng cây con", "25–40 năm (gỗ); nhựa từ năm 15", "8–12 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng", "Năm 3–12"),
         ("Trích nhựa", "Năm 15+"), ("Khai thác gỗ", "Năm 25–40")),
      "Sâu róm thông, nấm thối cổ rễ, bệnh vàng lá",
      "Gỗ xây dựng & đồ mộc; nhựa thông (rosin, turpentine); rừng cảnh quan du lịch",
      "—", "—", "Nhựa thông làm thuốc dán, tinh dầu thông xông",
      "Gỗ & nhựa thông ba lá tiêu thụ rộng; rừng thông Đà Lạt gắn du lịch",
      "Thông ba lá có lá kim mọc thành bó 3 chiếc — đặc điểm phân biệt với thông nhựa (2 lá/bó)",
      ["#2D5016", "#9C8B5A"], "https://vi.wikipedia.org/wiki/Th%C3%B4ng_ba_l%C3%A1"),
]


def main():
    with open(path, 'r', encoding='utf-8') as f:
        d = json.load(f)

    # 1) Migrate cây hiện có: thêm linhVuc + tách nhóm con lâm nghiệp + chuyển tỏi/ớt
    moved, sub, lv = 0, 0, 0
    for c in d['cay']:
        cid = c['id']
        if cid in ('toi', 'ot') and c.get('nhom') != 'gia-vi':
            c['nhom'] = 'gia-vi'; moved += 1
        if c.get('nhom') == 'lam-nghiep' or cid in LAM_SUB:
            if cid in LAM_SUB:
                c['nhom'] = LAM_SUB[cid]; sub += 1
        # linhVuc
        new_lv = 'lam-nghiep' if c['nhom'] in ('go-quy', 'trong-rung', 'lam-san') else 'nong-nghiep'
        if c.get('linhVuc') != new_lv:
            c['linhVuc'] = new_lv; lv += 1

    # 2) Thêm cây mới
    existing = {c['id'] for c in d['cay']}
    added = 0
    for p in NEW:
        if p['id'] in existing:
            print('SKIP', p['id']); continue
        d['cay'].append(p); existing.add(p['id']); added += 1

    d['_meta']['capNhat'] = '2026-05-26'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    # thống kê
    lvg, nhg = {}, {}
    for c in d['cay']:
        lvg[c['linhVuc']] = lvg.get(c['linhVuc'], 0) + 1
        nhg[c['nhom']] = nhg.get(c['nhom'], 0) + 1
    print(f'Migrate: linhVuc {lv}, nhóm con {sub}, chuyển gia vị {moved}. Thêm {added} cây. Tổng {len(d["cay"])}.')
    print('Lĩnh vực:', lvg)
    print('Nhóm:', nhg)


if __name__ == '__main__':
    main()
