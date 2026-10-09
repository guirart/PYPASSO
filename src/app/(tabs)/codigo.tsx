import { router } from 'expo-router';
import { useEffect, useMemo, useRef, useState } from 'react';
import { KeyboardAvoidingView, Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Mascot } from '@/components/Characters';
import { CodeEditorPane, VS, type LineMarks } from '@/components/CodeEditorPane';
import { FloatingPipo } from '@/components/FloatingPipo';
import { PipoPanel, type PanelColors } from '@/components/PipoPanel';
import { aiProvider, reviewAI, reviewLocal, PipoAIError, type Review } from '@/lib/assistant';
import { supabase } from '@/lib/supabase';
import { reportAIAnswer } from '@/lib/account';
import { usePrivacidade } from '@/lib/privacidade';
import { useGame } from '@/lib/store';
import { Icone } from '@/components/Icone';
import { EXAMPLES, usePlayground } from '@/lib/playground';
import { resetRepl, runProject, runRepl } from '@/lib/python/runner';
import { mono } from '@/lib/theme';

type Line = { kind: 'cmd' | 'out' | 'err' | 'info' | 'ok' | 'pipo'; text: string };

const HELLO: Line[] = [
  { kind: 'info', text: 'Python 3 (Pyodide) — terminal de treino do PyPasso' },
  { kind: 'info', text: 'Toque em Executar para rodar o arquivo aberto, ou digite comandos após >>>.' },
];

export default function CodeScreen() {
  const insets = useSafeAreaInsets();
  const { width } = useWindowDimensions();
  const wide = width >= 900;
  const pg = usePlayground();
  const [term, setTerm] = useState<Line[]>(HELLO);
  const [running, setRunning] = useState(false);
  const [cmd, setCmd] = useState('');
  const [history, setHistory] = useState<string[]>([]);
  const [hIdx, setHIdx] = useState(-1);
  const [showStdin, setShowStdin] = useState(true);
  const [menu, setMenu] = useState<'none' | 'examples' | 'newfile'>('none');
  const [newName, setNewName] = useState('');
  const [nameErr, setNameErr] = useState<string | null>(null);
  const [confirmDel, setConfirmDel] = useState<string | null>(null);
  const [cursor, setCursor] = useState({ ln: 1, col: 1 });
  const termRef = useRef<ScrollView>(null);
  // Pipo assistente
  const [pipoOpen, setPipoOpen] = useState(false);
  const [peek, setPeek] = useState<string | null>('Oi! Eu sou o Pipo. Rode seu código e eu te ajudo.');
  const [shakeKey, setShakeKey] = useState(0);
  const [area, setArea] = useState({ w: 0, h: 0 });
  const peekTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const say = (text: string | null, ms = 6000) => {
    setPeek(text);
    if (peekTimer.current) clearTimeout(peekTimer.current);
    if (text) peekTimer.current = setTimeout(() => setPeek(null), ms);
  };
  useEffect(() => { say(peek, 7000); return () => { if (peekTimer.current) clearTimeout(peekTimer.current); }; }, []); // eslint-disable-line react-hooks/exhaustive-deps
  const [review, setReview] = useState<Review | null>(null);
  const [reviewed, setReviewed] = useState<{ file: string; code: string } | null>(null);
  const [reviewing, setReviewing] = useState<'local' | 'ia' | null>(null);
  const [pipoNews, setPipoNews] = useState(false);
  const [lastRun, setLastRun] = useState<{ file: string; code: string; output: string; error: string } | null>(null);
  const [undo, setUndo] = useState<{ file: string; code: string } | null>(null);
  const [ai, setAi] = useState<{ state: 'indisponivel' | 'pronto' | 'pensando' | 'erro'; message?: string }>({ state: 'indisponivel' });
  const aiCtl = useRef<AbortController | null>(null);
  const iaPermitida = usePrivacidade((s) => s.ia); // Central de privacidade: a pessoa pode desligar a explicação com IA

  useEffect(() => {
    let alive = true;
    aiProvider().then((p) => alive && setAi({ state: p ? 'pronto' : 'indisponivel' })).catch(() => {});
    return () => { alive = false; };
  }, []);

  const aiHint = !supabase
    ? 'A explicação com IA aparece quando o app estiver ligado ao Supabase (veja o README).'
    : 'Entre na sua conta (aba Perfil) para usar a explicação com IA.';

  /** Pede a análise do Pipo local para o arquivo aberto. */
  const askPipo = async (opts: { error: string; open: boolean }) => {
    const file = pg.active;
    const snapshot = usePlayground.getState().files;
    setReviewing('local');
    if (opts.open) { setPipoOpen(true); say(null); }
    const r = await reviewLocal({ files: snapshot, entry: file, error: opts.error });
    setReviewing(null);
    setReview(r);
    setReviewed({ file, code: snapshot[file] ?? '' });
    if (ai.state === 'erro') setAi({ state: 'pronto' });
    return r;
  };

  const askAI = async () => {
    if (!review || !usePrivacidade.getState().ia) return;
    const file = pg.active;
    const files = usePlayground.getState().files;
    const same = lastRun && lastRun.file === file && lastRun.code === files[file];
    aiCtl.current = new AbortController();
    setAi({ state: 'pensando' }); setReviewing('ia');
    try {
      const r = await reviewAI({
        files, entry: file, stdin: pg.stdin, output: same ? lastRun!.output : '', error: same ? lastRun!.error : '',
        local: review.fonte === 'local' ? review : null,
      }, aiCtl.current.signal);
      setReview(r); setReviewed({ file, code: files[file] ?? '' }); setAi({ state: 'pronto' });
    } catch (e) {
      const err = e as PipoAIError;
      if (err.code === 'cancelled') setAi({ state: 'pronto' });
      else if (err.code === 'not_granted' || err.code === 'sampling_disabled' || err.code === 'indisponivel') setAi({ state: 'indisponivel' });
      else setAi({ state: 'erro', message: err.message });
    } finally {
      setReviewing(null);
    }
  };

  const apply = (code: string) => {
    const file = pg.active;
    setUndo({ file, code: pg.files[file] ?? '' });
    pg.setCode(file, code);
    setReview((r) => r && { ...r, titulo: 'Pronto, apliquei! Toque em Executar para testar.', humor: 'cheer', problemas: [], dicas: [], corrigido: null, mudancas: [], aviso: undefined });
    push({ kind: 'info', text: `Pipo aplicou a correção em ${file}.` });
  };
  const undoApply = () => {
    if (!undo) return;
    pg.setActive(undo.file); pg.setCode(undo.file, undo.code); setUndo(null);
    setReview(null); push({ kind: 'info', text: '↶ Correção desfeita.' });
  };

  const marks = useMemo<LineMarks | undefined>(() => {
    if (!review || !reviewed || reviewed.file !== pg.active || reviewed.code !== (pg.files[pg.active] ?? '')) return undefined;
    const m: LineMarks = {};
    review.dicas.forEach((d) => { if (d.linha) m[d.linha] = 'tip'; });
    review.problemas.forEach((p) => { if (p.linha && !p.arquivo) m[p.linha] = 'error'; });
    return m;
  }, [review, reviewed, pg.active, pg.files]);

  const push = (...l: Line[]) => setTerm((t) => [...t, ...l].slice(-400));
  const code = pg.files[pg.active] ?? '';

  // input() interativo: o programa pausa na pergunta e o terminal pede a resposta.
  const [waiting, setWaiting] = useState<{ prompt: string; answers: string[]; seed: number; file: string; t0: number } | null>(null);
  const runStart = useRef(0);

  const execRun = async (file: string, answers: string[], seed: number, t0: number) => {
    setRunning(true);
    const r = await runProject(usePlayground.getState().files, file, JSON.stringify(answers), seed);
    setRunning(false);
    const out: Line[] = [];
    const text = (r.stdout + (r.wait ?? '')).replace(/\n$/, '');
    if (text) out.push({ kind: 'out', text });
    if (r.wait !== undefined) {
      setTerm((t) => [...t.slice(0, runStart.current), ...out].slice(-400));
      setWaiting({ prompt: r.wait, answers, seed, file, t0 });
      return;
    }
    setWaiting(null);
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    if (r.error) out.push({ kind: 'err', text: r.error });
    out.push(r.ok ? { kind: 'ok', text: `✓ Concluído em ${secs}s. As variáveis ficam disponíveis no >>>.` } : { kind: 'info', text: `✗ Terminou com erro (${secs}s).` });
    setTerm((t) => [...t.slice(0, runStart.current), ...out].slice(-400));
    const code = usePlayground.getState().files[file] ?? '';
    setLastRun({ file, code, output: r.stdout, error: r.error ?? '' });
    setUndo(null);
    const rev = await askPipo({ error: r.error ?? '', open: !r.ok });
    if (!r.ok) {
      setShakeKey((k) => k + 1);
      push({ kind: 'pipo', text: 'O Pipo encontrou o problema. Veja a caixa dele.' });
    } else if (rev.dicas.length || rev.corrigido) {
      const n = rev.dicas.length;
      say(`Funcionou! Tenho ${n ? `${n} dica${n > 1 ? 's' : ''}` : 'uma melhoria'} pra você. Toque em mim.`, 9000);
      setPipoNews(true);
    } else {
      say('Funcionou! Código limpinho.', 4000);
    }
  };

  const run = async () => {
    if (running) return;
    const fresh = term.length <= HELLO.length;
    const base = [...term, { kind: 'cmd' as const, text: `$ python ${pg.active}` }];
    if (fresh) base.push({ kind: 'info', text: 'Carregando o Python… (só demora na primeira vez)' });
    if (waiting) base.splice(base.length - 1, 0, { kind: 'info', text: '■ Programa anterior interrompido.' });
    setTerm(base.slice(-400));
    runStart.current = Math.min(base.length, 400);
    setWaiting(null);
    // Respostas da caixa Entrada vêm primeiro; o que faltar, o terminal pergunta.
    const pre = pg.stdin ? pg.stdin.replace(/\r/g, '').replace(/\n+$/, '').split('\n') : [];
    useGame.getState().registrar('codigo');
    await execRun(pg.active, pre, 1 + Math.floor(Math.random() * 1e9), Date.now());
  };

  const reply = async () => {
    if (!waiting || running) return;
    const v = cmd;
    setCmd('');
    await execRun(waiting.file, [...waiting.answers, v], waiting.seed, waiting.t0);
  };

  const stop = () => {
    setWaiting(null);
    push({ kind: 'info', text: '■ Programa interrompido.' });
  };

  const revise = async () => {
    const file = pg.active;
    const code = pg.files[file] ?? '';
    const same = lastRun && lastRun.file === file && lastRun.code === code;
    setPipoNews(false);
    await askPipo({ error: same ? lastRun!.error : '', open: true });
  };

  const repl = async () => {
    const src = cmd.trim();
    if (!src) return;
    setCmd(''); setHistory((h) => [...h, src]); setHIdx(-1);
    if (src === 'clear' || src === 'cls') { setTerm(HELLO); return; }
    push({ kind: 'cmd', text: `>>> ${src}` });
    setRunning(true);
    const r = await runRepl(src);
    setRunning(false);
    if (r.stdout) push({ kind: 'out', text: r.stdout.replace(/\n$/, '') });
    if (r.error) push({ kind: 'err', text: r.error });
  };

  const onCmdKey = (e: { nativeEvent: { key: string } }) => {
    const k = e.nativeEvent.key;
    if (k !== 'ArrowUp' && k !== 'ArrowDown' || !history.length) return;
    const idx = k === 'ArrowUp' ? (hIdx < 0 ? history.length - 1 : Math.max(0, hIdx - 1)) : (hIdx < 0 ? -1 : hIdx + 1);
    if (idx >= history.length || idx < 0) { setHIdx(-1); setCmd(''); return; }
    setHIdx(idx); setCmd(history[idx]);
  };

  const createFile = () => {
    const err = pg.addFile(newName);
    if (err) { setNameErr(err); return; }
    setNewName(''); setNameErr(null); setMenu('none');
  };

  const editor = (
    <View style={{ flex: 1, minHeight: 240 }}>
      {/* Abas de arquivo */}
      <View style={styles.tabsRow}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ flexGrow: 1 }}>
          {pg.order.map((name) => {
            const active = name === pg.active;
            return (
              <Pressable key={name} onPress={() => { pg.setActive(name); setConfirmDel(null); }} style={[styles.tab, active && styles.tabActive]}>
                <Text style={[styles.pyDot]}>●</Text>
                <Text style={{ color: active ? '#fff' : VS.dim, fontSize: 13 }}>{name}</Text>
                {name !== 'main.py' && (
                  <Pressable hitSlop={8} onPress={() => { if (confirmDel === name) { pg.removeFile(name); setConfirmDel(null); } else setConfirmDel(name); }}
                    accessibilityLabel={`Fechar e apagar ${name}`}>
                    <Text style={{ color: confirmDel === name ? VS.red : VS.dim, fontSize: 12 }}>{confirmDel === name ? 'apagar?' : '✕'}</Text>
                  </Pressable>
                )}
              </Pressable>
            );
          })}
          <Pressable onPress={() => setMenu(menu === 'newfile' ? 'none' : 'newfile')} style={styles.tabPlus} accessibilityLabel="Novo arquivo">
            <Text style={{ color: VS.dim, fontSize: 18 }}>＋</Text>
          </Pressable>
        </ScrollView>
      </View>

      {/* Barra de ações */}
      <View style={styles.toolbar}>
        <Pressable onPress={run} disabled={running} style={[styles.runBtn, running && { opacity: 0.6 }]} accessibilityLabel="Executar arquivo">
          <Icone nome={running ? 'ampulheta' : waiting ? 'desfazer' : 'play'} size={14} color="#fff" /><Text style={styles.runTxt}>{running ? 'Rodando' : waiting ? 'Reiniciar' : 'Executar'}</Text>
        </Pressable>
        {waiting && (
          <Pressable onPress={stop} style={[styles.toolBtn, { borderColor: VS.red }]} accessibilityLabel="Parar o programa">
            <Text style={[styles.toolTxt, { color: '#FF8A8A' }]}>■ Parar</Text>
          </Pressable>
        )}
        <Pressable onPress={revise} disabled={!!reviewing} style={[styles.toolBtn, { borderColor: VS.blue }]} accessibilityLabel="Revisar com o Pipo">
          <Icone nome="cobra" size={14} color="#7FB0FF" /><Text style={[styles.toolTxt, { color: '#7FB0FF' }]}>Revisar</Text>
        </Pressable>
        <Pressable onPress={() => router.push('/biblioteca')} style={styles.toolBtn} accessibilityLabel="Abrir a Biblioteca">
          <Icone nome="livros" size={16} color="#C5C5C5" />
        </Pressable>
        <Pressable onPress={() => setMenu(menu === 'examples' ? 'none' : 'examples')} style={styles.toolBtn}>
          <Text style={styles.toolTxt}>Exemplos ▾</Text>
        </Pressable>
        <Pressable onPress={() => setShowStdin(!showStdin)} style={styles.toolBtn}>
          <Text style={styles.toolTxt}>Entrada {showStdin ? '▴' : '▾'}</Text>
        </Pressable>
        {Platform.OS === 'web' && <Text style={[styles.hint, { marginLeft: 'auto' }]}>Ctrl+Enter executa · Tab recua</Text>}
      </View>

      {menu === 'newfile' && (
        <View style={styles.dropdown}>
          <Text style={styles.hint}>Nome do novo arquivo (para importar: from nome import …)</Text>
          <View style={{ flexDirection: 'row', gap: 8 }}>
            <TextInput value={newName} onChangeText={(t) => { setNewName(t); setNameErr(null); }} onSubmitEditing={createFile} autoFocus
              placeholder="utils.py" placeholderTextColor={VS.dim} autoCapitalize="none" autoCorrect={false}
              style={[styles.field, { flex: 1, fontFamily: mono }]} />
            <Pressable onPress={createFile} style={styles.runBtn}><Text style={styles.runTxt}>Criar</Text></Pressable>
          </View>
          {nameErr && <Text style={{ color: VS.red }}>{nameErr}</Text>}
        </View>
      )}
      {menu === 'examples' && (
        <View style={styles.dropdown}>
          <Text style={styles.hint}>Carregar um exemplo substitui os arquivos abertos.</Text>
          {EXAMPLES.map((ex) => (
            <Pressable key={ex.title} onPress={() => { pg.load(ex.files, ex.stdin); setMenu('none'); push({ kind: 'info', text: `Exemplo carregado: ${ex.title}` }); }}
              style={({ pressed }) => [styles.exItem, pressed && { backgroundColor: VS.tab }]}>
              <Text style={{ color: VS.text, fontSize: 14 }}>{ex.title}</Text>
              <Text style={{ color: VS.dim, fontSize: 12, fontFamily: mono }}>{Object.keys(ex.files).join(', ')}</Text>
            </Pressable>
          ))}
        </View>
      )}

      <CodeEditorPane value={code} onChange={(v) => pg.setCode(pg.active, v)} onRun={run} onCursor={(ln, col) => setCursor({ ln, col })} marks={marks} />

      {showStdin && (
        <View style={styles.stdin}>
          <Text style={styles.panelTitle}>ENTRADA (opcional) · respostas prontas para input(), uma por linha. Se faltar, o terminal pergunta.</Text>
          <TextInput value={pg.stdin} onChangeText={pg.setStdin} multiline autoCapitalize="none" autoCorrect={false}
            placeholder="Ana" placeholderTextColor={VS.dim}
            style={[styles.field, { fontFamily: mono, minHeight: 52, maxHeight: 110, textAlignVertical: 'top' }]} />
        </View>
      )}
    </View>
  );

  const terminal = (
    <View style={[styles.terminal, wide ? { flex: 0.85, borderLeftWidth: 1 } : { height: 250, borderTopWidth: 1 }]}>
      <View style={styles.termHead}>
        <Text style={styles.panelTitle}>TERMINAL</Text>
        <Pressable onPress={async () => { setTerm(HELLO); await resetRepl(); }} hitSlop={8}><Text style={styles.toolTxt}>Limpar</Text></Pressable>
      </View>
      <ScrollView ref={termRef} style={{ flex: 1 }} contentContainerStyle={{ padding: 10, gap: 2 }}
        onContentSizeChange={() => termRef.current?.scrollToEnd({ animated: false })} keyboardShouldPersistTaps="handled">
        {term.map((l, i) => (
          <Text key={i} selectable style={[styles.termLine, { fontFamily: mono, color: COLORS[l.kind] }]}>{l.text}</Text>
        ))}
      </ScrollView>
      <View style={styles.prompt}>
        <Text style={{ color: waiting ? VS.yellow : VS.green, fontFamily: mono, fontSize: 14 }}>{waiting ? 'input ›' : '>>>'}</Text>
        <TextInput value={cmd} onChangeText={setCmd} onSubmitEditing={waiting ? reply : repl} onKeyPress={waiting ? undefined : onCmdKey} blurOnSubmit={false}
          placeholder={waiting ? 'digite sua resposta e Enter' : 'digite um comando e Enter'} placeholderTextColor={VS.dim} autoCapitalize="none" autoCorrect={false} returnKeyType="send"
          autoFocus={!!waiting} key={waiting ? 'in' : 'cmd'}
          accessibilityLabel={waiting ? 'Resposta para o input' : 'Comando Python'}
          style={[styles.promptInput, { fontFamily: mono }, Platform.OS === 'web' && ({ outlineStyle: 'none' } as object)]} />
      </View>
    </View>
  );

  return (
    <KeyboardAvoidingView style={{ flex: 1, backgroundColor: VS.bg }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <View style={[styles.header, { paddingTop: insets.top + 6 }]}>
        <Mascot size={30} animated={false} />
        <Text style={styles.title}>Código livre</Text>
        <Text style={styles.subtitle}>teste o que quiser, sem valer nota</Text>
      </View>
      <View style={{ flex: 1, flexDirection: wide ? 'row' : 'column' }} onLayout={(e) => setArea({ w: e.nativeEvent.layout.width, h: e.nativeEvent.layout.height })}>
        {editor}
        {terminal}
        <FloatingPipo
          area={area}
          mood={reviewing ? 'think' : review?.humor ?? 'happy'}
          open={pipoOpen}
          onToggle={(o) => {
            setPipoOpen(o); say(null);
            if (o) { setPipoNews(false); if (!review && !reviewing) revise(); }
          }}
          badge={pipoNews || (!!review?.problemas.length && !pipoOpen)}
          peek={peek}
          shakeKey={shakeKey}
          title={reviewing === 'local' ? 'Deixa eu ver seu código…' : reviewing === 'ia' ? 'Pensando com calma…' : review?.titulo ?? 'Oi! Eu sou o Pipo.'}
          colors={{ card: VS.panel, border: '#4A4A4A', text: VS.text, dim: VS.dim, accent: '#7FB0FF', bad: '#F14C4C' }}>
          <PipoPanel
            hideHead
            review={review}
            original={reviewed?.code ?? code}
            colors={PANEL}
            loading={reviewing}
            onApply={(c) => { apply(c); }}
            onUndo={undoApply}
            canUndo={!!undo}
            ai={{ state: iaPermitida ? ai.state : 'indisponivel', message: ai.message, onAsk: askAI, onCancel: () => aiCtl.current?.abort(), hint: aiHint }}
            onReport={(m) => (review ? reportAIAnswer(review, m) : Promise.resolve(true))}
          />
        </FloatingPipo>
      </View>
      <View style={styles.status}>
        <Text style={styles.statusTxt}>Python 3 · Pyodide</Text>
        <Text style={styles.statusTxt}>{pg.active}  ·  Ln {cursor.ln}, Col {cursor.col}</Text>
      </View>
    </KeyboardAvoidingView>
  );
}

const COLORS: Record<Line['kind'], string> = { cmd: VS.yellow, out: VS.text, err: VS.red, info: VS.dim, ok: VS.green, pipo: '#7FB0FF' };
const PANEL: PanelColors = {
  bg: VS.bg, card: VS.panel, border: VS.border, text: VS.text, dim: VS.dim, accent: VS.blue,
  good: VS.green, bad: '#F14C4C', warn: '#D7A54A', codeBg: '#141414', codeFg: VS.text,
};

const styles = StyleSheet.create({
  header: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 12, paddingBottom: 8, backgroundColor: VS.panel, borderBottomWidth: 1, borderBottomColor: VS.border, flexWrap: 'wrap' },
  title: { color: '#fff', fontSize: 17, fontWeight: '800' },
  subtitle: { color: VS.dim, fontSize: 13 },
  tabsRow: { backgroundColor: VS.panel, borderBottomWidth: 1, borderBottomColor: VS.border },
  tab: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: 9, paddingHorizontal: 12, backgroundColor: VS.tab, borderRightWidth: 1, borderRightColor: VS.border },
  tabActive: { backgroundColor: VS.bg, borderTopWidth: 2, borderTopColor: VS.blue, paddingTop: 7 },
  tabPlus: { paddingHorizontal: 14, justifyContent: 'center' },
  pyDot: { color: '#FFD43B', fontSize: 9 },
  toolbar: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 10, paddingVertical: 7, backgroundColor: VS.bg, borderBottomWidth: 1, borderBottomColor: VS.border, flexWrap: 'wrap' },
  runBtn: { backgroundColor: VS.green, borderRadius: 6, paddingVertical: 7, paddingHorizontal: 14, justifyContent: 'center' },
  runTxt: { color: '#fff', fontWeight: '800', fontSize: 14 },
  toolBtn: { borderWidth: 1, borderColor: VS.border, borderRadius: 6, paddingVertical: 6, paddingHorizontal: 10 },
  toolTxt: { color: VS.text, fontSize: 13 },
  hint: { color: VS.dim, fontSize: 12 },
  dropdown: { backgroundColor: VS.panel, borderBottomWidth: 1, borderBottomColor: VS.border, padding: 10, gap: 6 },
  exItem: { paddingVertical: 8, paddingHorizontal: 10, borderRadius: 6, gap: 2 },
  field: { color: VS.text, backgroundColor: VS.bg, borderWidth: 1, borderColor: VS.border, borderRadius: 6, paddingHorizontal: 10, paddingVertical: 8, fontSize: 14 },
  stdin: { backgroundColor: VS.panel, borderTopWidth: 1, borderTopColor: VS.border, padding: 8, gap: 6 },
  panelTitle: { color: VS.dim, fontSize: 11, fontWeight: '700', letterSpacing: 0.8 },
  paneOn: { color: '#fff', textDecorationLine: 'underline' },
  terminal: { backgroundColor: VS.bg, borderColor: VS.border },
  termHead: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 10, paddingVertical: 7, borderBottomWidth: 1, borderBottomColor: VS.border, backgroundColor: VS.panel },
  termLine: { fontSize: 13, lineHeight: 19 },
  prompt: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 10, paddingVertical: 6, borderTopWidth: 1, borderTopColor: VS.border },
  promptInput: { flex: 1, color: VS.text, fontSize: 14, paddingVertical: 6 },
  status: { flexDirection: 'row', justifyContent: 'space-between', backgroundColor: VS.blueBar, paddingHorizontal: 10, paddingVertical: 3 },
  statusTxt: { color: '#fff', fontSize: 12 },
});
