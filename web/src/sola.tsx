/**
 * El editor de videos SOLO en el navegador (Kuyuy): la cáscara mínima de Tiqsi con el módulo web del editor, contra el
 * anfitrión mínimo del backend (kuyuy/sola.py). No importa nada de Qillqa. Se construye desde la raíz con
 * `npm run web:construir`.
 */
import { createRoot } from 'react-dom/client'
import { CascaronMinimo } from '@qillqa/tiqsi/minimo'
import { KUYUY } from './componentes/videos/modulo'

createRoot(document.getElementById('root')!).render(<CascaronMinimo modulo={KUYUY} />)
