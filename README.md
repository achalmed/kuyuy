# Kuyuy — un editor de video con línea de tiempo

Kuyuy («mover, movimiento» en quechua) es un editor de video para el navegador: una línea de tiempo con pistas de
video, texto y audio, transiciones, títulos y rótulos de una marca, música con ducking y subtítulos automáticos, que
exporta con ffmpeg en la computadora o con [ffmpeg.wasm](https://github.com/ffmpegwasm/ffmpeg.wasm) en el navegador.
Es un módulo de [Tiqsi](https://github.com/achalmed/tiqsi) sobre [Ruray](https://github.com/achalmed/ruray), la base
común de los editores: funciona solo, con el anfitrión mínimo de Tiqsi, o dentro de una plataforma que lo monte por su
manifiesto (como Qillqa).

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -e '.[pruebas,sola]'   # requiere tiqsi y ruray
.venv/bin/python -m pytest -q tests
npm install && npm run web:construir
paginas/vendor/ffmpeg/actualizar.sh --aplicar            # ffmpeg-core.wasm (31 MB), para exportar en el navegador
KUYUY_DIR=/ruta/kuyuy JWT_SECRET=<32 o más caracteres> KUYUY_WEB=web/dist .venv/bin/uvicorn kuyuy.sola:app --port 8038
```

Los colores, la letra, los logos y los marcos salen de un kit de identidad (`UNANCHA_DIR`). Esta es una **versión de
demostración**. Licencia: AGPL-3.0 (`LICENSE`); ffmpeg.wasm, la suya (`paginas/vendor/ffmpeg/README.md`).
