/* ══════════════════════════════════════
   comic.js — Products page JS
   ══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Product Filter ──
  const filterTabs = document.querySelectorAll('.filter-tab');
  const productItems = document.querySelectorAll('.product-item');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', function() {
      // Update active tab
      filterTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      const filter = this.dataset.filter;

      productItems.forEach((item, i) => {
        const category = item.dataset.category;
        const show = filter === 'all' || category === filter;

        if (show) {
          item.classList.remove('hidden');
          // Stagger reveal
          setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
          }, i * 60);
        } else {
          item.style.opacity = '0';
          item.style.transform = 'translateY(20px)';
          setTimeout(() => item.classList.add('hidden'), 300);
        }
      });

      // Recheck "featured" spans: if only 1 visible, remove span
      const visibleItems = [...productItems].filter(i => !i.classList.contains('hidden'));
      visibleItems.forEach(item => {
        if (item.classList.contains('product-featured')) {
          item.style.gridColumn = visibleItems.length === 1 ? 'span 1' : 'span 2';
        }
      });
    });
  });
});
