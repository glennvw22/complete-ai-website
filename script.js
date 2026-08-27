(function(){
  "use strict";
  var rust = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.getElementById('jaar').textContent = new Date().getFullYear();

  /* ── kopbalk krijgt een rand zodra je scrollt ── */
  var balk = document.getElementById('balk');
  addEventListener('scroll', function(){
    balk.classList.toggle('vast', scrollY > 12);
  }, {passive:true});

  /* ── onthullen bij scrollen ── */
  var items = document.querySelectorAll('.reveal');
  if (rust || !('IntersectionObserver' in window)) {
    items.forEach(function(e){ e.classList.add('in'); });
  } else {
    var obs = new IntersectionObserver(function(en){
      en.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('in'); obs.unobserve(e.target); }
      });
    }, {rootMargin:'0px 0px -10% 0px', threshold:.06});
    items.forEach(function(e){ obs.observe(e); });
  }

  /* ── gloed volgt de muis over de dienstenkaarten ── */
  if (!rust && matchMedia('(hover:hover)').matches) {
    document.querySelectorAll('.dienst').forEach(function(k){
      k.addEventListener('pointermove', function(ev){
        var b = k.getBoundingClientRect();
        k.style.setProperty('--mx', (ev.clientX - b.left) + 'px');
        k.style.setProperty('--my', (ev.clientY - b.top) + 'px');
      });
    });
  }

  /* ── de lijst in het paneel loopt door ── */
  var regels = Array.prototype.slice.call(document.querySelectorAll('#stroomlijst .regel'));
  if (rust) {
    regels.forEach(function(r){ r.classList.add('aan'); });
  } else {
    var i = 0, timer = null;
    function tik(){
      if (i < regels.length){ regels[i].classList.add('aan'); i++; timer = setTimeout(tik, 640); }
      else {
        timer = setTimeout(function(){
          regels.forEach(function(r){ r.classList.remove('aan'); });
          i = 0; timer = setTimeout(tik, 720);
        }, 4400);
      }
    }
    timer = setTimeout(tik, 800);
    document.addEventListener('visibilitychange', function(){
      if (document.hidden){ clearTimeout(timer); }
      else { clearTimeout(timer); timer = setTimeout(tik, 400); }
    });
  }

  /* ── het paneel beweegt subtiel mee met de muis ── */
  if (!rust && matchMedia('(hover:hover)').matches){
    var paneel = document.querySelector('.paneel'), hero = document.querySelector('.hero');
    if (paneel && hero){
      paneel.style.transition = 'transform .5s cubic-bezier(.2,.8,.2,1)';
      hero.addEventListener('pointermove', function(ev){
        var b = hero.getBoundingClientRect();
        var dx = (ev.clientX - b.left) / b.width - .5;
        var dy = (ev.clientY - b.top) / b.height - .5;
        paneel.style.transform = 'translate3d(' + (dx * -14).toFixed(1) + 'px,' +
                                 (dy * -10).toFixed(1) + 'px,0)';
      });
      hero.addEventListener('pointerleave', function(){ paneel.style.transform = 'translate3d(0,0,0)'; });
    }
  }

  /* ── contactformulier: stelt een e-mail op in het mailprogramma van
       de bezoeker. Geen backend, geen derde partij.
       LATER: vervang door een echte endpoint (Formspree/Web3Forms). ── */
  var f = document.getElementById('contactformulier');
  if (f) f.addEventListener('submit', function(e){
    e.preventDefault();
    if (!f.reportValidity()) return;
    var fd = new FormData(f), v = function(k){ return (fd.get(k) || '').toString().trim(); };
    var body = ['Naam: ' + v('naam'), 'Bedrijf: ' + (v('bedrijf') || '—'),
      'E-mail: ' + v('email'), 'Telefoon: ' + (v('telefoon') || '—'),
      'Onderwerp: ' + v('onderwerp'), '', v('bericht') || '(geen toelichting)'].join('\n');
    location.href = 'mailto:glenn@complete-ai.nl?subject=' +
      encodeURIComponent('Aanvraag nulmeting — ' + (v('bedrijf') || v('naam'))) +
      '&body=' + encodeURIComponent(body);
  });
  /* ── hero-achtergrond: vijf stromen die samenkomen tot één ──
     Vijf dunne lijnen komen links binnen, buigen naar één punt en
     gaan als één heldere lijn verder naar rechts. Dat is letterlijk
     de belofte van Complete AI, rustig genoeg om niet af te leiden. */
  var doek = document.getElementById('stroomdoek');
  if (!doek || !doek.getContext) return;
  var ctx = doek.getContext('2d', {alpha:true}), B = 0, H = 0, deeltjes = [], loopId = 0,
      zichtbaar = true, gloedCache = null, gloedX = 0, gloedY = 0, vorigeTijd = 0;

  function meet(){
    var r = doek.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    B = Math.max(r.width, 1); H = Math.max(r.height, 1);
    doek.width = Math.round(B * dpr); doek.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function knoop(){ return { fx: B * 0.52, fy: H * 0.52 }; }
  function pad(i){
    var k = knoop(), y0 = H * (0.20 + (i / 4) * 0.60);
    return { x0: -B * 0.06, y0: y0, cx: B * 0.30, cy: y0, x1: k.fx, y1: k.fy };
  }
  function punt(p, t){
    var u = 1 - t;
    return { x: u*u*p.x0 + 2*u*t*p.cx + t*t*p.x1, y: u*u*p.y0 + 2*u*t*p.cy + t*t*p.y1 };
  }
  function samen(t){
    var k = knoop();
    return { x: k.fx + (B * 1.10 - k.fx) * t, y: k.fy - Math.sin(t * Math.PI) * H * 0.045 };
  }
  function bouw(){
    deeltjes = [];
    for (var i = 0; i < 5; i++){
      for (var j = 0; j < 3; j++){
        deeltjes.push({ lijn: i, f: (j / 3) + i * 0.06, snelheid: 0.0018 + (i % 3) * 0.0002 });
      }
    }
  }
  function teken(){
    ctx.clearRect(0, 0, B, H);
    var i, t, s;

    for (i = 0; i < 5; i++){
      var p = pad(i);
      ctx.beginPath();
      ctx.moveTo(p.x0, p.y0);
      ctx.quadraticCurveTo(p.cx, p.cy, p.x1, p.y1);
      ctx.strokeStyle = 'rgba(61,109,255,0.19)';
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    var k = knoop();
    var g = ctx.createLinearGradient(k.fx, 0, B, 0);
    g.addColorStop(0, 'rgba(93,140,255,0.62)');
    g.addColorStop(1, 'rgba(37,216,196,0.04)');
    ctx.beginPath();
    var s0 = samen(0); ctx.moveTo(s0.x, s0.y);
    for (t = 0.02; t <= 1.0001; t += 0.02){ s = samen(t); ctx.lineTo(s.x, s.y); }
    ctx.strokeStyle = g; ctx.lineWidth = 2; ctx.stroke();

    if (!gloedCache || gloedX !== k.fx || gloedY !== k.fy){
      gloedCache = ctx.createRadialGradient(k.fx, k.fy, 0, k.fx, k.fy, 46);
      gloedCache.addColorStop(0, 'rgba(37,216,196,0.28)');
      gloedCache.addColorStop(1, 'rgba(37,216,196,0)');
      gloedX = k.fx; gloedY = k.fy;
    }
    ctx.beginPath(); ctx.arc(k.fx, k.fy, 46, 0, Math.PI * 2); ctx.fillStyle = gloedCache; ctx.fill();
    ctx.beginPath(); ctx.arc(k.fx, k.fy, 2.6, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(37,216,196,0.85)'; ctx.fill();

    for (var d = 0; d < deeltjes.length; d++){
      var q = deeltjes[d];
      q.f += q.snelheid;
      if (q.f >= 2) q.f -= 2;
      var pos, helder;
      if (q.f < 1){ pos = punt(pad(q.lijn), q.f); helder = 0.30 + q.f * 0.45; }
      else { pos = samen(q.f - 1); helder = 0.75 * (1 - (q.f - 1) * 0.85); }
      if (helder <= 0.02) continue;
      var straal = q.f < 1 ? 1.5 : 2.3;
      ctx.globalAlpha = helder * 0.22;
      ctx.beginPath(); ctx.arc(pos.x, pos.y, straal * 3.4, 0, Math.PI * 2);
      ctx.fillStyle = '#78B4FF'; ctx.fill();
      ctx.globalAlpha = Math.min(helder + 0.2, 1);
      ctx.beginPath(); ctx.arc(pos.x, pos.y, straal, 0, Math.PI * 2);
      ctx.fillStyle = '#C8E1FF'; ctx.fill();
      ctx.globalAlpha = 1;
    }
  }
  function lus(nu){
    loopId = requestAnimationFrame(lus);
    if (!zichtbaar) return;
    if (nu - vorigeTijd < 32) return;   // ~30 beelden per seconde
    vorigeTijd = nu;
    teken();
  }

  // op smalle schermen geen canvas — daar telt elke milliseconde
  if (innerWidth < 700){ doek.style.display = 'none'; return; }

  meet(); bouw();
  if (rust){ teken(); }
  else {
    lus();
    if ('IntersectionObserver' in window){
      new IntersectionObserver(function(en){ zichtbaar = en[0].isIntersecting; }, {threshold:0}).observe(doek);
    }
    document.addEventListener('visibilitychange', function(){
      if (document.hidden){ cancelAnimationFrame(loopId); }
      else { cancelAnimationFrame(loopId); loopId = requestAnimationFrame(lus); }
    });
  }
  var wacht;
  addEventListener('resize', function(){
    clearTimeout(wacht);
    wacht = setTimeout(function(){ meet(); bouw(); if (rust) teken(); }, 180);
  }, {passive:true});

})();
