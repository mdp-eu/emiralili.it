(() => {
  // anno footer
  document.querySelectorAll("[data-year]").forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  const nav = document.querySelector(".site-nav");
  const openBtn = document.querySelector("[data-nav-toggle]");
  const panel = document.querySelector("[data-nav-panel]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const closeBtn = document.querySelector("[data-nav-close]");

  if (!nav || !openBtn || !panel || !backdrop) return;

  const openMenu = () => {
    nav.classList.add("is-open");
    openBtn.setAttribute("aria-expanded", "true");
    document.documentElement.classList.add("no-scroll");
    document.body.classList.add("no-scroll");
  };

  const closeMenu = () => {
    nav.classList.remove("is-open");
    openBtn.setAttribute("aria-expanded", "false");
    document.documentElement.classList.remove("no-scroll");
    document.body.classList.remove("no-scroll");
  };

  openBtn.addEventListener("click", e => {
    e.preventDefault();
    nav.classList.contains("is-open") ? closeMenu() : openMenu();
  });

  backdrop.addEventListener("click", closeMenu);
  if (closeBtn) closeBtn.addEventListener("click", closeMenu);

  panel.addEventListener("click", e => {
    if (e.target.closest("a")) closeMenu();
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && nav.classList.contains("is-open")) {
      closeMenu();
    }
  });
})();
