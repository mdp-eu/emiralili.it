(() => {
  // Year
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  const html = document.documentElement;

  const openBtn = document.querySelector("[data-nav-toggle]");
  const panel = document.querySelector("[data-nav-panel]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const closeBtn = document.querySelector("[data-nav-close]");

  // Se manca qualcosa, non rompiamo la pagina
  if (!openBtn || !panel || !backdrop) return;

  const isOpen = () => html.classList.contains("menu-open");

  const open = () => {
    if (isOpen()) return;
    html.classList.add("menu-open");
    document.body.classList.add("menu-open");
    openBtn.setAttribute("aria-expanded", "true");

    // Focus primo elemento cliccabile nel drawer (accessibilità senza focus trap aggressivo)
    const firstLink = panel.querySelector('a[href], button:not([disabled])');
    if (firstLink) firstLink.focus({ preventScroll: true });
  };

  const close = () => {
    if (!isOpen()) return;
    html.classList.remove("menu-open");
    document.body.classList.remove("menu-open");
    openBtn.setAttribute("aria-expanded", "false");
    openBtn.focus({ preventScroll: true });
  };

  // IMPORTANT: stopPropagation evita click “doppi” strani in alcuni browser
  openBtn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    isOpen() ? close() : open();
  });

  // Backdrop close (pointerdown è più affidabile su mobile)
  backdrop.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    close();
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", (e) => {
      e.preventDefault();
      close();
    });
  }

  // Close on link click
  panel.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) close();
  });

  // ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
})();
