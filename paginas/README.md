---
tipo: readme
estado: activo
---
# paginas/ — la página del editor de videos

La sirve la base común de los editores (Ruray) bajo `/api/videos/` (`Editor.carpeta` de `kuyuy/api.py`): primero de
aquí y, lo común del estudio (`estudio-tema.css`, `estudio-iconos.js`, `estudio-movil.js`), desde Ruray. Pide todo
relativo a su carpeta (`api("api/x")` → `/api/videos/api/x`); no se reescribe para el servidor.

| archivo | qué es |
|---|---|
| `video.html` | edición de video con línea de tiempo (al estilo de Kdenlive y CapCut): pistas de video, superposición, texto y audio; cortar, recortar normal u ondulado, imán, marcadores, deshacer; velocidad, volumen, fundidos, transiciones, Ken Burns, color; títulos y rótulos de la marca, marcos y logos, zonas seguras; música con ducking; subtítulos automáticos palabra a palabra (Whisper); exporta con ffmpeg en la computadora (−14 LUFS) o con ffmpeg.wasm en el navegador. Rutas del servidor: `../../ruray/estudio/editor/servidor/README.md` |
| `vendor/ffmpeg/` | ffmpeg.wasm 0.12 (núcleo de un hilo, GPL-2.0-or-later; clase y utilidades MIT) que `video.html` carga solo al exportar en el navegador; origen, sha256, licencias y actualización en su README |
