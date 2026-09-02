/* Ana sayfaya özel: site-geneli arama (TÜM kategori/alt kategori sayfalarını
   tarar) + scroll'da belirme. site.js'teki aramaFiltrele (tek sayfa içi filtre)
   ile karışmasın diye ayrı isim kullanılıyor: siteGeneliAra. Kategori
   sayfalarında bu dosya yüklenmez.

   TUM_KATEGORI_DOSYALARI bu dosyanın kendisi gibi scripts/generate_index.py
   tarafından scripts/categories.py'den otomatik üretilir — elle düzenlemeyin,
   yeni kategori/alt kategori eklenince scripts/generate_index.py yeniden
   çalıştırılmalı. */
var TUM_KATEGORI_DOSYALARI = [
  "agirlik-ve-bulgar-cantalari.html",
  "atlama-engelleri.html",
  "atlama-ipi.html",
  "atletizm.html",
  "badminton-fileleri.html",
  "badminton-gripleri.html",
  "badminton-kordajlari.html",
  "badminton-malzemeleri.html",
  "badminton-toplari.html",
  "badminton.html",
  "barlar-ve-barfiks-ekipmanlari.html",
  "basketbol-potalari.html",
  "basketbol.html",
  "beyzbol.html",
  "bocce.html",
  "boneler.html",
  "cekicler.html",
  "cikis-takozu.html",
  "cimnastik-malzemeleri.html",
  "cimnastik.html",
  "ciritler.html",
  "dambil-standlari.html",
  "dart.html",
  "diskler.html",
  "dovus-sporlari.html",
  "egzersiz.html",
  "el-ve-ayak-agirliklari.html",
  "el-yayi.html",
  "firlatma-toplari.html",
  "fitness-aletleri.html",
  "fitness-eldiven-ve-kemerleri.html",
  "fitness.html",
  "futbol-malzemeleri.html",
  "futbol.html",
  "gulleler.html",
  "halatlar.html",
  "hentbol.html",
  "hokey-ekipmanlari.html",
  "hokey-sopalari.html",
  "hokey.html",
  "kaleci-eldivenleri.html",
  "kano.html",
  "kasklar.html",
  "kaykay.html",
  "kettlebell.html",
  "masa-tenisi-malzemeleri.html",
  "masa-tenisi-toplari.html",
  "masa-tenisi.html",
  "oryantiring.html",
  "oyun-grubu.html",
  "padel.html",
  "paten.html",
  "pickleball.html",
  "pilates-cemberleri.html",
  "plaka-ve-plaka-setleri.html",
  "ragbi.html",
  "saglik-toplari.html",
  "satranc.html",
  "softball.html",
  "squash.html",
  "stafet.html",
  "step-tahtalari.html",
  "su-topu.html",
  "sungerler.html",
  "tenis-fileleri.html",
  "tenis-malzemeleri.html",
  "tenis-overgrip-sac-bandi-bileklikler.html",
  "tenis-sort-ve-etekleri.html",
  "tenis-toplari.html",
  "tenis.html",
  "trambolin.html",
  "voleybol-aksesuarlari.html",
  "voleybol.html",
  "yoga-bloklari.html",
  "yoga-malzemeleri.html",
  "yoga-mat-pilates-bantlari.html",
  "yoga-pilates.html",
  "yoga-roller.html",
  "yuzme-malzemeleri.html",
  "yuzme.html"
];

var katalogVerisi = null;

function katalogYukle(cb) {
  if (katalogVerisi) { cb(); return; }
  katalogVerisi = [];
  var kalan = TUM_KATEGORI_DOSYALARI.length;
  TUM_KATEGORI_DOSYALARI.forEach(function (href) {
    fetch(href).then(function (r) { return r.text(); }).then(function (html) {
      var dom = new DOMParser().parseFromString(html, 'text/html');
      dom.querySelectorAll('.product-card').forEach(function (k) {
        var e = k.querySelector('.pf-label');
        var ad = e ? e.textContent.replace(/^Ürün Adı\s*:?\s*/, '').trim() : '';
        var img = k.querySelector('img');
        if (ad) katalogVerisi.push({ ad: ad, gorsel: img ? img.getAttribute('src') : '', href: href });
      });
    }).catch(function () {}).then(function () { if (--kalan === 0) cb(); });
  });
}

function siteGeneliAra(inp) {
  var q = inp.value.trim();
  var kutu = document.getElementById('aramaSonuclari');
  if (!q) { kutu.innerHTML = ''; document.querySelector('.urun-bulunamadi').hidden = true; return; }
  katalogYukle(function () {
    // aramaSkoru (site.js) yazım hatalarını tolere eder, kelime sırasını önemsemez.
    // En iyi eşleşme en üstte olacak şekilde sıralanır.
    var sonuc = katalogVerisi
      .map(function (u) { return { u: u, skor: aramaSkoru(u.ad, q) }; })
      .filter(function (x) { return x.skor > 0; })
      .sort(function (a, b) { return b.skor - a.skor; })
      .slice(0, 40)
      .map(function (x) { return x.u; });
    kutu.innerHTML = sonuc.map(function (u) {
      return '<a class="arama-sonuc-item" href="' + u.href + '"><img src="' + u.gorsel + '" alt=""><span>' + u.ad + '</span></a>';
    }).join('');
    document.querySelector('.urun-bulunamadi').hidden = sonuc.length > 0;
  });
}

(function () {
  var elemanlar = document.querySelectorAll('.oz-belir');
  if (!elemanlar.length) return;
  if (!('IntersectionObserver' in window)) {
    elemanlar.forEach(function (el) { el.classList.add('gorunur'); });
    return;
  }
  var gozlemci = new IntersectionObserver(function (girenler) {
    girenler.forEach(function (giren) {
      if (giren.isIntersecting) {
        giren.target.classList.add('gorunur');
        gozlemci.unobserve(giren.target);
      }
    });
  }, { threshold: 0.15 });
  elemanlar.forEach(function (el) { gozlemci.observe(el); });
})();
