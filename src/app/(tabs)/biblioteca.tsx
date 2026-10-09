import { router } from 'expo-router';
import { useMemo, useState } from 'react';
import { Pressable, ScrollView, SectionList, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Mascot } from '@/components/Characters';
import { LIB, LIB_CATS, catName, searchLib, type LibEntry } from '@/content/library';
import { usePlayground } from '@/lib/playground';
import { useGame } from '@/lib/store';
import { mono, useTheme } from '@/lib/theme';
import { Icone } from '@/components/Icone';

type Filter = 'todas' | 'favs' | string;

export default function LibraryScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const favs = usePlayground((s) => s.favs);
  const aprendidos = useGame((s) => s.aprendidos);
  const vistos = useGame((s) => s.vistosBib);
  // Conceitos que a pessoa acabou de aprender nas lições e ainda não abriu aqui.
  const novos = useMemo(() => Object.entries(aprendidos ?? {}).filter(([id]) => !vistos?.[id])
    .sort((a, b) => b[1] - a[1]).map(([id]) => LIB.find((f) => f.id === id)).filter((f): f is LibEntry => !!f), [aprendidos, vistos]);
  const ehNovo = (id: string) => !!aprendidos?.[id] && !vistos?.[id];
  const [q, setQ] = useState('');
  const [filter, setFilter] = useState<Filter>('todas');

  const sections = useMemo(() => {
    let items = searchLib(q);
    if (filter === 'favs') items = items.filter((f) => favs.includes(f.id));
    else if (filter === 'builtins') items = items.filter((f) => f.builtin).sort((a, b) => a.nome.replace(/^_+/, '').localeCompare(b.nome.replace(/^_+/, '')));
    else if (filter !== 'todas') items = items.filter((f) => f.cat === filter);
    if (filter === 'builtins') return [{ title: 'As 71 funções embutidas, de A a Z', desc: 'Funcionam sem nenhum import.', data: items }];
    if (q.trim()) return items.length ? [{ title: `${items.length} resultado${items.length > 1 ? 's' : ''}`, data: items }] : [];
    const porCategoria = LIB_CATS.map((c) => ({ title: c.nome, desc: c.desc, data: items.filter((f) => f.cat === c.id) })).filter((s) => s.data.length);
    if (filter === 'todas' && novos.length) {
      return [{ title: 'Novos para você', desc: 'O que você acabou de aprender nas lições. Toque para revisar.', novos: true, data: novos }, ...porCategoria];
    }
    return porCategoria;
  }, [q, filter, favs, novos]);

  const chips: { id: Filter; label: string }[] = [
    { id: 'todas', label: 'Todas' },
    { id: 'favs', label: `Favoritas${favs.length ? ` (${favs.length})` : ''}` },
    { id: 'builtins', label: '71 built-ins' },
    ...LIB_CATS.map((c) => ({ id: c.id, label: c.nome })),
  ];

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.header, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <View style={styles.titleRow}>
          <Mascot size={44} mood="think" animated={false} />
          <View style={{ flex: 1 }}>
            <Text style={[styles.h1, { color: t.ink }]}>Biblioteca</Text>
            <Text style={{ color: t.muted, fontWeight: '600' }}>{LIB.length} funções e recursos do Python, incluindo as 71 funções embutidas.</Text>
          </View>
        </View>
        <TextInput
          value={q}
          onChangeText={setQ}
          placeholder="Buscar: strip, ordenar, sortear, arquivo…"
          placeholderTextColor={t.muted}
          autoCapitalize="none"
          autoCorrect={false}
          accessibilityLabel="Buscar na biblioteca"
          style={[styles.search, { backgroundColor: t.surface, borderColor: t.line, color: t.ink }]}
        />
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8 }}>
          {chips.map((c) => {
            const on = filter === c.id;
            return (
              <Pressable key={c.id} onPress={() => setFilter(c.id)} accessibilityRole="button" accessibilityState={{ selected: on }}
                style={[styles.chip, { backgroundColor: on ? t.brand : t.surface, borderColor: on ? t.brand : t.line }]}>
                <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '800', fontSize: 13 }}>{c.label}</Text>
              </Pressable>
            );
          })}
        </ScrollView>
      </View>

      <SectionList
        sections={sections}
        keyExtractor={(f) => f.id}
        stickySectionHeadersEnabled={false}
        contentContainerStyle={styles.list}
        keyboardShouldPersistTaps="handled"
        ListEmptyComponent={
          <View style={styles.empty}>
            <Mascot size={80} mood={filter === 'favs' ? 'happy' : 'sad'} />
            <Text style={{ color: t.muted, fontWeight: '700', textAlign: 'center' }}>
              {filter === 'favs' ? 'Você ainda não favoritou nada. Toque na estrela de uma função para guardá-la aqui.' : `Não achei nada para "${q}". Tente outra palavra, como "texto", "lista" ou "sortear".`}
            </Text>
          </View>
        }
        renderSectionHeader={({ section }) => (
          <View style={styles.secHead}>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>{'novos' in section && <Icone nome="brilho" size={18} color={t.sunDeep} />}<Text style={[styles.secTitle, { color: 'novos' in section ? t.sunDeep : t.ink }]}>{section.title}</Text></View>
            {'desc' in section && section.desc ? <Text style={{ color: t.muted, fontSize: 13 }}>{String(section.desc)}</Text> : null}
          </View>
        )}
        renderItem={({ item }) => <Card f={item} fav={favs.includes(item.id)} novo={ehNovo(item.id)} showCat={!!q.trim() || filter === 'favs'} />}
      />
    </View>
  );
}

function Card({ f, fav, showCat, novo }: { f: LibEntry; fav: boolean; showCat: boolean; novo: boolean }) {
  const t = useTheme();
  return (
    <Pressable onPress={() => router.push(`/biblioteca/${encodeURIComponent(f.id)}`)} accessibilityRole="button" accessibilityLabel={`${novo ? 'Novo: ' : ''}${f.nome}: ${f.resumo}`}
      style={({ pressed }) => [styles.card, { backgroundColor: novo ? t.surface : t.surface, borderColor: novo ? t.sun : t.line, borderBottomColor: novo ? t.sunDeep : t.lineDeep }, novo && styles.cardNovo, pressed && { transform: [{ translateY: 2 }] }]}>
      <View style={{ flex: 1, gap: 2 }}>
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
          <Text style={[styles.name, { color: t.brand, fontFamily: mono, flexShrink: 1 }]} numberOfLines={1}>{f.nome}</Text>
          {novo && <Text style={[styles.novo, { backgroundColor: t.sun, color: t.sunInk }]}>NOVO</Text>}
        </View>
        <Text style={{ color: t.ink, fontWeight: '600' }} numberOfLines={2}>{f.resumo}</Text>
        {showCat ? <Text style={{ color: t.muted, fontSize: 12, fontWeight: '700' }}>{catName(f.cat)}</Text> : null}
      </View>
      {fav ? <Icone nome="estrela" size={16} color="#E0A21C" /> : null}
      <Text style={{ color: t.muted, fontSize: 20 }}>›</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  header: { paddingHorizontal: 16, paddingBottom: 12, gap: 10, borderBottomWidth: 2 },
  titleRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  h1: { fontSize: 26, fontWeight: '900' },
  search: { borderWidth: 2, borderRadius: 14, paddingHorizontal: 14, paddingVertical: 11, fontSize: 16, fontWeight: '600' },
  chip: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 12, paddingVertical: 6 },
  list: { padding: 16, paddingBottom: 48, gap: 8, maxWidth: 720, width: '100%', alignSelf: 'center' },
  secHead: { marginTop: 14, marginBottom: 6, gap: 2 },
  secTitle: { fontSize: 18, fontWeight: '900' },
  card: { flexDirection: 'row', alignItems: 'center', gap: 10, borderWidth: 2, borderBottomWidth: 4, borderRadius: 14, paddingVertical: 10, paddingHorizontal: 14, marginBottom: 8 },
  name: { fontSize: 16, fontWeight: '700' },
  cardNovo: { borderWidth: 3, borderBottomWidth: 5, shadowColor: '#FFC83D', shadowOpacity: 0.35, shadowRadius: 10, shadowOffset: { width: 0, height: 2 }, elevation: 3 },
  novo: { fontSize: 11, fontWeight: '900', letterSpacing: 0.8, paddingHorizontal: 7, paddingVertical: 2, borderRadius: 6, overflow: 'hidden' },
  empty: { alignItems: 'center', gap: 12, padding: 32 },
});
