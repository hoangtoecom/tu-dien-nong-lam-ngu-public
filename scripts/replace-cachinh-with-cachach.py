# -*- coding: utf-8 -*-
"""Thay loài cá chình (ca-chinh) bằng cá chạch lấu (ca-chach) trong data."""
import json, os
P=os.path.join(os.path.dirname(__file__),'..','data','cay.json')
d=json.load(open(P,encoding='utf-8'))
rec={
 "id":"ca-chach","ten":"Cá chạch lấu","tenKhoaHoc":"Mastacembelus favus","tenKhac":"Tire-track spiny eel · chạch lấu","nhom":"ca-nuoi","linhVuc":"thuy-san","anh":"img/ca-chach.jpg",
 "moTa":"Cá chạch lấu là cá nước ngọt thân dài, mõm nhọn, da trơn hoa văn vằn đẹp; thịt chắc ngọt ít xương, là đặc sản nuôi giá cao ở Đồng bằng Sông Cửu Long.",
 "moiTruongNuoc":"Nước ngọt (sông, ao, bể); thích đáy có chỗ trú","nhietDoPH":"26–32°C, pH 6,5–8",
 "thucAn":"Trùn, ốc, cá tạp, thức ăn viên đạm cao; ăn thiên động vật","hinhThucNuoi":"Bể lót bạt, ao, bè có giá thể/ống trú; mật độ vừa",
 "thuHoach":"8–12 tháng, đạt 150–400 g/con","sanLuong":"Giá trị cao dù sản lượng vừa",
 "sanPham":"Cá chạch lấu thương phẩm (đặc sản nhà hàng)","benhThuongGap":"Nấm, ký sinh trùng, lở loét, đường ruột",
 "vungNuoi":"Đồng bằng Sông Cửu Long (An Giang, Đồng Tháp), miền Trung",
 "giaTri":"Đặc sản nước ngọt giá cao; nghề nuôi chạch lấu cho con giống & cá thịt lãi tốt.",
 "suThatThuVi":"Tuy thân dài như lươn, cá chạch lấu thực ra là CÁ có vây — dải vây lưng gai chạy dọc lưng và hoa văn vằn như vết bánh xe là dấu nhận dạng.",
 "mauDacTrung":["#6b5a3a","#cabf8a"],"nguon":"https://vi.wikipedia.org/wiki/C%C3%A1_ch%E1%BA%A1ch_l%E1%BA%A5u"}
i=next((k for k,c in enumerate(d['cay']) if c['id']=='ca-chinh'), None)
if i is not None: d['cay'][i]=rec; print("Thay ca-chinh -> ca-chach tại vị trí", i)
elif not any(c['id']=='ca-chach' for c in d['cay']): d['cay'].append(rec); print("Thêm ca-chach (không thấy ca-chinh)")
else: print("ca-chach đã có, bỏ qua")
json.dump(d,open(P,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print("Tổng:",len(d['cay']))
