"""Smoke-test the portable executable and package only distributable files."""
from pathlib import Path
import subprocess
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
exe=ROOT/'CRONO - Ecos del tiempo.exe'
out=ROOT/'capturas'/'educativa-0.9.1'/'ejecutable'
out.mkdir(parents=True,exist_ok=True)
# Focused executable checks for this release's changed screens and routes.
for scene,era,stage in (('menu',1,1),('dlc_menu',13,1),('skins',1,1),('workshop',1,1),
                        ('play',2,1),('voyage',1,1),('voyage',10,3),('story',13,2),
                        ('play',13,1),('play',13,2),('play',13,3),('play',14,1),
                        ('play',14,2),('play',14,3),('play',15,1),('play',15,2),('play',15,3),('play',16,1),('teacher',13,1)):
    path=out/f'{scene}-{era}-{stage}.png'
    if path.exists():
        path.unlink()
    start=time.perf_counter()
    result=subprocess.run([str(exe),'--headless','--scene',scene,'--era',str(era),
                           '--map',str(stage),'--capture',str(path),
                           '--touch','--aspect','2.2222222222'],cwd=ROOT,timeout=40)
    if result.returncode or not path.exists() or path.stat().st_size<1000:
        raise RuntimeError(f'Executable smoke failed: {scene}, exit {result.returncode}')
    print(f'{scene}: exit 0, PNG {path.stat().st_size} bytes, {time.perf_counter()-start:.2f}s',flush=True)

files=[exe,*[ROOT/name for name in ('Jugar.bat','README.md','FUENTES.md','VERIFICACION.md','LICENCIAS.txt','COPYRIGHT.txt','docs/CAMBIOS-0.9.md','docs/CAMBIOS-0.9.1.md','docs/CAMBIOS-0.9.1-ANDROID.md','docs/GUIA-DOCENTE.md')],
       ROOT/'contenido'/'LEEME.txt']
for folder in ('_internal','licencias'):
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
target=ROOT/'CRONO-Beta-Educativa-0.9.1-Windows.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for path in files:
        archive.write(path,path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    names=archive.namelist()
    assert exe.name in names and '_internal/python312.dll' in names
    assert not any(n.startswith('saves/') or n.endswith('preguntas.json') for n in names)
print(f'ZIP checked: {len(names)} files, {target.stat().st_size/1024/1024:.1f} MiB')
