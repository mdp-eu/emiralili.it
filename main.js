(() => {
  const burger = document.querySelector("[data-burger]");
  const menu = document.querySelector("[data-menu]");
  const panel = menu ? menu.querySelector(".menu__panel") : null;

  const openMenu = () => {
    if (!menu) return;
    menu.classList.add("is-open");
    menu.setAttribute("aria-hidden", "false");
    if (burger) burger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };

  const closeMenu = () => {
    if (!menu) return;
    menu.classList.remove("is-open");
    menu.setAttribute("aria-hidden", "true");
    if (burger) burger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  if (burger && menu) {
    burger.addEventListener("click", () => {
      menu.classList.contains("is-open") ? closeMenu() : openMenu();
    });

    // click fuori dal pannello -> chiude
    menu.addEventListener("click", (e) => {
      if (!panel) return;
      if (!panel.contains(e.target)) closeMenu();
    });

    // ESC -> chiude
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && menu.classList.contains("is-open")) closeMenu();
    });

    // click su link menu -> chiude
    menu.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => closeMenu());
    });
  }

  // scroll “ASCOLTA” verso video
  document.querySelectorAll(".js-scroll-video").forEach((el) => {
    el.addEventListener("click", (e) => {
      const target = document.getElementById("video");
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
})();
