const lang=document.documentElement.lang;
const dialog=document.querySelector('dialog');
const content=document.querySelector('#dialog-content');
function show(id){const t=document.querySelector(id);if(!t)return;content.replaceChildren(t.content.cloneNode(true));dialog.showModal()}
document.querySelectorAll('.nav-contact').forEach(b=>b.addEventListener('click',()=>show('#contact-content')));
document.querySelectorAll('[data-checkout]').forEach(b=>b.addEventListener('click',()=>show('#checkout-note')));
document.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close()}});
const menu=document.querySelector('.mobile-menu');
menu.querySelectorAll('a,button').forEach(el=>el.addEventListener('click',()=>menu.open=false));
document.addEventListener('click',e=>{if(!menu.contains(e.target))menu.open=false});
document.addEventListener('keydown',e=>{if(e.key==='Escape')menu.open=false});
document.querySelectorAll('.copy-prompt').forEach(b=>b.addEventListener('click',async()=>{const block=b.closest('.prompt-block');try{await navigator.clipboard.writeText(block.querySelector('pre').textContent);block.querySelector('.copy-status').textContent=lang==='ru'?'Скопировано':'Copied'}catch{block.querySelector('.copy-status').textContent=lang==='ru'?'Выделите и скопируйте текст сообщения ниже.':'Select and copy the message below.';const selection=window.getSelection();const range=document.createRange();range.selectNodeContents(block.querySelector('pre'));selection.removeAllRanges();selection.addRange(range)}}));
