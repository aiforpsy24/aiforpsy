const cards=[...document.querySelectorAll('.card')];
const media=matchMedia('(min-width:761px)');
function responsive(){if(media.matches)cards.forEach(card=>card.removeAttribute('name'));cards.forEach(card=>{if(!media.matches)card.setAttribute('name','services');card.open=media.matches;card.querySelector('summary').tabIndex=media.matches?-1:0})}
responsive();media.addEventListener('change',responsive);
cards.forEach(card=>card.addEventListener('toggle',()=>{if(media.matches&&!card.open)card.open=true}));
const dialog=document.querySelector('dialog'),content=document.querySelector('#dialog-content');let selected='AIforPsy';
function showTemplate(id){content.replaceChildren(document.querySelector(id).content.cloneNode(true));dialog.showModal()}
document.querySelectorAll('.read-more').forEach(button=>button.addEventListener('click',()=>{selected=button.closest('.card').querySelector('.card-title').textContent;showTemplate('#service-'+button.dataset.service)}));
document.querySelectorAll('.nav-contact').forEach(button=>button.addEventListener('click',()=>showTemplate('#contact-content')));
const mobileMenu=document.querySelector('.mobile-menu');
mobileMenu.querySelectorAll('a,button').forEach(link=>link.addEventListener('click',()=>mobileMenu.open=false));
document.addEventListener('keydown',event=>{if(event.key==='Escape')mobileMenu.open=false});
document.addEventListener('click',event=>{if(!mobileMenu.contains(event.target))mobileMenu.open=false});
content.addEventListener('click',async event=>{if(event.target.closest('.contact-button'))content.replaceChildren(document.querySelector('#contact-content').content.cloneNode(true));if(event.target.closest('.copy-selection')){try{await navigator.clipboard.writeText(selected);event.target.textContent=document.documentElement.lang==='ru'?'Скопировано':'Copied'}catch{event.target.textContent=selected}}});
document.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close()}});
// Keep introductions top aligned using the tallest actual text, without an oversized fixed spacer.
function alignCardIntroductions(){
 const container=document.querySelector('.cards');
 container.style.removeProperty('--card-title-height');
 container.style.removeProperty('--card-lead-height');
 container.style.removeProperty('--card-preview-height');
 if(!media.matches)return;
 const titleHeight=Math.max(...cards.map(card=>card.querySelector('.card-title').getBoundingClientRect().height));
 container.style.setProperty('--card-title-height',Math.ceil(titleHeight)+'px');
 const leadHeight=Math.max(...cards.map(card=>card.querySelector('.card-body .lead').getBoundingClientRect().height));
 container.style.setProperty('--card-lead-height',Math.ceil(leadHeight)+'px');
 const previewHeight=Math.max(...cards.map(card=>card.querySelector('.preview').getBoundingClientRect().height));
 container.style.setProperty('--card-preview-height',Math.ceil(previewHeight)+'px');
}
requestAnimationFrame(alignCardIntroductions);
window.addEventListener('resize',alignCardIntroductions);
if(document.fonts)document.fonts.ready.then(alignCardIntroductions);
