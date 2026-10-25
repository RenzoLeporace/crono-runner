/* Offline-capable browser storage and input. No external account or tracker. */
(() => {
  if (window.CronoAndroid) return;
  window.CronoWebReady = false;
  const files = new Map(), jobs = new Map(); let database, pending = 0;
  const enc = s => {
    const bytes = new TextEncoder().encode(s); let value = '';
    for (let n = 0; n < bytes.length; n += 8192) value += String.fromCharCode(...bytes.subarray(n, n + 8192));
    return btoa(value);
  };
  const dec = s => new TextDecoder().decode(Uint8Array.from(atob(s), c => c.charCodeAt(0)));
  const ascii = obj => JSON.stringify(obj).replace(/[\u007f-\uffff]/g, c => '\\u' + c.charCodeAt(0).toString(16).padStart(4,'0'));
  const valid = p => typeof p === 'string' && /^(saves|contenido)\//.test(p) && !p.split('/').includes('..');
  const job = () => { const id = crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random(); jobs.set(id,{ready:false}); return id; };
  function write(path, text, remove=false) {
    if (!valid(path) || !database || text.length > 32*1024*1024) return false;
    const tx = database.transaction('files','readwrite'); pending++;
    if (remove) tx.objectStore('files').delete(path); else tx.objectStore('files').put(text,path);
    tx.oncomplete = () => { pending--; };
    tx.onerror = () => { pending--; window.CronoWebStorageError = 'No se pudo conservar el último cambio. Exporta tus datos y revisa el espacio del navegador.'; };
    return true;
  }
  const bridge = {
    loadFiles: () => ascii(Object.fromEntries(['saves/perfiles.json','saves/docente.json'].filter(p => files.has(p)).map(p => [p,files.get(p)]))),
    loadFile: p => files.has(p) ? enc(files.get(p)) : null,
    saveFile: (p,b64) => { try { const text=dec(b64); if(!write(p,text))return false;files.set(p,text);return true; } catch{return false;} },
    deleteFile: p => { if(!write(p,'',true))return false;files.delete(p);return true; },
    openUrl: b64 => { const url=dec(b64);if(url.startsWith('https://'))window.open(url,'_blank','noopener'); },
    poll: id => { const result=jobs.get(id)||{ready:true,error:'Solicitud desconocida'};if(result.ready)jobs.delete(id);return ascii(result); },
    enqueue: () => { const id=job();jobs.set(id,{ready:true,error:'Las salas LAN están disponibles en Windows y Android. Esta versión web permite jugar y guardar de forma individual.'});return id; },
    editText: (initial,limit,multiline,password) => {
      const id=job(), dialog=document.createElement('dialog'), title=document.createElement('h2');title.textContent='CRONO · Escribir';
      const input=document.createElement(multiline?'textarea':'input');input.value=dec(initial);input.maxLength=limit;
      if(password)input.type='password';
      const accept=document.createElement('button'),cancel=document.createElement('button');accept.textContent='Aceptar';cancel.textContent='Cancelar';
      const finish = result => { jobs.set(id,{ready:true,...result});dialog.close();dialog.remove();document.querySelector('#canvas')?.focus(); };
      accept.onclick=()=>finish({text:input.value});cancel.onclick=()=>finish({});dialog.oncancel=e=>{e.preventDefault();finish({});};
      dialog.append(title,input,accept,cancel);document.body.append(dialog);dialog.showModal();input.focus();input.select();return id;
    },
    pickQuestionBank: () => {
      const id=job(),input=document.createElement('input');input.type='file';input.accept='.json,application/json';
      input.onchange=async()=>{const file=input.files[0];if(!file){jobs.set(id,{ready:true});return;}jobs.set(id,file.size>4000000?{ready:true,error:'El banco supera 4 MB.'}:{ready:true,text:await file.text()});};
      input.oncancel=()=>jobs.set(id,{ready:true});input.click();return id;
    },
    exportDocument: (name,b64,mime) => {
      const id=job(),url=URL.createObjectURL(new Blob([dec(b64)],{type:mime+';charset=utf-8'})),link=document.createElement('a');
      link.href=url;link.download=name;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);jobs.set(id,{ready:true,saved:true});return id;
    },
    finishGame: () => { const timer=setInterval(()=>{if(!pending){clearInterval(timer);document.body.insertAdjacentHTML('beforeend','<div id="crono-exit">Partida guardada. Puedes cerrar esta ventana.</div>');}},50); }
  };
  window.CronoAndroid=bridge;
  const request=indexedDB.open('crono-educativo',1);
  request.onupgradeneeded=()=>request.result.createObjectStore('files');
  request.onerror=()=>{
    window.CronoWebStorageError='No se pudo abrir el guardado del navegador.';
    const message=()=>document.body.insertAdjacentHTML('beforeend','<div id="crono-exit">Activa el almacenamiento del navegador para guardar tu viaje y vuelve a abrir CRONO.</div>');
    if(document.body)message();else document.addEventListener('DOMContentLoaded',message,{once:true});
  };
  request.onsuccess=()=>{
    database=request.result;const cursor=database.transaction('files').objectStore('files').openCursor();
    cursor.onsuccess=()=>{const row=cursor.result;if(row){if(!row.key.includes('/respaldos/'))files.set(row.key,row.value);row.continue();}else window.CronoWebReady=true;};
  };
  if('serviceWorker' in navigator && window.isSecureContext) navigator.serviceWorker.register('./service-worker.js').catch(()=>{});
})();
