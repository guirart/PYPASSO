import * as Haptics from 'expo-haptics';
import { useEffect, useRef } from 'react';
import { Animated, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useAvisos, type Aviso } from '@/lib/avisos';
import { Icone } from './Icone';
import { useTheme } from '@/lib/theme';

/** Mostra a fila de avisos (um por vez) descendo do topo da tela. */
export function AvisosHost() {
  const atual = useAvisos((s) => s.fila[0]);
  if (!atual) return null;
  return <Cartao key={atual.id} a={atual} />;
}

function Cartao({ a }: { a: Aviso }) {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const tirar = useAvisos((s) => s.tirar);
  const y = useRef(new Animated.Value(-140)).current;
  const pulo = useRef(new Animated.Value(0.6)).current;
  const grande = a.tipo === 'nivel';

  useEffect(() => {
    if (Platform.OS !== 'web') Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success).catch(() => {});
    Animated.parallel([
      Animated.spring(y, { toValue: 0, useNativeDriver: Platform.OS !== 'web', friction: 7 }),
      Animated.spring(pulo, { toValue: 1, useNativeDriver: Platform.OS !== 'web', friction: 4, tension: 120 }),
    ]).start();
    const tempo = setTimeout(sair, grande ? 3600 : 2800);
    return () => clearTimeout(tempo);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function sair() {
    Animated.timing(y, { toValue: -160, duration: 220, useNativeDriver: Platform.OS !== 'web' }).start(() => tirar(a.id));
  }

  const cor = a.tipo === 'nivel' ? t.brand : a.tipo === 'conquista' ? t.sun : t.surface;
  const tinta = a.tipo === 'nivel' ? '#fff' : a.tipo === 'conquista' ? t.sunInk : t.ink;
  return (
    <Animated.View pointerEvents="box-none" style={[styles.wrap, { top: insets.top + 8, transform: [{ translateY: y }] }]}>
      <Pressable onPress={sair} accessibilityRole="alert" accessibilityLabel={`${a.titulo}. ${a.texto ?? ''}`}
        style={[styles.card, { backgroundColor: cor, borderColor: a.tipo === 'info' || !a.tipo ? t.line : 'rgba(0,0,0,0.15)' }]}>
        <Animated.View style={[styles.ic, { backgroundColor: a.tipo === 'nivel' ? 'rgba(255,255,255,0.22)' : a.tipo === 'conquista' ? 'rgba(0,0,0,0.12)' : t.bg, transform: [{ scale: pulo }] }, grande && { width: 54, height: 54 }]}><Icone nome={a.icone} size={grande ? 34 : 28} color={tinta} /></Animated.View>
        <View style={{ flex: 1 }}>
          <Text style={[styles.titulo, { color: tinta }, grande && { fontSize: 22 }]}>{a.titulo}</Text>
          {a.texto ? <Text style={[styles.texto, { color: tinta }]}>{a.texto}</Text> : null}
        </View>
      </Pressable>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  wrap: { position: 'absolute', left: 12, right: 12, alignItems: 'center', zIndex: 1000, elevation: 20 },
  card: { flexDirection: 'row', alignItems: 'center', gap: 12, width: '100%', maxWidth: 460, borderRadius: 18, borderWidth: 2, borderBottomWidth: 5, paddingVertical: 12, paddingHorizontal: 16, shadowColor: '#000', shadowOpacity: 0.2, shadowRadius: 12, shadowOffset: { width: 0, height: 4 } },
  ic: { width: 46, height: 46, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  titulo: { fontSize: 18, fontWeight: '900' },
  texto: { fontSize: 14, fontWeight: '700', opacity: 0.95 },
});
