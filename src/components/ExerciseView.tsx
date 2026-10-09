import { useState } from 'react';
import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import type { Exercise } from '@/content/types';
import type { Answer } from '@/lib/grade';
import { runPython } from '@/lib/python/runner';
import { mono, useTheme } from '@/lib/theme';
import { SpeakingHost } from './Characters';
import { CodeBlock } from './CodeBlock';

const KIND: Record<Exercise['k'], string> = {
  mc: 'Escolha a resposta', out: 'Preveja a saída', fill: 'Complete o código',
  order: 'Ordene as linhas', type: 'Escreva a saída', code: 'Escreva e rode', learn: 'Novo conceito',
};

type Props = { ex: Exercise; answer: Answer; onChange: (a: Answer) => void; locked: boolean; reaction?: 'cheer' | 'sad' };

export function ExerciseView({ ex, answer, onChange, locked, reaction }: Props) {
  const t = useTheme();
  if (ex.k === 'learn') return <LearnCard ex={ex} />;
  return (
    <View style={{ gap: 18 }}>
      <Text style={[styles.kind, { color: t.brand }]}>{KIND[ex.k]}</Text>
      <SpeakingHost host={ex.host} text={ex.q} mood={reaction} />
      {answer.k === 'choice' && (ex.k === 'mc' || ex.k === 'out') && <Choice ex={ex} a={answer} onChange={onChange} locked={locked} />}
      {answer.k === 'fill' && ex.k === 'fill' && <Fill ex={ex} a={answer} onChange={onChange} locked={locked} />}
      {answer.k === 'order' && ex.k === 'order' && <Order ex={ex} a={answer} onChange={onChange} locked={locked} />}
      {answer.k === 'type' && ex.k === 'type' && (
        <>
          <CodeBlock code={ex.c} />
          <TextInput
            value={answer.text} editable={!locked} autoCapitalize="none" autoCorrect={false} autoFocus
            placeholder="Digite a saída aqui" placeholderTextColor={t.muted}
            onChangeText={(text) => onChange({ k: 'type', text })}
            style={[styles.input, { borderColor: t.line, backgroundColor: t.surface, color: t.ink, fontFamily: mono }]}
          />
        </>
      )}
      {answer.k === 'code' && ex.k === 'code' && <CodeEditor a={answer} onChange={onChange} locked={locked} />}
    </View>
  );
}

function LearnCard({ ex }: { ex: Extract<Exercise, { k: 'learn' }> }) {
  const t = useTheme();
  return (
    <View style={{ gap: 16 }}>
      <View style={[styles.badge, { backgroundColor: t.sun }]}>
        <Text style={{ color: t.sunInk, fontWeight: '900', fontSize: 12, letterSpacing: 1 }}>NOVO CONCEITO</Text>
      </View>
      <SpeakingHost host={ex.host} text={ex.q} mood="think" />
      <Text style={[styles.body, { color: t.ink }]}>{ex.body}</Text>
      <View style={{ gap: 6 }}>
        <Text style={[styles.caption, { color: t.muted }]}>{ex.rc ?? 'EXEMPLO'}</Text>
        <CodeBlock code={ex.c} />
      </View>
      {ex.out ? (
        <View style={[styles.console, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={[styles.caption, { color: t.muted }]}>{ex.ro ?? 'SAÍDA'}</Text>
          <Text style={{ fontFamily: mono, color: t.ink, fontSize: 15, lineHeight: 22 }}>{ex.out}</Text>
        </View>
      ) : null}
    </View>
  );
}

function Choice({ ex, a, onChange, locked }: { ex: Extract<Exercise, { k: 'mc' | 'out' }>; a: Extract<Answer, { k: 'choice' }>; onChange: (a: Answer) => void; locked: boolean }) {
  const t = useTheme();
  const isMono = ex.mono ?? (ex.k === 'out' || ex.o.some((v) => /[()<>[\]#=]/.test(v)));
  return (
    <>
      {ex.c ? <CodeBlock code={ex.c} /> : null}
      <View style={{ gap: 12 }}>
        {a.options.map((o, i) => {
          const sel = a.selected === i;
          return (
            <Pressable key={i} disabled={locked} accessibilityRole="radio" accessibilityState={{ selected: sel }}
              onPress={() => onChange({ ...a, selected: i })}
              style={[styles.opt, { backgroundColor: sel ? t.brandSoft : t.surface, borderColor: sel ? t.brand : t.line, borderBottomColor: sel ? t.brand : t.line }]}>
              <View style={[styles.key, { borderColor: sel ? t.brand : t.line }]}><Text style={{ color: sel ? t.brand : t.muted, fontWeight: '800', fontSize: 12 }}>{i + 1}</Text></View>
              <Text style={[styles.optText, { color: t.ink }, isMono && { fontFamily: mono, fontWeight: '600', fontSize: 15 }]}>{o.v}</Text>
            </Pressable>
          );
        })}
      </View>
    </>
  );
}

function Tile({ label, onPress, hidden, disabled, left }: { label: string; onPress: () => void; hidden?: boolean; disabled?: boolean; left?: boolean }) {
  const t = useTheme();
  return (
    <Pressable onPress={onPress} disabled={disabled || hidden} accessibilityRole="button"
      style={[styles.tile, { backgroundColor: t.surface, borderColor: t.line, opacity: hidden ? 0 : 1, alignSelf: left ? 'stretch' : 'auto' }]}>
      <Text style={{ fontFamily: mono, fontSize: 15, color: t.ink, fontWeight: '600' }}>{label}</Text>
    </Pressable>
  );
}

function Fill({ ex, a, onChange, locked }: { ex: Extract<Exercise, { k: 'fill' }>; a: Extract<Answer, { k: 'fill' }>; onChange: (a: Answer) => void; locked: boolean }) {
  const t = useTheme();
  const next = a.slots.indexOf(null);
  return (
    <>
      <CodeBlock code={ex.c} renderSlot={(i) => {
        const v = a.slots[i];
        return (
          <Text key={`s${i}`} onPress={locked || v === null ? undefined : () => { const slots = a.slots.slice(); slots[i] = null; onChange({ ...a, slots }); }}
            style={{ backgroundColor: v !== null ? t.brand : 'rgba(255,255,255,0.08)', color: '#fff', textDecorationLine: v === null ? 'underline' : 'none', textDecorationColor: i === next ? t.sun : t.cCom }}>
            {v !== null ? ` ${a.bank[v]} ` : '      '}
          </Text>
        );
      }} />
      <View style={styles.bank}>
        {a.bank.map((w, i) => (
          <Tile key={i} label={w} hidden={a.slots.includes(i)} disabled={locked}
            onPress={() => { if (next < 0) return; const slots = a.slots.slice(); slots[next] = i; onChange({ ...a, slots }); }} />
        ))}
      </View>
    </>
  );
}

function Order({ ex, a, onChange, locked }: { ex: Extract<Exercise, { k: 'order' }>; a: Extract<Answer, { k: 'order' }>; onChange: (a: Answer) => void; locked: boolean }) {
  const t = useTheme();
  return (
    <>
      <View style={[styles.zone, { borderColor: t.lineDeep }]}>
        {a.seq.length === 0 && <Text style={{ color: t.muted, fontWeight: '700', textAlign: 'center', margin: 'auto' }}>Toque nas linhas abaixo na ordem certa</Text>}
        {a.seq.map((li, p) => (
          <Tile key={`${li}-${p}`} left label={ex.l[li]} disabled={locked} onPress={() => onChange({ ...a, seq: a.seq.filter((_, j) => j !== p) })} />
        ))}
      </View>
      <View style={{ gap: 10 }}>
        {a.bank.map((li) => (
          <Tile key={li} left label={ex.l[li]} hidden={a.seq.includes(li)} disabled={locked} onPress={() => onChange({ ...a, seq: [...a.seq, li] })} />
        ))}
      </View>
    </>
  );
}

function CodeEditor({ a, onChange, locked }: { a: Extract<Answer, { k: 'code' }>; onChange: (a: Answer) => void; locked: boolean }) {
  const t = useTheme();
  const [out, setOut] = useState<{ text: string; err: boolean } | null>(null);
  const [running, setRunning] = useState(false);
  const run = async () => {
    setRunning(true); setOut({ text: 'Rodando… (a primeira execução baixa o Python e pode levar alguns segundos)', err: false });
    const r = await runPython(a.text);
    setRunning(false);
    setOut({ text: (r.stdout || '') + (r.error ? (r.stdout ? '\n' : '') + r.error : '') || '(sem saída)', err: !!r.error });
  };
  return (
    <View style={{ gap: 10 }}>
      <TextInput
        value={a.text} editable={!locked} multiline autoCapitalize="none" autoCorrect={false} spellCheck={false}
        onChangeText={(text) => onChange({ k: 'code', text })}
        style={[styles.editor, { backgroundColor: t.codeBg, color: t.codeFg, fontFamily: mono }]}
      />
      <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center' }}>
        <Pressable onPress={run} disabled={running || locked} style={[styles.run, { borderColor: t.brand }]}>
          <Text style={{ color: t.brand, fontWeight: '800' }}>{running ? 'RODANDO…' : 'RODAR'}</Text>
        </Pressable>
        <Text style={{ color: t.muted, fontSize: 13, flex: 1 }}>Rode quantas vezes quiser. "Verificar" roda os testes.</Text>
      </View>
      {out && (
        <View style={[styles.console, { backgroundColor: t.surface, borderColor: out.err ? t.bad : t.line }]}>
          <Text style={{ color: t.muted, fontSize: 11, fontWeight: '800', letterSpacing: 0.8 }}>SAÍDA</Text>
          <Text style={{ fontFamily: mono, color: out.err ? t.bad : t.ink, fontSize: 14 }}>{out.text}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  badge: { alignSelf: 'flex-start', borderRadius: 8, paddingHorizontal: 10, paddingVertical: 4 },
  body: { fontSize: 17, lineHeight: 26, fontWeight: '600' },
  caption: { fontSize: 11, fontWeight: '800', letterSpacing: 0.8 },
  kind: { fontSize: 13, fontWeight: '800', letterSpacing: 1, textTransform: 'uppercase' },
  opt: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderBottomWidth: 5, borderRadius: 14, paddingVertical: 14, paddingHorizontal: 16 },
  key: { width: 28, height: 28, borderRadius: 8, borderWidth: 2, alignItems: 'center', justifyContent: 'center' },
  optText: { flex: 1, fontSize: 17, fontWeight: '700' },
  tile: { borderWidth: 2, borderBottomWidth: 4, borderRadius: 12, paddingVertical: 9, paddingHorizontal: 14 },
  bank: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, justifyContent: 'center' },
  zone: { minHeight: 150, borderWidth: 2, borderStyle: 'dashed', borderRadius: 14, padding: 12, gap: 8 },
  input: { borderWidth: 2, borderRadius: 14, paddingVertical: 14, paddingHorizontal: 16, fontSize: 18 },
  editor: { minHeight: 170, borderRadius: 14, padding: 16, fontSize: 15, lineHeight: 24, textAlignVertical: 'top' },
  run: { borderWidth: 2, borderRadius: 12, paddingVertical: 9, paddingHorizontal: 14 },
  console: { borderWidth: 2, borderRadius: 12, padding: 12, gap: 4 },
});
