"""Stage the actual game and its offline WebAssembly runtime for Android.

This creates web assets, not an Android APK. build_android.py performs the
separate Android packaging and signing step after functional checks are complete.
"""
import hashlib
import json
import re
import os
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.android-build';APP=WORK/'webapp';RUNTIME=WORK/'runtime'
PYGBAG_VERSION='0.9.3'
FILES=('pythons.js','cpythonrc.py','empty.ogg','cpython312/main.js','cpython312/main.wasm','cpython312/main.data')
WHEEL='pygame_ce-2.5.7-cp312-cp312-wasm32_bi_emscripten.whl'

def download(relative,url):
    target=RUNTIME/relative;target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        with urlopen(url,timeout=60) as source,target.open('wb') as output:shutil.copyfileobj(source,output)
    return target

def prepare():
    APP.mkdir(parents=True,exist_ok=True);RUNTIME.mkdir(parents=True,exist_ok=True)
    for relative in FILES:download(relative,'https://pygame-web.github.io/cdn/0.9.3/'+relative)
    download('index-0.9.3-cp312.json','https://pygame-web.github.io/cdn/index-0.9.3-cp312.json')
    download('cp312/'+WHEEL,'https://pygame-web.github.io/cdn/cp312/'+WHEEL)
    shutil.copy2(ROOT/'android'/'main.py',APP/'main.py')
    staged=APP/'crono'
    if staged.exists():
        for old in staged.rglob('*.py'):
            if not (ROOT/'crono'/old.relative_to(staged)).is_file():old.unlink()
    shutil.copytree(ROOT/'crono',staged,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copytree(ROOT/'licencias',APP/'licencias',dirs_exist_ok=True)
    shutil.copytree(ROOT/'assets',APP/'assets',dirs_exist_ok=True)
    for filename in ('COPYRIGHT.txt','LICENCIAS.txt','FUENTES.md'):shutil.copy2(ROOT/filename,APP/filename)
    env=os.environ.copy();env['PYTHONPATH']=str(WORK/'toolchain');env['PYTHONUTF8']='1'
    subprocess.run([sys.executable,'-m','pygbag','--build','--no_opt','--disable-sound-format-error','--ume_block','0','--title','CRONO · Ecos del tiempo',str(APP)],env=env,cwd=ROOT,check=True)
    output=APP/'build'/'web';assets=ROOT/'android'/'app'/'src'/'main'/'assets'
    assets.mkdir(parents=True,exist_ok=True)
    for filename in ('webapp.tar.gz','favicon.png'):shutil.copy2(output/filename,assets/filename)
    unused=assets/'webapp.apk'
    if unused.exists():unused.unlink()
    html=(output/'index.html').read_text(encoding='utf-8')
    start=html.index("    if platform.window.location.host.find('.itch.zone')>0:")
    end=html.index('    # preloader',start)
    html=html[:start]+'''    import tarfile
    async with platform.fopen("webapp.tar.gz", "rb") as archive:
        tar = tarfile.open(fileobj=archive, mode="r:gz")
        tar.extractall(path=appdir.as_posix(), filter='tar')
        tar.close()

'''+html[end:]
    html=html.replace('https://pygame-web.github.io/cdn/0.9.3/','./runtime/').replace('data-os="vtx,snd,gui"','data-os="snd,gui"')
    html='\n'.join(row for row in html.splitlines() if 'browserfs.min.js' not in row)
    html=html.replace('Ready to start ! Please click/touch page','CRONO · Toca para comenzar')
    html=html.replace('background-color:powderblue','background-color:#0d1b25').replace('background: green','background: #193b49').replace('color: blue','color: #b4f3e9')
    html=html.replace('Loading, please wait','Cargando CRONO… / Carregando CRONO…')
    html=re.sub(r'<meta name="viewport"[^>]*>','',html)
    html=html.replace('<head>','<head><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">')
    html+='\n<style>html,body{margin:0;padding:0;overflow:hidden;touch-action:none;background:#102a38}#canvas{touch-action:none;position:fixed!important;inset:0!important;width:100vw!important;height:100dvh!important;max-width:none!important;max-height:none!important}#infobox{font:20px sans-serif;border-radius:12px}#html{display:none}#crono-rotate{display:none}@media(orientation:portrait){#crono-rotate{display:grid;position:fixed;inset:0;place-items:center;background:#102a38;color:#e4edda;font:24px sans-serif;z-index:90}}</style><div id="crono-rotate">Gira el dispositivo para explorar en horizontal.<br>Gire o dispositivo para jogar na horizontal.</div>'
    (assets/'index.html').write_text(html,encoding='utf-8')
    for relative in FILES+('index-0.9.3-cp312.json','cp312/'+WHEEL):
        target=assets/'runtime'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(RUNTIME/relative,target)
    (assets/'runtime'/'empty.html').write_text('<!doctype html><html><head><meta charset="utf-8"></head><body></body></html>',encoding='utf-8')
    rc=assets/'runtime'/'cpythonrc.py'
    source=rc.read_text(encoding='utf-8')
    source=source.replace('import aio.toplevel','import os\n    # CRONO offline distribution: all package resources stay in this APK.\n    os.environ["PYGPI"] = str(platform.window.location.origin) + "/runtime/"\n    import aio.toplevel',1)
    rc.write_text(source,encoding='utf-8')
    manifest={p.relative_to(assets).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in assets.rglob('*') if p.is_file()}
    (WORK/'assets-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'Offline Android assets: {sum(p.stat().st_size for p in assets.rglob("*") if p.is_file())/1024/1024:.1f} MiB. No APK has been compiled.')

if __name__=='__main__':prepare()
