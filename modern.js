const menu=document.querySelector('.menu'),mobile=document.querySelector('.mobile-nav'),bar=document.querySelector('.progress');
if(menu&&mobile){menu.addEventListener('click',()=>mobile.classList.toggle('open'));mobile.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mobile.classList.remove('open')))}
const reveal=()=>{document.querySelectorAll('.reveal').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.88)el.classList.add('visible')});if(bar){const max=document.documentElement.scrollHeight-innerHeight;bar.style.transform=`scaleX(${max?scrollY/max:0})`}};
addEventListener('scroll',reveal,{passive:true});reveal();
const archiveEntries=[...document.querySelectorAll('.archive-entry')];
if(archiveEntries.length){
const filters=[...document.querySelectorAll('.macro-filter')],query=document.querySelector('#archive-query'),clear=document.querySelector('#clear-search'),searchLabel=document.querySelector('.archive-search'),count=document.querySelector('#result-count'),areaLabel=document.querySelector('#active-area'),empty=document.querySelector('#archive-empty');let activeArea='tutte';
const labels={'tutte':'Tutte le pubblicazioni','medio-oriente':'Medio Oriente','ordine-mondiale':'Ordine mondiale','balcani-macedonia':'Balcani e Macedonia','diaspora-identita':'Diaspora e identità'};
const normalize=value=>value.toLocaleLowerCase('it').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim();
const update=()=>{const term=normalize(query.value);let visible=0;archiveEntries.forEach(entry=>{const areaMatch=activeArea==='tutte'||entry.dataset.area===activeArea;const textMatch=!term||normalize(entry.dataset.search+' '+entry.textContent).includes(term);const show=areaMatch&&textMatch;entry.hidden=!show;if(show)visible++});areaLabel.textContent=labels[activeArea];count.textContent=`${visible} dossier`;empty.hidden=visible!==0;searchLabel.classList.toggle('has-value',Boolean(query.value))};
filters.forEach(filter=>filter.addEventListener('click',()=>{activeArea=filter.dataset.area;filters.forEach(item=>{const selected=item===filter;item.classList.toggle('active',selected);item.setAttribute('aria-selected',String(selected))});update()}));query.addEventListener('input',update);clear.addEventListener('click',()=>{query.value='';query.focus();update()});update();
}

if(!document.querySelector('script[data-analytics-loader]')){
const analytics=document.createElement('script');
analytics.src='/analytics.js?v=1';
analytics.defer=true;
analytics.dataset.analyticsLoader='true';
document.head.appendChild(analytics);
}

/* Article sharing: compact icons plus the device share sheet */
(() => {
  const article=document.querySelector('main.report .report-body');
  if(!article||document.querySelector('.article-share'))return;
  const url=document.querySelector('link[rel="canonical"]')?.href||location.href.split('#')[0];
  const title=document.querySelector('meta[property="og:title"]')?.content||document.querySelector('main.report h1')?.textContent?.trim()||document.title;
  const eu=encodeURIComponent(url),et=encodeURIComponent(title),em=encodeURIComponent(title+'\n'+url);
  const svg={
    f:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.6 22v-9h3l.5-3.5h-3.5V7.3c0-1 .3-1.7 1.8-1.7h1.9V2.5c-.3 0-1.5-.2-2.8-.2-2.8 0-4.7 1.7-4.7 4.8v2.4H6.7V13h3.1v9h3.8Z"/></svg>',
    w:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.5 4.1 1.6 5.9L.2 24l6.4-1.7a11.8 11.8 0 0 0 5.5 1.4c6.5 0 11.8-5.3 11.8-11.8 0-3.2-1.2-6.1-3.4-8.4Zm-8.4 18.2c-1.7 0-3.4-.5-4.9-1.3l-.4-.2-3.8 1 1-3.7-.2-.4a9.8 9.8 0 1 1 8.3 4.6Zm5.4-7.4c-.3-.1-1.8-.9-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8 1-1 1.2-.2.2-.4.2-.7.1-2-.9-3.3-1.8-4.6-4-.3-.6.3-.6.9-1.3.1-.2.1-.3.2-.5 0-.2 0-.4-.1-.5-.1-.2-.7-1.7-1-2.3-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.4 1.8.8 2.5.8 3.4.7 1-.1 1.8-.8 2.1-1.5.3-.7.3-1.3.2-1.5-.2-.2-.4-.3-.7-.4Z"/></svg>',
    t:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.6 2.3 20 20.9c-.3 1.3-1 1.6-2.1 1l-5.5-4-2.7 2.6c-.3.3-.5.6-1.1.6l.4-5.6L19.2 6c.4-.4-.1-.6-.7-.2L5.9 13.7.5 12c-1.2-.4-1.2-1.2.3-1.8L22 2c1-.4 1.9.2 1.6.3Z"/></svg>',
    s:'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 16.1c-.8 0-1.5.3-2.1.8l-7.7-4.5c.1-.3.1-.6.1-.9s0-.6-.1-.9l7.6-4.4A3.5 3.5 0 1 0 15 4c0 .3 0 .6.1.9L7.5 9.3A3.5 3.5 0 1 0 7.5 14l7.6 4.4c-.1.2-.1.5-.1.8a3.5 3.5 0 1 0 3-3.1Z"/></svg>'
  };
  const nav=document.createElement('nav');
  nav.className='article-share';nav.setAttribute('aria-label','Condividi questo dossier');
  nav.innerHTML=
    '<button class="share-icon share-facebook" type="button" aria-label="Condividi su Facebook" title="Facebook">'+svg.f+'</button>'+
    '<a class="share-icon share-whatsapp" href="https://wa.me/?text='+em+'" target="_blank" rel="noopener noreferrer" aria-label="Condividi su WhatsApp" title="WhatsApp">'+svg.w+'</a>'+
    '<a class="share-icon share-telegram" href="https://t.me/share/url?url='+eu+'&text='+et+'" target="_blank" rel="noopener noreferrer" aria-label="Condividi su Telegram" title="Telegram">'+svg.t+'</a>'+
    '<button class="share-icon share-native" type="button" aria-label="Condividi con un’altra applicazione" title="Condividi">'+svg.s+'</button>'+
    '<span class="share-feedback" role="status" aria-live="polite"></span>';
  article.insertAdjacentElement('afterend',nav);
  const feedback=nav.querySelector('.share-feedback');let timer;
  const say=m=>{feedback.textContent=m;clearTimeout(timer);timer=setTimeout(()=>feedback.textContent='',3000)};
  const track=method=>{if(typeof window.gtag==='function')window.gtag('event','share',{method,content_type:'article',item_id:url})};
  nav.querySelector('.share-facebook').addEventListener('click',async()=>{
    const data={title,text:title,url};
    const webFallback='https://m.facebook.com/sharer.php?u='+eu+'&quote='+et;
    try{
      if(navigator.share&&(!navigator.canShare||navigator.canShare(data))){await navigator.share(data);track('facebook_native');return}
      location.href=webFallback;
    }catch(error){
      if(error?.name==='AbortError')return;
      location.href=webFallback;
    }
  });
  nav.querySelector('.share-whatsapp').addEventListener('click',()=>track('whatsapp'));
  nav.querySelector('.share-telegram').addEventListener('click',()=>track('telegram'));
  nav.querySelector('.share-native').addEventListener('click',async()=>{
    const data={title,text:title,url};
    try{
      if(navigator.share&&(!navigator.canShare||navigator.canShare(data))){await navigator.share(data);track('native');return}
      await navigator.clipboard.writeText(url);say('Link copiato');track('copy_link');
    }catch(error){
      if(error?.name==='AbortError')return;
      const input=document.createElement('textarea');input.value=url;input.setAttribute('readonly','');input.style.position='fixed';input.style.opacity='0';document.body.appendChild(input);input.select();
      const copied=document.execCommand('copy');input.remove();say(copied?'Link copiato':'Copia il link dalla barra del browser');
    }
  });
})();

