import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import type { BossId } from '@/components/boss-art';
import { Cross } from '@/components/Icons';
import { Icone } from '@/components/Icone';
import { ChefeArte } from '@/components/mapa/ChefeArena';
import { TRACKS } from '@/content';
import { BUGS, type Bug } from '@/content/provas';
import { chefeDaZona } from '@/lib/mapa';
import { useGame } from '@/lib/store';
import { mono, useTheme } from '@/lib/theme';

/** O erro que cada chefe representa. Os exemplos vêm do banco de bugs da Prova de fogo, já conferidos pelo Python. */
const ERRO_DO_CHEFE: Record<BossId, string> = {
  aranha: 'SyntaxError', besouro: 'IndentationError', escaravelho: 'TypeError', centopeia: 'Laço infinito', gosma: 'NameError',
  diabrete: 'IndexError', caveira: 'KeyError', lodo: 'ValueError', golem: 'AttributeError', dragao: 'RecursionError',
};
/** O exemplo mais simples (nível menor, menos linhas) de cada erro. */
const exemploDe = (tipo: string): Bug | undefined =>
  BUGS.filter((b) => b.tipo === tipo).sort((a, b) => a.nivel - b.nivel || a.linhas.length - b.linhas.length)[0];

/** Museu dos erros: cada chefe mostra o erro dele, como acontece, o que o Python diz e como consertar. */
export default function MuseuScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const rotas = useGame((s) => s.rotas);
  const [aberto, setAberto] = useState<number | null>(0);

  /** O chefe i aparece na zona i, i+10, i+20... de cada trilha; vale como "vencido" se alguma dessas já foi premiada. */
  const vencido = (i: number) => TRACKS.some((tr) => tr.course.units.some((u, idx) => idx % 10 === i && rotas?.[u.id]?.premiada));

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Museu dos erros</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]}>
        <Text style={{ color: t.muted, fontWeight: '700', lineHeight: 21 }}>
          Todo chefe é um erro de Python. Conhecer o erro de perto ajuda a reconhecê-lo (e consertá-lo) quando aparecer no seu código.
        </Text>
        {Array.from({ length: 10 }, (_, i) => {
          const chefe = chefeDaZona(i);
          const tipo = ERRO_DO_CHEFE[chefe.id];
          const ex = exemploDe(tipo);
          const on = aberto === i;
          return (
            <View key={chefe.id} style={[styles.card, { backgroundColor: t.surface, borderColor: on ? t.brand : t.line }]}>
              <Pressable onPress={() => setAberto(on ? null : i)} accessibilityRole="button" accessibilityState={{ expanded: on }} accessibilityLabel={`${chefe.nome}, ${tipo}`} style={styles.linhaTopo}>
                <ChefeArte chefe={chefe} size={72} />
                <View style={{ flex: 1, gap: 2 }}>
                  <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>{chefe.nome}</Text>
                  <Text style={{ color: t.muted, fontStyle: 'italic', fontSize: 13 }}>“{chefe.fala}”</Text>
                  {vencido(i) && <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Icone nome="check" size={14} color={t.good} /><Text style={{ color: t.good, fontWeight: '800', fontSize: 12 }}>Chefe derrotado</Text></View>}
                </View>
                <Text style={{ color: t.muted, fontSize: 20, fontWeight: '900' }}>{on ? '−' : '+'}</Text>
              </Pressable>
              {on && ex && (
                <View style={{ gap: 10, paddingTop: 4 }}>
                  <Text style={styles.rot}>O QUE ACONTECE</Text>
                  <Text style={{ color: t.ink, fontWeight: '700', lineHeight: 21 }}>{ex.explica}</Text>
                  <Text style={styles.rot}>O CÓDIGO COM O ERRO</Text>
                  <View style={[styles.codigo, { backgroundColor: t.codeBg }]}>
                    {ex.linhas.map((l, k) => (
                      <View key={k} style={[styles.linha, k === ex.linha && { backgroundColor: 'rgba(240,100,106,0.3)' }]}>
                        <Text style={styles.num}>{k + 1}</Text>
                        <Text style={{ color: t.codeFg, fontFamily: mono, fontSize: 13, flex: 1 }}>{l || ' '}</Text>
                      </View>
                    ))}
                  </View>
                  <Text style={styles.rot}>O QUE O PYTHON DIZ</Text>
                  <View style={[styles.codigo, { backgroundColor: t.codeBg, padding: 10 }]}><Text style={{ color: '#FFB7BA', fontFamily: mono, fontSize: 13 }}>{ex.msg}</Text></View>
                  <Text style={styles.rot}>COMO CONSERTAR (linha {ex.linha + 1})</Text>
                  <View style={[styles.codigo, { backgroundColor: t.codeBg, padding: 10 }]}><Text style={{ color: '#B6F2C6', fontFamily: mono, fontSize: 13 }}>{ex.correcao}</Text></View>
                </View>
              )}
              {on && !ex && <Text style={{ color: t.muted }}>Ainda não há exemplo deste erro.</Text>}
            </View>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 680, width: '100%', alignSelf: 'center' },
  card: { borderWidth: 2, borderRadius: 18, padding: 12, gap: 8 },
  linhaTopo: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  rot: { color: '#6B7886', fontWeight: '900', fontSize: 11, letterSpacing: 0.8 },
  codigo: { borderRadius: 12, paddingVertical: 6, overflow: 'hidden' },
  linha: { flexDirection: 'row', gap: 10, paddingHorizontal: 10, paddingVertical: 1 },
  num: { color: '#6F8496', fontFamily: mono, fontSize: 12, width: 18, textAlign: 'right', paddingTop: 1 },
});
