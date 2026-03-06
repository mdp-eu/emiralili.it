(() => {
  // ── Anno nel footer ──
  document.querySelectorAll('[data-year]').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  // ── Nav scroll shrink ──
  const navEl = document.querySelector('nav');
  if (navEl) {
    window.addEventListener('scroll', () => {
      const isMobile = window.innerWidth <= 900;
      navEl.style.padding = window.scrollY > 50
        ? (isMobile ? '0.7rem 1.4rem' : '0.8rem 3rem')
        : (isMobile ? '1rem 1.4rem'  : '1.2rem 3rem');
    }, { passive: true });
  }

  // ── Mobile overlay ──
  const hamburger   = document.getElementById('hamburger');
  const overlay     = document.getElementById('navOverlay');
  const overlayClose = document.getElementById('overlayClose');

  const openOverlay = () => {
    overlay && overlay.classList.add('open');
    hamburger && hamburger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  };
  const closeOverlay = () => {
    overlay && overlay.classList.remove('open');
    hamburger && hamburger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };

  hamburger    && hamburger.addEventListener('click', openOverlay);
  overlayClose && overlayClose.addEventListener('click', closeOverlay);
  overlay      && overlay.addEventListener('click', e => {
    if (e.target === overlay) closeOverlay();
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeOverlay();
  });

  // ── Active nav link ──
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav .nav-links a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href && !href.startsWith('http') && current === href) {
      a.classList.add('active');
    }
  });

  // ── Scroll reveal ──
  const reveals = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });

  reveals.forEach(r => {
    if (r.getBoundingClientRect().top < window.innerHeight) {
      r.classList.add('visible');
    } else {
      io.observe(r);
    }
  });
})();
