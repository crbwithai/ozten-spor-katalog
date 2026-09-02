function aramaFiltrele(inp){
  var q=inp.value.toLocaleLowerCase('tr-TR').trim(), gorunen=0;
  document.querySelectorAll('.product-card').forEach(function(k){
    var e=k.querySelector('.pf-label');
    var esles=(e?e.textContent.toLocaleLowerCase('tr-TR'):'').indexOf(q)!==-1;
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
