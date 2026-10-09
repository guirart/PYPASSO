import { useEffect, useRef, useState } from 'react';
import type { BossMood } from '../boss-art';
import type { EnemyId } from '../enemy-art';
import { SPRITES } from '../inimigos-sprites';
import { SpriteQuadro } from './SpriteQuadro';

export { AREA_H, AREA_W } from './SpriteQuadro';
const HURT_MS = 550;
const IDLE_MS = 130; // tempo de cada quadro da animação parada

/**
 * Inimigo em pixel art. Parado repete o ciclo, ao atacar toca a folha de ataque no ritmo de `t` (0 a 1),
 * e ferido toca a de dano. O inimigo olha para a esquerda, para quem está lutando.
 */
export function SpriteInimigo({ id, mood = 'normal', t = 0, morto = false }: { id: EnemyId; mood?: BossMood; t?: number; morto?: boolean }) {
  const sp = SPRITES[id];
  const [agora, setAgora] = useState(() => Date.now());
  const inicioDano = useRef(0);
  const inicioMorte = useRef(0);

  useEffect(() => {
    const iv = setInterval(() => setAgora(Date.now()), 60);
    return () => clearInterval(iv);
  }, []);
  useEffect(() => { if (mood === 'hurt') inicioDano.current = Date.now(); }, [mood]);
  useEffect(() => { if (morto) inicioMorte.current = Date.now(); }, [morto]);

  const folha = morto ? sp.morte : mood === 'attack' ? sp.ataque : mood === 'hurt' ? sp.dano : sp.idle;
  const n = folha.quadros;
  // morto: toca a folha de morte uma vez e fica no último quadro
  const quadro = morto ? Math.min(n - 1, Math.floor((agora - inicioMorte.current) / 110)) : mood === 'attack' ? Math.floor(t * n)
    : mood === 'hurt' ? Math.floor(((agora - inicioDano.current) / HURT_MS) * n)
    : Math.floor(agora / IDLE_MS) % n;
  return <SpriteQuadro folha={folha} escala={sp.escala} cx={sp.cx} pe={sp.pe} quadro={quadro} espelhar />;
}
