(function(){
  var ANAHTAR='oztenSepet';
  var KISI_ANAHTAR='oztenSecilenKisi';
  var WHATSAPP_NUMARA=null;
  var SECILEN_KISI_ADI=null;
  var KISILER=[
    {ad:'SERHAT', gorev:'Satış Sorumlusu', numara:'905522025737'},
    {ad:'FATİH', gorev:'Satış Sorumlusu', numara:'905388985539'},
    {ad:'POYRAZ', gorev:'Satış Sorumlusu', numara:'905550380752'},
    {ad:'YAĞIZ', gorev:'Satış Sorumlusu', numara:'905434207118'}
  ];

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
    var sayi=parseFloat(metin.replace(/[^\d.,]/g,'').replace(',','.'));
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
          '<span id="sepetToplam">0 ürün</span>'+
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
    var genelToplam=fiyatVar?(toplamFiyat.toLocaleString('tr-TR')+' TL'):(toplamAdet+' ürün');
    var selam=SECILEN_KISI_ADI?('Merhaba '+SECILEN_KISI_ADI+',\n\nAşağıdaki ürünler için sipariş vermek istiyorum:\n\n'):'Merhaba, aşağıdaki ürünler için sipariş vermek istiyorum:\n\n';
    return selam+satirlar.join('\n\n')+'\n\nGenel Toplam: '+genelToplam;
  }
  function whatsappGonder(){
    var mesaj=whatsappMesajiOlustur();
    if(!mesaj){ alert('Sepetiniz boş.'); return; }
    if(!WHATSAPP_NUMARA){ alert('Lütfen iletişime geçmek istediğiniz kişiyi seçin.'); return; }
    window.open('https://wa.me/'+WHATSAPP_NUMARA+'?text='+encodeURIComponent(mesaj), '_blank');
  }
  function kisiSec(kisi, btn){
    document.querySelectorAll('.kisi-karti.aktif').forEach(function(b){ b.classList.remove('aktif'); });
    btn.classList.add('aktif');
    WHATSAPP_NUMARA=kisi.numara;
    SECILEN_KISI_ADI=kisi.ad;
    try{ localStorage.setItem(KISI_ANAHTAR, kisi.numara); }catch(e){}
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
      btn.innerHTML='<span class="kisi-ad">'+kisi.ad+'</span><span class="kisi-gorev">'+kisi.gorev+'</span><span class="kisi-tel">'+kisi.numara+'</span>';
      btn.addEventListener('click', function(){ kisiSec(kisi, btn); });
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
    if(toplamEl) toplamEl.textContent=fiyatVar?(toplamFiyat.toLocaleString('tr-TR')+' ₺'):(toplamAdet+' ürün');
  }

  document.addEventListener('DOMContentLoaded', function(){
    kartlariIsle();
    panelOlustur();
    butonEkle();
    whatsappButonuEkle();
    kisiKartlariOlustur();
    guncelle();
  });
})();
