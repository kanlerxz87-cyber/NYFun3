// Progressive client-side search & pill filtering for static verified tables
(function () {
  function initTableFilter(wrapper) {
    var tableId = wrapper.getAttribute('data-target-table');
    var table = document.getElementById(tableId);
    if (!table) return;

    var tbody = table.querySelector('tbody');
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
    var searchInput = wrapper.querySelector('[data-filter-search]');
    var selectFilter = wrapper.querySelector('[data-filter-select]');
    var pillBtns = Array.prototype.slice.call(wrapper.querySelectorAll('[data-filter-pill]'));
    var countEl = wrapper.querySelector('[data-filter-count]');
    var activePill = 'all';

    function applyFilters() {
      var q = searchInput ? searchInput.value.trim().toLowerCase() : '';
      var sel = selectFilter ? selectFilter.value : 'all';
      var shown = 0;

      rows.forEach(function (row) {
        var tags = (row.getAttribute('data-tags') || '').toLowerCase();
        var cluster = row.getAttribute('data-cluster') || '';
        var text = row.textContent.toLowerCase();

        var matchPill = activePill === 'all' || tags.split(',').indexOf(activePill) !== -1;
        var matchSel = sel === 'all' || cluster === sel;
        var matchQ = !q || text.indexOf(q) !== -1;

        if (matchPill && matchSel && matchQ) {
          row.style.display = '';
          shown += 1;
        } else {
          row.style.display = 'none';
        }
      });

      if (countEl) {
        countEl.textContent = 'Showing ' + shown + ' of ' + rows.length + ' verified rows';
      }
    }

    if (searchInput) {
      searchInput.addEventListener('input', applyFilters);
    }
    if (selectFilter) {
      selectFilter.addEventListener('change', applyFilters);
    }
    pillBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        pillBtns.forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        activePill = btn.getAttribute('data-filter-pill') || 'all';
        applyFilters();
      });
    });

    applyFilters();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var bars = document.querySelectorAll('[data-target-table]');
    Array.prototype.forEach.call(bars, initTableFilter);
  });
})();
