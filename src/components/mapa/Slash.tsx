import { useEffect, useRef } from 'react';
import { Animated, Easing, Platform, View } from 'react-native';
import { SvgXml } from 'react-native-svg';

const nd = Platform.OS !== 'web';
// Meia-lua diagonal: borda de fora brilhante e miolo branco.
const CORTE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M4 94 Q30 34 98 4 Q64 64 4 94 Z" fill="#7DCFFF" stroke="#7DCFFF" stroke-width="7" stroke-linejoin="round" opacity=".55"/><path d="M4 94 Q30 34 98 4 Q64 64 4 94 Z" fill="#fff" stroke="#FFF6C2" stroke-width="2.5" stroke-linejoin="round"/></svg>';
const CORTE_OURO = CORTE.replace(/#7DCFFF/g, '#FFB020').replace('#FFF6C2', '#FFE27A');
const FAISCAS = [-150, -100, -40, 20, 70, 130].map((graus, i) => ({ rad: (graus * Math.PI) / 180, longe: 0.42 + (i % 3) * 0.08, r: 3 + (i % 2) * 1.6 }));

/**
 * Corte que cruza o monstro a cada acerto: `golpe` é um contador, e cada vez que muda o corte passa de novo
 * (alternando a direção) e saem faíscas do impacto. Fica centrado e é maior que o monstro de propósito.
 */
export function Slash({ golpe, size, forte, cruz }: { golpe: number; size: number; forte?: boolean; cruz?: boolean }) {
  const p = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    if (!golpe) return;
    p.setValue(0);
    Animated.timing(p, { toValue: 1, duration: forte ? 560 : 480, easing: Easing.out(Easing.cubic), useNativeDriver: nd }).start();
  }, [golpe, p]);
  if (!golpe) return null;
  const s = size * (forte ? 1.7 : 1.35);
  const espelho = (golpe % 2 === 0 ? -1 : 1) * (cruz ? -1 : 1);
  return (
    <View pointerEvents="none" style={{ position: 'absolute', left: '50%', top: '50%', width: s, height: s, marginLeft: -s / 2, marginTop: -s / 2 }}>
      <Animated.View style={{
        width: s, height: s,
        opacity: p.interpolate({ inputRange: [0, 0.1, 0.6, 1], outputRange: [0, 1, 0.95, 0] }),
        transform: [
          { scaleX: espelho },
          { translateX: p.interpolate({ inputRange: [0, 1], outputRange: [-s * 0.16, s * 0.16] }) },
          { translateY: p.interpolate({ inputRange: [0, 1], outputRange: [s * 0.16, -s * 0.16] }) },
          { scale: p.interpolate({ inputRange: [0, 0.3, 1], outputRange: [0.55, 1.05, 1.2] }) },
        ],
      }}>
        <SvgXml xml={forte ? CORTE_OURO : CORTE} width={s} height={s} />
      </Animated.View>
      {FAISCAS.map((f, i) => (
        <Animated.View key={i} style={{
          position: 'absolute', left: s / 2 - f.r, top: s / 2 - f.r, width: f.r * 2, height: f.r * 2, borderRadius: f.r, backgroundColor: i % 2 ? '#FFD43B' : '#fff',
          opacity: p.interpolate({ inputRange: [0, 0.1, 1], outputRange: [0, 1, 0] }),
          transform: [
            { translateX: p.interpolate({ inputRange: [0, 1], outputRange: [0, Math.cos(f.rad) * s * f.longe] }) },
            { translateY: p.interpolate({ inputRange: [0, 1], outputRange: [0, Math.sin(f.rad) * s * f.longe] }) },
            { scale: p.interpolate({ inputRange: [0, 1], outputRange: [1, 0.3] }) },
          ],
        }} />
      ))}
    </View>
  );
}

/** "CRÍTICO!" que sobe e some depois de um golpe em cheio. */
export function Critico({ golpe }: { golpe: number }) {
  const p = useRef(new Animated.Value(0)).current;
  useEffect(() => {
    if (!golpe) return;
    p.setValue(0);
    Animated.timing(p, { toValue: 1, duration: 900, easing: Easing.out(Easing.cubic), useNativeDriver: nd }).start();
  }, [golpe, p]);
  if (!golpe) return null;
  return (
    <Animated.Text pointerEvents="none" style={{
      position: 'absolute', alignSelf: 'center', top: -2, color: '#FFD43B', fontWeight: '900', fontSize: 20, letterSpacing: 1,
      textShadowColor: '#11151A', textShadowRadius: 5, textShadowOffset: { width: 0, height: 2 },
      opacity: p.interpolate({ inputRange: [0, 0.1, 0.7, 1], outputRange: [0, 1, 1, 0] }),
      transform: [{ translateY: p.interpolate({ inputRange: [0, 1], outputRange: [10, -26] }) }, { scale: p.interpolate({ inputRange: [0, 0.2, 1], outputRange: [0.5, 1.3, 1] }) }],
    }}>CRÍTICO!</Animated.Text>
  );
}
