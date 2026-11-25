// NYFun3 site — shared lightweight behaviour
document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('nav.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', menu.classList.contains('open'));
    });
  }
  // Table row filter: any input[data-filter] filters rows of target table(s)
  document.querySelectorAll('input[data-filter]').forEach(function (input) {
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      document.querySelectorAll(input.getAttribute('data-filter')).forEach(function (tbl) {
        tbl.querySelectorAll('tbody tr').forEach(function (row) {
          row.style.display = !q || row.textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
        });
      });
    });
  });
  // Last-updated stamp
  document.querySelectorAll('.js-stamp').forEach(function (el) {
    el.textContent = '2026-11-25';
  });
});
