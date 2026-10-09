import { useEffect, useMemo, useRef, useState } from 'react';
import { Animated, Easing, Platform, Pressable, StyleSheet, View } from 'react-native';
import Svg, { Defs, G, Line, LinearGradient, Path, Rect, Stop } from 'react-native-svg';
import { AvatarMoldura } from '../Characters';
import { FundoMapa } from './FundoMapa';
import { NoHex, type EstadoNo } from './NoHex';
import { INFO_NO, PALETAS, type Mapa, type No } from '@/lib/mapa';
import type { Rota } from '@/lib/store';

const ROW = 104;
const TOPO = 70;
const NO = 70;

export const alturaMapa = (m: Mapa) => TOPO + (m.linhas.length + 1) * ROW + 90;

/** Nós que dá para entrar agora: os ligados à posição atual (ou à entrada). */
export function disponiveis(m: Mapa, rota: Rota): Set<string> {
  const pos = rota.pos && m.nos[rota.pos] ? m.nos[rota.pos] : m.entrada;
  return new Set(pos.liga);
}

export function estadoDoNo(m: Mapa, rota: Rota, n: No, livres: Set<string>, zonaAberta: boolean, chefeVencido: boolean): EstadoNo {
  if (!zonaAberta) return 'bloqueado';
  if (n.tipo === 'chefe' && chefeVencido) return 'visitado';
  if (n.tipo === 'entrada') return rota.pos ? 'futuro' : 'atual';
  if (rota.pos === n.id) return 'atual';
  if (rota.visitados.includes(n.id)) return 'visitado';
  if (livres.has(n.id)) return 'disponivel';
  const linhaAtual = rota.pos && m.nos[rota.pos] ? m.nos[rota.pos].linha : -1;
  return n.linha <= linhaAtual ? 'fora' : 'futuro';
}

/** Mapa de uma zona: fundo, caminhos, nós e o personagem da pessoa no nó atual. */
export function MapaZona({ mapa, rota, indice, zonaAberta, chefeVencido, escuro, avatar, moldura, onNo }: {
  mapa: Mapa; rota: Rota; indice: number; zonaAberta: boolean; chefeVencido: boolean; escuro: boolean;
  avatar: string; moldura?: string; onNo: (n: No) => void;
}) {
  const [W, setW] = useState(0);
  const H = alturaMapa(mapa);
  const pal = PALETAS[indice % PALETAS.length][escuro ? 'escuro' : 'claro'];
  const livres = useMemo(() => disponiveis(mapa, rota), [mapa, rota]);
  const xy = (n: No) => ({ x: W * (0.2 + 0.3 * n.col), y: TOPO + (n.linha + 1) * ROW });
  const todos = useMemo(() => [mapa.entrada, ...mapa.linhas.flat(), mapa.chefe], [mapa]);

  // Caminho percorrido (entrada → visitados, na ordem)
  const feitos = useMemo(() => {
    const seq = [mapa.entrada.id, ...rota.visitados];
    const set = new Set<string>();
    for (let i = 1; i < seq.length; i++) set.add(`${seq[i - 1]}>${seq[i]}`);
    return set;
  }, [mapa, rota]);

  // Personagem: anda até o nó atual
  const atual = rota.pos && mapa.nos[rota.pos] ? mapa.nos[rota.pos] : mapa.entrada;
  const alvo = W ? xy(atual) : { x: 0, y: 0 };
  const pos = useRef(new Animated.ValueXY(alvo)).current;
  const pulo = useRef(new Animated.Value(0)).current;
  const primeiro = useRef(true);
  useEffect(() => {
    if (!W) return;
    if (primeiro.current) { pos.setValue(alvo); primeiro.current = false; return; }
    Animated.timing(pos, { toValue: alvo, duration: 650, easing: Easing.inOut(Easing.cubic), useNativeDriver: false }).start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [alvo.x, alvo.y, W]);
  useEffect(() => {
    const a = Animated.loop(Animated.sequence([
      Animated.timing(pulo, { toValue: 1, duration: 700, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
      Animated.timing(pulo, { toValue: 0, duration: 700, easing: Easing.inOut(Easing.quad), useNativeDriver: Platform.OS !== 'web' }),
    ]));
    a.start();
    return () => a.stop();
  }, [pulo]);

  const AV = 40;
  return (
    <View onLayout={(e) => setW(e.nativeEvent.layout.width)} style={[styles.wrap, { height: H }]}>
      {W > 0 && (
        <>
          <FundoMapa indice={indice} W={W} H={H} />
          <Svg width={W} height={H} style={StyleSheet.absoluteFill}>
            <Defs>
              <LinearGradient id={`fundo${indice}`} x1="0" y1="0" x2="0" y2="1">
                <Stop offset="0" stopColor={pal[0]} />
                <Stop offset="0.55" stopColor={pal[1]} />
                <Stop offset="1" stopColor={pal[2]} />
              </LinearGradient>
            </Defs>
            {/* a cor da zona cobre a pixel art em parte: dá identidade à zona e mantém caminhos e nós legíveis */}
            <Rect x={0} y={0} width={W} height={H} fill={`url(#fundo${indice})`} opacity={escuro ? 0.4 : 0.18} />
            {/* caminhos */}
            {todos.flatMap((n) => n.liga.map((k) => {
              const a = xy(n), b = xy(mapa.nos[k]);
              const feito = feitos.has(`${n.id}>${k}`);
              const aberto = zonaAberta && (n.id === atual.id) && livres.has(k);
              return (
                <G key={`${n.id}>${k}`}>
                  <Line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={escuro ? '#0A0F14' : '#3B4553'} strokeOpacity={0.55} strokeWidth={9} strokeLinecap="round" />
                  <Line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={feito ? '#FFD25C' : aberto ? '#BFF4FF' : escuro ? '#4A5866' : '#6B7889'} strokeWidth={feito || aberto ? 5 : 4} strokeLinecap="round" />
                </G>
              );
            }))}
          </Svg>
          {todos.map((n) => {
            const { x, y } = xy(n);
            const S = n.tipo === 'chefe' ? 96 : n.tipo === 'entrada' ? 62 : NO;
            const estado = estadoDoNo(mapa, rota, n, livres, zonaAberta, chefeVencido);
            const info = INFO_NO[n.tipo];
            return (
              <Pressable key={n.id} onPress={() => onNo(n)} accessibilityRole="button"
                accessibilityLabel={`${info.nome}${estado === 'disponivel' ? ', disponível' : estado === 'visitado' ? ', concluído' : estado === 'atual' ? ', você está aqui' : ''}`}
                style={{ position: 'absolute', left: x - S / 2, top: y - S / 2, width: S, height: S }}>
                {estado === 'disponivel' && (
                  <View pointerEvents="none" style={[styles.seta, { left: S / 2 - 9, top: -22 }]}>
                    <Svg width={18} height={14}><Path d="M2 2 L9 11 L16 2 Z" fill="#BFF4FF" stroke="#2B9BB5" strokeWidth={1.5} strokeLinejoin="round" /></Svg>
                  </View>
                )}
                <NoHex tipo={n.tipo} size={S} estado={estado} />
              </Pressable>
            );
          })}
          {/* personagem */}
          {zonaAberta && !chefeVencido && (
            <Animated.View pointerEvents="none" style={{
              position: 'absolute', left: 0, top: 0,
              transform: [{ translateX: Animated.subtract(pos.x, AV + 20) }, { translateY: Animated.subtract(pos.y, AV + 8) }],
            }}>
              <Animated.View style={{ transform: [{ translateY: pulo.interpolate({ inputRange: [0, 1], outputRange: [0, -6] }) }] }}>
                <View style={styles.avSombra} />
                <View style={[styles.av, { borderColor: '#fff' }]}><AvatarMoldura seed={avatar} size={AV} moldura={moldura} /></View>
              </Animated.View>
            </Animated.View>
          )}
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { width: '100%', overflow: 'hidden' },
  seta: { position: 'absolute' },
  av: { borderWidth: 3, borderRadius: 999, overflow: 'hidden', backgroundColor: '#fff' },
  avSombra: { position: 'absolute', left: 6, bottom: -6, width: 34, height: 10, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.25)' },
});
