// Cenários de pixel art em camadas (paralaxe) das batalhas. Arte de Luis Zuno (@ansimuz), via OpenGameArt:
// GothicVania Cemetery (CC-BY 3.0, o crédito aparece no Perfil), Junk Wasteland, Mountain at Dusk e Forest Background.
// As licenças ficam em assets/cenarios/<pasta>/LICENCA.txt.
import type { ImageSourcePropType } from 'react-native';
import type { EnemyId } from './enemy-art';

export type CenarioId = 'cemiterio' | 'terra' | 'montanha' | 'floresta';
/** Uma camada: tamanho original da imagem (w x h) e a velocidade em px/s quando o herói anda (0 = parada). */
export type Camada = { src: ImageSourcePropType; w: number; h: number; vel: number };
/** `esc` é a ampliação inteira da arte (os pixels ficam nítidos). Camadas vão de trás para a frente. */
export type Cenario = { esc: number; camadas: Camada[] };

export const CENARIOS: Record<CenarioId, Cenario> = {
  cemiterio: {
    esc: 1,
    camadas: [
      { src: require('../../assets/cenarios/cemiterio/ceu.png'), w: 384, h: 224, vel: 0 },
      { src: require('../../assets/cenarios/cemiterio/montanhas.png'), w: 192, h: 179, vel: 14 },
      { src: require('../../assets/cenarios/cemiterio/tumulos.png'), w: 384, h: 123, vel: 80 },
    ],
  },
  terra: {
    esc: 1,
    camadas: [
      { src: require('../../assets/cenarios/terra/fundo.png'), w: 144, h: 240, vel: 10 },
      { src: require('../../assets/cenarios/terra/meio.png'), w: 336, h: 240, vel: 40 },
      { src: require('../../assets/cenarios/terra/perto.png'), w: 512, h: 240, vel: 90 },
    ],
  },
  montanha: {
    esc: 2,
    camadas: [
      { src: require('../../assets/cenarios/montanha/ceu.png'), w: 272, h: 160, vel: 0 },
      { src: require('../../assets/cenarios/montanha/longe.png'), w: 272, h: 160, vel: 8 },
      { src: require('../../assets/cenarios/montanha/montanhas.png'), w: 544, h: 160, vel: 20 },
      { src: require('../../assets/cenarios/montanha/arvores.png'), w: 544, h: 160, vel: 50 },
      { src: require('../../assets/cenarios/montanha/frente.png'), w: 544, h: 160, vel: 90 },
    ],
  },
  floresta: {
    esc: 2,
    camadas: [
      { src: require('../../assets/cenarios/floresta/fundo.png'), w: 272, h: 160, vel: 10 },
      { src: require('../../assets/cenarios/floresta/meio.png'), w: 272, h: 160, vel: 35 },
      { src: require('../../assets/cenarios/floresta/frente.png'), w: 272, h: 160, vel: 90 },
      { src: require('../../assets/cenarios/floresta/luz.png'), w: 272, h: 160, vel: 20 },
    ],
  },
};

/** Cada inimigo luta no cenário que mais combina com ele. */
export const CENARIO_DO_INIMIGO: Record<EnemyId, CenarioId> = {
  morcego: 'floresta', fogofatuo: 'cemiterio', olho: 'cemiterio', bruxo: 'montanha',
  monstro: 'montanha', golem: 'terra', cao: 'terra', lodo: 'floresta',
};
