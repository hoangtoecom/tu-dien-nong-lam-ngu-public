# Từ điển Nông Lâm Ngư

Bách khoa tra cứu **180 loài** cây trồng, vật nuôi & thủy sản phổ biến ở Việt Nam, trình bày theo phong cách bản khắc cổ.

Một web tĩnh gọn (một file `index.html` + dữ liệu JSON + ảnh minh hoạ). Toàn bộ dựng bằng AI, làm cho buổi chia sẻ AI tại ĐH Nông Lâm — như một minh chứng: một người không biết code vẫn dựng được khung sản phẩm thật bằng AI.

🌐 Live: https://tudiennonglam.com

## Chạy thử

Không cần cài gì. Tải repo về, mở `index.html` bằng trình duyệt là chạy (kể cả offline).

Hoặc chạy server tĩnh:

```bash
python3 -m http.server 8000
# rồi mở http://localhost:8000
```

## Cấu trúc

- `index.html` — toàn bộ web (1 file, không framework)
- `data/tu-dien-nong-lam-ngu.json` — dữ liệu 180 loài (4 lĩnh vực, 20 nhóm)
- `img/` — ảnh minh hoạ phong cách bản khắc cổ (gen bằng AI)
- `scripts/` — script Python dựng dữ liệu + gen ảnh bằng AI (cách mình build, chia sẻ luôn cho ai tò mò)

## Lưu ý về dữ liệu

Đây là **bộ dữ liệu mẫu để demo**, phục vụ mục đích chia sẻ và giáo dục — **không phải tài liệu chuẩn ngành**. Số liệu có thể chưa chính xác tuyệt đối. Nếu dùng cho mục đích chuyên môn, vui lòng đối chiếu nguồn chính thống.

Anh em làm nông nghiệp, lâm nghiệp, hoặc đang học Nông Lâm mà thấy chỗ nào sai, mở issue góp ý giúp mình.

## License

- Code / web: **MIT** (xem `LICENSE`).
- Dữ liệu & ảnh: bộ mẫu demo, dùng lại tự do; ghi nguồn thì quý.

Tác giả: Hoàng Tô (Jordan To) · 2026
