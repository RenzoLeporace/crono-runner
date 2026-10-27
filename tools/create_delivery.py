"""Keep the user's fixed delivery structure: Proyecto / Windows / APK."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
DELIVERY=ROOT/'Entrega'
VERSION='0.9.3'
APK_VERSION='0.9.3'

def inside(path):
    path=path.resolve()
    if not path.is_relative_to(DELIVERY.resolve()) or path==DELIVERY.resolve():
        raise ValueError('Delivery cleanup must remain inside Entrega.')
    return path

def remove(path):
    path=inside(path)
    if path.is_dir():shutil.rmtree(path)
    elif path.exists():path.unlink()

def main():
    DELIVERY.mkdir(exist_ok=True)
    for name in ('Proyecto','Windows','APK'):(DELIVERY/name).mkdir(exist_ok=True)
    # These are known generated outputs from previous delivery layouts.
    for name in ('Android','iOS','LEEME.txt','CHECKSUMS.json'):remove(DELIVERY/name)
    tracked=set(filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode('utf-8').split('\0')))
    old=set(filter(None,subprocess.check_output(['git','ls-tree','-r','--name-only','-z','HEAD'],cwd=ROOT).decode('utf-8').split('\0')))
    for relative in old-tracked:
        target=DELIVERY/'Proyecto'/relative
        if target.is_file():remove(target)
    for relative in tracked:
        source=ROOT/relative
        if source.is_file():
            target=DELIVERY/'Proyecto'/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    archive=ROOT/f'CRONO-Beta-Educativa-{VERSION}-Windows.zip'
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        allowed=set(z.namelist())
        for name in allowed:inside(DELIVERY/'Windows'/name)
        for path in (DELIVERY/'Windows').rglob('*'):
            if not path.is_file():continue
            relative=path.relative_to(DELIVERY/'Windows')
            # Existing local player data belongs to the user, not the package.
            if relative.parts[0] in ('saves','docente','capturas'):continue
            if relative.as_posix() not in allowed:remove(path)
        z.extractall(DELIVERY/'Windows')
    apk=ROOT/f'build/android/CRONO-Beta-Educativa-{APK_VERSION}-Android.apk'
    for previous in (DELIVERY/'APK').glob('*.apk'):
        if previous.name!=apk.name:remove(previous)
    shutil.copy2(apk,DELIVERY/'APK'/apk.name)
    for folder,files in (('Windows',(DELIVERY/'Windows'/'CRONO - Ecos del tiempo.exe',archive)),('APK',(apk,))):
        checks={p.name:dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in files}
        (DELIVERY/folder/'SHA256.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    assert {p.name for p in DELIVERY.iterdir()}=={'Proyecto','Windows','APK'}
    print('Delivery ready: Proyecto / Windows / APK.')

if __name__=='__main__':main()
