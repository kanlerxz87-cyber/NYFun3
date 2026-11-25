/* Progressive enhancement only: the site is fully usable without JavaScript. */
document.addEventListener('DOMContentLoaded', function () {
  // Per-table filtering and "unverified only" toggle.
  document.querySelectorAll('.table-wrap').forEach(function (wrap) {
    var table = wrap.querySelector('table');
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tr.data-row'));
    if (!rows.length) return;

    var controls = document.createElement('div');
    controls.className = 'table-controls';

    var input = document.createElement('input');
    input.type = 'search';
    input.placeholder = 'Filter rows…';
    input.setAttribute('aria-label', 'Filter rows in this table');

    var label = document.createElement('label');
    label.className = 'unverified-toggle';
    var checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(' Unverified only'));

    controls.appendChild(input);
    controls.appendChild(label);
    wrap.parentNode.insertBefore(controls, wrap);

    function apply() {
      var query = input.value.trim().toLowerCase();
      var only = checkbox.checked;
      rows.forEach(function (row) {
        var text = row.textContent.toLowerCase();
        var unverified = row.classList.contains('has-unverified');
        var hiddenByQuery = query.length > 0 && text.indexOf(query) === -1;
        var hiddenByToggle = only && !unverified;
        row.hidden = hiddenByQuery || hiddenByToggle;
      });
    }

    input.addEventListener('input', apply);
    checkbox.addEventListener('change', apply);
  });

  // Back-to-top button.
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'back-to-top';
  btn.setAttribute('aria-label', 'Back to top');
  btn.textContent = '↑ Top';
  document.body.appendChild(btn);
  window.addEventListener('scroll', function () {
    if (window.scrollY > 500) btn.classList.add('show');
    else btn.classList.remove('show');
  }, { passive: true });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
