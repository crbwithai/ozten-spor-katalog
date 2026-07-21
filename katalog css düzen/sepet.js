(function(){
  var ANAHTAR='oztenSepet';

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
        '<div class="sepet-alt"><span id="sepetToplam">0 ürün</span></div>'+
      '</div>';
    document.body.appendChild(sarici);
    document.getElementById('sepetKapat').addEventListener('click', panelKapat);
    document.getElementById('sepetArkaplan').addEventListener('click', panelKapat);
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
    guncelle();
  });
})();
