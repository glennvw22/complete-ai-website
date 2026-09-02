/* Toont de Engelse tekst als de sollicitant via de Engelse pagina
   binnenkwam (?lang=en). Los bestandje, want het strikte
   veiligheidsbeleid van deze pagina staat geen script in de HTML toe. */
(function () {
  if (new URLSearchParams(location.search).get('lang') !== 'en') return;
  document.documentElement.lang = 'en';
  document.title = 'Thank you — we will call you · Saltz Producement';
  document.getElementById('nl').hidden = true;
  document.getElementById('en').hidden = false;
})();
