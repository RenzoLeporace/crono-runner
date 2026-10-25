"""Smoke-test the portable executable and package only distributable files."""
from pathlib import Path
import subprocess
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
exe=ROOT/'CRONO - Ecos del tiempo.exe'
out=ROOT/'capturas'/'educativa-0.7'/'ejecutable'
out.mkdir(parents=True,exist_ok=True)
for scene,era,stage in (('menu',1,1),('chapters',9,1),('settings',1,1),('teacher',9,1),('question_edit',9,1),
                        ('scenarios',8,1),('quiz',9,3),('boss',7,3),('atlas',6,2),('play',8,2),
                        ('boss',9,3),('play',9,1),('play',9,2),('heritage',8,1),('heritage',8,2),('heritage',9,3),
                        ('skins',1,1),('achievements',1,1),('community',1,1),('school_settings',1,1),
                        ('accessibility',1,1),('credits',1,1),('teacher_tools',9,3),('activity',10,3),
                        ('play',10,1),('play',10,2),('play',10,3),('play',11,1),('play',11,2),('play',11,3),
                        ('play',12,1),('play',12,2),('play',12,3)):
    path=out/f'{scene}-{era}-{stage}.png'
    if path.exists():
        path.unlink()
    start=time.perf_counter()
    result=subprocess.run([str(exe),'--headless','--scene',scene,'--era',str(era),
                           '--map',str(stage),'--capture',str(path)],cwd=ROOT,timeout=40)
    if result.returncode or not path.exists() or path.stat().st_size<1000:
        raise RuntimeError(f'Executable smoke failed: {scene}, exit {result.returncode}')
    print(f'{scene}: exit 0, PNG {path.stat().st_size} bytes, {time.perf_counter()-start:.2f}s',flush=True)

files=[exe,*[ROOT/name for name in ('Jugar.bat','README.md','FUENTES.md','VERIFICACION.md','LICENCIAS.txt','COPYRIGHT.txt','docs/AUDITORIA-0.7.md','docs/AUDITORIA-0.7-JUGABILIDAD.md','docs/AUDITORIA-0.7-SISTEMAS.md','docs/GUIA-DOCENTE.md')],
       ROOT/'contenido'/'LEEME.txt']
for folder in ('_internal','licencias','docs/imagenes'):
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
target=ROOT/'CRONO-Beta-Educativa-0.7-Windows.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for path in files:
        archive.write(path,path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    names=archive.namelist()
    assert exe.name in names and '_internal/python312.dll' in names
    assert not any(n.startswith('saves/') or n.endswith('preguntas.json') for n in names)
print(f'ZIP checked: {len(names)} files, {target.stat().st_size/1024/1024:.1f} MiB')
