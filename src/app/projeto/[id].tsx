import { router, useLocalSearchParams } from 'expo-router';
import { useRef, useState } from 'react';
import { Pressable, ScrollView, Share, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { Celebration } from '@/components/Celebration';
import { CodeBlock } from '@/components/CodeBlock';
import { Cross } from '@/components/Icons';
import { Moeda } from '@/components/Moeda';
import { NivelBar } from '@/components/NivelBar';
import { lessonById } from '@/content';
import { ICONE_PROJ, projetoPorId } from '@/content/projetos';
import { MOEDAS } from '@/lib/gamificacao';
import { usePlayground } from '@/lib/playground';
import { runProject, runPython } from '@/lib/python/runner';
import { useGame } from '@/lib/store';
import { mono, useTheme } from '@/lib/theme';
import { Icone } from '@/components/Icone';

const XP_PASSO = 15;
const XP_FINAL = 30;

/** Projeto guiado: um programa de verdade construído passo a passo, com testes em cada passo. */
export default function ProjetoScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const P = projetoPorId(String(id));
  const salvo = useGame((s) => s.projetos?.[String(id)]);
  const done = useGame((s) => s.done);
  const [passo, setPasso] = useState(Math.min(salvo?.passo ?? 0, (P?.passos.length ?? 1) - 1));
  const [codigo, setCodigo] = useState(salvo?.codigo ?? P?.passos[passo]?.starter ?? '');
  const [res, setRes] = useState<{ ok: boolean; texto: string } | null>(null);
  const [rodando, setRodando] = useState(false);
  const [dica, setDica] = useState(false);
  const [falhas, setFalhas] = useState(0);
  const [verSolucao, setVerSolucao] = useState(false);
  const [fim, setFim] = useState<{ xpAntes: number } | null>(null);
  const [compMsg, setCompMsg] = useState('');
  const scroll = useRef<ScrollView>(null);

  if (!P) {
    return (
      <View style={[styles.center, { backgroundColor: t.bg }]}>
        <Text style={[styles.h1, { color: t.ink }]}>Projeto não encontrado</Text>
        <Button3D label="Voltar" onPress={() => router.back()} />
      </View>
    );
  }
  const liberado = P.requer in done;
  const p = P.passos[passo];
  const ultimo = passo === P.passos.length - 1;
  const terminado = !!salvo?.feito;

  const guardar = (np: number, cod: string, feito = terminado) => useGame.getState().salvarProjeto(P.id, { passo: np, codigo: cod, feito });

  const jogar = (cod: string) => {
    usePlayground.getState().openExample(`projeto_${P.id}`, cod.trimEnd(), P.entrada);
    router.navigate('/codigo');
  };

  /** Cartão de texto do projeto (nome, código e o que o programa escreve) para colar numa conversa ou rede. */
  const compartilhar = async (cod: string) => {
    setCompMsg('Preparando seu cartão…');
    let saida = '';
    try {
      const r = await runProject({ 'main.py': cod }, 'main.py', P.entrada ?? '', 1);
      saida = (r.ok ? r.stdout : r.error ?? '').trim().slice(0, 600);
    } catch { /* sem saída: compartilha só o código */ }
    const texto = `Fiz o projeto “${P.titulo}” no PyPasso!\n\nCódigo:\n${cod.trim()}\n${saida ? `\nSaída:\n${saida}\n` : ''}`;
    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && typeof window !== 'undefined') await navigator.clipboard.writeText(texto);
      else await Share.share({ message: texto });
      setCompMsg('Cartão copiado. Cole onde quiser compartilhar.');
    } catch { setCompMsg('Não consegui copiar aqui.'); }
  };

  const verificar = async () => {
    setRodando(true); setRes(null);
    const r = await runPython(codigo, p.tests, 'projeto');
    setRodando(false);
    guardar(passo, codigo);
    if (!r.ok) {
      setFalhas((f) => f + 1);
      setRes({ ok: false, texto: r.error ?? 'Um dos testes falhou.' });
      return;
    }
    setRes({ ok: true, texto: ultimo ? 'Tudo certo! Seu programa está pronto.' : 'Passou em todos os testes!' });
    const g = useGame.getState();
    const jaFeito = terminado; // refazendo: sem XP de novo
    if (!jaFeito) {
      g.completeLesson(null, XP_PASSO, 100);
      g.ganharMoedas(MOEDAS.passo);
      g.registrar('passos');
    }
    if (ultimo && !jaFeito) {
      const xpAntes = useGame.getState().xp;
      g.completeLesson(null, XP_FINAL, 100);
      g.ganharMoedas(MOEDAS.projeto);
      g.registrar('projetos');
      guardar(passo, codigo, true);
      setFim({ xpAntes });
    }
    setTimeout(() => scroll.current?.scrollToEnd({ animated: true }), 50);
  };

  const proximo = () => {
    if (ultimo) { setFim({ xpAntes: useGame.getState().xp }); return; }
    const np = passo + 1;
    const cod = P.passos[np].starter;
    setPasso(np); setCodigo(cod); setRes(null); setDica(false); setFalhas(0); setVerSolucao(false);
    guardar(np, cod);
    scroll.current?.scrollTo({ y: 0, animated: false });
  };

  const head = (
    <View style={[styles.head, { paddingTop: insets.top + 10 }]}>
      <Pressable onPress={() => { guardar(passo, codigo); router.back(); }} accessibilityLabel="Sair do projeto" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
      <View style={styles.segs}>
        {P.passos.map((_, i) => (
          <View key={i} style={[styles.seg, { backgroundColor: i < passo || terminado ? t.good : i === passo ? t.brand : t.line }]} />
        ))}
      </View>
      <Icone nome={ICONE_PROJ[P.id] ?? 'martelo'} size={24} color={t.brand} />
    </View>
  );

  if (!liberado) {
    const l = lessonById(P.requer);
    return (
      <View style={{ flex: 1, backgroundColor: t.bg }}>
        {head}
        <View style={styles.center}>
          <Mascot size={110} mood="think" />
          <Text style={[styles.h1, { color: t.ink }]}>{P.titulo}</Text>
          <Text style={[styles.sub, { color: t.muted }]}>Este projeto libera quando você terminar a lição "{l?.title ?? P.requer}" da trilha Python do zero. Ele usa o que você aprende até lá.</Text>
          <Button3D label="Voltar" style={styles.wide} onPress={() => router.back()} />
        </View>
      </View>
    );
  }

  if (fim) {
    const final = salvo?.codigo ?? codigo;
    return (
      <ScrollView style={{ backgroundColor: t.bg }} contentContainerStyle={[styles.center, { paddingTop: insets.top + 30, paddingBottom: insets.bottom + 30 }]}>
        <Celebration c={{ pose: 'festa', titulo: 'PROJETO PRONTO!', frase: `Você construiu "${P.titulo}" do zero. Isso é programar de verdade!`, confete: true }} />
        <View style={[styles.premio, { borderColor: t.sun, backgroundColor: t.surface }]}>
          <Moeda size={26} /><Text style={{ color: t.ink, fontWeight: '900', fontSize: 17 }}>+{MOEDAS.projeto} moedas · +{XP_FINAL} XP</Text>
        </View>
        <NivelBar xp={useGame.getState().xp} antes={fim.xpAntes} />
        <Button3D label="Jogar no editor" style={styles.wide} onPress={() => jogar(final)} />
        <Button3D label="Compartilhar meu projeto" variant="sun" style={styles.wide} onPress={() => compartilhar(final)} />
        {!!compMsg && <Text style={{ color: t.good, fontWeight: '800', textAlign: 'center' }} accessibilityLiveRegion="polite">{compMsg}</Text>}
        <Button3D label="Voltar aos projetos" variant="ghost" style={styles.wide} onPress={() => router.back()} />
      </ScrollView>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      {head}
      <ScrollView ref={scroll} contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled">
        <Text style={[styles.eyebrow, { color: t.brand }]}>{P.titulo.toUpperCase()} · PASSO {passo + 1} DE {P.passos.length}</Text>
        <Text style={[styles.h1, { color: t.ink, textAlign: 'left' }]}>{p.titulo}</Text>
        <View style={styles.pipoRow}>
          <Mascot size={58} mood={res ? (res.ok ? 'cheer' : 'sad') : 'happy'} />
          <View style={[styles.balao, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={[styles.texto, { color: t.ink }]}>{p.explica}</Text>
          </View>
        </View>
        <View style={[styles.tarefa, { borderColor: t.brand, backgroundColor: t.surface }]}>
          <Text style={[styles.cap, { color: t.brand }]}>SUA TAREFA</Text>
          <Text style={[styles.texto, { color: t.ink }]}>{p.tarefa}</Text>
        </View>

        <TextInput value={codigo} onChangeText={(v) => { setCodigo(v); setRes(null); }} multiline autoCapitalize="none" autoCorrect={false} spellCheck={false}
          accessibilityLabel="Editor de código do projeto"
          style={[styles.editor, { backgroundColor: t.codeBg, color: t.codeFg, fontFamily: mono }]} />
        <View style={styles.acoes}>
          <Pressable onPress={() => setDica((d) => !d)} style={[styles.chip, { borderColor: t.sunDeep }]} accessibilityRole="button">
            <Icone nome="lampada" size={15} color={t.sunDeep} /><Text style={{ color: t.sunDeep, fontWeight: '800' }}>{dica ? 'Esconder dica' : 'Dica'}</Text>
          </Pressable>
          <Pressable onPress={() => { setCodigo(p.starter); setRes(null); }} style={[styles.chip, { borderColor: t.line }]} accessibilityRole="button">
            <Icone nome="desfazer" size={15} color={t.muted} /><Text style={{ color: t.muted, fontWeight: '800' }}>Recomeçar passo</Text>
          </Pressable>
          {falhas >= 2 && (
            <Pressable onPress={() => setVerSolucao((v) => !v)} style={[styles.chip, { borderColor: t.line }]} accessibilityRole="button">
              <Icone nome="olho" size={15} color={t.muted} /><Text style={{ color: t.muted, fontWeight: '800' }}>{verSolucao ? 'Esconder solução' : 'Ver solução'}</Text>
            </Pressable>
          )}
        </View>
        {dica && <Text style={[styles.dica, { color: t.ink, backgroundColor: t.surface, borderColor: t.sun }]}>{p.dica}</Text>}
        {verSolucao && (
          <View style={{ gap: 8 }}>
            <Text style={[styles.cap, { color: t.muted }]}>UMA SOLUÇÃO POSSÍVEL</Text>
            <CodeBlock code={p.solucao} />
            <Button3D label="Usar esta solução" variant="ghost" onPress={() => { setCodigo(p.solucao); setVerSolucao(false); }} />
          </View>
        )}
        {res && (
          <View style={[styles.res, { backgroundColor: res.ok ? t.goodBg : t.badBg }]} accessibilityLiveRegion="polite">
            <Text style={{ color: res.ok ? t.goodInk : t.badInk, fontWeight: '900', fontSize: 17 }}>{res.ok ? res.texto : 'Ainda não'}</Text>
            {!res.ok && <Text style={{ color: t.badInk, fontFamily: mono, fontSize: 13 }}>{res.texto}</Text>}
            {res.ok && !terminado && <Text style={{ color: t.goodInk, fontWeight: '700' }}>+{XP_PASSO} XP · +{MOEDAS.passo} moedas</Text>}
          </View>
        )}
      </ScrollView>
      <View style={[styles.foot, { borderTopColor: t.line, paddingBottom: insets.bottom + 14 }]}>
        {res?.ok
          ? <Button3D style={styles.footBtn} variant="good" label={ultimo ? 'Ver meu programa pronto' : 'Próximo passo'} onPress={proximo} />
          : <Button3D style={styles.footBtn} label={rodando ? 'Rodando os testes…' : 'Verificar'} disabled={rodando || !codigo.trim()} onPress={verificar} />}
        {terminado && <Button3D style={styles.footBtn} variant="ghost" label="Jogar no editor" onPress={() => jogar(salvo?.codigo ?? codigo)} />}
        {terminado && <Button3D style={styles.footBtn} variant="sun" label={compMsg || 'Compartilhar meu projeto'} onPress={() => compartilhar(salvo?.codigo ?? codigo)} />}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 12, paddingHorizontal: 16, paddingBottom: 10, maxWidth: 760, width: '100%', alignSelf: 'center' },
  segs: { flex: 1, flexDirection: 'row', gap: 5 },
  seg: { flex: 1, height: 12, borderRadius: 99 },
  body: { padding: 16, paddingBottom: 40, gap: 14, maxWidth: 680, width: '100%', alignSelf: 'center' },
  eyebrow: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  h1: { fontSize: 26, fontWeight: '900', textAlign: 'center' },
  sub: { fontSize: 16, fontWeight: '700', textAlign: 'center', maxWidth: 380 },
  pipoRow: { flexDirection: 'row', gap: 10, alignItems: 'flex-start' },
  balao: { flex: 1, borderWidth: 2, borderRadius: 16, padding: 12 },
  texto: { fontSize: 16, lineHeight: 23, fontWeight: '600' },
  tarefa: { borderWidth: 2, borderRadius: 16, padding: 12, gap: 4 },
  cap: { fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  editor: { minHeight: 260, borderRadius: 14, padding: 14, fontSize: 14, lineHeight: 21, textAlignVertical: 'top' },
  acoes: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: { flexDirection: 'row', alignItems: 'center', gap: 5, borderWidth: 2, borderRadius: 12, paddingVertical: 7, paddingHorizontal: 12 },
  dica: { borderWidth: 2, borderRadius: 14, padding: 12, fontWeight: '700', fontSize: 15, lineHeight: 21 },
  res: { borderRadius: 14, padding: 14, gap: 6 },
  foot: { borderTopWidth: 2, paddingHorizontal: 16, paddingTop: 14, gap: 10 },
  footBtn: { width: '100%', maxWidth: 680, alignSelf: 'center' },
  center: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', gap: 18, padding: 24 },
  premio: { flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 14, paddingVertical: 8, paddingHorizontal: 14 },
  wide: { width: '100%', maxWidth: 440 },
});
