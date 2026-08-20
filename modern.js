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
