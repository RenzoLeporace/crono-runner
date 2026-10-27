"""Small Android WebView bridge; desktop code never depends on Java APIs."""
import json
import base64
from pathlib import Path
import sys
_text_job=None
_file_jobs=[]

def encode_text(value):return base64.b64encode(value.encode('utf-8')).decode('ascii')
def decode_text(value):return base64.b64decode(str(value),validate=True).decode('utf-8')

def speak(value):
    native=bridge()
    return bool(native.speak(encode_text(value))) if native else False

def bridge():
    if sys.platform!='emscripten':return None
    try:
        import platform
        if str(platform.window.eval('typeof window.CronoAndroid'))=='undefined':return None
        value=platform.window.CronoAndroid
        return value if value else None
    except (AttributeError,ImportError):return None

def initialize():
    native=bridge()
    if not native:return
    import webbrowser
    webbrowser.open=lambda url,*args,**kwargs:native.openUrl(encode_text(url))
    root=Path(__file__).resolve().parents[1]
    raw=json.loads(str(native.loadFiles()))
    if not isinstance(raw,dict):return
    for relative,contents in raw.items():
        path=Path(relative)
        if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] not in ('saves','contenido') or not isinstance(contents,str):continue
        target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(contents,encoding='utf-8')

def persist(path):
    native=bridge()
    if not native:return
    root=Path(__file__).resolve().parents[1]
    try:
        relative=Path(path).resolve().relative_to(root).as_posix()
        result=native.saveFile(relative,encode_text(Path(path).read_text(encoding='utf-8')))
        if not result:raise OSError('Android no pudo conservar el archivo.')
    except ValueError:raise OSError('Ruta de guardado fuera de la aplicación.')


def ensure_file(path):
    """Fetch one private file on demand; archived banks stay on native storage."""
    native=bridge();path=Path(path)
    if not native or path.exists():return
    root=Path(__file__).resolve().parents[1]
    try:relative=path.resolve().relative_to(root).as_posix()
    except ValueError:return
    if not relative.startswith(('saves/','contenido/')):return
    contents=native.loadFile(relative)
    if contents is not None and str(contents):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(decode_text(contents),encoding='utf-8')

def delete(path):
    native=bridge()
    if not native:return
    root=Path(__file__).resolve().parents[1]
    try:native.deleteFile(Path(path).resolve().relative_to(root).as_posix())
    except ValueError:pass

def request_text(field):
    global _text_job
    if _text_job is not None:return
    native=bridge()
    if native:
        job=str(native.editText(encode_text(field.value),field.limit,field.multiline,getattr(field,'password',False)))
        _text_job=(job,field)

def poll_text():
    global _text_job
    if _text_job is None:return
    native=bridge()
    if not native:return
    job,field=_text_job;result=json.loads(str(native.poll(job)))
    if result.get('ready'):
        if isinstance(result.get('text'),str):field.set_value(result['text'][:field.limit])
        _text_job=None

def import_bank(callback):
    native=bridge()
    if not native:return False
    _file_jobs.append((str(native.pickQuestionBank()),callback));return True

def export_document(path,callback=None):
    native=bridge()
    if not native:return False
    path=Path(path);mime='text/csv' if path.suffix=='.csv' else 'application/json'
    _file_jobs.append((str(native.exportDocument(path.name,encode_text(path.read_text(encoding='utf-8')),mime)),callback))
    return True

def poll_files():
    if not _file_jobs:return
    native=bridge()
    if not native:return
    for job,callback in list(_file_jobs):
        result=json.loads(str(native.poll(job)))
        if result.get('ready'):
            _file_jobs.remove((job,callback))
            if callback:callback(result)

class NetworkFuture:
    """Java performs HTTP on a worker; Python polls without blocking a frame."""
    def __init__(self,client,operation,**data):
        self.client=client;self.operation=operation;self.response=None
        self.job=str(bridge().enqueue(json.dumps(dict(data,operation=operation,address=client.address,token=client.token))))
    def done(self):
        if self.response is None:
            response=json.loads(str(bridge().poll(self.job)))
            if response.get('ready'):self.response=response
        return self.response is not None
    def result(self):
        if not self.done():raise RuntimeError('La sala todavía está respondiendo.')
        if self.response.get('error'):raise OSError(self.response['error'])
        result=self.response['result']
        if self.operation=='join':
            self.client.token=result['token']
            return dict(joined_client=self.client,activity=result['activity'],rankings=result['rankings'])
        return dict(activity_update=result['activity'],rankings=result['rankings'])
