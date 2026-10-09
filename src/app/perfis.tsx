import { router } from 'expo-router';
import { useState } from 'react';
import { Platform, Pressable, ScrollView, StyleSheet, Switch, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Avatar, Mascot } from '@/components/Characters';
import { MAX_PERFIS, removerPerfil, trocarPerfil, useProfiles } from '@/lib/profiles';
import { useTheme } from '@/lib/theme';

/** "Quem está estudando?": escolher, criar, renomear e apagar perfis deste aparelho. */
export default function PerfisScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { perfis, ativo, perguntar, criar, editar, setPerguntar } = useProfiles();
  const [editando, setEditando] = useState(false);
  const [novo, setNovo] = useState<string | null>(null);
  const [renomear, setRenomear] = useState<{ id: string; nome: string } | null>(null);
  const [apagar, setApagar] = useState<string | null>(null);
  const [trocando, setTrocando] = useState(false);

  const escolher = async (id: string) => {
    if (editando || trocando) return;
    setTrocando(true);
    if (id !== ativo) await trocarPerfil(id);
    setTrocando(false);
    if (router.canGoBack()) router.back(); else router.replace('/');
  };

  const criarPerfil = async () => {
    const id = novo ? criar(novo) : null;
    if (!id) return;
    setNovo(null);
    await escolher(id);
  };

  const field = [styles.field, { color: t.ink, borderColor: t.line, backgroundColor: t.bg }, Platform.OS === 'web' && ({ outlineStyle: 'none' } as object)];

  return (
    <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top + 12 }}>
      <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled">
        <Mascot size={80} />
        <Text style={[styles.h1, { color: t.ink }]}>{editando ? 'Editar perfis' : 'Quem está estudando?'}</Text>
        <Text style={[styles.sub, { color: t.muted }]}>Cada perfil tem seu próprio progresso, vidas, liga e arquivos.</Text>

        <View style={styles.grid}>
          {perfis.map((p) => (
            <View key={p.id} style={styles.cell}>
              <Pressable onPress={() => escolher(p.id)} disabled={editando} accessibilityRole="button"
                accessibilityLabel={`Perfil ${p.nome}${p.id === ativo ? ', em uso' : ''}`}
                style={({ pressed }) => [styles.card, { borderColor: p.id === ativo ? t.brand : t.line, backgroundColor: t.surface, transform: [{ scale: pressed ? 0.96 : 1 }] }]}>
                <Avatar seed={p.avatar} size={84} />
                {p.conta && <Text style={[styles.badge, { backgroundColor: t.brand }]}>conta</Text>}
              </Pressable>
              {renomear?.id === p.id ? (
                <View style={{ gap: 6, width: '100%' }}>
                  <TextInput value={renomear.nome} onChangeText={(nome) => setRenomear({ id: p.id, nome })} maxLength={20} autoFocus
                    accessibilityLabel="Novo nome" style={field}
                    onSubmitEditing={() => { if (renomear.nome.trim()) editar(p.id, { nome: renomear.nome.trim() }); setRenomear(null); }} />
                  <Button3D label="OK" onPress={() => { if (renomear.nome.trim()) editar(p.id, { nome: renomear.nome.trim() }); setRenomear(null); }} />
                </View>
              ) : (
                <Text style={[styles.name, { color: t.ink }]} numberOfLines={1}>{p.nome}</Text>
              )}
              {editando && renomear?.id !== p.id && (
                <View style={styles.actions}>
                  <Pressable onPress={() => setRenomear({ id: p.id, nome: p.nome })} accessibilityLabel={`Renomear ${p.nome}`} hitSlop={6}>
                    <Text style={[styles.action, { color: t.brand }]}>Editar nome</Text>
                  </Pressable>
                  {p.id !== ativo && perfis.length > 1 && (
                    apagar === p.id ? (
                      <Pressable onPress={async () => { await removerPerfil(p.id); setApagar(null); }} accessibilityLabel={`Confirmar apagar ${p.nome}`} hitSlop={6}>
                        <Text style={[styles.action, { color: t.bad }]}>Apagar mesmo?</Text>
                      </Pressable>
                    ) : (
                      <Pressable onPress={() => setApagar(p.id)} accessibilityLabel={`Apagar ${p.nome}`} hitSlop={6}>
                        <Text style={[styles.action, { color: t.bad }]}>Apagar</Text>
                      </Pressable>
                    )
                  )}
                </View>
              )}
            </View>
          ))}

          {perfis.length < MAX_PERFIS && !editando && (
            <View style={styles.cell}>
              {novo === null ? (
                <Pressable onPress={() => setNovo('')} accessibilityRole="button" accessibilityLabel="Adicionar perfil"
                  style={[styles.card, styles.add, { borderColor: t.line }]}>
                  <Text style={{ fontSize: 40, color: t.muted }}>＋</Text>
                </Pressable>
              ) : (
                <View style={[styles.card, { borderColor: t.brand, backgroundColor: t.surface, padding: 10, gap: 8 }]}>
                  <TextInput value={novo} onChangeText={setNovo} placeholder="Nome" placeholderTextColor={t.muted} maxLength={20} autoFocus
                    accessibilityLabel="Nome do novo perfil" style={field} onSubmitEditing={criarPerfil} />
                  <Button3D label="Criar" disabled={!novo.trim()} onPress={criarPerfil} />
                </View>
              )}
              <Text style={[styles.name, { color: t.muted }]}>{novo === null ? 'Adicionar' : 'Novo perfil'}</Text>
            </View>
          )}
        </View>

        <View style={[styles.opt, { borderColor: t.line, backgroundColor: t.surface }]}>
          <View style={{ flex: 1 }}>
            <Text style={{ color: t.ink, fontWeight: '800' }}>Perguntar ao abrir o app</Text>
            <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>Mostra esta tela quando houver mais de um perfil.</Text>
          </View>
          <Switch value={perguntar} onValueChange={setPerguntar} accessibilityLabel="Perguntar ao abrir o app" />
        </View>
        <Text style={[styles.note, { color: t.muted }]}>
          A conta online (login, liga com pessoas de verdade) fica ligada a um perfil. Os outros estudam offline, na liga de treino. A assinatura Plus vale para todos os perfis do aparelho.
        </Text>

        <Button3D label={editando ? 'Pronto' : 'Editar perfis'} variant="ghost" style={styles.wide}
          onPress={() => { setEditando(!editando); setRenomear(null); setApagar(null); setNovo(null); }} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  body: { alignItems: 'center', gap: 14, padding: 20, paddingBottom: 48, maxWidth: 560, width: '100%', alignSelf: 'center' },
  h1: { fontSize: 26, fontWeight: '900', textAlign: 'center' },
  sub: { fontSize: 15, fontWeight: '700', textAlign: 'center' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 16, marginTop: 8 },
  cell: { width: 132, alignItems: 'center', gap: 8 },
  card: { width: 120, height: 120, borderRadius: 24, borderWidth: 3, alignItems: 'center', justifyContent: 'center' },
  add: { borderStyle: 'dashed' },
  badge: { position: 'absolute', bottom: -10, color: '#fff', fontSize: 11, fontWeight: '900', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 99, overflow: 'hidden' },
  name: { fontSize: 16, fontWeight: '900', maxWidth: 130 },
  actions: { flexDirection: 'row', gap: 10 },
  action: { fontWeight: '800', fontSize: 13 },
  field: { borderWidth: 2, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 8, fontSize: 15, fontWeight: '700', width: '100%' },
  opt: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, padding: 14, width: '100%', marginTop: 8 },
  note: { fontSize: 13, fontWeight: '600', textAlign: 'center', lineHeight: 19 },
  wide: { width: '100%' },
});
