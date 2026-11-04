"""Smoke-test the portable executable and package only distributable files."""
from pathlib import Path
import subprocess
import time
import zipfile

ROOT=Path(__file__).resolve().parents[1]
exe=ROOT/'CRONO - Ecos del tiempo.exe'
out=ROOT/'capturas'/'educativa-0.9.3'/'ejecutable'
out.mkdir(parents=True,exist_ok=True)
# Focused executable checks for this release's changed screens and routes.
for scene,era,stage in (('menu',1,1),('dlc_menu',13,1),('skins',1,1),('workshop',1,1),
                        ('play',2,1),('voyage',1,1),('voyage',10,3),('story',13,2),
                        ('play',13,1),('play',13,2),('play',13,3),('play',14,1),
                        ('play',14,2),('play',14,3),('play',15,1),('play',15,2),('play',15,3),('play',16,1),('teacher',13,1),
                        ('intro',1,1),('activity',1,1),('quiz',1,1),('help',1,1),('boss',1,3)):
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

# Exercise the packaged locale asset, both question layouts and new war routes.
for language in ('es','pt-BR'):
    for scene,era,stage,touch in (('language_settings',1,1,False),('quiz',1,1,False),('quiz',1,1,True),
                                ('play',16,2,True),('play',17,1,True),('play',12,3,True)):
        path=out/f'{language}-{scene}-{era}-{stage}-{int(touch)}.png'
        command=[str(exe),'--headless','--scene',scene,'--era',str(era),'--map',str(stage),
                 '--capture',str(path),'--language',language]
        if touch:command.extend(['--touch','--aspect','2.2222222222'])
        result=subprocess.run(command,cwd=ROOT,timeout=40)
        if result.returncode or not path.exists() or path.stat().st_size<1000:
            raise RuntimeError(f'Locale executable check failed: {language}, {scene}')
        print(f'{language}/{scene}/{era}.{stage}: exit 0, locale and PNG checked',flush=True)

files=[exe,*[ROOT/name for name in ('Jugar.bat','README.md','CHANGELOG.md','FUENTES.md','LICENCIAS.txt','COPYRIGHT.txt','docs/GUIA-DOCENTE.md','docs/IDIOMAS.md','docs/HOJA-DE-RUTA.md')],
       ROOT/'contenido'/'LEEME.txt']
for folder in ('_internal','licencias'):
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
target=ROOT/'CRONO-Beta-Educativa-0.9.3-Windows.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for path in files:
        archive.write(path,path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None
    names=archive.namelist()
    assert exe.name in names and '_internal/python312.dll' in names
    assert not any(n.startswith('saves/') or n.endswith('preguntas.json') for n in names)
print(f'ZIP checked: {len(names)} files, {target.stat().st_size/1024/1024:.1f} MiB')
