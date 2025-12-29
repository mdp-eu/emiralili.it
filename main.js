(() => {
  const burger = document.querySelector("[data-burger]");
  const menu = document.querySelector("[data-menu]");
  const year = document.querySelector("[data-year]");

  if (year) year.textContent = new Date().getFullYear();

  function openMenu() {
    document.body.classList.add("menu-open");
    burger.setAttribute("aria-expanded", "true");
    menu.setAttribute("aria-hidden", "false");
  }

  function closeMenu() {
    document.body.classList.remove("menu-open");
    burger.setAttribute("aria-expanded", "false");
    menu.setAttribute("aria-hidden", "true");
  }

  if (burger && menu) {
    burger.addEventListener("click", () => {
      document.body.classList.contains("menu-open") ? closeMenu() : openMenu();
    });

    // click fuori = chiudi
    menu.addEventListener("click", (e) => {
      if (e.target === menu) closeMenu();
    });

    // ESC = chiudi
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeMenu();
    });
  }
})();
