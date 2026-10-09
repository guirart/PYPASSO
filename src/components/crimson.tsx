import { useEffect, useRef, useState } from 'react';
import { Animated, Image, Platform, StyleSheet, Text, View, type ImageSourcePropType } from 'react-native';

// Peças do "Crimson Fantasy GUI" (pixel art): barras de vida, corações e molduras. Recortadas do pacote em assets/crimson.
export const CRIMSON = {
  coracao: [
    require('../../assets/crimson/coracao_0.png'), require('../../assets/crimson/coracao_1.png'),
    require('../../assets/crimson/coracao_2.png'), require('../../assets/crimson/coracao_3.png'),
  ] as ImageSourcePropType[],
  barra: { cheia: require('../../assets/crimson/barra_cheia.png') as ImageSourcePropType, vazia: require('../../assets/crimson/barra_vazia.png') as ImageSourcePropType, w: 64, h: 9 },
  orbe: { cheia: require('../../assets/crimson/barra_orbe_cheia.png') as ImageSourcePropType, vazia: require('../../assets/crimson/barra_orbe_vazia.png') as ImageSourcePropType, w: 64, h: 16 },
  ornada: { cheia: require('../../assets/crimson/barra_orn_cheia.png') as ImageSourcePropType, vazia: require('../../assets/crimson/barra_orn_vazia.png') as ImageSourcePropType, w: 62, h: 16 },
  slot: require('../../assets/crimson/slot.png') as ImageSourcePropType,
  divisor: require('../../assets/crimson/divisor.png') as ImageSourcePropType,
};

export const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

export type EstiloBarra = 'simples' | 'orbe' | 'ornada';

/**
 * Barra de vida em pixel art: a barra vazia fica por baixo e a cheia aparece só até a fração `ratio` (0 a 1),
 * recortada, então os pixels continuam nítidos. `esc` amplia em número inteiro. `ratio` pode ser um Animated.Value.
 */
export function BarraVida({ ratio, estilo = 'simples', esc = 3, texto, rotulo, orbeTexto, hp, hpMax }: { ratio: number | Animated.Value; estilo?: EstiloBarra; esc?: number; texto?: string; rotulo?: string; orbeTexto?: string; hp?: number; hpMax?: number }) {
  // Efeitos: com `hp` e `hpMax`, quando a vida cai a barra pisca em branco e deixa um rastro claro do que foi perdido;
  // quando sobe, ela brilha em dourado. (As animações prontas do pacote são de uma barra específica, então o efeito é refeito aqui.)
  const antes = useRef(hp);
  const rastro = useRef(new Animated.Value(0)).current;
  const brilho = useRef(new Animated.Value(0)).current;
  const [faixa, setFaixa] = useState({ de: 1, para: 1, cura: false });
  useEffect(() => {
    if (hp === undefined || !hpMax) return;
    const a = antes.current ?? hp;
    if (hp < a) {
      setFaixa({ de: a / hpMax, para: Math.max(0, hp) / hpMax, cura: false });
      rastro.setValue(1); brilho.setValue(0.75);
      Animated.parallel([
        Animated.timing(brilho, { toValue: 0, duration: 260, useNativeDriver: false }),
        Animated.timing(rastro, { toValue: 0, duration: 800, delay: 200, useNativeDriver: false }),
      ]).start();
    } else if (hp > a) {
      setFaixa({ de: hp / hpMax, para: a / hpMax, cura: true });
      brilho.setValue(0.7);
      Animated.timing(brilho, { toValue: 0, duration: 650, useNativeDriver: false }).start();
    }
    antes.current = hp;
  }, [hp, hpMax, rastro, brilho]);
  const p = estilo === 'orbe' ? CRIMSON.orbe : estilo === 'ornada' ? CRIMSON.ornada : CRIMSON.barra;
  const W = p.w * esc, H = p.h * esc;
  const larg = typeof ratio === 'number' ? Math.max(0, Math.min(1, ratio)) * W : ratio.interpolate({ inputRange: [0, 1], outputRange: [0, W], extrapolate: 'clamp' });
  return (
    <View style={{ width: W, height: H, alignItems: 'center', justifyContent: 'center' }} accessibilityLabel={rotulo}>
      <Image source={p.vazia} resizeMode="stretch" style={[{ position: 'absolute', width: W, height: H }, pixelado]} />
      <Animated.View style={{ position: 'absolute', left: 0, top: 0, height: H, width: larg, overflow: 'hidden' }}>
        <Image source={p.cheia} resizeMode="stretch" style={[{ width: W, height: H }, pixelado]} />
      </Animated.View>
      {hp !== undefined && (
        <>
          <Animated.View pointerEvents="none" style={{ position: 'absolute', left: Math.max(2 * esc, faixa.para * W), width: Math.max(0, (faixa.de - faixa.para) * W), top: 2 * esc, height: H - 4 * esc, backgroundColor: 'rgba(255,255,255,0.85)', opacity: faixa.cura ? 0 : rastro }} />
          <Animated.View pointerEvents="none" style={{ position: 'absolute', left: 2 * esc, right: 2 * esc, top: 2 * esc, height: H - 4 * esc, borderRadius: esc, backgroundColor: faixa.cura ? '#FFE066' : '#FFFFFF', opacity: brilho }} />
        </>
      )}
      {!!texto && <Text style={styles.texto}>{texto}</Text>}
      {!!orbeTexto && <Text style={[styles.orbe, { width: 16 * esc, height: H, lineHeight: H, fontSize: 6 * esc }]}>{orbeTexto}</Text>}
    </View>
  );
}

/** Coração em pixel art. estado: 0 cheio, 1 pela metade, 2 quase vazio, 3 vazio. */
export function CoracaoPixel({ estado = 0, esc = 2 }: { estado?: 0 | 1 | 2 | 3; esc?: number }) {
  return <Image source={CRIMSON.coracao[estado]} resizeMode="stretch" style={[{ width: 16 * esc, height: 16 * esc }, pixelado]} />;
}

/** Fileira de corações: `vidas` cheios e o resto vazios. */
export function Coracoes({ vidas, max, esc = 2 }: { vidas: number; max: number; esc?: number }) {
  return (
    <View style={{ flexDirection: 'row' }} accessibilityLabel={`${vidas} de ${max} vidas`}>
      {Array.from({ length: max }, (_, i) => <CoracaoPixel key={i} estado={i < vidas ? 0 : 3} esc={esc} />)}
    </View>
  );
}

const styles = StyleSheet.create({
  orbe: { position: 'absolute', left: 0, top: 0, color: '#fff', fontWeight: '900', textAlign: 'center', textShadowColor: 'rgba(60,0,0,0.95)', textShadowRadius: 3, textShadowOffset: { width: 0, height: 1 }, fontVariant: ['tabular-nums'] },
  texto: { color: '#fff', fontSize: 10, fontWeight: '900', textAlign: 'center', textShadowColor: 'rgba(0,0,0,0.9)', textShadowRadius: 2, textShadowOffset: { width: 0, height: 1 }, fontVariant: ['tabular-nums'] },
});
