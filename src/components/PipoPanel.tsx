import { useMemo, useState } from 'react';
import { ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import type { Review } from '@/lib/assistant/types';
import { mono } from '@/lib/theme';
import { Mascot } from './Characters';

/** Cores do painel: o tema escuro da aba Código ou o tema claro/escuro do app. */
export type PanelColors = {
  bg: string; card: string; border: string; text: string; dim: string;
  accent: string; good: string; bad: string; warn: string; codeBg: string; codeFg: string;
};

type DiffLine = { kind: 'same' | 'add' | 'del'; text: string; n?: number };

/** Diferença linha a linha (LCS), suficiente para arquivos de exercício. */
export function diffLines(a: string, b: string): DiffLine[] {
  const A = a.split('\n'), B = b.split('\n');
  if (A.length * B.length > 250000) return B.map((t) => ({ kind: 'add' as const, text: t }));
  const dp = Array.from({ length: A.length + 1 }, () => new Array<number>(B.length + 1).fill(0));
  for (let i = A.length - 1; i >= 0; i--)
    for (let j = B.length - 1; j >= 0; j--)
      dp[i][j] = A[i] === B[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const out: DiffLine[] = [];
  let i = 0, j = 0;
  while (i < A.length && j < B.length) {
    if (A[i] === B[j]) { out.push({ kind: 'same', text: A[i], n: j + 1 }); i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) out.push({ kind: 'del', text: A[i++] });
    else { out.push({ kind: 'add', text: B[j], n: j + 1 }); j++; }
  }
  while (i < A.length) out.push({ kind: 'del', text: A[i++] });
  while (j < B.length) { out.push({ kind: 'add', text: B[j], n: j + 1 }); j++; }
  return out;
}

/** Mostra só as mudanças com 1 linha de contexto. */
function compact(d: DiffLine[]): (DiffLine | { kind: 'gap' })[] {
  const changed = (k: number) => k >= 0 && k < d.length && d[k].kind !== 'same';
  const keep = d.map((_, k) => changed(k) || changed(k - 1) || changed(k + 1));
  const out: (DiffLine | { kind: 'gap' })[] = [];
  d.forEach((l, k) => {
    if (keep[k]) out.push(l);
    else if (out[out.length - 1]?.kind !== 'gap') out.push({ kind: 'gap' });
  });
  return out;
}

export function PipoPanel({ review, original, colors: c, loading, onApply, onUndo, canUndo, ai, compactMode, hideHead, onReport }: {
  review: Review | null;
  original: string;
  colors: PanelColors;
  loading?: 'local' | 'ia' | null;
  onApply?: (code: string) => void;
  onUndo?: () => void;
  canUndo?: boolean;
  ai?: { state: 'indisponivel' | 'pronto' | 'pensando' | 'erro'; message?: string; onAsk: () => void; onCancel?: () => void; hint?: string };
  /** Nas lições: só o diagnóstico, sem entregar o código corrigido. */
  compactMode?: boolean;
  /** Dentro da caixa de diálogo do Pipo flutuante, a fala já aparece no topo. */
  hideHead?: boolean;
  /** Denunciar resposta da IA (exigência da Google Play). */
  onReport?: (motivo: string) => Promise<boolean>;
}) {
  const [report, setReport] = useState<'fechado' | 'escolher' | 'enviando' | 'enviado' | 'erro'>('fechado');
  const diff = useMemo(() => (review?.corrigido ? compact(diffLines(original, review.corrigido)) : []), [review, original]);

  if (!review) {
    return (
      <View style={[styles.empty, { backgroundColor: c.bg, borderBottomLeftRadius: 16, borderBottomRightRadius: 16 }]}>
        {loading ? <ActivityIndicator color={c.accent} /> : hideHead ? null : <Mascot size={84} mood="happy" />}
        <Text style={[styles.emptyTxt, { color: c.dim }]}>
          {loading ? 'O Pipo está lendo seu código…' : 'Rode o código ou toque em "Revisar com o Pipo". Quando der erro, eu explico onde e como corrigir.'}
        </Text>
      </View>
    );
  }

  const mono14 = { fontFamily: mono, fontSize: 13, lineHeight: 19 };
  const Wrapper = (compactMode ? View : ScrollView) as typeof ScrollView;
  return (
    <Wrapper {...(compactMode ? { style: [styles.wrap, { backgroundColor: c.bg, borderRadius: 14 }] } : { style: { flexGrow: 0, flexShrink: 1, backgroundColor: c.bg, borderBottomLeftRadius: 16, borderBottomRightRadius: 16 }, contentContainerStyle: styles.wrap, keyboardShouldPersistTaps: 'handled' as const })}>
      {/* Fala do Pipo */}
      {!hideHead && <View style={styles.head}>
        <Mascot size={compactMode ? 56 : 68} mood={loading ? 'think' : review.humor} />
        <View style={[styles.bubble, { backgroundColor: c.card, borderColor: c.border }]}>
          <View style={styles.badgeRow}>
            <Text style={[styles.name, { color: c.accent }]}>PIPO</Text>
            <Text style={[styles.badge, { color: c.dim, borderColor: c.border }]}>{review.fonte === 'ia' ? 'com IA' : 'análise rápida'}</Text>
          </View>
          <Text style={[styles.say, { color: c.text }]}>{review.titulo}</Text>
        </View>
      </View>}
      {hideHead && <Text style={[styles.badge, { color: c.dim, borderColor: c.border, alignSelf: 'flex-start' }]}>{review.fonte === 'ia' ? 'revisão com IA' : 'análise rápida'}</Text>}

      {review.aviso ? <Text style={{ color: c.warn, fontSize: 13 }}>{review.aviso}</Text> : null}

      {/* Problemas */}
      {review.problemas.map((p, k) => (
        <View key={`p${k}`} style={[styles.card, { backgroundColor: c.card, borderColor: c.bad }]}>
          <View style={styles.cardHead}>
            {p.linha ? <Text style={[styles.chip, { backgroundColor: c.bad }]}>{p.arquivo ? `${p.arquivo} · ` : ''}linha {p.linha}</Text> : null}
            <Text style={[styles.cardTitle, { color: c.text }]}>{p.titulo}</Text>
          </View>
          {p.codigo ? (
            <View style={[styles.code, { backgroundColor: c.codeBg }]}>
              <Text style={[mono14, { color: c.codeFg }]}>{p.codigo}</Text>
            </View>
          ) : null}
          {p.explicacao ? <Text style={[styles.body, { color: c.text }]}><Text style={styles.label}>Por quê: </Text>{p.explicacao}</Text> : null}
          {p.como_corrigir ? <Text style={[styles.body, { color: c.text }]}><Text style={[styles.label, { color: c.good }]}>Como corrigir: </Text>{p.como_corrigir}</Text> : null}
        </View>
      ))}

      {/* Versão corrigida */}
      {!compactMode && review.corrigido && (
        <View style={[styles.card, { backgroundColor: c.card, borderColor: c.good }]}>
          <Text style={[styles.cardTitle, { color: c.text }]}>{review.problemas.length ? 'Como o código fica corrigido' : 'Versão melhorada'}</Text>
          {review.mudancas.map((m, k) => (
            <Text key={`m${k}`} style={[styles.body, { color: c.dim }]}>• {m}</Text>
          ))}
          <ScrollView horizontal style={[styles.code, { backgroundColor: c.codeBg, padding: 0 }]}>
            <View style={{ paddingVertical: 8 }}>
              {diff.map((l, k) =>
                l.kind === 'gap' ? (
                  <Text key={k} style={[mono14, { color: c.dim, paddingHorizontal: 10 }]}>⋯</Text>
                ) : (
                  <Text key={k} style={[mono14, {
                    paddingHorizontal: 10,
                    color: l.kind === 'del' ? '#FFB4B4' : l.kind === 'add' ? '#B6F2C6' : c.codeFg,
                    backgroundColor: l.kind === 'del' ? 'rgba(244,71,71,0.22)' : l.kind === 'add' ? 'rgba(46,160,67,0.25)' : 'transparent',
                    textDecorationLine: l.kind === 'del' ? 'line-through' : 'none',
                  }]}>
                    {l.kind === 'del' ? '− ' : l.kind === 'add' ? '+ ' : '  '}{l.text || ' '}
                  </Text>
                ),
              )}
            </View>
          </ScrollView>
          <View style={styles.row}>
            {onApply && <Pressable onPress={() => onApply(review.corrigido!)} style={[styles.btn, { backgroundColor: c.good }]}><Text style={styles.btnTxt}>✓ Aplicar no editor</Text></Pressable>}
            {canUndo && onUndo && <Pressable onPress={onUndo} style={[styles.btnGhost, { borderColor: c.border }]}><Text style={{ color: c.text }}>Desfazer</Text></Pressable>}
          </View>
        </View>
      )}
      {!compactMode && !review.corrigido && canUndo && onUndo && (
        <Pressable onPress={onUndo} style={[styles.btnGhost, { borderColor: c.border, alignSelf: 'flex-start' }]}><Text style={{ color: c.text }}>Desfazer a última correção</Text></Pressable>
      )}

      {/* Dicas */}
      {!compactMode && review.dicas.length > 0 && (
        <View style={{ gap: 8 }}>
          <Text style={[styles.section, { color: c.dim }]}>DICAS PARA MELHORAR</Text>
          {review.dicas.map((d, k) => (
            <View key={`d${k}`} style={[styles.card, { backgroundColor: c.card, borderColor: d.bug ? c.warn : c.border }]}>
              <View style={styles.cardHead}>
                {d.linha ? <Text style={[styles.chip, { backgroundColor: d.bug ? c.warn : c.accent }]}>linha {d.linha}</Text> : null}
                <Text style={[styles.cardTitle, { color: c.text }]}>{d.titulo}</Text>
              </View>
              {d.explicacao ? <Text style={[styles.body, { color: c.text }]}>{d.explicacao}</Text> : null}
              {(d.antes || d.depois) && (
                <View style={{ gap: 4 }}>
                  {d.antes ? <View style={[styles.code, { backgroundColor: c.codeBg }]}><Text style={[mono14, { color: '#FFB4B4' }]}>{d.antes}</Text></View> : null}
                  {d.depois ? <View style={[styles.code, { backgroundColor: c.codeBg }]}><Text style={[mono14, { color: '#B6F2C6' }]}>{d.depois}</Text></View> : null}
                </View>
              )}
            </View>
          ))}
        </View>
      )}

      {/* IA */}
      {!compactMode && ai && ai.state !== 'indisponivel' && review.fonte === 'local' && (
        <View style={[styles.card, { backgroundColor: c.card, borderColor: c.accent }]}>
          <Text style={[styles.cardTitle, { color: c.text }]}>Quer uma explicação mais completa?</Text>
          <Text style={[styles.body, { color: c.dim }]}>A IA lê o programa inteiro, explica com calma e reescreve o código de um jeito melhor.</Text>
          {ai.state === 'pensando' ? (
            <View style={styles.row}>
              <ActivityIndicator color={c.accent} />
              <Text style={{ color: c.dim }}>Pensando… pode levar alguns segundos.</Text>
              {ai.onCancel && <Pressable onPress={ai.onCancel} style={[styles.btnGhost, { borderColor: c.border }]}><Text style={{ color: c.text }}>Parar</Text></Pressable>}
            </View>
          ) : (
            <Pressable onPress={ai.onAsk} style={[styles.btn, { backgroundColor: c.accent, alignSelf: 'flex-start' }]}>
              <Text style={styles.btnTxt}>Explicar com IA</Text>
            </Pressable>
          )}
          {ai.state === 'erro' && ai.message ? <Text style={{ color: c.bad, fontSize: 13 }}>{ai.message}</Text> : null}
        </View>
      )}
      {/* Denúncia de resposta da IA */}
      {review.fonte === 'ia' && onReport && (
        <View style={{ gap: 6 }}>
          {report === 'fechado' && (
            <Pressable onPress={() => setReport('escolher')} hitSlop={6} accessibilityLabel="Denunciar esta resposta da IA">
              <Text style={{ color: c.dim, fontSize: 12, textDecorationLine: 'underline' }}>⚑ Denunciar esta resposta</Text>
            </Pressable>
          )}
          {report === 'escolher' && (
            <View style={[styles.card, { backgroundColor: c.card, borderColor: c.border }]}>
              <Text style={[styles.body, { color: c.text, fontWeight: '700' }]}>O que há de errado com esta resposta?</Text>
              <View style={styles.row}>
                {['Ofensiva ou inadequada', 'Explicação errada', 'Outro problema'].map((m) => (
                  <Pressable key={m} onPress={async () => { setReport('enviando'); setReport((await onReport(m)) ? 'enviado' : 'erro'); }}
                    style={[styles.btnGhost, { borderColor: c.border }]}>
                    <Text style={{ color: c.text, fontSize: 13 }}>{m}</Text>
                  </Pressable>
                ))}
                <Pressable onPress={() => setReport('fechado')} style={styles.btnGhost}><Text style={{ color: c.dim, fontSize: 13 }}>Cancelar</Text></Pressable>
              </View>
            </View>
          )}
          {report === 'enviando' && <Text style={{ color: c.dim, fontSize: 12 }}>Enviando…</Text>}
          {report === 'enviado' && <Text style={{ color: c.good, fontSize: 12 }}>Obrigado! Sua denúncia foi registrada e vai ajudar a melhorar o Pipo.</Text>}
          {report === 'erro' && <Text style={{ color: c.bad, fontSize: 12 }}>Não consegui enviar agora. Tente de novo mais tarde.</Text>}
        </View>
      )}
      {!compactMode && ai?.state === 'indisponivel' && ai.hint && review.fonte === 'local' ? (
        <Text style={{ color: c.dim, fontSize: 12 }}>{ai.hint}</Text>
      ) : null}
    </Wrapper>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 12, gap: 12, paddingBottom: 28 },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 12, padding: 20 },
  emptyTxt: { textAlign: 'center', fontSize: 14, maxWidth: 320 },
  head: { flexDirection: 'row', alignItems: 'flex-end', gap: 10 },
  bubble: { flex: 1, borderWidth: 1, borderRadius: 14, paddingVertical: 10, paddingHorizontal: 12, gap: 2 },
  badgeRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  name: { fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  badge: { fontSize: 10, borderWidth: 1, borderRadius: 6, paddingHorizontal: 5, paddingVertical: 1, overflow: 'hidden' },
  say: { fontSize: 16, fontWeight: '800', lineHeight: 22 },
  card: { borderWidth: 1, borderLeftWidth: 4, borderRadius: 10, padding: 12, gap: 8 },
  cardHead: { flexDirection: 'row', alignItems: 'center', gap: 8, flexWrap: 'wrap' },
  chip: { color: '#fff', fontSize: 11, fontWeight: '800', borderRadius: 6, paddingHorizontal: 7, paddingVertical: 2, overflow: 'hidden' },
  cardTitle: { fontSize: 15, fontWeight: '800', flexShrink: 1 },
  code: { borderRadius: 6, paddingHorizontal: 10, paddingVertical: 6 },
  body: { fontSize: 14, lineHeight: 20 },
  label: { fontWeight: '800' },
  section: { fontSize: 11, fontWeight: '800', letterSpacing: 0.8 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 10, flexWrap: 'wrap' },
  btn: { borderRadius: 8, paddingVertical: 9, paddingHorizontal: 14 },
  btnTxt: { color: '#fff', fontWeight: '800' },
  btnGhost: { borderWidth: 1, borderRadius: 8, paddingVertical: 8, paddingHorizontal: 12 },
});
