#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gắn anhChiTiet='img/detail/<id>.jpg' cho mọi mục có file ảnh chi tiết mà chưa khai báo.
Tự nhận đúng các loài mới vừa gen ảnh detail. python3 scripts/set-anhchitiet-from-detail.py"""
import json, os
BASE = os.path.join(os.path.dirname(__file__), '..')
PATH = os.path.join(BASE, 'data', 'tu-dien-nong-lam-ngu.json')

def main():
    data = json.load(open(PATH, encoding='utf-8'))
    n = 0
    for c in data['cay']:
        det = os.path.join(BASE, 'img', 'detail', c['id'] + '.jpg')
        if os.path.exists(det) and not c.get('anhChiTiet'):
            c['anhChiTiet'] = f"img/detail/{c['id']}.jpg"; n += 1
    json.dump(data, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'Gắn anhChiTiet cho {n} mục.')

if __name__ == '__main__':
    main()
