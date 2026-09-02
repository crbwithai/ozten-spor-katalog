/* Bulanık arama: kelime sırası önemli değil, küçük yazım hataları tolere
   edilir (ör. "futbal" -> "futbol" eşleşir). aramaFiltrele (bu dosyada,
   sayfa içi filtre) ve siteGeneliAra (index.js, tüm kataloğu tarar) bu
   paylaşılan skor fonksiyonunu kullanır — mantık iki yerde ayrı ayrı
   yazılmasın diye. */
function metniSadelestir(s){ return (s||'').toLocaleLowerCase('tr-TR').trim(); }

function duzenlemeMesafesi(a,b){
  var m=a.length, n=b.length;
  if(m===0) return n;
  if(n===0) return m;
  var onceki=[], simdi=[];
  for(var j=0;j<=n;j++) onceki[j]=j;
  for(var i=1;i<=m;i++){
    simdi[0]=i;
    for(j=1;j<=n;j++){
      var maliyet=a[i-1]===b[j-1]?0:1;
      simdi[j]=Math.min(onceki[j]+1, simdi[j-1]+1, onceki[j-1]+maliyet);
    }
    onceki=simdi.slice();
  }
  return onceki[n];
}

function kelimeEslesiyorMu(arananKelime, hedefKelime){
  if(hedefKelime.indexOf(arananKelime)!==-1) return true;
  var esik=arananKelime.length<=3?1:(arananKelime.length<=6?2:3);
  var parcaUzunluk=Math.min(hedefKelime.length, arananKelime.length+esik);
  return duzenlemeMesafesi(arananKelime, hedefKelime.slice(0,parcaUzunluk))<=esik;
}

// Ürün adının arama sorgusuyla ne kadar iyi eşleştiğini döndürür (0 = eşleşmiyor).
// Sorgudaki HER kelime ürün adında (herhangi bir sırada) karşılık bulmalı.
function aramaSkoru(urunAdi, sorgu){
  var sorguKelimeleri=metniSadelestir(sorgu).split(/\s+/).filter(Boolean);
  if(!sorguKelimeleri.length) return 0;
  var urunKelimeleri=metniSadelestir(urunAdi).split(/\s+/).filter(Boolean);
  var toplam=0;
  for(var i=0;i<sorguKelimeleri.length;i++){
    var enIyi=0;
    for(var j=0;j<urunKelimeleri.length;j++){
      if(kelimeEslesiyorMu(sorguKelimeleri[i], urunKelimeleri[j])){
        var skor=urunKelimeleri[j].indexOf(sorguKelimeleri[i])===0?2:1;
        if(skor>enIyi) enIyi=skor;
      }
    }
    if(enIyi===0) return 0;
    toplam+=enIyi;
  }
  return toplam;
}

function aramaFiltrele(inp){
  var q=inp.value.trim(), gorunen=0;
  document.querySelectorAll('.product-card').forEach(function(k){
    var e=k.querySelector('.pf-label');
    var esles=!q || aramaSkoru(e?e.textContent:'', q)>0;
    k.style.display=esles?'':'none';
    if(esles)gorunen++;
  });
  document.querySelector('.urun-bulunamadi').hidden=!(q&&gorunen===0);
}

(function(){
  var panel=document.getElementById('kategoriPanel');
  function panelDegistir(){ panel.hidden=!panel.hidden; }
  document.getElementById('kategoriAc').addEventListener('click', panelDegistir);
  document.getElementById('altKategori').addEventListener('click', panelDegistir);

  document.getElementById('altAra').addEventListener('click', function(){
    window.scrollTo({top:0,behavior:'smooth'});
    document.getElementById('aramaKutusu').focus();
  });

  // sepet.js kendi yüzen butonunu üretiyor; CSS ile gizledik.
  // Bizim butonlarımız o butona tıklayarak paneli açar — sepet.js değişmedi.
  function sepetiAc(){
    var eski=document.querySelector('.sepet-buton-sarici .sepet-buton');
    if(eski) eski.click();
  }
  document.getElementById('sepetAc').addEventListener('click', sepetiAc);
  document.getElementById('altSepet').addEventListener('click', sepetiAc);

  // sepet.js'in gizli rozetini izleyip kendi rozetlerimize yansıtıyoruz
  function rozetleriEsitle(){
    var kaynak=document.getElementById('sepetSayi');
    if(!kaynak) return;
    var sayi=kaynak.textContent.trim();
    document.getElementById('ustSepetSayi').textContent=sayi;
    var alt=document.getElementById('altSepetSayi');
    alt.textContent=sayi;
    alt.hidden=(sayi==='0'||sayi==='');
  }
  setInterval(rozetleriEsitle, 400);
  rozetleriEsitle();
})();
