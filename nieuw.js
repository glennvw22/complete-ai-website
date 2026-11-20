/* Complete AI, nieuwe website: kopbalk, menu en formulieren. Geen animaties. */
(function(){
  "use strict";

  /* oude ankers van de vorige site blijven werken */
  var oud = {'#scan':'scan.html', '#over':'#over-ons', '#diensten':'#oplossingen', '#intake':'#contact'};
  if (oud[location.hash]) {
    if (oud[location.hash].charAt(0) === '#') location.hash = oud[location.hash];
    else if (/(^|\/)(index\.html)?$/.test(location.pathname)) location.replace(oud[location.hash]);
  }

  var jaar = document.getElementById('jaar');
  if (jaar) jaar.textContent = new Date().getFullYear();

  /* ── kopbalk krijgt een rand zodra je scrolt ── */
  var balk = document.getElementById('balk');
  if (balk) {
    var zetRand = function(){ balk.classList.toggle('vast', window.scrollY > 12); };
    addEventListener('scroll', zetRand, {passive:true});
    zetRand();
  }

  /* ── menu op telefoon en tablet ── */
  var knop = document.getElementById('menuknop');
  var lade = document.getElementById('mobielmenu');
  var waas = document.getElementById('mobielwaas');
  if (knop && lade && waas && balk) {
    var open = false;
    var zet = function(aan){
      open = aan;
      knop.setAttribute('aria-expanded', aan ? 'true' : 'false');
      knop.setAttribute('aria-label', aan ? 'Menu sluiten' : 'Menu openen');
      lade.classList.toggle('open', aan);
      waas.classList.toggle('open', aan);
      document.body.classList.toggle('menu-open', aan);
      if (aan) lade.style.top = balk.getBoundingClientRect().height + 'px';
    };
    knop.addEventListener('click', function(){ zet(!open); });
    waas.addEventListener('click', function(){ zet(false); });
    lade.addEventListener('click', function(e){ if (e.target.closest('a')) zet(false); });
    addEventListener('keydown', function(e){ if (e.key === 'Escape' && open) { zet(false); knop.focus(); } });
    addEventListener('resize', function(){ if (open && innerWidth > 1100) zet(false); });
  }

  /* ── formulieren verzenden ──
     Twee onafhankelijke routes, zoals op de vorige site: Telegram voor het
     seintje, e-mail voor het archief. Eén die aankomt is genoeg. */
  function gelukt(r){
    if (!r.ok) return false;
    return r.json().then(function(d){ return String(d && d.success) === 'true'; })
                   .catch(function(){ return false; });
  }
  function nee(){ return false; }

  window.CAI = window.CAI || {};
  window.CAI.verstuur = function(fd){
    return Promise.all([
      fetch('https://complete-ai-production.up.railway.app/api/koppeling/website-formulier',
            {method:'POST', body: fd}).then(gelukt).catch(nee),
      fetch('https://formsubmit.co/ajax/glenn@complete-ai.nl',
            {method:'POST', headers:{'Accept':'application/json'}, body: fd})
            .then(gelukt).catch(nee)
    ]).then(function(u){ return u.indexOf(true) > -1; });
  };

  function basisVelden(fd, onderwerp){
    fd.set('_subject', 'Nieuwe aanvraag via complete-ai.nl');
    fd.set('_template', 'table');
    fd.set('_captcha', 'false');
    if (onderwerp) fd.set('onderwerp', onderwerp);
    return fd;
  }
  window.CAI.basisVelden = basisVelden;

  /* Een formulier koppelt zichzelf aan de verzendroutes. Formulieren die al in de pagina staan
     worden hieronder gekoppeld. Een formulier dat later door een script wordt gemaakt (de uitslag
     van de scan) roept window.CAI.koppel(formulier) zelf aan. */
  function koppel(f){
    if (!f || f.getAttribute('data-gekoppeld')) return;
    f.setAttribute('data-gekoppeld', '1');
    var knopEl = f.querySelector('button[type="submit"]');
    var stand = f.querySelector('.n-stand');
    var knoptekst = knopEl ? knopEl.textContent : '';

    f.addEventListener('submit', function(e){
      e.preventDefault();
      if (!f.reportValidity()) return;
      knopEl.disabled = true;
      knopEl.textContent = 'Bezig met versturen…';
      stand.hidden = true;

      var fd = basisVelden(new FormData(f), f.getAttribute('data-onderwerp'));
      var v = function(k){ return (fd.get(k) || '').toString().trim(); };
      var extra = f.getAttribute('data-bericht-hook');
      if (extra && window.CAI.berichtHooks && window.CAI.berichtHooks[extra]) {
        fd.set('bericht', window.CAI.berichtHooks[extra](v('bericht')));
      }

      window.CAI.verstuur(fd).then(function(ok){
        knopEl.disabled = false;
        knopEl.textContent = knoptekst;
        stand.hidden = false;
        if (ok) {
          f.reset();
          stand.className = 'n-stand goed';
          stand.textContent = 'Dank u. Wij hebben uw aanvraag ontvangen en bellen u binnen één werkdag terug.';
        } else {
          var body = ['Naam: ' + v('naam'), 'Bedrijf: ' + (v('bedrijf') || '-'),
                      'Telefoon: ' + (v('telefoon') || '-'), 'E-mail: ' + (v('email') || '-'), '',
                      v('bericht')].join('\n');
          stand.className = 'n-stand mis';
          stand.textContent = 'Het versturen lukte niet. Stuur uw gegevens rechtstreeks naar ';
          var a = document.createElement('a');
          a.href = 'mailto:glenn@complete-ai.nl?subject=' + encodeURIComponent('Aanvraag via complete-ai.nl') +
                   '&body=' + encodeURIComponent(body);
          a.textContent = 'glenn@complete-ai.nl';
          stand.appendChild(a);
          stand.appendChild(document.createTextNode('. Uw gegevens staan er dan al in.'));
        }
      });
    });
  }
  window.CAI.koppel = koppel;
  Array.prototype.forEach.call(document.querySelectorAll('form[data-verzend]'), koppel);
})();
