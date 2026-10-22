"""kuyuy/sola.py — el editor de videos SOLO: sin Qillqa, con el anfitrión mínimo de Tiqsi (Kuyuy). Sin base de datos y
sin Mediateca: su banco, su almacén, sus proyectos y su salida viven en su carpeta; el kit común (colores, fuentes,
logos, marcos), en Unancha.

    KUYUY_DIR=…  UNANCHA_DIR=…  JWT_SECRET=<32 o más caracteres> \\
      .venv/bin/uvicorn kuyuy.sola:app --port 8038

Las cuentas viven en KUYUY_CUENTAS (por omisión <KUYUY_DIR>/cuentas.json). Sin IDENTIDAD_PERFIL, el perfil del editor
se escribe la primera vez en <KUYUY_DIR>/perfil.json, con sus carpetas dentro de KUYUY_DIR.
"""
from __future__ import annotations

import os
from pathlib import Path

from ruray.comun import perfil_propio
from tiqsi.minimo import crear_app

from kuyuy.manifiesto import MANIFIESTO

carpeta = os.environ.get("KUYUY_DIR", "")
if not carpeta:
    raise SystemExit("El editor de videos solo necesita su carpeta (su banco, sus proyectos, su salida y sus cuentas): KUYUY_DIR.")
secreto = os.environ.get("JWT_SECRET", "")
if len(secreto) < 32:
    raise SystemExit("El editor de videos solo necesita su secreto: JWT_SECRET (32 caracteres o más; firma las sesiones).")
# El servidor del estudio lee el perfil al cargarse (la primera petición): va antes.
os.environ.setdefault("IDENTIDAD_PERFIL", str(perfil_propio(Path(carpeta), "editor de videos")))

app = crear_app([MANIFIESTO], nombre="Editor de videos", secreto=secreto,
                cuentas=os.environ.get("KUYUY_CUENTAS") or Path(carpeta) / "cuentas.json",
                web=os.environ.get("KUYUY_WEB") or None)
