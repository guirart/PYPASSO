import { Avatar as DBAvatar, Style } from '@dicebear/core';
import critters from '@dicebear/styles/critters.json';

/**
 * Avatares "Critters" (DiceBear, domínio público). O avatar do usuário é guardado
 * como texto: uma semente qualquer (avatar sorteado) ou "look:{...}" (montado no editor).
 */
type Def = { components: Record<string, { variants: Record<string, unknown> }>; colors: Record<string, { values: string[] }> };
const DEF = critters as unknown as Def;
export const CRITTERS = new Style(critters as ConstructorParameters<typeof Style>[0]);
const BASE = { animationVariant: 'none', borderRadius: 50 };

export type PartKey = 'body' | 'top' | 'eyes' | 'mouth' | 'pattern' | 'cheeks';
export type Look = Record<PartKey, string> & { bodyColor: string; accentColor: string; bg: string };

const LABELS: Record<string, string> = {
  // cabeça
  horns: 'Chifres', hornsIn: 'Chifres curvos', hornsSmall: 'Chifrinhos', spike: 'Ponta', antenna: 'Antena', antennae: 'Antenas',
  earsRound: 'Orelhas redondas', earsPointy: 'Orelhas pontudas', earsDroop: 'Orelhas caídas', spikes: 'Espinhos', fin: 'Barbatana',
  crown: 'Coroa', sprout: 'Broto', nub: 'Toquinho', bobble: 'Pompom',
  // corpo
  dome: 'Cúpula', block: 'Bloco', tower: 'Torre', chimney: 'Chaminé', squat: 'Baixinho', blob: 'Gota', round: 'Redondo', tilt: 'Inclinado',
  lean: 'Esguio', peak: 'Pico', bell: 'Sino', wedge: 'Cunha', wedgeInv: 'Cunha invertida', steps: 'Degraus',
  // detalhes
  belly: 'Barriga', dots: 'Bolinhas', speckles: 'Pintinhas', bar: 'Faixa', bars: 'Faixas', spot: 'Mancha', stripes: 'Listras',
  dotRow: 'Fileira', chevron: 'Divisas', ring: 'Anel', blush: 'Bochechas', blushBig: 'Bochechões', freckles: 'Sardas',
  // olhos
  bigPupils: 'Pupilas grandes', sideeye: 'De lado', inward: 'Vesgos', mono: 'Ciclope', uneven: 'Desiguais', trio: 'Três olhos',
  threeRow: 'Três em fila', four: 'Quatro olhos', happy: 'Felizes', closedLine: 'Fechados', wink: 'Piscando', squint: 'Apertados',
  wide: 'Arregalados', sleepy: 'Sonolentos', angry: 'Bravos', monoSleepy: 'Ciclope com sono', close: 'Juntinhos',
  // boca
  smile: 'Sorriso', tinySmile: 'Sorrisinho', grin: 'Sorrisão', laugh: 'Risada', teeth: 'Dentes', ooh: 'Ó', line: 'Reta', smirk: 'De canto',
  wavy: 'Ondulada', catMouth: 'De gato', zigzag: 'Zigue-zague', frown: 'Bico', sad: 'Triste', slant: 'Torta', dot: 'Pontinho',
  open: 'Aberta', tooth: 'Dentinho', tongue: 'Língua', blep: 'Linguinha', none: 'Nada',
};
// Alguns nomes aparecem em mais de uma parte com sentidos diferentes.
const BY_PART: Partial<Record<PartKey, Record<string, string>>> = { eyes: { round: 'Redondos', dots: 'Pontinhos' } };
export const partLabel = (v: string, part?: PartKey) => (part && BY_PART[part]?.[v]) ?? LABELS[v] ?? v;

const variants = (k: string) => Object.keys(DEF.components[k]?.variants ?? {});
export const PARTS: { key: PartKey; label: string; options: string[] }[] = [
  { key: 'body', label: 'Corpo', options: variants('body') },
  { key: 'top', label: 'Cabeça', options: ['none', ...variants('top')] },
  { key: 'eyes', label: 'Olhos', options: variants('eyes') },
  { key: 'mouth', label: 'Boca', options: variants('mouth') },
  { key: 'pattern', label: 'Desenho', options: ['none', ...variants('pattern')] },
  { key: 'cheeks', label: 'Bochechas', options: ['none', ...variants('cheeks')] },
];
export const COLORS = {
  bg: DEF.colors.background.values,
  bodyColor: DEF.colors.body.values,
  accentColor: DEF.colors.accent.values,
};

/** Itens raros, liberados ao alcançar uma liga (ver src/lib/leagues.ts). */
export const LOCKED: Partial<Record<PartKey, Record<string, number>>> = {
  top: { crown: 3, fin: 6 },
  eyes: { four: 5 },
};
export const lockTier = (part: PartKey, v: string) => LOCKED[part]?.[v] ?? 0;

export function lookToOptions(l: Look): Record<string, unknown> {
  const o: Record<string, unknown> = {
    ...BASE,
    bodyVariant: l.body, eyesVariant: l.eyes, mouthVariant: l.mouth,
    bodyColor: [l.bodyColor], accentColor: [l.accentColor], backgroundColor: [l.bg],
  };
  for (const k of ['top', 'pattern', 'cheeks'] as const) {
    if (l[k] === 'none') o[`${k}Probability`] = 0;
    else { o[`${k}Variant`] = l[k]; o[`${k}Probability`] = 100; }
  }
  return o;
}

export const encodeLook = (l: Look) => `look:${JSON.stringify(l)}`;
export function decodeLook(s: string): Look | null {
  if (!s.startsWith('look:')) return null;
  try { return JSON.parse(s.slice(5)) as Look; } catch { return null; }
}

/** Opções do DiceBear para um avatar salvo (semente ou look montado). */
export function avatarOptions(saved: string): Record<string, unknown> {
  const look = decodeLook(saved);
  return look ? lookToOptions(look) : { ...BASE, seed: saved, topProbability: 100, patternProbability: 100, cheeksProbability: 100 };
}
/**
 * O DiceBear gera ids iguais (clip, símbolos) para avatares parecidos. Na web, vários
 * SVGs na mesma página com o mesmo id "roubam" as partes uns dos outros — então
 * cada SVG ganha ids únicos.
 */
let svgN = 0;
export function uniqueIds(svg: string): string {
  const n = `u${++svgN}`;
  return svg.replace(/id="([^"]+)"/g, `id="$1-${n}"`).replace(/url\(#([^)]+)\)/g, `url(#$1-${n})`).replace(/href="#([^"]+)"/g, `href="#$1-${n}"`);
}
export const avatarSvg = (saved: string) => uniqueIds(new DBAvatar(CRITTERS, avatarOptions(saved)).toString());
export const lookSvg = (l: Look) => uniqueIds(new DBAvatar(CRITTERS, lookToOptions(l)).toString());

/** Descobre as partes de qualquer avatar salvo, para abrir no editor. */
export function resolveLook(saved: string): Look {
  const direct = decodeLook(saved);
  if (direct) return direct;
  const o = (new DBAvatar(CRITTERS, avatarOptions(saved)).toJSON() as { options: Record<string, unknown> }).options;
  const first = (v: unknown, fb: string) => (Array.isArray(v) ? String(v[0]) : typeof v === 'string' ? v : fb);
  return {
    body: first(o.bodyVariant, 'round'), top: first(o.topVariant, 'none'), eyes: first(o.eyesVariant, 'happy'),
    mouth: first(o.mouthVariant, 'smile'), pattern: first(o.patternVariant, 'none'), cheeks: first(o.cheeksVariant, 'none'),
    bodyColor: first(o.bodyColor, COLORS.bodyColor[0]), accentColor: first(o.accentColor, COLORS.accentColor[1]), bg: first(o.backgroundColor, COLORS.bg[0]),
  };
}

const pick = <T,>(a: T[]) => a[Math.floor(Math.random() * a.length)];
/** Sorteia um look respeitando os itens bloqueados. */
export function randomLook(league: number): Look {
  const ok = (k: PartKey) => PARTS.find((p) => p.key === k)!.options.filter((v) => lockTier(k, v) <= league && (k === 'top' || k === 'body' || k === 'eyes' || k === 'mouth' ? v !== 'none' : true));
  const bodyColor = pick(COLORS.bodyColor);
  return {
    body: pick(ok('body')), top: pick(ok('top')), eyes: pick(ok('eyes')), mouth: pick(ok('mouth')),
    pattern: pick(ok('pattern')), cheeks: pick(ok('cheeks')), bodyColor,
    accentColor: pick(COLORS.accentColor.filter((c) => c !== bodyColor)), bg: pick(COLORS.bg),
  };
}
