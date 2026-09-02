/* Ana sayfaya özel: site-geneli arama (tüm kategorileri tarar) + scroll'da belirme.
   site.js'teki aramaFiltrele (tek sayfa içi filtre) ile karışmasın diye ayrı isim
   kullanılıyor: siteGeneliAra. Kategori sayfalarında bu dosya yüklenmez. */

var katalogVerisi = null;

function katalogYukle(cb) {
  if (katalogVerisi) { cb(); return; }
  katalogVerisi = [];
  var linkler = document.querySelectorAll('.kategori-link');
  var kalan = linkler.length;
  linkler.forEach(function (a) {
    fetch(a.getAttribute('href')).then(function (r) { return r.text(); }).then(function (html) {
      var dom = new DOMParser().parseFromString(html, 'text/html');
      dom.querySelectorAll('.product-card').forEach(function (k) {
        var e = k.querySelector('.pf-label');
        var ad = e ? e.textContent.replace(/^Ürün Adı\s*:?\s*/, '').trim() : '';
        var img = k.querySelector('img');
        if (ad) katalogVerisi.push({ ad: ad, gorsel: img ? img.getAttribute('src') : '', href: a.getAttribute('href') });
      });
    }).catch(function () {}).then(function () { if (--kalan === 0) cb(); });
  });
}

function siteGeneliAra(inp) {
  var q = inp.value.toLocaleLowerCase('tr-TR').trim();
  var kutu = document.getElementById('aramaSonuclari');
  if (!q) { kutu.innerHTML = ''; document.querySelector('.urun-bulunamadi').hidden = true; return; }
  katalogYukle(function () {
    var sonuc = katalogVerisi.filter(function (u) { return u.ad.toLocaleLowerCase('tr-TR').indexOf(q) !== -1; });
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
