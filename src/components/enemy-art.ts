// Os inimigos das batalhas do mapa: monstrinhos de erros de Python. A arte (pixel art) vem do
// Tiny RPG Character Asset Pack 02; veja inimigos-sprites.ts e o componente SpriteInimigo.
export const ENEMY_IDS = ['morcego', 'fogofatuo', 'bruxo', 'olho', 'cao', 'lodo', 'monstro', 'golem'] as const;
export type EnemyId = (typeof ENEMY_IDS)[number];
export const ENEMIES: Record<EnemyId, { nome: string; fala: string }> = {
  morcego: { nome: 'Morcego Bugado', fala: 'Um errinho aqui, outro ali...' },
  fogofatuo: { nome: 'Fogo-fátuo do Typo', fala: 'Escrevi errado de propósito.' },
  bruxo: { nome: 'Bruxo do Tab', fala: 'Quatro espaços ou um tab? Mistério.' },
  olho: { nome: 'Olho das Aspas', fala: 'Abri e esqueci de fechar.' },
  cao: { nome: 'Cão do Loop', fala: 'Correndo em círculos...' },
  lodo: { nome: 'Lodo None', fala: 'Eu não retorno nada.' },
  monstro: { nome: 'Monstro Torto', fala: 'Ssserá que indentou?' },
  golem: { nome: 'Golem do Crash', fala: 'Cuidado com o traceback!' },
};
