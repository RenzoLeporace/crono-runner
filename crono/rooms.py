from .campaign import TOTAL_LEVELS
"""Teacher-hosted LAN rooms. No cloud, outbound discovery or firewall changes."""
import json
from pathlib import Path
import secrets
from .school import atomic_json,clean_label,rankings,valid_records

LIMIT=2_000_000
RESPONSE_LIMIT=8_000_000  # A teacher bank may contain up to 4 MB of UTF-8 JSON.

class Room:
    def __init__(self,path,bank=None,topics=None):
        import threading
        self.path=Path(path);self.lock=threading.RLock();self.server=None
        self.code=secrets.token_hex(3).upper();self.teacher_token=secrets.token_urlsafe(24)
        self.members={};self.bank=bank or [];self.topics=topics or [];self.name='Aula de Crono'
        self.warning=''
        try:
            raw=json.loads(self.path.read_text(encoding='utf-8'))
            members=raw.get('members',{})
            for key,value in members.items() if isinstance(members,dict) else []:
                if not isinstance(key,str) or not isinstance(value,dict):continue
                self.members[key]=dict(alias=clean_label(value.get('alias','Explorador')) or 'Explorador',
                    classroom=clean_label(value.get('classroom','')),institution=clean_label(value.get('institution','')),role='teacher' if value.get('role')=='teacher' else 'student',records=valid_records(value.get('records',{})))
        except (OSError,ValueError,AttributeError):pass

    def persist(self):atomic_json(self.path,dict(members=self.members))
    def request(self,route,body):
        if not isinstance(body,dict):raise ValueError('Solicitud inválida.')
        with self.lock:
            if route=='/join':
                code=str(body.get('code','')).strip().upper()
                if len(code)!=6 or any(c not in '0123456789ABCDEF' for c in code) or not secrets.compare_digest(code,self.code):raise PermissionError('Código incorrecto.')
                alias=clean_label(body.get('alias',''))
                if not alias:raise ValueError('Falta el alias.')
                token=body.get('token')
                if not isinstance(token,str) or token not in self.members:token=secrets.token_urlsafe(24)
                if len(self.members)>=200 and token not in self.members:raise ValueError('Sala completa (200 dispositivos).')
                old=self.members.get(token,{})
                self.members[token]=dict(alias=alias,classroom=clean_label(body.get('classroom','Mi clase')),
                    institution=clean_label(body.get('institution','Mi institución')),role='teacher' if body.get('role')=='teacher' else 'student',records=old.get('records',{}))
                self.persist();return dict(token=token,room=self.name,topics=self.topics,bank=self.bank)
            token=body.get('token')
            if not isinstance(token,str) or token not in self.members:raise PermissionError('Vuelve a unirte a la sala.')
            member=self.members[token]
            if route=='/results':
                if body.get('practice') or member.get('role')=='teacher':return dict(accepted=False,reason='Las pruebas docentes no cuentan.')
                records=body.get('records',{})
                if not isinstance(records,dict) or len(records)>TOTAL_LEVELS:raise ValueError('Resultados inválidos.')
                normalized={}
                for key,record in records.items():
                    if not str(key).isdigit() or not 0<=int(key)<TOTAL_LEVELS or not isinstance(record,dict):raise ValueError('Mapa inválido.')
                    score=record.get('score')
                    if type(score) is not int or not 0<=score<=100000:raise ValueError('Puntuación inválida.')
                    canonical=str(int(key))
                    if canonical in normalized:raise ValueError('Un mapa aparece más de una vez.')
                    normalized[canonical]=record
                for key,record in normalized.items():
                    previous=member['records'].get(str(key),{}).get('score',-1)
                    if record['score']>previous:member['records'][str(key)]={'score':record['score']}
                self.persist();return dict(accepted=True)
            if route=='/rankings':
                rows=[m for m in self.members.values() if m.get('role')!='teacher']
                return dict(classroom=rankings(rows,member['classroom'],member['institution']),institution=rankings(rows,institution=member['institution']))
            if route=='/activity':return dict(topics=self.topics,bank=self.bank)
            raise ValueError('Ruta desconocida.')

    def start(self,host='0.0.0.0',port=8765):
        import threading
        from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
        room=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 0<length<=LIMIT:raise ValueError('Solicitud demasiado grande o vacía.')
                    body=json.loads(self.rfile.read(length).decode('utf-8'))
                    result=room.request(self.path,body);status=200
                except PermissionError as error:result={'error':str(error)};status=403
                except (ValueError,UnicodeError) as error:result={'error':str(error)};status=400
                except OSError:result={'error':'No se pudieron guardar los resultados en el servidor.'};status=503
                payload=json.dumps(result,ensure_ascii=False).encode('utf-8')
                self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
                self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
        self.server=ThreadingHTTPServer((host,port),Handler);self.server.daemon_threads=True
        self.server.timeout=.5
        threading.Thread(target=self.server.serve_forever,daemon=True,name='Crono aula LAN').start()
        return self.server.server_port
    def stop(self):
        if self.server:self.server.shutdown();self.server.server_close();self.server=None

class RoomClient:
    def __init__(self,address,token=None):
        from urllib.parse import urlparse
        if '://' not in address:address='http://'+address
        parsed=urlparse(address)
        if parsed.scheme!='http' or not parsed.hostname or parsed.username or parsed.password:raise ValueError('Usa IP:puerto de la computadora docente.')
        self.address=f'http://{parsed.hostname}:{parsed.port or 8765}';self.token=token
    def call(self,route,**body):
        from urllib.request import Request,urlopen
        request=Request(self.address+route,data=json.dumps(dict(body,token=self.token)).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
        with urlopen(request,timeout=3) as response:
            data=response.read(RESPONSE_LIMIT+1)
            if len(data)>RESPONSE_LIMIT:raise ValueError('Respuesta demasiado grande.')
            result=json.loads(data)
        if route=='/join':self.token=result['token']
        return result

def local_addresses():
    import socket
    try:return sorted({a[4][0] for a in socket.getaddrinfo(socket.gethostname(),None,socket.AF_INET) if not a[4][0].startswith('127.')}) or ['127.0.0.1']
    except OSError:return ['127.0.0.1']
