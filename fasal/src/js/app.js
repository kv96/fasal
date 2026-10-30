/* Fasal app.js — original code. Motifs, i18n, search, tabs, carousel, accordion, modal, compare. */
(function(){
"use strict";
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];

/* ---------- Original botanical SVG motifs (duotone, hue-parameterised) ---------- */
function motifSVG(motif,hue,size){
  const P=`hsl(${hue},48%,52%)`, T=`hsl(${hue},38%,86%)`, D=`hsl(${hue},45%,34%)`;
  const open=`<svg viewBox="0 0 100 100" width="${size||96}" height="${size||96}" fill="none" aria-hidden="true">`;
  const M={
  grain:`<path d="M50 92V38" stroke="${D}" stroke-width="4" stroke-linecap="round"/><path d="M50 30c-9-2-15-10-15-20 10 0 15 8 15 20zm0 0c9-2 15-10 15-20-10 0-15 8-15 20z" fill="${P}"/><path d="M50 52c-8-2-13-8-13-17 9 0 13 7 13 17zm0 0c8-2 13-8 13-17-9 0-13 7-13 17z" fill="${T}" stroke="${D}" stroke-width="2"/><path d="M50 74c-8-2-13-8-13-17 9 0 13 7 13 17zm0 0c8-2 13-8 13-17-9 0-13 7-13 17z" fill="${P}" opacity=".8"/><path d="M50 92c-6 0-12-3-16-8M50 92c6 0 12-3 16-8" stroke="${D}" stroke-width="3" stroke-linecap="round"/>`,
  pod:`<path d="M28 70C28 44 44 30 74 26c2 0 3 2 2 4C70 58 54 72 30 74c-1 0-2-2-2-4z" fill="${T}" stroke="${D}" stroke-width="3"/><circle cx="42" cy="58" r="5" fill="${P}"/><circle cx="54" cy="50" r="5" fill="${P}"/><circle cx="64" cy="42" r="5" fill="${P}"/><path d="M74 26c8-6 16-6 20-2-4 6-12 6-20 2z" fill="${P}"/>`,
  flower:`<circle cx="50" cy="50" r="9" fill="${D}"/><g fill="${P}"><ellipse cx="50" cy="28" rx="10" ry="14"/><ellipse cx="50" cy="72" rx="10" ry="14"/><ellipse cx="28" cy="50" rx="14" ry="10"/><ellipse cx="72" cy="50" rx="14" ry="10"/><ellipse cx="34" cy="34" rx="10" ry="12" transform="rotate(-45 34 34)"/><ellipse cx="66" cy="34" rx="10" ry="12" transform="rotate(45 66 34)"/><ellipse cx="34" cy="66" rx="10" ry="12" transform="rotate(45 34 66)"/><ellipse cx="66" cy="66" rx="10" ry="12" transform="rotate(-45 66 66)"/></g><circle cx="50" cy="50" r="6" fill="${T}"/>`,
  fruit:`<circle cx="50" cy="58" r="26" fill="${P}"/><path d="M50 58c-8-8-8-20 0-26 8 6 8 18 0 26z" fill="${T}" opacity=".55"/><path d="M50 32c0-8 4-12 10-14" stroke="${D}" stroke-width="4" stroke-linecap="round"/><path d="M60 20c8-4 16-2 20 4-6 4-14 4-20-4z" fill="${D}"/>`,
  leaf:`<path d="M50 88C30 70 26 44 34 18c26 4 40 24 34 52-4 12-10 16-18 18z" fill="${P}"/><path d="M50 88C48 64 44 40 34 18" stroke="${D}" stroke-width="3" stroke-linecap="round"/><path d="M48 66l-12-6M47 54l-10-8M46 42l-8-8M52 66l12-6M53 54l10-8" stroke="${D}" stroke-width="2" stroke-linecap="round"/>`,
  root:`<path d="M50 12c10 0 16 6 16 14 0 14-8 26-12 44-2 10-6 18-8 18s-4-8-5-16c-3-18-9-32-9-46 0-8 8-14 18-14z" fill="${P}"/><path d="M50 12c-4-6-12-8-18-6M50 12c4-6 12-8 18-6" stroke="${D}" stroke-width="3" stroke-linecap="round"/><path d="M38 40h24M40 54h20" stroke="${D}" stroke-width="2" opacity=".5"/>`,
  grass:`<g stroke="${P}" stroke-width="5" stroke-linecap="round"><path d="M50 90C50 70 46 50 34 34"/><path d="M50 90c0-22 4-42 16-58"/><path d="M50 90c-8-14-20-22-32-26"/><path d="M50 90c8-14 20-22 32-26"/><path d="M50 90V60"/></g><path d="M30 90h40" stroke="${D}" stroke-width="5" stroke-linecap="round"/>`,
  tree:`<circle cx="50" cy="36" r="22" fill="${P}"/><circle cx="34" cy="46" r="12" fill="${T}"/><path d="M50 58v32M50 70l-14-8M50 70l14-8" stroke="${D}" stroke-width="5" stroke-linecap="round"/><path d="M38 90h24" stroke="${D}" stroke-width="5" stroke-linecap="round"/>`,
  bulb:`<path d="M50 88c-14-8-20-20-20-34 0-16 10-28 20-34 10 6 20 18 20 34 0 14-6 26-20 34z" fill="${T}" stroke="${D}" stroke-width="3"/><path d="M50 20c-6 12-8 26-6 44M50 20c6 12 8 26 6 44" stroke="${P}" stroke-width="3"/><path d="M50 20c0-6 2-10 6-12" stroke="${D}" stroke-width="3" stroke-linecap="round"/>`
  };
  return open+(M[motif]||M.leaf)+`</svg>`;
}
window.fasalMotif=motifSVG;

/* ---------- i18n (UI chrome; crop long-form copy stays English — see README) ---------- */
const STR={
en:{home:"Home",learn:"Learn",about:"About",challenge:"Challenge",join:"Join",searchLabel:"What are you curious about?",searchPh:"Search for a crop, plant, or fun fact...",searchBtn:"Search",results:"Search results",noResults:"No crops found — try another word.",explore:"Explore crop groups",allCrops:"Browse all crops",back:"Back to groups",crops:"crops",info:"Info",structure:"Structure",compare:"Compare",pdf:"PDF",aboutPlant:"About this plant",uses:"Uses",grows:"Where it grows",care:"Plant care",facts:"Interesting facts",moreIn:"More in",listen:"Listen",pickCompare:"Pick a crop to compare with",signin:"Sign in",joinTitle:"Welcome to Fasal",create:"Create profile",login:"Log in",email:"Email address",name:"Your name",faqH:"Questions, answered",rulesH:"Challenge rules",howH:"How it works",lbH:"Top explorers",pointsH:"Your explorer points",pointsP:"Sign in to start collecting points.",ctaH:"Start exploring nature today.",ctaP:"From seed to plate — 39 field notes and counting.",ctaBtn:"Open the field notebook"},
hi:{home:"होम",learn:"सीखें",about:"हमारे बारे में",challenge:"चुनौती",join:"जुड़ें",searchLabel:"आप क्या जानना चाहते हैं?",searchPh:"फ़सल, पौधा या रोचक तथ्य खोजें...",searchBtn:"खोजें",results:"खोज परिणाम",noResults:"कोई फ़सल नहीं मिली — कोई और शब्द आज़माएँ।",explore:"फ़सल समूह देखें",allCrops:"सभी फ़सलें देखें",back:"समूहों पर वापस",crops:"फ़सलें",info:"जानकारी",structure:"संरचना",compare:"तुलना",pdf:"पीडीएफ",aboutPlant:"इस पौधे के बारे में",uses:"उपयोग",grows:"कहाँ उगता है",care:"देखभाल",facts:"रोचक तथ्य",moreIn:"इसी समूह में और",listen:"सुनें",pickCompare:"तुलना के लिए फ़सल चुनें",signin:"साइन इन",joinTitle:"फ़सल में आपका स्वागत है",create:"प्रोफ़ाइल बनाएँ",login:"लॉग इन",email:"ईमेल पता",name:"आपका नाम",faqH:"सवालों के जवाब",rulesH:"चुनौती के नियम",howH:"यह कैसे काम करता है",lbH:"शीर्ष खोजकर्ता",pointsH:"आपके एक्सप्लोरर पॉइंट्स",pointsP:"पॉइंट्स जुटाना शुरू करने के लिए साइन इन करें।",ctaH:"आज ही प्रकृति की खोज शुरू करें।",ctaP:"बीज से थाली तक — 39 फ़ील्ड नोट्स और गिनती जारी।",ctaBtn:"फ़ील्ड नोटबुक खोलें"}};
let lang=localStorage.getItem('fasal-lang')||'en';
function applyLang(){
  document.documentElement.lang=lang==='hi'?'hi':'en';
  $$('[data-i18n]').forEach(el=>{const k=el.dataset.i18n; if(STR[lang][k]) el.textContent=STR[lang][k];});
  $$('[data-i18n-ph]').forEach(el=>{el.placeholder=STR[lang][el.dataset.i18nPh]||'';});
  $$('.lang-toggle button').forEach(b=>b.classList.toggle('on',b.dataset.lang===lang));
  $$('[data-name-en]').forEach(el=>{el.textContent=lang==='hi'?el.dataset.nameHi:el.dataset.nameEn;});
  $$('[data-tag-en]').forEach(el=>{el.textContent=lang==='hi'?el.dataset.tagHi:el.dataset.tagEn;});
  syncUser();
}
document.addEventListener('click',e=>{
  const b=e.target.closest('.lang-toggle button'); if(!b) return;
  lang=b.dataset.lang; localStorage.setItem('fasal-lang',lang); applyLang();
});
document.addEventListener('DOMContentLoaded',applyLang);

/* ---------- Live search ---------- */
const CROPS=window.FASAL_CROPS||[];
function cropURL(c){return (window.FASAL_BASE||'.')+'/crop/'+c.slug+'/index.html';}
function searchHTML(q){
  q=q.trim().toLowerCase(); if(!q) return '';
  const hits=CROPS.filter(c=>(c.name+' '+c.hindi+' '+c.binomial+' '+(c.tags||'')).toLowerCase().includes(q)).slice(0,7);
  if(!hits.length) return `<div class="sr-empty">${STR[lang].noResults}</div>`;
  return `<div class="sr-head">${STR[lang].results} (${hits.length})</div>`+hits.map(c=>
    `<a class="sr-item" href="${cropURL(c)}"><span class="sr-thumb" style="background:hsl(${c.hue},45%,90%)">${motifSVG(c.motif,c.hue,30)}</span><span><b>${lang==='hi'?c.hindi:c.name}</b><i>${c.binomial}</i></span></a>`).join('');
}
function wireSearch(inputId,boxId){
  const inp=document.getElementById(inputId), box=document.getElementById(boxId);
  if(!inp||!box) return;
  const render=()=>{const h=searchHTML(inp.value); box.innerHTML=h; box.classList.toggle('open',!!h);};
  inp.addEventListener('input',render);
  inp.addEventListener('focus',render);
  const btn=inp.closest('.search-row')?.querySelector('button');
  btn?.addEventListener('click',e=>{
    e.preventDefault();
    const a=box.querySelector('.sr-item');
    if(a){location.href=a.href;}else{render();}
  });
  document.addEventListener('click',e=>{
    if(!e.target.closest('#'+boxId)&&!e.target.closest('#'+inputId)&&!e.target.closest('.search-row')) box.classList.remove('open');
  });
  inp.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();const a=box.querySelector('.sr-item'); if(a) location.href=a.href;}});
}
document.addEventListener('DOMContentLoaded',()=>{wireSearch('q','sr');});

/* ---------- Tabs ---------- */
document.addEventListener('click',e=>{
  const t=e.target.closest('.tab'); if(!t) return;
  const wrap=t.closest('[data-tabs]');
  $$('.tab',wrap).forEach(x=>x.classList.remove('on')); t.classList.add('on');
  $$('.tabpane',wrap).forEach(p=>p.classList.toggle('on',p.id==='pane-'+t.dataset.tab));
});

/* ---------- Carousel ---------- */
function initCarousels(){
  $$('.carousel').forEach(car=>{
    if(car.__inited) return;
    car.__inited=true;
    const slides=$$('.car-slide',car), dots=$$('.car-dots i',car), count=$('.car-count',car);
    let i=0;
    const show=n=>{i=(n+slides.length)%slides.length;
      slides.forEach((s,k)=>s.style.display=k===i?'grid':'none');
      dots.forEach((d,k)=>d.classList.toggle('on',k===i));
      if(count) count.textContent=`${i+1} / ${slides.length}`;};
    $('.car-prev',car)?.addEventListener('click',()=>show(i-1));
    $('.car-next',car)?.addEventListener('click',()=>show(i+1));
    dots.forEach((d,k)=>d.addEventListener('click',()=>show(k)));
    show(0);
  });
}
document.addEventListener('DOMContentLoaded',initCarousels);
initCarousels();

/* ---------- FAQ accordion ---------- */
document.addEventListener('click',e=>{
  const q=e.target.closest('.faq-q'); if(!q) return;
  q.closest('.faq-item').classList.toggle('open');
});

/* ---------- Modal ---------- */
function openModal(id){document.getElementById(id)?.classList.add('open');}
function closeModal(el){el.closest('.modal-back')?.classList.remove('open');}
document.addEventListener('click',e=>{
  const opener=e.target.closest('[data-open-modal]');
  if(opener){e.preventDefault();openModal(opener.dataset.openModal);return;}
  if(e.target.matches('.modal-back')||e.target.closest('.modal .x')) closeModal(e.target);
  if(e.target.matches('#modalSignoutBtn, #pageSignoutBtn')){
    e.preventDefault();
    localStorage.removeItem('fasal-user');
    syncUser();
  }
});
document.addEventListener('keydown',e=>{if(e.key==='Escape')$$('.modal-back.open').forEach(m=>m.classList.remove('open'));});

/* Demo auth: front-end only, stored in localStorage */
document.addEventListener('submit',e=>{
  if(!e.target.matches('#joinForm, #loginPageForm')) return;
  e.preventDefault();
  const name=e.target.querySelector('[name=name]').value.trim()||'Explorer';
  localStorage.setItem('fasal-user',name);
  closeModal(e.target);
  syncUser();
});
function syncUser(){
  const u=localStorage.getItem('fasal-user');
  $$('[data-user-greet]').forEach(el=>{el.textContent=u?`Namaste, ${u}!`:`${STR[lang].signin}`;});
  $$('[data-points-note]').forEach(el=>{el.textContent=u?`${u}, you have 0 explorer points — photograph 10 different plants to score!`:`${STR[lang].pointsP}`;});
  $$('.user-name-display').forEach(el=>{el.textContent=u||'Explorer';});
  const mOut=document.getElementById('joinModalLoggedOut'), mIn=document.getElementById('joinModalLoggedIn');
  if(mOut) mOut.style.display=u?'none':'block';
  if(mIn) mIn.style.display=u?'block':'none';
  const lOut=document.getElementById('loginLoggedOut'), lIn=document.getElementById('loginLoggedIn');
  if(lOut) lOut.style.display=u?'none':'block';
  if(lIn) lIn.style.display=u?'block':'none';
}
document.addEventListener('DOMContentLoaded',syncUser);

/* ---------- Compare tool ---------- */
document.addEventListener('change',e=>{
  const sel=e.target.closest('.compare-select'); if(!sel) return;
  const host=document.getElementById('compareOut');
  if(!host) return;
  if(!sel.value){host.innerHTML='';return;}
  const other=CROPS.find(c=>c.slug===sel.value);
  if(!other) return;
  const cur=window.FASAL_CURRENT;
  if(!cur) return;
  const card=c=>{
    const cName=lang==='hi'?(c.hindi||c.name):c.name;
    const linkText=lang==='hi'?'पूरी फ़ील्ड नोट →':'Full field note →';
    return `<div class="compare-card ${c.slug===cur.slug?'vs':''}">
    <div style="height:110px;display:grid;place-items:center;background:hsl(${c.hue},45%,92%);border-radius:12px;margin-bottom:14px">${motifSVG(c.motif,c.hue,72)}</div>
    <h4>${cName}</h4><div class="binomial">${c.binomial}</div>
    <ul><li><b>${STR[lang].uses}:</b> ${c.uses[0]}</li><li><b>${STR[lang].grows}:</b> ${c.grows[0]}</li><li><b>${STR[lang].care}:</b> ${c.care[0]}</li></ul>
    <a href="${(window.FASAL_BASE||'.')}/crop/${c.slug}/index.html" style="font-weight:700;font-size:.9rem">${linkText}</a></div>`;
  };
  const curTitle=lang==='hi'?(cur.hindi||cur.name):cur.name;
  const otherTitle=lang==='hi'?(other.hindi||other.name):other.name;
  const vsText=lang==='hi'?'बनाम':'vs';
  host.innerHTML=`<div class="vs-badge">${curTitle}  ${vsText}  ${otherTitle}</div><div class="compare-grid">${card(cur)}${card(other)}</div>`;
  host.scrollIntoView({behavior:'smooth',block:'nearest'});
});

/* ---------- Learn page: A–Z filter ---------- */
document.addEventListener('DOMContentLoaded',()=>{
  const grid=document.getElementById('azGrid'); if(!grid) return;
  const bar=document.getElementById('azBar'), count=document.getElementById('azCount'), q2=document.getElementById('q2');
  const all=[...grid.children]; let letter='ALL';
  const draw=()=>{
    const q=(q2?.value||'').toLowerCase();
    let n=0;
    all.forEach(card=>{
      const name=card.dataset.name.toLowerCase();
      const okL=letter==='ALL'||name.startsWith(letter.toLowerCase());
      const okQ=!q||name.includes(q)||(card.dataset.tags||'').toLowerCase().includes(q);
      const show=okL&&okQ; card.style.display=show?'':'none'; if(show)n++;
    });
    if(count) count.textContent=`${n} crops`;
  };
  bar?.addEventListener('click',e=>{
    const b=e.target.closest('button'); if(!b) return;
    letter=b.dataset.letter; $$('button',bar).forEach(x=>x.classList.remove('on')); b.classList.add('on'); draw();
  });
  q2?.addEventListener('input',draw);
  q2?.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();draw();}});
  q2?.closest('.search-row')?.querySelector('button')?.addEventListener('click',e=>{e.preventDefault();draw();});
  draw();
});

/* ---------- Footer year ---------- */
document.addEventListener('DOMContentLoaded',()=>{$$('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());});
})();
