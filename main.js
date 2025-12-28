(() => {
  const year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  const burger = document.querySelector("[data-burger]");
  const menu = document.querySelector("[data-menu]");

  if (!burger || !menu) return;

  const openMenu = () => {
    menu.classList.add("is-open");
    menu.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    document.documentElement.style.overflow = "hidden";
  };

  const closeMenu = () => {
    menu.classList.remove("is-open");
    menu.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    document.documentElement.style.overflow = "";
  };

  burger.addEventListener("click", () => {
    const isOpen = burger.getAttribute("aria-expanded") === "true";
    isOpen ? closeMenu() : openMenu();
  });

  // click fuori dal pannello chiude
  menu.addEventListener("click", (e) => {
    const insidePanel = e.target.closest(".menu__panel");
    if (!insidePanel) closeMenu();
  });

  // ESC chiude
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
  });

  // chiude quando clicchi su un link del menu
  menu.querySelectorAll("a").forEach(a => {
    a.addEventListener("click", () => closeMenu());
  });
})();
