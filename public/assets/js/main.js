// Kontaktformular: Zeitstempel setzen (Spam-Schutz) und Rückmeldung anzeigen
(function () {
  var f = document.querySelector('form.form');
  if (!f) return;
  var ts = f.querySelector('input[name="ts"]');
  if (ts) ts.value = Math.floor(Date.now() / 1000);
  var q = new URLSearchParams(location.search);
  var el = q.get('sent') === '1' ? document.getElementById('form-ok')
         : q.get('error') === '1' ? document.getElementById('form-err') : null;
  if (el) {
    el.hidden = false;
    history.replaceState(null, '', location.pathname + '#kontakt');
    document.getElementById('kontakt').scrollIntoView();
  }
})();
