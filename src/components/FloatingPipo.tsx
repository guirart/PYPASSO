import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Animated, Easing, PanResponder, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { Mascot } from './Characters';
import type { PipoMood } from './pipo-art';

const SIZE = 74;
const EDGE = 12;
const native = Platform.OS !== 'web';

/**
 * Pipo flutuante: fica por cima da tela, pode ser arrastado (gruda na borda
 * mais próxima) e abre uma caixa de diálogo que sobe a partir dele.
 */
export function FloatingPipo({ area, mood, open, onToggle, badge, peek, shakeKey, title, children, colors }: {
  /** Tamanho da área onde ele flutua. */
  area: { w: number; h: number };
  mood: PipoMood;
  open: boolean;
  onToggle: (open: boolean) => void;
  /** Bolinha de aviso (há algo novo para ler). */
  badge?: boolean;
  /** Balãozinho curto ao lado do Pipo, quando a caixa está fechada. */
  peek?: string | null;
  /** Muda a cada erro novo: faz o Pipo tremer. */
  shakeKey?: number;
  title: string;
  children: ReactNode;
  colors: { card: string; border: string; text: string; dim: string; accent: string; bad: string };
}) {
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);
  const drag = useRef(new Animated.ValueXY()).current;
  const shake = useRef(new Animated.Value(0)).current;
  const pop = useRef(new Animated.Value(0)).current;
  const peekAnim = useRef(new Animated.Value(0)).current;
  const posRef = useRef(pos);
  posRef.current = pos;
  const areaRef = useRef(area);
  areaRef.current = area;

  // Posição inicial: canto inferior direito, acima da barra de teclas.
  useEffect(() => {
    if (!area.w || !area.h) return;
    setPos((p) => clamp(p ?? { x: area.w - SIZE - EDGE, y: area.h - SIZE - 110 }, area));
  }, [area.w, area.h]); // eslint-disable-line react-hooks/exhaustive-deps

  // Caixa de diálogo subindo
  useEffect(() => {
    Animated.spring(pop, { toValue: open ? 1 : 0, friction: 8, tension: 90, useNativeDriver: native }).start();
  }, [open, pop]);

  // Balãozinho
  useEffect(() => {
    Animated.timing(peekAnim, { toValue: peek && !open ? 1 : 0, duration: 220, useNativeDriver: native }).start();
  }, [peek, open, peekAnim]);

  // Tremidinha a cada erro
  useEffect(() => {
    if (!shakeKey) return;
    shake.setValue(0);
    Animated.sequence([0, 1, 2, 3, 4, 5].map((i) =>
      Animated.timing(shake, { toValue: i === 5 ? 0 : i % 2 ? -1 : 1, duration: 60, easing: Easing.linear, useNativeDriver: native }),
    )).start();
  }, [shakeKey, shake]);

  const responder = useRef(PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onMoveShouldSetPanResponder: (_, g) => Math.abs(g.dx) + Math.abs(g.dy) > 4,
    onPanResponderMove: Animated.event([null, { dx: drag.x, dy: drag.y }], { useNativeDriver: false }),
    onPanResponderRelease: (_, g) => {
      drag.setValue({ x: 0, y: 0 });
      if (Math.abs(g.dx) < 6 && Math.abs(g.dy) < 6) { onToggleRef.current(!openRef.current); return; }
      const a = areaRef.current, p = posRef.current ?? { x: 0, y: 0 };
      const moved = clamp({ x: p.x + g.dx, y: p.y + g.dy }, a);
      // Gruda na borda mais próxima
      moved.x = moved.x + SIZE / 2 < a.w / 2 ? EDGE : a.w - SIZE - EDGE;
      setPos(moved);
    },
    onPanResponderTerminate: () => drag.setValue({ x: 0, y: 0 }),
  })).current;
  const onToggleRef = useRef(onToggle);
  onToggleRef.current = onToggle;
  const openRef = useRef(open);
  openRef.current = open;

  if (!pos || !area.w) return null;

  const onRight = pos.x + SIZE / 2 >= area.w / 2;
  const below = pos.y < area.h * 0.45;
  const boxW = Math.min(440, area.w - EDGE * 2);
  const boxMaxH = below ? area.h - (pos.y + SIZE + 14) - EDGE : pos.y - 14 - EDGE;
  const boxStyle = {
    width: boxW,
    maxHeight: Math.max(160, boxMaxH),
    ...(onRight ? { right: EDGE } : { left: EDGE }),
    ...(below ? { top: pos.y + SIZE + 12 } : { bottom: area.h - pos.y + 12 }),
  };
  const tailLeft = Math.min(Math.max(pos.x + SIZE / 2 - (onRight ? area.w - EDGE - boxW : EDGE) - 9, 16), boxW - 34);

  return (
    <View pointerEvents="box-none" style={StyleSheet.absoluteFill}>
      {/* Caixa de diálogo */}
      <Animated.View
        pointerEvents={open ? 'auto' : 'none'}
        accessibilityViewIsModal={open}
        style={[styles.box, boxStyle, { backgroundColor: colors.card, borderColor: colors.border },
          { opacity: pop, transform: [{ translateY: pop.interpolate({ inputRange: [0, 1], outputRange: [below ? -16 : 24, 0] }) }, { scale: pop.interpolate({ inputRange: [0, 1], outputRange: [0.92, 1] }) }] }]}>
        <View style={[styles.tail, below ? styles.tailUp : styles.tailDown, { left: tailLeft, borderColor: colors.border, backgroundColor: colors.card }]} />
        <View style={[styles.boxHead, { borderBottomColor: colors.border }]}>
          <Text style={[styles.name, { color: colors.accent }]}>PIPO</Text>
          <Text style={[styles.title, { color: colors.text }]} numberOfLines={3}>{title}</Text>
          <Pressable onPress={() => onToggle(false)} hitSlop={10} accessibilityLabel="Fechar a caixa do Pipo" style={styles.close}>
            <Text style={{ color: colors.dim, fontSize: 18 }}>✕</Text>
          </Pressable>
        </View>
        <View style={{ flexShrink: 1 }}>{children}</View>
      </Animated.View>

      {/* Balãozinho */}
      {peek ? (
        <Animated.View pointerEvents="none" style={[styles.peek, {
          backgroundColor: colors.card, borderColor: colors.border, opacity: peekAnim,
          top: pos.y + 8, ...(onRight ? { right: area.w - pos.x + 6 } : { left: pos.x + SIZE + 6 }),
          transform: [{ translateX: peekAnim.interpolate({ inputRange: [0, 1], outputRange: [onRight ? 10 : -10, 0] }) }],
        }]}>
          <Text style={{ color: colors.text, fontWeight: '700', fontSize: 13 }} numberOfLines={3}>{peek}</Text>
        </Animated.View>
      ) : null}

      {/* O Pipo */}
      <Animated.View
        {...responder.panHandlers}
        accessibilityRole="button"
        accessibilityLabel={open ? 'Fechar o Pipo' : 'Abrir o Pipo'}
        style={[styles.pipo, {
          left: pos.x, top: pos.y,
          transform: [
            ...drag.getTranslateTransform(),
            { translateX: shake.interpolate({ inputRange: [-1, 1], outputRange: [-7, 7] }) },
          ],
        }, Platform.OS === 'web' && ({ cursor: 'grab', userSelect: 'none' } as object)]}>
        <View style={styles.halo} />
        <Mascot size={SIZE} mood={mood} />
        {badge && !open ? <View style={[styles.badge, { backgroundColor: colors.bad, borderColor: colors.card }]} /> : null}
      </Animated.View>
    </View>
  );
}

function clamp(p: { x: number; y: number }, a: { w: number; h: number }) {
  return {
    x: Math.min(Math.max(EDGE, p.x), Math.max(EDGE, a.w - SIZE - EDGE)),
    y: Math.min(Math.max(EDGE, p.y), Math.max(EDGE, a.h - SIZE - EDGE)),
  };
}

const styles = StyleSheet.create({
  pipo: { position: 'absolute', width: SIZE, height: SIZE, alignItems: 'center', justifyContent: 'center' },
  halo: { position: 'absolute', bottom: 2, width: SIZE * 0.7, height: 10, borderRadius: 10, backgroundColor: 'rgba(0,0,0,0.28)' },
  badge: { position: 'absolute', top: 4, right: 6, width: 16, height: 16, borderRadius: 8, borderWidth: 2 },
  box: {
    position: 'absolute', borderWidth: 1, borderRadius: 16, overflow: 'visible',
    shadowColor: '#000', shadowOpacity: 0.35, shadowRadius: 18, shadowOffset: { width: 0, height: 8 }, elevation: 12,
  },
  boxHead: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 14, paddingVertical: 10, borderBottomWidth: 1 },
  name: { fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  title: { flex: 1, fontSize: 15, fontWeight: '800' },
  close: { paddingHorizontal: 4 },
  tail: { position: 'absolute', width: 18, height: 18, transform: [{ rotate: '45deg' }] },
  tailDown: { bottom: -9, borderRightWidth: 1, borderBottomWidth: 1 },
  tailUp: { top: -9, borderLeftWidth: 1, borderTopWidth: 1 },
  peek: {
    position: 'absolute', maxWidth: 220, borderWidth: 1, borderRadius: 12, paddingHorizontal: 10, paddingVertical: 7,
    shadowColor: '#000', shadowOpacity: 0.25, shadowRadius: 8, shadowOffset: { width: 0, height: 3 }, elevation: 6,
  },
});
