(function(){
  var ANAHTAR='oztenSepet';
  var KISI_ANAHTAR='oztenSecilenKisi';
  var INDIRIM_ANAHTAR='oztenIndirimKodu';
  var WHATSAPP_NUMARA=null;
  var SECILEN_KISI_ADI=null;
  var UYGULANAN_INDIRIM_KODU=null;
  var KISILER=[
    {ad:'SERHAT', gorev:'Satış Sorumlusu', numara:'905522025737'},
    {ad:'FATİH', gorev:'Satış Sorumlusu', numara:'905388985539'},
    {ad:'YAĞIZ', gorev:'Satış Sorumlusu', numara:'905434207118'}
  ];
  // Yeni indirim kodu eklemek için bu listeye satır ekleyin: tip 'yuzde' (%) veya 'tutar' (sabit TL)
  var INDIRIM_KODLARI={
    'OZTEN5': {tip:'yuzde', deger:5}
  };

  function sepetiOku(){ try{ return JSON.parse(localStorage.getItem(ANAHTAR))||[]; }catch(e){ return []; } }
  function sepetiYaz(sepet){ localStorage.setItem(ANAHTAR, JSON.stringify(sepet)); guncelle(); }

  function urunEkle(urun){
    var sepet=sepetiOku();
    var mevcut=sepet.find(function(u){ return u.id===urun.id; });
    if(mevcut){ mevcut.adet++; } else { urun.adet=1; sepet.push(urun); }
    sepetiYaz(sepet);
  }
  function adetDegistir(id, fark){
    var sepet=sepetiOku();
    var u=sepet.find(function(x){ return x.id===id; });
    if(!u) return;
    u.adet+=fark;
    if(u.adet<=0) sepet=sepet.filter(function(x){ return x.id!==id; });
    sepetiYaz(sepet);
  }
  function urunSil(id){ sepetiYaz(sepetiOku().filter(function(x){ return x.id!==id; })); }

  function fiyatAyikla(kart){
    var satir=kart.querySelector('.pf-price .pf-line');
    var metin=satir?satir.textContent.trim():'';
    if(!metin) return null;
    // Türkçe sayı biçimi: "." binlik ayraç, "," ondalık ayraç
    var temiz=metin.replace(/[^\d.,]/g,'').replace(/\./g,'').replace(',','.');
    var sayi=parseFloat(temiz);
    return isNaN(sayi)?null:sayi;
  }

  function kartlariIsle(){
    document.querySelectorAll('.product-card').forEach(function(kart){
      if(kart.querySelector('.sepet-ekle-btn')) return;
      var etiket=kart.querySelector('.pf-label');
      var ad=etiket?etiket.textContent.replace(/^Ürün Adı\s*:?\s*/,'').trim():'';
      if(!ad) return;
      var img=kart.querySelector('img');
      var fiyat=fiyatAyikla(kart);
      var id=location.pathname+'|'+ad;
      var btn=document.createElement('button');
      btn.type='button'; btn.className='sepet-ekle-btn'; btn.textContent='Sepete Ekle';
      btn.addEventListener('click', function(){
        urunEkle({id:id, ad:ad, gorsel:img?img.getAttribute('src'):'', fiyat:fiyat});
      });
      kart.appendChild(btn);
    });
  }

  function panelOlustur(){
    var sarici=document.createElement('div');
    sarici.id='sepetSarici';
    sarici.innerHTML=
      '<div id="sepetArkaplan" class="sepet-arkaplan" hidden></div>'+
      '<div id="sepetPaneli" class="sepet-paneli" hidden>'+
        '<div class="sepet-baslik"><span>Sepetim</span><button id="sepetKapat" class="sepet-kapat" type="button" aria-label="Kapat">&times;</button></div>'+
        '<div id="sepetListe" class="sepet-liste"></div>'+
        '<div class="sepet-alt">'+
          '<div class="sepet-indirim">'+
            '<div class="sepet-indirim-form">'+
              '<input type="text" id="indirimKoduInput" class="sepet-indirim-input" placeholder="İndirim Kodu" autocomplete="off">'+
              '<button type="button" id="indirimUygulaBtn" class="sepet-indirim-btn">Uygula</button>'+
            '</div>'+
            '<div id="indirimMesaj" class="sepet-indirim-mesaj"></div>'+
          '</div>'+
          '<div id="sepetToplam">0 ürün</div>'+
          '<button type="button" id="sepetWhatsapp" class="sepet-whatsapp-btn">'+
            '<svg viewBox="0 0 32 32" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3 9 3 16c0 2.4.6 4.6 1.8 6.6L3 29l6.6-1.7c1.9 1 4 1.6 6.4 1.6 7 0 13-6 13-13S23 3 16 3zm7.6 18.4c-.3.9-1.7 1.7-2.7 1.9-.7.1-1.6.2-4.6-1-3.9-1.6-6.4-5.5-6.6-5.8-.2-.3-1.6-2.1-1.6-4s1-2.8 1.3-3.2c.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1.1 2.6 1.2 2.8.1.2.2.4 0 .7-.1.3-.2.4-.4.6-.2.2-.4.5-.6.7-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.3.2.5.1.7-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2.1 1 2.5 1.2.4.2.6.3.7.5.1.2.1 1-.2 1.9z"/></svg>'+
            'WhatsApp\'tan Sipariş Ver'+
          '</button>'+
        '</div>'+
      '</div>';
    document.body.appendChild(sarici);
    document.getElementById('sepetKapat').addEventListener('click', panelKapat);
    document.getElementById('sepetArkaplan').addEventListener('click', panelKapat);
    document.getElementById('sepetWhatsapp').addEventListener('click', whatsappGonder);
    document.getElementById('indirimUygulaBtn').addEventListener('click', indirimUygula);
    document.getElementById('indirimKoduInput').addEventListener('keydown', function(e){
      if(e.key==='Enter'){ e.preventDefault(); indirimUygula(); }
    });
  }
  function panelAc(){ document.getElementById('sepetPaneli').hidden=false; document.getElementById('sepetArkaplan').hidden=false; }
  function panelKapat(){ document.getElementById('sepetPaneli').hidden=true; document.getElementById('sepetArkaplan').hidden=true; }

  function butonEkle(){
    var sarici=document.createElement('div');
    sarici.className='sepet-buton-sarici';
    var btn=document.createElement('a');
    btn.href='javascript:void(0)'; btn.className='floating-nav-btn sepet-buton';
    btn.innerHTML='Sepetim <span id="sepetSayi" class="sepet-badge">0</span>';
    btn.addEventListener('click', panelAc);
    sarici.appendChild(btn);
    document.body.appendChild(sarici);
  }

  function whatsappMesajiOlustur(){
    var sepet=sepetiOku();
    if(!sepet.length) return null;
    var toplamAdet=0, toplamFiyat=0, fiyatVar=false;
    var satirlar=sepet.map(function(u,i){
      var blok=(i+1)+'. '+u.ad+'\nAdet: '+u.adet;
      toplamAdet+=u.adet;
      if(u.fiyat!=null){
        var araToplam=u.fiyat*u.adet;
        toplamFiyat+=araToplam; fiyatVar=true;
        blok+='\nBirim Fiyat: '+u.fiyat.toLocaleString('tr-TR')+' TL\nAra Toplam: '+araToplam.toLocaleString('tr-TR')+' TL';
      }
      return blok;
    });
    var indirimliToplam=(fiyatVar && UYGULANAN_INDIRIM_KODU)?indirimHesapla(UYGULANAN_INDIRIM_KODU, toplamFiyat):null;
    var toplamMetni;
    if(!fiyatVar){
      toplamMetni='Genel Toplam: '+toplamAdet+' ürün';
    } else if(indirimliToplam!=null && indirimliToplam<toplamFiyat){
      toplamMetni='İndirim Kodu: '+UYGULANAN_INDIRIM_KODU+
        '\nEski Tutar: '+toplamFiyat.toLocaleString('tr-TR')+' TL'+
        '\nTutar: '+indirimliToplam.toLocaleString('tr-TR')+' TL';
    } else {
      toplamMetni='Genel Toplam: '+toplamFiyat.toLocaleString('tr-TR')+' TL';
    }
    var selam=SECILEN_KISI_ADI?('Merhaba '+SECILEN_KISI_ADI+',\n\nAşağıdaki ürünler için sipariş vermek istiyorum:\n\n'):'Merhaba, aşağıdaki ürünler için sipariş vermek istiyorum:\n\n';
    return selam+satirlar.join('\n\n')+'\n\n'+toplamMetni;
  }
  function whatsappGonder(){
    var mesaj=whatsappMesajiOlustur();
    if(!mesaj){ alert('Sepetiniz boş.'); return; }
    if(!WHATSAPP_NUMARA){ alert('Lütfen iletişime geçmek istediğiniz kişiyi seçin.'); return; }
    window.open('https://wa.me/'+WHATSAPP_NUMARA+'?text='+encodeURIComponent(mesaj), '_blank');
  }
  function kisiSec(kisi, btn){
    document.querySelectorAll('.kisi-karti.aktif').forEach(function(b){ b.classList.remove('aktif'); });
    if(btn) btn.classList.add('aktif');
    WHATSAPP_NUMARA=kisi.numara;
    SECILEN_KISI_ADI=kisi.ad;
    try{ localStorage.setItem(KISI_ANAHTAR, kisi.numara); }catch(e){}
  }
  // Kartı seçer (sepet var ise sonraki "WhatsApp'tan Sipariş Ver" bu kişiye gider)
  // VE aynı anda WhatsApp'ı açar: sepet doluysa sepet mesajıyla, boşsa genel bir
  // karşılama mesajıyla. Katalog dijital bir vitrin — asıl sipariş satış
  // temsilcisiyle WhatsApp üzerinden tamamlanıyor, o yüzden tek tıkla ulaşım önemli.
  function kisiSecVeYaz(kisi, btn){
    kisiSec(kisi, btn);
    var sepetMesaji=whatsappMesajiOlustur();
    var mesaj=sepetMesaji || ('Merhaba '+kisi.ad+', Özten Spor kataloğu hakkında bilgi almak istiyorum.');
    window.open('https://wa.me/'+kisi.numara+'?text='+encodeURIComponent(mesaj), '_blank');
  }
  function indirimHesapla(kod, toplamFiyat){
    var tanim=INDIRIM_KODLARI[kod];
    if(!tanim) return null;
    var indirimliToplam=tanim.tip==='yuzde'?(toplamFiyat-toplamFiyat*tanim.deger/100):(toplamFiyat-tanim.deger);
    if(indirimliToplam<0) indirimliToplam=0;
    return indirimliToplam;
  }
  function indirimMesajGoster(metin, basarili){
    var el=document.getElementById('indirimMesaj');
    if(!el) return;
    el.textContent=metin;
    el.className='sepet-indirim-mesaj'+(metin?(basarili?' basarili':' hata'):'');
  }
  function indirimUygula(){
    var girdi=document.getElementById('indirimKoduInput');
    var kod=girdi?girdi.value.trim().toUpperCase():'';
    if(!kod){ indirimMesajGoster('Lütfen bir indirim kodu girin.', false); return; }
    if(!INDIRIM_KODLARI[kod]){
      UYGULANAN_INDIRIM_KODU=null;
      try{ localStorage.removeItem(INDIRIM_ANAHTAR); }catch(e){}
      indirimMesajGoster('Geçersiz indirim kodu.', false);
      guncelle();
      return;
    }
    UYGULANAN_INDIRIM_KODU=kod;
    try{ localStorage.setItem(INDIRIM_ANAHTAR, kod); }catch(e){}
    indirimMesajGoster('İndirim kodu uygulandı: '+kod, true);
    guncelle();
  }
  function indirimSeciminiUygula(){
    var kayitliKod=null;
    try{ kayitliKod=localStorage.getItem(INDIRIM_ANAHTAR); }catch(e){}
    if(kayitliKod && INDIRIM_KODLARI[kayitliKod]){
      UYGULANAN_INDIRIM_KODU=kayitliKod;
      var girdi=document.getElementById('indirimKoduInput');
      if(girdi) girdi.value=kayitliKod;
      indirimMesajGoster('İndirim kodu uygulandı: '+kayitliKod, true);
    }
  }
  function kisiSeciminiUygula(){
    var kayitliNumara=null;
    try{ kayitliNumara=localStorage.getItem(KISI_ANAHTAR); }catch(e){}
    if(!kayitliNumara) return;
    var kisi=KISILER.find(function(k){ return k.numara===kayitliNumara; });
    if(kisi){ WHATSAPP_NUMARA=kisi.numara; SECILEN_KISI_ADI=kisi.ad; }
  }
  function kisiKartlariOlustur(){
    kisiSeciminiUygula();
    var kapsayici=document.getElementById('iletisimKisiler');
    if(!kapsayici) return;
    KISILER.forEach(function(kisi){
      var btn=document.createElement('button');
      btn.type='button'; btn.className='kisi-karti'+(kisi.numara===WHATSAPP_NUMARA?' aktif':'');
      btn.innerHTML='<span class="kisi-karti-metin"><span class="kisi-ad">'+kisi.ad+'</span><span class="kisi-gorev">'+kisi.gorev+'</span></span>'+
        '<span class="kisi-wa"><svg viewBox="0 0 32 32" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3 9 3 16c0 2.4.6 4.6 1.8 6.6L3 29l6.6-1.7c1.9 1 4 1.6 6.4 1.6 7 0 13-6 13-13S23 3 16 3zm7.6 18.4c-.3.9-1.7 1.7-2.7 1.9-.7.1-1.6.2-4.6-1-3.9-1.6-6.4-5.5-6.6-5.8-.2-.3-1.6-2.1-1.6-4s1-2.8 1.3-3.2c.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1.1 2.6 1.2 2.8.1.2.2.4 0 .7-.1.3-.2.4-.4.6-.2.2-.4.5-.6.7-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.3.2.5.1.7-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2.1 1 2.5 1.2.4.2.6.3.7.5.1.2.1 1-.2 1.9z"/></svg>WhatsApp\'tan Yaz</span>';
      btn.addEventListener('click', function(){ kisiSecVeYaz(kisi, btn); });
      kapsayici.appendChild(btn);
    });
  }
  function whatsappButonuEkle(){
    var sarici=document.createElement('div');
    sarici.className='whatsapp-buton-sarici';
    var btn=document.createElement('a');
    btn.href='javascript:void(0)'; btn.className='floating-nav-btn whatsapp-buton';
    btn.innerHTML='<svg viewBox="0 0 32 32" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M16 3C9 3 3 9 3 16c0 2.4.6 4.6 1.8 6.6L3 29l6.6-1.7c1.9 1 4 1.6 6.4 1.6 7 0 13-6 13-13S23 3 16 3zm7.6 18.4c-.3.9-1.7 1.7-2.7 1.9-.7.1-1.6.2-4.6-1-3.9-1.6-6.4-5.5-6.6-5.8-.2-.3-1.6-2.1-1.6-4s1-2.8 1.3-3.2c.3-.3.7-.4 1-.4h.7c.2 0 .5 0 .8.6.3.7 1.1 2.6 1.2 2.8.1.2.2.4 0 .7-.1.3-.2.4-.4.6-.2.2-.4.5-.6.7-.2.2-.4.4-.2.8.2.4 1 1.6 2.1 2.6 1.4 1.3 2.6 1.7 3 1.9.3.2.5.1.7-.1.2-.2.9-1 1.1-1.4.2-.4.5-.3.8-.2.3.1 2.1 1 2.5 1.2.4.2.6.3.7.5.1.2.1 1-.2 1.9z"/></svg><span class="whatsapp-metin">WhatsApp\'tan Sipariş Ver</span>';
    btn.addEventListener('click', whatsappGonder);
    sarici.appendChild(btn);
    document.body.appendChild(sarici);
  }

  function guncelle(){
    var sepet=sepetiOku();
    var toplamAdet=0, toplamFiyat=0, fiyatVar=false;
    var liste=document.getElementById('sepetListe');
    if(liste){
      liste.innerHTML=sepet.length?'':'<p class="sepet-bos">Sepetiniz boş.</p>';
      sepet.forEach(function(u){
        toplamAdet+=u.adet;
        if(u.fiyat!=null){ toplamFiyat+=u.fiyat*u.adet; fiyatVar=true; }
        var satir=document.createElement('div');
        satir.className='sepet-urun';
        satir.innerHTML=
          '<img src="'+(u.gorsel||'')+'" alt="">'+
          '<div class="sepet-urun-bilgi"><span>'+u.ad+'</span>'+
          (u.fiyat!=null?'<b>'+u.fiyat.toLocaleString('tr-TR')+' ₺</b>':'')+'</div>'+
          '<div class="sepet-adet">'+
          '<button type="button" data-id="'+u.id+'" data-fark="-1">−</button>'+
          '<span>'+u.adet+'</span>'+
          '<button type="button" data-id="'+u.id+'" data-fark="1">+</button>'+
          '</div>'+
          '<button type="button" class="sepet-sil" data-id="'+u.id+'">Kaldır</button>';
        liste.appendChild(satir);
      });
      liste.querySelectorAll('[data-fark]').forEach(function(b){
        b.addEventListener('click', function(){ adetDegistir(b.getAttribute('data-id'), parseInt(b.getAttribute('data-fark'),10)); });
      });
      liste.querySelectorAll('.sepet-sil').forEach(function(b){
        b.addEventListener('click', function(){ urunSil(b.getAttribute('data-id')); });
      });
    }
    var sayiEl=document.getElementById('sepetSayi');
    if(sayiEl) sayiEl.textContent=toplamAdet;
    var toplamEl=document.getElementById('sepetToplam');
    if(toplamEl){
      if(!fiyatVar){
        toplamEl.textContent=toplamAdet+' ürün';
      } else {
        var indirimliToplam=UYGULANAN_INDIRIM_KODU?indirimHesapla(UYGULANAN_INDIRIM_KODU, toplamFiyat):null;
        if(indirimliToplam!=null && indirimliToplam<toplamFiyat){
          toplamEl.innerHTML=
            '<span class="sepet-toplam-eski">'+toplamFiyat.toLocaleString('tr-TR')+' ₺</span>'+
            '<span class="sepet-toplam-yeni">'+indirimliToplam.toLocaleString('tr-TR')+' ₺</span>';
        } else {
          toplamEl.textContent=toplamFiyat.toLocaleString('tr-TR')+' ₺';
        }
      }
    }
  }

  function kategoriMenuKur(){
    var butonlar = document.querySelectorAll('.kategori-menu-buton');
    butonlar.forEach(function(btn){
      var panel = btn.nextElementSibling;
      if(!panel || !panel.classList.contains('kategori-menu-panel')) return;
      btn.setAttribute('aria-expanded', 'false');
      btn.addEventListener('click', function(e){
        e.stopPropagation();
        var acik = !panel.hidden;
        document.querySelectorAll('.kategori-menu-panel').forEach(function(p){ p.hidden = true; });
        butonlar.forEach(function(b){ b.setAttribute('aria-expanded', 'false'); });
        panel.hidden = acik;
        btn.setAttribute('aria-expanded', String(!acik));
      });
    });
    document.addEventListener('click', function(){
      document.querySelectorAll('.kategori-menu-panel').forEach(function(p){ p.hidden = true; });
      butonlar.forEach(function(b){ b.setAttribute('aria-expanded', 'false'); });
    });
  }

  document.addEventListener('DOMContentLoaded', function(){
    kartlariIsle();
    panelOlustur();
    indirimSeciminiUygula();
    butonEkle();
    whatsappButonuEkle();
    kisiKartlariOlustur();
    kategoriMenuKur();
    guncelle();
  });
})();
