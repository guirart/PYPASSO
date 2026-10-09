import { router } from 'expo-router';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { lessonById } from '@/content';
import { PROJETOS } from '@/content/projetos';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';
import { IconeTile } from '@/components/Icone';
import { COR_PROJ, ICONE_PROJ } from '@/content/projetos';

/** Lista dos Projetos guiados: cada um libera com uma lição da trilha Python do zero. */
export default function ProjetosScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const done = useGame((s) => s.done);
  const prog = useGame((s) => s.projetos ?? {});
  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => (router.canGoBack() ? router.back() : router.replace('/'))} hitSlop={10} accessibilityLabel="Voltar">
          <Text style={{ color: t.muted, fontSize: 28, fontWeight: '700' }}>‹</Text>
        </Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Projetos guiados</Text>
      </View>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 21 }}>
          Programas de verdade, construídos passo a passo. Cada passo tem testes automáticos, dica e, se travar, a solução. No fim, você joga o que fez no editor. Cada passo vale 15 XP e o projeto pronto, 50 moedas.
        </Text>
        {PROJETOS.map((p) => {
          const livre = p.requer in done;
          const pr = prog[p.id];
          const feito = !!pr?.feito;
          const passo = feito ? p.passos.length : pr?.passo ?? 0;
          return (
            <Pressable key={p.id} onPress={() => router.push(`/projeto/${p.id}`)} accessibilityRole="button"
              accessibilityLabel={`${p.titulo}. ${livre ? (feito ? 'Concluído' : `Passo ${passo + 1} de ${p.passos.length}`) : 'Bloqueado'}`}
              style={({ pressed }) => [styles.card, { backgroundColor: t.surface, borderColor: feito ? t.good : livre ? t.brand : t.line, borderBottomWidth: pressed ? 2 : 5, opacity: livre ? 1 : 0.75 }]}>
              <IconeTile nome={livre ? ICONE_PROJ[p.id] ?? 'martelo' : 'cadeado'} cor={COR_PROJ[p.id] ?? t.brand} size={52} apagado={!livre} />
              <View style={{ flex: 1, gap: 4 }}>
                <Text style={[styles.nome, { color: t.ink }]}>{p.titulo}</Text>
                <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{p.resumo}</Text>
                {livre ? (
                  <View style={styles.row}>
                    <View style={[styles.bar, { backgroundColor: t.line }]}><View style={[styles.fill, { backgroundColor: feito ? t.good : t.brand, width: `${(passo / p.passos.length) * 100}%` }]} /></View>
                    <Text style={{ color: feito ? t.good : t.brand, fontWeight: '900', fontSize: 12 }}>{feito ? 'PRONTO' : `${passo}/${p.passos.length}`}</Text>
                  </View>
                ) : (
                  <Text style={{ color: t.sunDeep, fontWeight: '800', fontSize: 12 }}>Libera depois de "{lessonById(p.requer)?.title ?? p.requer}"</Text>
                )}
              </View>
            </Pressable>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  h1: { fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, paddingBottom: 50, gap: 12, maxWidth: 620, width: '100%', alignSelf: 'center' },
  card: { flexDirection: 'row', alignItems: 'center', gap: 14, borderWidth: 2, borderRadius: 18, padding: 14 },
  emoji: { fontSize: 36 },
  nome: { fontSize: 18, fontWeight: '900' },
  row: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 2 },
  bar: { flex: 1, height: 10, borderRadius: 99, overflow: 'hidden' },
  fill: { height: '100%', borderRadius: 99 },
});
