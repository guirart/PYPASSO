import { router } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';
import { leagueOf } from '@/lib/leagues';
import { Trophy } from './Trophy';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';
import { Flame } from './Icons';
import { Moeda } from './Moeda';

export function TopStats() {
  const t = useTheme();
  const { streak, league, moedas } = useGame();
  return (
    <View style={styles.row}>
      <Pressable onPress={() => router.push('/ranking')} accessibilityLabel={`Liga ${leagueOf(league).gem}: ${leagueOf(league).title}`} hitSlop={6}>
        <Trophy tier={league} size={28} />
      </Pressable>
      <Stat icon={<Flame color={streak ? t.sunDeep : t.muted} />} value={streak} color={streak ? t.sunDeep : t.muted} label="dias seguidos" />
      <Pressable onPress={() => router.push('/loja')} hitSlop={6} accessibilityLabel={`${moedas ?? 0} moedas. Abrir a Loja`}>
        <Stat icon={<Moeda size={20} />} value={moedas ?? 0} color={t.sunDeep} label="moedas" />
      </Pressable>
    </View>
  );
}

function Stat({ icon, value, color, label }: { icon: React.ReactNode; value: number | string; color: string; label: string }) {
  return (
    <View style={styles.stat} accessibilityLabel={`${value} ${label}`}>
      {icon}
      <Text style={[styles.val, { color }]}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 2, alignItems: 'center' },
  stat: { flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 5, paddingVertical: 4 },
  val: { fontWeight: '800', fontSize: 16, fontVariant: ['tabular-nums'] },
});
