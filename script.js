(function(){
  "use strict";
  var rust = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.getElementById('jaar').textContent = new Date().getFullYear();

  /* ── kopbalk krijgt een rand zodra je scrollt ── */
  var balk = document.getElementById('balk');
  addEventListener('scroll', function(){
    balk.classList.toggle('vast', scrollY > 12);
  }, {passive:true});

  /* ── menu op telefoon en tablet ──
     Onder 1100px verdwijnt de balknavigatie. Zonder deze lade zijn de
     losse pagina's daar alleen via de voettekst te bereiken. */
  var menuknop = document.getElementById('menuknop');
  var mobiel = document.getElementById('mobielmenu');
  var waas = document.getElementById('mobielwaas');
  if (menuknop && mobiel && waas) {
    var menuOpen = false;
    var zetMenu = function(open){
      menuOpen = open;
      menuknop.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuknop.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
      mobiel.classList.toggle('open', open);
      waas.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
      if (open) mobiel.style.top = balk.getBoundingClientRect().height + 'px';
    };
    menuknop.addEventListener('click', function(){ zetMenu(!menuOpen); });
    waas.addEventListener('click', function(){ zetMenu(false); });
    mobiel.addEventListener('click', function(e){
      if (e.target.closest('a')) zetMenu(false);      // ook bij ankers op dezelfde pagina
    });
    addEventListener('keydown', function(e){
      if (e.key === 'Escape' && menuOpen){ zetMenu(false); menuknop.focus(); }
    });
    addEventListener('resize', function(){
      if (!menuOpen) return;
      if (innerWidth > 1100) zetMenu(false);
      else mobiel.style.top = balk.getBoundingClientRect().height + 'px';
    }, {passive:true});
  }

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
      var kader = null, wacht = false;
      k.addEventListener('pointerenter', function(){ kader = k.getBoundingClientRect(); }, {passive:true});
      k.addEventListener('pointermove', function(ev){
        if (wacht || !kader) return;
        wacht = true;
        requestAnimationFrame(function(){
          k.style.setProperty('--mx', (ev.clientX - kader.left) + 'px');
          k.style.setProperty('--my', (ev.clientY - kader.top) + 'px');
          wacht = false;
        });
      }, {passive:true});
    });
  }

  /* ── de lijst in het paneel loopt door ── */
  var regels = Array.prototype.slice.call(document.querySelectorAll('#stroomlijst .regel'));
  if (!regels.length) {
    /* geen paneel op deze pagina — geen timer starten */
  } else if (rust) {
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
      var hk = null, bezig = false;
      var meetHero = function(){ hk = hero.getBoundingClientRect(); };
      hero.addEventListener('pointerenter', meetHero, {passive:true});
      addEventListener('resize', meetHero, {passive:true});
      hero.addEventListener('pointermove', function(ev){
        if (bezig || !hk) return;
        bezig = true;
        requestAnimationFrame(function(){
          var dx = (ev.clientX - hk.left) / hk.width - .5;
          var dy = (ev.clientY - hk.top) / hk.height - .5;
          paneel.style.transform = 'translate3d(' + (dx * -14).toFixed(1) + 'px,' +
                                   (dy * -10).toFixed(1) + 'px,0)';
          bezig = false;
        });
      }, {passive:true});
      hero.addEventListener('pointerleave', function(){ paneel.style.transform = 'translate3d(0,0,0)'; });
    }
  }

  /* ── contactformulier ──
     Wordt echt verstuurd naar de mailbox, via de endpoint in het
     action-attribuut. Lukt dat niet, dan krijgt de bezoeker het
     e-mailadres én zijn eigen tekst te zien, zodat er niets verloren
     gaat. Zonder JavaScript werkt het formulier ook: dan doet de
     browser een gewone POST naar hetzelfde adres. ── */
  var f = document.getElementById('contactformulier');
  if (f) {
    var knop = document.getElementById('verstuurknop');
    var stand = document.getElementById('formstand');
    var knoptekst = knop ? knop.textContent : '';

    var meld = function(tekst, soort){
      stand.hidden = false;
      stand.className = 'formstand ' + soort;
      stand.textContent = tekst;
    };

    f.addEventListener('submit', function(e){
      e.preventDefault();
      if (!f.reportValidity()) return;

      knop.disabled = true;
      knop.textContent = 'Bezig met versturen\u2026';
      stand.hidden = true;

      var fd = new FormData(f);
      var mislukt = function(){
        var v = function(k){ return (fd.get(k) || '').toString().trim(); };
        var body = ['Naam: ' + v('naam'), 'Bedrijf: ' + (v('bedrijf') || '\u2014'),
                    'E-mail: ' + v('email'), 'Telefoon: ' + (v('telefoon') || '\u2014'),
                    'Onderwerp: ' + v('onderwerp'), '', v('bericht') || ''].join('\n');
        stand.hidden = false;
        stand.className = 'formstand mis';
        stand.innerHTML = 'Het versturen lukte niet. Stuur uw bericht rechtstreeks naar ' +
          '<a href="mailto:glenn@complete-ai.nl?subject=' +
          encodeURIComponent('Aanvraag intake \u2014 ' + (v('bedrijf') || v('naam'))) +
          '&body=' + encodeURIComponent(body) + '">glenn@complete-ai.nl</a> \u2014 ' +
          'uw gegevens staan er dan al in.';
        knop.disabled = false;
        knop.textContent = knoptekst;
      };

      fetch('https://formsubmit.co/ajax/glenn@complete-ai.nl', {
        method: 'POST',
        headers: {'Accept': 'application/json'},
        body: fd
      }).then(function(r){
        return r.ok ? r.json() : Promise.reject(r.status);
      }).then(function(){
        f.reset();
        knop.textContent = knoptekst;
        knop.disabled = false;
        meld('Uw aanvraag is verstuurd. U hoort binnen \u00e9\u00e9n werkdag van ons.', 'goed');
      }).catch(mislukt);
    });
  }

  /* ══ pakketsamensteller ══════════════════════════
     De drie kaarten zijn vertrekpunten; de bezoeker past ze daarna aan.
     Zo is meteen zichtbaar dat een pakket wordt samengesteld en niet
     uit een menu van drie wordt gekozen. */
  var blad = document.getElementById('bladlijst');
  if (blad) {

    var THEMAS = {
      klanten:   {naam:'Klanten & verkoop', punten:[
        'Aanvragen uit alle kanalen in één lijst',
        'Offerte klaargezet binnen één werkdag',
        'Automatische opvolging als een reactie uitblijft']},
      planning:  {naam:'Planning & afspraken', punten:[
        'Klanten plannen zelf in, ook buiten openingstijden',
        'Bevestiging en herinnering vooraf',
        'Één agenda, geen dubbele boekingen']},
      financien: {naam:'Financiën & facturatie', punten:[
        'Factuur automatisch na afronding',
        'Betaalherinneringen zonder ongemakkelijk telefoontje',
        'Bonnen en kosten rechtstreeks de boekhouding in']},
      marketing: {naam:'Marketing & zichtbaarheid', punten:[
        'Website die klanten oplevert, live in 1 tot 2 weken',
        'Google-bedrijfsprofiel volledig ingericht',
        'Lokale SEO voor uw regio',
        'Social media wekelijks bijgehouden in uw huisstijl',
        'Reviews die vanzelf binnenkomen']},
      bereikbaar:{naam:'Bereikbaarheid', punten:[
        'AI-telefonist die opneemt wanneer u niet kunt',
        '24/7 bereikbaar, ook ’s avonds en in het weekend',
        'Terugbelnotities met volledig transcript']},
      personeel: {naam:'Personeel', punten:[
        'Roosters en urenregistratie zonder papierwerk',
        'Verlof- en ziekmeldingen automatisch verwerkt',
        'Instructies en inwerken op één vaste plek']},
      voorraad:  {naam:'Voorraad & inkoop', punten:[
        'Voorraad die zichzelf bijhoudt',
        'Bestelsignaal voordat iets opraakt',
        'Leveranciers en inkooporders op één overzicht']},
      inzicht:   {naam:'Inzicht & rapportage', punten:[
        'Eén dashboard met al uw cijfers',
        'Maandrapport in gewone taal',
        'Zicht op wat een klant kost en oplevert']}
    };
    var VOLGORDE = ['klanten','planning','financien','marketing','bereikbaar','personeel','voorraad','inzicht'];

    /* Per branche wijken enkele bundels af. Dat is waar het concreet wordt:
       "planning" betekent bij een garage iets anders dan bij een restaurant. */
    var BRANCHES = {
      kapsalon: {naam:'kapsalon', lid:'kapsalons', pagina:'ai-voor-kapsalons.html', anders:{
        planning:['Online afspraken, ook op de dagen dat de salon dicht is',
                  'Herinnering de dag ervoor tegen no-shows',
                  'Terugkeerbericht na zes tot acht weken'],
        bereikbaar:['AI-telefonist die opneemt tijdens een behandeling',
                    'Plant de afspraak direct in de agenda',
                    'Schakelt door zodra u het gesprek zelf wilt voeren']}},
      garage: {naam:'garagebedrijf', lid:'garagebedrijven', pagina:'ai-voor-garagebedrijven.html', anders:{
        planning:['APK-herinnering vóór de vervaldatum',
                  'Online een werkplaatsafspraak maken',
                  'Statusbericht zodra de auto klaar staat'],
        bereikbaar:['AI-telefonist voor in de werkplaats',
                    'Schakelt door zodra het technisch wordt',
                    'Terugbelnotities met volledig transcript']}},
      horeca: {naam:'horecazaak', lid:'de horeca', pagina:'ai-voor-de-horeca.html', anders:{
        planning:['Online reserveren binnen uw capaciteit',
                  'Bevestiging en herinnering met annuleerknop',
                  'Vrijgekomen tafels opnieuw te vergeven'],
        bereikbaar:['AI-telefonist die opneemt midden in de service',
                    'Neemt reserveringen en afhaalbestellingen aan',
                    'Bestelling komt als tekst binnen bij de keuken']}},
      bouw: {naam:'bouw- of installatiebedrijf', lid:'bouw en installatie', pagina:'ai-voor-bouw-en-installatie.html', anders:{
        klanten:['Aanvraag volledig vastgelegd terwijl u werkt',
                 'Offerte-concept met uw standaardposten klaar',
                 'Opvolging als de offerte blijft liggen'],
        bereikbaar:['AI-telefonist die spoed herkent en direct doorschakelt',
                    'Alles wat kan wachten wordt vastgelegd',
                    'Bereikbaar vanaf het dak of uit de kruipruimte'],
        personeel:['Urenregistratie per project, vanaf de telefoon',
                   'Uren staan klaar voor de factuur',
                   'Verlof en ziekmeldingen automatisch verwerkt']}},
      webshop: {naam:'webshop', lid:'webshops', anders:{
        klanten:['Orderverwerking van bestelling tot verzending',
                 'Klantvragen automatisch beantwoord',
                 'Retouren zonder handmatige stappen'],
        voorraad:['Voorraad per variant bijgehouden',
                  'Bestelsignaal voordat iets uitverkocht raakt',
                  'Leveranciers en inkooporders op één overzicht']}},
      praktijk: {naam:'praktijk', lid:'praktijken', anders:{
        planning:['Online afspraken met de juiste behandelduur',
                  'Herinnering vooraf, dus minder no-shows',
                  'Eén agenda over alle behandelaars heen']}},
      detailhandel: {naam:'winkel', lid:'de detailhandel', anders:{
        voorraad:['Voorraad in de winkel en online gelijk',
                  'Bestelsignaal per artikel',
                  'Leveranciers en inkooporders op één overzicht']}},
      zzp: {naam:'eenmanszaak', lid:'zzp’ers', anders:{
        financien:['Factuur direct na de klus',
                   'Herinneringen zonder dat u hoeft te bellen',
                   'Bonnen fotograferen, de rest gaat vanzelf']}},
      sportschool: {naam:'sportschool', lid:'sportscholen', anders:{
        planning:['Lesroosters en inschrijvingen online',
                  'Herinnering voor de les',
                  'Wachtlijst die zichzelf doorschuift']}}
    };

    var STARTPUNTEN = {
      fundament: ['marketing'],
      groei:     ['klanten','planning','financien','marketing'],
      volledig:  VOLGORDE.slice()
    };

    var gekozenBranche = null;
    var gekozenThemas  = STARTPUNTEN.groei.slice();

    var kop     = document.getElementById('bladkop');
    var niveau  = document.getElementById('bladniveau');
    var leeg    = document.getElementById('bladleeg');
    var tijd    = document.getElementById('bladtijd').querySelector('span');
    var meer    = document.getElementById('bladmeer');
    var knop    = document.getElementById('bladknop');
    var VINK    = '<svg viewBox="0 0 14 14" aria-hidden="true"><path d="M2 7.5l3 3L12 3.5"/></svg>';

    function punten(thema){
      var b = gekozenBranche && BRANCHES[gekozenBranche];
      if (b && b.anders[thema]) return b.anders[thema];
      return THEMAS[thema].punten;
    }

    function levertijd(){
      var delen = [];
      if (gekozenThemas.indexOf('marketing') > -1) delen.push('website live in 1 tot 2 weken');
      var overig = gekozenThemas.filter(function(t){ return t !== 'marketing' && t !== 'bereikbaar'; });
      if (overig.length) delen.push('automatiseringen binnen enkele werkdagen');
      if (gekozenThemas.indexOf('bereikbaar') > -1) delen.push('AI-telefonist binnen twee weken');
      if (!delen.length) return 'Doorlooptijd hangt af van wat u kiest';
      return delen.join(' · ').replace(/^./, function(c){ return c.toUpperCase(); });
    }

    function teken(){
      var n = gekozenThemas.length;
      var vol = n <= 2 ? 1 : (n <= 5 ? 2 : 3);
      var etiket = vol === 1 ? 'Gericht' : (vol === 2 ? 'Breed' : 'Volledig autonoom');
      niveau.innerHTML = '<em>' + etiket + '</em><span class="staaf">' +
        '<i class="' + (vol > 0 ? 'vol' : '') + '"></i>' +
        '<i class="' + (vol > 1 ? 'vol' : '') + '"></i>' +
        '<i class="' + (vol > 2 ? 'vol' : '') + '"></i></span>';

      var b = gekozenBranche && BRANCHES[gekozenBranche];
      kop.textContent = b ? ('Pakket voor een ' + b.naam) : 'Uw pakket';

      var regels = [];
      VOLGORDE.forEach(function(t){
        if (gekozenThemas.indexOf(t) > -1) regels = regels.concat(punten(t));
      });

      leeg.hidden = regels.length > 0;
      niveau.hidden = regels.length === 0;
      blad.innerHTML = regels.map(function(r, i){
        return '<li style="animation-delay:' + Math.min(i * 22, 420) + 'ms">' + VINK + r + '</li>';
      }).join('');

      tijd.textContent = levertijd();

      if (b && b.pagina){
        meer.hidden = false;
        meer.href = b.pagina;
        meer.textContent = 'Lees wat wij voor ' + b.lid + ' inrichten →';
      } else {
        meer.hidden = true;
      }

      document.querySelectorAll('[data-start]').forEach(function(k){
        var lijst = STARTPUNTEN[k.dataset.start];
        var gelijk = lijst.length === gekozenThemas.length &&
                     lijst.every(function(t){ return gekozenThemas.indexOf(t) > -1; });
        k.classList.toggle('actief', gelijk);
        k.querySelector('.pakknop').setAttribute('aria-pressed', gelijk ? 'true' : 'false');
      });
    }

    document.querySelectorAll('[data-thema]').forEach(function(k){
      k.addEventListener('click', function(){
        var t = k.dataset.thema, i = gekozenThemas.indexOf(t);
        if (i > -1) gekozenThemas.splice(i, 1); else gekozenThemas.push(t);
        k.setAttribute('aria-pressed', i > -1 ? 'false' : 'true');
        teken();
      });
    });

    document.querySelectorAll('[data-branche]').forEach(function(k){
      k.addEventListener('click', function(){
        var b = k.dataset.branche;
        gekozenBranche = (gekozenBranche === b) ? null : b;
        document.querySelectorAll('[data-branche]').forEach(function(a){
          a.setAttribute('aria-pressed', a.dataset.branche === gekozenBranche ? 'true' : 'false');
        });
        teken();
      });
    });

    document.querySelectorAll('[data-start]').forEach(function(k){
      k.addEventListener('click', function(){
        if (gekozenThemas.length === STARTPUNTEN[k.dataset.start].length &&
            k.classList.contains('actief')) return;
        gekozenThemas = STARTPUNTEN[k.dataset.start].slice();
        document.querySelectorAll('[data-thema]').forEach(function(a){
          a.setAttribute('aria-pressed', gekozenThemas.indexOf(a.dataset.thema) > -1 ? 'true' : 'false');
        });
        teken();
        if (innerWidth < 900) {
          document.getElementById('bouwer').scrollIntoView({behavior: rust ? 'auto' : 'smooth', block:'start'});
        }
      });
    });

    /* De samenstelling gaat mee naar het formulier, zodat het gesprek
       niet bij nul begint. Wat de bezoeker zelf typte blijft staan. */
    knop.addEventListener('click', function(){
      var vak = document.querySelector('#contactformulier [name="bericht"]');
      if (!vak || vak.value.trim()) return;
      var namen = VOLGORDE.filter(function(t){ return gekozenThemas.indexOf(t) > -1; })
                          .map(function(t){ return THEMAS[t].naam; });
      if (!namen.length) return;
      var b = gekozenBranche && BRANCHES[gekozenBranche];
      vak.value = 'Graag een voorstel voor: ' + namen.join(', ') + '.' +
                  (b ? ' Mijn bedrijf is een ' + b.naam + '.' : '');
    });

    document.querySelectorAll('[data-thema]').forEach(function(k){
      k.setAttribute('aria-pressed', gekozenThemas.indexOf(k.dataset.thema) > -1 ? 'true' : 'false');
    });
    teken();
  }

  /* ── hero-achtergrond: vijf stromen die samenkomen tot één ──
     Vijf dunne lijnen komen links binnen, buigen naar één punt en
     gaan als één heldere lijn verder naar rechts. Dat is letterlijk
     de belofte van Complete AI, rustig genoeg om niet af te leiden. */
  var doek = document.getElementById('stroomdoek');
  if (!doek || !doek.getContext) return;
  var ctx = doek.getContext('2d', {alpha:true}), B = 0, H = 0, deeltjes = [], loopId = 0,
      zichtbaar = true, gloedCache = null, gloedX = 0, gloedY = 0, vorigeTijd = 0,
      lijnCache = null, lijnX = -1;

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
    if (!lijnCache || lijnX !== k.fx) {
      lijnCache = ctx.createLinearGradient(k.fx, 0, B, 0);
      lijnCache.addColorStop(0, 'rgba(93,140,255,0.62)');
      lijnCache.addColorStop(1, 'rgba(37,216,196,0.04)');
      lijnX = k.fx;
    }
    var g = lijnCache;
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
    if (!zichtbaar) { loopId = 0; return; }   // echt stoppen, niet leeg doortikken
    loopId = requestAnimationFrame(lus);
    if (nu - vorigeTijd < 32) return;         // ~30 beelden per seconde
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
      new IntersectionObserver(function(en){
        zichtbaar = en[0].isIntersecting;
        if (zichtbaar && !loopId) loopId = requestAnimationFrame(lus);
      }, {threshold:0}).observe(doek);
    }
    document.addEventListener('visibilitychange', function(){
      if (document.hidden){ cancelAnimationFrame(loopId); }
      else { cancelAnimationFrame(loopId); loopId = requestAnimationFrame(lus); }
    });
  }
  var wacht;
  addEventListener('resize', function(){
    clearTimeout(wacht);
    wacht = setTimeout(function(){ meet(); bouw(); gloedCache = null; lijnCache = null; lijnX = -1; if (rust) teken(); }, 180);
  }, {passive:true});



})();
