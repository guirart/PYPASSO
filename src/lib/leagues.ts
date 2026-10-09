/**
 * Ligas de evolução do PyPasso. Cada semana, 15 pessoas disputam XP numa liga:
 * as 5 primeiras sobem, as 3 últimas descem (na Bronze ninguém desce).
 */
export type League = {
  tier: number; // 1..10
  gem: string; // nome da liga
  title: string; // título engraçado
  joke: string;
  emblem: string; // símbolo no troféu
  c1: string; // cor clara
  c2: string; // cor escura
  ink: string; // cor do símbolo
  hero: string; // fundo do cabeçalho (contraste com texto branco)
};

export const LEAGUES: League[] = [
  { tier: 1, gem: 'Bronze', title: 'Noob', joke: 'Ainda acha que Python é só uma cobra', emblem: '?', c1: '#E8A15C', c2: '#9A5B26', ink: '#5A3412' , hero: '#8A4F1E' },
  { tier: 2, gem: 'Prata', title: 'Vibecoder', joke: 'Programa no feeling e reza pra rodar', emblem: '~', c1: '#E6EBF0', c2: '#8E99A4', ink: '#4B5560' , hero: '#5F6B77' },
  { tier: 3, gem: 'Ouro', title: 'Caçador de Bugs', joke: 'Já sabe que o erro é na linha de cima', emblem: '!', c1: '#FFD95C', c2: '#C99200', ink: '#6B4A00' , hero: '#9A6B00' },
  { tier: 4, gem: 'Safira', title: 'Rei do print()', joke: 'Debuga tudo com print("aqui")', emblem: '( )', c1: '#7DB2FF', c2: '#1D4ED8', ink: '#0B2A78' , hero: '#1D4ED8' },
  { tier: 5, gem: 'Rubi', title: 'Domador de Indentação', joke: '4 espaços. Nem mais, nem menos', emblem: '⇥', c1: '#FF7A93', c2: '#BE123C', ink: '#5E0A1E' , hero: '#BE123C' },
  { tier: 6, gem: 'Esmeralda', title: 'Mago dos Laços', joke: 'for dentro de for sem perder a cabeça', emblem: '∞', c1: '#5EE6B0', c2: '#047857', ink: '#023D2C' , hero: '#047857' },
  { tier: 7, gem: 'Ametista', title: 'Lorde das Funções', joke: 'Repetiu duas vezes? Vira def', emblem: 'def', c1: '#D3A6FF', c2: '#7C3AED', ink: '#3B1278' , hero: '#6D28D9' },
  { tier: 8, gem: 'Pérola', title: 'Arquiteto de Classes', joke: 'self é seu melhor amigo', emblem: '{ }', c1: '#FFFDF7', c2: '#C9BBA0', ink: '#6E6047' , hero: '#7D6C4C' },
  { tier: 9, gem: 'Obsidiana', title: 'Sênior Movido a Café', joke: '"Na minha máquina funciona"', emblem: '☕', c1: '#6B7280', c2: '#111827', ink: '#E9D5FF' , hero: '#111827' },
  { tier: 10, gem: 'Diamante', title: 'Lenda Pythônica', joke: 'Sabe o import this de cor', emblem: '>>>', c1: '#B5F5FF', c2: '#0891B2', ink: '#05445A' , hero: '#0E7490' },
];

export const leagueOf = (tier: number) => LEAGUES[Math.min(Math.max(tier, 1), LEAGUES.length) - 1];
export const GROUP_SIZE = 15;
export const PROMOTE = 5;
export const DEMOTE = 3;

/** Desenho do troféu em SVG (usado no app e para gerar imagens). */
export function trophySvg(tier: number, opts: { locked?: boolean } = {}): string {
  const L = leagueOf(tier);
  const c1 = opts.locked ? '#C8D0D8' : L.c1;
  const c2 = opts.locked ? '#8F9AA5' : L.c2;
  const ink = opts.locked ? '#6B7681' : L.ink;
  const id = `t${tier}${opts.locked ? 'l' : ''}`;
  const fs = L.emblem.length >= 3 ? 12.5 : L.emblem.length === 2 ? 18 : 24;
  const sparkle = tier >= 8 && !opts.locked
    ? `<path d="M80 14l2.2 5.8 5.8 2.2-5.8 2.2L80 30l-2.2-5.8L72 22l5.8-2.2z" fill="#fff" opacity=".95"/><path d="M18 38l1.4 3.6 3.6 1.4-3.6 1.4L18 48l-1.4-3.6L13 43l3.6-1.4z" fill="#fff" opacity=".85"/>`
    : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
<defs>
<linearGradient id="${id}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/></linearGradient>
<linearGradient id="${id}b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c2}"/><stop offset="1" stop-color="${opts.locked ? '#6F7A85' : shade(c2)}"/></linearGradient>
</defs>
<path d="M26 22 C10 22 8 46 30 50" fill="none" stroke="${c2}" stroke-width="7" stroke-linecap="round"/>
<path d="M74 22 C90 22 92 46 70 50" fill="none" stroke="${c2}" stroke-width="7" stroke-linecap="round"/>
<path d="M24 14 H76 V34 C76 52 64 62 50 62 C36 62 24 52 24 34 Z" fill="url(#${id}g)"/>
<path d="M31 18 H39 V34 C39 44 43 50 47 54 C36 52 31 44 31 34 Z" fill="#fff" opacity=".35"/>
<rect x="44" y="61" width="12" height="11" fill="${c2}"/>
<path d="M34 72 H66 L70 84 H30 Z" fill="url(#${id}b)"/>
<rect x="26" y="83" width="48" height="8" rx="3" fill="${c2}"/>
${L.emblem === '☕'
    ? `<path d="M39 30 H57 V40 C57 45 53 48 48 48 C43 48 39 45 39 40 Z" fill="${ink}"/><path d="M57 32 C63 32 63 41 57 41" fill="none" stroke="${ink}" stroke-width="2.6"/><path d="M44 21 C42 24 46 25 44 28 M50 20 C48 23 52 24 50 27" fill="none" stroke="${ink}" stroke-width="2" stroke-linecap="round"/>`
    : `<text x="50" y="${41 + fs * 0.12}" font-family="Menlo, Consolas, monospace" font-weight="700" font-size="${fs}" text-anchor="middle" fill="${ink}">${esc(L.emblem)}</text>`}
${sparkle}
</svg>`;
}

function shade(hex: string) {
  const n = parseInt(hex.slice(1), 16);
  const f = (v: number) => Math.max(0, Math.round(v * 0.7));
  return `#${[(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => f(v).toString(16).padStart(2, '0')).join('')}`;
}
const esc = (s: string) => s.replace(/</g, '‹'); // só < precisa de cuidado; o leitor de SVG do app não decodifica entidades

// ---------------------------------------------------------------- semanas
/** Segunda-feira 00:00 (horário local) da semana da data. */
export function weekStart(d = new Date()) {
  const s = new Date(d.getFullYear(), d.getMonth(), d.getDate());
  const dow = (s.getDay() + 6) % 7; // segunda = 0
  s.setDate(s.getDate() - dow);
  return s;
}
export const weekId = (d = new Date()) => {
  const s = weekStart(d);
  return `${s.getFullYear()}-${String(s.getMonth() + 1).padStart(2, '0')}-${String(s.getDate()).padStart(2, '0')}`;
};
export function weekEnd(d = new Date()) {
  const e = weekStart(d);
  e.setDate(e.getDate() + 7);
  return e;
}
/** Quanto da semana já passou (0 a 1). */
export function weekProgress(d = new Date()) {
  const s = weekStart(d).getTime();
  return Math.min(1, Math.max(0, (d.getTime() - s) / (7 * 24 * 3600 * 1000)));
}
export function timeLeft(d = new Date()) {
  const ms = weekEnd(d).getTime() - d.getTime();
  const h = Math.floor(ms / 3600000);
  const days = Math.floor(h / 24);
  return days >= 1 ? `${days}d ${h % 24}h` : `${h}h ${Math.floor((ms % 3600000) / 60000)}min`;
}

// ---------------------------------------------------------------- rivais (modo offline)
/** Gerador pseudoaleatório determinístico. */
function rng(seed: string) {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i++) h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
  return () => {
    h = Math.imul(h ^ (h >>> 15), 2246822507);
    h = Math.imul(h ^ (h >>> 13), 3266489909);
    return ((h ^= h >>> 16) >>> 0) / 4294967296;
  };
}

const NAMES = ['Marina', 'Lucas', 'Júlia', 'Pedro', 'Rafa', 'Duda', 'Gabi', 'Theo', 'Nina', 'Igor', 'Luna', 'Davi', 'Malu', 'Enzo', 'Clara',
  'Bento', 'Lívia', 'Heitor', 'Iris', 'Otávio', 'Zoe', 'Caetano', 'Maya', 'Benício', 'Alice', 'Vicente', 'Lara', 'Joca', 'Pietra', 'Ravi'];
const CAST_IDS = ['ana', 'caio', 'bia', 'teo'] as const;

export type Rival = { id: string; name: string; seed: string; cast?: (typeof CAST_IDS)[number]; xp: number; me?: boolean };

/**
 * 14 rivais para a semana e liga indicadas. O XP de cada um cresce ao longo
 * da semana (sempre igual para a mesma semana), então a liga parece viva.
 */
export function rivalsFor(week: string, tier: number, progress = weekProgress()): Rival[] {
  const r = rng(`${week}#${tier}`);
  const pool = [...NAMES];
  const out: Rival[] = [];
  const castPick = CAST_IDS.filter(() => r() < 0.6);
  const scale = 0.5 + (tier - 1) * 0.22; // Bronze é fácil; cada liga acima tem rivais mais fortes
  for (let i = 0; i < GROUP_SIZE - 1; i++) {
    const cast = castPick[i];
    const name = cast ? { ana: 'Ana', caio: 'Caio', bia: 'Bia', teo: 'Téo' }[cast] : pool.splice(Math.floor(r() * pool.length), 1)[0];
    const kind = r();
    // perfis: sumido, casual, constante, viciado
    const target = kind < 0.18 ? r() * 15 : kind < 0.5 ? 30 + r() * 60 : kind < 0.85 ? 80 + r() * 90 : 160 + r() * 140;
    const curve = 0.6 + r() * 0.9; // uns começam rápido, outros deixam pro fim
    const xp = Math.round((target * scale * Math.pow(progress, curve)) / 5) * 5;
    out.push({ id: `bot${i}`, name, seed: `${name}-${tier}-${i}`, cast, xp });
  }
  return out;
}

export type Zone = 'promo' | 'safe' | 'demo';
export function zoneOf(rank: number, tier: number, size = GROUP_SIZE): Zone {
  if (rank <= PROMOTE && tier < LEAGUES.length) return 'promo';
  if (rank > size - DEMOTE && tier > 1) return 'demo';
  return 'safe';
}

/** Ordena a liga com você dentro (empates: você fica na frente). */
export function standings(rivals: Rival[], me: { name: string; seed: string; xp: number }): Rival[] {
  return [...rivals, { id: 'me', name: me.name || 'Você', seed: me.seed, xp: me.xp, me: true }]
    .sort((a, b) => b.xp - a.xp || (a.me ? -1 : b.me ? 1 : 0));
}

export type WeekResult = { week: string; from: number; to: number; rank: number; xp: number };

/** Fecha a semana: decide se sobe, fica ou desce. */
export function closeWeek(week: string, tier: number, me: { name: string; seed: string; xp: number }): WeekResult {
  const table = standings(rivalsFor(week, tier, 1), me);
  const rank = table.findIndex((x) => x.me) + 1;
  const z = zoneOf(rank, tier);
  const to = z === 'promo' && me.xp > 0 ? tier + 1 : z === 'demo' ? tier - 1 : tier;
  return { week, from: tier, to, rank, xp: me.xp };
}

/** Comentário do Pipo sobre a sua situação na liga. */
export function pipoLeagueLine(rank: number, tier: number, table: Rival[]): string {
  const me = table[rank - 1];
  const z = zoneOf(rank, tier, table.length);
  const next = tier < LEAGUES.length ? leagueOf(tier + 1) : null;
  if (!me.xp) return 'Ainda sem XP nesta semana! Uma lição rapidinha já te coloca no jogo.';
  if (z === 'promo' && rank === 1) return next ? `Você tá liderando! Segura o 1º lugar e vira ${next.title}.` : 'Primeiro lugar na liga mais alta. Lenda viva!';
  if (z === 'promo') return next ? `Zona de promoção! Fica no top ${PROMOTE} até domingo e você vira ${next.title}.` : 'Você está entre os melhores da liga Diamante!';
  if (z === 'demo') {
    const safe = table[table.length - DEMOTE - 1];
    const gap = Math.max(5, safe.xp - me.xp + 5);
    return `Eita, zona de rebaixamento! Faltam ${gap} XP pra sair do perigo... uma lição resolve.`;
  }
  const target = table[Math.min(PROMOTE, table.length) - 1];
  const gap = Math.max(5, target.xp - me.xp + 5);
  return next ? `Faltam ${gap} XP pra entrar na zona de promoção e virar ${next.title}.` : `Faltam ${gap} XP pro top ${PROMOTE} da liga Diamante.`;
}
