#!/usr/bin/env bash
# paginas/vendor/ffmpeg/actualizar.sh — vuelve a traer ffmpeg.wasm del registro oficial de npm, verifica la
# integridad que publica el registro y copia los módulos ES. Simula por defecto; --aplicar escribe.
#   paginas/vendor/ffmpeg/actualizar.sh [--aplicar] [VERSION_FFMPEG VERSION_UTIL VERSION_CORE]
set -euo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APLICAR=0
if [ "${1:-}" = "--aplicar" ]; then APLICAR=1; shift; fi
VF="${1:-0.12.15}"; VU="${2:-0.12.2}"; VC="${3:-0.12.10}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cd "$TMP"
for par in "ffmpeg@$VF" "util@$VU" "core@$VC"; do
  npm pack "@ffmpeg/$par" --silent >/dev/null
  tgz="ffmpeg-${par/@/-}.tgz"
  esperado="$(npm view "@ffmpeg/$par" dist.integrity)"
  real="sha512-$(openssl dgst -sha512 -binary "$tgz" | base64 -w0)"
  [ "$esperado" = "$real" ] || { echo "integridad distinta en $tgz" >&2; exit 1; }
  echo "· @ffmpeg/$par  $real  (sha256 $(sha256sum "$tgz" | cut -d' ' -f1))"
  mkdir -p "${par%@*}" && tar xzf "$tgz" -C "${par%@*}"
done
if [ "$APLICAR" = 0 ]; then echo "simulación: nada escrito (use --aplicar)"; exit 0; fi
cp ffmpeg/package/dist/esm/*.js ffmpeg/package/dist/esm/empty.mjs ffmpeg/package/package.json "$AQUI/ffmpeg/"
cp util/package/dist/esm/*.js util/package/package.json "$AQUI/util/"
cp core/package/dist/esm/ffmpeg-core.js core/package/dist/esm/ffmpeg-core.wasm core/package/package.json "$AQUI/core/"
cd "$AQUI" && find . -type f ! -name SHA256SUMS ! -name README.md ! -name actualizar.sh | sort | xargs sha256sum > SHA256SUMS
echo "copiado; revise README.md (versiones y licencias) y el plan del editor (video.html) antes de publicar"
