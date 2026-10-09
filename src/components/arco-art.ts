// Arco e flecha em pixel art, desenhados por código (o pacote gratuito do herói não tem arco). Cada "pixel" é um retângulo
// de 1x1 num SVG com shape-rendering crispEdges, então escala em número inteiro sem borrar.

const sombra = (hex: string, f: number) => {
  const n = parseInt(hex.slice(1), 16);
  const c = (v: number) => Math.max(0, Math.min(255, Math.round(v * f)));
  return `#${[(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => c(v).toString(16).padStart(2, '0')).join('')}`;
};

export const ARCO_W = 18; // largura da arte, em pixels (o x vai de -6 a 11)
export const ARCO_H = 28;

/** Arco virado para a direita. `esticado`: a corda puxada para trás, com uma flecha encaixada. */
export function arcoSvg(hexOriginal: string, esticado = false): string {
  let hex = hexOriginal;
  const r: string[] = [];
  const px = (x: number, y: number, cor: string, w = 1, h = 1) => r.push(`<rect x="${x + 6}" y="${y}" width="${w}" height="${h}" fill="${cor}"/>`);
  // madeiras muito escuras somem no cenário: clareia o corpo do arco e põe um brilho na borda
  const n = parseInt(hex.slice(1), 16);
  const lum = (((n >> 16) & 255) * 0.3 + ((n >> 8) & 255) * 0.59 + (n & 255) * 0.11);
  if (lum < 110) hex = sombra(hex, 110 / Math.max(lum, 20));
  const escuro = sombra(hex, 0.55), claro = sombra(hex, 1.35);
  // braços do arco: uma curva que encosta para a direita no meio
  for (let y = 0; y < ARCO_H; y++) {
    const t = (y - 13.5) / 13.5;
    const x = Math.round(7 - t * t * 6);
    px(x - 1, y, escuro);
    px(x, y, hex);
    px(x + 1, y, y % 3 === 0 ? claro : hex);
  }
  px(5, 12, '#3b2a1c', 4, 5); // empunhadura
  px(5, 12, '#5b4330', 4, 1);
  // corda
  const corda = '#efe8d4';
  if (!esticado) for (let y = 1; y < ARCO_H - 1; y++) px(1, y, corda);
  else {
    // forma um "V" até o ponto de encaixe da flecha
    for (let k = 0; k <= 12; k++) { const x = Math.round(1 - (5 * k) / 12); px(x, 1 + k, corda); px(x, ARCO_H - 2 - k, corda); }
    // flecha encaixada, apontando para a direita
    px(-4, 13, '#c9a56a', 15, 1);
    px(-4, 12, '#d9534f', 3, 1); px(-4, 14, '#d9534f', 3, 1);
    px(11, 12, '#cfd5da', 1, 3); px(10, 13, '#cfd5da', 1, 1);
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${ARCO_W} ${ARCO_H}" shape-rendering="crispEdges">${r.join('')}</svg>`;
}

export const FLECHA_W = 20;
export const FLECHA_H = 5;
/** Flecha em voo, apontando para a direita. */
export const FLECHA_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${FLECHA_W} ${FLECHA_H}" shape-rendering="crispEdges">
<rect x="3" y="2" width="14" height="1" fill="#d6b27a"/>
<rect x="0" y="0" width="4" height="1" fill="#e5e5e5"/><rect x="1" y="1" width="3" height="1" fill="#d9534f"/>
<rect x="0" y="4" width="4" height="1" fill="#e5e5e5"/><rect x="1" y="3" width="3" height="1" fill="#d9534f"/>
<rect x="16" y="1" width="1" height="3" fill="#b9c2c9"/><rect x="17" y="2" width="3" height="1" fill="#e4e9ec"/><rect x="17" y="1" width="2" height="1" fill="#b9c2c9"/><rect x="17" y="3" width="2" height="1" fill="#b9c2c9"/>
</svg>`;
