#!/usr/bin/env python3
"""Yeni tasarımda index-yeni.html (ana sayfa taslağı) üretir.
Kinetra'dan esinlenilen kategori duvarı, hero, manifesto, istatistik ve
iletişim bölümlerini; mevcut ust-cubuk/kategori-panel/footer/alt-cubuk
şablonuyla birleştirir. Vitrin ürünleri ve iletişim metni index.html'in
mevcut içeriğinden alınmıştır.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from categories import CATEGORIES, all_files_in_group
from generate_pages import render_kategori_panel

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(REPO_ROOT, "katalog css düzen")

# (cat_num, label, top_file, img_src, img_alt) — her kategorinin ilk ürününden alındı
DUVAR_GORSEL = {
    "01": ("%C4%B0mage/Futbol%20image/futbol%20topu%20shine%20pro.jpg", "Helix Futbol Topu Shine Pro No:4"),
    "02": ("%C4%B0mage/Basketbol%20image/C7%20HATTRICK.webp", "C7 HATTRICK"),
    "03": ("%C4%B0mage/Voleybol%20image/BV100%20ALTIS.webp", "BV100 ALTIS"),
    "04": ("%C4%B0mage/Badminton%20image/B100%20ALTIS.webp", "B100 ALTIS"),
    "05": ("%C4%B0mage/Masa%20Tenisi%20image/TS2000%20SPORTICA.webp", "TS2000 SPORTICA"),
    "06": ("%C4%B0mage/Tenis%20image/ATS19%20HATTRICK.webp", "ATS19 HATTRICK"),
    "07": ("%C4%B0mage/Atlama%20ipi%20image/EY116%20ALTIS.webp", "EY116 ALTIS"),
    "08": ("%C4%B0mage/El%20yaylar%C4%B1/EY103%20ALTIS.webp", "EY103 ALTIS"),
    "09": ("%C4%B0mage/Yoga%20ve%20Pilates%20image/P%C4%B0LATES%20TOPU%20HB20%20HATTRICK.webp", "PİLATES TOPU HB20 HATTRICK"),
    "10": ("%C4%B0mage/Fitness%20image/DAMBIL%20SET%C4%B0%20DS10%20ALTIS.webp", "DAMBIL SETİ DS10 ALTIS"),
    "11": ("%C4%B0mage/Y%C3%BCzme%20image/CROSSFIT%20HALATI%203809CRS.webp", "CROSSFIT HALATI 3809CRS"),
    "12": ("%C4%B0mage/Hentbol%20image/HB60%20HATTRICK.webp", "HB60 HATTRICK"),
    "13": ("%C4%B0mage/Y%C3%BCzme%20image/ADG23%20HATTRICK.webp", "ADG23 HATTRICK"),
    "14": ("%C4%B0mage/Bocce%20image/BCS08%20HATTRICK.webp", "BCS08 HATTRICK"),
    "15": ("%C4%B0mage/hokey%20image/Helix%20Hokey%20%C4%B0pli%20Antrenman%20Topu%20Beyaz.png", "Helix Hokey İpli Antrenman Topu Beyaz"),
    "16": ("%C4%B0mage/kano%20image/Helix%20SUP%20%C5%9Ei%C5%9Fme%20K%C3%BCrek%20S%C3%B6rf%C3%BC%20PLB%2010%276%27%27.webp", "Helix SUP Şişme Kürek Sörfü PLB 10'6''"),
    "17": ("%C4%B0mage/beyzbol%20image/Helix%20Beyzbol%20At%C4%B1%C5%9F%20Makinas%C4%B1%20Topu%20AB-9.webp", "Helix Beyzbol Atış Makinası Topu AB-9"),
    "18": ("%C4%B0mage/kaykay%20paten%20kask/Helix%20Paten%20-%20Pembe.webp", "Helix Paten - Pembe"),
    "19": ("%C4%B0mage/oryantring%20image/Helix%20El%20Pusula%20OC-50.webp", "Helix El Pusula OC-50"),
    "20": ("%C4%B0mage/padel%20image/Helix%20Padel%20Raket%20Fiber%20FPD-10.webp", "Helix Padel Raket Fiber FPD-10"),
    "21": ("%C4%B0mage/pickleball%20image/Helix%20Pickleball%20Filesi%20Portatif.webp", "Helix Pickleball Filesi Portatif"),
    "22": ("%C4%B0mage/ragbi%20image/Helix%20Ragbi%20M%C3%BCcadele%20%C3%9Cst%20Minderi%20RM-2%2080x44x25cm.webp", "Helix Ragbi Mücadele Üst Minderi RM-2"),
    "23": ("%C4%B0mage/satran%C3%A7%20image/Helix%20Matara%20Klasik%20SMB01%20Satran%C3%A7%20Tak%C4%B1m%C4%B1.webp", "Helix Matara Klasik SMB01 Satranç Takımı"),
    "24": ("%C4%B0mage/softball%20image/Helix%20Softbol%20Topu%20Sert%20MSB-H12%20TRF%20Onayl%C4%B1.webp", "Helix Softbol Topu Sert MSB-H12"),
    "25": ("%C4%B0mage/SQUASH%20%C4%B0MAGE/Helix%20Squash%20Raketi%20Buddie%20SQ-030.webp", "Helix Squash Raketi Buddie SQ-030"),
    "26": ("%C4%B0mage/dart%20image/Hatrrick%20Dart%20Oku%2018%20GR.webp", "Hatrrick Dart Oku 18 GR"),
    "27": ("%C4%B0mage/Atletizm%20image/Vinex%20Atma%20%C3%87emberi%20G%C3%BClle%20%C3%87eki%C3%A7%20DSHC-SPA10.webp", "Vinex Atma Çemberi Gülle Çekiç"),
    "28": ("%C4%B0mage/cimnastik%20image/Firefly%20Batakl%C4%B1k%20Minderi%20100x200x10cm.webp", "Firefly Bataklık Minderi"),
    "29": ("%C4%B0mage/Sa%C4%9Fl%C4%B1k%20topu%20image/Helix%20Sa%C4%9Fl%C4%B1k%20Topu%20Z%C4%B1plamayan%20RSB%2010kg.webp", "Helix Sağlık Topu Zıplamayan RSB 10kg"),
    "30": ("%C4%B0mage/su%20topu%20image/Helix%20Su%20Topu%20Kalesi%20WPG10.webp", "Helix Su Topu Kalesi WPG10"),
    "31": ("%C4%B0mage/oyun%20grubu%20image/Helix%20Balon%20Multicolor%20CB%20100%27l%C3%BC.webp", "Helix Balon Multicolor CB 100'lü"),
    "32": ("%C4%B0mage/D%C3%B6v%C3%BC%C5%9F%20image/BBS10%20HATTRICK.webp", "BBS10 HATTRICK"),
}

# Vitrin (öne çıkanlar) — mevcut index.html'in "featured" kartlarından taşındı
VITRIN = [
    ("%C4%B0mage/Dart.image/Helix%20Dart%20Tahtas%C4%B1%20DBSA-30%20WDF%20Onayl%C4%B1.jpeg",
     "Helix Dart Tahtası DBSA-30 WDF Onaylı",
     "WDF onaylı, A sınıfı doğal sisal yapı, 45 cm çap / 3,8 cm kalınlık. Kendini onaran yüzey ile uzun ömürlü, kulüp ve turnuva kullanımına uygun.",
     "2.750 ₺"),
    ("%C4%B0mage/Futbol%20image/Helix%20Futbol%20Topu%20Hybrid%20Unity.jpg",
     "Helix Futbol Topu Hybrid Unity No:5",
     "32 panel – klasik dengeli tasarım, Hibrit dikiş (makine + el dikişi hissi), PU suni deri yüzey malzeme, Çok katmanlı polyester-pamuk astar. Lateks destekli form koruma, Dayanıklı bladder – yüksek hava tutuşu, 5 – resmi standart ölçü.",
     "650 ₺"),
    ("%C4%B0mage/Futbol%20image/PLATINO%20PRO%20HATTRICK%20NO%205.webp",
     "PLATINO PRO HATTRICK NO:5",
     "5 Numara, Premium PU yüzey, Hybrid (yapıştırma) teknoloji, Butil iç lastik 380 g. Salon kullanımına uygun, Maç ve antrenman kullanımına uygun.",
     "720 ₺"),
    ("%C4%B0mage/Voleybol%20image/Summit%20SMT-X360.png",
     "Summit SMT-X360",
     "5 Numara, Sarı-Lacivert renk, Dayanıklı kauçuk yüzey, Antrenman topu. Kapalı ve açık saha antrenmanlarına uygun, Ekonomik ve dayanıklı kullanım.",
     "560 ₺"),
    ("%C4%B0mage/Voleybol%20image/PROFINAL%20HATTR%C4%B0CK.webp",
     "PROFINAL HATTRİCK",
     "5 Numara, Sentetik deri (PVC) yüzey, El dikişli, Butil iç lastik 260–280 g ağırlık. Salon kullanımına uygun, Antrenman ve maç kullanımına uygun.",
     "330 ₺"),
    ("%C4%B0mage/Basketbol%20image/Helix%20Basketbol%20Topu%20Wizard%20RX8%20%20NO%207.webp",
     "Helix Basketbol Topu Wizard RX8 No:7",
     "Helix Wizard RX8, 7 numara, 600–650 g ağırlık, 12 panel, Outdoor (dış mekân). Okul, sokak basketbolu, spor kulübü, antrenman.",
     "370 ₺"),
]


def render_duvar():
    items = []
    for cat_num, label, top_file, _desc, _chips in CATEGORIES:
        img_src, img_alt = DUVAR_GORSEL[cat_num]
        items.append(f'''      <a class="kat-duvar-oge oz-belir" href="{top_file}">
        <span class="kat-duvar-gorsel"><img src="{img_src}" alt="" loading="lazy"></span>
        <span class="kat-duvar-no">{cat_num}</span>
        <span class="kat-duvar-ad">{label}</span>
      </a>''')
    return "\n".join(items)


def render_vitrin():
    items = []
    for img_src, name, desc, price in VITRIN:
        items.append(f'''      <div class="product-card oz-vitrin-kart oz-belir">
        <span class="oz-vitrin-rozet">ÇOK TERCİH EDİLEN</span>
        <div class="kart-gorsel"><img src="{img_src}" alt="{name}" loading="lazy"></div>
        <div class="kart-govde">
          <span class="pf-label"><span class="gizli-etiket">Ürün Adı : </span>{name}</span>
          <p class="kart-aciklama">{desc}</p>
          <div class="kart-alt">
            <div class="pf pf-price"><span class="pf-line">{price}</span></div>
          </div>
        </div>
      </div>''')
    return "\n".join(items)


PAGE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Özten Spor Kataloğu — Toptan ve Perakende Spor Malzemeleri</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="ozten-yeni.css">
<script src="sepet.js" defer></script>
<script src="site.js" defer></script>
<script src="index.js" defer></script>
</head>
<body>

<header class="ust-cubuk">
  <a class="marka" href="index.html">ÖZTEN<span>SPOR</span></a>
  <div class="ust-arama">
    <span class="arama-ikon">&#9906;</span>
    <input type="text" id="aramaKutusu" placeholder="Ürün ara" autocomplete="off" oninput="siteGeneliAra(this)">
    <div id="aramaSonuclari" class="arama-sonuclari"></div>
    <p class="urun-bulunamadi" hidden>Aramanla eşleşen ürün bulunamadı.</p>
  </div>
  <div class="ust-butonlar">
    <button type="button" class="ust-btn" id="kategoriAc">Kategoriler &#9662;</button>
    <button type="button" class="ust-btn" id="sepetAc">Sepetim <span class="ust-rozet" id="ustSepetSayi">0</span></button>
  </div>
</header>

{kategori_panel}

<section class="oz-hero">
  <div class="oz-hero-metin">
    <div class="oz-hero-kicker">SPOR MALZEMELERİ KATALOĞU · 2026</div>
    <h1>Güvenle Oynayın.<br>Kalite ile Kazanın.</h1>
    <p class="oz-hero-slogan">32 spor branşında toptan ve perakende ekipman. Kulüplere, mağazalara ve distribütörlere hızlı, güvenilir tedarik.</p>
    <div class="oz-hero-cta">
      <a href="#kategoriler" class="oz-btn oz-btn-dolu">Kategorileri Keşfet</a>
    </div>
  </div>
  <div class="oz-hero-kisiler">
    <div class="oz-hero-kisiler-baslik">Bir satış temsilcimizi seçin, hemen WhatsApp'tan ulaşın</div>
    <div id="iletisimKisiler" class="oz-kisi-liste"></div>
  </div>
</section>

<section class="oz-bolum oz-manifesto">
  <div class="oz-bolum-etiket">HAKKIMIZDA</div>
  <h2 class="oz-belir">Sahada da, İşte de Güvenilir Ortağınız</h2>
  <div class="oz-belir">
    <p>ÖZTEN SPOR olarak; futboldan fitnessa, atletizmden masa tenisine kadar geniş bir ürün yelpazesiyle toptan ve perakende spor malzemesi alıcılarının yanında yer alıyoruz.</p>
    <p>Deneyimli ekibimiz ve güçlü tedarik ağımız sayesinde kulüplere, mağazalara ve distribütörlere hızlı, güvenilir ve rekabetçi çözümler sunuyoruz.</p>
  </div>
  <div class="oz-mv-grid">
    <div class="oz-mv-card oz-belir">
      <div class="oz-mv-cubuk" style="background:var(--kirmizi);"></div>
      <h3>Misyonumuz</h3>
      <p>Müşterilerimizin performansını ve konforunu artıracak yenilikçi, dayanıklı ve erişilebilir spor ürünleri sunarak, onların sportif hedeflerine ulaşmalarındaki en büyük destekçisi olmak.</p>
    </div>
    <div class="oz-mv-card oz-belir">
      <div class="oz-mv-cubuk" style="background:var(--turuncu);"></div>
      <h3>Vizyonumuz</h3>
      <p>Sektördeki yenilikleri takip ederek, her yaştan bireyin sporu bir yaşam tarzı haline getirdiği, bölgesinin en çok tercih edilen ve referans gösterilen lider spor merkezi olmak.</p>
    </div>
  </div>
  <div class="oz-stat-row">
    <div class="oz-stat oz-belir"><span class="oz-stat-num">1000+</span><span class="oz-stat-label">Ürün Çeşidi</span></div>
    <div class="oz-stat oz-belir"><span class="oz-stat-num">32</span><span class="oz-stat-label">Kategori</span></div>
    <div class="oz-stat oz-belir"><span class="oz-stat-num">100+</span><span class="oz-stat-label">İş Ortağı</span></div>
    <div class="oz-stat oz-belir"><span class="oz-stat-num">5+</span><span class="oz-stat-label">Yıllık Deneyim</span></div>
  </div>
</section>

<section class="oz-bolum oz-bolum-koyu" id="kategoriler">
  <div class="oz-bolum-etiket">KATALOG</div>
  <h2 class="oz-belir">32 Branş, Tek Katalog</h2>
  <p class="oz-bolum-lead oz-belir">Bir kategoriye dokunun, o branşın imza ürünüyle tanışın.</p>
  <div class="kat-duvar-izgara">
{duvar}
  </div>
</section>

<section class="oz-bolum">
  <div class="oz-bolum-etiket" style="color:var(--kirmizi);">VİTRİN</div>
  <h2 class="oz-belir">En Çok Tercih Edilenler</h2>
  <p class="oz-bolum-lead oz-belir">Alıcılarımızın ve kulüplerin en çok tercih ettiği ürünler tek sayfada.</p>
  <div class="product-grid" style="margin-top:40px;">
{vitrin}
  </div>
</section>

<section class="oz-bolum oz-bolum-koyu" id="iletisim">
  <div class="oz-bolum-etiket">İLETİŞİM</div>
  <h2 class="oz-belir">Bize Ulaşın</h2>
  <p class="oz-bolum-lead oz-belir">Toptan ve perakende sipariş, iş birliği ve bilgi talepleriniz için bizimle iletişime geçin.</p>
  <div class="oz-iletisim-grid">
    <div class="oz-iletisim-kart oz-belir">
      <div class="oz-iletisim-ikon">✉</div>
      <div><h4>E-posta</h4><p><a href="mailto:oztensporltd@gmail.com" style="color:inherit;">oztensporltd@gmail.com</a></p></div>
    </div>
    <div class="oz-iletisim-kart oz-belir">
      <div class="oz-iletisim-ikon">⚑</div>
      <div><h4>Adres</h4><p>Kirazlı Mahallesi 1201. Sokak, Bağcılar / İstanbul</p></div>
    </div>
    <div class="oz-iletisim-kart oz-belir">
      <div class="oz-iletisim-ikon">@</div>
      <div><h4>Sosyal Medya</h4><p>@oztenspor — Instagram / LinkedIn / Facebook</p></div>
    </div>
  </div>
</section>

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


INDEX_JS = """/* Ana sayfaya özel: site-geneli arama (TÜM kategori/alt kategori sayfalarını
   tarar) + scroll'da belirme. site.js'teki aramaFiltrele (tek sayfa içi filtre)
   ile karışmasın diye ayrı isim kullanılıyor: siteGeneliAra. Kategori
   sayfalarında bu dosya yüklenmez.

   TUM_KATEGORI_DOSYALARI bu dosyanın kendisi gibi scripts/generate_index.py
   tarafından scripts/categories.py'den otomatik üretilir — elle düzenlemeyin,
   yeni kategori/alt kategori eklenince scripts/generate_index.py yeniden
   çalıştırılmalı. */
var TUM_KATEGORI_DOSYALARI = [
{dosyalar}
];

var katalogVerisi = null;

function katalogYukle(cb) {{
  if (katalogVerisi) {{ cb(); return; }}
  katalogVerisi = [];
  var kalan = TUM_KATEGORI_DOSYALARI.length;
  TUM_KATEGORI_DOSYALARI.forEach(function (href) {{
    fetch(href).then(function (r) {{ return r.text(); }}).then(function (html) {{
      var dom = new DOMParser().parseFromString(html, 'text/html');
      dom.querySelectorAll('.product-card').forEach(function (k) {{
        var e = k.querySelector('.pf-label');
        var ad = e ? e.textContent.replace(/^Ürün Adı\\s*:?\\s*/, '').trim() : '';
        var img = k.querySelector('img');
        if (ad) katalogVerisi.push({{ ad: ad, gorsel: img ? img.getAttribute('src') : '', href: href }});
      }});
    }}).catch(function () {{}}).then(function () {{ if (--kalan === 0) cb(); }});
  }});
}}

function siteGeneliAra(inp) {{
  var q = inp.value.trim();
  var kutu = document.getElementById('aramaSonuclari');
  if (!q) {{ kutu.innerHTML = ''; document.querySelector('.urun-bulunamadi').hidden = true; return; }}
  katalogYukle(function () {{
    // aramaSkoru (site.js) yazım hatalarını tolere eder, kelime sırasını önemsemez.
    // En iyi eşleşme en üstte olacak şekilde sıralanır.
    var sonuc = katalogVerisi
      .map(function (u) {{ return {{ u: u, skor: aramaSkoru(u.ad, q) }}; }})
      .filter(function (x) {{ return x.skor > 0; }})
      .sort(function (a, b) {{ return b.skor - a.skor; }})
      .slice(0, 40)
      .map(function (x) {{ return x.u; }});
    kutu.innerHTML = sonuc.map(function (u) {{
      return '<a class="arama-sonuc-item" href="' + u.href + '"><img src="' + u.gorsel + '" alt=""><span>' + u.ad + '</span></a>';
    }}).join('');
    document.querySelector('.urun-bulunamadi').hidden = sonuc.length > 0;
  }});
}}

(function () {{
  var elemanlar = document.querySelectorAll('.oz-belir');
  if (!elemanlar.length) return;
  if (!('IntersectionObserver' in window)) {{
    elemanlar.forEach(function (el) {{ el.classList.add('gorunur'); }});
    return;
  }}
  var gozlemci = new IntersectionObserver(function (girenler) {{
    girenler.forEach(function (giren) {{
      if (giren.isIntersecting) {{
        giren.target.classList.add('gorunur');
        gozlemci.unobserve(giren.target);
      }}
    }});
  }}, {{ threshold: 0.15 }});
  elemanlar.forEach(function (el) {{ gozlemci.observe(el); }});
}})();
"""


def all_category_files():
    files = set()
    for g in CATEGORIES:
        files.update(all_files_in_group(g))
    return sorted(files)


def main():
    out = PAGE.format(
        kategori_panel=render_kategori_panel(None),
        duvar=render_duvar(),
        vitrin=render_vitrin(),
    )
    out_path = os.path.join(SITE_ROOT, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"{out_path} yazıldı.")

    dosyalar = ",\n".join(f'  "{f}"' for f in all_category_files())
    js_out = INDEX_JS.format(dosyalar=dosyalar)
    js_path = os.path.join(SITE_ROOT, "index.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_out)
    print(f"{js_path} yazıldı ({len(all_category_files())} dosya).")


if __name__ == "__main__":
    main()
