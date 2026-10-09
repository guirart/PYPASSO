import * as Haptics from 'expo-haptics';
import { router, useLocalSearchParams } from 'expo-router';
import { useMemo, useRef, useState } from 'react';
import { Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { SvgXml } from 'react-native-svg';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { ExerciseView } from '@/components/ExerciseView';
import { Check, Cross, Star } from '@/components/Icons';
import { cenaSvg } from '@/components/scenes';
import { estrelasDigitacao, estrelasLeitura, lerId, questoesDeLeitura, TITULOS, trechosParaDigitar } from '@/lib/especiais';
import { grade, initAnswer, isReady, type Answer, type Verdict } from '@/lib/grade';
import { useGame } from '@/lib/store';
import { MOEDAS } from '@/lib/gamificacao';
import { pushLessonResult } from '@/lib/sync';
import { mono, useTheme } from '@/lib/theme';

const buzz = (ok: boolean) => {
  if (Platform.OS === 'web') return;
  Haptics.notificationAsync(ok ? Haptics.NotificationFeedbackType.Success : Haptics.NotificationFeedbackType.Error).catch(() => {});
};

type Resultado = { estrelas: number; xp: number; melhorou: boolean; linhas: string[] };

/** Exercício especial de uma cena do Pipo na trilha (leitura ou digitação de código). */
export default function EspecialScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { id } = useLocalSearchParams<{ id: string }>();
  const info = lerId(String(id));
  const [fase, setFase] = useState<'intro' | 'jogo' | 'fim'>('intro');
  const [tentativa, setTentativa] = useState(0);
  const [res, setRes] = useState<Resultado | null>(null);
  const melhor = useGame((s) => s.stars?.[String(id)] ?? 0);

  if (!info) {
    return (
      <View style={[styles.center, { backgroundColor: t.bg }]}>
        <Text style={[styles.h2, { color: t.ink }]}>Exercício não encontrado</Text>
        <Button3D label="Voltar" onPress={() => router.back()} />
      </View>
    );
  }

  const terminar = (estrelas: number, linhas: string[]) => {
    const g = useGame.getState();
    const melhorou = g.setStars(String(id), estrelas);
    const xp = estrelas === 0 ? 0 : melhorou ? 4 * estrelas : 2;
    if (xp) { g.completeLesson(null, xp, 100); pushLessonResult(null, xp, 100).catch(() => {}); }
    g.registrar('especiais');
    if (melhorou) g.ganharMoedas(MOEDAS.especial * estrelas);
    setRes({ estrelas, xp, melhorou, linhas });
    setFase('fim');
  };

  const sair = (
    <Pressable onPress={() => router.back()} accessibilityLabel="Sair" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
  );

  if (fase === 'intro') {
    const leitura = info.cena === 'lendo';
    return (
      <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
        <View style={styles.head}>{sair}</View>
        <ScrollView contentContainerStyle={styles.introBody}>
          <SvgXml xml={cenaSvg(info.cena)} width={260} height={230} />
          <Text style={[styles.eyebrow, { color: t.brand }]}>EXERCÍCIO ESPECIAL · UNIDADE {info.numero}</Text>
          <Text style={[styles.h2, { color: t.ink }]}>{TITULOS[info.cena]}</Text>
          <Text style={[styles.sub, { color: t.muted }]}>
            {leitura
              ? `O Pipo separou trechos de "${info.unit.title}". Leia com calma e diga o que cada um mostra na tela. Aqui você não perde vidas.`
              : `Copie trechos de "${info.unit.title}" exatamente como estão, o mais rápido que conseguir. Digitar código treina os dedos para os dois-pontos, parênteses e aspas.`}
          </Text>
          <Estrelas n={melhor} tamanho={30} />
          <Text style={[styles.rule, { color: t.muted }]}>
            {leitura ? '★★★ acertando tudo · ★★ com um erro · ★ mais da metade' : '★ terminando · ★★ rápido e quase sem erros · ★★★ muito rápido e preciso'}
          </Text>
          <Button3D label={melhor ? 'Jogar de novo' : 'Começar'} style={styles.wide} onPress={() => setFase('jogo')} />
        </ScrollView>
      </View>
    );
  }

  if (fase === 'fim' && res) {
    return (
      <View style={[styles.center, { backgroundColor: t.bg, paddingTop: insets.top, paddingBottom: insets.bottom + 20 }]}>
        <Mascot size={130} mood={res.estrelas >= 2 ? 'cheer' : res.estrelas === 1 ? 'happy' : 'sad'} />
        <Estrelas n={res.estrelas} tamanho={44} />
        <Text style={[styles.h2, { color: t.ink }]}>{['Quase lá!', 'Muito bem!', 'Mandou bem!', 'Perfeito!'][res.estrelas]}</Text>
        {res.linhas.map((l) => <Text key={l} style={[styles.sub, { color: t.muted }]}>{l}</Text>)}
        <Text style={[styles.sub, { color: t.brand }]}>
          {res.xp ? `+${res.xp} XP${res.melhorou ? ' (novo recorde de estrelas)' : ''}` : 'Tente de novo para ganhar estrelas.'}
        </Text>
        <Button3D label="Continuar" style={styles.wide} onPress={() => router.back()} />
        {res.estrelas < 3 && <Button3D label="Tentar de novo" variant="ghost" style={styles.wide} onPress={() => { setTentativa((n) => n + 1); setFase('jogo'); }} />}
      </View>
    );
  }

  return info.cena === 'lendo'
    ? <Leitura key={tentativa} unitId={info.unit.id} tentativa={tentativa} sair={sair} onFim={terminar} />
    : <Digitacao key={tentativa} unitId={info.unit.id} tentativa={tentativa} sair={sair} onFim={terminar} />;
}

function Estrelas({ n, tamanho }: { n: number; tamanho: number }) {
  const t = useTheme();
  return (
    <View style={{ flexDirection: 'row', gap: 6 }} accessibilityLabel={`${n} de 3 estrelas`}>
      {[0, 1, 2].map((i) => <Star key={i} color={i < n ? t.sun : t.line} size={tamanho} />)}
    </View>
  );
}

// ---------------------------------------------------------------- Leitura de código
function Leitura({ unitId, tentativa, sair, onFim }: { unitId: string; tentativa: number; sair: React.ReactNode; onFim: (e: number, linhas: string[]) => void }) {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const unit = lerId(`lendo-${unitId}`)!.unit;
  const qs = useMemo(() => questoesDeLeitura(unit, tentativa), [unit, tentativa]);
  const [i, setI] = useState(0);
  const [acertos, setAcertos] = useState(0);
  const [answer, setAnswer] = useState<Answer>(() => initAnswer(qs[0]));
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const ex = qs[i];

  const verificar = async () => {
    if (!isReady(answer) || verdict) return;
    const v = await grade(ex, answer);
    setVerdict(v); buzz(v.ok);
    if (v.ok) setAcertos((a) => a + 1);
  };
  const proxima = () => {
    if (i + 1 >= qs.length) {
      const total = qs.length;
      const ac = acertos;
      onFim(estrelasLeitura(ac, total), [`${ac} de ${total} trechos lidos certinho.`]);
      return;
    }
    setI(i + 1); setVerdict(null); setAnswer(initAnswer(qs[i + 1]));
  };
  const footBg = verdict ? (verdict.ok ? t.goodBg : t.badBg) : t.bg;
  const footInk = verdict ? (verdict.ok ? t.goodInk : t.badInk) : t.ink;
  return (
    <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
      <View style={styles.head}>
        {sair}
        <View style={[styles.prog, { backgroundColor: t.line }]}><View style={[styles.progFill, { backgroundColor: t.brand, width: `${(i / qs.length) * 100}%` }]} /></View>
        <Text style={{ color: t.brand, fontWeight: '900' }}>{i + 1}/{qs.length}</Text>
      </View>
      <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled">
        <ExerciseView key={ex.id} ex={ex} answer={answer} onChange={setAnswer} locked={!!verdict} reaction={verdict ? (verdict.ok ? 'cheer' : 'sad') : undefined} />
      </ScrollView>
      <View style={[styles.foot, { backgroundColor: footBg, borderTopColor: verdict ? 'transparent' : t.line, paddingBottom: insets.bottom + 16 }]}>
        {verdict && (
          <View style={styles.fb}>
            {verdict.ok ? <Check color={t.good} size={28} /> : <Cross color={t.bad} size={28} />}
            <View style={{ flex: 1 }}>
              <Text style={{ color: footInk, fontWeight: '900', fontSize: 18 }}>{verdict.ok ? 'Leu certinho!' : 'Resposta correta:'}</Text>
              {!verdict.ok && !!verdict.solution && <Text style={{ color: footInk, fontFamily: mono }}>{verdict.solution}</Text>}
              <Text style={{ color: footInk, fontWeight: '600' }}>{ex.e}</Text>
            </View>
          </View>
        )}
        <Button3D style={styles.wide} label={verdict ? 'Continuar' : 'Verificar'} variant={verdict ? (verdict.ok ? 'good' : 'bad') : 'brand'}
          disabled={!verdict && !isReady(answer)} onPress={verdict ? proxima : verificar} />
      </View>
    </View>
  );
}

// ---------------------------------------------------------------- Digitação de código
const SIMBOLOS = ['⇥', '(', ')', ':', '"', "'", '[', ']', '=', '_', '.', ',', '+', '{', '}', '↵'];

function Digitacao({ unitId, tentativa, sair, onFim }: { unitId: string; tentativa: number; sair: React.ReactNode; onFim: (e: number, linhas: string[]) => void }) {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const unit = lerId(`digitando-${unitId}`)!.unit;
  const trechos = useMemo(() => trechosParaDigitar(unit, tentativa), [unit, tentativa]);
  const [i, setI] = useState(0);
  const [texto, setTexto] = useState('');
  const [erros, setErros] = useState(0);
  const [agora, setAgora] = useState(Date.now());
  const inicio = useRef<number | null>(null);
  const input = useRef<TextInput>(null);
  const alvo = trechos[i] ?? '';
  const totalChars = trechos.reduce((n, x) => n + x.length, 0);

  const mudar = (novo: string) => {
    novo = novo.replace(/\r/g, '').replace(/\t/g, '    ');
    if (inicio.current === null && novo) inicio.current = Date.now();
    // conta erro quando a pessoa acrescenta um caractere diferente do esperado
    let errosAgora = erros;
    if (novo.length > texto.length) {
      for (let k = texto.length; k < novo.length; k++) if (novo[k] !== alvo[k]) errosAgora++;
      setErros(errosAgora);
    }
    setTexto(novo);
    setAgora(Date.now());
    const limpo = (s: string) => s.split('\n').map((l) => l.replace(/\s+$/, '')).join('\n').replace(/\n+$/, '');
    if (limpo(novo) === limpo(alvo)) {
      buzz(true);
      if (i + 1 >= trechos.length) {
        const min = Math.max(1, Date.now() - (inicio.current ?? Date.now())) / 60000;
        const cpm = Math.round(totalChars / min);
        const precisao = Math.max(0, 1 - errosAgora / totalChars);
        onFim(estrelasDigitacao(cpm, precisao), [`${cpm} caracteres por minuto`, `Precisão: ${Math.round(precisao * 100)}%`]);
      } else {
        setI(i + 1); setTexto('');
      }
    }
  };
  const inserir = (s: string) => {
    mudar(texto + (s === '⇥' ? '    ' : s === '↵' ? '\n' : s));
    input.current?.focus();
  };

  // Texto-alvo pintado: verde = certo, vermelho = errado, cinza = falta digitar.
  const cor = (k: number) => (k < texto.length ? (texto[k] === alvo[k] ? t.good : t.bad) : t.muted);
  const segundos = inicio.current ? Math.floor((agora - inicio.current) / 1000) : 0;
  return (
    <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
      <View style={styles.head}>
        {sair}
        <View style={[styles.prog, { backgroundColor: t.line }]}><View style={[styles.progFill, { backgroundColor: t.brand, width: `${(i / trechos.length) * 100}%` }]} /></View>
        <Text style={{ color: t.brand, fontWeight: '900', fontVariant: ['tabular-nums'] }}>⌨️ {i + 1}/{trechos.length} · {segundos}s</Text>
      </View>
      <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="always">
        <Text style={[styles.h3, { color: t.ink }]}>Copie o código</Text>
        <Pressable onPress={() => input.current?.focus()} style={[styles.alvo, { backgroundColor: t.codeBg }]} accessibilityLabel={`Código para copiar: ${alvo}`}>
          <Text style={{ fontFamily: mono, fontSize: 16, lineHeight: 26 }}>
            {alvo.split('').map((c, k) => (
              <Text key={k} style={{ color: cor(k), backgroundColor: k < texto.length && texto[k] !== alvo[k] ? 'rgba(240,100,106,0.25)' : k === texto.length ? 'rgba(255,255,255,0.18)' : 'transparent' }}>
                {c === '\n' ? '↵\n' : c === ' ' && k < texto.length && texto[k] !== ' ' ? '·' : c}
              </Text>
            ))}
          </Text>
        </Pressable>
        <TextInput ref={input} value={texto} onChangeText={mudar} multiline autoFocus autoCapitalize="none" autoCorrect={false} spellCheck={false}
          accessibilityLabel="Digite aqui" placeholder="Digite aqui…" placeholderTextColor={t.muted}
          style={[styles.digitar, { color: t.ink, borderColor: t.line, backgroundColor: t.surface, fontFamily: mono }, Platform.OS === 'web' && ({ outlineStyle: 'none' } as object)]} />
        <View style={styles.simbolos}>
          {SIMBOLOS.map((s) => (
            <Pressable key={s} onPress={() => inserir(s)} style={[styles.simbolo, { borderColor: t.line, backgroundColor: t.surface }]} accessibilityLabel={`Inserir ${s === '⇥' ? 'recuo' : s === '↵' ? 'nova linha' : s}`}>
              <Text style={{ color: t.ink, fontFamily: mono, fontWeight: '700' }}>{s}</Text>
            </Pressable>
          ))}
        </View>
        <Text style={{ color: t.muted, fontWeight: '700' }}>Erros: {erros} · Quando o código ficar igual, o próximo aparece sozinho.</Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingVertical: 12, maxWidth: 760, width: '100%', alignSelf: 'center' },
  prog: { flex: 1, height: 16, borderRadius: 99, overflow: 'hidden' },
  progFill: { height: '100%', borderRadius: 99 },
  introBody: { alignItems: 'center', gap: 12, padding: 20, paddingBottom: 40, maxWidth: 560, width: '100%', alignSelf: 'center' },
  body: { padding: 16, gap: 12, paddingBottom: 32, maxWidth: 640, width: '100%', alignSelf: 'center' },
  eyebrow: { fontSize: 12, fontWeight: '900', letterSpacing: 1.2 },
  h2: { fontSize: 26, fontWeight: '900', textAlign: 'center' },
  h3: { fontSize: 20, fontWeight: '900' },
  sub: { fontSize: 16, fontWeight: '700', textAlign: 'center', lineHeight: 22 },
  rule: { fontSize: 13, fontWeight: '700', textAlign: 'center' },
  wide: { width: '100%', maxWidth: 440 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 14, padding: 24 },
  foot: { borderTopWidth: 2, paddingHorizontal: 16, paddingTop: 16, gap: 12, alignItems: 'center' },
  fb: { flexDirection: 'row', gap: 12, alignItems: 'flex-start', maxWidth: 728, width: '100%' },
  alvo: { borderRadius: 14, padding: 16 },
  digitar: { borderWidth: 2, borderRadius: 14, padding: 14, fontSize: 16, minHeight: 110, textAlignVertical: 'top' },
  simbolos: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  simbolo: { borderWidth: 2, borderRadius: 10, minWidth: 40, paddingVertical: 8, alignItems: 'center' },
});
