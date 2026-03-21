/* ══════════════════════════════════════
   main.js — Shared JS for all pages
   ══════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Sticky Header ──
  const header = document.getElementById('main-header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── Mobile Nav Toggle ──
  const toggle = document.getElementById('nav-toggle');
  const nav    = document.getElementById('main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('open');
      toggle.classList.toggle('open', isOpen);
      // Prevent body scroll when menu is open
      document.body.style.overflow = isOpen ? 'hidden' : '';
      // Make sure header is always visible above drawer
      if (header) header.style.zIndex = '10000';
    });

    // Close on any nav link click
    nav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('open');
        toggle.classList.remove('open');
        document.body.style.overflow = '';
      });
    });

    // Close on backdrop tap (outside the nav area)
    document.addEventListener('click', (e) => {
      if (nav.classList.contains('open') &&
          !nav.contains(e.target) &&
          !toggle.contains(e.target)) {
        nav.classList.remove('open');
        toggle.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  // ── Active Nav Link (auto-detect current page) ──
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav ul li a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) {
      link.classList.add('active');
    }
  });

  // ── Scroll Reveal ──
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Also trigger nc-bar animations
        const bars = entry.target.querySelectorAll('.nc-bar');
        bars.forEach(bar => bar.style.width = bar.style.getPropertyValue('--pct') || bar.parentElement.style.getPropertyValue('--pct'));
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal').forEach(el => {
    revealObserver.observe(el);
  });

  // ── Nutrient card bar animation trigger ──
  const ncObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('.nutrient-card').forEach(card => {
    ncObserver.observe(card);
  });

  // ── Smooth product item stagger ──
  const productItems = document.querySelectorAll('.product-item');
  const piObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'none';
          entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease, border-color 0.45s, box-shadow 0.45s';
        }, 0);
        piObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  productItems.forEach((item, i) => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(30px)';
    piObserver.observe(item);
  });

  // ── Favorite Button Toggle ──
  document.querySelectorAll('.pi-fav').forEach(btn => {
    btn.addEventListener('click', function() {
      this.classList.toggle('active');
      this.textContent = this.classList.contains('active') ? '♥' : '♡';
    });
  });

  // ── Parallax hero orbs (subtle) ──
  const orbs = document.querySelectorAll('.hero-orb, .ph-orb, .bh-orb, .ah-orb');
  if (orbs.length > 0) {
    window.addEventListener('mousemove', (e) => {
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx;
      const dy = (e.clientY - cy) / cy;
      orbs.forEach((orb, i) => {
        const factor = (i % 2 === 0 ? 1 : -1) * 12;
        orb.style.transform = `translate(${dx * factor}px, ${dy * factor}px)`;
      });
    }, { passive: true });
  }

  // ── Scroll progress indicator (optional thin line) ──
  const progressBar = document.createElement('div');
  progressBar.id = 'scroll-progress';
  progressBar.style.cssText = `
    position: fixed; top: 0; left: 0; height: 2px;
    background: linear-gradient(to right, var(--amber), var(--amber-lt));
    z-index: 99999; width: 0; transition: width 0.1s linear;
    pointer-events: none;
  `;
  document.body.appendChild(progressBar);
  window.addEventListener('scroll', () => {
    const pct = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = pct + '%';
  }, { passive: true });

});
