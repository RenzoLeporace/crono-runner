// Pruebas del puente del navegador sin navegador: node --test web/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

function cargarPuente({ tactil = false, busqueda = '' } = {}) {
  const abiertas = [];
  const window = {
    matchMedia: (consulta) => ({ matches: tactil && consulta.includes('coarse') }),
    open: (url) => abiertas.push(url)
  };
  const contexto = {
    window, console, atob, btoa, TextEncoder, TextDecoder, URLSearchParams, setTimeout,
    location: { search: busqueda },
    navigator: {},
    document: {
      documentElement: {},
      getElementById: () => null,
      createElement: () => ({ append() {}, addEventListener() {}, setAttribute() {}, focus() {}, select() {}, remove() {} }),
      body: { append() {} }
    }
  };
  vm.createContext(contexto);
  vm.runInContext(readFileSync(new URL('./crono-web.js', import.meta.url), 'utf8'), contexto);
  return { puente: window.CronoAndroid, web: window.CronoWeb, abiertas };
}

const esperarPoll = (puente, id) => JSON.parse(puente.poll(id));

test('sin IndexedDB queda listo y juega sin conservar el progreso', async () => {
  const { web } = cargarPuente();
  await web.cargando;
  assert.equal(web.isReady(), true);
  assert.equal(web.persistent(), false);
});

test('guarda y lee archivos con acentos, como el puente de Android', () => {
  const { puente, web } = cargarPuente();
  const { codificar, decodificar } = web._interno;
  const texto = JSON.stringify({ alias: 'Ñandú', pregunta: '¿Qué pasó en 1816?', pt: 'São Paulo' });
  assert.equal(puente.saveFile('saves/perfiles.json', codificar(texto)), true);
  assert.equal(decodificar(puente.loadFile('saves/perfiles.json')), texto);
  assert.deepEqual(JSON.parse(puente.loadFiles()), { 'saves/perfiles.json': texto });
  assert.equal(puente.loadFile('saves/no-existe.json'), '');
  assert.equal(puente.deleteFile('saves/perfiles.json'), true);
  assert.equal(puente.loadFile('saves/perfiles.json'), '');
});

test('solo acepta rutas dentro de saves/ y contenido/', () => {
  const { puente, web } = cargarPuente();
  const contenido = web._interno.codificar('{}');
  for (const ruta of ['../saves/x.json', 'saves/../crono/game.py', '/saves/x.json', 'crono/game.py', 'saves', 'saves//x.json']) {
    assert.equal(puente.saveFile(ruta, contenido), false, ruta);
  }
  assert.equal(puente.saveFile('contenido/preguntas.json', contenido), true);
});

test('loadFiles solo devuelve perfiles y configuración docente', () => {
  const { puente, web } = cargarPuente();
  const c = web._interno.codificar;
  puente.saveFile('saves/perfiles.json', c('{"a":1}'));
  puente.saveFile('saves/docente.json', c('{"b":2}'));
  puente.saveFile('saves/progreso.json', c('{"c":3}'));
  assert.deepEqual(Object.keys(JSON.parse(puente.loadFiles())).sort(), ['saves/docente.json', 'saves/perfiles.json']);
});

test('las salas en red local responden con un aviso en lugar de colgarse', () => {
  const { puente } = cargarPuente();
  const id = puente.enqueue(JSON.stringify({ operation: 'join', address: 'http://192.168.0.10:8765' }));
  const respuesta = esperarPoll(puente, id);
  assert.equal(respuesta.ready, true);
  assert.match(respuesta.error, /red local/);
  assert.match(puente.poll(id), /Solicitud desconocida/, 'un trabajo terminado se consulta una sola vez');
});

test('con teclado no abre un cuadro para escribir; en pantallas táctiles sí', () => {
  const pc = cargarPuente();
  const id = pc.puente.editText(pc.web._interno.codificar('Ana'), 80, false, false);
  assert.deepEqual(esperarPoll(pc.puente, id), { ready: true });

  const celular = cargarPuente({ tactil: true });
  const otro = celular.puente.editText(celular.web._interno.codificar('Ana'), 80, false, false);
  assert.deepEqual(esperarPoll(celular.puente, otro), { ready: false });
  assert.equal(celular.web.touchFirst(), true);
  assert.equal(cargarPuente({ busqueda: '?tactil=1' }).web.touchFirst(), true);
});

test('abre solo enlaces https', () => {
  const { puente, web, abiertas } = cargarPuente();
  puente.openUrl(web._interno.codificar('https://es.wikipedia.org/wiki/Crono'));
  puente.openUrl(web._interno.codificar('javascript:alert(1)'));
  assert.deepEqual(abiertas, ['https://es.wikipedia.org/wiki/Crono']);
});
