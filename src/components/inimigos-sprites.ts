// Sprites dos inimigos das batalhas: Tiny RPG Character Asset Pack 02 (pixel art, quadros de 100x100 lado a lado).
// Gerado a partir das medidas das imagens: escala inteira (para os pixels ficarem nítidos), e a coluna e a linha onde ficam os pés.
import type { ImageSourcePropType } from 'react-native';
import type { EnemyId } from './enemy-art';

export type Folha = { src: ImageSourcePropType; quadros: number };
export type Sprite = { idle: Folha; ataque: Folha; dano: Folha; morte: Folha; escala: number; cx: number; pe: number };

export const SPRITES: Record<EnemyId, Sprite> = {
  morcego: { idle: { src: require('../../assets/inimigos/morcego/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/morcego/ataque.png'), quadros: 6 }, dano: { src: require('../../assets/inimigos/morcego/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/morcego/morte.png'), quadros: 4 }, escala: 4, cx: 48.5, pe: 54 },
  fogofatuo: { idle: { src: require('../../assets/inimigos/fogofatuo/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/fogofatuo/ataque.png'), quadros: 6 }, dano: { src: require('../../assets/inimigos/fogofatuo/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/fogofatuo/morte.png'), quadros: 6 }, escala: 4, cx: 52, pe: 52 },
  bruxo: { idle: { src: require('../../assets/inimigos/bruxo/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/bruxo/ataque.png'), quadros: 7 }, dano: { src: require('../../assets/inimigos/bruxo/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/bruxo/morte.png'), quadros: 11 }, escala: 4, cx: 50, pe: 57 },
  olho: { idle: { src: require('../../assets/inimigos/olho/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/olho/ataque.png'), quadros: 8 }, dano: { src: require('../../assets/inimigos/olho/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/olho/morte.png'), quadros: 4 }, escala: 6, cx: 50, pe: 57 },
  cao: { idle: { src: require('../../assets/inimigos/cao/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/cao/ataque.png'), quadros: 8 }, dano: { src: require('../../assets/inimigos/cao/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/cao/morte.png'), quadros: 4 }, escala: 4, cx: 50, pe: 56 },
  lodo: { idle: { src: require('../../assets/inimigos/lodo/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/lodo/ataque.png'), quadros: 6 }, dano: { src: require('../../assets/inimigos/lodo/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/lodo/morte.png'), quadros: 4 }, escala: 5, cx: 47.5, pe: 56 },
  monstro: { idle: { src: require('../../assets/inimigos/monstro/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/monstro/ataque.png'), quadros: 8 }, dano: { src: require('../../assets/inimigos/monstro/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/monstro/morte.png'), quadros: 4 }, escala: 5, cx: 51.5, pe: 57 },
  golem: { idle: { src: require('../../assets/inimigos/golem/idle.png'), quadros: 6 }, ataque: { src: require('../../assets/inimigos/golem/ataque.png'), quadros: 9 }, dano: { src: require('../../assets/inimigos/golem/dano.png'), quadros: 4 }, morte: { src: require('../../assets/inimigos/golem/morte.png'), quadros: 6 }, escala: 4, cx: 51.5, pe: 56 },
};
