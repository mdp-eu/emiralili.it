(() => {
  const body = document.body;
  const btnOpen = document.querySelector('[data-menu-open]');
  const btnClose = document.querySelector('[data-menu-close]');
  const overlay = document.querySelector('[data-menu-overlay]');
  const drawerLinks = document.querySelectorAll('.drawer__links a');

  const openMenu = () => body.classList.add('menu-open');
  const closeMenu = () => body.classList.remove('menu-open');

  if (btnOpen) btnOpen.addEventListener('click', openMenu);
  if (btnClose) btnClose.addEventListener('click', closeMenu);
  if (overlay) overlay.addEventListener('click', closeMenu);

  drawerLinks.forEach(a => a.addEventListener('click', closeMenu));

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });

  // Year
  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();
})();
