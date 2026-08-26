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

/* Article sharing: direct channels plus the device's native share sheet */
(() => {
  const article = document.querySelector('main.report .report-body');
  if (!article || document.querySelector('.article-share')) return;

  const canonical = document.querySelector('link[rel="canonical"]')?.href || location.href.split('#')[0];
  const title = document.querySelector('meta[property="og:title"]')?.content
    || document.querySelector('main.report h1')?.textContent?.trim()
    || document.title;
  const encodedUrl = encodeURIComponent(canonical);
  const encodedTitle = encodeURIComponent(title);
  const encodedMessage = encodeURIComponent(title + '\n' + canonical);

  const share = document.createElement('section');
  share.className = 'article-share';
  share.setAttribute('aria-labelledby', 'article-share-title');
  share.innerHTML = [
    '<div class="article-share-copy">',
      '<p class="kicker">Diffondi l’analisi</p>',
      '<h2 id="article-share-title">Condividi questo dossier</h2>',
      '<p>Se ritieni utile questo approfondimento, aiutalo a raggiungere altri lettori.</p>',
    '</div>',
    '<div class="article-share-actions">',
      '<a class="share-button share-facebook" href="https://www.facebook.com/sharer/sharer.php?u=' + encodedUrl + '" target="_blank" rel="noopener noreferrer" aria-label="Condividi su Facebook"><span aria-hidden="true">f</span><b>Facebook</b></a>',
      '<a class="share-button share-whatsapp" href="https://wa.me/?text=' + encodedMessage + '" target="_blank" rel="noopener noreferrer" aria-label="Condividi su WhatsApp"><span aria-hidden="true">WA</span><b>WhatsApp</b></a>',
      '<a class="share-button share-telegram" href="https://t.me/share/url?url=' + encodedUrl + '&text=' + encodedTitle + '" target="_blank" rel="noopener noreferrer" aria-label="Condividi su Telegram"><span aria-hidden="true">↗</span><b>Telegram</b></a>',
      '<button class="share-button share-native" type="button" aria-describedby="share-feedback"><span aria-hidden="true">⌁</span><b>Condividi</b></button>',
    '</div>',
    '<p class="share-feedback" id="share-feedback" role="status" aria-live="polite"></p>'
  ].join('');

  article.insertAdjacentElement('afterend', share);

  const nativeButton = share.querySelector('.share-native');
  const feedback = share.querySelector('.share-feedback');
  let feedbackTimer;

  const announce = message => {
    feedback.textContent = message;
    clearTimeout(feedbackTimer);
    feedbackTimer = setTimeout(() => { feedback.textContent = ''; }, 3500);
  };

  nativeButton.addEventListener('click', async () => {
    const data = { title, text: title, url: canonical };
    try {
      if (navigator.share && (!navigator.canShare || navigator.canShare(data))) {
        await navigator.share(data);
        if (typeof window.gtag === 'function') window.gtag('event', 'share', { method: 'native', content_type: 'article', item_id: canonical });
        return;
      }
      await navigator.clipboard.writeText(canonical);
      announce('Link copiato: ora puoi condividerlo dove preferisci.');
      if (typeof window.gtag === 'function') window.gtag('event', 'share', { method: 'copy_link', content_type: 'article', item_id: canonical });
    } catch (error) {
      if (error?.name === 'AbortError') return;
      const input = document.createElement('textarea');
      input.value = canonical;
      input.setAttribute('readonly', '');
      input.style.position = 'fixed';
      input.style.opacity = '0';
      document.body.appendChild(input);
      input.select();
      const copied = document.execCommand('copy');
      input.remove();
      announce(copied ? 'Link copiato: ora puoi condividerlo dove preferisci.' : 'Copia il link dalla barra del browser per condividerlo.');
    }
  });

  share.querySelectorAll('a.share-button').forEach(link => {
    link.addEventListener('click', () => {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'share', {
          method: link.classList.contains('share-facebook') ? 'facebook' : link.classList.contains('share-whatsapp') ? 'whatsapp' : 'telegram',
          content_type: 'article',
          item_id: canonical
        });
      }
    });
  });
})();

