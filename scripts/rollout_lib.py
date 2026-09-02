import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from price_lib import split_cards, NAME_RE_A, PRICE_BLOCK_RE_A

FILLED_RE = re.compile(r'<div class="pf pf-filled"><span class="pf-label filled">([^<]*)</span></div>')
IMG_RE = re.compile(r'<img src="([^"]+)" alt="([^"]*)"')


def extract_full_card(card_block):
    """Eski şablon kart bloğundan (name, desc, price, img_src, img_alt) çıkarır.
    Boş/doldurulmamış (hiç ürün adı olmayan) kartlarda None döner."""
    name_match = NAME_RE_A.search(card_block)
    if not name_match:
        return None
    name = name_match.group(1).strip()

    filled = FILLED_RE.findall(card_block)
    desc_parts = []
    for text in filled[1:]:
        text = re.sub(r'^Açıklama\s*:?\s*', '', text).strip()
        if text:
            desc_parts.append(text)
    desc = ' '.join(desc_parts)

    price_match = PRICE_BLOCK_RE_A.search(card_block)
    price = price_match.group(2).strip() if price_match else ''

    img_match = IMG_RE.search(card_block)
    img_src = img_match.group(1) if img_match else ''
    # alt metni her zaman ürün adından üretilir: eski şablonun kendi alt
    # metni bazen kısaltılmış/eksik oluyordu (ör. "Futbol Topu Shine Pro"
    # vs. ürün adı "Helix Futbol Topu Shine Pro No:4").
    img_alt = name

    return {"name": name, "desc": desc, "price": price, "img_src": img_src, "img_alt": img_alt}


def extract_all_cards(html_content):
    """Bir eski şablon sayfasındaki (sahte sayfalama varsa dahil, hepsi birleşik)
    tüm geçerli ürün kartlarını sırayla döndürür."""
    cards = []
    for block in split_cards(html_content):
        c = extract_full_card(block)
        if c:
            cards.append(c)
    return cards


def html_escape_attr(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;")


def render_card(card):
    return (
        '      <div class="product-card">\n'
        f'        <div class="kart-gorsel"><img src="{card["img_src"]}" alt="{html_escape_attr(card["img_alt"])}" loading="lazy"></div>\n'
        '        <div class="kart-govde">\n'
        f'          <span class="pf-label"><span class="gizli-etiket">Ürün Adı : </span>{card["name"]}</span>\n'
        f'          <p class="kart-aciklama">{card["desc"]}</p>\n'
        '          <div class="kart-alt">\n'
        f'            <div class="pf pf-price"><span class="pf-line">{card["price"]}</span></div>\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>'
    )
