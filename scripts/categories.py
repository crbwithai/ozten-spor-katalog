"""32 üst kategori ve alt kategori (chip) yapısı.

Kaynak: index.html'deki category-nav-button listesi (cat_num, label, top_file sırası)
+ her üst dosyanın kendi kategori-menu-panel'inden çıkarılan alt kategori linkleri.
Üst dosyanın kendi chip etiketi (ör. futbol.html için "Toplar") o dosyadaki ilk
birkaç ürün adına bakılarak elle belirlendi — kategori-menu-panel bunu içermiyor.
generate_pages.py bu yapıyı kullanarak her dosya için yeni tasarım sayfası üretir.
"""

# (cat_num, label, top_file, description, [(chip_file, chip_label), ...])
# chips listesi BOŞSA: tek sayfalık kategori, alt-kat-serit hiç gösterilmez.
# chips listesi DOLUYSA: ilk eleman top_file'ın kendi etiketidir (chip strip'te de görünür).
CATEGORIES = [
    ("01", "FUTBOL", "futbol.html",
     "Sahadan halı sahaya, her seviyeye uygun toplar, forma ve ekipmanlar.",
     [("futbol.html", "Toplar"), ("futbol-malzemeleri.html", "Futbol Malzemeleri"), ("kaleci-eldivenleri.html", "Kaleci Eldivenleri")]),
    ("02", "BASKETBOL", "basketbol.html",
     "Antrenman ve maç için dayanıklı basketbol topları.",
     [("basketbol.html", "Toplar"), ("basketbol-potalari.html", "Basketbol Potaları")]),
    ("03", "VOLEYBOL", "voleybol.html",
     "Salon ve plaj voleybolu için profesyonel toplar.",
     [("voleybol.html", "Toplar"), ("voleybol-aksesuarlari.html", "Aksesuarlar")]),
    ("04", "BADMINTON", "badminton.html",
     "Hafif ve dayanıklı badminton raketleri.",
     [("badminton.html", "Raketler"), ("badminton-toplari.html", "Badminton Topları"), ("badminton-fileleri.html", "Badminton Fileleri"),
      ("badminton-gripleri.html", "Badminton Gripleri"), ("badminton-kordajlari.html", "Badminton Kordajları"),
      ("badminton-malzemeleri.html", "Badminton Malzemeleri")]),
    ("05", "MASA TENİSİ", "masa-tenisi.html",
     "Kulüp ve ev kullanımına uygun masa tenisi raketleri.",
     [("masa-tenisi.html", "Raketler"), ("masa-tenisi-toplari.html", "Masa Tenisi Topları"), ("masa-tenisi-malzemeleri.html", "Masa Tenisi Malzemeleri")]),
    ("06", "TENİS", "tenis.html",
     "Kort performansını artıran tenis raketleri.",
     [("tenis.html", "Raketler"), ("tenis-toplari.html", "Tenis Topları"), ("tenis-fileleri.html", "Tenis Fileleri"),
      ("tenis-sort-ve-etekleri.html", "Tenis Şort ve Etekleri"),
      ("tenis-overgrip-sac-bandi-bileklikler.html", "Overgrip, Saç Bandı ve Bileklikler"),
      ("tenis-malzemeleri.html", "Tenis Malzemeleri")]),
    ("07", "ATLAMA İPİ", "atlama-ipi.html",
     "Kondisyon ve kardiyo antrenmanları için ayarlanabilir ve hızlı ip modelleri.", []),
    ("08", "EL YAYI", "el-yayi.html",
     "Kavrama gücü ve önkol antrenmanı için farklı direnç seviyelerinde el yayları.", []),
    ("09", "YOGA PİLATES", "yoga-pilates.html",
     "Denge ve esneklik çalışmaları için pilates topları.",
     [("yoga-pilates.html", "Pilates Topları"), ("yoga-mat-pilates-bantlari.html", "Yoga Mat ve Pilates Bantları"), ("yoga-roller.html", "Yoga Roller"),
      ("pilates-cemberleri.html", "Pilates Çemberleri"), ("step-tahtalari.html", "Step Tahtaları"),
      ("yoga-bloklari.html", "Yoga Blokları"), ("yoga-malzemeleri.html", "Yoga Malzemeleri")]),
    ("10", "FITNESS", "fitness.html",
     "Ev ve salon antrenmanları için dambıl çeşitleri.",
     [("fitness.html", "Dambıllar"), ("fitness-aletleri.html", "Fitness Aletleri"), ("barlar-ve-barfiks-ekipmanlari.html", "Barlar ve Barfiks Ekipmanları"),
      ("plaka-ve-plaka-setleri.html", "Plaka ve Plaka Setleri"), ("el-ve-ayak-agirliklari.html", "El ve Ayak Ağırlıkları"),
      ("fitness-eldiven-ve-kemerleri.html", "Fitness Eldiven ve Kemerleri"), ("halatlar.html", "Halatlar"),
      ("agirlik-ve-bulgar-cantalari.html", "Ağırlık ve Bulgar Çantaları"), ("kettlebell.html", "Kettlebell"),
      ("dambil-standlari.html", "Dambıl Standları")]),
    ("11", "EGZERSİZ", "egzersiz.html",
     "Mat, denge topu ve direnç ekipmanlarıyla tam vücut antrenmanı.", []),
    ("12", "HENTBOL", "hentbol.html",
     "Maç ve antrenman standartlarında top ve saha ekipmanları.", []),
    ("13", "YÜZME", "yuzme.html",
     "Yetişkin ve çocuklar için yüzücü gözlükleri.",
     [("yuzme.html", "Gözlükler"), ("boneler.html", "Boneler"), ("sungerler.html", "Süngerler"), ("yuzme-malzemeleri.html", "Yüzme Malzemeleri")]),
    ("14", "BOCCE", "bocce.html",
     "Açık alan ve turnuva kullanımına uygun bocce set ve topları.", []),
    ("15", "HOKEY", "hokey.html",
     "Hokey sopaları ve ekipmanları.",
     [("hokey.html", "Toplar"), ("hokey-sopalari.html", "Hokey Sopaları"), ("hokey-ekipmanlari.html", "Hokey Ekipmanları")]),
    ("16", "KANO", "kano.html",
     "Kano ve kürek sporları için ürünler.", []),
    ("17", "BEYZBOL", "beyzbol.html",
     "Beyzbol sporu için ürünler.", []),
    ("18", "PATEN", "paten.html",
     "Paten çeşitleri.",
     [("paten.html", "Patenler"), ("kaykay.html", "Kaykay"), ("kasklar.html", "Kasklar")]),
    ("19", "ORYANTİRİNG", "oryantiring.html",
     "Oryantiring sporu için ürünler.", []),
    ("20", "PADEL", "padel.html",
     "Padel raket ve ekipmanları.", []),
    ("21", "PICKLEBALL", "pickleball.html",
     "Pickleball raket ve topları.", []),
    ("22", "RAGBİ", "ragbi.html",
     "Ragbi topları ve ekipmanları.", []),
    ("23", "SATRANÇ", "satranc.html",
     "Satranç takımları ve aksesuarları.", []),
    ("24", "SOFTBALL", "softball.html",
     "Softball sporu için ürünler.", []),
    ("25", "SQUASH", "squash.html",
     "Squash raket ve topları.", []),
    ("26", "DART", "dart.html",
     "Dart tahtası ve okları.", []),
    ("27", "ATLETİZM", "atletizm.html",
     "Atletizm sporu için ürünler.",
     [("atletizm.html", "Diğer Ekipmanlar"), ("diskler.html", "Diskler"), ("gulleler.html", "Gülleler"), ("firlatma-toplari.html", "Fırlatma Topları"),
      ("atlama-engelleri.html", "Atlama Engelleri"), ("ciritler.html", "Ciritler"), ("cekicler.html", "Çekiçler"),
      ("stafet.html", "Stafet"), ("cikis-takozu.html", "Çıkış Takozu")]),
    ("28", "CİMNASTİK", "cimnastik.html",
     "Cimnastik ürünleri.",
     [("cimnastik.html", "Minderler"), ("trambolin.html", "Trambolin"), ("cimnastik-malzemeleri.html", "Cimnastik Malzemeleri")]),
    ("29", "SAĞLIK TOPLARI", "saglik-toplari.html",
     "Sağlık topu çeşitleri.", []),
    ("30", "SU TOPU", "su-topu.html",
     "Su topu sporu için ürünler.", []),
    ("31", "OYUN GRUBU", "oyun-grubu.html",
     "Oyun grubu ürünleri.", []),
    ("32", "DÖVÜŞ SPORLARI", "dovus-sporlari.html",
     "Dövüş sporları ekipmanları.", []),
]


def all_files_in_group(group):
    _cat_num, _label, top_file, _desc, chips = group
    files = {top_file}
    files.update(c[0] for c in chips)
    return list(files)


def find_group_for_file(fname):
    """Bir dosyanın ait olduğu grubu ve o dosyanın chip etiketini döndürür (tek sayfalık
    kategorilerde chip yok, bu durumda etiket grup adının kendisidir)."""
    for g in CATEGORIES:
        cat_num, label, top_file, desc, chips = g
        for chip_file, chip_label in chips:
            if fname == chip_file:
                return g, chip_label
        if fname == top_file:
            return g, label
    return None, None
