"""tests/test_kuyuy.py — el editor de videos (Kuyuy; nació en Qillqa el 2026-10-20, editores E3) sobre la base común de los
editores (Ruray): sus páginas y su API bajo /api/videos/, la cola de video con ffmpeg de verdad (un clip de 2 s recortado), el
fotograma y, con una Mediateca falsa, el video listo que entra a ella una vez con la pieza de la sesión.
"""
import base64
import io
import shutil
import subprocess
import time
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ruray import comun as estudio_comun
from ruray import mediateca as estudio_mediateca
from ruray.pruebas import PNG, MediatecaFalsa, entorno  # noqa: F401 — el entorno temporal común de los editores (Ruray)
from tiqsi import puertos

from kuyuy import api as videos


def _app():
    app = FastAPI()
    app.include_router(videos.router)
    app.dependency_overrides[puertos.usuario_actual] = lambda: SimpleNamespace(id=7, rol="asesor")
    return app


@pytest.fixture
def cliente(entorno):
    c = TestClient(_app())
    assert c.post("/api/videos/sesion").status_code == 200
    return c


@pytest.fixture
def clip(entorno, cliente):
    """Un video de 2 s en el banco, subido por el editor."""
    if shutil.which("ffmpeg") is None:
        pytest.skip("sin ffmpeg en esta máquina")
    tmp, _ = entorno
    ruta = tmp / "clip.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=320x240:rate=25", "-t", "2",
                    "-pix_fmt", "yuv420p", str(ruta)], check=True)
    r = cliente.post("/api/videos/api/subir", content=ruta.read_bytes(), headers={"X-Nombre": "clip.mp4", "Content-Type": "video/mp4"})
    assert r.json()["esVideo"]
    return r.json()["url"]


def _esperar(cliente, trabajo: str) -> dict:
    for _ in range(120):
        t = cliente.get(f"/api/videos/api/trabajo?id={trabajo}").json()
        if t["estado"] in ("listo", "error"):
            return t
        time.sleep(0.5)
    raise AssertionError("el trabajo no terminó")


def _capa(w: int, h: int) -> str:
    """La capa de la marca que compone el navegador: aquí, transparente, del tamaño del video."""
    from PIL import Image

    b = io.BytesIO()
    Image.new("RGBA", (w, h), (0, 0, 0, 0)).save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def _recorte(url: str) -> dict:
    return {"origen": url, "nombre": "corte.mp4", "canal": "youtube", "inicio": 0, "fin": 1, "w": 320, "h": 240,
            "overlay": _capa(320, 240), "segmentos": [{"ini": 0, "fin": 1}]}


def test_sus_paginas_y_las_de_otros(cliente):
    assert cliente.get("/api/videos/video.html").status_code == 200
    assert cliente.get("/api/videos/vendor/ffmpeg/ffmpeg/index.js").status_code == 200
    assert cliente.get("/api/videos/estudio-tema.css").status_code == 200                       # lo común, de Ruray
    for ruta in ("README.md", "vendor/ffmpeg/..%2F..%2F..%2Fkuyuy%2Fapi.py"):                # ni su README ni su código
        assert cliente.get("/api/videos/" + ruta).status_code in (403, 404), ruta
    assert cliente.get("/api/videos/foto.html", follow_redirects=False).status_code == 404     # solo: no hay a dónde
    assert cliente.get("/api/videos/api/video-config").json()["ffmpeg"] in (True, False)
    assert cliente.post("/api/videos/api/mejorar-foto", json={}).status_code == 404               # es del editor de fotos


def test_recorta_un_clip_en_la_cola(cliente, clip, entorno):
    tmp, _ = entorno
    r = cliente.post("/api/videos/api/exportar-video", json=_recorte(clip)).json()
    t = _esperar(cliente, r["trabajo"])
    assert t["estado"] == "listo", t
    assert t["url"].startswith("/api/videos/redes/youtube/") and "fototeca" not in t
    assert cliente.get(t["url"]).content[4:8] == b"ftyp"
    assert (tmp / "salida" / "redes" / "youtube" / t["archivo"]).is_file()
    # El fotograma del clip, para la línea de tiempo.
    f = cliente.get("/api/videos/api/fotograma", params={"origen": clip, "t": "0.5"})
    assert f.status_code == 200 and f.headers["content-type"] == "image/jpeg"


def test_lo_exportado_entra_a_la_mediateca_una_vez(entorno, clip, monkeypatch):
    tmp, _ = entorno
    falsa = MediatecaFalsa(tmp / "mediateca")
    monkeypatch.setattr(estudio_mediateca, "ft", falsa)
    monkeypatch.setattr(estudio_mediateca, "con_mediateca", lambda: True)

    async def pieza_de(pid):
        return {"id": pid, "titular": "Obra en Huanta"}

    monkeypatch.setattr(estudio_comun, "pieza_de", pieza_de)
    c = TestClient(_app())
    c.post("/api/videos/sesion", json={"pieza": 9})
    r = c.post("/api/videos/api/exportar-video", json=_recorte(clip)).json()
    t = _esperar(c, r["trabajo"])
    assert t["estado"] == "listo" and t["fototeca"]["nueva"]
    # El archivo se nombró por la hora, y el nombre escrito viaja como título; la pieza de la sesión, en sus usos.
    assert t["archivo"][11:].removesuffix(".mp4").isdigit()
    entrada = falsa.ingresos[-1]
    assert entrada["usos"] == ["red:youtube", "pieza:9"] and entrada["metadatos"]["titulo"] == "Corte"
    # Consultarlo otra vez no lo registra de nuevo; «Guardar en la Fototeca» es la puerta explícita.
    assert "fototeca" not in c.get(f"/api/videos/api/trabajo?id={r['trabajo']}").json()
    g = c.post("/api/videos/api/fototeca-video", json={"url": t["url"], "titulo": "Otro", "canal": "youtube"}).json()
    assert g["ok"] and len(falsa.ingresos) == 2
    assert c.post("/api/videos/api/fototeca-video", json={"url": "/api/videos/../../perfil.json"}).status_code == 400
