import { PIPO } from './pipo-art';

/**
 * Visuais do Pipo para comemorar o fim da lição (acessórios desenhados por cima do Pipo).
 *  oculos: 0 erros, "Mr. Perfeito" de óculos escuros
 *  raio:   terminou muito rápido (linhas de velocidade e um raio)
 *  festa:  quase perfeito (chapéu de festa e confete)
 *  suor:   muitos erros, mas terminou (faixa na testa e gotinha de suor)
 */
export type Pose = 'oculos' | 'raio' | 'festa' | 'suor';

const miolo = (svg: string) => svg.replace(/^<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');

const OCULOS = `
<path d="M24 22 Q 24 17 28 17 L 47 17 Q 50.5 17 50 21 L 48.5 33 Q 47 42 38 42 Q 27.5 42 25 34 Z" fill="#111A22"/>
<path d="M76 22 Q 76 17 72 17 L 53 17 Q 49.5 17 50 21 L 51.5 33 Q 53 42 62 42 Q 72.5 42 75 34 Z" fill="#111A22"/>
<path d="M47 21 Q 50 19 53 21" fill="none" stroke="#111A22" stroke-width="3"/>
<path d="M24 21 L 16 18 M76 21 L 84 18" stroke="#111A22" stroke-width="2.6" stroke-linecap="round"/>
<path d="M29 23 L 36 23 M30.5 27 L 33.5 27" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity=".85"/>
<path d="M56 23 L 63 23 M57.5 27 L 60.5 27" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity=".85"/>
<path d="M88 4 l2 -5 l2 5 l5 2 l-5 2 l-2 5 l-2 -5 l-5 -2 z" fill="#FFD43B"/><path d="M8 0 l1.5 -4 l1.5 4 l4 1.5 l-4 1.5 l-1.5 4 l-1.5 -4 l-4 -1.5 z" fill="#FFD43B"/>`;

const RAIO = `
<g stroke="#7DB3FF" stroke-width="3.2" stroke-linecap="round" opacity=".9">
  <path d="M-8 30 L 8 30"/><path d="M-12 44 L 12 44"/><path d="M-6 58 L 14 58"/><path d="M-10 72 L 10 72"/>
</g>
<path d="M92 -8 L 80 14 L 89 14 L 83 32 L 100 6 L 90 6 L 96 -8 Z" fill="#FFD43B" stroke="#E8AE00" stroke-width="1.5" stroke-linejoin="round"/>`;

const FESTA = `
<g transform="rotate(-22 30 6)">
  <path d="M19 12 L 30 -18 L 41 12 Z" fill="#E8455A"/>
  <path d="M23 2 L 37 2 M26 -7 L 34 -7" stroke="#FFD43B" stroke-width="3" stroke-linecap="round"/>
  <circle cx="30" cy="-19" r="4.2" fill="#FFD43B"/>
  <path d="M18 12 Q 30 16 42 12" fill="none" stroke="#C7334A" stroke-width="2.4"/>
</g>
<g>
  <rect x="2" y="2" width="5" height="9" rx="1.5" fill="#2EA043" transform="rotate(25 4 6)"/>
  <rect x="88" y="-6" width="5" height="9" rx="1.5" fill="#7DB3FF" transform="rotate(-30 90 -2)"/>
  <rect x="96" y="40" width="5" height="9" rx="1.5" fill="#E8455A" transform="rotate(40 98 44)"/>
  <rect x="-6" y="52" width="5" height="9" rx="1.5" fill="#FFD43B" transform="rotate(-20 -4 56)"/>
  <circle cx="72" cy="-10" r="3" fill="#FF9E64"/><circle cx="-4" cy="26" r="2.6" fill="#B07CFF"/><circle cx="104" cy="22" r="2.6" fill="#2EA043"/>
</g>`;

const SUOR = `
<path d="M20 20 Q 50 6 80 20 L 80 27 Q 50 13 20 27 Z" fill="#E8455A"/>
<path d="M78 21 Q 92 16 96 24 M79 25 Q 90 28 92 36" fill="none" stroke="#E8455A" stroke-width="4" stroke-linecap="round"/>
<path d="M88 30 Q 84 39 88 42 Q 93 39 88 30 Z" fill="#7DCFFF" stroke="#3B9BDB" stroke-width="1"/>
<path d="M14 40 Q 11 46 14 48 Q 17 46 14 40 Z" fill="#7DCFFF" stroke="#3B9BDB" stroke-width="1"/>`;

const BASE: Record<Pose, keyof typeof PIPO> = { oculos: 'happy', raio: 'cheer', festa: 'cheer', suor: 'happy' };
const EXTRA: Record<Pose, string> = { oculos: OCULOS, raio: RAIO, festa: FESTA, suor: SUOR };

const CACHE: Partial<Record<Pose, string>> = {};
export function poseSvg(p: Pose) {
  if (!CACHE[p]) {
    const corpo = miolo(PIPO[BASE[p]]);
    // os acessórios de cabeça vão por cima; o raio e as linhas de velocidade, atrás
    const atras = p === 'raio' ? EXTRA[p] : '';
    const frente = p === 'raio' ? '' : EXTRA[p];
    CACHE[p] = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -26 132 128">${atras}${corpo}${frente}</svg>`;
  }
  return CACHE[p]!;
}
