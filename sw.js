/* Offline cache. Bump VERSION whenever app files change; content files are refreshed from the network when online. */
const VERSION='v1';
const CORE=['./','index.html','manifest.webmanifest','icons/icon.svg','icons/icon-180.png','icons/icon-192.png','icons/icon-512.png','content/index.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(VERSION).then(async c=>{await c.addAll(CORE);const idx=await (await fetch('content/index.json',{cache:'no-cache'})).json();await c.addAll(idx.sets.map(x=>'content/'+x.file))}).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==VERSION).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const r=e.request;if(r.method!=='GET')return;
  const u=new URL(r.url);
  const fresh=u.origin===location.origin&&(u.pathname.includes('/content/')||r.mode==='navigate'||u.pathname.endsWith('index.html'));
  if(fresh){ // network first, fall back to cache
    e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(VERSION).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r).then(m=>m||caches.match('index.html'))));
  }else{ // cache first (fonts, icons)
    e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==='opaque'){const cp=res.clone();caches.open(VERSION).then(c=>c.put(r,cp))}return res})));
  }
});
