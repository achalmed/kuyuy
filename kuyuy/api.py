"""kuyuy/api.py — el editor de videos (Kuyuy; nació en Qillqa el 2026-10-20, editores E3, y salió a su repositorio el
2026-10-21).

Su página vive en `paginas/` de este repositorio: `video.html` (línea de tiempo con pistas, títulos, transiciones,
música y subtítulos automáticos; render con ffmpeg en el servidor o con ffmpeg.wasm en el navegador, `vendor/ffmpeg/`).
La sirve la base común de los editores (Ruray, `ruray.comun`) bajo `/api/videos/`, con su cookie: las rutas comunes
(kit, banco, almacén, salidas, el aspecto del estudio), los proyectos de medios y las de video (configuración,
trabajos, fotogramas, plan para ffmpeg.wasm, transcripción). La cola de video (ffmpeg, un trabajo a la vez) y la orden
que arma (`montaje.py`) son del servidor del estudio, en Ruray; también recorta el video suelto de `media.html` (Tullpu,
que la llama por `?video=/api/videos/`).

Con la Mediateca, lo exportado entra a ella cuando su trabajo queda listo («Guardar en la Fototeca» es la puerta
explícita); solo, queda en la salida de su canal.
"""
from __future__ import annotations

from pathlib import Path

from ruray.comun import COMUNES, VIDEO, Editor, crear_router

PAGINAS = Path(__file__).resolve().parents[1] / "paginas"

EDITOR = Editor(
    id="videos", nombre="Editor de videos", prefijo="/api/videos", inicio="video.html",
    paginas=("video.html", "estudio-tema.css", "estudio-iconos.js", "estudio-movil.js", "vendor/ffmpeg/"),
    rutas=COMUNES | VIDEO | {"GET api/proyectos-media", "GET api/proyecto-media", "POST api/proyecto-media"},
    carpeta=PAGINAS,
)

router = crear_router(EDITOR)
