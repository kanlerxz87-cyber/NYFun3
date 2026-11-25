(function () {
  'use strict';
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
  }

  // Lightweight table filter: buttons with data-filter-group / data-filter-value
  // hide table rows whose data-tags attribute does not contain the value.
  var filterButtons = document.querySelectorAll('[data-filter-value]');
  var search = document.getElementById('table-search');
  var targetTable = document.querySelector('table[data-filterable]');
  var count = document.getElementById('visible-count');

  function applyFilters() {
    if (!targetTable) return;
    var active = document.querySelector('[data-filter-value].active');
    var value = active ? active.getAttribute('data-filter-value') : 'all';
    var term = (search && search.value || '').trim().toLowerCase();
    var shown = 0;
    Array.prototype.forEach.call(targetTable.querySelectorAll('tbody tr'), function (row) {
      var tags = (row.getAttribute('data-tags') || '').toLowerCase();
      var text = row.textContent.toLowerCase();
      var okGroup = value === 'all' || tags.indexOf(value) !== -1;
      var okTerm = !term || text.indexOf(term) !== -1;
      var visible = okGroup && okTerm;
      row.hidden = !visible;
      if (visible) shown++;
    });
    if (count) count.textContent = shown + ' row' + (shown === 1 ? '' : 's') + ' shown';
  }

  filterButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      filterButtons.forEach(function (b) { b.classList.remove('active'); });
      button.classList.add('active');
      applyFilters();
    });
  });
  if (search) search.addEventListener('input', applyFilters);
  applyFilters();
})();
