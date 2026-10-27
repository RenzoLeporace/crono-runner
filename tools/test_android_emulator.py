"""Small ADB harness locked to the disposable emulator, never a physical phone.

Examples (run only after the intended APK has been built):
  python tools/test_android_emulator.py --inspect
  python tools/test_android_emulator.py --apk build/android/CRONO-Beta-Educativa-0.9.3-Android.apk --install --fresh --offline --launch
  python tools/test_android_emulator.py --tap-ui 400 300 --capture menu-to-map
  python tools/test_android_emulator.py --hold-world 214 608 1600 --capture move-right
  python tools/test_android_emulator.py --wait 5 --logs

Coordinates are logical game units. UI is the central 1280x720 canvas; world
coordinates include the expanded viewport. A screenshot supplies the actual
landscape dimensions instead of assuming the emulator's portrait wm size.
"""
import argparse,hashlib,json,os,re,struct,subprocess,time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ADB=Path(os.environ.get('ANDROID_SDK_ROOT',str(Path.home()/'AppData'/'Local'/'Android'/'Sdk')))/'platform-tools'/'adb.exe'
SERIAL='emulator-5554'
PACKAGE='org.renzoleporace.crono'

def adb(*args,binary=False,timeout=30):
    command=[str(ADB),'-s',SERIAL,*map(str,args)]
    result=subprocess.run(command,capture_output=True,timeout=timeout)
    if result.returncode:
        raise RuntimeError('ADB command failed: '+result.stderr.decode('utf-8','replace')[:1200])
    return result.stdout if binary else result.stdout.decode('utf-8','replace').strip()

def verify_emulator():
    if adb('shell','getprop','ro.kernel.qemu')!='1':
        raise RuntimeError('Refusing access: target is not the expected Android emulator.')

def screen():
    data=adb('exec-out','screencap','-p',binary=True)
    if data[:8]!=b'\x89PNG\r\n\x1a\n':raise RuntimeError('Invalid screenshot')
    width,height=struct.unpack('>II',data[16:24])
    return data,width,height

def coordinates(x,y,ui=False):
    _,width,height=screen()
    if width<=height:raise RuntimeError('The game must be in landscape before using coordinates.')
    logical=max(960,min(2560,round(720*width/height)));scale=min(width/logical,height/720)
    if ui:
        ui_scale=min(1,logical/1280)
        x=x*ui_scale+(logical-1280*ui_scale)/2
        y=y*ui_scale+(720-720*ui_scale)/2
    return round((width-logical*scale)/2+x*scale),round((height-720*scale)/2+y*scale)

def inspect():
    _,width,height=screen()
    return dict(serial=SERIAL,model=adb('shell','getprop','ro.product.model'),
                android=adb('shell','getprop','ro.build.version.release'),api=adb('shell','getprop','ro.build.version.sdk'),
                abi=adb('shell','getprop','ro.product.cpu.abi'),image_fingerprint=adb('shell','getprop','ro.build.fingerprint'),
                screenshot_size=[width,height],wm_size=adb('shell','wm','size'),wm_density=adb('shell','wm','density'),
                webview=adb('shell','dumpsys','webviewupdate'),airplane_mode=adb('shell','settings','get','global','airplane_mode_on'))

def collect_logs(folder):
    log=adb('logcat','-d','-v','threadtime','CRONO:D','AndroidRuntime:E','chromium:E','*:S')
    (folder/'logcat.txt').write_text(log,encoding='utf-8')
    metrics=[]
    for row in log.splitlines():
        if 'CRONO_FRAME_STATS ' not in row:continue
        match=re.search(r'CRONO_FRAME_STATS (\{.*\})',row)
        if match:
            try:metrics.append(json.loads(match.group(1)))
            except json.JSONDecodeError:pass
    errors=[row for row in log.splitlines() if any(value in row for value in ('FATAL EXCEPTION','Traceback (most recent call last)','SyntaxError:','ModuleNotFoundError:','OutOfMemoryError'))]
    result=dict(samples=metrics,errors=errors)
    (folder/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'.test-tmp'/'android-emulator')
    parser.add_argument('--inspect',action='store_true');parser.add_argument('--apk',type=Path)
    parser.add_argument('--install',action='store_true');parser.add_argument('--fresh',action='store_true')
    parser.add_argument('--offline',action='store_true');parser.add_argument('--launch',action='store_true')
    parser.add_argument('--tap-ui',type=float,nargs=2);parser.add_argument('--hold-world',type=float,nargs=3)
    parser.add_argument('--key',type=int);parser.add_argument('--wait',type=float,default=0)
    parser.add_argument('--capture');parser.add_argument('--logs',action='store_true')
    args=parser.parse_args();verify_emulator();folder=args.output.resolve();folder.mkdir(parents=True,exist_ok=True)
    if args.install:
        if not args.apk or not args.apk.is_file():raise RuntimeError('Supply the built APK explicitly.')
        print(adb('install','-r',args.apk.resolve(),timeout=120))
        (folder/'apk-sha256.txt').write_text(hashlib.sha256(args.apk.read_bytes()).hexdigest()+'  '+args.apk.name+'\n',encoding='utf-8')
    if args.fresh:print(adb('shell','pm','clear',PACKAGE))
    if args.offline:
        adb('shell','cmd','connectivity','airplane-mode','enable');adb('shell','svc','wifi','disable');adb('shell','svc','data','disable')
    if args.launch:
        adb('shell','am','force-stop',PACKAGE);adb('logcat','-c')
        print(adb('shell','am','start','-n',PACKAGE+'/.MainActivity','--ez','crono_performance','true'))
    if args.tap_ui:
        x,y=coordinates(*args.tap_ui,ui=True);adb('shell','input','tap',x,y)
    if args.hold_world:
        x,y=coordinates(*args.hold_world[:2]);adb('shell','input','swipe',x,y,x,y,int(args.hold_world[2]))
    if args.key is not None:adb('shell','input','keyevent',args.key)
    if args.wait:time.sleep(min(60,max(0,args.wait)))
    if args.capture:
        if not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}',args.capture):raise RuntimeError('Use a plain capture name.')
        data,_,_=screen();(folder/(args.capture+'.png')).write_bytes(data)
    if args.inspect:
        result=inspect();(folder/'environment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
    if args.logs:print(json.dumps(collect_logs(folder),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
