import { router, useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { CodeBlock } from '@/components/CodeBlock';
import { lessonById } from '@/content';
import { catName, libById } from '@/content/library';
import { usePlayground } from '@/lib/playground';
import { useGame } from '@/lib/store';
import { mono, useTheme } from '@/lib/theme';
import { Icone } from '@/components/Icone';

export default function LibraryEntry() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const f = libById(decodeURIComponent(id ?? ''));
  // Conceito novo (aprendido numa lição): mostra o destaque nesta visita e deixa de ser "novo".
  const [eraNovo] = useState(() => { const g = useGame.getState(); return !!f && !!g.aprendidos?.[f.id] && !g.vistosBib?.[f.id]; });
  useEffect(() => { if (f) useGame.getState().verNaBiblioteca(f.id); }, [f]);
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { favs, toggleFav, openExample } = usePlayground();

  if (!f) {
    return (
      <View style={[styles.center, { backgroundColor: t.bg }]}>
        <Mascot size={90} mood="sad" />
        <Text style={{ color: t.ink, fontWeight: '800' }}>Não encontrei essa função.</Text>
        <Button3D label="Voltar à biblioteca" onPress={() => router.replace('/biblioteca')} />
      </View>
    );
  }
  const fav = favs.includes(f.id);
  const test = () => {
    openExample(f.id, `# Exemplo da Biblioteca: ${f.nome}\n# Mude o código à vontade e toque em Executar.\n\n${f.exemplo}`, f.entrada);
    router.push('/codigo');
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.top, { paddingTop: insets.top + 8, borderBottomColor: t.line, backgroundColor: t.bg }]}>
        <Pressable onPress={() => (router.canGoBack() ? router.back() : router.replace('/biblioteca'))} hitSlop={10} accessibilityLabel="Voltar">
          <Text style={{ color: t.muted, fontSize: 26, fontWeight: '700' }}>‹</Text>
        </Pressable>
        <Text style={[styles.cat, { color: t.brand, borderColor: t.brand }]}>{catName(f.cat)}</Text>
        {f.builtin ? <Text style={[styles.cat, { color: t.sunDeep, borderColor: t.sunDeep }]}>built-in</Text> : null}
        <Pressable onPress={() => toggleFav(f.id)} hitSlop={10} style={{ marginLeft: 'auto' }} accessibilityLabel={fav ? 'Tirar dos favoritos' : 'Favoritar'}>
          <Icone nome="estrela" size={24} color={fav ? '#E0A21C' : t.line} />
        </Pressable>
      </View>

      <ScrollView contentContainerStyle={styles.wrap}>
        {eraNovo && (
          <View style={[styles.novoBox, { backgroundColor: t.surface, borderColor: t.sun }]}>
            <Icone nome="brilho" size={22} color={t.sunDeep} />
            <Text style={{ color: t.ink, fontWeight: '800', flex: 1 }}>Novo na sua biblioteca! Você aprendeu isso numa lição. Aqui fica o resumo para revisar quando quiser.</Text>
          </View>
        )}
        <View style={{ gap: 6 }}>
          <Text style={[styles.name, { color: t.ink, fontFamily: mono }]}>{f.nome}</Text>
          <Text style={[styles.resumo, { color: t.brand }]}>{f.resumo}</Text>
        </View>

        <Section title="O QUE FAZ">
          <Text style={[styles.body, { color: t.ink }]}>{f.explica}</Text>
        </Section>

        <Section title="COMO ESCREVER">
          <CodeBlock code={f.sig} />
        </Section>

        {f.params.length > 0 && (
          <Section title="PARÂMETROS">
            <View style={{ gap: 8 }}>
              {f.params.map((p) => (
                <View key={p.nome} style={styles.param}>
                  <Text style={[styles.pname, { color: t.brand, backgroundColor: t.brandSoft, fontFamily: mono }]}>{p.nome}</Text>
                  <Text style={[styles.body, { color: t.ink, flex: 1 }]}>{p.desc}</Text>
                </View>
              ))}
            </View>
          </Section>
        )}

        {f.retorna ? (
          <Section title="DEVOLVE">
            <Text style={[styles.body, { color: t.ink }]}>{f.retorna}</Text>
          </Section>
        ) : null}

        <Section title="EXEMPLO">
          <CodeBlock code={f.exemplo} />
          {f.entrada ? (
            <Text style={{ color: t.muted, fontSize: 13 }}>Respostas digitadas: <Text style={{ fontFamily: mono }}>{f.entrada.split('\n').join(', ')}</Text></Text>
          ) : null}
          <View style={[styles.out, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={[styles.label, { color: t.muted }]}>SAÍDA</Text>
            <Text style={{ fontFamily: mono, color: t.ink, fontSize: 14, lineHeight: 21 }}>{f.saida || '(nada é mostrado)'}</Text>
          </View>
          <Button3D label="Testar no editor" onPress={test} />
          {f.licao && lessonById(f.licao) ? (
            <Button3D label={`Fazer a lição de ${f.nome}`} variant="ghost" onPress={() => router.push(`/lesson/${f.licao}`)} />
          ) : null}
        </Section>

        {f.cuidado ? (
          <View style={[styles.warn, { backgroundColor: t.surface, borderColor: t.sunDeep }]}>
            <Mascot size={52} mood="think" animated={false} />
            <View style={{ flex: 1, gap: 2 }}>
              <Text style={{ color: t.sunDeep, fontWeight: '900' }}>CUIDADO</Text>
              <Text style={[styles.body, { color: t.ink }]}>{f.cuidado}</Text>
            </View>
          </View>
        ) : null}

        {f.rel.length > 0 && (
          <Section title="VEJA TAMBÉM">
            <View style={styles.rel}>
              {f.rel.map((r) => {
                const g = libById(r);
                return g ? (
                  <Pressable key={r} onPress={() => router.push(`/biblioteca/${encodeURIComponent(r)}`)}
                    style={[styles.relChip, { borderColor: t.line, backgroundColor: t.surface }]}>
                    <Text style={{ color: t.brand, fontWeight: '700', fontFamily: mono }}>{g.nome}</Text>
                  </Pressable>
                ) : null;
              })}
            </View>
          </Section>
        )}
      </ScrollView>
    </View>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  const t = useTheme();
  return (
    <View style={{ gap: 8 }}>
      <Text style={[styles.label, { color: t.muted }]}>{title}</Text>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  novoBox: { flexDirection: 'row', alignItems: 'center', gap: 10, borderWidth: 2, borderRadius: 14, padding: 12 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 14, padding: 24 },
  top: { flexDirection: 'row', alignItems: 'center', gap: 12, paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  cat: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 10, paddingVertical: 3, fontWeight: '800', fontSize: 12, overflow: 'hidden' },
  wrap: { padding: 16, paddingBottom: 56, gap: 22, maxWidth: 720, width: '100%', alignSelf: 'center' },
  name: { fontSize: 28, fontWeight: '800' },
  resumo: { fontSize: 18, fontWeight: '800' },
  body: { fontSize: 16, lineHeight: 24 },
  label: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  param: { flexDirection: 'row', gap: 10, alignItems: 'flex-start' },
  pname: { fontWeight: '700', borderRadius: 6, paddingHorizontal: 6, paddingVertical: 2, overflow: 'hidden' },
  out: { borderWidth: 2, borderRadius: 12, padding: 12, gap: 4 },
  warn: { flexDirection: 'row', gap: 12, alignItems: 'flex-start', borderWidth: 2, borderLeftWidth: 6, borderRadius: 14, padding: 12 },
  rel: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  relChip: { borderWidth: 2, borderRadius: 10, paddingHorizontal: 10, paddingVertical: 6 },
});
