#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Suy baoTonCap (LC/NT/VU/EN/CR) từ text baoTon cho CÂY (động vật đã set sẵn).
Quy tắc severe-wins: CR > EN > VU > NT. Loài phổ biến → '' (không cờ).
Chạy: python3 scripts/add-baoton-cap.py"""
import json, os, unicodedata

BASE = os.path.join(os.path.dirname(__file__), '..')
F = os.path.join(BASE, 'data', 'tu-dien-nong-lam-ngu.json')

def da(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c) != 'Mn').lower()

def cap_of(text):
    t = da(text)
    if 'cuc ky nguy cap' in t or 'critically' in t or '(cr)' in t:
        return 'CR'
    if 'endangered' in t or '(en)' in t or 'nguy cap (en' in t:
        return 'EN'
    if 'vulnerable' in t or '(vu)' in t or 'se nguy cap' in t or 'sap nguy cap' in t:
        return 'VU'
    # còn dấu hiệu bảo vệ nhưng không rõ hạng IUCN → Sắp bị đe dọa
    if any(k in t for k in ['cites', 'nghi dinh', 'sach do', 'nguy cap', 'bao ton', 'bao ve']):
        return 'NT'
    return ''

def main():
    d = json.load(open(F, encoding='utf-8'))
    items = d['cay']
    out = []
    for x in items:
        lv = str(x.get('linhVuc'))
        if lv in ('chan-nuoi', 'thuy-san'):
            continue  # động vật đã set baoTonCap
        cap = cap_of(x.get('baoTon', ''))
        x['baoTonCap'] = cap
        if cap in ('VU', 'EN', 'CR', 'NT'):
            out.append(f"{cap}\t{x['id']}\t{x.get('ten','')}")
    # hiệu chỉnh tay loài đặc biệt
    fix = {'vu-huong': 'CR', 'thong-nuoc': 'CR'}
    by = {x['id']: x for x in items}
    for cid, cap in fix.items():
        if cid in by:
            by[cid]['baoTonCap'] = cap
    json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('PLANT_CAP_RESULT:')
    for r in sorted(out):
        print('  ' + r)
    print('TOTAL_FLAGGED_PLANTS=' + str(len(out)))

if __name__ == '__main__':
    main()
