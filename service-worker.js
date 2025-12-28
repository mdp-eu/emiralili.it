(() => {
  // Year
  const y = document.querySelector("[data-year]");
  if (y) y.textContent = String(new Date().getFullYear());

  const navRoot = document.querySelector(".site-nav");
  const btnOpen = document.querySelector("[data-nav-toggle]");
  const btnClose = document.querySelector("[data-nav-close]");
  const panel = document.querySelector("[data-nav-panel]");
  const backdrop = document.querySelector("[data-nav-backdrop]");

  if (!navRoot || !btnOpen || !panel || !backdrop) return;

  const focusableSel = [
    'a[href]',
    'button:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(",");

  const focusables = () => Array.from(panel.querySelectorAll(focusableSel));
  const isOpen = () => navRoot.classList.contains("is-open");

  const open = () => {
    navRoot.classList.add("is-open");
    btnOpen.setAttribute("aria-expanded", "true");
    document.documentElement.classList.add("no-scroll");
    document.body.classList.add("no-scroll");
    const f = focusables();
    if (f[0]) f[0].focus({ preventScroll: true });
  };

  const close = () => {
    navRoot.classList.remove("is-open");
    btnOpen.setAttribute("aria-expanded", "false");
    document.documentElement.classList.remove("no-scroll");
    document.body.classList.remove("no-scroll");
    btnOpen.focus({ preventScroll: true });
  };

  btnOpen.addEventListener("click", (e) => {
    e.preventDefault();
    isOpen() ? close() : open();
  });

  if (btnClose) btnClose.addEventListener("click", close);
  backdrop.addEventListener("click", close);

  // Close on link click
  panel.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) close();
  });

  // ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && isOpen()) close();
  });

  // Focus trap
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
})();
