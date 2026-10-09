// Tipos dos chefes. A arte (pixel art) vem do Tiny RPG Character Asset Pack 02; veja chefes-sprites.ts e ChefeArena.tsx.
export type BossMood = 'normal' | 'attack' | 'hurt';
export const BOSS_IDS = ['aranha', 'besouro', 'escaravelho', 'centopeia', 'gosma', 'diabrete', 'caveira', 'lodo', 'golem', 'dragao'] as const;
export type BossId = (typeof BOSS_IDS)[number];
