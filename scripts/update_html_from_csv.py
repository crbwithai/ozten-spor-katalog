#!/usr/bin/env python3
"""fiyatlar.csv'yi okuyup ilgili HTML sayfalarındaki fiyatları günceller.

Kullanım:
    python3 scripts/update_html_from_csv.py

fiyatlar.csv'de bir ürünün Fiyat sütununu değiştirip bu betiği çalıştırmak
yeterli — ilgili HTML sayfasındaki fiyat kartı otomatik güncellenir.
GitHub Actions da fiyatlar.csv her push'landığında bu betiği otomatik çalıştırır
(bkz. .github/workflows/update-prices.yml).

Çıkış kodu 0: her satır uygulandı. 1: eşleşmeyen satır var (rapor basılır;
eşleşen satırlar yine de yazılır, hiçbir dosya bozuk bırakılmaz).
"""
import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from price_lib import split_cards, extract_name_and_price, replace_price_in_card, format_price

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_SITE_ROOT = os.path.join(REPO_ROOT, "katalog css düzen")


def load_csv(path):
    rows = []
    with open(path, encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append((row["Dosya"].strip(), row["Urun Adi"].strip(), row["Fiyat"].strip()))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-root", default=DEFAULT_SITE_ROOT)
    ap.add_argument("--csv", default=None)
    args = ap.parse_args()
    csv_path = args.csv or os.path.join(args.site_root, "fiyatlar.csv")

    rows = load_csv(csv_path)

    by_file = {}
    for dosya, urun, fiyat in rows:
        by_file.setdefault(dosya, []).append((urun, fiyat))

    not_found = []
    changed_files = []
    changed_count = 0
    unchanged_count = 0

    for dosya, entries in by_file.items():
        path = os.path.join(args.site_root, dosya)
        if not os.path.exists(path):
            for urun, fiyat in entries:
                not_found.append((dosya, urun, "DOSYA YOK"))
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        cards = split_cards(content)
        card_index = {}
        for i, card in enumerate(cards):
            r = extract_name_and_price(card)
            if r:
                name, _price, _template = r
                card_index.setdefault(name, []).append(i)

        file_changed = False
        for urun, fiyat in entries:
            idxs = card_index.get(urun)
            if not idxs:
                not_found.append((dosya, urun, "ÜRÜN BULUNAMADI"))
                continue
            for i in idxs:
                card = cards[i]
                _name, current_price, template = extract_name_and_price(card)
                new_price_text = format_price(fiyat)
                if current_price.strip() == new_price_text.strip():
                    unchanged_count += 1
                    continue
                cards[i] = replace_price_in_card(card, new_price_text, template)
                changed_count += 1
                file_changed = True

        if file_changed:
            new_content = content.split('class="product-card')[0]
            for c in cards:
                new_content += 'class="product-card' + c
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            changed_files.append(dosya)

    print(f"Güncellenen fiyat sayısı: {changed_count}")
    print(f"Değişmeyen (zaten güncel): {unchanged_count}")
    print(f"Değişen dosya sayısı: {len(changed_files)}")
    for f in changed_files:
        print(f"  {f}")

    if not_found:
        print(f"\nUYARI: eşleşmeyen {len(not_found)} satır:")
        for dosya, urun, reason in not_found:
            print(f"  {dosya}: {urun}  [{reason}]")
        sys.exit(1)


if __name__ == "__main__":
    main()
