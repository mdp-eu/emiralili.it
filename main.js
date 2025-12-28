(() => {
  // Footer year
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  // NAV (robusto)
  const navRoot = document.querySelector(".site-nav");
  const btnOpen = document.querySelector("[data-nav-toggle]");
  const panel = document.querySelector("[data-nav-panel]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const btnClose = document.querySelector("[data-nav-close]");

  // Se manca qualcosa, esci senza errori
  if (!navRoot || !btnOpen || !panel || !backdrop) {
    // Debug rapido (non rompe il sito)
    console.warn("[nav] elementi mancanti:", {
      navRoot: !!navRoot,
      btnOpen: !!btnOpen,
      panel: !!panel,
      backdrop: !!backdrop,
      btnClose: !!btnClose
    });
    return;
  }

  const focusableSel = [
    'a[href]',
    'button:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(",");

  const isOpen = () => navRoot.classList.contains("is-open");
  const focusables = () => Array.from(panel.querySelectorAll(focusableSel));

  const lockScroll = (lock) => {
    document.documentElement.classList.toggle("no-scroll", lock);
    document.body.classList.toggle("no-scroll", lock);
  };

  const open = () => {
    if (isOpen()) return;
    navRoot.classList.add("is-open");
    btnOpen.setAttribute("aria-expanded", "true");
    lockScroll(true);

    // focus primo elemento del drawer (accessibilità)
    const f = focusables();
    if (f[0]) f[0].focus({ preventScroll: true });
  };

  const close = () => {
    if (!isOpen()) return;
    navRoot.classList.remove("is-open");
    btnOpen.setAttribute("aria-expanded", "false");
    lockScroll(false);

    // ritorna focus al bottone hamburger
    btnOpen.focus({ preventScroll: true });
  };

  btnOpen.addEventListener("click", (e) => {
    e.preventDefault();
    isOpen() ? close() : open();
  });

  if (btnClose) {
    btnClose.addEventListener("click", (e) => {
      e.preventDefault();
      close();
    });
  }

  backdrop.addEventListener("click", close);

  // Chiudi su click link
  panel.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) close();
  });

  // Chiudi su ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });

  // Focus trap quando aperto
  document.addEventListener("keydown", (e) => {
    if (!isOpen() || e.key !== "Tab") return;

    const f = focusables();
    if (!f.length) return;

    const first = f[0];
    const last = f[f.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  // Sicurezza: se ridimensioni a desktop con menu aperto, chiudi.
  window.addEventListener("resize", () => {
    // se supera 900px, in genere non serve drawer
    if (window.innerWidth >= 900) close();
  });
})();
