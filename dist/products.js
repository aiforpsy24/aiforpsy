const dialog=document.querySelector('dialog');
const content=document.querySelector('#dialog-content');
function show(id){const t=document.querySelector(id);if(!t)return;content.replaceChildren(t.content.cloneNode(true));dialog.showModal()}
document.querySelectorAll('.nav-contact').forEach(b=>b.addEventListener('click',()=>show('#contact-content')));
document.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
const menu=document.querySelector('.mobile-menu');
menu.querySelectorAll('a,button').forEach(el=>el.addEventListener('click',()=>menu.open=false));
document.addEventListener('click',e=>{if(!menu.contains(e.target))menu.open=false});
document.addEventListener('keydown',e=>{if(e.key==='Escape')menu.open=false});
dialog.addEventListener("close",()=>content.replaceChildren());
