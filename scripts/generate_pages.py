#!/usr/bin/env python3
"""futbol-yeni.html prototipindeki tasarımı (ozten-yeni.css + site.js) kalan
kategori sayfalarına uygular. Her sayfa: eski şablondaki ürün kartlarını
(sahte sayfalama birleştirilmiş, açıklama parçaları tek paragrafta) yeni
tasarımın kart yapısına çevirir; header/kategori paneli/alt kategori şeridi/
footer/alt çubuk sabit şablondan üretilir.

Kullanım:
    python3 scripts/generate_pages.py                  # tüm 80 dosyayı üret
    python3 scripts/generate_pages.py --only futbol.html basketbol.html
    python3 scripts/generate_pages.py --dry-run         # sadece rapor, yazma
"""
import argparse
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from categories import CATEGORIES, find_group_for_file
from rollout_lib import extract_all_cards, render_card

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(REPO_ROOT, "katalog css düzen")


def render_kategori_panel(active_cat_num):
    items = []
    for cat_num, label, top_file, _desc, _chips in CATEGORIES:
        aktif = " aktif" if cat_num == active_cat_num else ""
        items.append(f'        <a class="kategori-link{aktif}" href="{top_file}">{label}</a>')
    return (
        '<nav class="kategori-panel" id="kategoriPanel" hidden>\n'
        '  <div class="kategori-panel-baslik">TÜM KATEGORİLER</div>\n'
        '  <div class="kategori-izgara">\n'
        + "\n".join(items) + "\n"
        '  </div>\n'
        '</nav>'
    )


def render_alt_kat_serit(chips, active_file):
    if not chips:
        return ""
    items = []
    for chip_file, chip_label in chips:
        aktif = " aktif" if chip_file == active_file else ""
        items.append(f'      <a class="alt-kat-cip{aktif}" href="{chip_file}">{chip_label}</a>')
    return (
        '\n<nav class="alt-kat-serit" aria-label="Alt kategoriler">\n'
        '  <div class="alt-kat-ic">\n'
        + "\n".join(items) + "\n"
        '  </div>\n'
        '</nav>\n'
    )


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{label} — Özten Spor Kataloğu</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="ozten-yeni.css">
<script src="sepet.js" defer></script>
<script src="site.js" defer></script>
</head>
<body>

<header class="ust-cubuk">
  <a class="marka" href="index.html">ÖZTEN<span>SPOR</span></a>
  <div class="ust-arama">
    <span class="arama-ikon">&#9906;</span>
    <input type="text" id="aramaKutusu" placeholder="Ürün ara" autocomplete="off" oninput="aramaFiltrele(this)">
  </div>
  <div class="ust-butonlar">
    <button type="button" class="ust-btn" id="kategoriAc">Kategoriler &#9662;</button>
    <button type="button" class="ust-btn" id="sepetAc">Sepetim <span class="ust-rozet" id="ustSepetSayi">0</span></button>
  </div>
</header>

{kategori_panel}

<section class="kat-basi">
  <div class="kat-basi-ic">
    <div class="kat-etiket">KATEGORİ {cat_num}</div>
    <h1>{label}</h1>
    <p class="kat-aciklama">{desc}</p>
    <span class="kat-sayac">{urun_sayisi} ürün</span>
  </div>
</section>
{alt_kat_serit}
<main class="icerik">
  <p class="urun-bulunamadi" hidden>Aramanla eşleşen ürün bulunamadı.</p>
  <div class="product-grid">
{cards}
  </div>
</main>

<a class="wa-buton" href="https://wa.me/905522025737" target="_blank" rel="noopener" aria-label="WhatsApp'tan yazın">
  <svg viewBox="0 0 32 32" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3 9 3 16c0 2.4.6 4.6 1.8 6.6L3 29l6.6-1.7c1.9 1 4 1.6 6.4 1.6 7 0 13-6 13-13S23 3 16 3zm7.6 18.4c-.3.9-1.7 1.7-2.7 1.9-.7.1-1.6.2-4.6-1-3.9-1.6-6.4-5.5-6.6-5.8-.2-.3-1.6-2.1-1.6-4s1-2.8 1.3-3.2c.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1.1 2.6 1.2 2.8.1.2.2.4 0 .7-.1.3-.2.4-.4.6-.2.2-.4.5-.6.7-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.3.2.5.1.7-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2.1 1 2.5 1.2.4.2.6.3.7.5.1.2.1 1-.2 1.9z"/></svg>
</a>

<footer class="alt-bilgi">
  <div class="alt-bilgi-ic">
    <strong>ÖZTEN SPOR</strong>
    Kirazlı Mahallesi 1201. Sokak, Bağcılar / İstanbul<br>
    <a href="mailto:oztensporltd@gmail.com">oztensporltd@gmail.com</a>
  </div>
</footer>

<nav class="alt-cubuk">
  <a class="alt-btn" href="index.html">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>
    Ana Sayfa
  </a>
  <button type="button" class="alt-btn" id="altAra">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    Ara
  </button>
  <button type="button" class="alt-btn" id="altKategori">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    Kategoriler
  </button>
  <button type="button" class="alt-btn" id="altSepet">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6h15l-1.5 9h-12z"/><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M6 6 5 3H3"/></svg>
    Sepet
    <span class="alt-rozet" id="altSepetSayi" hidden>0</span>
  </button>
</nav>

</body>
</html>
"""


def generate_one(fname, dry_run=False):
    group, _chip_label = find_group_for_file(fname)
    if not group:
        print(f"UYARI: {fname} için grup bulunamadı, atlandı.")
        return False
    cat_num, label, top_file, desc, chips = group

    src_path = os.path.join(SITE_ROOT, fname)
    with open(src_path, encoding="utf-8") as f:
        old_content = f.read()

    cards = extract_all_cards(old_content)
    if not cards:
        print(f"UYARI: {fname} içinde hiç geçerli ürün kartı bulunamadı, atlandı.")
        return False

    cards_html = "\n".join(render_card(c) for c in cards)

    out = PAGE_TEMPLATE.format(
        label=label,
        cat_num=cat_num,
        desc=desc,
        urun_sayisi=len(cards),
        kategori_panel=render_kategori_panel(cat_num),
        alt_kat_serit=render_alt_kat_serit(chips, fname),
        cards=cards_html,
    )

    if dry_run:
        print(f"{fname}: {len(cards)} ürün (dry-run, yazılmadı)")
        return True

    with open(src_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{fname}: {len(cards)} ürün yazıldı")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None, help="sadece bu dosyaları üret")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.only:
        targets = args.only
    else:
        targets = sorted(
            os.path.basename(p) for p in glob.glob(os.path.join(SITE_ROOT, "*.html"))
            if os.path.basename(p) not in ("index.html", "futbol-yeni.html")
        )

    ok = 0
    for fname in targets:
        if generate_one(fname, dry_run=args.dry_run):
            ok += 1
    print(f"\nToplam: {ok}/{len(targets)} sayfa işlendi.")


if __name__ == "__main__":
    main()
