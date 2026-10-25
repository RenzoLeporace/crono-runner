"""Export the iPhone/iPad web version. This does not create or sign an IPA."""
from pathlib import Path
import shutil
import json
import zipfile
ROOT=Path(__file__).resolve().parents[1]

def export():
    source=ROOT/'android/app/src/main/assets';target=ROOT/'.web-build/ios'
    shutil.copytree(source,target,dirs_exist_ok=True)
    shutil.copy2(ROOT/'web/pwa_bridge.js',target/'pwa-bridge.js')
    html=(target/'index.html').read_text(encoding='utf-8')
    html=html.replace('<head>','<head>\n<script src="./pwa-bridge.js"></script>\n<link rel="manifest" href="./manifest.webmanifest">\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n<link rel="apple-touch-icon" href="./favicon.png">')
    html+='''<style>dialog{border:1px solid #6de3d6;border-radius:14px;background:#132d3b;color:#eee9d5;width:min(650px,85vw);font:18px sans-serif}dialog input,dialog textarea{box-sizing:border-box;width:100%;font:20px sans-serif;margin-bottom:20px}dialog button{font:18px sans-serif;padding:14px;margin:6px}dialog::backdrop{background:#00101ad9}#crono-exit{position:fixed;inset:0;background:#102a38;color:#e6efd6;display:grid;place-items:center;font:24px sans-serif;z-index:100}</style>'''
    (target/'index.html').write_text(html,encoding='utf-8')
    (target/'manifest.webmanifest').write_text(json.dumps(dict(name='CRONO · Ecos del tiempo',short_name='CRONO',start_url='./',scope='./',display='standalone',orientation='landscape',background_color='#102a38',theme_color='#102a38',icons=[dict(src='./favicon.png',sizes='any',type='image/png')]),ensure_ascii=False),encoding='utf-8')
    for name in ('COPYRIGHT.txt','LICENCIAS.txt'):
        shutil.copy2(ROOT/name,target/name)
    shutil.copy2(ROOT/'docs/IOS-WEB.md',target/'LEEME-iOS.md')
    shutil.copytree(ROOT/'licencias',target/'licencias',dirs_exist_ok=True)
    paths=['./'+p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file() and p.name!='service-worker.js']
    sw='const CACHE="crono-0.8-1";const FILES='+json.dumps(paths)+';\n'
    sw+='self.addEventListener("install",e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));\n'
    sw+='self.addEventListener("activate",e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));\n'
    sw+='self.addEventListener("fetch",e=>{if(e.request.method==="GET"&&new URL(e.request.url).origin===self.location.origin)e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||(new URL(e.request.url).pathname===new URL("./",self.location).pathname?caches.match(new URL("./index.html",self.location).href):null)).then(r=>r||fetch(e.request)));});'
    (target/'service-worker.js').write_text(sw,encoding='utf-8')
    release=ROOT/'build/ios';release.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(release/'CRONO-Beta-Educativa-0.8-iOS-Web.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for p in target.rglob('*'):
            if p.is_file():archive.write(p,p.relative_to(target))
    # The portable Windows game can host these public assets on the local WiFi.
    shutil.copytree(target,ROOT/'iOS-Web',dirs_exist_ok=True)
    print('iOS web version exported. HTTPS is required for offline service-worker installation; no IPA was generated.')

if __name__=='__main__':export()
