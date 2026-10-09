import { useEffect, useRef } from 'react';
import { Animated, Easing, Image, Platform, StyleSheet, View } from 'react-native';
import { CENARIOS, type Camada, type CenarioId } from '../cenarios';

const nd = Platform.OS !== 'web';
const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

/** Uma camada que se repete na horizontal e desliza enquanto o herói anda. As de trás andam devagar e as da frente depressa. */
function CamadaRolante({ c, esc, larg, andando }: { c: Camada; esc: number; larg: number; andando: boolean }) {
  const tileW = c.w * esc;
  const h = c.h * esc;
  const x = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    if (!andando || c.vel <= 0) return;
    x.setValue(0);
    const anim = Animated.loop(Animated.timing(x, { toValue: -tileW, duration: (tileW / c.vel) * 1000, easing: Easing.linear, useNativeDriver: nd }));
    anim.start();
    return () => anim.stop();
  }, [andando, c.vel, tileW, x]);
  const n = Math.ceil(larg / tileW) + 1;
  return (
    <Animated.View style={{ position: 'absolute', left: 0, bottom: 0, width: n * tileW, height: h, flexDirection: 'row', transform: [{ translateX: x }] }}>
      {Array.from({ length: n }, (_, i) => (
        <Image key={i} source={c.src} resizeMode="stretch" resizeMethod="scale" style={[{ width: tileW, height: h }, pixelado]} />
      ))}
    </Animated.View>
  );
}

/**
 * Cenário de pixel art em camadas (paralaxe), alinhado na base. Com `andando`, as camadas deslizam em velocidades
 * diferentes, como se o herói caminhasse pelo cenário; parado, tudo congela. O container que o usa deve cortar o excesso.
 */
export function CenaPixel({ cenario, larg, andando }: { cenario: CenarioId; larg: number; andando: boolean }) {
  const cen = CENARIOS[cenario];
  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none">
      {cen.camadas.map((c, i) => <CamadaRolante key={i} c={c} esc={cen.esc} larg={larg} andando={andando} />)}
    </View>
  );
}
