"""kuyuy/manifiesto.py — el manifiesto del editor de videos (Kuyuy): el mismo dentro de Qillqa y solo.

El editor de video del estudio (`video.html`) y la cola de video (ffmpeg, un trabajo a la vez) como módulo: su API
(`kuyuy/api.py`) sobre la base común de los editores (Ruray). Sin base de datos y sin necesitar nada del anfitrión: la
cuenta llega por «identidad.v1» y el kit común, de Unancha (UNANCHA_DIR). Aprovecha la Mediateca («medios.v2»: su
selector, y lo exportado va a ella) y la referencia «piezas:pieza:N»; solo, sin ellas, trabaja con su banco y su salida
(`kuyuy/sola.py`). Su web: `web/src/componentes/videos/modulo.ts`.
"""
from __future__ import annotations

from tiqsi import Manifiesto

from kuyuy import api as videos

VERSION = "0.1.0"

MANIFIESTO = Manifiesto(
    id="videos", nombre="Editor de videos", version=VERSION, contrato="^0.1",
    routers=[videos.router],
    # Los prefijos con que se apaga (los del registro de módulos encendibles de Qillqa).
    prefijos=("/api/videos",),
)
