import { Image, Platform, StyleSheet, View } from 'react-native';

// Fundos do mapa: pixel art de castelo (Craftpix, "Free Castle Interior Pixel Game Backgrounds"), 576x324 cada.
// A arte é ampliada em número inteiro (os pixels ficam nítidos) até cobrir o mapa todo; sobra um pedaço dos lados,
// que é cortado. Cada zona usa uma cena e um enquadramento diferentes.
const CENAS = [
  require('../../../assets/castelo/fundo1.png'),
  require('../../../assets/castelo/fundo2.png'),
  require('../../../assets/castelo/fundo3.png'),
  require('../../../assets/castelo/fundo4.png'),
];
const LARG = 576;
const ALT = 324;
/** Onde cortar na horizontal (0 = borda esquerda da arte, 1 = direita), para as zonas não ficarem iguais. */
const ENQUADRA = [0.5, 0.3, 0.7, 0.2, 0.8, 0.4, 0.6, 0.1];

const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

export function FundoMapa({ indice, W, H }: { indice: number; W: number; H: number }) {
  const esc = Math.max(1, Math.ceil(Math.max(H / ALT, W / LARG))); // menor ampliação inteira que cobre o mapa
  const w = LARG * esc, h = ALT * esc;
  const frac = ENQUADRA[indice % ENQUADRA.length];
  return (
    <View style={[StyleSheet.absoluteFill, { overflow: 'hidden' }]} pointerEvents="none">
      <Image source={CENAS[indice % CENAS.length]} resizeMode="stretch"
        style={[{ position: 'absolute', width: w, height: h, left: -(w - W) * frac, top: -(h - H) / 2 }, pixelado]} />
      {/* escurece um pouco para os caminhos e nós se destacarem sobre a arte */}
      <View style={[StyleSheet.absoluteFill, { backgroundColor: 'rgba(10,8,14,0.30)' }]} />
    </View>
  );
}
