"""Build the browser version of CRONO for GitHub Pages or any static host.

Stages the game like tools/prepare_android.py, packs it with pygbag and keeps the
WebAssembly runtime next to the page, so the site does not depend on a CDN.
Saved games stay in the browser (IndexedDB) through web/crono-web.js.

    python -m pip install pygbag==0.9.3
    python tools/build_web.py            # result: .web-build/sitio
    python tools/build_web.py --servir   # also serves it at http://127.0.0.1:8000
"""
import argparse
import functools
import hashlib
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.web-build';APP=WORK/'webapp';RUNTIME=WORK/'runtime';SITE=WORK/'sitio'
PYGBAG_VERSION='0.9.3'
CDN=f'https://pygame-web.github.io/cdn/{PYGBAG_VERSION}/'
FILES=('pythons.js','cpythonrc.py','empty.ogg','cpython312/main.js','cpython312/main.wasm','cpython312/main.data')
WHEEL='pygame_ce-2.5.7-cp312-cp312-wasm32_bi_emscripten.whl'
TITLE='CRONO · Ecos del tiempo'
DESCRIPTION='Juego educativo de plataformas para viajar por la historia. Jugá en el navegador, sin instalar nada.'

def download(relative,url):
    target=RUNTIME/relative;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        with urlopen(url,timeout=120) as source,target.open('wb') as output:shutil.copyfileobj(source,output)
    return target

def stage():
    """Copy the game exactly as the Android build does, with the browser entry point."""
    if APP.exists():shutil.rmtree(APP)
    APP.mkdir(parents=True)
    shutil.copy2(ROOT/'web'/'main.py',APP/'main.py')
    shutil.copytree(ROOT/'crono',APP/'crono',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copytree(ROOT/'licencias',APP/'licencias')
    shutil.copytree(ROOT/'assets',APP/'assets')
    for filename in ('COPYRIGHT.txt','LICENCIAS.txt','FUENTES.md'):shutil.copy2(ROOT/filename,APP/filename)

def customize(html):
    """Adapt pygbag's page: local runtime, CRONO colors, bridge script and phone layout."""
    html=html.replace(CDN,'./runtime/').replace('<html lang="en-us">','<html lang="es">',1)
    html=html.replace('data-os="vtx,snd,gui"','data-os="snd,gui"')
    html='\n'.join(row for row in html.splitlines() if 'browserfs.min.js' not in row)
    html=html.replace('Ready to start ! Please click/touch page','CRONO · Hacé clic o tocá para comenzar')
    html=html.replace('Loading, please wait','Cargando CRONO… / Carregando CRONO…')
    html=html.replace('platform.document.body.style.background = "#7f7f7f"','platform.document.body.style.background = "#102a38"')
    html=html.replace('background-color:powderblue','background-color:#0d1b25').replace('background: green','background: #193b49').replace('color: blue','color: #b4f3e9')
    html=re.sub(r'<title>.*?</title>',f'<title>{TITLE}</title>',html,count=1,flags=re.S)
    html=re.sub(r'<meta name="viewport"[^>]*>','',html)
    head=('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
          f'<meta name="description" content="{DESCRIPTION}">'
          f'<meta property="og:title" content="{TITLE}"><meta property="og:description" content="{DESCRIPTION}">'
          '<meta name="theme-color" content="#0d1b25"><link rel="stylesheet" href="crono-web.css">'
          '<script src="crono-web.js"></script>')
    html=html.replace('<head>','<head>'+head,1)
    html=html.replace('</body>','<div id="crono-rotate">Girá el dispositivo para jugar en horizontal.<br>Gire o dispositivo para jogar na horizontal.</div></body>',1)
    return html

def build():
    for relative in FILES:download(relative,CDN+relative)
    download(f'index-{PYGBAG_VERSION}-cp312.json',f'https://pygame-web.github.io/cdn/index-{PYGBAG_VERSION}-cp312.json')
    download('cp312/'+WHEEL,'https://pygame-web.github.io/cdn/cp312/'+WHEEL)
    stage()
    env=os.environ.copy();env['PYTHONUTF8']='1'
    subprocess.run([sys.executable,'-m','pygbag','--build','--no_opt','--disable-sound-format-error','--ume_block','0','--title',TITLE,str(APP)],env=env,cwd=ROOT,check=True)
    output=APP/'build'/'web'
    if SITE.exists():shutil.rmtree(SITE)
    # Fuera de itch.io, el cargador de pygbag usa webapp.tar.gz: el .apk sería un duplicado.
    shutil.copytree(output,SITE,ignore=shutil.ignore_patterns('*.apk'))
    for filename in ('crono-web.js','crono-web.css'):shutil.copy2(ROOT/'web'/filename,SITE/filename)
    shutil.copy2(ROOT/'tools'/'crono.png',SITE/'favicon.png')
    (SITE/'index.html').write_text(customize((output/'index.html').read_text(encoding='utf-8')),encoding='utf-8')
    for relative in FILES+(f'index-{PYGBAG_VERSION}-cp312.json','cp312/'+WHEEL):
        target=SITE/'runtime'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(RUNTIME/relative,target)
    (SITE/'runtime'/'empty.html').write_text('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>',encoding='utf-8')
    rc=SITE/'runtime'/'cpythonrc.py'
    source=rc.read_text(encoding='utf-8')
    marker='import aio.toplevel'
    if marker not in source:raise SystemExit('cpythonrc.py cambió: revisar dónde fijar PYGPI.')
    # pygame se instala desde ./runtime/ y no desde el CDN de pygbag.
    rc.write_text(source.replace(marker,'import os\n    os.environ["PYGPI"] = str(platform.window.location.href).split("?")[0].rsplit("/", 1)[0] + "/runtime/"\n    '+marker,1),encoding='utf-8')
    (SITE/'.nojekyll').write_text('',encoding='utf-8')
    manifest={p.relative_to(SITE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SITE.rglob('*')) if p.is_file()}
    (WORK/'sitio-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    size=sum(p.stat().st_size for p in SITE.rglob('*') if p.is_file())/1024/1024
    print(f'Versión web lista en {SITE.relative_to(ROOT).as_posix()}: {size:.1f} MiB.')

def serve(port):
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(SITE))
    print(f'Sirviendo http://127.0.0.1:{port}/ (Ctrl+C para salir)')
    http.server.ThreadingHTTPServer(('127.0.0.1',port),handler).serve_forever()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--servir',action='store_true',help='servir el sitio al terminar')
    parser.add_argument('--puerto',type=int,default=8000)
    args=parser.parse_args()
    build()
    if args.servir:serve(args.puerto)
