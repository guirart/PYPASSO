/**
 * Livro da Biblioteca (capa dura bege, com moldura dourada), desenhado em SVG.
 * Três camadas: a base (contracapa, páginas e fitinha), a capa por fora e a capa por dentro.
 * A capa gira pela lombada para abrir e fechar (src/components/VooBiblioteca.tsx).
 */
export const LIVRO_W = 118;
export const LIVRO_H = 88;

const BEGE = '#E9D6AF';
const BEGE_ESCURO = '#CDB284';
const BORDA = '#A9834A';
const OURO = '#B98B3A';
const MARROM = '#6B4A25';

/** Contracapa + bloco de páginas (com o "texto" que aparece quando o livro abre) + fitinha. */
export const LIVRO_BASE = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 118 104">
<ellipse cx="60" cy="99" rx="54" ry="4.5" fill="#000" opacity=".12"/>
<rect x="1" y="5" width="116" height="86" rx="9" fill="${BEGE_ESCURO}"/>
<rect x="1" y="5" width="116" height="86" rx="9" fill="none" stroke="${BORDA}" stroke-width="1.6"/>
<rect x="5" y="2" width="108" height="82" rx="4" fill="#FFF9EC"/>
<g stroke="#E6D9BE" stroke-width="1"><path d="M110 6 V80 M107.5 5 V82 M8 81 H108 M8 78.5 H108"/></g>
<g stroke-linecap="round" stroke-width="3">
  <path d="M16 16 H72" stroke="#D8C7A5"/><path d="M16 25 H90" stroke="#E2D4B7"/><path d="M16 34 H84" stroke="#E2D4B7"/>
  <path d="M16 45 H32" stroke="#E07B39"/><path d="M36 45 H60" stroke="#2F6FD6"/><path d="M64 45 H80" stroke="#2E9E5B"/>
  <path d="M22 54 H52" stroke="#2F6FD6"/><path d="M56 54 H74" stroke="#E07B39"/>
  <path d="M16 65 H88" stroke="#E2D4B7"/><path d="M16 73 H62" stroke="#E2D4B7"/>
</g>
<path d="M88 78 h9 v24 l-4.5 -4.5 l-4.5 4.5 z" fill="#D9473F"/><path d="M88 78 h9 v3 h-9 z" fill="#A92E28"/>
</svg>`;

/** Capa por fora: bege com moldura dourada, cantoneiras, emblema e título. */
export const LIVRO_CAPA = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 118 88">
<rect x="0.8" y="0.8" width="116.4" height="86.4" rx="9" fill="${BEGE}" stroke="${BORDA}" stroke-width="1.6"/>
<rect x="0.8" y="0.8" width="12" height="86.4" rx="6" fill="${BEGE_ESCURO}"/>
<path d="M2 14 H12 M2 74 H12" stroke="${BORDA}" stroke-width="1.6"/>
<path d="M12.8 2 V86" stroke="${BORDA}" stroke-width="1.2" opacity=".6"/>
<rect x="20" y="7" width="91" height="74" rx="5" fill="none" stroke="${OURO}" stroke-width="1.6"/>
<rect x="23.5" y="10.5" width="84" height="67" rx="3.5" fill="none" stroke="${OURO}" stroke-width=".8" opacity=".8"/>
<g fill="${OURO}">
  <path d="M20 7 l7 0 l-7 7 z"/><path d="M111 7 l-7 0 l7 7 z"/><path d="M20 81 l7 0 l-7 -7 z"/><path d="M111 81 l-7 0 l7 -7 z"/>
</g>
<text x="65.5" y="22" text-anchor="middle" font-family="Georgia, serif" font-weight="700" font-size="7.2" letter-spacing="1.6" fill="${MARROM}">BIBLIOTECA</text>
<path d="M44 26 H87" stroke="${OURO}" stroke-width=".9"/>
<circle cx="65.5" cy="48" r="15" fill="#F6EBD3" stroke="${OURO}" stroke-width="1.8"/>
<circle cx="65.5" cy="48" r="11.5" fill="none" stroke="${OURO}" stroke-width=".7" stroke-dasharray="1.5 1.5"/>
<text x="65.5" y="52.5" text-anchor="middle" font-family="ui-monospace, Menlo, monospace" font-weight="800" font-size="12" fill="#2F6FD6">Py</text>
<g fill="${OURO}"><path d="M46 48 l3 -2 l3 2 l-3 2 z"/><path d="M79 48 l3 -2 l3 2 l-3 2 z"/></g>
<path d="M44 70 H87" stroke="${OURO}" stroke-width=".9"/>
<text x="65.5" y="77" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="5.2" fill="${MARROM}">do PyPasso</text>
</svg>`;

/** Capa por dentro (aparece quando o livro está aberto): guarda marmorizada clarinha. */
export const LIVRO_CAPA_DENTRO = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 118 88">
<rect x="0.8" y="0.8" width="116.4" height="86.4" rx="9" fill="${BEGE_ESCURO}" stroke="${BORDA}" stroke-width="1.6"/>
<rect x="6" y="5" width="106" height="78" rx="4" fill="#F4E7CB"/>
<g fill="none" stroke="#E2CFA6" stroke-width="2" stroke-linecap="round" opacity=".9">
  <path d="M12 20 Q 30 10 48 20 T 84 20 T 108 18"/><path d="M12 40 Q 34 30 56 40 T 106 38"/><path d="M12 62 Q 28 52 46 62 T 82 62 T 108 60"/>
</g>
</svg>`;
