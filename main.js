// main.js
document.addEventListener("DOMContentLoaded", () => {
  // NAV MOBILE
  const nav = document.querySelector(".nav");
  const navToggle = document.querySelector(".nav-toggle");

  if (nav && navToggle) {
    navToggle.addEventListener("click", () => {
      nav.classList.toggle("mobile-open");
    });
  }

  // ANNO AUTOMATICO NEL FOOTER
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // ANIMAZIONE DI INGRESSO DELLE SEZIONI
  const revealEls = document.querySelectorAll(
    ".section-box, .card, .contact-card, .cta-inner, .hero-card"
  );

  if (revealEls.length) {
    revealEls.forEach((el) => el.classList.add("reveal"));

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    revealEls.forEach((el) => observer.observe(el));
  }
});
