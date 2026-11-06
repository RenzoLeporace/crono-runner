// CRONO en el navegador: ofrece el mismo puente que la app de Android (window.CronoAndroid,
// ver android/.../MainActivity.java) con APIs web, así el código de crono/ no cambia.
// - Guardados y bancos docentes: IndexedDB, con una copia en memoria para leer sin esperas.
// - Lectura en voz alta: speechSynthesis del navegador.
// - Textos en pantallas táctiles, importar y exportar: un cuadro propio, <input type=file> y descargas.
// - Salas docentes: no disponibles, porque una página HTTPS no puede hablar con la red local por HTTP.
(function () {
  'use strict';

  const BASE = 'crono-runner';
  const ALMACEN = 'archivos';
  const LIMITE = 32 * 1024 * 1024;
  const archivos = new Map();
  const trabajos = new Map();
  let base = null;
  let listo = false;
  let persistente = false;
  let idioma = 'es';
  let siguiente = 0;

  const textos = {
    es: { escribir: 'CRONO · Escribir', aceptar: 'Aceptar', cancelar: 'Cancelar', sala: 'Las salas docentes funcionan en la red local: uní este dispositivo desde la app de Windows o Android.', fin: 'Partida guardada. Recargá la página para volver a jugar.' },
    'pt-BR': { escribir: 'CRONO · Escrever', aceptar: 'Confirmar', cancelar: 'Cancelar', sala: 'As salas docentes funcionam na rede local: entre neste dispositivo pelo app de Windows ou Android.', fin: 'Partida salva. Recarregue a página para jogar de novo.' }
  };
  const t = (clave) => (textos[idioma] || textos.es)[clave];

  // ---- Texto en base64 UTF-8, como lo intercambia crono/mobile.py --------------------------
  function decodificar(valor) {
    const binario = atob(String(valor));
    const bytes = new Uint8Array(binario.length);
    for (let i = 0; i < binario.length; i++) bytes[i] = binario.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }
  function codificar(texto) {
    const bytes = new TextEncoder().encode(String(texto));
    let binario = '';
    for (let i = 0; i < bytes.length; i += 0x8000) binario += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(binario);
  }

  // Solo se guardan rutas relativas dentro de saves/ y contenido/, como en Android.
  function rutaValida(ruta) {
    const partes = String(ruta).split('/');
    return partes.length > 1 && (partes[0] === 'saves' || partes[0] === 'contenido') && !partes.includes('..') && !partes.includes('') && !String(ruta).startsWith('/');
  }

  // ---- Almacenamiento ---------------------------------------------------------------------
  function abrirBase() {
    return new Promise((resolve, reject) => {
      const pedido = indexedDB.open(BASE, 1);
      pedido.onupgradeneeded = () => pedido.result.createObjectStore(ALMACEN);
      pedido.onsuccess = () => resolve(pedido.result);
      pedido.onerror = () => reject(pedido.error);
    });
  }

  async function cargar() {
    try {
      base = await abrirBase();
      await new Promise((resolve, reject) => {
        const cursor = base.transaction(ALMACEN, 'readonly').objectStore(ALMACEN).openCursor();
        cursor.onsuccess = () => {
          const actual = cursor.result;
          if (!actual) return resolve();
          if (typeof actual.value === 'string') archivos.set(actual.key, actual.value);
          actual.continue();
        };
        cursor.onerror = () => reject(cursor.error);
      });
      persistente = true;
      if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
    } catch (error) {
      // Sin IndexedDB (por ejemplo, algunas ventanas privadas) se juega igual, sin conservar el progreso.
      base = null;
      persistente = false;
    } finally {
      listo = true;
    }
  }

  function escribirEnBase(operacion) {
    if (!base) return;
    try {
      operacion(base.transaction(ALMACEN, 'readwrite').objectStore(ALMACEN));
    } catch (error) {
      console.warn('CRONO: no se pudo guardar en el navegador', error);
    }
  }

  // ---- Trabajos asíncronos que Python consulta con poll() ----------------------------------
  function nuevoTrabajo() {
    const id = 'web-' + (++siguiente);
    trabajos.set(id, { ready: false });
    return id;
  }
  const terminar = (id, datos) => trabajos.set(id, Object.assign({ ready: true }, datos));

  function pedirTexto(id, inicial, limite, multilinea, clave) {
    const capa = document.createElement('div');
    capa.className = 'crono-dialogo';
    capa.setAttribute('role', 'dialog');
    capa.setAttribute('aria-modal', 'true');
    const caja = document.createElement('form');
    const titulo = document.createElement('p');
    titulo.textContent = t('escribir');
    const campo = document.createElement(multilinea ? 'textarea' : 'input');
    if (!multilinea) campo.type = clave ? 'password' : 'text';
    campo.value = inicial;
    campo.maxLength = Math.max(1, Math.min(1000, limite));
    campo.setAttribute('aria-label', t('escribir'));
    const botones = document.createElement('div');
    const cancelar = document.createElement('button');
    cancelar.type = 'button';
    cancelar.textContent = t('cancelar');
    const aceptar = document.createElement('button');
    aceptar.type = 'submit';
    aceptar.textContent = t('aceptar');
    botones.append(cancelar, aceptar);
    caja.append(titulo, campo, botones);
    capa.append(caja);
    const cerrar = (datos) => {
      capa.remove();
      terminar(id, datos);
      const lienzo = document.getElementById('canvas');
      if (lienzo) lienzo.focus();
    };
    caja.addEventListener('submit', (evento) => {
      evento.preventDefault();
      cerrar({ text: campo.value });
    });
    cancelar.addEventListener('click', () => cerrar({}));
    capa.addEventListener('keydown', (evento) => {
      evento.stopPropagation();
      if (evento.key === 'Escape') cerrar({});
    });
    document.body.append(capa);
    campo.focus();
    if (campo.select) campo.select();
  }

  // ?tactil=1 fuerza los controles en pantalla, por ejemplo para probarlos con el mouse.
  const esTactil = () => new URLSearchParams(location.search).has('tactil') || window.matchMedia('(pointer: coarse)').matches;

  // ---- El puente, con la misma interfaz que MainActivity.Bridge ----------------------------
  const puente = {
    setLanguage(valor) { idioma = valor === 'pt-BR' ? 'pt-BR' : 'es'; document.documentElement.lang = idioma; },
    performanceLogging() { return new URLSearchParams(location.search).has('rendimiento'); },
    speak(contenido, lengua) {
      if (!('speechSynthesis' in window)) return false;
      try {
        const texto = decodificar(contenido);
        if (texto.length > 3500) return false;
        const frase = new SpeechSynthesisUtterance(texto);
        frase.lang = lengua === 'pt-BR' ? 'pt-BR' : 'es-AR';
        const voz = speechSynthesis.getVoices().find((v) => v.lang.toLowerCase().startsWith(lengua === 'pt-BR' ? 'pt' : 'es'));
        if (voz) frase.voice = voz;
        speechSynthesis.cancel();
        speechSynthesis.speak(frase);
        return true;
      } catch (error) {
        return false;
      }
    },
    loadFiles() {
      const resultado = {};
      for (const ruta of ['saves/perfiles.json', 'saves/docente.json']) {
        if (archivos.has(ruta)) resultado[ruta] = archivos.get(ruta);
      }
      return JSON.stringify(resultado);
    },
    loadFile(ruta) {
      return rutaValida(ruta) && archivos.has(ruta) ? codificar(archivos.get(ruta)) : '';
    },
    saveFile(ruta, contenido) {
      try {
        if (!rutaValida(ruta)) return false;
        const texto = decodificar(contenido);
        if (texto.length > LIMITE) return false;
        archivos.set(ruta, texto);
        escribirEnBase((almacen) => almacen.put(texto, ruta));
        return true;
      } catch (error) {
        return false;
      }
    },
    deleteFile(ruta) {
      if (!rutaValida(ruta)) return false;
      const existia = archivos.delete(ruta);
      escribirEnBase((almacen) => almacen.delete(ruta));
      return existia;
    },
    openUrl(codificada) {
      try {
        const url = decodificar(codificada);
        if (url.startsWith('https://')) window.open(url, '_blank', 'noopener');
      } catch (error) { /* enlace inválido: se ignora, como en Android */ }
    },
    finishGame() { window.CronoWeb.finished(); },
    enqueue() {
      const id = nuevoTrabajo();
      terminar(id, { error: t('sala') });
      return id;
    },
    poll(id) {
      const trabajo = trabajos.get(String(id));
      if (!trabajo) return JSON.stringify({ ready: true, error: 'Solicitud desconocida' });
      if (trabajo.ready) trabajos.delete(String(id));
      return JSON.stringify(trabajo);
    },
    editText(inicial, limite, multilinea, clave) {
      const id = nuevoTrabajo();
      // Con teclado físico se escribe directo en el juego; en pantallas táctiles hace falta un campo real.
      if (!esTactil()) terminar(id, {});
      else pedirTexto(id, decodificar(inicial), Number(limite), Boolean(multilinea), Boolean(clave));
      return id;
    },
    pickQuestionBank() {
      const id = nuevoTrabajo();
      const selector = document.createElement('input');
      selector.type = 'file';
      selector.accept = 'application/json,.json';
      selector.addEventListener('change', () => {
        const archivo = selector.files && selector.files[0];
        if (!archivo) return terminar(id, {});
        if (archivo.size > 4000000) return terminar(id, { error: 'El archivo supera los 4 MB.' });
        archivo.text().then((texto) => terminar(id, { text: texto }), (error) => terminar(id, { error: String(error) }));
      });
      selector.addEventListener('cancel', () => terminar(id, {}));
      selector.click();
      return id;
    },
    exportDocument(nombre, contenido, tipo) {
      const id = nuevoTrabajo();
      try {
        const url = URL.createObjectURL(new Blob([decodificar(contenido)], { type: tipo + ';charset=utf-8' }));
        const enlace = document.createElement('a');
        enlace.href = url;
        enlace.download = String(nombre);
        document.body.append(enlace);
        enlace.click();
        enlace.remove();
        setTimeout(() => URL.revokeObjectURL(url), 2000);
        terminar(id, { saved: true });
      } catch (error) {
        terminar(id, { error: String(error) });
      }
      return id;
    }
  };

  window.CronoAndroid = puente;
  window.CronoWeb = {
    cargando: cargar(),
    isReady: () => listo,
    persistent: () => persistente,
    touchFirst: esTactil,
    finished() {
      const aviso = document.createElement('div');
      aviso.className = 'crono-dialogo';
      aviso.textContent = t('fin');
      document.body.append(aviso);
    },
    // Para las pruebas automáticas del puente.
    _interno: { archivos, trabajos, codificar, decodificar, rutaValida }
  };
})();
