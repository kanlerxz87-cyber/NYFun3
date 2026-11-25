(() => {
  const getCounter = (targetId) =>
    Array.from(document.querySelectorAll('[data-filter-count]')).find(
      (node) => node.dataset.filterCount === targetId,
    );

  const normalize = (value) => value.toLocaleLowerCase().trim();

  document.querySelectorAll('[data-filter-for]').forEach((input) => {
    const targetId = input.dataset.filterFor;
    const table = document.getElementById(targetId);
    if (!table) return;

    input.setAttribute('aria-controls', targetId);
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const count = getCounter(targetId);

    const update = () => {
      const query = normalize(input.value);
      let visible = 0;

      rows.forEach((row) => {
        const matches = !query || normalize(row.textContent).includes(query);
        row.hidden = !matches;
        if (matches) visible += 1;
      });

      if (count) {
        count.textContent = query ? `${visible} of ${rows.length} entries` : `${rows.length} entries`;
      }
    };

    input.addEventListener('input', update);
    update();
  });

  document.querySelectorAll('[data-filter-cards]').forEach((input) => {
    const targetId = input.dataset.filterCards;
    const container = document.getElementById(targetId);
    if (!container) return;

    input.setAttribute('aria-controls', targetId);
    const cards = Array.from(container.querySelectorAll('[data-search], .venue-card'));
    const count = getCounter(targetId);

    const update = () => {
      const query = normalize(input.value);
      let visible = 0;

      cards.forEach((card) => {
        const haystack = normalize(`${card.dataset.search || ''} ${card.textContent}`);
        const matches = !query || haystack.includes(query);
        card.hidden = !matches;
        if (matches) visible += 1;
      });

      if (count) {
        count.textContent = query ? `${visible} of ${cards.length} restaurants` : `${cards.length} restaurants`;
      }
    };

    input.addEventListener('input', update);
    update();
  });
})();
