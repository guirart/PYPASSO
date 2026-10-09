import { router } from 'expo-router';
import { useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Cross } from '@/components/Icons';
import { classificar, lerFormula, mostrar, tabela, validade, type Formula, type Tabela, type Veredito } from '@/lib/proposicional';
import { mono, useTheme } from '@/lib/theme';

const SIMBOLOS = ['¬', '∧', '∨', '→', '↔', '(', ')'];
const EXEMPLOS: { nome: string; premissas: string; conclusao: string }[] = [
  { nome: 'Modus ponens', premissas: 'P -> Q\nP', conclusao: 'Q' },
  { nome: 'Modus tollens', premissas: 'P -> Q\n~Q', conclusao: '~P' },
  { nome: 'Afirmar o consequente', premissas: 'P -> Q\nQ', conclusao: 'P' },
  { nome: 'Negar o antecedente', premissas: 'P -> Q\n~P', conclusao: '~Q' },
  { nome: 'Silogismo hipotético', premissas: 'P -> Q\nQ -> R', conclusao: 'P -> R' },
  { nome: 'Silogismo disjuntivo', premissas: 'P | Q\n~P', conclusao: 'Q' },
  { nome: 'De Morgan', premissas: '~(P & Q)', conclusao: '~P | ~Q' },
  { nome: 'Tautologia', premissas: 'P | ~P', conclusao: '' },
];

type Saida = { erro?: string; veredito?: Veredito; tb?: Tabela; classes?: { f: string; c: string }[] };

function analisar(premissasTxt: string, conclusaoTxt: string): Saida {
  try {
    const linhas = premissasTxt.split('\n').map((s) => s.trim()).filter(Boolean);
    const ps: Formula[] = linhas.map((l) => lerFormula(l));
    if (conclusaoTxt.trim()) {
      const c = lerFormula(conclusaoTxt);
      const v = validade(ps, c);
      if (v.vars.length > 8) return { erro: 'Use no máximo 8 letras diferentes.' };
      return { veredito: v, tb: v.tabela };
    }
    if (!ps.length) return { erro: 'Escreva ao menos uma fórmula.' };
    const tb = tabela(ps);
    if (tb.vars.length > 8) return { erro: 'Use no máximo 8 letras diferentes.' };
    return { tb, classes: ps.map((f) => ({ f: mostrar(f), c: classificar(f) })) };
  } catch (e) {
    return { erro: (e as Error).message };
  }
}
const NOME_CLASSE: Record<string, string> = { tautologia: 'Tautologia (sempre verdadeira)', contradicao: 'Contradição (sempre falsa)', contingencia: 'Contingência (depende dos valores)' };

/** Calculadora de lógica: tabela de verdade, validade de argumentos e contra-exemplo. */
export default function LogicaScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const [premissas, setPremissas] = useState('P -> Q\nQ');
  const [conclusao, setConclusao] = useState('P');
  const [foco, setFoco] = useState<'p' | 'c'>('p');
  const refs = { p: useRef<TextInput>(null), c: useRef<TextInput>(null) };
  const saida = analisar(premissas, conclusao);

  const inserir = (s: string) => {
    if (foco === 'p') setPremissas((x) => x + s); else setConclusao((x) => x + s);
    refs[foco].current?.focus();
  };
  const v = saida.veredito;
  const numPrem = premissas.split('\n').map((s) => s.trim()).filter(Boolean).length;

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Calculadora de lógica</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]} keyboardShouldPersistTaps="handled">
        <Text style={{ color: t.muted, fontWeight: '700', lineHeight: 21 }}>
          Escreva as premissas (uma por linha) e a conclusão. Use letras como P, Q, R e os símbolos abaixo, ou o teclado: ~ (não), & (e), | (ou), -&gt; (se...então), &lt;-&gt; (se e somente se).
        </Text>

        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ gap: 8 }}>
          {EXEMPLOS.map((e) => (
            <Pressable key={e.nome} onPress={() => { setPremissas(e.premissas); setConclusao(e.conclusao); }} accessibilityRole="button" accessibilityLabel={`Exemplo: ${e.nome}`}
              style={[styles.chip, { backgroundColor: t.brandSoft, borderColor: t.brand }]}>
              <Text style={{ color: t.brand, fontWeight: '800', fontSize: 13 }}>{e.nome}</Text>
            </Pressable>
          ))}
        </ScrollView>

        <Text style={[styles.rot, { color: t.muted }]}>PREMISSAS (uma por linha)</Text>
        <TextInput ref={refs.p} value={premissas} onChangeText={setPremissas} onFocus={() => setFoco('p')} multiline autoCapitalize="none" autoCorrect={false} spellCheck={false}
          accessibilityLabel="Premissas" placeholder="P -> Q" placeholderTextColor={t.muted}
          style={[styles.input, { borderColor: foco === 'p' ? t.brand : t.line, backgroundColor: t.surface, color: t.ink, fontFamily: mono, minHeight: 84 }]} />
        <Text style={[styles.rot, { color: t.muted }]}>CONCLUSÃO (deixe vazio para só ver a tabela)</Text>
        <TextInput ref={refs.c} value={conclusao} onChangeText={setConclusao} onFocus={() => setFoco('c')} autoCapitalize="none" autoCorrect={false} spellCheck={false}
          accessibilityLabel="Conclusão" placeholder="Q" placeholderTextColor={t.muted}
          style={[styles.input, { borderColor: foco === 'c' ? t.brand : t.line, backgroundColor: t.surface, color: t.ink, fontFamily: mono }]} />

        <View style={styles.teclas}>
          {SIMBOLOS.map((s) => (
            <Pressable key={s} onPress={() => inserir(s)} accessibilityRole="button" accessibilityLabel={`Inserir ${s}`} style={[styles.tecla, { backgroundColor: t.surface, borderColor: t.line }]}>
              <Text style={{ color: t.ink, fontSize: 20, fontWeight: '800' }}>{s}</Text>
            </Pressable>
          ))}
        </View>

        {saida.erro && (
          <View style={[styles.card, { backgroundColor: t.badBg, borderColor: t.bad }]} accessibilityRole="alert">
            <Text style={{ color: t.badInk, fontWeight: '800' }}>{saida.erro}</Text>
          </View>
        )}

        {v && (
          <View style={[styles.card, { backgroundColor: v.valido ? t.goodBg : t.badBg, borderColor: v.valido ? t.good : t.bad }]} accessibilityLabel={v.valido ? 'Argumento válido' : 'Argumento inválido'}>
            <Text style={{ color: v.valido ? t.goodInk : t.badInk, fontWeight: '900', fontSize: 20 }}>{v.valido ? 'Argumento VÁLIDO' : 'Argumento INVÁLIDO'}</Text>
            {v.valido ? (
              <Text style={{ color: t.goodInk, fontWeight: '700', lineHeight: 21 }}>
                {numPrem === 0 ? 'Sem premissas, a conclusão é sempre verdadeira (é uma tautologia).' : v.linhasComPremissasV === 0 ? 'As premissas nunca são todas verdadeiras ao mesmo tempo, então não existe contra-exemplo.' : `Em todas as ${v.linhasComPremissasV} linha(s) em que as premissas são verdadeiras, a conclusão também é.`}
              </Text>
            ) : (
              <Text style={{ color: t.badInk, fontWeight: '700', lineHeight: 21 }}>
                Contra-exemplo: {Object.entries(v.contraExemplo!).map(([k, x]) => `${k} = ${x ? 'V' : 'F'}`).join(', ')}. Nessa situação todas as premissas são verdadeiras e a conclusão é falsa.
              </Text>
            )}
          </View>
        )}

        {saida.classes?.map((c, i) => (
          <View key={i} style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={{ color: t.ink, fontFamily: mono, fontWeight: '700' }}>{c.f}</Text>
            <Text style={{ color: t.brand, fontWeight: '900' }}>{NOME_CLASSE[c.c]}</Text>
          </View>
        ))}

        {saida.tb && <TabelaView tb={saida.tb} contra={v?.contraExemplo} nPrem={v ? numPrem : -1} />}
      </ScrollView>
    </View>
  );
}

function TabelaView({ tb, contra, nPrem }: { tb: Tabela; contra?: Record<string, boolean>; nPrem: number }) {
  const t = useTheme();
  const cabecas = [...tb.vars, ...tb.colunas];
  const larg = (i: number) => (i < tb.vars.length ? 34 : Math.max(64, tb.colunas[i - tb.vars.length].length * 9 + 16));
  const eContra = (v: Record<string, boolean>) => !!contra && tb.vars.every((k) => v[k] === contra[k]);
  const letra = (b: boolean) => (b ? 'V' : 'F');
  return (
    <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line, padding: 0, overflow: 'hidden' }]}>
      <ScrollView horizontal showsHorizontalScrollIndicator>
        <View>
          <View style={[styles.tr, { backgroundColor: t.brandSoft }]}>
            {cabecas.map((h, i) => (
              <Text key={i} style={[styles.td, { width: larg(i), color: i < tb.vars.length ? t.ink : nPrem >= 0 && i - tb.vars.length === nPrem ? t.sunDeep : t.brand, fontWeight: '900', fontFamily: mono }]}>{h}</Text>
            ))}
          </View>
          {tb.linhas.map((l, r) => {
            const c = eContra(l.v);
            return (
              <View key={r} style={[styles.tr, { backgroundColor: c ? t.badBg : 'transparent', borderTopWidth: 1, borderTopColor: t.line }]}>
                {tb.vars.map((k, i) => <Text key={k} style={[styles.td, { width: larg(i), color: t.muted, fontFamily: mono, fontWeight: '800' }]}>{letra(l.v[k])}</Text>)}
                {l.valores.map((x, i) => (
                  <Text key={i} style={[styles.td, { width: larg(tb.vars.length + i), color: x ? t.good : t.bad, fontFamily: mono, fontWeight: '900' }]}>{letra(x)}</Text>
                ))}
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 680, width: '100%', alignSelf: 'center' },
  rot: { fontWeight: '900', fontSize: 11, letterSpacing: 0.8 },
  input: { borderWidth: 2, borderRadius: 14, paddingHorizontal: 14, paddingVertical: 10, fontSize: 18, textAlignVertical: 'top' },
  chip: { borderWidth: 2, borderRadius: 999, paddingHorizontal: 12, paddingVertical: 6 },
  teclas: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  tecla: { minWidth: 44, height: 44, alignItems: 'center', justifyContent: 'center', borderWidth: 2, borderBottomWidth: 4, borderRadius: 12, paddingHorizontal: 10 },
  card: { borderWidth: 2, borderRadius: 16, padding: 14, gap: 6 },
  tr: { flexDirection: 'row' },
  td: { textAlign: 'center', paddingVertical: 8, fontSize: 15 },
});
