"""A local static-assets-only host, with a visible close-to-stop window."""
from pathlib import Path
import sys
import threading
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import pygame as pg

def run(port=8080):
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    folder=root/'iOS-Web'
    if not (folder/'index.html').is_file():raise SystemExit('Falta la carpeta iOS-Web junto al juego.')
    server=ThreadingHTTPServer(('0.0.0.0',port),partial(SimpleHTTPRequestHandler,directory=str(folder)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    pg.init();screen=pg.display.set_mode((940,440));pg.display.set_caption('CRONO · Servidor local para iPhone/iPad')
    from .rooms import local_addresses
    lines=['CRONO para iPhone / iPad','En Safari, desde la misma WiFi, abre:',*[f'http://{address}:{port}' for address in local_addresses()],
           'Mantén esta ventana abierta. Ciérrala para detener el servidor.',
           'Este acceso local requiere la PC conectada. Para instalar offline,','publica la versión web mediante HTTPS. No es un IPA firmado.']
    running=True;clock=pg.time.Clock()
    try:
        while running:
            for event in pg.event.get():
                if event.type==pg.QUIT:running=False
            screen.fill((15,34,45))
            for n,label in enumerate(lines):screen.blit(pg.font.Font(None,30 if n else 42).render(label,True,(206,228,217)),(35,35+n*46))
            pg.display.flip();clock.tick(15)
    finally:server.shutdown();server.server_close();pg.quit()
