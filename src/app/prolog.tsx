import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Cross } from '@/components/Icons';
import { EXEMPLOS_PROLOG } from '@/lib/logica/exemplos';
import { Prolog } from '@/lib/logica/prolog';
import { mono, useTheme } from '@/lib/theme';

type Resposta = { erros: string[]; solucoes: Record<string, string>[]; saida: string; mais: boolean; erro?: string; consulta: string };

/** Laboratório Prolog: escreva fatos e regras, faça perguntas e veja as respostas (interpretador próprio, roda no aparelho). */
export default function PrologScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const [ex, setEx] = useState(EXEMPLOS_PROLOG[0]);
  const [programa, setPrograma] = useState(ex.programa);
  const [consulta, setConsulta] = useState(ex.consulta);
  const [max, setMax] = useState(10);
  const [resp, setResp] = useState<Resposta | null>(null);

  const rodar = (m = 10, q = consulta, prog = programa) => {
    const p = new Prolog();
    const erros = p.carregar(prog);
    const r = p.consultar(q, m);
    setMax(m);
    setResp({ erros, solucoes: r.solucoes, saida: r.saida, mais: r.mais, erro: r.erro, consulta: q });
  };
  const escolher = (e: (typeof EXEMPLOS_PROLOG)[number]) => {
    setEx(e); setPrograma(e.programa); setConsulta(e.consulta); rodar(10, e.consulta, e.programa);
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Laboratório Prolog</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]} keyboardShouldPersistTaps="handled">
        <Text style={{ color: t.muted, fontWeight: '700', lineHeight: 21 }}>
          Escolha um exemplo (inspirados nos do SWISH) ou escreva o seu. Em cima ficam os fatos e as regras; embaixo, a pergunta.
        </Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8 }}>
          {EXEMPLOS_PROLOG.map((e) => {
            const on = e.id === ex.id;
            return (
              <Pressable key={e.id} onPress={() => escolher(e)} accessibilityRole="button" accessibilityState={{ selected: on }} accessibilityLabel={`Exemplo: ${e.nome}`}
                style={[styles.chip, { backgroundColor: on ? t.brand : t.brandSoft, borderColor: t.brand }]}>
                <Text style={{ color: on ? '#fff' : t.brand, fontWeight: '800', fontSize: 13 }}>{e.nome}</Text>
              </Pressable>
            );
          })}
        </ScrollView>
        <Text style={{ color: t.muted, fontSize: 13, fontWeight: '700' }}>{ex.descricao}</Text>

        <Text style={[styles.rot, { color: t.muted }]}>PROGRAMA</Text>
        <TextInput value={programa} onChangeText={setPrograma} multiline autoCapitalize="none" autoCorrect={false} spellCheck={false} accessibilityLabel="Programa Prolog"
          style={[styles.input, { borderColor: t.line, backgroundColor: t.codeBg, color: t.codeFg, fontFamily: mono, minHeight: 190, fontSize: 14, lineHeight: 20 }]} />

        <Text style={[styles.rot, { color: t.muted }]}>PERGUNTA</Text>
        <View style={styles.linha}>
          <Text style={{ color: t.brand, fontFamily: mono, fontWeight: '900', fontSize: 18 }}>?-</Text>
          <TextInput value={consulta} onChangeText={setConsulta} onSubmitEditing={() => rodar()} autoCapitalize="none" autoCorrect={false} spellCheck={false} accessibilityLabel="Pergunta"
            placeholder="gosta(maria, X)." placeholderTextColor={t.muted}
            style={[styles.input, { flex: 1, borderColor: t.line, backgroundColor: t.surface, color: t.ink, fontFamily: mono, fontSize: 16, paddingVertical: 8 }]} />
        </View>
        <Pressable onPress={() => rodar()} accessibilityRole="button" accessibilityLabel="Rodar a pergunta"
          style={({ pressed }) => [styles.botao, { backgroundColor: t.brand, borderBottomColor: t.brandDeep, opacity: pressed ? 0.9 : 1 }]}>
          <Text style={{ color: '#fff', fontWeight: '900', fontSize: 16 }}>RODAR</Text>
        </Pressable>

        {resp && (
          <View style={[styles.card, { backgroundColor: t.surface, borderColor: resp.erro || resp.erros.length ? t.bad : t.line }]} accessibilityLabel="Resultado">
            {resp.erros.map((e, i) => <Text key={i} style={{ color: t.bad, fontWeight: '800', fontFamily: mono, fontSize: 13 }}>{e}</Text>)}
            {!!resp.saida && <Text style={{ color: t.ink, fontFamily: mono, fontSize: 14 }}>{resp.saida}</Text>}
            {resp.solucoes.length === 0 && !resp.erro && <Text style={{ color: t.ink, fontFamily: mono, fontWeight: '900', fontSize: 16 }}>false.</Text>}
            {resp.solucoes.map((s, i) => {
              const pares = Object.entries(s);
              return (
                <Text key={i} style={{ color: t.ink, fontFamily: mono, fontSize: 15, lineHeight: 22 }}>
                  {pares.length === 0 ? 'true.' : pares.map(([k, v]) => `${k} = ${v}`).join(',\n') + (i === resp.solucoes.length - 1 && !resp.mais ? '.' : ' ;')}
                </Text>
              );
            })}
            {resp.mais && (
              <Pressable onPress={() => rodar(max + 10, resp.consulta)} accessibilityRole="button" style={[styles.chip, { alignSelf: 'flex-start', backgroundColor: t.brandSoft, borderColor: t.brand }]}>
                <Text style={{ color: t.brand, fontWeight: '800' }}>Ver mais respostas</Text>
              </Pressable>
            )}
            {!!resp.erro && <Text style={{ color: t.bad, fontWeight: '800', lineHeight: 21 }}>{resp.erro}</Text>}
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 680, width: '100%', alignSelf: 'center' },
  rot: { fontWeight: '900', fontSize: 11, letterSpacing: 0.8 },
  input: { borderWidth: 2, borderRadius: 14, paddingHorizontal: 14, paddingVertical: 10, textAlignVertical: 'top' },
  linha: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  chip: { borderWidth: 2, borderRadius: 999, paddingHorizontal: 12, paddingVertical: 6 },
  botao: { alignItems: 'center', borderRadius: 16, paddingVertical: 13, borderBottomWidth: 4 },
  card: { borderWidth: 2, borderRadius: 16, padding: 14, gap: 6 },
});
