import { PIPO } from './pipo-art';

/**
 * Cenas do Pipo que enfeitam os espaços vazios da trilha (estilo das cenas de personagem do
 * Duolingo). Cada cena abre um exercício especial:
 *  - "lendo": Pipo lendo um livro  → Leitura de código (perguntas sobre um trecho)
 *  - "digitando": Pipo no computador → Digitação de código (copiar um trecho, contra o relógio)
 * Desenho próprio, montado sobre o Pipo (mascote original do PyPasso).
 */
export type Cena = 'lendo' | 'digitando';

const corpo = (olhar: 'baixo' | 'direita') => {
  let s = PIPO.happy.replace(/^<svg[^>]*>/, '').replace(/<\/svg>\s*$/, '');
  // Move as pupilas (e os brilhos) para o Pipo olhar para o livro ou para a tela.
  const [dx, dy] = olhar === 'baixo' ? [0, 3.2] : [3, 1];
  s = s.replace(/<circle cx="([\d.]+)" cy="([\d.]+)" r="(7|2\.6|1\.2)"/g, (_m, cx, cy, r) =>
    `<circle cx="${(+cx + dx).toFixed(1)}" cy="${(+cy + dy).toFixed(1)}" r="${r}"`);
  return s;
};

const LENDO = () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 150">
<ellipse cx="85" cy="138" rx="72" ry="9" fill="#000" opacity=".10"/>
<!-- pilha de livros -->
<rect x="118" y="112" width="44" height="12" rx="2.5" fill="#2E9E5B"/><rect x="118" y="112" width="44" height="3.5" rx="1.5" fill="#46C077"/>
<rect x="122" y="100" width="38" height="12" rx="2.5" fill="#E8455A"/><rect x="122" y="100" width="38" height="3.5" rx="1.5" fill="#FF6B7A"/>
<rect x="116" y="124" width="48" height="13" rx="2.5" fill="#FFC83D"/><rect x="116" y="124" width="48" height="3.5" rx="1.5" fill="#FFE08A"/>
<rect x="150" y="100" width="4" height="12" fill="#fff" opacity=".7"/>
<!-- Pipo -->
<g transform="translate(18 22) scale(1.12)">${corpo('baixo')}</g>
<!-- livro aberto na frente -->
<path d="M36 96 L80 104 L80 134 L33 126 Z" fill="#1D4C9C"/>
<path d="M124 96 L80 104 L80 134 L127 126 Z" fill="#1D4C9C"/>
<path d="M40 94 Q 60 92 80 101 L80 130 Q 60 121 37 122 Z" fill="#FFFDF5"/>
<path d="M120 94 Q 100 92 80 101 L80 130 Q 100 121 123 122 Z" fill="#F4EEDD"/>
<path d="M80 101 L80 130" stroke="#D8CDB0" stroke-width="1.5"/>
<g stroke-linecap="round" stroke-width="2.2">
  <path d="M46 101 L70 104" stroke="#FF9E64"/><path d="M46 107 L64 109" stroke="#2F6FD6"/>
  <path d="M50 113 L74 116" stroke="#2E9E5B"/><path d="M46 119 L60 120" stroke="#2F6FD6"/>
  <path d="M90 104 L113 101" stroke="#2F6FD6"/><path d="M90 110 L108 108" stroke="#E8455A"/>
  <path d="M94 116 L116 113" stroke="#2E9E5B"/>
</g>
<text x="99" y="120" font-family="monospace" font-weight="700" font-size="8" fill="#1D4C9C">py</text>
</svg>`;

const DIGITANDO = () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 170 150">
<ellipse cx="85" cy="140" rx="74" ry="8" fill="#000" opacity=".10"/>
<!-- mesa -->
<rect x="6" y="118" width="158" height="9" rx="4" fill="#B7794A"/><rect x="6" y="118" width="158" height="3" rx="1.5" fill="#D39867"/>
<rect x="16" y="127" width="7" height="14" fill="#8C5A33"/><rect x="147" y="127" width="7" height="14" fill="#8C5A33"/>
<!-- monitor com código -->
<rect x="96" y="44" width="68" height="50" rx="6" fill="#16212B"/>
<rect x="100" y="48" width="60" height="40" rx="3" fill="#14202B"/>
<g stroke-linecap="round" stroke-width="2.6">
  <path d="M105 55 L118 55" stroke="#FF9E64"/><path d="M121 55 L140 55" stroke="#FFD866"/>
  <path d="M110 62 L128 62" stroke="#7DCFFF"/><path d="M131 62 L150 62" stroke="#9ECE6A"/>
  <path d="M110 69 L122 69" stroke="#FF9E64"/><path d="M125 69 L146 69" stroke="#9ECE6A"/>
  <path d="M105 76 L130 76" stroke="#6F8496"/><path d="M105 82 L113 82" stroke="#2EA043"/>
</g>
<rect x="114" y="82" width="5" height="3" fill="#E4ECF2"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
<path d="M124 94 L136 94 L139 112 L121 112 Z" fill="#2B3742"/><rect x="113" y="111" width="34" height="5" rx="2.5" fill="#2B3742"/>
<!-- caneca de café -->
<path d="M14 100 L32 100 L30 117 L16 117 Z" fill="#fff"/><path d="M32 104 Q 39 104 38 109 Q 37 113 31 113" fill="none" stroke="#fff" stroke-width="3"/>
<path d="M14 100 L32 100 L31.6 104 L14.4 104 Z" fill="#E8455A"/>
<path d="M19 95 Q 17 90 20 86 M25 95 Q 23 90 26 86" fill="none" stroke="#B9C7D3" stroke-width="2" stroke-linecap="round"/>
<!-- Pipo -->
<g transform="translate(26 12) scale(1.02)">${corpo('direita')}</g>
<!-- teclado -->
<rect x="44" y="106" width="64" height="12" rx="3" fill="#D5DEE6"/><rect x="44" y="114" width="64" height="4" rx="2" fill="#AEBBC7"/>
<g fill="#fff">${Array.from({ length: 9 }, (_, i) => `<rect x="${47.5 + i * 6.6}" y="108" width="4.6" height="3" rx=".8"/>`).join('')}
<rect x="58" y="112" width="34" height="2.6" rx="1"/></g>
</svg>`;

/** Desenho em tons de cinza (cena ainda bloqueada). */
const cinza = (svg: string) =>
  svg.replace(/#([0-9a-f]{6})\b/gi, (_m, h) => {
    const n = parseInt(h, 16);
    const l = Math.round(0.3 * (n >> 16) + 0.59 * ((n >> 8) & 255) + 0.11 * (n & 255));
    const v = Math.round(120 + (l / 255) * 95); // tudo num cinza claro e suave
    const c = v.toString(16).padStart(2, '0');
    return `#${c}${c}${c}`;
  }).replace(/<animate[^>]*\/>/g, '');

const CACHE: Record<string, string> = {};
export function cenaSvg(cena: Cena, bloqueada = false) {
  const k = `${cena}-${bloqueada}`;
  if (!CACHE[k]) {
    const s = cena === 'lendo' ? LENDO() : DIGITANDO();
    CACHE[k] = bloqueada ? cinza(s) : s;
  }
  return CACHE[k];
}
