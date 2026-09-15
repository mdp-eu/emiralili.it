document.addEventListener('DOMContentLoaded',()=>{
  if(![...document.querySelectorAll('link[rel="stylesheet"]')].some(l=>(l.getAttribute('href')||'').includes('site-fixes.css'))){
    const css=document.createElement('link');
    css.rel='stylesheet';
    css.href='/site-fixes.css?v=1';
    document.head.appendChild(css);
  }

  const menu=document.querySelector('.menu');
  const mobile=document.querySelector('.mobile-nav');
  const modernAlreadyPresent=[...document.scripts].some(s=>/(^|\/)modern\.js(?:\?|$)/.test(s.getAttribute('src')||''));

  if(menu&&mobile&&!modernAlreadyPresent){
    menu.setAttribute('aria-expanded','false');
    menu.dataset.menuBound='true';

    const setOpen=open=>{
      mobile.classList.toggle('open',open);
      menu.classList.toggle('open',open);
      menu.setAttribute('aria-expanded',String(open));
      document.documentElement.classList.toggle('nav-open',open);
      document.body.classList.toggle('nav-open',open);
    };
    const close=()=>setOpen(false);

    menu.addEventListener('click',e=>{
      e.preventDefault();
      e.stopImmediatePropagation();
      setOpen(!mobile.classList.contains('open'));
    });
    mobile.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
    document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});

    const observer=new MutationObserver(()=>{
      if(!mobile.classList.contains('open')&&menu.classList.contains('open'))setOpen(false);
    });
    observer.observe(mobile,{attributes:true,attributeFilter:['class']});
  }

  if(!modernAlreadyPresent&&!document.querySelector('script[data-modern-loader]')){
    const s=document.createElement('script');
    s.src='/modern.js?v=6';
    s.defer=true;
    s.dataset.modernLoader='true';
    document.body.appendChild(s);
  }
});
