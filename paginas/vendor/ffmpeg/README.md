---
tipo: readme
estado: activo
---
# paginas/vendor/ffmpeg/ — ffmpeg.wasm para exportar video en el navegador (editor de video)

Copia sin cambios de **ffmpeg.wasm**, la compilación de FFmpeg a WebAssembly, que `paginas/video.html` carga
**solo** cuando se elige «Exportar en el navegador» (importación dinámica: quien exporta en esta computadora
nunca descarga los 31 MB). Se usa el núcleo **de un solo hilo** (`@ffmpeg/core`), que no necesita
`SharedArrayBuffer` ni las cabeceras COOP/COEP: el estudio corre detrás del proxy de Qillqa, que no las envía
(`qillqa/backend/app/api/prensa.py`, `_DESDE`), y activarlas rompería el marco de Qillqa.

## Origen y versiones

Traídas del registro oficial de npm (`npm pack`) el 2026-10-06; la integridad coincide con la que publica el
registro (`npm view <paquete> dist.integrity`).

| carpeta | paquete | versión | licencia | integridad del paquete (npm) | sha256 del `.tgz` |
|---|---|---|---|---|---|
| `ffmpeg/` | `@ffmpeg/ffmpeg` (clase `FFmpeg` y su worker; `dist/esm`) | 0.12.15 | MIT | `sha512-1C8Obr4GsN3xw+/1Ww6PFM84wSQAGsdoTuTWPOj2OizsRDLT4CXTaVjPhkw6ARyDus1B9X/L2LiXHqYYsGnRFw==` | `c8a23365fb39b46d3d1d9baa2e74b522d00ce5d57e8b20471ad2665eaad38e3e` |
| `util/` | `@ffmpeg/util` (`fetchFile`; `dist/esm`) | 0.12.2 | MIT | `sha512-ouyoW+4JB7WxjeZ2y6KpRvB+dLp7Cp4ro8z0HIVpZVCM7AwFlHa0c4R8Y/a4M3wMqATpYKhC7lSFHQ0T11MEDw==` | `1a37765f61421a6da0dc955a3b5a8872c6a0ce46928d50dfa99ce3a12a85ba1a` |
| `core/` | `@ffmpeg/core` (un solo hilo; `dist/esm`) | 0.12.10 | GPL-2.0-or-later | `sha512-dzNplnn2Nxle2c2i2rrDhqcB19q9cglCkWnoMTDN9Q9l3PvdjZWd1HfSPjCNWc/p8Q3CT+Es9fWOR0UhAeYQZA==` | `d00089ce82e1bdf637ddbe42e0c3d41a1ba8cf4c9e825e7fa4d0bb970e844bd4` |

`SHA256SUMS` guarda la suma de cada archivo copiado (`sha256sum -c SHA256SUMS` desde esta carpeta lo comprueba).

## Licencias (precisas)

- `@ffmpeg/ffmpeg` y `@ffmpeg/util`: **MIT**, © 2019 Jerome Wu (`ffmpeg/LICENSE`, `util/LICENSE`, el
  `LICENSE` del repositorio ffmpegwasm/ffmpeg.wasm; los paquetes de npm no lo incluyen).
- `@ffmpeg/core` 0.12.10: **GPL-2.0-or-later** (`core/LICENSE`, texto de la GPL v2). No es LGPL: el binario es
  FFmpeg 5.1 (libavformat 59.27.100) configurado con `--enable-gpl --enable-libx264 --enable-libx265`, además de
  libvpx, libmp3lame, libtheora, libvorbis, libopus, zlib, libwebp, libfreetype, libfribidi, libass y libzimg
  (línea de configuración incrustada en `ffmpeg-core.wasm`). x264 y x265 son GPL-2.0-or-later, por eso el
  conjunto se distribuye bajo GPL.
- Obligación de fuente: quien reciba este estudio recibe el `.wasm` tal cual lo publica npm; su código
  correspondiente es el de ffmpegwasm/ffmpeg.wasm en la etiqueta del núcleo 0.12.10
  (<https://github.com/ffmpegwasm/ffmpeg.wasm>, carpeta `build/` con las versiones de cada biblioteca) y el de
  FFmpeg (<https://ffmpeg.org/download.html>). El editor no enlaza ni modifica el núcleo: lo carga como módulo
  independiente en un worker; el resto del repo conserva su licencia.

## Cómo se usa

`video.html` hace `import("vendor/ffmpeg/ffmpeg/index.js")` (ruta relativa a la página, así funciona también
bajo `/estudio/` de Qillqa) y llama a `ffmpeg.load({coreURL, wasmURL})` con las URL absolutas de `core/`. El
worker es un módulo ES: `importScripts` falla y se importa `core/ffmpeg-core.js` (ESM). El servidor sirve `.wasm`
como `application/wasm` y `.js`/`.mjs` como `text/javascript` (el servidor del estudio, en Ruray: `estudio/editor/servidor/servidor.py`).

## Cómo se actualiza

```bash
paginas/vendor/ffmpeg/actualizar.sh                       # simula: descarga, verifica la integridad y lista
paginas/vendor/ffmpeg/actualizar.sh --aplicar 0.12.15 0.12.2 0.12.10   # copia y rehace SHA256SUMS
```

Después: actualizar la tabla de arriba (versiones, integridad, sha256), revisar la línea de configuración del
núcleo (`strings core/ffmpeg-core.wasm | grep -m1 -- --enable-gpl`) por si cambió la licencia, y exportar un
proyecto corto con «Exportar en el navegador» en `video.html`.
