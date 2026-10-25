"""Build, align, sign and verify a real Android APK with the local SDK/JDK."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.android-build';SOURCE=ROOT/'android'/'app'/'src'/'main'
SDK=Path(os.environ.get('ANDROID_SDK_ROOT',str(Path.home()/'AppData'/'Local'/'Android'/'Sdk')))
JDK=Path(os.environ.get('JAVA_HOME','C:/Program Files/Eclipse Adoptium/jdk-17.0.20.101-hotspot'))
TOOLS=SDK/'build-tools'/'34.0.0';ANDROID=SDK/'platforms'/'android-34'/'android.jar'

def run(args,cwd=ROOT):
    env=os.environ.copy();env['JAVA_HOME']=str(JDK);env['PATH']=str(JDK/'bin')+os.pathsep+env.get('PATH','')
    result=subprocess.run([str(a) for a in args],cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.stdout.strip():print(result.stdout.strip())
    if result.stderr.strip():print(result.stderr.strip())
    result.check_returncode()

def build():
    assets=SOURCE/'assets'
    if not (assets/'runtime'/'cpython312'/'main.wasm').is_file():raise SystemExit('Run tools/prepare_android.py first.')
    classes=WORK/'classes';dex=WORK/'dex';release=ROOT/'build'/'android'
    for directory in (classes,dex,release,SOURCE/'res'/'drawable'):directory.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'tools'/'crono.png',SOURCE/'res'/'drawable'/'icon.png')
    java=SOURCE/'java'/'org'/'renzoleporace'/'crono'/'MainActivity.java'
    run([JDK/'bin'/'javac.exe','-encoding','UTF-8','--release','8','-classpath',ANDROID,'-d',classes,java])
    run([TOOLS/'d8.bat','--release','--lib',ANDROID,'--min-api','26','--output',dex,*classes.rglob('*.class')])
    unsigned=WORK/'crono-unsigned.apk';aligned=WORK/'crono-aligned.apk';target=release/'CRONO-Beta-Educativa-0.9.1-Android.apk'
    run([TOOLS/'aapt.exe','package','-f','-0','gz','-M',SOURCE/'AndroidManifest.xml','-S',SOURCE/'res','-A',assets,'-I',ANDROID,'-F',unsigned])
    # aapt transparently expands .gz assets and removes the suffix. The Python
    # loader requests the original gzip, so add it explicitly after packaging.
    run([TOOLS/'aapt.exe','remove',unsigned,'assets/webapp.tar'])
    with zipfile.ZipFile(unsigned,'a',zipfile.ZIP_DEFLATED) as archive:
        archive.write(assets/'webapp.tar.gz','assets/webapp.tar.gz')
    run([TOOLS/'aapt.exe','add',unsigned,'classes.dex'],cwd=dex)
    run([TOOLS/'zipalign.exe','-f','4',unsigned,aligned])
    keystore=WORK/'crono-beta.keystore'
    if not keystore.exists():
        run([JDK/'bin'/'keytool.exe','-genkeypair','-keystore',keystore,'-storepass','android','-keypass','android',
            '-alias','crono-beta','-keyalg','RSA','-keysize','2048','-validity','10000','-dname','CN=Renzo Leporace, OU=CRONO Beta, O=Renzo Leporace, C=AR'])
    run([TOOLS/'apksigner.bat','sign','--ks',keystore,'--ks-pass','pass:android','--ks-key-alias','crono-beta','--out',target,aligned])
    run([TOOLS/'apksigner.bat','verify','--verbose','--print-certs',target])
    run([TOOLS/'aapt.exe','dump','badging',target])
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:raise RuntimeError('APK archive integrity failure')
        for name in ('AndroidManifest.xml','classes.dex','assets/runtime/cpython312/main.wasm','assets/webapp.tar.gz'):
            if name not in archive.namelist():raise RuntimeError('APK missing '+name)
    print(f'Android APK verified: {target} ({target.stat().st_size/1024/1024:.1f} MiB)')

if __name__=='__main__':build()
