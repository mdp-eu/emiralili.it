(() => {
  const y = document.querySelector("[data-year]");
  if (y) y.textContent = String(new Date().getFullYear());

  const burger = document.querySelector("[data-burger]");
  const menu = document.querySelector("[data-menu]");
  if (!burger || !menu) return;

  const open = () => {
    menu.style.display = "block";
    menu.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
  };

  const close = () => {
    menu.style.display = "none";
    menu.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
  };

  burger.addEventListener("click", () => {
    const isOpen = burger.getAttribute("aria-expanded") === "true";
    isOpen ? close() : open();
  });

  menu.addEventListener("click", (e) => {
    const isPanel = e.target.closest(".menu__panel");
    if (!isPanel) close();
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
})();
