#!/usr/bin/env python3
"""Canlı HTML sayfalarındaki ürün adı + fiyatı tarayıp fiyatlar.csv üretir.

Bu betik normalde BİR KEZ çalıştırılır (fiyatlar.csv'yi ilk oluştururken,
ya da HTML'e doğrudan yeni bir ürün eklendiğinde CSV'yi HTML ile yeniden
senkronlamak için). Günlük fiyat değişiklikleri fiyatlar.csv üzerinden,
update_html_from_csv.py ile yapılır — bu betik değil.
"""
import csv
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from price_lib import split_cards, extract_name_and_price

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(REPO_ROOT, "katalog css düzen")
OUT_CSV = os.path.join(SITE_ROOT, "fiyatlar.csv")


def main():
    rows = []
    no_price = []
    html_files = sorted(glob.glob(os.path.join(SITE_ROOT, "*.html")))

    for path in html_files:
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        for card in split_cards(content):
            result = extract_name_and_price(card)
            if not result:
                continue
            name, price, _template = result
            if not price:
                no_price.append((fname, name))
                continue
            rows.append((fname, name, price))

    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Dosya", "Urun Adi", "Fiyat"])
        for r in rows:
            w.writerow(r)

    print(f"{OUT_CSV} yazıldı: {len(rows)} satır")
    if no_price:
        print(f"Fiyatsız ürün kartı (atlandı): {len(no_price)}")
        for f, n in no_price:
            print(f"  {f}: {n}")


if __name__ == "__main__":
    main()
