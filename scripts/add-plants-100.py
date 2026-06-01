#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thêm 10 cây phổ biến còn thiếu → tổng 100 loài.
+6 nông (dưa hấu, dưa gang, dâu tây, dâu tằm, bí xanh, củ dền)
+4 lâm (dó bầu/trầm hương, kơ nia, bằng lăng, long não)
Chạy: python3 scripts/add-plants-100.py"""
import json, os
path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tu-dien-nong-lam-ngu.json')


def ls(*p): return [{"giaiDoan": g, "thoiGian": t} for g, t in p]


def P(id, ten, sci, khac, ho, lv, nhom, bo, chi, loai, xuatXu, moTa, loaiThan, chieuCao, chuKy,
      anhSang, nuoc, loaiDat, vungTrong, muaVu, dieuKien, nhanGiong, thuHoach, nangSuat, lich,
      sauBenh, giaTri, dinhDuong, huongVi, yhct, thiTruong, thuVi, mau, nguon):
    return {"id": id, "ten": ten, "tenKhoaHoc": sci, "tenKhac": khac, "ho": ho, "linhVuc": lv,
            "nhom": nhom, "anh": f"img/{id}.jpg", "anhChiTiet": f"img/detail/{id}.jpg", "xuatXu": xuatXu,
            "phanLoai": {"bo": bo, "ho": ho, "chi": chi, "loai": loai}, "moTa": moTa, "loaiThan": loaiThan,
            "chieuCao": chieuCao, "chuKy": chuKy, "anhSang": anhSang, "nuoc": nuoc, "loaiDat": loaiDat,
            "vungTrong": vungTrong, "muaVu": muaVu, "dieuKien": dieuKien, "nhanGiong": nhanGiong,
            "thoiGianThuHoach": thuHoach, "nangSuat": nangSuat, "lichSinhTruong": lich, "sauBenh": sauBenh,
            "giaTri": giaTri, "dinhDuong": dinhDuong, "huongVi": huongVi, "yHocCoTruyen": yhct,
            "thiTruong": thiTruong, "suThatThuVi": thuVi, "mauDacTrung": mau, "nguon": nguon}


NEW = [
    P("dua-hau", "Dưa hấu", "Citrullus lanatus", "Watermelon · dưa đỏ", "Bầu bí (Cucurbitaceae)",
      "nong-nghiep", "an-qua", "Bầu bí (Cucurbitales)", "Citrullus", "C. lanatus",
      "Có nguồn gốc châu Phi; trồng rộng khắp Việt Nam, đặc biệt vụ Tết ở miền Trung & Nam Bộ.",
      "Dưa hấu là cây bò cho quả lớn vỏ xanh ruột đỏ mọng nước ngọt mát; trái cây giải nhiệt mùa hè & dịp Tết.",
      "Cây thân bò, có tua cuốn", "Bò 2–4 m", "Cây hàng năm (60–90 ngày)",
      "Ưa nắng hoàn toàn", "Trung bình — cần đủ ẩm, sợ úng", "Đất cát pha, tơi xốp, thoát nước tốt",
      "Miền Trung, ĐBSCL, Đông Nam Bộ", "Trồng nhiều vụ, rộ vụ Tết & hè",
      "Ưa nóng, nắng nhiều; đất tơi thoát nước, tránh úng thối gốc",
      "Gieo hạt", "60–90 ngày sau gieo", "25–40 tấn/ha",
      ls(("Gieo hạt", "Ngày 0–7"), ("Bò lan & ra hoa", "Ngày 7–40"),
         ("Đậu & lớn quả", "Ngày 40–70"), ("Chín & thu hoạch", "Ngày 70–90")),
      "Bọ trĩ, rệp, ruồi đục quả, bệnh sương mai, héo rũ",
      "Trái cây giải nhiệt ăn tươi & ép nước; vỏ làm mứt; hạt rang (Tết)",
      "Nhiều nước (~92%), vitamin C, A, lycopene", "Ngọt, mọng nước, mát",
      "Dưa hấu thanh nhiệt, lợi tiểu, giải khát mùa hè",
      "Tiêu thụ nội địa lớn & xuất khẩu sang Trung Quốc; cao điểm vụ Tết",
      "Dưa hấu khoảng 92% là nước — một trong những trái cây giải khát tốt nhất mùa hè",
      ["#C1121F", "#4F7A34"], "https://vi.wikipedia.org/wiki/D%C6%B0a_h%E1%BA%A5u"),

    P("dua-gang", "Dưa gang", "Cucumis melo", "Vietnamese melon · dưa bở", "Bầu bí (Cucurbitaceae)",
      "nong-nghiep", "an-qua", "Bầu bí (Cucurbitales)", "Cucumis", "C. melo",
      "Loài dưa thuộc nhóm Cucumis melo; trồng phổ biến vườn nhà khắp Việt Nam, ăn mùa hè.",
      "Dưa gang là cây bò cho quả dài vỏ vàng nhạt, thịt giòn xốp; ăn sống chấm đường hoặc dầm, giải nhiệt.",
      "Cây thân bò, có tua cuốn", "Bò 2–3 m", "Cây hàng năm (60–80 ngày)",
      "Ưa nắng hoàn toàn", "Trung bình — cần ẩm đều", "Đất thịt nhẹ, tơi xốp, thoát nước",
      "Khắp cả nước, vườn nhà", "Trồng vụ xuân–hè, thu mùa hè",
      "Ưa nóng ẩm; cần thoát nước tốt tránh thối quả",
      "Gieo hạt", "60–80 ngày sau gieo", "15–25 tấn/ha",
      ls(("Gieo hạt", "Ngày 0–7"), ("Bò lan & ra hoa", "Ngày 7–40"),
         ("Đậu & lớn quả", "Ngày 40–60"), ("Chín & thu hoạch", "Ngày 60–80")),
      "Bọ dưa, rệp, ruồi đục quả, bệnh sương mai",
      "Trái cây giải nhiệt ăn tươi (dầm đường), nấu canh khi xanh",
      "Nhiều nước, vitamin C, chất xơ, ít calo", "Thanh mát, giòn xốp, ngọt dịu",
      "Dưa gang tính mát, giải nhiệt, lợi tiểu mùa hè",
      "Tiêu thụ nội địa & vườn nhà; rau quả mùa hè dân dã",
      "Dưa gang cùng loài Cucumis melo với dưa lê, dưa lưới — chỉ khác giống và cách dùng",
      ["#E3C16F", "#9CB04A"], "https://vi.wikipedia.org/wiki/D%C6%B0a_gang"),

    P("dau-tay", "Dâu tây", "Fragaria × ananassa", "Strawberry · dâu tây Đà Lạt", "Hoa hồng (Rosaceae)",
      "nong-nghiep", "an-qua", "Hoa hồng (Rosales)", "Fragaria", "F. × ananassa",
      "Cây ôn đới lai tạo; ở Việt Nam trồng tập trung ở Đà Lạt, Mộc Châu, Sơn La — vùng khí hậu mát.",
      "Dâu tây là cây thân thảo thấp cho quả đỏ mọng ngọt chua thơm; đặc sản & nông nghiệp du lịch vùng cao.",
      "Cây thân thảo thấp, bò lan bằng thân ngó", "15–25 cm", "Cây lâu năm ngắn (trồng lại theo vụ)",
      "Ưa nắng, ưa mát", "Nhiều — cần ẩm đều, không úng", "Đất tơi xốp, giàu mùn, thoát nước, pH 5,5–6,5",
      "Đà Lạt (Lâm Đồng), Mộc Châu (Sơn La)", "Trồng vụ thu–đông, thu quả nhiều đợt mùa mát",
      "Cần khí hậu mát 15–22°C; trồng nhà màng/thủy canh phổ biến để sạch bệnh",
      "Trồng cây con từ ngó (thân bò) hoặc cấy mô", "Thu quả sau 2–3 tháng, hái nhiều đợt", "10–25 tấn/ha/vụ",
      ls(("Trồng cây con", "Tháng 0"), ("Phát triển & ra hoa", "Tháng 1–2"),
         ("Đậu quả", "Tháng 2–3"), ("Thu hái nhiều đợt", "Tháng 3+")),
      "Nhện đỏ, bọ trĩ, bệnh thán thư, mốc xám quả",
      "Trái cây đặc sản ăn tươi, mứt, sinh tố; nông nghiệp du lịch (hái dâu)",
      "Giàu vitamin C, mangan, chất chống oxy hóa (anthocyanin)", "Ngọt chua, thơm đặc trưng, mọng",
      "Dâu tây giàu chất chống oxy hóa, tốt cho da & tim mạch",
      "Đặc sản Đà Lạt giá cao; vườn dâu gắn du lịch trải nghiệm",
      "Quả dâu tây không phải 'quả' thật — phần đỏ mọng là đế hoa phình, các hạt li ti mới là quả thật",
      ["#C1121F", "#6A994E"], "https://vi.wikipedia.org/wiki/D%C3%A2u_t%C3%A2y"),

    P("dau-tam", "Dâu tằm", "Morus alba", "Mulberry · cây dâu (nuôi tằm)", "Dâu tằm (Moraceae)",
      "nong-nghiep", "an-qua", "Hoa hồng (Rosales)", "Morus", "M. alba",
      "Có nguồn gốc Đông Á; trồng lâu đời ở Việt Nam (bãi sông Hồng, Lâm Đồng) vừa lấy lá nuôi tằm vừa ăn quả.",
      "Dâu tằm là cây gỗ nhỏ: lá nuôi tằm dệt tơ lụa, quả chín tím đen ăn tươi & làm siro, rượu, mứt.",
      "Cây gỗ nhỏ / bụi rụng lá", "3–10 m (đốn thấp khi nuôi tằm)", "Cây lâu năm",
      "Ưa nắng hoàn toàn", "Trung bình — cần ẩm đều", "Đất phù sa, thịt nhẹ, thoát nước",
      "Bãi sông Hồng, Thái Bình, Lâm Đồng (Bảo Lộc)", "Hái lá quanh năm; quả chín tháng 3–5",
      "Dễ trồng, mọc nhanh; đốn tỉa để ra nhiều lá nuôi tằm",
      "Giâm cành, gieo hạt", "Hái lá sau vài tháng; quả sau 1–2 năm", "Lá 15–25 tấn/ha/năm",
      ls(("Trồng / giâm cành", "Năm 0"), ("Ra cành lá", "Tháng 2–4"),
         ("Hái lá nuôi tằm", "Quanh năm"), ("Quả chín", "Tháng 3–5")),
      "Sâu cuốn lá, rầy, bệnh gỉ sắt, đốm lá",
      "Lá nuôi tằm dệt tơ lụa; quả ăn tươi, siro, rượu, mứt; vị thuốc",
      "Quả giàu vitamin C, sắt, anthocyanin", "Quả chín ngọt chua, mọng tím đen",
      "Lá (tang diệp), quả (tang thầm), vỏ rễ (tang bạch bì) đều là vị thuốc Đông y",
      "Tơ tằm là nghề truyền thống (Bảo Lộc, Nam Định); siro & rượu dâu tằm tiêu thụ nội địa",
      "Một con tằm ăn lá dâu nhả ra sợi tơ dài tới ~1.000 m để làm kén — nền của nghề dệt lụa",
      ["#5E2750", "#6A994E"], "https://vi.wikipedia.org/wiki/D%C3%A2u_t%E1%BA%B1m"),

    P("bi-xanh", "Bí xanh", "Benincasa hispida", "Winter melon · bí đao · bí phấn", "Bầu bí (Cucurbitaceae)",
      "nong-nghiep", "rau", "Bầu bí (Cucurbitales)", "Benincasa", "B. hispida",
      "Có nguồn gốc nhiệt đới châu Á; rau quả quen thuộc, trồng khắp Việt Nam, để được lâu.",
      "Bí xanh (bí đao) là cây leo/bò cho quả dài vỏ xanh phủ phấn; nấu canh giải nhiệt, làm mứt, nước bí đao.",
      "Cây leo/bò thân có lông, tua cuốn", "Bò/leo 4–8 m", "Cây hàng năm (90–120 ngày)",
      "Ưa nắng hoàn toàn", "Trung bình — cần ẩm đều", "Đất thịt nhẹ, giàu mùn, thoát nước",
      "Khắp cả nước, nhiều ở đồng bằng", "Trồng vụ xuân–hè & thu, thu sau 80–110 ngày",
      "Ưa nóng ẩm; có thể làm giàn hoặc để bò đất; quả để được nhiều tháng",
      "Gieo hạt", "80–110 ngày sau gieo", "30–50 tấn/ha",
      ls(("Gieo hạt", "Ngày 0–10"), ("Bò/leo & ra hoa", "Ngày 10–55"),
         ("Đậu & lớn quả", "Ngày 55–90"), ("Thu hoạch", "Ngày 90–120")),
      "Bọ dưa, ruồi đục quả, rệp, bệnh sương mai, phấn trắng",
      "Rau quả nấu canh, kho, làm mứt bí, nước bí đao giải nhiệt",
      "Nhiều nước, ít calo, vitamin C, chất xơ", "Thanh mát, ngọt dịu",
      "Bí đao tính mát, lợi tiểu, thanh nhiệt, hỗ trợ giảm cân (Đông y)",
      "Tiêu thụ nội địa lớn; nước bí đao & mứt bí chế biến phổ biến",
      "Quả bí xanh phủ lớp phấn trắng giúp bảo quản tự nhiên — để nơi thoáng được vài tháng không hỏng",
      ["#6E9E73", "#C8DEBA"], "https://vi.wikipedia.org/wiki/B%C3%AD_%C4%91ao"),

    P("cu-den", "Củ dền", "Beta vulgaris", "Beetroot · củ dền đỏ", "Dền (Amaranthaceae)",
      "nong-nghiep", "rau", "Cẩm chướng (Caryophyllales)", "Beta", "B. vulgaris",
      "Cây ôn đới nguồn gốc châu Âu; ở Việt Nam trồng nhiều ở Đà Lạt, cho củ đỏ tím giàu dinh dưỡng.",
      "Củ dền là rau ăn củ màu đỏ tím đậm, ngọt; ép nước, nấu súp, hầm — bổ máu, tạo màu tự nhiên.",
      "Cây thân thảo, rễ củ phình to", "Củ 7–12 cm; lá 25–40 cm", "Cây hàng năm (80–110 ngày)",
      "Ưa nắng, ưa mát", "Trung bình — ẩm đều", "Đất tơi xốp, sâu, giàu mùn, thoát nước",
      "Đà Lạt (Lâm Đồng), vùng rau mát", "Trồng vụ mát, thu sau 80–110 ngày",
      "Ưa mát 15–22°C; đất tơi sâu cho củ tròn đều",
      "Gieo hạt thẳng", "80–110 ngày sau gieo", "20–35 tấn/ha",
      ls(("Gieo hạt", "Ngày 0–12"), ("Cây con & tỉa", "Ngày 12–35"),
         ("Phình củ", "Ngày 35–85"), ("Thu hoạch", "Ngày 85–110")),
      "Sâu xám, bệnh đốm lá, thối củ",
      "Rau củ ép nước, nấu súp, hầm, làm salad; tạo màu thực phẩm tự nhiên",
      "Giàu folate, mangan, kali, nitrat & sắc tố betalain", "Ngọt đậm, vị đất nhẹ, màu đỏ tím",
      "Củ dền bổ máu, hỗ trợ huyết áp & tuần hoàn nhờ nitrat tự nhiên",
      "Tiêu thụ nội địa; nước ép củ dền & bột củ dền làm sản phẩm sức khỏe",
      "Màu đỏ tím của củ dền (betalain) đậm tới mức được dùng làm phẩm màu thực phẩm tự nhiên",
      ["#7A1E3A", "#6A994E"], "https://vi.wikipedia.org/wiki/C%E1%BB%A7_d%E1%BB%81n"),

    # ===== LÂM NGHIỆP (4) =====
    P("do-bau", "Dó bầu (Trầm hương)", "Aquilaria crassna", "Agarwood · cây dó · trầm hương", "Trầm (Thymelaeaceae)",
      "lam-nghiep", "lam-san", "Bông (Malvales)", "Aquilaria", "A. crassna",
      "Loài cây bản địa cho trầm hương quý; phân bố rừng Hà Tĩnh, Quảng Nam, Khánh Hòa, Phú Quốc.",
      "Dó bầu là cây gỗ tạo ra trầm hương (kỳ nam) — phần gỗ tích nhựa thơm khi cây bị thương, lâm sản giá trị bậc nhất.",
      "Cây gỗ thường xanh, thân thẳng", "15–25 m", "Cây lâu năm; tạo trầm sau 7–10 năm (cấy tạo trầm)",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất feralit, thịt sâu, thoát nước",
      "Hà Tĩnh, Quảng Nam, Khánh Hòa, Kiên Giang (Phú Quốc)", "Trồng đầu mùa mưa; cấy tạo trầm khi cây ≥5 năm",
      "Ưa khí hậu nhiệt đới ẩm; trầm hình thành khi thân bị tổn thương & nhiễm nấm (cấy chế phẩm)",
      "Gieo hạt, trồng cây con", "Tạo trầm thu sau 7–10 năm", "Tùy mức cấy trầm (giá trị theo chất lượng trầm)",
      ls(("Ươm & trồng", "Năm 1–3"), ("Phát triển thân", "Năm 3–6"),
         ("Cấy tạo trầm", "Năm 6–8"), ("Thu trầm hương", "Năm 8–12+")),
      "Sâu đục thân, sâu ăn lá",
      "Trầm hương (agarwood) làm hương liệu, nước hoa, dược liệu, đồ thờ — lâm sản ngoài gỗ giá trị rất cao",
      "—", "—", "Trầm hương an thần, ấm bụng, dùng trong Đông y & tâm linh",
      "Trầm hương loại tốt giá hàng trăm triệu đến hàng tỷ đồng/kg; nghề cấy tạo trầm phát triển ở miền Trung",
      "Trầm hương chỉ hình thành khi cây dó bị thương và nhiễm nấm — phần nhựa thơm tích lại qua nhiều năm mới thành trầm",
      ["#4A2E1E", "#9C6B30"], "https://vi.wikipedia.org/wiki/D%C3%B3_b%E1%BA%A7u"),

    P("ko-nia", "Kơ nia", "Irvingia malayana", "Wild almond · cây cầy", "Kơ nia (Irvingiaceae)",
      "lam-nghiep", "go-quy", "Sơ ri (Malpighiales)", "Irvingia", "I. malayana",
      "Loài cây gỗ lớn bản địa, biểu tượng của Tây Nguyên; mọc rải rác trên nương rẫy và rừng khộp.",
      "Kơ nia là cây gỗ lớn tán tròn, rễ cọc sâu chịu hạn; gỗ cứng, hạt ăn được — gắn liền văn hóa Tây Nguyên.",
      "Cây gỗ lớn, tán tròn đều", "15–30 m", "Cây lâu năm, sinh trưởng chậm",
      "Ưa nắng hoàn toàn", "Thấp — chịu hạn rất tốt", "Đất feralit, đất xám, chịu khô hạn",
      "Tây Nguyên (Đắk Lắk, Gia Lai, Kon Tum), Đông Nam Bộ", "Quả chín mùa khô; sinh trưởng chậm",
      "Chịu hạn cực tốt nhờ rễ cọc sâu; thường được giữ lại khi phát nương làm bóng mát",
      "Gieo hạt (vỏ cứng, nảy chậm)", "Cây gỗ chục năm; quả hằng năm khi trưởng thành", "Gỗ ~ chậm; hạt thu theo mùa",
      ls(("Gieo hạt", "Năm 1"), ("Cây con chịu hạn", "Năm 1–5"),
         ("Phát triển tán", "Năm 5–20"), ("Trưởng thành & ra quả", "Năm 20+")),
      "Ít sâu bệnh; đôi khi sâu đục thân",
      "Gỗ cứng làm cột, chày cối; hạt rang ăn bùi như hạnh nhân; cây bóng mát, giá trị văn hóa",
      "Hạt giàu chất béo, đạm", "Hạt rang bùi, béo (như hạnh nhân)",
      "Nhân hạt kơ nia ăn được; dầu hạt dùng trong dân gian",
      "Giá trị văn hóa – sinh thái là chính; gỗ & hạt dùng địa phương",
      "Cây kơ nia đi vào thơ ca ('Bóng cây Kơ-nia') như biểu tượng của núi rừng Tây Nguyên và lòng thủy chung",
      ["#5A4A2E", "#8B6B3A"], "https://vi.wikipedia.org/wiki/K%C6%A1_nia"),

    P("bang-lang", "Bằng lăng", "Lagerstroemia speciosa", "Pride of India · bằng lăng nước", "Tử vi (Lythraceae)",
      "lam-nghiep", "trong-rung", "Sim (Myrtales)", "Lagerstroemia", "L. speciosa",
      "Loài cây gỗ bản địa nhiệt đới; trồng rộng làm cây bóng mát đường phố và lấy gỗ, nổi với hoa tím mùa hè.",
      "Bằng lăng là cây gỗ vừa, nở hoa tím rực mùa hè; vừa là cây cảnh quan đô thị vừa cho gỗ xây dựng.",
      "Cây gỗ vừa, rụng lá mùa khô", "10–20 m", "Cây lâu năm, khai thác gỗ sau 20–30 năm",
      "Ưa nắng hoàn toàn", "Trung bình — chịu hạn khá, ưa ẩm", "Đất thịt, phù sa, thoát nước; chịu ngập nhẹ",
      "Khắp cả nước; phổ biến cây đường phố, ven sông", "Ra hoa tím tháng 5–7 (mùa hè)",
      "Dễ trồng, ưa sáng; chịu được đất ẩm ven nước",
      "Gieo hạt, trồng cây con", "20–30 năm (gỗ); ra hoa sau vài năm", "5–8 m³ gỗ/ha/năm",
      ls(("Ươm & trồng", "Năm 1–2"), ("Sinh trưởng", "Năm 2–10"),
         ("Ra hoa & phát triển gỗ", "Năm 5–20"), ("Khai thác", "Năm 20–30")),
      "Sâu ăn lá, sâu đục thân, rệp",
      "Cây bóng mát & cảnh quan (hoa tím); gỗ làm xây dựng, đồ mộc, đóng thuyền; vỏ & lá làm thuốc",
      "—", "—", "Lá bằng lăng nước hỗ trợ hạ đường huyết (nghiên cứu dân gian & hiện đại)",
      "Giá trị cảnh quan lớn; gỗ tiêu thụ nội địa",
      "Mùa hè, bằng lăng nở tím rực cả tuyến phố — cùng phượng đỏ tạo nên sắc màu mùa hè đặc trưng Việt Nam",
      ["#7D5BA6", "#5A6B4A"], "https://vi.wikipedia.org/wiki/B%E1%BA%B1ng_l%C4%83ng_n%C6%B0%E1%BB%9Bc"),

    P("long-nao", "Long não", "Cinnamomum camphora", "Camphor tree · cây dã hương", "Long não (Lauraceae)",
      "lam-nghiep", "go-quy", "Long não (Laurales)", "Cinnamomum", "C. camphora",
      "Loài cây gỗ lớn thơm; trồng làm cây bóng mát & lấy tinh dầu long não, gỗ quý chống mối mọt.",
      "Long não là cây gỗ lớn thường xanh, toàn cây thơm; cho tinh dầu long não (camphor) và gỗ bền chống mối.",
      "Cây gỗ lớn thường xanh, tán rộng", "20–30 m", "Cây lâu năm",
      "Ưa nắng, chịu bóng khi nhỏ", "Trung bình — cần ẩm", "Đất thịt sâu, ẩm, thoát nước",
      "Trồng ở nhiều đô thị & vùng trung du miền Bắc, miền Trung", "Thường xanh; chưng tinh dầu từ gỗ & lá",
      "Ưa khí hậu ấm ẩm; cây sống rất lâu năm, có cây cổ thụ hàng trăm tuổi",
      "Gieo hạt, giâm cành", "Gỗ lâu năm; tinh dầu từ cây trưởng thành", "Gỗ & tinh dầu tùy quy mô",
      ls(("Ươm & trồng", "Năm 1–3"), ("Sinh trưởng", "Năm 3–15"),
         ("Tích lũy gỗ & tinh dầu", "Năm 15–40"), ("Khai thác", "Năm 40+")),
      "Sâu đục thân, sâu ăn lá",
      "Tinh dầu long não (camphor) làm dược phẩm, dầu xoa, xua côn trùng; gỗ thơm bền làm tủ, rương chống mối",
      "—", "—", "Long não xoa bóp giảm đau, thông mũi; lưu ý độc nếu dùng liều cao",
      "Tinh dầu long não & gỗ long não có giá trị; cây cảnh quan đô thị",
      "Cây dã hương Bắc Giang — một cây long não cổ thụ hơn ngàn năm tuổi — được công nhận là Cây Di sản Việt Nam",
      ["#5A6B4A", "#A98D5B"], "https://vi.wikipedia.org/wiki/Long_n%C3%A3o_(c%C3%A2y)"),
]


def main():
    d = json.load(open(path, encoding='utf-8'))
    have = {c['id'] for c in d['cay']}
    added = 0
    for p in NEW:
        if p['id'] in have:
            print('SKIP', p['id']); continue
        d['cay'].append(p); have.add(p['id']); added += 1
    d['_meta']['capNhat'] = '2026-05-26'
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    lvg, nhg = {}, {}
    for c in d['cay']:
        lvg[c['linhVuc']] = lvg.get(c['linhVuc'], 0)+1
        nhg[c['nhom']] = nhg.get(c['nhom'], 0)+1
    print(f'Thêm {added}. Tổng {len(d["cay"])} cây.', lvg, nhg)


if __name__ == '__main__':
    main()
