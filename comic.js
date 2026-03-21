/* ══════════════════════════════════════
   comic.js — Products page JS
   Filter + Lightbox
   ══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─────────────────────────────────────
     PRODUCT FILTER
  ───────────────────────────────────── */
  const filterTabs  = document.querySelectorAll('.filter-tab');
  const productItems = document.querySelectorAll('.product-item');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', function () {
      filterTabs.forEach(t => t.classList.remove('active'));
      this.classList.add('active');

      const filter = this.dataset.filter;

      productItems.forEach((item, i) => {
        const match = filter === 'all' || item.dataset.category === filter;

        if (match) {
          item.classList.remove('hidden');
          item.style.opacity = '0';
          item.style.transform = 'translateY(20px)';
          // Stagger reveal
          requestAnimationFrame(() => {
            setTimeout(() => {
              item.style.transition = 'opacity 0.4s ease, transform 0.4s ease, border-color 0.35s, box-shadow 0.35s, transform 0.35s';
              item.style.opacity = '1';
              item.style.transform = 'translateY(0)';
            }, i * 55);
          });
        } else {
          item.style.opacity = '0';
          item.style.transform = 'translateY(10px)';
          setTimeout(() => item.classList.add('hidden'), 280);
        }
      });
    });
  });

  /* ─────────────────────────────────────
     LIGHTBOX
  ───────────────────────────────────── */
  const lightbox   = document.getElementById('lightbox');
  const lbImg      = document.getElementById('lb-img');
  const lbCaption  = document.getElementById('lb-caption');
  const lbClose    = document.getElementById('lb-close');
  const lbBackdrop = document.getElementById('lb-backdrop');

  if (!lightbox) return;

  function openLightbox(src, alt, caption) {
    lbImg.src = src;
    lbImg.alt = alt;
    lbCaption.textContent = caption || alt;
    lightbox.classList.add('open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    // Focus close button for accessibility
    setTimeout(() => lbClose.focus(), 50);
  }

  function closeLightbox() {
    lightbox.classList.remove('open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    // Clear src after transition
    setTimeout(() => { lbImg.src = ''; }, 320);
  }

  // Attach click to every [data-lightbox] image
  document.querySelectorAll('img[data-lightbox]').forEach(img => {
    img.style.cursor = 'zoom-in';
    img.addEventListener('click', (e) => {
      e.stopPropagation();
      openLightbox(img.src, img.alt, img.dataset.caption || '');
    });
  });

  // Close via ✕ button
  lbClose.addEventListener('click', closeLightbox);

  // Close via backdrop click
  lbBackdrop.addEventListener('click', closeLightbox);

  // Close via ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('open')) {
      closeLightbox();
    }
  });

  /* ─────────────────────────────────────
     FAVORITE TOGGLE
  ───────────────────────────────────── */
  document.querySelectorAll('.pi-fav').forEach(btn => {
    btn.addEventListener('click', function () {
      const isActive = this.classList.toggle('active');
      this.textContent = isActive ? '♥' : '♡';
    });
  });

});
