#!/usr/bin/env bash
# Tối ưu ảnh: resize + nén JPEG bằng sips (macOS) — giảm dung lượng web.
# Thumbnail (img/*.jpg) -> max 760px, q80.  Detail (img/detail/*.jpg) -> max 1100px, q82.
# Chạy in-place (idempotent: chạy lại chỉ nén thêm chút). bash scripts/optimize-images.sh
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$DIR"

opt() { # $1=glob dir, $2=maxdim, $3=quality
  local n=0
  for f in $1; do
    sips -s format jpeg -s formatOptions "$3" -Z "$2" "$f" --out "$f" >/dev/null 2>&1 && n=$((n+1))
  done
  echo "  $1 → $n ảnh"
}

echo "Trước:"; du -sh img/
echo "Đang tối ưu thumbnail (760px, q80)..."
opt "img/*.jpg" 760 80
echo "Đang tối ưu ảnh chi tiết (1100px, q82)..."
opt "img/detail/*.jpg" 1100 82
echo "Đang tối ưu visual UI (1200px, q82)..."
[ -d img/ui ] && opt "img/ui/*.jpg" 1200 82
echo "Sau:"; du -sh img/
