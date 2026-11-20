/* De tijdverlies-scan van Complete AI.
   Zeven stappen, uitslag direct op het scherm. Alles wordt in de browser
   berekend. Antwoorden verlaten het apparaat pas als de bezoeker zelf op
   "Bespreek mijn uitslag" drukt. Geen cookies, geen meting.

   Rekenmodel (zichtbaar in de uitslag, zodat niets verborgen zit):
   1. Bij elk van de vijf onderdelen kiest de bezoeker hoe het nu gaat en
      hoeveel uur per week het kost. Wij rekenen met het midden van de gekozen
      klasse. De uren die in de uitslag staan zijn dus de uren die de bezoeker
      zelf noemde, niet door ons verdeeld.
   2. Hoe handmatiger het antwoord, hoe lager het cijfer "hoe goed geregeld".
   3. Hoeveel de bezoeker uit handen wil geven bepaalt een schuif. Wij noemen
      geen percentage en beloven er geen.
   4. Het voorwerk per nieuwe klus (aanvraag, offerte, planning, materiaal) is
      ook een klasse. Het rekenvoorbeeld "meer klussen" vermenigvuldigt dat met
      een aantal dat de bezoeker zelf instelt. */
(function(){
  "use strict";

  var app = document.getElementById('scan-app');
  var intro = document.getElementById('scan-intro');
  if (!app || !intro) return;
  var TITEL = document.title;

  var GEBIED = {
    offerte:     {naam:'Offertes en calculaties',
                  stap:'Zet uw tien meest voorkomende klussen op een rij, met materiaal en uren. Dat is meteen de basis voor een offerte die zichzelf klaarzet.',
                  wij:'De assistent leest de aanvraag uit, rekent met uw eigen prijzen en zet een conceptofferte klaar. U kijkt na en verstuurt.',
                  link:'oplossingen.html#offertes', linktekst:'Bekijk de oplossing voor offertes'},
    admin:       {naam:'Administratie',
                  stap:'Laat uw monteurs elke werkbon afsluiten met uren, materiaal en een foto. Dan hoeft er op kantoor niets meer nagebeld te worden.',
                  wij:'Werkbonnen en uren komen rechtstreeks uit het werk. Daar maakt de app een conceptfactuur van, met controle op de wettelijke regels.',
                  link:'oplossingen.html#administratie', linktekst:'Bekijk de oplossing voor administratie'},
    planning:    {naam:'Planning en werkvoorbereiding',
                  stap:'Zet de planning in één gedeelde agenda in plaats van losse appgroepen, en loop elke vrijdag een kwartier de volgende week door.',
                  wij:'Eén overzicht met klussen, agenda en materiaal. Na het tekenen kiest de klant zelf een vrij moment uit uw agenda.',
                  link:'oplossingen.html#planning', linktekst:'Bekijk de oplossing voor planning'},
    klantcontact:{naam:'Klantcontact',
                  stap:'Schrijf de vijf antwoorden die u het vaakst typt één keer uit. Die kunt u daarna laten klaarzetten door een assistent.',
                  wij:'Alles van één klant op één tijdlijn, en conceptantwoorden voor de vragen die steeds terugkomen. U leest mee en verstuurt.',
                  link:'oplossingen.html#klantcontact', linktekst:'Bekijk de oplossing voor klantcontact'},
    telefoon:    {naam:'Telefoon en opvolging',
                  stap:'Noteer een week lang hoeveel oproepen u mist en wie het waren. Dat getal laat zien of een telefonist zich terugbetaalt. De rekentool helpt daarbij.',
                  wij:'Een AI-telefonist die opneemt wanneer u dat niet kunt, de aanvraag vastlegt en een afspraak inplant. Elk gesprek is terug te lezen.',
                  link:'ai-telefonist.html', linktekst:'Bekijk de AI-telefonist'}
  };
  var SLEUTELS = ['offerte','admin','planning','klantcontact','telefoon'];
  var AANTAL_GEBIEDEN = SLEUTELS.length;

  /* Uren per onderdeel: vijf klassen, gerekend met het midden. */
  var UREN_KLASSEN = ['Minder dan 2 uur', '2 tot 5 uur', '5 tot 10 uur', '10 tot 20 uur', 'Meer dan 20 uur'];
  var UREN_MIDDEN = [1, 3.5, 7.5, 15, 25];

  var VRAGEN = [
    {label:'Offertes en calculaties', q:'Hoe komt bij u een offerte tot stand?',
      opts:[
        'Elke keer vanaf nul, in Excel of Word',
        'Met een sjabloon of prijslijst, maar veel handwerk per aanvraag',
        'In een programma, maar opnemen en rekenen kost nog veel tijd',
        'Grotendeels automatisch, ik controleer alleen'],
      urenq:'Hoeveel uur per week kost het maken van offertes en calculaties?'},
    {label:'Administratie', q:'Hoe komen werkbonnen, uren en facturen in uw administratie?',
      opts:[
        'Alles wordt met de hand overgetikt',
        'Monteurs appen een foto of schrijven het op, iemand op kantoor tikt het over',
        'Deels automatisch, maar met veel controleren en nabellen',
        'Het komt vanzelf goed in het systeem'],
      urenq:'Hoeveel uur per week kost de administratie rond werkbonnen, uren en facturen?'},
    {label:'Planning en werkvoorbereiding', q:'Hoe regelt u de planning en wat er bij een klus klaar moet liggen?',
      opts:[
        'Ik houd het vooral zelf bij, zonder vast overzicht',
        'Excel of een gedeelde agenda, met veel appjes voor wijzigingen',
        'Een planningsprogramma, maar wijzigingen en materiaal geef ik nog los door',
        'Eén overzicht waarin iedereen ziet waar hij moet zijn en wat klaarligt'],
      urenq:'Hoeveel uur per week kost het plannen en voorbereiden van klussen?'},
    {label:'Klantcontact', q:'Hoe handelt u mail en berichten van klanten af?',
      opts:[
        'Alles komt bij één persoon binnen, die alles zelf beantwoordt',
        'Verdeeld over meerdere mailboxen en telefoons, zonder overzicht',
        'Eén gezamenlijke inbox, maar elk antwoord wordt met de hand geschreven',
        'Vaste routes en standaardantwoorden, weinig handwerk'],
      urenq:'Hoeveel uur per week kosten mail en berichten van klanten?'},
    {label:'Telefoon en opvolging', q:'Wat gebeurt er als de telefoon gaat terwijl niemand kan opnemen?',
      opts:[
        'De beller krijgt de voicemail en ik bel soms terug',
        'Iemand belt terug als er tijd is, zonder vaste aanpak',
        'Er is een vaste terugbelregel, maar die kost veel tijd',
        'Een assistent of dienst vangt het op en legt het vast'],
      urenq:'Hoeveel uur per week kost het opnemen, terugbellen en opvolgen van oproepen?'},
    {label:'Als het drukker wordt', q:'Hoeveel tijd zit er gemiddeld in een nieuwe klus voordat het echte werk begint?',
      sub:'Denk aan de aanvraag verwerken, een offerte maken, de klus inplannen en het materiaal klaarzetten.',
      opts:[
        'Minder dan een half uur',
        'Een half uur tot twee uur',
        'Twee tot vijf uur',
        'Meer dan vijf uur']},
    {label:'Wat het met u doet', q:'Waar merkt u dit zelf het meest van?',
      opts:[
        'Ik zit ’s avonds of in het weekend nog achter de laptop',
        'Offertes blijven liggen en wij missen klussen',
        'Er gaat te vaak iets mis of wordt iets vergeten',
        'Ik zit vast in de uitvoering en kom niet toe aan ondernemen',
        'Alles loopt door elkaar en wij missen overzicht',
        'Wij kunnen niet groeien zonder extra mensen']}
  ];
  var TOT = VRAGEN.length;                 /* zeven stappen */
  var I_VOORWERK = AANTAL_GEBIEDEN;        /* stap 6 */
  var I_PIJN = AANTAL_GEBIEDEN + 1;        /* stap 7 */
  var VOORWERK_MIDDEN = [0.25, 1.25, 3.5, 6];   /* uur per nieuwe klus */
  var PIJNREGEL = [
    'U gaf aan dat u ’s avonds of in het weekend nog achter de laptop zit. Dat is precies de tijd die u terug wilt hebben.',
    'U gaf aan dat offertes blijven liggen. Sneller een offerte klaar hebben is direct meer kans op de klus.',
    'U gaf aan dat er te vaak iets misgaat. Minder overtikken betekent ook minder fouten.',
    'U gaf aan dat u vastzit in de uitvoering. Hoe minder handwerk, hoe meer tijd u overhoudt voor het bedrijf zelf.',
    'U gaf aan dat het overzicht ontbreekt. Eén plek per klant en vaste routes brengen rust.',
    'U gaf aan dat u niet kunt groeien zonder extra mensen. Elk uur dat uw team terugkrijgt is ruimte voor meer werk.'
  ];
  var WEGING = [4, 3, 2, 1];

  /* S.n = hoe het nu gaat (0 tot 3, per onderdeel), S.h = uren-klasse (0 tot 4, per onderdeel),
     S.v = voorwerk per klus (0 tot 3), S.p = pijnpunt (0 tot 5). */
  var S = {i:0, n:[], h:[], v:null, p:null, pct:50, tarief:'', k:10};
  var nl = function(n, d){ return n.toLocaleString('nl-NL', {minimumFractionDigits:d||0, maximumFractionDigits:d||0}); };
  var uur = function(h){ var x = h >= 10 ? Math.round(h) : Math.round(h * 10) / 10; return nl(x, x % 1 ? 1 : 0); };
  var geld = function(x){ return new Intl.NumberFormat('nl-NL', {style:'currency', currency:'EUR', maximumFractionDigits:0}).format(x); };
  var is = function(x){ return typeof x === 'number'; };

  function el(tag, attrs, kids){
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function(k){
      if (k === 'class') e.className = attrs[k];
      else if (k === 'tekst') e.textContent = attrs[k];
      else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function(c){ if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function leeg(){ while (app.firstChild) app.removeChild(app.firstChild); }
  function naarBoven(h){
    var t = document.getElementById('scan-kop');
    if (t) t.hidden = true;
    window.scrollTo({top: Math.max(0, app.getBoundingClientRect().top + window.scrollY - 76), behavior:'instant'});
    if (h) { h.setAttribute('tabindex', '-1'); h.focus({preventScroll:true}); }
  }

  /* ── rekenen ── */
  function bereken(){
    var H = 0, niveaus = 0;
    var gebieden = SLEUTELS.map(function(k, n){
      var u = UREN_MIDDEN[S.h[n]];
      H += u; niveaus += S.n[n];
      return {key:k, niveau:S.n[n], uren:u, klasse:UREN_KLASSEN[S.h[n]], antwoord:VRAGEN[n].opts[S.n[n]]};
    }).sort(function(x, y){ return (y.uren - x.uren) || (x.niveau - y.niveau); });
    var score = 10 * niveaus / (3 * AANTAL_GEBIEDEN);
    var band = score < 4 ? 'Veel handwerk' : score < 7 ? 'Half op orde' : 'Goed geregeld';
    /* Eerste stap: het grootste onderdeel dat nog niet goed geregeld is. */
    var begin = gebieden[0];
    for (var j = 0; j < gebieden.length; j++) { if (gebieden[j].niveau < 3) { begin = gebieden[j]; break; } }
    return {H:H, gebieden:gebieden, top:gebieden[0], begin:begin, score:score, band:band, pijn:S.p, voorwerk:VOORWERK_MIDDEN[S.v]};
  }

  /* ── de vragen ── */
  function klaar(i){
    if (i < AANTAL_GEBIEDEN) return is(S.n[i]) && is(S.h[i]);
    return i === I_VOORWERK ? is(S.v) : is(S.p);
  }
  function opslaan(i, k){
    if (i < AANTAL_GEBIEDEN) S.n[i] = k;
    else if (i === I_VOORWERK) S.v = k;
    else S.p = k;
  }
  function gekozen(i){ return i < AANTAL_GEBIEDEN ? S.n[i] : (i === I_VOORWERK ? S.v : S.p); }

  function toonVraag(){
    var i = S.i, q = VRAGEN[i], dubbel = i < AANTAL_GEBIEDEN;
    leeg();
    var kop = el('h2', {tekst:q.q});
    var opties = el('div', {class:'n-opties', role:'radiogroup', 'aria-label':q.q});
    var volgende = el('button', {type:'button', class:'n-knop n-knop-vol n-knop-klein', tekst:'Volgende →', onclick:function(){ verder(); }});
    volgende.hidden = !klaar(i);
    var urenBlok = null, chips = null;

    function verder(){
      if (i < TOT - 1) { S.i++; toonVraag(); }
      else { zetHash(); toonUitslag(); }
    }
    var bezig = false;
    function mark(groep, knop){
      Array.prototype.forEach.call(groep.children, function(b){ b.classList.remove('sel'); b.setAttribute('aria-checked', 'false'); });
      knop.classList.add('sel'); knop.setAttribute('aria-checked', 'true');
    }
    function opslagKlik(k, knop){
      if (bezig) return;
      opslaan(i, k);
      mark(opties, knop);
      volgende.hidden = !klaar(i);
      if (dubbel) {
        urenBlok.hidden = false;
        urenBlok.scrollIntoView({block:'nearest', behavior:'instant'});
      } else {
        bezig = true;
        setTimeout(function(){ bezig = false; verder(); }, 220);
      }
    }
    q.opts.forEach(function(o, k){
      var b = el('button', {type:'button', class:'n-opt' + (gekozen(i) === k ? ' sel' : ''), role:'radio', 'aria-checked':gekozen(i) === k ? 'true' : 'false', tekst:o,
        onclick:function(){ opslagKlik(k, b); }});
      opties.appendChild(b);
    });

    if (dubbel) {
      chips = el('div', {class:'n-chips', role:'radiogroup', 'aria-label':q.urenq});
      UREN_KLASSEN.forEach(function(o, k){
        var b = el('button', {type:'button', class:'n-chip' + (S.h[i] === k ? ' sel' : ''), role:'radio', 'aria-checked':S.h[i] === k ? 'true' : 'false', tekst:o,
          onclick:function(){
            if (bezig) return;
            S.h[i] = k; mark(chips, b);
            volgende.hidden = false;
            bezig = true;
            setTimeout(function(){ bezig = false; verder(); }, 220);
          }});
        chips.appendChild(b);
      });
      urenBlok = el('div', {class:'n-uren'}, [
        el('h3', {tekst:q.urenq}),
        el('p', {class:'n-sub', tekst:'Bij benadering, voor u en iedereen die meewerkt.'}),
        chips
      ]);
      urenBlok.hidden = !is(S.n[i]);
    }

    var terug = el('button', {type:'button', class:'n-terug', tekst:'← Vorige', onclick:function(){
      if (S.i === 0) { terugNaarIntro(); } else { S.i--; toonVraag(); }
    }});
    app.appendChild(el('div', null, [
      el('h1', {class:'n-sr', tekst:'Tijdverlies-scan'}),
      el('div', {class:'n-voortgang', role:'progressbar', 'aria-valuemin':'0', 'aria-valuemax':String(TOT), 'aria-valuenow':String(i)}, [el('i', {style:'width:' + (i / TOT * 100) + '%'})]),
      el('div', {class:'n-voortgang-tekst'}, [el('span', {tekst:q.label}), el('span', {tekst:'Stap ' + (i + 1) + ' van ' + TOT})]),
      el('div', {class:'n-vraagkaart'}, [
        kop,
        q.sub ? el('p', {class:'n-sub', tekst:q.sub}) : null,
        opties,
        urenBlok,
        el('div', {class:'n-scan-nav'}, [terug, volgende]),
        el('p', {class:'n-klein', style:'margin-top:1rem', tekst:'Uw antwoorden blijven op dit apparaat.'})
      ])
    ]));
    naarBoven(kop);
  }
  function terugNaarIntro(){
    leeg(); intro.hidden = false;
    document.title = TITEL;
    var t = document.getElementById('scan-kop'); if (t) t.hidden = false;
    history.replaceState(null, '', location.pathname);
  }
  function start(){
    S.i = 0; S.n = []; S.h = []; S.v = null; S.p = null; S.pct = 50; S.tarief = ''; S.k = 10;
    document.title = TITEL;
    try { history.replaceState(null, '', location.pathname); } catch (e) {}
    intro.hidden = true;
    toonVraag();
  }
  /* De link naar de uitslag bevat alleen de antwoorden als cijfers. Er staat geen naam of bedrijf in. */
  function zetHash(){
    var h = '#u=' + S.n.join('') + '-' + S.h.join('') + '-' + S.v + '-' + S.p + '&p=' + S.pct + '&k=' + S.k;
    var t = Math.round(Number(S.tarief));
    if (t > 0) h += '&t=' + t;
    try { history.replaceState(null, '', location.pathname + h); } catch (e) {}
  }

  /* ── de uitslag ── */
  function toonUitslag(){
    var r = bereken();
    var topNaam = GEBIED[r.top.key].naam;
    var beginNaam = GEBIED[r.begin.key].naam;
    intro.hidden = true;
    document.title = 'Uitslag tijdverlies-scan | Complete AI';
    var t = document.getElementById('scan-kop'); if (t) t.hidden = true;
    leeg();

    var uitgave = el('div', {class:'n-uitslag'});

    /* alleen bij het afdrukken: een kop zodat de pdf een rapport is */
    uitgave.appendChild(el('div', {class:'n-alleen-print'}, [
      el('b', {tekst:'Complete AI'}),
      el('span', {tekst:'Tijdverlies-scan, uitslag van ' + new Date().toLocaleDateString('nl-NL', {day:'numeric', month:'long', year:'numeric'})})
    ]));

    /* kop met het grote getal */
    var goed = r.score >= 7.5 && r.H <= 15;
    var getalKop = el('h1', {class:'n-sr', tekst:'Uw uitslag van de tijdverlies-scan'});
    var groot = el('div', {class:'n-groot'}, [
      el('span', {class:'n-boven', tekst:'Uw uitslag'}),
      el('div', {class:'n-getal n-glans', tekst:uur(r.H)}),
      el('p', {class:'n-eenheid', tekst: goed
        ? 'uur per week aan kantoorwerk. U heeft het goed geregeld, de winst zit in de laatste handmatige stappen.'
        : 'uur per week gaat naar kantoorwerk. Dat is ongeveer ' + uur(r.H * 52 / 12) + ' uur per maand.'})
    ]);
    uitgave.appendChild(getalKop);
    uitgave.appendChild(groot);

    /* drie kengetallen */
    var kengetallen = el('div', {class:'n-raster n-drie n-kengetallen'}, [
      el('div', {class:'n-kaart'}, [el('span', {class:'n-boven', tekst:'Hoe goed geregeld'}),
        el('div', {class:'n-k-getal', tekst:nl(Math.round(r.score * 10) / 10, 1) + ' / 10'}),
        el('p', {class:'n-k-naam', tekst:r.band})]),
      el('div', {class:'n-kaart'}, [el('span', {class:'n-boven', tekst:'Grootste tijdvreter'}),
        el('div', {class:'n-k-getal n-k-tekst', tekst:topNaam}),
        el('p', {class:'n-k-naam', tekst:'U gaf aan: ' + r.top.klasse.toLowerCase() + ' per week'})]),
      el('div', {class:'n-kaart'}, [el('span', {class:'n-boven', tekst:'Per jaar'}),
        el('div', {class:'n-k-getal', tekst:nl(Math.round(r.H * 52 / 10) * 10) + ' uur'}),
        el('p', {class:'n-k-naam', tekst:'Bij 52 weken, afgerond op tientallen'})])
    ]);
    uitgave.appendChild(kengetallen);

    /* waar de tijd heen gaat */
    var maxH = r.gebieden[0].uren;
    var balken = el('div', null, r.gebieden.map(function(g, n){
      return el('div', {class:'n-balk-rij'}, [
        el('div', {class:'n-balk-kop'}, [
          el('b', null, [el('span', {class:'n-rang', tekst:String(n + 1)}), GEBIED[g.key].naam]),
          el('span', {tekst:g.klasse.toLowerCase() + ' per week'})]),
        el('div', {class:'n-balkje'}, [el('i', {style:'width:' + Math.max(4, Math.round(g.uren / maxH * 100)) + '%'})]),
        el('small', {tekst:'Nu: ' + g.antwoord})
      ]);
    }));
    uitgave.appendChild(el('div', {class:'n-kaart', style:'margin-top:var(--gat)'}, [
      el('h3', {tekst:'Waar de tijd naartoe gaat'}),
      el('p', {class:'n-klein', tekst:'Op volgorde van uren, zoals u ze zelf per onderdeel opgaf.'}),
      balken
    ]));

    /* wat u terugwint, in uren en in euro's */
    var uitUren = el('output', {tekst:''}), uitJaar = el('output', {tekst:''}), uitGeld = el('p', {class:'n-geld', tekst:''});
    var schuif = el('input', {type:'range', min:'10', max:'90', step:'5', value:String(S.pct), 'aria-label':'Welk deel van dit werk wilt u uit handen geven'});
    var pctUit = el('output', {tekst:S.pct + '%'});
    var tarief = el('input', {class:'n-veld', type:'number', min:'0', max:'500', step:'1', inputmode:'numeric', placeholder:'bijvoorbeeld 45', value:S.tarief, 'aria-label':'Wat een kantooruur u kost, in euro'});
    function ververs(){
      S.pct = Number(schuif.value);
      var u = r.H * S.pct / 100;
      pctUit.textContent = S.pct + '%';
      uitUren.textContent = uur(u) + ' uur per week';
      uitJaar.textContent = nl(Math.round(u * 52)) + ' uur per jaar';
      S.tarief = tarief.value;
      var tt = Number(tarief.value);
      uitGeld.textContent = tt > 0
        ? 'Bij ' + geld(tt) + ' per uur kost het kantoorwerk u nu ongeveer ' + geld(Math.round(r.H * 52 * tt)) + ' per jaar. Het deel dat u uit handen geeft is ongeveer ' + geld(Math.round(u * 52 * tt)) + ' per jaar.'
        : '';
      zetHash();
    }
    schuif.addEventListener('input', ververs);
    tarief.addEventListener('input', ververs);
    uitgave.appendChild(el('div', {class:'n-kaart', style:'margin-top:var(--gat)'}, [
      el('h3', {tekst:'Wat als u een deel uit handen geeft?'}),
      el('p', {tekst:'Wij beloven geen percentage. Schuif zelf om te zien wat het u zou opleveren.'}),
      el('div', {class:'n-cijfer'}, [el('span', {class:'n-print-label', tekst:'Deel dat u uit handen geeft:'}), schuif, pctUit]),
      el('div', {class:'n-cijfer'}, [el('span', {tekst:'Dat is'}), uitUren, el('span', {tekst:'en'}), uitJaar]),
      el('label', {class:'n-klein n-tariefrij'}, [
        el('span', {tekst:'Wat kost een kantooruur u ongeveer, in euro? (optioneel)'}), tarief]),
      uitGeld
    ]));

    /* als het drukker wordt */
    var uitExtra = el('p', {class:'n-geld', tekst:''});
    var kSchuif = el('input', {type:'range', min:'1', max:'30', step:'1', value:String(S.k), 'aria-label':'Hoeveel klussen er per maand bij komen'});
    var kUit = el('output', {tekst:String(S.k)});
    function verversK(){
      S.k = Number(kSchuif.value);
      kUit.textContent = String(S.k);
      var x = S.k * r.voorwerk;
      var weken = x / 40;
      var week = weken >= 2 ? ', ruim ' + Math.floor(weken) + ' werkweken van 40 uur'
               : weken >= 1 ? ', ruim een hele werkweek van 40 uur'
               : weken >= 0.5 ? ', ruim een halve werkweek van 40 uur' : '';
      uitExtra.textContent = 'Alleen het voorwerk kost dan ongeveer ' + uur(x) + ' uur per maand extra' + week + ', nog voordat er één klus is uitgevoerd.';
      zetHash();
    }
    kSchuif.addEventListener('input', verversK);
    uitgave.appendChild(el('div', {class:'n-kaart', style:'margin-top:var(--gat)'}, [
      el('h3', {tekst:'En als het drukker wordt?'}),
      el('p', {tekst:'U gaf aan hoeveel tijd er gemiddeld in een nieuwe klus zit voordat het echte werk begint. Stel zelf in hoeveel klussen er per maand bij komen.'}),
      el('div', {class:'n-cijfer'}, [el('span', {tekst:'Klussen erbij per maand'}), kSchuif, kUit]),
      uitExtra
    ]));
    ververs(); verversK();

    /* eerste stap en wat wij overnemen */
    var g = GEBIED[r.begin.key];
    uitgave.appendChild(el('div', {class:'n-raster n-twee', style:'margin-top:var(--gat)'}, [
      el('div', {class:'n-kaart n-eerst'}, [el('span', {class:'n-boven', tekst:'Uw eerste stap, vandaag nog'}), el('h3', {tekst:beginNaam}), el('p', {tekst:g.stap}),
        r.begin.key === 'telefoon' ? el('a', {class:'n-meer', href:'gemiste-oproepen-berekenen.html', tekst:'Naar de rekentool voor gemiste oproepen'}) : null]),
      el('div', {class:'n-kaart'}, [el('span', {class:'n-boven', tekst:'Wat wij ervan overnemen'}), el('h3', {tekst:beginNaam}), el('p', {tekst:g.wij}),
        el('a', {class:'n-meer', href:g.link, tekst:g.linktekst})])
    ]));
    uitgave.appendChild(el('p', {class:'n-tabelnoot', style:'text-align:center;margin-inline:auto', tekst:PIJNREGEL[r.pijn]}));

    /* bespreken */
    var vorm = el('form', {class:'n-form', id:'scanformulier', novalidate:'', 'data-bericht-hook':'scan', 'data-verzend':'', 'data-onderwerp':'Tijdverlies-scan uitslag'}, [
      el('input', {type:'text', name:'_honey', class:'n-honing', tabindex:'-1', autocomplete:'off', 'aria-hidden':'true'}),
      el('div', {class:'n-rij'}, [
        el('label', null, ['Naam', el('input', {type:'text', name:'naam', autocomplete:'name', required:''})]),
        el('label', null, ['Bedrijf', el('input', {type:'text', name:'bedrijf', autocomplete:'organization', required:''})])]),
      el('div', {class:'n-rij'}, [
        el('label', null, ['Telefoonnummer', el('input', {type:'tel', name:'telefoon', autocomplete:'tel', required:''})]),
        el('label', null, ['E-mail (optioneel)', el('input', {type:'email', name:'email', autocomplete:'email'})])]),
      el('label', null, ['Wat voor bedrijf is het?', el('select', {name:'branche'}, ['Installatiebedrijf', 'Metaal of lasbedrijf', 'Bouw of klusbedrijf', 'Garagebedrijf', 'Anders'].map(function(o){ return el('option', {tekst:o}); }))]),
      el('label', null, ['Welk programma gebruikt u nu voor offertes en facturen? (optioneel)', el('input', {type:'text', name:'programma', autocomplete:'off'})]),
      el('label', null, ['Wilt u nog iets kwijt? (optioneel)', el('textarea', {name:'bericht'})]),
      el('button', {type:'submit', class:'n-knop n-knop-vol', tekst:'Bespreek mijn uitslag'}),
      el('p', {class:'n-stand', role:'status', hidden:''}),
      el('p', {class:'n-klein', tekst:'Wij bellen u binnen één werkdag. Uw gegevens gebruiken wij alleen om contact op te nemen en uw uitslag toe te lichten.'})
    ]);
    uitgave.appendChild(el('div', {class:'n-kaart n-geen-print', style:'margin-top:var(--gat);padding:clamp(22px,3vw,34px)'}, [
      el('h3', {tekst:'Bespreek uw uitslag met ons'}),
      el('p', {tekst:'Wij lopen uw antwoorden met u door en zeggen eerlijk of automatiseren nu iets voor u is. Ook als dat niet zo is. Uw uitslag gaat pas naar ons als u hieronder op de knop drukt.'}),
      vorm
    ]));

    /* bewaren en opnieuw */
    var kopieerStand = el('span', {class:'n-klein', role:'status', tekst:''});
    uitgave.appendChild(el('div', {class:'n-acties n-geen-print', style:'justify-content:center;margin-top:28px'}, [
      el('button', {type:'button', class:'n-knop n-knop-lijn', tekst:'Bewaar als PDF', onclick:function(){ window.print(); }}),
      el('button', {type:'button', class:'n-knop n-knop-lijn', tekst:'Kopieer de link naar uw uitslag', onclick:function(){
        var url = location.href;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function(){ kopieerStand.textContent = 'Link gekopieerd.'; }, function(){ kopieerStand.textContent = url; });
        } else { kopieerStand.textContent = url; }
      }}),
      el('button', {type:'button', class:'n-knop n-knop-lijn', tekst:'Opnieuw beginnen', onclick:start}),
      kopieerStand
    ]));
    uitgave.appendChild(el('p', {class:'n-tabelnoot', style:'text-align:center;margin-inline:auto', tekst:
      'Zo is dit gerekend: de uren zijn de uren die u per onderdeel zelf koos, gerekend met het midden van de klasse. Hoe handmatiger uw antwoord, hoe lager het cijfer voor hoe goed het geregeld is. Het rekenvoorbeeld voor meer klussen vermenigvuldigt de voorwerktijd die u noemde met het aantal dat u instelt. Het is een schatting op basis van uw eigen antwoorden en geen belofte.'}));
    uitgave.appendChild(el('p', {class:'n-alleen-print n-printvoet', tekst:'Bespreken? glenn@complete-ai.nl, +31 6 24 56 96 86, complete-ai.nl'}));

    app.appendChild(uitgave);
    naarBoven(getalKop);
    window.CAI = window.CAI || {};
    /* Het formulier ontstaat pas nu, dus nieuw.js kan het niet bij het laden koppelen. Zonder koppeling
       zou een druk op de knop de pagina herladen met de gegevens in de adresbalk. */
    vorm.addEventListener('submit', function(e){ e.preventDefault(); });
    if (window.CAI.koppel) window.CAI.koppel(vorm);
    window.CAI.berichtHooks = window.CAI.berichtHooks || {};
    window.CAI.berichtHooks.scan = function(vrij){
      var veld = function(n){ var f = document.querySelector('#scanformulier [name="' + n + '"]'); return f ? f.value.trim() : ''; };
      var regels = ['Uitslag van de tijdverlies-scan', ''];
      regels.push('Uren per week (kantoorwerk, samen): ongeveer ' + uur(r.H));
      regels.push('Hoe goed geregeld: ' + nl(Math.round(r.score * 10) / 10, 1) + ' van 10 (' + r.band + ')');
      regels.push('Grootste tijdvreter: ' + topNaam);
      regels.push('Eerste stap die de uitslag noemt: ' + beginNaam);
      regels.push('');
      r.gebieden.forEach(function(x){ regels.push(GEBIED[x.key].naam + ': ' + x.klasse.toLowerCase() + ' per week. Nu: ' + x.antwoord); });
      regels.push('');
      regels.push('Voorwerk per nieuwe klus: ' + VRAGEN[I_VOORWERK].opts[S.v]);
      regels.push('Pijnpunt: ' + VRAGEN[I_PIJN].opts[r.pijn]);
      regels.push('Wil ' + S.pct + '% uit handen geven' + (Number(S.tarief) > 0 ? ' (kantooruur ' + S.tarief + ' euro)' : ''));
      if (veld('branche')) regels.push('Bedrijf: ' + veld('branche'));
      if (veld('programma')) regels.push('Programma voor offertes en facturen: ' + veld('programma'));
      if (vrij) { regels.push(''); regels.push('Bericht: ' + vrij); }
      return regels.join('\n');
    };
  }

  /* ── opstarten ── */
  var startknop = document.getElementById('scan-start');
  if (startknop) startknop.addEventListener('click', start);

  /* Een gedeelde link: #u=<offerte, admin, planning, klantcontact, telefoon>-<uren per onderdeel>-<voorwerk>-<pijn>&p=..&k=..&t=.. */
  var m = location.hash.match(/^#u=([0-3]{5})-([0-4]{5})-([0-3])-([0-5])((?:&[pkt]=\d{1,3})*)$/);
  if (m) {
    S.n = m[1].split('').map(Number);
    S.h = m[2].split('').map(Number);
    S.v = Number(m[3]);
    S.p = Number(m[4]);
    m[5].split('&').forEach(function(d){
      var w = d.split('=');
      if (w[0] === 'p') S.pct = Math.min(90, Math.max(10, Math.round(Number(w[1]) / 5) * 5));
      else if (w[0] === 'k') S.k = Math.min(30, Math.max(1, Number(w[1])));
      else if (w[0] === 't' && Number(w[1]) > 0) S.tarief = String(Math.min(500, Number(w[1])));
    });
    toonUitslag();
  }
})();
