"""Build the standalone beta using the project-local packaging toolchain."""
import os
from pathlib import Path
import subprocess
import sys
import shutil

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.vendor'))
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
import pygame as pg
from PIL import Image
sys.path.insert(0,str(ROOT))
from crono.art import clock_icon, CYAN, INK

pg.init()
image=pg.Surface((256,256),pg.SRCALPHA)
pg.draw.rect(image,INK,(0,0,256,256),border_radius=48)
clock_icon(image,128,128,88,CYAN,.8)
pg.image.save(image,str(ROOT/'tools'/'crono.png'))
Image.open(ROOT/'tools'/'crono.png').save(ROOT/'tools'/'crono.ico',sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
pg.quit()
env=os.environ.copy()
env['PYTHONPATH']=str(ROOT/'.build-tools')+os.pathsep+str(ROOT/'.vendor')
env['PYINSTALLER_CONFIG_DIR']=str(ROOT/'build'/'cache')
debug=os.environ.get('CRONO_BUILD_DEBUG')=='1'
args=[sys.executable,'-m','PyInstaller','--noconfirm','--onedir','--console' if debug else '--windowed',
      '--name','CRONO-Debug' if debug else 'CRONO - Ecos del tiempo','--icon',str(ROOT/'tools'/'crono.ico'),
      '--distpath',str(ROOT/'build'/'debug') if debug else str(ROOT/'build'/'release'),'--workpath',str(ROOT/'build'/'work'),
      '--specpath',str(ROOT/'build'),'--paths',str(ROOT/'.vendor'),
      '--add-data',str(ROOT/'licencias')+os.pathsep+'licencias',
      '--add-data',str(ROOT/'assets')+os.pathsep+'assets']
for module in ('numpy','PIL','matplotlib','tkinter','pandas','IPython','pytest','scipy'):
    args.extend(['--exclude-module',module])
args.append(str(ROOT/'Main.py'))
subprocess.run(args,cwd=ROOT,env=env,check=True)
if not debug:
    release=ROOT/'build'/'release'/'CRONO - Ecos del tiempo'
    shutil.copytree(release/'_internal',ROOT/'_internal',dirs_exist_ok=True)
    shutil.copy2(release/'CRONO - Ecos del tiempo.exe',ROOT/'CRONO - Ecos del tiempo.exe')
    print('Portable release copied to project root.')
