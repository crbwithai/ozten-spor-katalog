# Özten Spor Katalog — Yenileme Notları

Bu dosya, projede alınan kararları ve sıradaki işleri kaydeder.
Yeni bir oturuma başlarken önce bunu oku.

---

## Projenin durumu

Site Cloudflare Pages üzerinde yayında, GitHub reposuna bağlı.
`main` dalına atılan her commit canlı siteyi günceller.
Çalışmalar `yeni-tasarim` dalında yapılıyor; onaylanmadan main'e birleştirilmiyor.

**Sahibi kod bilmiyor.** Her adımda ne yapıldığı ve neden o yöntemin
seçildiği açıklanmalı. Bir yön belirlendiğinde alternatifleri de sunulmalı.

---

## Temel teşhis

Mevcut CSS bir **basılı katalog** için yazılmış, sonra üstüne web
özellikleri eklenmiş. Kanıtı: `@page { size: A5 }`, mm ve pt cinsinden
ölçüler, 210mm × 297mm sabit sayfa kutuları, elle doldurulmak için
bırakılmış noktalı çizgiler.

Kullanılabilirlik sorunlarının çoğu buradan geliyor.

### Tespit edilen sorunlar

1. **Sayfa ağırlığı.** 922 görselin neredeyse tamamı BMP. Toplam 347 MB.
   Sayfa başına 18–22 MB. Mobilde açılması 30–60 saniye sürüyor.
   WebP'ye çevrilirse tahminen %95 küçülme.

2. **Dört köşede dört yüzen buton.** Yukarı Çık, WhatsApp, Sepet,
   Kategori geçişi. Mobilde ekranın dört köşesi de kapalı.

3. **Sabit gezinme yok.** Kategori menü çubuğu `position: relative`,
   sayfayla kayıp gidiyor. 58 ürünlük sayfada kategori değiştirmek için
   en yukarı dönmek gerekiyor.

4. **Yazı boyutları çok küçük.** Ürün metni 7.5pt ≈ 10px.
   Mobil için önerilen alt sınır 16px.

5. **Başlık tekrarı.** `futbol.html` içinde "FUTBOL 01" başlığı ve alt
   bilgi 10 kez tekrarlanıyor — basılı katalogda her A4 sayfasının kendi
   başlığı olduğu için. Web'de gereksiz.

6. **Kod tekrarı.** `aramaFiltrele` fonksiyonu 81 HTML dosyasının her
   birine ayrı ayrı kopyalanmış. Üst menü ve arama kutusu da öyle.
   Bir düzeltme 81 dosyayı elle değiştirmeyi gerektiriyor.

7. **Fiyatlar iki yerde.** Hem 1084 ürün kartının içine gömülü,
   hem `fiyat_listesi.csv` dosyasında. Biri güncellenince diğeri eskiyor.

8. **index.html'de 3 kırık görsel bağlantısı** var.

9. **Klasör adlarında Türkçe karakter ve boşluk** var
   (`katalog css düzen`, `İmage`). Linux sunucularda kırılma riski.

---

## Öncelik sırası (sahibi belirledi)

1. Tasarım ve görünüm
2. Görsel boyutlarını küçültmek
3. Fiyat güncellemeyi kolaylaştırmak
4. Yeni özellikler

---

## Alınan tasarım kararları

**Yön: karma.** Ana sayfa ve kategori başlıkları enerjik (koyu zemin,
büyük tipografi, marka renkleri); ürün listeleme sakin ve verimli.
Gerekçe: ziyaretçi gösteri için değil fiyat görmek için geliyor,
ama toptancının ciddi görünmesi de gerekiyor.

**Gezinme:**
- Sabit üst çubuk: logo + arama + Kategoriler + Sepet
- Mobilde üst çubuk sadeleşir (logo + arama), gezinme alta iner:
  Ana Sayfa · Ara · Kategoriler · Sepet
- Yüzen butonlardan sadece WhatsApp kalır
- Alt kategoriler: kategori başlığının altında yatay şerit (chip),
  `sticky`, mobilde yana kaydırılır. Eski açılır menü kaldırıldı —
  orada alt kategorilerin varlığı görünmüyordu.

**Tipografi:** Inter. Ürün adı 15px, açıklama 13px, fiyat 19px.
Ölçüler px cinsinden; mm ve pt kullanılmaz.

**Renkler:** kırmızı `#E11D2E`, turuncu `#FD8C22`, siyah `#111111`.
Mevcut marka renkleri korundu, daha ölçülü kullanıldı.

**Kartlar:** kare görsel alanı (`aspect-ratio: 1/1`), `object-fit: contain`.
Farklı boyuttaki fotoğraflar ızgarayı bozmasın diye. Açıklama iki satırda
kesiliyor, kart boyları eşit kalsın diye.

---

## sepet.js ile uyum — ÖNEMLİ

Sepet sistemi ürün bilgisini HTML'den okuyor. Yeni markup yazarken şu üç
şey korunmalı, yoksa sepet bozulur:

- `.product-card` — kart kabı
- Kart içindeki **ilk** `.pf-label` — ürün adı, `Ürün Adı :` ön ekiyle
- `.pf-price .pf-line` — fiyat

Prototipte kullanılan iki numara:

1. `Ürün Adı :` ön eki `<span class="gizli-etiket">` içine alınıp CSS ile
   gizlendi. `textContent` CSS'ten etkilenmediği için sepet metni okumaya
   devam ediyor, kullanıcı görmüyor.

2. `sepet.js` kendi yüzen sepet butonunu üretiyor. O buton CSS ile
   gizlendi; yeni üst/alt çubuk butonları JavaScript ile ona tıklıyor.
   Böylece `sepet.js` hiç değiştirilmedi — indirim kodu (OZTEN5) ve
   WhatsApp sipariş akışı aynen çalışıyor.

---

## Yapılanlar

- [x] `futbol.html` için prototip hazırlandı: `futbol-yeni.html` + `ozten-yeni.css`
- [x] 58 ürün gerçek verisiyle yeni yapıya aktarıldı
- [x] Alt kategori şeridi eklendi (Toplar · Futbol Malzemeleri · Kaleci Eldivenleri)
- [x] İlk şerit düğmesi "Tümü" değil "Toplar" — sayfa sadece toplardan oluşuyor
- [x] Prototip ekran görüntüsüyle incelendi, tasarım onaylandı (kart boyutu, renkler, alt çubuk sorunsuz)
- [x] 915 BMP görsel WebP'ye çevrildi (352MB → 16MB, `İmage/` klasörü), 82 HTML'deki
      `.bmp` referansı `.webp` olarak güncellendi. Eski BMP dosyaları `git rm` ile kaldırıldı.
- [x] index.html'deki 2 kırık görsel linki düzeltildi (yollarda ters slash `\` hatası)
- [x] **Fiyatlar tek kaynağa bağlandı**: `katalog css düzen/fiyatlar.csv` artık tüm
      fiyatların tek kaynağı. `scripts/update_html_from_csv.py` bu dosyayı okuyup
      ilgili HTML sayfalarındaki fiyatı günceller. `.github/workflows/update-prices.yml`
      ile fiyatlar.csv her push'landığında bu işlem otomatik çalışır ve değişen
      HTML sayfalarını kendisi commit'ler — sahibin hiçbir script çalıştırması
      gerekmez, sadece CSV'yi GitHub üzerinden düzenleyip kaydetmesi yeterli.
      (Eski `fiyat_listesi.csv` / `fiyat_listesi_yeni_urunler.csv` dosyaları artık
      kullanılmıyor, referans olarak duruyor — silinebilir.)

### Fiyat nasıl değiştirilir (sahibi için)

1. GitHub'da `katalog css düzen/fiyatlar.csv` dosyasını aç, düzenle (kalem ikonu).
2. İlgili ürünün satırındaki "Fiyat" sütununu değiştir (sadece sayı yazman yeterli,
   ör. `950` — "₺" işaretini ve nokta ayracını script kendisi ekler).
3. Sayfanın altından "Commit changes" ile kaydet.
4. ~1 dakika içinde ilgili kategori sayfasındaki fiyat otomatik güncellenir
   (GitHub Actions çalışır, HTML'i günceller, `main`'e ise Cloudflare otomatik yayınlar).
5. Ürün adını veya dosya adını YANLIŞ yazarsan işlem "başarısız" görünür ve
   o satır güncellenmez — diğer tüm doğru satırlar yine de uygulanır.

- [x] `aramaFiltrele` fonksiyonu (81 dosyaya kopyalanmıştı) geçici olarak tek
      `arama.js` dosyasına taşındı — sonra 80 sayfa yeni tasarıma geçince bu
      dosya da gereksiz kaldı, `site.js` içine taşındı ve silindi (aşağıya bakın).
- [x] **Yeni tasarım kalan 80 sayfaya uygulandı.** `scripts/categories.py`
      (32 üst kategori + alt kategori/chip haritası, index.html'in nav'ından ve
      her sayfanın kendi `kategori-menu-panel`'inden çıkarıldı) +
      `scripts/rollout_lib.py` (eski karttan yeni karta çevirme: açıklama
      parçalarını birleştirme, "sahte sayfalama" bloklarını tek ızgarada
      toplama) + `scripts/generate_pages.py` (tam sayfa üretimi) ile yapıldı.
      Doğrulama: üretilen `futbol.html`, elle onaylanmış `futbol-yeni.html`
      prototipiyle 58 üründe birebir eşleşti (sadece kasıtlı farklar: script
      dışa alındı, başlık büyük harf, kategori paneli 32'ye çıktı). Görsel
      bütünlük (1059 görsel, 0 eksik), fiyat script uyumluluğu (round-trip 0
      sapma) ve 4 farklı sayfada tarayıcı testi (masaüstü+mobil, konsol hatası
      yok) ile teyit edildi. `futbol-yeni.html` (prototip) ve `arama.js`
      artık gereksiz, silindi — ortak JS mantığı `site.js`'e taşındı.
      **Eksik 16 kategori** (Atlama İpi, El Yayı, Bocce, Kano, Beyzbol, Paten,
      Oryantiring, Padel, Pickleball, Ragbi, Softball, Squash, Sağlık Topları,
      Oyun Grubu) kategori paneline eklendi — artık tüm 32 kategori erişilebilir.
      **Bilinen küçük içerik kusuru**: 11/1052 üründe açıklama metni ürün adının
      tekrarıyla başlıyor (ör. "B100 ALTIS Çelik gövde...") — bu eski veride de
      vardı, dokunulmadı (kapsam dışı, çok düşük risk/etki).

## Sıradakiler

- [ ] `index.html` (ana sayfa/vitrin) hâlâ eski şablonda — yeni tasarıma
      geçirilmedi, ayrı bir iş (kendi site-geneli arama mantığı var, dikkatli
      taşınmalı).
- [ ] Henüz hiçbir şey commit edilmedi — sahibi inceleyip onaylayınca commit
      atılacak.

---

## Bilinen ama şimdilik dokunulmayan konular

**Dosya adlandırma tutarsızlığı:** `futbol.html` aslında sadece topları
içeriyor, `futbol-toplari.html` olmalıydı. `futbol.html` de üç alt
kategoriyi listeleyen giriş sayfası olmalıydı. Dosya adı değişirse
Cloudflare'deki mevcut bağlantılar kırılacağı için ertelendi.

**Klasör adları:** `katalog css düzen` ve `İmage` — Türkçe karakter ve
boşluk içeriyor. Değiştirmek tüm görsel yollarını etkiler, ayrı bir iş.
