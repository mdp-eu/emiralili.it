const menu=document.querySelector('.menu'),mobile=document.querySelector('.mobile-nav'),bar=document.querySelector('.progress');
menu.addEventListener('click',()=>mobile.classList.toggle('open'));
mobile.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mobile.classList.remove('open')));
const reveal=()=>{document.querySelectorAll('.reveal').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.88)el.classList.add('visible')});const max=document.documentElement.scrollHeight-innerHeight;bar.style.transform=`scaleX(${max?scrollY/max:0})`};
addEventListener('scroll',reveal,{passive:true});reveal();
