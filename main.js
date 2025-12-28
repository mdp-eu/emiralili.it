(() => {
  // Year
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });

  const html = document.documentElement;

  const btn = document.querySelector("[data-menu-btn]");
  const drawer = document.querySelector("[data-menu-drawer]");
  const backdrop = document.querySelector("[data-menu-backdrop]");
  const closeBtn = document.querySelector("[data-menu-close]");

  if (!btn || !drawer || !backdrop) {
    // Se una pagina non ha il menu, non rompiamo nulla.
    return;
  }

  const isOpen = () => html.classList.contains("menu-open");

  const open = () => {
    if (isOpen()) return;
    html.classList.add("menu-open");
    document.body.classList.add("menu-open");
    btn.setAttribute("aria-expanded", "true");
  };

  const close = () => {
    if (!isOpen()) return;
    html.classList.remove("menu-open");
    document.body.classList.remove("menu-open");
    btn.setAttribute("aria-expanded", "false");
  };

  // Apri/chiudi
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    isOpen() ? close() : open();
  });

  // Chiudi su backdrop (pointerdown evita “open+close nello stesso tap”)
  backdrop.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    close();
  });

  // Chiudi su X
  if (closeBtn) {
    closeBtn.addEventListener("click", (e) => {
      e.preventDefault();
      close();
    });
  }

  // Chiudi su click link
  drawer.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) close();
  });

  // ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
})();
