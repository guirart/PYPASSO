import { Image, Platform, type ImageSourcePropType } from 'react-native';
import type { ModeloBau } from '@/lib/baus';

// Treasure Chests, da Mana Seed (pixel art): cada baú tem um quadro fechado e um aberto, ambos de 20x24 e alinhados embaixo.
const BAUS: Record<string, { fechado: ImageSourcePropType; aberto: ImageSourcePropType }> = {
  n0: { fechado: require('../../assets/baus/n0_f.png'), aberto: require('../../assets/baus/n0_a.png') },
  n1: { fechado: require('../../assets/baus/n1_f.png'), aberto: require('../../assets/baus/n1_a.png') },
  n2: { fechado: require('../../assets/baus/n2_f.png'), aberto: require('../../assets/baus/n2_a.png') },
  n3: { fechado: require('../../assets/baus/n3_f.png'), aberto: require('../../assets/baus/n3_a.png') },
  n4: { fechado: require('../../assets/baus/n4_f.png'), aberto: require('../../assets/baus/n4_a.png') },
  b0: { fechado: require('../../assets/baus/b0_f.png'), aberto: require('../../assets/baus/b0_a.png') },
  b1: { fechado: require('../../assets/baus/b1_f.png'), aberto: require('../../assets/baus/b1_a.png') },
  b2: { fechado: require('../../assets/baus/b2_f.png'), aberto: require('../../assets/baus/b2_a.png') },
};
export const LARG_BAU = 20;
export const ALT_BAU = 24;

/** O baú em pixel art, ampliado por um número inteiro (`esc`) para os pixels ficarem nítidos. */
export function ImagemBau({ modelo, aberto, esc = 3 }: { modelo: ModeloBau; aberto?: boolean; esc?: number }) {
  const b = BAUS[modelo.id];
  return (
    <Image source={aberto ? b.aberto : b.fechado} resizeMode="stretch" accessibilityLabel={modelo.nome}
      style={[{ width: LARG_BAU * esc, height: ALT_BAU * esc }, Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null]} />
  );
}
