import { memo, useEffect, useId, useRef } from 'react';
import { Animated, Easing, Platform, View } from 'react-native';
import Svg, { Circle, Defs, Ellipse, LinearGradient, Path, Polygon, Stop } from 'react-native-svg';
import { Icone } from '../Icone';
import { INFO_NO, type TipoNo } from '@/lib/mapa';

export type EstadoNo = 'disponivel' | 'atual' | 'visitado' | 'futuro' | 'fora' | 'bloqueado';

const hexPts = (cx: number, cy: number, r: number) =>
  [-90, -30, 30, 90, 150, 210].map((a) => `${(cx + r * Math.cos((a * Math.PI) / 180)).toFixed(2)},${(cy + r * Math.sin((a * Math.PI) / 180)).toFixed(2)}`).join(' ');

/** Nó hexagonal do mapa: moldura metálica, miolo colorido pelo tipo e ícone branco. */
export const NoHex = memo(function NoHex({ tipo, size, estado }: { tipo: TipoNo; size: number; estado: EstadoNo }) {
  const uid = useId().replace(/[^a-zA-Z0-9]/g, '');
  const info = INFO_NO[tipo];
  const brilho = useRef(new Animated.Value(0)).current;
  const disponivel = estado === 'disponivel';
  useEffect(() => {
    if (!disponivel) return;
    const a = Animated.loop(Animated.sequence([
      Animated.timing(brilho, { toValue: 1, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
      Animated.timing(brilho, { toValue: 0, duration: 900, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
    ]));
    a.start();
    return () => a.stop();
  }, [disponivel, brilho]);

  const S = size, c = S / 2;
  const cinza = estado === 'bloqueado';
  const [c1, c2] = cinza ? ['#B8C2CE', '#8592A3'] : info.cor;
  const chefe = tipo === 'chefe';
  return (
    <View style={{ width: S, height: S, opacity: estado === 'fora' ? 0.38 : 1 }}>
      {disponivel && (
        <Animated.View pointerEvents="none" style={{
          position: 'absolute', left: -S * 0.14, top: -S * 0.14, width: S * 1.28, height: S * 1.28,
          opacity: brilho.interpolate({ inputRange: [0, 1], outputRange: [0.55, 1] }),
          transform: [{ scale: brilho.interpolate({ inputRange: [0, 1], outputRange: [0.97, 1.05] }) }],
        }}>
          <Svg width={S * 1.28} height={S * 1.28}>
            <Polygon points={hexPts(S * 0.64, S * 0.64, S * 0.6)} fill="#7FE7FF" opacity={0.35} />
            <Polygon points={hexPts(S * 0.64, S * 0.64, S * 0.56)} fill="none" stroke="#A6F0FF" strokeWidth={3} />
          </Svg>
        </Animated.View>
      )}
      {/* posicionado para ficar por cima do brilho (que também é absoluto) */}
      <View style={{ position: 'absolute', left: 0, top: 0 }}>
      <Svg width={S} height={S}>
        <Defs>
          <LinearGradient id={`m${uid}`} x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor={estado === 'atual' ? '#FFF6D6' : '#F7FAFD'} />
            <Stop offset="0.55" stopColor={estado === 'atual' ? '#F5CD62' : '#C9D3DF'} />
            <Stop offset="1" stopColor={estado === 'atual' ? '#C8961E' : '#8C9AAD'} />
          </LinearGradient>
          <LinearGradient id={`c${uid}`} x1="0" y1="0" x2="0" y2="1">
            <Stop offset="0" stopColor={c1} />
            <Stop offset="1" stopColor={c2} />
          </LinearGradient>
        </Defs>
        <Polygon points={hexPts(c, c + S * 0.035, S * 0.47)} fill="#000" opacity={0.28} />
        <Polygon points={hexPts(c, c, S * 0.47)} fill={`url(#m${uid})`} stroke={estado === 'atual' ? '#8A6510' : '#5D6B7E'} strokeWidth={S * 0.03} />
        <Polygon points={hexPts(c, c, S * 0.385)} fill="#E9EEF4" opacity={0.55} />
        {chefe && <Path d={`M${c - S * 0.3} ${c - S * 0.2} L${c - S * 0.4} ${c - S * 0.44} L${c - S * 0.16} ${c - S * 0.3} Z M${c + S * 0.3} ${c - S * 0.2} L${c + S * 0.4} ${c - S * 0.44} L${c + S * 0.16} ${c - S * 0.3} Z`} fill="#5D6B7E" />}
        <Circle cx={c} cy={c} r={S * 0.31} fill={`url(#c${uid})`} stroke={c2} strokeWidth={S * 0.025} />
        <Ellipse cx={c} cy={c - S * 0.15} rx={S * 0.2} ry={S * 0.09} fill="#fff" opacity={0.28} />
      </Svg>
      </View>
      <View pointerEvents="none" style={{ position: 'absolute', left: 0, top: 0, width: S, height: S, alignItems: 'center', justifyContent: 'center' }}>
        <Icone nome={cinza ? 'cadeado' : info.icone} size={S * (chefe ? 0.4 : 0.36)} color="#fff" />
      </View>
      {estado === 'visitado' && (
        <View style={{ position: 'absolute', right: S * 0.04, bottom: S * 0.06, width: S * 0.3, height: S * 0.3, borderRadius: 99, backgroundColor: '#2E9E5B', borderWidth: 2, borderColor: '#fff', alignItems: 'center', justifyContent: 'center' }}>
          <Icone nome="check" size={S * 0.17} color="#fff" />
        </View>
      )}
    </View>
  );
});
