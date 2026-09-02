import re

CARD_SPLIT_RE = re.compile(r'class="product-card')

# Template A (canlı sayfalar, index.html dahil):
#   <span class="pf-label filled">Ürün Adı : NAME</span>
#   ...
#   <div class="pf pf-price"><span class="pf-label">Fiyat</span><span class="pf-line short...">PRICE</span></div>
NAME_RE_A = re.compile(r'class="pf-label filled">Ürün Adı\s*:\s*([^<]+)</span>')
PRICE_BLOCK_RE_A = re.compile(
    r'(<div class="pf pf-price"><span class="pf-label">Fiyat\s*</span><span class="pf-line short[^"]*"[^>]*>)([^<]*)(</span></div>)'
)

# Template B (futbol-yeni.html gibi yeni tasarım prototipleri):
#   <span class="pf-label"><span class="gizli-etiket">Ürün Adı : </span>NAME</span>
#   ...
#   <div class="pf pf-price"><span class="pf-line">PRICE</span></div>
NAME_RE_B = re.compile(r'class="gizli-etiket">Ürün Adı\s*:\s*</span>([^<]+)</span>')
PRICE_BLOCK_RE_B = re.compile(
    r'(<div class="pf pf-price"><span class="pf-line"[^>]*>)([^<]*)(</span></div>)'
)


def split_cards(html):
    """HTML içeriğini product-card bloklarına ayırır. Her blok kendi
    kartının başlangıcından bir sonraki kartın başlangıcına kadardır."""
    parts = CARD_SPLIT_RE.split(html)
    if len(parts) <= 1:
        return []
    return parts[1:]


def extract_name_and_price(card_block):
    """Bir kart bloğundan (ürün adı, fiyat metni, şablon) döndürür.
    Bulunamazsa None döner."""
    m = NAME_RE_A.search(card_block)
    if m:
        pm = PRICE_BLOCK_RE_A.search(card_block)
        price = pm.group(2).strip() if pm else ""
        return m.group(1).strip(), price, "A"
    m = NAME_RE_B.search(card_block)
    if m:
        pm = PRICE_BLOCK_RE_B.search(card_block)
        price = pm.group(2).strip() if pm else ""
        return m.group(1).strip(), price, "B"
    return None


def format_price(fiyat_str):
    """'1930' -> '1.930 ₺', '80' -> '80 ₺'."""
    digits = re.sub(r'[^\d]', '', fiyat_str)
    if not digits:
        return fiyat_str
    n = int(digits)
    formatted = f"{n:,}".replace(",", ".")
    return f"{formatted} ₺"


def replace_price_in_card(card_block, new_price_text, template):
    if template == "A":
        return PRICE_BLOCK_RE_A.sub(lambda m: m.group(1) + new_price_text + m.group(3), card_block, count=1)
    else:
        return PRICE_BLOCK_RE_B.sub(lambda m: m.group(1) + new_price_text + m.group(3), card_block, count=1)
