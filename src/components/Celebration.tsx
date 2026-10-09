import { useEffect, useMemo, useRef } from 'react';
import { AccessibilityInfo, Animated, Easing, Platform, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { SvgXml } from 'react-native-svg';
import type { Comemoracao } from '@/lib/comemoracao';
import { useTheme } from '@/lib/theme';
import { poseSvg } from './pipo-poses';

const nativo = Platform.OS !== 'web';
const CORES = ['#FFD43B', '#2EA043', '#E8455A', '#7DB3FF', '#B07CFF', '#FF9E64'];

/** Fim de lição: o Pipo comemora com um visual e uma frase que combinam com o desempenho. */
export function Celebration({ c }: { c: Comemoracao }) {
  const t = useTheme();
  const pop = useRef(new Animated.Value(0)).current;
  const carimbo = useRef(new Animated.Value(0)).current;
  const balao = useRef(new Animated.Value(0)).current;
  const balanco = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Em cascata: o Pipo pula, o título carimba e o balão abre (sem esperar cada mola parar).
    Animated.stagger(280, [
      Animated.spring(pop, { toValue: 1, friction: 4, tension: 110, useNativeDriver: nativo }),
      Animated.spring(carimbo, { toValue: 1, friction: 5, tension: 160, useNativeDriver: nativo }),
      Animated.timing(balao, { toValue: 1, duration: 260, easing: Easing.out(Easing.back(1.5)), useNativeDriver: nativo }),
    ]).start();
    const loop = Animated.loop(Animated.sequence([
      Animated.timing(balanco, { toValue: 1, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: nativo }),
      Animated.timing(balanco, { toValue: 0, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: nativo }),
    ]));
    AccessibilityInfo.isReduceMotionEnabled().then((r) => { if (!r) loop.start(); }).catch(() => loop.start());
    return () => loop.stop();
  }, [pop, carimbo, balao, balanco]);

  const rot = balanco.interpolate({ inputRange: [0, 1], outputRange: ['-4deg', '4deg'] });
  const carimboScale = carimbo.interpolate({ inputRange: [0, 1], outputRange: [2.2, 1] });
  const cor = c.pose === 'oculos' ? '#111A22' : c.pose === 'raio' ? '#E8AE00' : c.pose === 'festa' ? t.bad : '#E8455A';

  return (
    <View style={styles.wrap} accessibilityLabel={`${c.titulo}. Pipo diz: ${c.frase}`}>
      {c.confete && <Confete />}
      <Animated.View style={[styles.balao, { backgroundColor: t.surface, borderColor: t.line, opacity: balao, transform: [{ scale: balao }] }]}>
        <Text style={[styles.frase, { color: t.ink }]}>{c.frase}</Text>
        <View style={[styles.ponta, { borderTopColor: t.line }]} />
        <View style={[styles.pontaIn, { borderTopColor: t.surface }]} />
      </Animated.View>
      <Animated.View style={{ transform: [{ scale: pop }, { rotate: rot }] }}>
        <SvgXml xml={poseSvg(c.pose)} width={190} height={184} />
      </Animated.View>
      <Animated.Text style={[styles.titulo, { color: '#fff', backgroundColor: cor, opacity: carimbo, transform: [{ scale: carimboScale }, { rotate: '-4deg' }] }]}>
        {c.titulo}
      </Animated.Text>
    </View>
  );
}

/** Confete caindo (leve: 18 pedacinhos). */
function Confete() {
  const { width } = useWindowDimensions();
  const pecas = useMemo(() => Array.from({ length: 18 }, (_, i) => ({
    x: Math.random() * Math.min(width, 520) - Math.min(width, 520) / 2,
    atraso: Math.random() * 600,
    dur: 1600 + Math.random() * 1200,
    cor: CORES[i % CORES.length],
    giro: Math.random() > 0.5 ? 1 : -1,
    v: new Animated.Value(0),
  })), [width]);
  useEffect(() => {
    let reduzir = false;
    AccessibilityInfo.isReduceMotionEnabled().then((r) => { reduzir = r; }).catch(() => {});
    pecas.forEach((p) => {
      setTimeout(() => {
        if (reduzir) return;
        Animated.timing(p.v, { toValue: 1, duration: p.dur, easing: Easing.in(Easing.quad), useNativeDriver: nativo }).start();
      }, p.atraso);
    });
  }, [pecas]);
  return (
    <View pointerEvents="none" style={StyleSheet.absoluteFill}>
      {pecas.map((p, i) => (
        <Animated.View key={i} style={[styles.peca, {
          backgroundColor: p.cor,
          left: '50%',
          opacity: p.v.interpolate({ inputRange: [0, 0.05, 0.85, 1], outputRange: [0, 1, 1, 0] }),
          transform: [
            { translateX: p.x },
            { translateY: p.v.interpolate({ inputRange: [0, 1], outputRange: [-40, 460] }) },
            { rotate: p.v.interpolate({ inputRange: [0, 1], outputRange: ['0deg', `${p.giro * 540}deg`] }) },
          ],
        }]} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { alignItems: 'center', width: '100%', maxWidth: 440, paddingTop: 8 },
  balao: { borderWidth: 2, borderRadius: 18, paddingHorizontal: 16, paddingVertical: 12, maxWidth: 340, marginBottom: 10 },
  frase: { fontSize: 16, fontWeight: '800', textAlign: 'center', lineHeight: 22 },
  ponta: { position: 'absolute', bottom: -12, alignSelf: 'center', width: 0, height: 0, borderLeftWidth: 11, borderRightWidth: 11, borderTopWidth: 12, borderLeftColor: 'transparent', borderRightColor: 'transparent' },
  pontaIn: { position: 'absolute', bottom: -8, alignSelf: 'center', width: 0, height: 0, borderLeftWidth: 9, borderRightWidth: 9, borderTopWidth: 10, borderLeftColor: 'transparent', borderRightColor: 'transparent' },
  titulo: { marginTop: -12, fontSize: 24, fontWeight: '900', letterSpacing: 1.5, paddingHorizontal: 16, paddingVertical: 6, borderRadius: 12, overflow: 'hidden' },
  peca: { position: 'absolute', top: 0, width: 9, height: 14, borderRadius: 2 },
});
