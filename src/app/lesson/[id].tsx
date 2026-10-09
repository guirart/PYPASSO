import { CoracaoPixel } from '@/components/crimson';
import * as Haptics from 'expo-haptics';
import { router, useLocalSearchParams } from 'expo-router';
import { useMemo, useRef, useState } from 'react';
import { Platform, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { Celebration } from '@/components/Celebration';
import { VooBiblioteca, type VooRef } from '@/components/VooBiblioteca';
import { conceitosDoCartao } from '@/content/conceitos';
import { libById } from '@/content/library';
import { escolherComemoracao, type Comemoracao } from '@/lib/comemoracao';
import { ExerciseView } from '@/components/ExerciseView';
import { PipoPanel } from '@/components/PipoPanel';
import { reviewLocal, type Review } from '@/lib/assistant';
import { Check, Cross, Flag } from '@/components/Icons';
import { BauDeDrop } from '@/components/BauDeDrop';
import type { ModeloBau } from '@/lib/baus';
import { armaVestida, type ItemInst } from '@/lib/itens';
import { Moeda } from '@/components/Moeda';
import { NivelBar } from '@/components/NivelBar';
import { RelatoModal } from '@/components/RelatoModal';
import { BONUS_FRAQUEZA, danoDoGolpe, FRAQUEZA_INIMIGO, NOME_ARMA, vidaDoInimigo, type EstiloArma } from '@/lib/batalha';
import { MOEDAS, nivelDe } from '@/lib/gamificacao';
import { inimigoDoNo, sortearReliquia } from '@/lib/mapa';
import { ENEMIES } from '@/components/enemy-art';
import { InimigoBarra } from '@/components/mapa/InimigoBarra';
import { CartaoReliquia } from '@/components/mapa/NoSheet';
import { filaDeRevisao } from '@/lib/revisao';
import { useTeste } from '@/lib/teste';
import { agendarLembretes } from '@/lib/lembretes';
import { LESSONS, exercicioPorId, lessonById } from '@/content';
import { exercicioDoDesafio } from '@/lib/desafio';
import { compararExplicacao, type Comparacao } from '@/lib/explicar';
import type { Exercise, LearnEx } from '@/content/types';
import { grade, initAnswer, isReady, shuffle, type Answer, type Verdict } from '@/lib/grade';
import { usePlus } from '@/lib/plus';
import { dayKey, useGame } from '@/lib/store';
import { pushLessonResult } from '@/lib/sync';
import { mono, useTheme } from '@/lib/theme';
import { Icone } from '@/components/Icone';

/** Exercícios em que a pessoa escreve ou monta o código (e não só reconhece) acertam o inimigo em cheio: dano 2. */
const pesoDe = (e: Exercise) => (e.k === 'fill' || e.k === 'type' || e.k === 'code' || e.k === 'order' ? 2 : 1);
const PRAISE = ['Muito bem!', 'Isso aí!', 'Perfeito!', 'Mandou bem!', 'Excelente!'];
const buzz = (ok: boolean) => {
  if (Platform.OS === 'web') return;
  Haptics.notificationAsync(ok ? Haptics.NotificationFeedbackType.Success : Haptics.NotificationFeedbackType.Error).catch(() => {});
};

type Phase = 'play' | 'done' | 'out';

export default function LessonScreen() {
  const { id, zona, no, modo } = useLocalSearchParams<{ id: string; zona?: string; no?: string; modo?: string }>();
  const elite = modo === 'elite';
  // Relíquias da expedição desta zona (src/lib/mapa.ts)
  const reliquias = (zona && useGame.getState().rotas?.[zona]?.reliquias) || [];
  const pato = reliquias.includes('pato');
  const cafe = reliquias.includes('cafe');
  const patoUsado = useRef(false);
  const protegidos = useRef(0); // erros já perdoados pela habilidade Guarda do equipamento
  const sequencia = useRef(0); // acertos seguidos (para a Vitalidade e a passiva do arco)
  const atordoado = useRef(false); // maça: o próximo erro é perdoado
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const game = useGame();
  const plusOn = usePlus((s) => s.ativo);
  const revisao = id === 'revisao';
  const desafio = id === 'desafio'; // Desafio do dia: um exercício de código, sem custo de vidas
  const practice = id === 'pratica' || revisao || desafio; // treino e revisão: não custam vidas
  const lesson = practice ? null : lessonById(id);

  const initialQueue = useMemo<Exercise[]>(() => {
    if (revisao) return filaDeRevisao(game.revisao);
    if (desafio) {
      const d = game.desafio;
      const hoje = d?.dia === dayKey() && d.exId ? exercicioPorId(d.exId)?.ex : undefined;
      const ex = hoje ?? exercicioDoDesafio(game.done, d?.feitos ?? [], dayKey(), game.semente);
      return ex ? [ex] : [];
    }
    if (practice) return shuffle(LESSONS.filter((l) => l.id in game.done).flatMap((l) => l.exercises.filter((e) => e.k !== 'code' && e.k !== 'learn'))).slice(0, 6);
    return lesson?.exercises ?? [];
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const [queue, setQueue] = useState(initialQueue);
  const total = initialQueue.length;
  const [correct, setCorrect] = useState(0);
  const [mistakes, setMistakes] = useState(0);
  const [answer, setAnswer] = useState<Answer | null>(() => (initialQueue[0] ? initAnswer(initialQueue[0]) : null));
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [checking, setChecking] = useState(false);
  const [help, setHelp] = useState<Review | null>(null);
  const [phase, setPhase] = useState<Phase>('play');
  const [result, setResult] = useState<{ xp: number; acc: number; secs: number; festa: Comemoracao; moedas: number; xpAntes: number; dobro: boolean; serie?: number } | null>(null);
  const [combo, setCombo] = useState(0);
  const maxCombo = useRef(0);
  const errosPorEx = useRef<Record<string, number>>({});
  const jaRespondeu = useRef<Set<string>>(new Set());
  const tEx = useRef(Date.now());
  const [relato, setRelato] = useState(false);
  const [relGanha, setRelGanha] = useState<string | null>(null);
  const [bauGanho, setBauGanho] = useState<{ item: ItemInst; bau: ModeloBau } | null>(null); // baú que a elite deixou cair
  const teste = useTeste();
  const t0 = useRef(Date.now());
  const voo = useRef<VooRef>(null);
  const [novosNaLicao, setNovosNaLicao] = useState<string[]>([]);
  const redo = !!lesson && lesson.id in game.done;
  // Batalha do mapa: um inimigo perde vida a cada exercício certo e ataca a cada erro.
  const batalha = !!(zona && no) && !practice;
  const inimigo = batalha ? inimigoDoNo(no as string) : null;
  const [golpe, setGolpe] = useState(0);
  const [ataque, setAtaque] = useState(0);
  const [acertos, setAcertos] = useState(0); // dano já causado ao inimigo (exercícios de completar valem 2)
  const [critico, setCritico] = useState(false);
  const [ultimoDano, setUltimoDano] = useState<{ n: number; fraco: boolean } | null>(null); // dano do último acerto (aparece em cima do inimigo)
  const nivelHeroi = useRef(nivelDe(useGame.getState().xp).nivel).current; // a vida do inimigo acompanha o nível do herói (fixo durante a lição)
  const zonaN = zona ? parseInt(zona.replace(/\D/g, ''), 10) || 0 : 0;
  const [dicas, setDicas] = useState<Record<string, string[]>>({}); // dicas do Pipo já pedidas, por exercício
  const dicasUsadas = useRef(0);
  const [expl, setExpl] = useState('');
  const [explRes, setExplRes] = useState<Comparacao | null>(null);
  const [explBonus, setExplBonus] = useState(false);  const ex = queue[0];
  const unidades = initialQueue.filter((e) => e.k !== 'learn').reduce((s, e) => s + pesoDe(e), 0) || 1; // exercícios de completar valem 2
  const vidaMax = vidaDoInimigo(unidades, nivelHeroi, zonaN, elite);

  if (!total || !ex && phase === 'play') {
    return (
      <View style={[styles.center, { backgroundColor: t.bg }]}>
        <Text style={[styles.h2, { color: t.ink }]}>Lição não encontrada</Text>
        <Button3D label="Voltar" onPress={() => router.back()} />
      </View>
    );
  }

  /** Cartão de conceito: só avança, sem correção nem perda de vida. */
  const learnNext = () => {
    // Conceito aprendido: vai voando para a Biblioteca (só o que ainda não estava lá).
    const novos = game.aprender(conceitosDoCartao(ex.id));
    if (novos.length) {
      voo.current?.voar({ titulo: ex.q, nomes: novos.map((id) => libById(id)?.nome ?? id), ...(ex.k === 'learn' ? { corpo: ex.body, codigo: ex.c, saida: ex.out } : {}) });
      setNovosNaLicao((n) => [...n, ...novos]);
    }
    const rest = queue.slice(1);
    setCorrect((c) => c + 1);
    if (!rest.length) { finish(); return; }
    setQueue(rest);
    setAnswer(initAnswer(rest[0]));
  };

  const check = async () => {
    if (!answer || !isReady(answer) || verdict || checking) return;
    setChecking(true);
    const v = await grade(ex, answer);
    if (!v.ok && answer.k === 'code' && v.detail && /Error|Traceback/.test(v.detail)) {
      // O Pipo explica o erro (sem entregar a resposta do exercício)
      const r = await reviewLocal({ files: { 'seu_codigo.py': answer.text }, entry: 'seu_codigo.py', error: v.detail }).catch(() => null);
      if (r?.problemas.length) setHelp(r);
    }
    setChecking(false);
    setVerdict(v);
    buzz(v.ok);
    teste.tentativa(ex.id, v.ok, Date.now() - tEx.current);
    // Revisão espaçada: só a 1ª resposta de cada exercício nesta sessão conta.
    const primeira = !jaRespondeu.current.has(ex.id);
    jaRespondeu.current.add(ex.id);
    if (revisao && primeira) game.revisou(ex.id, v.ok);
    if (v.ok) {
      // Efeitos do equipamento: habilidades das peças e a passiva de cada arma
      const st = useGame.getState();
      const bn = st.bonus();
      const arma = armaVestida(st.inv, st.equip);
      const critExtra = Math.random() * 100 < bn.crit; // Precisão (e a passiva da espada)
      const ehCritico = pesoDe(ex) > 1 || critExtra;
      sequencia.current += 1;
      // O dano é um multiplicador do dano do nível do herói; nenhum golpe tira mais de 34% da vida do inimigo
      const fraco = !!inimigo && FRAQUEZA_INIMIGO[inimigo] === arma; // ponto fraco: o inimigo apanha mais dessa arma
      let mult = 1 + (critExtra ? 0.5 : 0);
      if (ehCritico && arma === 'ax01') mult += 0.25; // machado: críticos pesam mais
      if (arma === 'arco' && sequencia.current >= 3) mult += 0.25; // arco: a partir de 3 acertos seguidos
      if (fraco) mult += BONUS_FRAQUEZA;
      const dano = danoDoGolpe({ unidades: pesoDe(ex), nivel: nivelHeroi, mult, vidaMax });
      setUltimoDano({ n: dano, fraco });
      if (arma === 'mc01' && Math.random() < 0.2) atordoado.current = true; // maça: 20% de atordoar
      if (bn.vida && sequencia.current % bn.vida === 0) game.gainHeart(); // Vitalidade: cura a cada N acertos seguidos
      setGolpe((x) => x + 1); setAcertos((a) => a + dano); setCritico(ehCritico);
      setCorrect((c) => c + 1);
      setCombo((c) => { const n = c + 1; maxCombo.current = Math.max(maxCombo.current, n); return n; });
    } else {
      setAtaque((x) => x + 1);
      sequencia.current = 0;
      setMistakes((m) => m + 1);
      setCombo(0);
      errosPorEx.current[ex.id] = (errosPorEx.current[ex.id] ?? 0) + 1;
      if (!revisao) game.errouExercicio(ex.id); // volta numa Revisão amanhã
      if (!practice) {
        if (pato && !patoUsado.current) patoUsado.current = true; // o pato de borracha segura o 1º erro
        else if (atordoado.current) atordoado.current = false; // maça: o erro foi perdoado
        else if (protegidos.current < useGame.getState().bonus().protecao) protegidos.current += 1; // habilidade Guarda
        else { game.loseHeart(); if (elite) game.loseHeart(); }
      }
    }
  };

  /** Dica do Pipo (só nos exercícios de código): a 1ª ensina um jeito de pensar, a 2ª olha o seu código, a 3ª mostra a explicação. Cada uma custa 2 XP. */
  const pedirDica = async () => {
    if (!ex || ex.k !== 'code' || verdict) return;
    const feitas = dicas[ex.id] ?? [];
    if (feitas.length >= 3) return;
    let texto: string;
    if (feitas.length === 0) texto = 'Rode seu código com RODAR e compare a saída com o que o enunciado pede. Confira letras, espaços e pontuação.';
    else if (feitas.length === 1) {
      const r = answer?.k === 'code' ? await reviewLocal({ files: { 'seu_codigo.py': answer.text }, entry: 'seu_codigo.py', error: '' }).catch(() => null) : null;
      const p = r?.problemas[0] ?? r?.dicas[0];
      texto = p ? `O Pipo olhou seu código: ${p.titulo}. ${p.explicacao}` : 'O Pipo olhou seu código e não viu erro de sintaxe. Se não deu certo, o problema está na lógica ou no texto exato da saída.';
    } else texto = `Explicação da resposta: ${ex.e}`;
    dicasUsadas.current += 1;
    setDicas((d) => ({ ...d, [ex.id]: [...(d[ex.id] ?? []), texto] }));
  };

  const next = () => {
    const rest = queue.slice(1);
    const newQueue = verdict?.ok ? rest : [...rest, ex];
    setVerdict(null);
    setHelp(null);
    if (!practice && !usePlus.getState().ativo && useGame.getState().hearts <= 0) { setPhase('out'); return; }
    if (!newQueue.length) { finish(); return; }
    setQueue(newQueue);
    setAnswer(initAnswer(newQueue[0]));
    tEx.current = Date.now();
  };

  /** Sair no meio: conta como abandono no relatório de teste (se já respondeu algo). */
  const sair = () => {
    if (jaRespondeu.current.size && phase === 'play') teste.fimDeLicao(id, Math.round((Date.now() - t0.current) / 1000), errosPorEx.current, true);
    router.back();
  };

  const finish = () => {
    const primeiraVez = desafio && !(game.desafio?.feito && game.desafio?.dia === dayKey());
    const secs = Math.round((Date.now() - t0.current) / 1000);
    const graded = initialQueue.filter((e) => e.k !== 'learn').length || 1;
    const acc = Math.round((graded / (graded + mistakes)) * 100);
    let xpBase: number;
    if (revisao) xpBase = 10;
    else if (desafio) xpBase = primeiraVez ? 15 + (mistakes === 0 ? 5 : 0) : 0;
    else if (practice) { xpBase = 5; game.gainHeart(); }
    else xpBase = (redo ? 5 : 10) + (mistakes === 0 ? 5 : 0);
    if (zona && no) xpBase = Math.round(xpBase * (elite ? 1.5 : 1)) + (cafe ? 5 : 0);
    const bn = game.bonus();
    const dicasPagas = Math.max(0, dicasUsadas.current - bn.dica); // habilidade Pipo: as primeiras dicas saem de graça
    if (xpBase > 0 && dicasPagas) xpBase = Math.max(1, xpBase - 2 * dicasPagas); // cada dica custa 2 XP
    if (xpBase > 0 && bn.xp) xpBase = Math.max(xpBase + 1, Math.round(xpBase * (1 + bn.xp / 100))); // habilidade Sabedoria
    const xpAntes = game.xp;
    const xp = game.completeLesson(lesson?.id ?? null, xpBase, acc);
    pushLessonResult(lesson?.id ?? null, xp, acc).catch(() => {});
    // Moedas, missões e conquistas
    const moedasBase = (revisao ? MOEDAS.revisao : desafio ? (primeiraVez ? 20 + (mistakes === 0 ? 10 : 0) : 0) : practice ? 0 : MOEDAS.licao + (mistakes === 0 ? MOEDAS.perfeita : 0)) * (elite ? 3 : 1);
    const moedas = moedasBase && bn.moedas ? Math.max(moedasBase + 1, Math.round(moedasBase * (1 + bn.moedas / 100))) : moedasBase; // habilidade Fortuna
    // Mapa: chegou no nó. Elite vencida dá uma relíquia.
    let relNova: string | null = null;
    let bauNovo: { item: ItemInst; bau: ModeloBau } | null = null;
    if (zona && no) {
      const jaTinha = useGame.getState().rotas?.[zona]?.visitados.includes(no);
      game.visitar(zona, no);
      if (elite && !jaTinha) {
        relNova = sortearReliquia(reliquias, `${no}e`); if (relNova) game.ganharReliquia(zona, relNova);
        if (Math.random() < 0.6) bauNovo = game.soltarItem(parseInt(zona.replace(/\D/g, ''), 10) || 0, 'normal'); // a elite deixa um baú normal da zona
      }
    }
    const serie = primeiraVez ? game.concluirDesafio() : 0;
    if (moedas) game.ganharMoedas(moedas);
    if (maxCombo.current) game.registrar('combo', maxCombo.current);
    if (revisao) game.registrar('revisoes');
    else if (!practice) { game.registrar('licoes'); if (mistakes === 0) game.registrar('perfeitas'); }
    teste.fimDeLicao(id, secs, errosPorEx.current, false);
    agendarLembretes();
    setRelGanha(relNova);
    setBauGanho(bauNovo);
    setResult({ xp, acc, secs, moedas, serie, xpAntes, dobro: xp > xpBase, festa: escolherComemoracao({ erros: mistakes, segundos: secs, exercicios: graded, pratica: practice && !revisao && !desafio }) });
    setPhase('done');
  };

  const cartaoConceito = lesson ? ([...lesson.exercises].reverse().find((e) => e.k === 'learn') as LearnEx | undefined) : undefined;
  if (phase === 'done' && result) {
    return (
      // rola quando o conteúdo passa da tela (ex.: com o cartão "Explique com suas palavras"), senão o botão Continuar some
      <ScrollView style={{ flex: 1, backgroundColor: t.bg }} contentContainerStyle={[styles.centerRola, { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 28 }]}>
        <Celebration c={result.festa} />
        <Text style={[styles.sub, { color: t.muted }]}>
          {revisao ? (mistakes === 0 ? 'Revisão perfeita! Esses exercícios vão voltar daqui a mais dias.' : 'Revisão feita. Os que você errou voltam amanhã.') : desafio ? (result.serie ? (mistakes === 0 ? 'Resolvido de primeira: +5 XP e +10 moedas de bônus.' : 'Desafio do dia resolvido!') : 'Você já tinha resolvido o desafio de hoje. Volte amanhã para um novo.') : practice ? 'Treino concluído.' : mistakes === 0 ? 'Lição concluída sem nenhum erro: +5 XP de bônus.' : `Lição concluída. ${mistakes} ${mistakes === 1 ? 'erro corrigido' : 'erros corrigidos'} pelo caminho.`}
        </Text>
        <View style={styles.tiles}>
          <StatTile label={result.dobro ? 'XP x2' : 'XP GANHO'} value={`+${result.xp}`} color={t.sun} ink={t.sunInk} />
          <StatTile label="PRECISÃO" value={`${result.acc}%`} color={t.good} ink="#fff" />
          <StatTile label="TEMPO" value={`${Math.floor(result.secs / 60)}:${String(result.secs % 60).padStart(2, '0')}`} color={t.brand} ink="#fff" />
        </View>
        {result.moedas > 0 && (
          <View style={[styles.moedas, { borderColor: t.sun, backgroundColor: t.surface }]} accessibilityLabel={`Mais ${result.moedas} moedas`}>
            <Moeda size={26} /><Text style={{ color: t.ink, fontWeight: '900', fontSize: 17 }}>+{result.moedas} moedas</Text>
          </View>
        )}
        <NivelBar xp={game.xp} antes={result.xpAntes} />
        {desafio && !!result.serie && (
          <View style={[styles.moedas, { borderColor: t.sunDeep, backgroundColor: t.surface }]} accessibilityLabel={`${result.serie} dias seguidos de desafio`}>
            <Icone nome="chama" size={26} color={t.sunDeep} />
            <Text style={{ color: t.ink, fontWeight: '900', fontSize: 17 }}>{result.serie} {result.serie === 1 ? 'dia' : 'dias'} seguidos de desafio</Text>
          </View>
        )}
        {inimigo && <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>{ENEMIES[inimigo].nome} derrotado!</Text>}
        {relGanha && <View style={{ width: '100%', maxWidth: 440, gap: 6 }}><Text style={{ color: t.sunDeep, fontWeight: '900', textAlign: 'center' }}>ELITE VENCIDA: NOVA RELÍQUIA</Text><CartaoReliquia id={relGanha} /></View>}
        {bauGanho && <BauDeDrop drop={bauGanho} quem="A ELITE" rotulo="Abrir o baú da elite" />}
        {novosNaLicao.length > 0 && (
          <Pressable onPress={() => router.replace('/biblioteca')} accessibilityRole="button" style={[styles.bibNovos, { borderColor: t.sun, backgroundColor: t.surface }]}>
            <Icone nome="livros" size={24} color={t.sunDeep} />
            <Text style={{ color: t.ink, fontWeight: '800', flex: 1 }}>
              {novosNaLicao.length === 1 ? '1 conceito novo' : `${novosNaLicao.length} conceitos novos`} na sua Biblioteca: {novosNaLicao.map((id) => libById(id)?.nome ?? id).join(', ')}
            </Text>
            <Text style={{ color: t.sunDeep, fontWeight: '900' }}>Ver ›</Text>
          </Pressable>
        )}
        {lesson && !practice && cartaoConceito && (explBonus || !game.explicacoes?.[lesson.id]) && (
          <View style={[styles.explica, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>Explique com suas palavras</Text>
            <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>Como você explicaria “{cartaoConceito.q}” para um amigo? Vale +5 XP.</Text>
            <TextInput value={expl} onChangeText={setExpl} multiline placeholder="Escreva aqui…" placeholderTextColor={t.muted} accessibilityLabel="Sua explicação"
              style={[styles.explicaInput, { borderColor: t.line, backgroundColor: t.bg, color: t.ink }]} />
            <Button3D label="Conferir" disabled={expl.trim().length < 3}
              onPress={() => { const r = compararExplicacao(expl, cartaoConceito.q, cartaoConceito.body); setExplRes(r); if (r.ok && game.bonusExplicacao(lesson.id)) setExplBonus(true); }} />
            {explRes && (
              <Text style={{ color: explRes.ok ? t.good : t.muted, fontWeight: '800', lineHeight: 20 }} accessibilityLiveRegion="polite">
                {explRes.curto ? 'Escreva um pouco mais: pelo menos uma frase.'
                  : explRes.ok ? `Boa! Você falou de: ${explRes.citadas.join(', ')}.${explBonus ? ' +5 XP!' : ''}`
                  : `Você falou de: ${explRes.citadas.join(', ') || 'nada ainda'}. Faltou falar de: ${explRes.faltaram.slice(0, 3).join(', ')}. Tente de novo ou continue.`}
              </Text>
            )}
          </View>
        )}
        <Button3D label="Continuar" style={styles.wide} onPress={() => router.back()} />
      </ScrollView>
    );
  }

  if (phase === 'out') {
    const anyDone = Object.keys(game.done).length > 0;
    return (
      <View style={[styles.center, { backgroundColor: t.bg }]}>
        <Mascot size={130} mood="sad" />
        <Text style={[styles.h2, { color: t.ink }]}>Suas vidas acabaram</Text>
        <Text style={[styles.sub, { color: t.muted }]}>
          Cada vida volta em 30 minutos. {anyDone ? 'Um treino rápido devolve uma vida agora.' : 'Como você ainda não concluiu nenhuma lição, pode recarregar e tentar de novo.'}
        </Text>
        {anyDone
          ? <Button3D label="Treino rápido (+1 vida)" style={styles.wide} onPress={() => router.replace('/lesson/pratica')} />
          : <Button3D label="Recarregar vidas" style={styles.wide} onPress={() => { game.refillHearts(); router.back(); }} />}
        <Button3D label="Plus: vidas ilimitadas" variant="sun" style={styles.wide} onPress={() => router.push('/plus')} />
        <Button3D label="Voltar à trilha" variant="ghost" style={styles.wide} onPress={() => router.back()} />
      </View>
    );
  }

  const ready = !!answer && isReady(answer);
  const footBg = verdict ? (verdict.ok ? t.goodBg : t.badBg) : t.bg;
  const footInk = verdict ? (verdict.ok ? t.goodInk : t.badInk) : t.ink;

  return (
    <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
      <View style={styles.head}>
        <Pressable onPress={sair} accessibilityLabel="Sair da lição" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <View style={[styles.prog, { backgroundColor: t.line }]}>
          <View style={[styles.progFill, { backgroundColor: t.good, width: `${(correct / total) * 100}%` }]} />
        </View>
        {elite && <Text style={[styles.elite, { backgroundColor: t.bad }]}>ELITE</Text>}
        {desafio && <Text style={[styles.elite, { backgroundColor: t.brand }]}>DESAFIO DO DIA</Text>}
        {combo >= 3 && <Icone nome="chama" size={18} color={t.sunDeep} />}
        {combo >= 3 && <Text style={[styles.combo, { color: t.sunDeep }]} accessibilityLabel={`${combo} acertos seguidos`}>{combo}x</Text>}
        <Pressable onPress={() => setRelato(true)} accessibilityLabel="Travei aqui: relatar um problema" hitSlop={8}><Flag color={t.muted} size={22} /></Pressable>
        <View style={styles.hearts}><CoracaoPixel esc={2} /><Text style={{ color: t.bad, fontWeight: '800', fontSize: 16 }}>{practice || plusOn ? '∞' : game.hearts}</Text></View>
      </View>

      {inimigo && <InimigoBarra id={inimigo} elite={elite} hp={Math.max(0, vidaMax - acertos)} hpMax={vidaMax} golpe={golpe} ataque={ataque} critico={critico} dano={ultimoDano?.n} pontoFraco={ultimoDano?.fraco} fraqueza={FRAQUEZA_INIMIGO[inimigo] as EstiloArma} nomeFraqueza={NOME_ARMA[FRAQUEZA_INIMIGO[inimigo] as EstiloArma]} escondeu={!!ex && ex.k !== 'learn' && pesoDe(ex) > 1 && !verdict} />}
      <ScrollView contentContainerStyle={styles.body} keyboardShouldPersistTaps="handled">
        {answer && <ExerciseView key={`${ex.id}-${queue.length}`} ex={ex} answer={answer} onChange={setAnswer} locked={!!verdict} reaction={verdict ? (verdict.ok ? 'cheer' : 'sad') : undefined} />}
        {help && verdict && !verdict.ok && (
          <View style={{ marginTop: 16 }}>
            <PipoPanel compactMode review={help} original={answer?.k === 'code' ? answer.text : ''} colors={{
              bg: t.surface, card: t.bg, border: t.line, text: t.ink, dim: t.muted, accent: t.brand,
              good: t.good, bad: t.bad, warn: t.sunDeep, codeBg: t.codeBg, codeFg: t.codeFg,
            }} />
          </View>
        )}
        {ex.k === 'code' && !verdict && (
          <View style={{ marginTop: 14, gap: 8 }}>
            {(dicas[ex.id] ?? []).map((d, i) => (
              <View key={i} style={[styles.dica, { backgroundColor: t.surface, borderColor: t.sun }]}>
                <Icone nome="lampada" size={18} color={t.sunDeep} />
                <Text style={{ color: t.ink, fontWeight: '700', flex: 1, lineHeight: 20 }}>{d}</Text>
              </View>
            ))}
            {(dicas[ex.id] ?? []).length < 3 && (
              <Pressable onPress={pedirDica} accessibilityRole="button" style={[styles.dicaBtn, { borderColor: t.sunDeep }]}>
                <Icone nome="lampada" size={18} color={t.sunDeep} />
                <Text style={{ color: t.sunDeep, fontWeight: '900' }}>Pedir dica ao Pipo ({(dicas[ex.id] ?? []).length}/3) · {dicasUsadas.current < useGame.getState().bonus().dica ? 'grátis' : '-2 XP'}</Text>
              </Pressable>
            )}
          </View>
        )}
      </ScrollView>

      <View style={[styles.foot, { backgroundColor: footBg, borderTopColor: verdict ? 'transparent' : t.line, paddingBottom: insets.bottom + 16 }]}>
        {verdict && (
          <View style={styles.fb}>
            <View style={[styles.fbIcon, { backgroundColor: t.surface }]}>{verdict.ok ? <Check color={t.good} size={28} /> : <Cross color={t.bad} size={28} />}</View>
            <View style={{ flex: 1, gap: 2 }}>
              <Text style={[styles.fbTitle, { color: footInk }]}>{verdict.ok ? PRAISE[correct % PRAISE.length] : verdict.solution ? 'Resposta correta:' : 'Ainda não'}</Text>
              {!verdict.ok && verdict.solution && <Text style={{ color: footInk, fontFamily: mono, fontSize: 14 }}>{verdict.solution}</Text>}
              {!verdict.ok && verdict.detail && <Text style={{ color: footInk, fontWeight: '700' }}>{verdict.detail}</Text>}
              <Text style={{ color: footInk, fontWeight: '600' }}>{ex.e}</Text>
            </View>
          </View>
        )}
        {ex.k === 'learn' ? <Button3D style={styles.footBtn} label="Entendi, continuar" onPress={learnNext} /> : <Button3D
          style={styles.footBtn}
          label={verdict ? 'Continuar' : checking ? 'Verificando…' : 'Verificar'}
          variant={verdict ? (verdict.ok ? 'good' : 'bad') : 'brand'}
          disabled={!verdict && (!ready || checking)}
          onPress={verdict ? next : check}
        />}
      </View>
      <VooBiblioteca ref={voo} />
      <RelatoModal visivel={relato} fechar={() => setRelato(false)} exId={ex?.id} licao={id} />
    </View>
  );
}

function StatTile({ label, value, color, ink }: { label: string; value: string; color: string; ink: string }) {
  const t = useTheme();
  return (
    <View style={[styles.st, { borderColor: color, backgroundColor: t.surface }]}>
      <Text style={[styles.stH, { backgroundColor: color, color: ink }]}>{label}</Text>
      <Text style={[styles.stV, { color: t.ink }]}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  dica: { flexDirection: 'row', alignItems: 'flex-start', gap: 10, borderWidth: 2, borderRadius: 14, padding: 12 },
  dicaBtn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, borderWidth: 2, borderRadius: 14, paddingVertical: 10, borderStyle: 'dashed' },
  explica: { width: '100%', maxWidth: 440, gap: 8, borderWidth: 2, borderRadius: 16, padding: 14 },
  explicaInput: { minHeight: 84, borderWidth: 2, borderRadius: 12, padding: 10, fontSize: 15, textAlignVertical: 'top' },
  moedas: { flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 14, paddingVertical: 8, paddingHorizontal: 14 },
  elite: { color: '#fff', fontWeight: '900', fontSize: 11, letterSpacing: 1, borderRadius: 8, paddingHorizontal: 6, paddingVertical: 2, overflow: 'hidden' },
  combo: { fontWeight: '900', fontSize: 16, fontVariant: ['tabular-nums'] },
  bibNovos: { flexDirection: 'row', alignItems: 'center', gap: 10, borderWidth: 2, borderRadius: 14, padding: 12, width: '100%', maxWidth: 440 },
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingVertical: 12, maxWidth: 760, width: '100%', alignSelf: 'center' },
  prog: { flex: 1, height: 16, borderRadius: 99, overflow: 'hidden' },
  progFill: { height: '100%', borderRadius: 99 },
  hearts: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  body: { paddingHorizontal: 16, paddingVertical: 12, paddingBottom: 32, maxWidth: 640, width: '100%', alignSelf: 'center' },
  foot: { borderTopWidth: 2, paddingHorizontal: 16, paddingTop: 16, gap: 14 },
  fb: { flexDirection: 'row', gap: 12, alignItems: 'flex-start', maxWidth: 728, width: '100%', alignSelf: 'center' },
  fbIcon: { width: 48, height: 48, borderRadius: 24, alignItems: 'center', justifyContent: 'center' },
  fbTitle: { fontSize: 22, fontWeight: '900' },
  centerRola: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', gap: 18, paddingHorizontal: 24 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 18, padding: 24 },
  h2: { fontSize: 28, fontWeight: '900', textAlign: 'center' },
  sub: { fontSize: 16, fontWeight: '700', textAlign: 'center', maxWidth: 360 },
  tiles: { flexDirection: 'row', gap: 10, width: '100%', maxWidth: 440 },
  st: { flex: 1, borderWidth: 2, borderRadius: 14, overflow: 'hidden', alignItems: 'stretch' },
  stH: { textAlign: 'center', fontSize: 11, fontWeight: '900', letterSpacing: 0.8, paddingVertical: 4 },
  stV: { textAlign: 'center', fontSize: 22, fontWeight: '900', paddingVertical: 10, fontVariant: ['tabular-nums'] },
  wide: { width: '100%', maxWidth: 440 },
  footBtn: { width: '100%', maxWidth: 728, alignSelf: 'center' },
});
