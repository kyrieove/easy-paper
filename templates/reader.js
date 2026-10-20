(() => {
  const progress=document.getElementById('progress');
  const links=[...document.querySelectorAll('.toc-link')];
  const headings=[...document.querySelectorAll('h2[id]')];
  function update(){
    const max=document.documentElement.scrollHeight-innerHeight;
    progress.style.width=(max>0?Math.min(100,scrollY/max*100):0)+'%';
    let active='';for(const h of headings){if(h.getBoundingClientRect().top<190)active=h.id;}
    for(const a of links)a.classList.toggle('active',a.hash==='#'+active);
  }
  window.addEventListener('scroll',update,{passive:true});update();
  const box=document.getElementById('lightbox'),large=box.querySelector('img');
  function close(){box.classList.remove('show');box.setAttribute('aria-hidden','true');large.removeAttribute('src');}
  for(const img of document.querySelectorAll('.figure-image')){
    img.tabIndex=0;img.setAttribute('role','button');
    const show=()=>{large.src=img.src;box.classList.add('show');box.setAttribute('aria-hidden','false');box.querySelector('button').focus();};
    img.addEventListener('click',show);
    img.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show();}});
  }
  box.querySelector('button').addEventListener('click',close);
  box.addEventListener('click',e=>{if(e.target===box)close();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
})();