import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Cross } from '@/components/Icons';
import { PipoPanel } from '@/components/PipoPanel';
import { BUGS } from '@/content/provas';
import { reviewLocal } from '@/lib/assistant';
import type { Review } from '@/lib/assistant/types';
import { runProject } from '@/lib/python/runner';
import { mono, useTheme } from '@/lib/theme';

const INICIAL = `idade = input("Sua idade: ")
if idade >= 18
    print("Maior de idade")
else:
    print("Menor de idade")
`;
const ARQ = 'codigo.py';

/**
 * Detetive de bugs: a pessoa escreve ou cola um código, o app roda e o Pipo explica, linha a linha,
 * o que está errado e como consertar. A análise é local, no aparelho.
 */
export default function DetetiveScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const [codigo, setCodigo] = useState(INICIAL);
  const [review, setReview] = useState<Review | null>(null);
  const [analisado, setAnalisado] = useState('');
  const [saida, setSaida] = useState<{ ok: boolean; texto: string } | null>(null);
  const [ocupado, setOcupado] = useState(false);

  const analisar = async () => {
    if (!codigo.trim() || ocupado) return;
    setOcupado(true); setReview(null); setSaida(null);
    try {
      const r = await runProject({ [ARQ]: codigo }, ARQ, '', 0);
      setSaida({ ok: r.ok, texto: (r.ok ? r.stdout : r.error ?? 'Erro desconhecido') || '(o programa não escreveu nada)' });
      const rev = await reviewLocal({ files: { [ARQ]: codigo }, entry: ARQ, error: r.ok ? '' : r.error ?? '' });
      setReview(rev); setAnalisado(codigo);
    } catch {
      setSaida({ ok: false, texto: 'Não consegui analisar agora. Tente de novo.' });
    }
    setOcupado(false);
  };

  const exemplo = () => {
    const b = BUGS[Math.floor(Math.random() * BUGS.length)];
    setCodigo(b.linhas.join('\n') + '\n'); setReview(null); setSaida(null);
  };

  const linhasRuins = new Set<number>();
  review?.problemas.forEach((p) => { if (p.linha) linhasRuins.add(p.linha); });
  review?.dicas.forEach((d) => { if (d.bug && d.linha) linhasRuins.add(d.linha); });

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Detetive de bugs</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]} keyboardShouldPersistTaps="handled">
        <Text style={{ color: t.muted, fontWeight: '700', lineHeight: 21 }}>
          Escreva ou cole um código Python. O app roda, o Pipo procura o que está errado e mostra em qual linha, por quê e como consertar. Tudo acontece no seu aparelho.
        </Text>
        <TextInput value={codigo} onChangeText={(v) => { setCodigo(v); }} multiline autoCapitalize="none" autoCorrect={false} spellCheck={false}
          accessibilityLabel="Seu código" style={[styles.editor, { backgroundColor: t.codeBg, color: t.codeFg, fontFamily: mono }]} />
        <View style={{ flexDirection: 'row', gap: 10 }}>
          <Button3D label={ocupado ? 'Analisando…' : 'Analisar meu código'} disabled={ocupado || !codigo.trim()} onPress={analisar} style={{ flex: 1 }} />
          <Button3D label="Sortear um bug" variant="ghost" disabled={ocupado} onPress={exemplo} />
        </View>

        {saida && (
          <View style={[styles.card, { backgroundColor: t.surface, borderColor: saida.ok ? t.good : t.bad }]}>
            <Text style={{ color: saida.ok ? t.good : t.bad, fontWeight: '900' }}>{saida.ok ? 'O programa rodou' : 'O programa deu erro'}</Text>
            <Text style={{ color: t.ink, fontFamily: mono, fontSize: 13, lineHeight: 19 }}>{saida.texto}</Text>
          </View>
        )}

        {review && (
          <>
            <View style={[styles.codigo, { backgroundColor: t.codeBg }]}>
              {analisado.replace(/\n$/, '').split('\n').map((l, i) => (
                <View key={i} style={[styles.linha, linhasRuins.has(i + 1) && { backgroundColor: 'rgba(240,100,106,0.28)' }]}>
                  <Text style={[styles.num, linhasRuins.has(i + 1) && { color: '#FFB7BA' }]}>{i + 1}</Text>
                  <Text style={{ color: t.codeFg, fontFamily: mono, fontSize: 13, flex: 1 }}>{l || ' '}</Text>
                </View>
              ))}
            </View>
            <PipoPanel review={review} original={analisado} onApply={(c) => { setCodigo(c); setReview(null); setSaida(null); }}
              colors={{ bg: t.surface, card: t.bg, border: t.line, text: t.ink, dim: t.muted, accent: t.brand, good: t.good, bad: t.bad, warn: t.sunDeep, codeBg: t.codeBg, codeFg: t.codeFg }} />
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 680, width: '100%', alignSelf: 'center' },
  editor: { minHeight: 180, borderRadius: 14, padding: 14, fontSize: 14, lineHeight: 21, textAlignVertical: 'top' },
  card: { borderWidth: 2, borderRadius: 14, padding: 12, gap: 6 },
  codigo: { borderRadius: 14, paddingVertical: 8, overflow: 'hidden' },
  linha: { flexDirection: 'row', gap: 10, paddingHorizontal: 12, paddingVertical: 1 },
  num: { color: '#6F8496', fontFamily: mono, fontSize: 12, width: 22, textAlign: 'right', paddingTop: 1 },
});
