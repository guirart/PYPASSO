import { useEffect, useRef } from 'react';
import { Animated, StyleSheet, Text, View } from 'react-native';
import { nivelDe } from '@/lib/gamificacao';
import { useTheme } from '@/lib/theme';
import { Icone } from './Icone';

/** Nível do jogador com a barra de XP até o próximo. `antes` anima a barra a partir do XP anterior. */
export function NivelBar({ xp, antes, compacto }: { xp: number; antes?: number; compacto?: boolean }) {
  const t = useTheme();
  const n = nivelDe(xp);
  const n0 = nivelDe(antes ?? xp);
  const subiu = n.nivel > n0.nivel;
  const w = useRef(new Animated.Value(subiu ? 0 : n0.pct)).current;
  useEffect(() => {
    Animated.timing(w, { toValue: n.pct, duration: 900, delay: 250, useNativeDriver: false }).start();
  }, [n.pct, w]);
  return (
    <View style={[styles.box, { backgroundColor: t.surface, borderColor: subiu ? t.brand : t.line }, compacto && { padding: 10 }]}
      accessibilityLabel={`Nível ${n.nivel}, ${n.titulo}. ${n.noNivel} de ${n.precisa} XP para o próximo nível`}>
      <View style={[styles.badge, { backgroundColor: t.brand, borderBottomColor: t.brandDeep }]}>
        <Text style={styles.badgeN}>{n.nivel}</Text>
        <Text style={styles.badgeL}>NÍVEL</Text>
      </View>
      <View style={{ flex: 1, gap: 5 }}>
        <View style={styles.row}>
          <Icone nome={n.icone} size={18} color={t.brand} />
          <Text style={[styles.titulo, { color: t.ink }]} numberOfLines={1}>{n.titulo}</Text>
          {subiu && <Text style={[styles.subiu, { color: t.brand }]}>SUBIU!</Text>}
        </View>
        <View style={[styles.bar, { backgroundColor: t.line }]}>
          <Animated.View style={[styles.fill, { backgroundColor: t.brand, width: w.interpolate({ inputRange: [0, 1], outputRange: ['0%', '100%'] }) }]} />
        </View>
        <Text style={[styles.sub, { color: t.muted }]}>{n.noNivel}/{n.precisa} XP para o nível {n.nivel + 1}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 18, padding: 14, width: '100%', maxWidth: 440 },
  badge: { width: 54, height: 54, borderRadius: 16, borderBottomWidth: 4, alignItems: 'center', justifyContent: 'center' },
  badgeN: { color: '#fff', fontSize: 22, fontWeight: '900', lineHeight: 24, fontVariant: ['tabular-nums'] },
  badgeL: { color: 'rgba(255,255,255,0.9)', fontSize: 9, fontWeight: '900', letterSpacing: 1 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  titulo: { fontSize: 16, fontWeight: '900', flexShrink: 1 },
  subiu: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  bar: { height: 12, borderRadius: 99, overflow: 'hidden' },
  fill: { height: '100%', borderRadius: 99 },
  sub: { fontSize: 12, fontWeight: '700', fontVariant: ['tabular-nums'] },
});
