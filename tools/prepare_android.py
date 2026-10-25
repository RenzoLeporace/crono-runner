"""Stage the actual game and its offline WebAssembly runtime for Android.

This creates web assets, not an Android APK. build_android.py performs the
separate Android packaging and signing step after source audits are complete.
"""
import hashlib
import json
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
    shutil.copytree(ROOT/'crono',APP/'crono',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    shutil.copytree(ROOT/'licencias',APP/'licencias',dirs_exist_ok=True)
    for filename in ('COPYRIGHT.txt','LICENCIAS.txt','FUENTES.md'):shutil.copy2(ROOT/filename,APP/filename)
    env=os.environ.copy();env['PYTHONPATH']=str(WORK/'toolchain');env['PYTHONUTF8']='1'
    subprocess.run([sys.executable,'-m','pygbag','--build','--no_opt','--ume_block','0','--title','CRONO · Ecos del tiempo',str(APP)],env=env,cwd=ROOT,check=True)
    output=APP/'build'/'web';assets=ROOT/'android'/'app'/'src'/'main'/'assets'
    assets.mkdir(parents=True,exist_ok=True)
    for filename in ('webapp.tar.gz','webapp.apk','favicon.png'):shutil.copy2(output/filename,assets/filename)
    html=(output/'index.html').read_text(encoding='utf-8')
    html=html.replace('https://pygame-web.github.io/cdn/0.9.3/','./runtime/').replace('data-os="vtx,snd,gui"','data-os="snd,gui"')
    html='\n'.join(row for row in html.splitlines() if 'browserfs.min.js' not in row)
    html=html.replace('Ready to start ! Please click/touch page','CRONO · Toca para comenzar')
    html=html.replace('background-color:powderblue','background-color:#0d1b25').replace('background: green','background: #193b49').replace('color: blue','color: #b4f3e9')
    html=html.replace('Loading, please wait','Cargando CRONO…')
    html+='\n<style>html,body{overflow:hidden;touch-action:none}#canvas{touch-action:none}#infobox{font:20px sans-serif;border-radius:12px}#html{display:none}</style>'
    (assets/'index.html').write_text(html,encoding='utf-8')
    for relative in FILES+('index-0.9.3-cp312.json','cp312/'+WHEEL):
        target=assets/'runtime'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(RUNTIME/relative,target)
    rc=assets/'runtime'/'cpythonrc.py'
    source=rc.read_text(encoding='utf-8')
    source=source.replace('import aio.toplevel','import os\n    # CRONO offline distribution: all package resources stay in this APK.\n    os.environ["PYGPI"] = str(platform.window.location.origin) + "/runtime/"\n    import aio.toplevel',1)
    rc.write_text(source,encoding='utf-8')
    manifest={p.relative_to(assets).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in assets.rglob('*') if p.is_file()}
    (WORK/'assets-sha256.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'Offline Android assets: {sum(p.stat().st_size for p in assets.rglob("*") if p.is_file())/1024/1024:.1f} MiB. No APK has been compiled.')

if __name__=='__main__':prepare()
