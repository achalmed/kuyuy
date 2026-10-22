/**
 * El módulo web del editor de videos (proyecto Kuyuy, editores E3; fase 10.2b del contrato de Tiqsi, 2026-10-20): su
 * pantalla y su ruta. En Qillqa no tiene entrada propia en el menú: Prensa (Video) carga su pantalla con `KUYUY.cargar` y
 * la pinta en su propio marco, sin importar nada más del módulo. Solo (src/kuyuy_sola.tsx), la cáscara mínima la monta en
 * su ruta.
 *
 * `video.html` (pistas, títulos, transiciones, música y subtítulos automáticos), servido por la API del módulo bajo
 * /api/videos/ con su cookie; la misma API recorta los videos sueltos del revelado del editor de fotos.
 */
import MovieOutlinedIcon from '@mui/icons-material/MovieOutlined'
import { definirModuloWeb } from '@qillqa/tiqsi'

export const KUYUY = definirModuloWeb({
  id: 'videos',
  nombre: 'Editor de videos',
  corto: 'Videos',
  ruta: '/videos',
  icono: MovieOutlinedIcon,
  descripcion: 'Videos con pistas, títulos, transiciones, música y subtítulos automáticos.',
  opciones: [
    { etiqueta: 'Video', ruta: '/videos', icono: MovieOutlinedIcon, ayuda: 'Línea de tiempo con pistas; se exporta con ffmpeg' },
  ],
  cargar: () => import('../../paginas/Videos'),
})
