import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { nivelDe } from '@/lib/gamificacao';
import { usePlus } from '@/lib/plus';
import { MAX_HEARTS, useGame } from '@/lib/store';
import { BarraVida, Coracoes } from './crimson';
import { Moldura } from './Moldura';

/**
 * Painel do topo da primeira página: o nível com a barra de XP até o próximo (o número do nível fica no orbe) e as vidas
 * em corações de pixel art. Toque na barra para abrir as Missões e nos corações para ver o Plus.
 */
export function HudTopo() {
  const xp = useGame((s) => s.xp);
  const hearts = useGame((s) => s.hearts);
  const plus = usePlus((s) => s.ativo);
  const n = nivelDe(xp);
  return (
    <Moldura tipo="crimsonB" esc={2} style={{ gap: 6, padding: 14 }}>
      <View style={styles.linha}>
        <Pressable onPress={() => router.push('/missoes')} accessibilityRole="button" accessibilityLabel={`Nível ${n.nivel}, ${n.titulo}. ${n.noNivel} de ${n.precisa} XP para o próximo nível. Abrir as Missões`}>
          <BarraVida ratio={n.pct} estilo="orbe" esc={3} orbeTexto={String(n.nivel)} />
        </Pressable>
        <Pressable onPress={() => router.push('/plus')} accessibilityRole="button" accessibilityLabel={plus ? 'Vidas ilimitadas (Plus)' : `${hearts} de ${MAX_HEARTS} vidas. Ver o Plus`} style={styles.vidas}>
          {plus ? <Text style={styles.infinito}>∞</Text> : <Coracoes vidas={hearts} max={MAX_HEARTS} esc={1} />}
        </Pressable>
      </View>
      <View style={styles.linha}>
        <Text style={styles.titulo} numberOfLines={1}>NÍVEL {n.nivel} · {n.titulo.toUpperCase()}</Text>
        <Text style={styles.xp}>{n.noNivel}/{n.precisa} XP</Text>
      </View>
    </Moldura>
  );
}

const styles = StyleSheet.create({
  linha: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 10 },
  vidas: { alignItems: 'flex-end', justifyContent: 'center', flexShrink: 1 },
  infinito: { color: '#FFD9D0', fontSize: 28, fontWeight: '900' },
  titulo: { flex: 1, color: '#EAF0F5', fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  xp: { color: '#EBDDB5', fontSize: 12, fontWeight: '800', fontVariant: ['tabular-nums'] },
});
