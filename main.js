(() => {
  const nav = document.querySelector(".site-nav");
  const openBtn = document.querySelector("[data-nav-toggle]");
  const drawer = document.querySelector("[data-nav-panel]");
  const backdrop = document.querySelector("[data-nav-backdrop]");
  const closeBtn = document.querySelector("[data-nav-close]");

  if (!nav || !openBtn || !drawer || !backdrop) return;

  const lock = () => {
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
  };

  const unlock = () => {
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
  };

  const open = () => {
    nav.classList.add("is-open");
    openBtn.setAttribute("aria-expanded", "true");
    lock();
  };

  const close = () => {
    nav.classList.remove("is-open");
    openBtn.setAttribute("aria-expanded", "false");
    unlock();
  };

  openBtn.addEventListener("click", e => {
    e.preventDefault();
    nav.classList.contains("is-open") ? close() : open();
  });

  backdrop.addEventListener("click", close);
  if (closeBtn) closeBtn.addEventListener("click", close);

  drawer.addEventListener("click", e => {
    if (e.target.closest("a")) close();
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && nav.classList.contains("is-open")) close();
  });
})();
