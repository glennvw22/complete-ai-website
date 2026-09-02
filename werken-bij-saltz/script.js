/* ══════════════════════════════════════════════════════════
   WERKEN BIJ SALTZ PRODUCEMENT — Breskens
   Alle gegevens die kunnen wijzigen (telefoonnummer, WhatsApp,
   e-mail) staan als data-attribuut op <body>. Dit bestand leest
   ze uit en zet ze in de knoppen. Eén plek aanpassen is genoeg,
   en dat geldt voor de Nederlandse én de Engelse pagina.
   Geen bibliotheken, geen externe verbindingen.
   ══════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var lijf = document.body;
  var gegeven = function (naam, terugval) {
    var w = (lijf.getAttribute('data-' + naam) || '').trim();
    return w || (terugval || '');
  };

  var whatsapp = gegeven('whatsapp').replace(/[^0-9]/g, '');
  var telefoon = gegeven('telefoon');
  var mail     = gegeven('mail');
  var watekst  = gegeven('watekst', 'Hoi, ik ben geïnteresseerd in de vacature in Breskens.');
  var bedankt  = gegeven('bedankt', 'bedankt.html');
  var hook     = gegeven('hook');           /* leeg = geen Make-webhook */
  var engels   = document.documentElement.lang === 'en';

  /* ── 1. waar komt de bezoeker vandaan ────────────────────
     Zonder dit weet je straks niet welke advertentie de
     sollicitaties oplevert. De campagnecode uit de link wordt
     onthouden en meegestuurd met het formulier én in het
     WhatsApp-bericht gezet. ── */
  var bron = (function () {
    var p = new URLSearchParams(location.search);
    var stukken = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content']
      .map(function (k) { return p.get(k); })
      .filter(Boolean);
    if (!stukken.length && document.referrer) {
      try { stukken.push('via ' + new URL(document.referrer).hostname); } catch (e) {}
    }
    var tekst = stukken.join(' · ');
    try {
      if (tekst) sessionStorage.setItem('saltz-bron', tekst);
      else tekst = sessionStorage.getItem('saltz-bron') || '';
    } catch (e) {}
    return tekst || 'rechtstreeks';
  })();

  var bronveld = document.getElementById('bron');
  if (bronveld) bronveld.value = bron;

  /* ── 2. knoppen vullen ───────────────────────────────── */
  var waLink = whatsapp
    ? 'https://wa.me/' + whatsapp + '?text=' + encodeURIComponent(watekst + (bron !== 'rechtstreeks' ? ' [' + bron + ']' : ''))
    : '';

  Array.prototype.forEach.call(document.querySelectorAll('[data-wa]'), function (a) {
    /* De knop bovenaan springt naar het formulier op de telefoon;
       op alle andere knoppen opent WhatsApp direct. */
    if (!waLink) { a.setAttribute('href', '#solliciteren'); return; }
    a.setAttribute('href', waLink);
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener');
    a.addEventListener('click', function () { melden('whatsapp'); });
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-bel]'), function (a) {
    if (!telefoon) { a.hidden = true; return; }
    a.setAttribute('href', 'tel:' + telefoon.replace(/[^0-9+]/g, ''));
    a.addEventListener('click', function () { melden('bellen'); });
  });

  Array.prototype.forEach.call(document.querySelectorAll('[data-mailto]'), function (a) {
    if (!mail) { a.hidden = true; return; }
    a.setAttribute('href', 'mailto:' + mail);
  });

  /* Een conversie doorgeven aan wat er verder ook meeluistert
     (Meta-pixel, Google Ads, Plausible). Ontbreekt dat, dan
     gebeurt er simpelweg niets. */
  function melden(soort) {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: 'sollicitatie', methode: soort, bron: bron });
      if (typeof window.fbq === 'function') window.fbq('track', 'Lead', { content_name: soort });
      if (typeof window.plausible === 'function') window.plausible('sollicitatie', { props: { methode: soort } });
    } catch (e) {}
  }

  /* ── 3. het formulier ────────────────────────────────────
     Twee onafhankelijke routes: de mailbox via FormSubmit en —
     als er een webhook is ingevuld — Make voor het seintje op de
     telefoon. Eén die aankomt is genoeg. Mislukken ze allebei,
     dan krijgt de sollicitant de WhatsApp-knop en het
     telefoonnummer te zien, zodat de reactie niet verdampt.
     Zonder JavaScript doet de browser gewoon een POST naar het
     adres in het action-attribuut. ── */
  var f = document.getElementById('sollicitatieformulier');
  if (!f) return;

  var knop = document.getElementById('verstuurknop');
  var stand = document.getElementById('formstand');
  var knoptekst = knop ? knop.textContent : '';

  var T = engels ? {
    bezig: 'Sending…',
    mis: 'Sending failed. Send us a WhatsApp message instead — that always works.',
    misKnop: 'Open WhatsApp'
  } : {
    bezig: 'Bezig met versturen…',
    mis: 'Het versturen lukte niet. Stuur je bericht via WhatsApp — dat werkt altijd.',
    misKnop: 'Open WhatsApp'
  };

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!f.reportValidity()) return;

    knop.disabled = true;
    knop.textContent = T.bezig;
    stand.hidden = true;

    var fd = new FormData(f);

    var geslaagd = function (r) {
      if (!r.ok) return false;
      return r.json().then(function (d) { return String(d && d.success) === 'true'; })
                     .catch(function () { return true; }); /* 200 zonder JSON: aangekomen */
    };
    var mislukking = function () { return false; };

    var routes = [
      fetch('https://formsubmit.co/ajax/' + mail,
            { method: 'POST', headers: { Accept: 'application/json' }, body: fd })
        .then(geslaagd).catch(mislukking)
    ];
    if (hook) {
      routes.push(fetch(hook, { method: 'POST', body: fd }).then(geslaagd).catch(mislukking));
    }

    Promise.all(routes).then(function (uitkomsten) {
      knop.disabled = false;
      knop.textContent = knoptekst;

      if (uitkomsten.indexOf(true) > -1) {
        melden('formulier');
        f.reset();
        location.href = bedankt + (engels ? '?lang=en' : '');
        return;
      }

      stand.hidden = false;
      stand.className = 'formstand mis';
      stand.textContent = T.mis + ' ';
      if (waLink) {
        var a = document.createElement('a');
        a.href = waLink;
        a.target = '_blank';
        a.rel = 'noopener';
        a.textContent = T.misKnop;
        stand.appendChild(a);
      } else if (telefoon) {
        stand.textContent = T.mis + ' ' + telefoon;
      }
    });
  });
})();
