// Preview-only local selection. No upload, storage or payment until TA-Next is wired.
const intake=document.querySelector('[data-photo-intake]');
if(intake){
 const objectFields=intake.querySelector('[data-object-fields]');
 intake.elements.package.addEventListener('change',()=>{const object=intake.elements.package.value==='photoshoot_object_45';objectFields.hidden=!object;for(const el of objectFields.querySelectorAll('input,select'))el.disabled=!object;});
 for(const el of objectFields.querySelectorAll('input,select'))el.disabled=true;
 intake.addEventListener('submit',e=>e.preventDefault());
 intake.addEventListener('change',()=>{
  const files=[...intake.querySelectorAll('input[type=file]:not(:disabled)')].flatMap(el=>[...el.files]);let message='';
  if(files.some(f=>f.size>20*1024*1024))message=intake.dataset.tooLarge;
  else if(files.some(f=>!['image/jpeg','image/png','image/webp'].includes(f.type)))message=intake.dataset.fileType;
  else if(intake.elements.source.files.length<6)message=intake.dataset.sourceCount;
  intake.querySelector('[data-intake-status]').textContent=message;
 });
}
