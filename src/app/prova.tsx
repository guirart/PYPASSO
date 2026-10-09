import { BauDeDrop } from '@/components/BauDeDrop';
import type { ModeloBau } from '@/lib/baus';
import type { ItemInst } from '@/lib/itens';
import * as Haptics from 'expo-haptics';
import { router, useLocalSearchParams } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { highlight } from '@/components/CodeBlock';
import { Mascot } from '@/components/Characters';
import { Celebration } from '@/components/Celebration';
import { escolherComemoracao } from '@/lib/comemoracao';
import { Cross } from '@/components/Icons';
import { Icone } from '@/components/Icone';
import { ChefeArena, ChefeArte } from '@/components/mapa/ChefeArena';
import { CartaoReliquia } from '@/components/mapa/NoSheet';
import { chefeDaZona } from '@/lib/mapa';
import { rotaVazia } from '@/lib/store';
import { TRACKS } from '@/content';
import { BUGS, fireSecs, unitBugs, type Bug } from '@/content/provas';
import { shuffle } from '@/lib/grade';
import { useGame } from '@/lib/store';
import { danoNoBoss, FRAQUEZA_CHEFE, NOME_ARMA, vidaBoss, type EstiloArma } from '@/lib/batalha';
import { MOEDAS, nivelDe } from '@/lib/gamificacao';
import { armaVestida } from '@/lib/itens';
import { pushLessonResult } from '@/lib/sync';
import { mono, useTheme } from '@/lib/theme';

/**
 * Prova de fogo: ache a linha com o erro antes do tempo acabar.
 * O banco de bugs (src/content/provas.json) é gerado e conferido por tools/gerar_provas.py.
 */
/** Unidade (e seu número) pelo id, nas duas trilhas. */
const findUnit = (id?: string) => {
  for (const tr of TRACKS) {
    const i = tr.course.units.findIndex((u) => u.id === id);
    if (i >= 0) return { unit: tr.course.units[i], n: i + 1, track: tr };
  }
  return null;
};

const FIRE_LEVELS = [
  { n: 1, name: 'Faísca', secs: 20, desc: 'Dois-pontos, aspas, nomes e tipos', color: '#FFB020', deep: '#C27C00' },
  { n: 2, name: 'Chama', secs: 15, desc: 'Lógica e erros na hora de rodar', color: '#FF7A1A', deep: '#C2500A' },
  { n: 3, name: 'Inferno', secs: 10, desc: 'Bugs escondidos que enganam até quem programa', color: '#E5383B', deep: '#A11D20' },
];
const ROUND = 10;
const LIVES = 3;

type Phase = 'menu' | 'play' | 'conserte' | 'reveal' | 'end';

const buzz = (ok: boolean) => {
  if (Platform.OS === 'web') return;
  Haptics.notificationAsync(ok ? Haptics.NotificationFeedbackType.Success : Haptics.NotificationFeedbackType.Error).catch(() => {});
};

export default function ProvaDeFogo() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const game = useGame();
  // Com ?unit=…, é a prova que fecha aquela unidade (5 bugs do assunto dela).
  const { unit: unitId } = useLocalSearchParams<{ unit?: string }>();
  const unitInfo = findUnit(unitId);
  // Chefe da zona (mapa roguelite): cada acerto tira vida dele; relíquias da expedição ajudam.
  const chefe = unitInfo ? chefeDaZona(unitInfo.n - 1) : null;
  const rota = unitInfo ? game.rotas?.[unitInfo.unit.id] ?? rotaVazia() : rotaVazia();
  const temRel = (id: string) => rota.reliquias.includes(id);
  const unitLevel = unitInfo ? { n: 0, name: `Zona ${unitInfo.n}`, secs: fireSecs(unitInfo.unit.id) + (temRel('lupa') ? 5 : 0) + game.bonus().tempo /* habilidade Relógio */, desc: unitInfo.unit.title, color: '#D13F4A', deep: '#8E1520' } : null;
  // O chefe acompanha o nível do herói e a zona: a vida e o dano dos golpes crescem juntos, e nenhum golpe tira mais de 30%
  const nivelHeroi = useRef(nivelDe(game.xp).nivel).current; // fixo durante a luta
  const zonaN = unitInfo ? unitInfo.n - 1 : 0;
  const HP_MAX = chefe ? vidaBoss(nivelHeroi, zonaN) : 100;
  const fraqueza = chefe ? (FRAQUEZA_CHEFE[chefe.id] as EstiloArma) : undefined;
  const fraco = !!fraqueza && fraqueza === armaVestida(game.inv, game.equip); // a arma vestida é o ponto fraco do chefe
  const [bossHp, setBossHp] = useState(HP_MAX);
  const [golpe, setGolpe] = useState(0);
  const [dano, setDano] = useState(0);
  const [ataque, setAtaque] = useState(0);
  const escudoUsado = useRef(false);
  const [bloqueou, setBloqueou] = useState(false); // o escudo já foi gasto
  const [bloqueouAgora, setBloqueouAgora] = useState(false); // esta resposta foi bloqueada
  const [phase, setPhase] = useState<Phase>('menu');
  // Fases do chefe: com a vida abaixo de 60 ele se irrita (precisa consertar a linha), abaixo de 30 entra em fúria (menos tempo).
  const [conserte, setConserte] = useState<{ opcoes: string[]; dano: number } | null>(null);
  const [conserteOk, setConserteOk] = useState<boolean | null>(null);
  const fase = bossHp > HP_MAX * 0.6 ? 1 : bossHp > HP_MAX * 0.3 ? 2 : 3;
  const [level, setLevel] = useState(FIRE_LEVELS[0]);
  const [queue, setQueue] = useState<Bug[]>([]);
  const [idx, setIdx] = useState(0);
  const [lives, setLives] = useState(LIVES);
  const [score, setScore] = useState(0);
  const [combo, setCombo] = useState(0);
  const [bestCombo, setBestCombo] = useState(0);
  const [hits, setHits] = useState(0);
  const [picked, setPicked] = useState<number | null>(null); // -1 = tempo esgotado
  const [gain, setGain] = useState(0);
  const [left, setLeft] = useState(0);
  const [result, setResult] = useState<{ xp: number; record: boolean; passed: boolean; festa?: ReturnType<typeof escolherComemoracao>; drop?: { item: ItemInst; bau: ModeloBau } } | null>(null);
  const deadline = useRef(0);

  const bug = queue[idx];

  const start = (lv: (typeof FIRE_LEVELS)[number]) => {
    setLevel(lv);
    setQueue(lv.n === 0 && unitInfo ? shuffle(unitBugs(unitInfo.unit.id)) : shuffle(BUGS.filter((b) => b.nivel === lv.n)).slice(0, ROUND));
    setBossHp(HP_MAX); setGolpe(0); setAtaque(0); escudoUsado.current = false; setBloqueou(false);
    setConserte(null); setConserteOk(null);
    setIdx(0); setLives(LIVES); setScore(0); setCombo(0); setBestCombo(0); setHits(0); setPicked(null); setResult(null);
    deadline.current = Date.now() + lv.secs * 1000;
    setLeft(lv.secs * 1000);
    setPhase('play');
  };

  const lv0 = () => level.n === 0;
  const tempoRodada = level.secs - (lv0() && chefe && fase >= 3 ? 3 : 0); // fúria: 3 segundos a menos por bug
  const answer = (line: number) => {
    if (phase !== 'play' || !bug) return;
    setBloqueouAgora(false);
    const ok = line === bug.linha;
    const rest = Math.max(0, deadline.current - Date.now());
    setPicked(line);
    buzz(ok);
    const precisaConserte = ok && !!chefe && lv0() && fase >= 2;
    if (ok) {
      const mult = Math.min(3, 1 + combo * 0.5);
      const pts = Math.round((100 + Math.ceil(rest / 1000) * 10) * mult);
      setGain(pts); setScore((s) => s + pts); setHits((h) => h + 1);
      setCombo((c) => { setBestCombo((b) => Math.max(b, c + 1)); return c + 1; });
      if (chefe && lv0()) {
        // Dano: base + rapidez + combo (+ teclado mecânico)
        const bruto = 22 + Math.round((rest / (tempoRodada * 1000)) * 14) + Math.min(combo, 3) * 4 + (temRel('teclado') ? 10 : 0);
        const d = danoNoBoss({ bruto, nivel: nivelHeroi, zona: zonaN, furiaPct: game.bonus().dano /* habilidade Fúria */, fraco });
        if (precisaConserte) {
          // Fase 2 e 3: achar a linha não basta, é preciso escolher o conserto certo para o golpe valer
          const parecidos = shuffle(BUGS.filter((b) => b.id !== bug.id && b.correcao !== bug.correcao && b.correcao !== bug.linhas[bug.linha] && b.tipo === bug.tipo)).map((b) => b.correcao);
          const outros = shuffle(BUGS.filter((b) => b.id !== bug.id && b.correcao !== bug.correcao && b.correcao !== bug.linhas[bug.linha])).map((b) => b.correcao);
          const falso = parecidos[0] ?? outros[0] ?? '';
          setConserte({ opcoes: shuffle([bug.correcao, bug.linhas[bug.linha], falso].filter((v, i, a) => v && a.indexOf(v) === i)), dano: d });
          setConserteOk(null);
        } else { setDano(d); setBossHp((h) => Math.max(0, h - d)); setGolpe((x) => x + 1); }
      }
    } else {
      setGain(0); setCombo(0);
      if (chefe && lv0() && temRel('escudo') && !escudoUsado.current) { escudoUsado.current = true; setBloqueou(true); setBloqueouAgora(true); }
      else setLives((l) => l - 1);
      if (chefe && lv0()) setAtaque((x) => x + 1);
    }
    setLeft(rest);
    setPhase(precisaConserte ? 'conserte' : 'reveal');
  };

  /** Escolha do conserto (fase 2 e 3): acertar causa o dano que estava guardado; errar deixa o chefe contra-atacar. */
  const escolherConserte = (opc: string) => {
    if (phase !== 'conserte' || !conserte || !bug) return;
    const certo = opc === bug.correcao;
    buzz(certo);
    setConserteOk(certo);
    if (certo) { setDano(conserte.dano); setBossHp((h) => Math.max(0, h - conserte.dano)); setGolpe((x) => x + 1); }
    else { setAtaque((x) => x + 1); setLives((l) => l - 1); setCombo(0); }
    setPhase('reveal');
  };

  // Cronômetro
  useEffect(() => {
    if (phase !== 'play') return;
    const id = setInterval(() => {
      const rest = deadline.current - Date.now();
      if (rest <= 0) { clearInterval(id); answer(-1); } else setLeft(rest);
    }, 100);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase, idx]);

  const finish = (finalHits: number) => {
    const acc = Math.round((finalHits / Math.max(1, idx + 1)) * 100);
    if (level.n === 0 && unitInfo) {
      // Prova da unidade: passa quem termina com pelo menos uma chama acesa.
      const id = `fogo-${unitInfo.unit.id}`;
      const passed = bossHp <= 0;
      const xp = passed ? (id in game.done ? 5 : 10) + (finalHits === queue.length ? 5 : 0) : 0;
      game.registrar('provas');
      let drop: { item: ItemInst; bau: ModeloBau } | undefined;
      if (passed) {
        drop = game.soltarItem(unitInfo.n - 1, 'boss'); // o chefe deixa o baú de chefe: sempre melhor que o normal da zona, e evolui com ela
        game.ganharMoedas(MOEDAS.prova);
        game.premiarZona(unitInfo.unit.id);
        game.visitar(unitInfo.unit.id, `${unitInfo.unit.id}:chefe`);
        game.completeLesson(id, xp, acc);
        pushLessonResult(id, xp, acc).catch(() => {});
      }
      setResult({ xp, record: false, passed, drop, festa: escolherComemoracao({ erros: queue.length - finalHits, segundos: 999, exercicios: queue.length }) });
      setPhase('end');
      return;
    }
    const xp = finalHits === 0 ? 0 : finalHits * 2 + (finalHits === ROUND ? 5 : 0);
    const record = game.finishFire(level.n, score);
    game.registrar('provas');
    if (finalHits > 0) game.ganharMoedas(MOEDAS.prova);
    if (xp > 0) {
      game.completeLesson(null, xp, acc);
      pushLessonResult(null, xp, acc).catch(() => {});
    }
    setResult({ xp, record, passed: true });
    setPhase('end');
  };

  const next = () => {
    if (lives <= 0 || idx + 1 >= queue.length || (lv0() && bossHp <= 0)) { finish(hits); return; }
    setIdx((i) => i + 1);
    setPicked(null);
    deadline.current = Date.now() + tempoRodada * 1000;
    setLeft(tempoRodada * 1000);
    setPhase('play');
  };

  // ------------------------------------------------------------------ abertura: o chefe da zona
  if (phase === 'menu' && unitInfo && unitLevel && chefe) {
    return (
      <ScrollView style={{ backgroundColor: t.bg }} contentContainerStyle={[styles.center, { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 24 }]}>
        <Text style={[styles.counter, { color: t.bad }]}>CHEFE DA ZONA {unitInfo.n} · {unitInfo.unit.title.toUpperCase()}</Text>
        <ChefeArte chefe={chefe} size={170} />
        <Text style={[styles.h2, { color: t.ink }]}>{chefe.nome}</Text>
        <Text style={[styles.fala, { color: t.muted }]}>"{chefe.fala}"</Text>
        {!!fraqueza && (
          <Text style={{ color: fraco ? t.good : t.sunDeep, fontWeight: '900', textAlign: 'center' }} accessibilityLabel={`Ponto fraco: ${NOME_ARMA[fraqueza]}`}>
            {fraco ? `★ PONTO FRACO: ${NOME_ARMA[fraqueza]} (você está usando!)` : `PONTO FRACO: ${NOME_ARMA[fraqueza]}. Troque a arma no Inventário para causar +25% de dano.`}
          </Text>
        )}
        <Text style={{ color: t.muted, fontWeight: '800', fontSize: 13 }}>Vida do chefe: {HP_MAX} (acompanha o seu nível {nivelHeroi})</Text>
        <View style={[styles.introBox, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '800', fontSize: 16, lineHeight: 22 }}>
            Cada código tem um bug sobre {unitInfo.unit.group ? unitInfo.unit.title : unitInfo.unit.description.toLowerCase()}. Toque na linha errada em até {unitLevel.secs} segundos: cada acerto tira vida do chefe. Quanto mais rápido e mais acertos seguidos, mais dano.
          </Text>
          <Text style={{ color: t.muted, fontWeight: '700', marginTop: 6 }}>
            Errou ou o tempo acabou, o chefe ataca: você tem {LIVES} vidas nesta luta.
          </Text>
        </View>
        {rota.reliquias.length > 0 && (
          <View style={{ width: '100%', maxWidth: 440, gap: 6 }}>
            <Text style={[styles.counter, { color: t.muted }]}>RELÍQUIAS ATIVAS</Text>
            {rota.reliquias.map((r) => <CartaoReliquia key={r} id={r} />)}
          </View>
        )}
        <Button3D label="Lutar" variant="bad" style={styles.wide} onPress={() => start(unitLevel)} />
        <Button3D label="Agora não" variant="ghost" style={styles.wide} onPress={() => router.back()} />
      </ScrollView>
    );
  }

  // ------------------------------------------------------------------ menu
  if (phase === 'menu') {
    return (
      <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
        <View style={styles.head}>
          <Pressable onPress={() => router.back()} accessibilityLabel="Sair da prova de fogo" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
          <Text style={[styles.headTitle, { color: t.ink }]}>Prova de fogo</Text>
          <View style={{ width: 26 }} />
        </View>
        <ScrollView contentContainerStyle={styles.menu}>
          <View style={styles.hero}>
            <Mascot size={110} mood="think" />
            <View style={[styles.bubble, { backgroundColor: t.surface, borderColor: t.line }]}>
              <Text style={{ color: t.ink, fontWeight: '800', fontSize: 16, lineHeight: 22 }}>
                Cada código tem UM erro. Toque na linha errada antes do tempo acabar!
              </Text>
              <Text style={{ color: t.muted, fontWeight: '700', marginTop: 6 }}>
                {ROUND} bugs por prova · {LIVES} chamas · acertos seguidos multiplicam os pontos
              </Text>
            </View>
          </View>
          {FIRE_LEVELS.map((lv) => {
            const best = game.fire?.[lv.n] ?? 0;
            const total = BUGS.filter((b) => b.nivel === lv.n).length;
            return (
              <Pressable key={lv.n} onPress={() => start(lv)} accessibilityLabel={`Nível ${lv.name}, ${lv.secs} segundos por bug`}
                style={({ pressed }) => [styles.level, { backgroundColor: lv.color, borderBottomColor: lv.deep, transform: [{ translateY: pressed ? 3 : 0 }], borderBottomWidth: pressed ? 2 : 5 }]}>
                <View style={styles.levelFlames}>{Array.from({ length: lv.n }, (_, k) => <Icone key={k} nome="chama" size={20} color="#fff" />)}</View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.levelName}>{lv.name}</Text>
                  <Text style={styles.levelDesc}>{lv.desc}</Text>
                  <Text style={styles.levelMeta}>{lv.secs}s por bug · {total} bugs no banco</Text>
                </View>
                <View style={styles.levelBest}>
                  <Text style={styles.levelBestLabel}>RECORDE</Text>
                  <Text style={styles.levelBestNum}>{best}</Text>
                </View>
              </Pressable>
            );
          })}
        </ScrollView>
      </View>
    );
  }

  // ------------------------------------------------------------------ fim
  if (phase === 'end' && result && unitInfo && level.n === 0) {
    return (
      <View style={{ flex: 1, backgroundColor: t.bg }}><ScrollView style={{ flex: 1 }} contentContainerStyle={[styles.centerRola, { paddingTop: insets.top + 24, paddingBottom: insets.bottom + 28 }]}>
        {result.passed
          ? <Celebration c={{ ...result.festa!, titulo: 'CHEFE DERROTADO!', frase: `${chefe?.nome ?? 'O chefe'} caiu. A zona ${unitInfo.n + 1} está liberada!` }} />
          : <>{chefe && <ChefeArte chefe={chefe} size={130} />}<Text style={[styles.h2, { color: t.ink }]}>O chefe venceu desta vez</Text></>}
        <Text style={[styles.sub, { color: t.muted }]}>
          {result.passed ? 'Recompensa da zona: 50 moedas na primeira vitória.' : `Ele ficou com ${bossHp} de vida. Os bugs mudam a cada luta, e as relíquias continuam com você.`}
        </Text>
        <View style={styles.tiles}>
          <Tile label="ACERTOS" value={`${hits}/${idx + 1}`} color={t.good} />
          <Tile label="XP" value={`+${result.xp}`} color={level.color} />
          <Tile label="VIDAS" value={`${Math.max(0, lives)}/${LIVES}`} color={t.bad} />
        </View>
        {result.drop && <BauDeDrop drop={result.drop} quem="O CHEFE" rotulo="Abrir o baú do chefe" />}
        {result.passed
          ? <Button3D label="Continuar" style={styles.wide} onPress={() => router.back()} />
          : <Button3D label="Lutar de novo" variant="bad" style={styles.wide} onPress={() => start(level)} />}
        {!result.passed && <Button3D label="Voltar ao mapa" variant="ghost" style={styles.wide} onPress={() => router.back()} />}
      </ScrollView>
      </View>
    );
  }

  if (phase === 'end' && result) {
    const perfect = hits === queue.length;
    return (
      <View style={[styles.center, { backgroundColor: t.bg, paddingTop: insets.top, paddingBottom: insets.bottom + 20 }]}>
        <Mascot size={140} mood={hits >= ROUND / 2 ? 'cheer' : 'sad'} />
        <Text style={[styles.h2, { color: t.ink }]}>{lives <= 0 ? 'As chamas apagaram!' : perfect ? 'Prova perfeita!' : 'Prova concluída!'}</Text>
        {result.record && <View style={[styles.recordBox, { backgroundColor: level.color }]}><Icone nome="trofeu" size={18} color="#fff" /><Text style={styles.record}>Recorde novo no {level.name}!</Text></View>}
        <View style={styles.tiles}>
          <Tile label="PONTOS" value={String(score)} color={level.color} />
          <Tile label="ACERTOS" value={`${hits}/${queue.length}`} color={t.good} />
          <Tile label="COMBO" value={`x${bestCombo}`} color={t.brand} />
        </View>
        <Text style={[styles.sub, { color: t.muted }]}>
          {result.xp > 0 ? `+${result.xp} XP${perfect ? ' (com bônus de prova perfeita)' : ''}` : 'Sem XP desta vez. Bora de novo?'}
        </Text>
        <Button3D label="Jogar de novo" style={styles.wide} onPress={() => start(level)} />
        <Button3D label="Escolher nível" variant="ghost" style={styles.wide} onPress={() => setPhase('menu')} />
      </View>
    );
  }

  if (!bug) return null;

  // ------------------------------------------------------------------ jogo
  const total = tempoRodada * 1000;
  const frac = Math.max(0, Math.min(1, left / total));
  const barColor = frac > 0.5 ? t.good : frac > 0.25 ? t.sun : t.bad;
  const reveal = phase === 'reveal';
  const travado = reveal || phase === 'conserte';
  const ok = picked === bug.linha;
  const mult = Math.min(3, 1 + combo * 0.5);

  return (
    <View style={{ flex: 1, backgroundColor: t.bg, paddingTop: insets.top }}>
      <View style={styles.head}>
        <Pressable onPress={() => (unitInfo ? router.back() : setPhase('menu'))} accessibilityLabel="Sair da prova" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        {lv0() ? <Text style={[styles.headTitle, { color: t.ink }]}>Chefe da zona</Text> : (
          <View style={{ flexDirection: 'row', gap: 2 }} accessibilityLabel={`${lives} chamas`}>
            {Array.from({ length: LIVES }, (_, i) => <Icone key={i} nome="chama" size={22} color={i < lives ? '#FF7A1A' : t.line} />)}
          </View>
        )}
        <Text style={[styles.score, { color: t.ink }]} accessibilityLabel={`${score} pontos`}>{lv0() ? '' : score}</Text>
      </View>

      <View style={styles.timerRow}>
        <View style={[styles.timer, { backgroundColor: t.line }]}>
          <View style={[styles.timerFill, { width: `${frac * 100}%`, backgroundColor: barColor }]} />
        </View>
        <Text style={[styles.secs, { color: frac > 0.25 ? t.ink : t.bad }]}>{Math.ceil(left / 1000)}s</Text>
      </View>

      <ScrollView contentContainerStyle={styles.body}>
        {lv0() && chefe && (
          <ChefeArena chefe={chefe} hp={bossHp} hpMax={HP_MAX} golpe={golpe} dano={dano} ataque={ataque} bloqueou={bloqueou}
            vidas={Math.max(0, lives)} vidasMax={LIVES} fase={fase} fraco={fraco} fraqueza={fraqueza} nomeFraqueza={fraqueza ? NOME_ARMA[fraqueza] : undefined} />
        )}
        {lv0() && chefe && fase >= 2 && (
          <Text style={[styles.faseTag, { backgroundColor: fase === 3 ? t.bad : t.sun, color: fase === 3 ? '#fff' : t.sunInk }]} accessibilityLiveRegion="polite">
            {fase === 3 ? 'FASE 3 · FÚRIA! Menos tempo por bug, e o conserto é obrigatório.' : 'FASE 2 · O chefe se irritou! Depois de achar a linha, escolha o conserto certo.'}
          </Text>
        )}

        <View style={styles.qRow}>
          <Text style={[styles.counter, { color: level.deep }]}>{level.name.toUpperCase()} · BUG {idx + 1} DE {queue.length}</Text>
          {combo >= 2 && <Text style={[styles.combo, { backgroundColor: level.color }]}>COMBO x{mult.toFixed(1).replace('.0', '')}</Text>}
        </View>
        <Text style={[styles.q, { color: t.ink }]}>Toque na linha com o erro</Text>

        <View style={[styles.code, { backgroundColor: t.codeBg }]}>
          {bug.linhas.map((ln, i) => {
            const isBug = i === bug.linha;
            const isPick = i === picked;
            const bg = reveal ? (isBug ? (ok ? 'rgba(56,194,119,0.28)' : 'rgba(240,100,106,0.30)') : isPick ? 'rgba(255,255,255,0.10)' : 'transparent') : 'transparent';
            return (
              <Pressable key={i} onPress={() => answer(i)} disabled={travado} accessibilityLabel={`Linha ${i + 1}: ${ln.trim() || 'vazia'}`}
                style={({ pressed, hovered }: { pressed: boolean; hovered?: boolean }) => [styles.line, { backgroundColor: !travado && (pressed || hovered) ? 'rgba(255,255,255,0.08)' : bg }]}>
                <Text style={[styles.gutter, { color: reveal && isBug ? (ok ? t.good : t.bad) : t.cCom, fontFamily: mono }]}>{i + 1}</Text>
                <Text style={[styles.lineText, { color: t.codeFg, fontFamily: mono }]}>{ln ? highlight(ln, t) : ' '}</Text>
                {reveal && isPick && !isBug && <View style={styles.mark}><Icone nome="x" size={16} color="#FF9DA1" /></View>}
                {reveal && isBug && <View style={styles.mark}><Icone nome={ok ? 'check' : 'inseto'} size={16} color={ok ? '#8BE3A9' : '#FF9DA1'} /></View>}
              </Pressable>
            );
          })}
        </View>

        {phase === 'conserte' && conserte && (
          <View style={[styles.fix, { backgroundColor: t.surface, borderColor: t.sun }]}>
            <Text style={[styles.fixTitle, { color: t.sunDeep }]}>Achou a linha {bug.linha + 1}! Agora, como fica o conserto?</Text>
            {conserte.opcoes.map((o) => (
              <Pressable key={o} onPress={() => escolherConserte(o)} accessibilityRole="button" accessibilityLabel={`Conserto: ${o}`}
                style={({ pressed }) => [styles.opcaoConserte, { backgroundColor: t.codeBg, opacity: pressed ? 0.8 : 1 }]}>
                <Text style={{ color: '#8BE3A9', fontFamily: mono, fontSize: 14 }}>{o}</Text>
              </Pressable>
            ))}
          </View>
        )}

        {reveal && (
          <View style={[styles.fix, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={[styles.fixTitle, { color: ok ? t.good : t.bad }]}>
              {ok ? (lv0() ? (conserteOk === false ? 'Achou a linha, mas o conserto estava errado. O chefe contra-atacou!' : `Acertou! -${dano} de vida do chefe${bossHp <= 0 ? '. Ele caiu!' : ''}`) : `Achou! +${gain} pontos`) : bloqueouAgora ? `O escudo try/except bloqueou o ataque! O erro estava na linha ${bug.linha + 1}.` : picked === -1 ? `Tempo esgotado! O erro estava na linha ${bug.linha + 1}.` : `Não era essa. O erro estava na linha ${bug.linha + 1}.`}
            </Text>
            <View style={styles.tipoRow}>
              <Text style={[styles.tipo, { backgroundColor: t.badBg, color: t.badInk }]}>{bug.tipo}</Text>
            </View>
            {bug.tipo !== 'Resultado errado' && <Text style={{ color: t.muted, fontFamily: mono, fontSize: 13 }}>{bug.msg}</Text>}
            <Text style={{ color: t.ink, fontWeight: '700', fontSize: 15, lineHeight: 21 }}>{bug.explica}</Text>
            <View style={[styles.diff, { backgroundColor: t.codeBg }]}>
              <Text style={[styles.diffLine, { color: '#FF9DA1', fontFamily: mono }]}>- {bug.linhas[bug.linha]}</Text>
              <Text style={[styles.diffLine, { color: '#8BE3A9', fontFamily: mono }]}>+ {bug.correcao}</Text>
            </View>
          </View>
        )}
      </ScrollView>

      {reveal && (
        <View style={[styles.foot, { borderTopColor: t.line, paddingBottom: insets.bottom + 16 }]}>
          <Button3D style={styles.footBtn} variant={ok ? 'good' : 'bad'}
            label={lives <= 0 || idx + 1 >= queue.length || (lv0() && bossHp <= 0) ? 'Ver resultado' : lv0() ? 'Próximo ataque' : 'Próximo bug'} onPress={next} />
        </View>
      )}
    </View>
  );
}

function Tile({ label, value, color }: { label: string; value: string; color: string }) {
  const t = useTheme();
  return (
    <View style={[styles.st, { borderColor: color, backgroundColor: t.surface }]}>
      <Text style={[styles.stH, { backgroundColor: color }]}>{label}</Text>
      <Text style={[styles.stV, { color: t.ink }]}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  faseTag: { fontWeight: '900', fontSize: 12.5, lineHeight: 17, borderRadius: 10, paddingVertical: 6, paddingHorizontal: 10, overflow: 'hidden', marginBottom: 8 },
  opcaoConserte: { borderRadius: 10, paddingVertical: 12, paddingHorizontal: 12, marginTop: 6 },
  head: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 14, paddingHorizontal: 16, paddingVertical: 12, maxWidth: 760, width: '100%', alignSelf: 'center' },
  headTitle: { fontSize: 18, fontWeight: '900' },
  score: { fontSize: 22, fontWeight: '900', fontVariant: ['tabular-nums'], minWidth: 60, textAlign: 'right' },
  menu: { padding: 16, gap: 14, maxWidth: 640, width: '100%', alignSelf: 'center', paddingBottom: 40 },
  hero: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 6 },
  bubble: { flex: 1, borderWidth: 2, borderRadius: 16, padding: 14 },
  introBox: { width: '100%', maxWidth: 440, borderWidth: 2, borderRadius: 16, padding: 14 },
  level: { flexDirection: 'row', alignItems: 'center', gap: 12, borderRadius: 18, padding: 16 },
  levelFlames: { width: 66, flexDirection: 'row', justifyContent: 'center' },
  levelName: { color: '#fff', fontSize: 22, fontWeight: '900' },
  levelDesc: { color: 'rgba(255,255,255,0.95)', fontWeight: '700', fontSize: 14 },
  levelMeta: { color: 'rgba(255,255,255,0.85)', fontWeight: '800', fontSize: 12, marginTop: 4 },
  levelBest: { alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.18)', borderRadius: 12, paddingVertical: 6, paddingHorizontal: 10 },
  levelBestLabel: { color: '#fff', fontSize: 10, fontWeight: '900', letterSpacing: 0.8 },
  levelBestNum: { color: '#fff', fontSize: 20, fontWeight: '900', fontVariant: ['tabular-nums'] },
  timerRow: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingHorizontal: 16, maxWidth: 760, width: '100%', alignSelf: 'center' },
  timer: { flex: 1, height: 14, borderRadius: 99, overflow: 'hidden' },
  timerFill: { height: '100%', borderRadius: 99 },
  secs: { fontWeight: '900', fontSize: 16, width: 36, textAlign: 'right', fontVariant: ['tabular-nums'] },
  body: { padding: 16, gap: 12, maxWidth: 640, width: '100%', alignSelf: 'center', paddingBottom: 40 },
  qRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  counter: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  combo: { color: '#fff', fontWeight: '900', fontSize: 12, borderRadius: 99, paddingHorizontal: 10, paddingVertical: 3, overflow: 'hidden' },
  q: { fontSize: 22, fontWeight: '900' },
  code: { borderRadius: 14, paddingVertical: 8 },
  line: { flexDirection: 'row', alignItems: 'flex-start', paddingVertical: 7, paddingRight: 10, minHeight: 40 },
  gutter: { width: 34, textAlign: 'right', paddingRight: 10, fontSize: 14, lineHeight: 24 },
  lineText: { flex: 1, fontSize: 15, lineHeight: 24 },
  mark: { marginLeft: 6, marginTop: 4 },
  fala: { fontSize: 16, fontWeight: '700', fontStyle: 'italic', textAlign: 'center' },
  fix: { borderWidth: 2, borderRadius: 16, padding: 14, gap: 8 },
  fixTitle: { fontSize: 18, fontWeight: '900' },
  tipoRow: { flexDirection: 'row' },
  tipo: { fontWeight: '900', fontSize: 12, borderRadius: 8, paddingHorizontal: 8, paddingVertical: 3, overflow: 'hidden' },
  diff: { borderRadius: 10, padding: 10, gap: 2 },
  diffLine: { fontSize: 14, lineHeight: 21 },
  foot: { borderTopWidth: 2, paddingHorizontal: 16, paddingTop: 16 },
  footBtn: { width: '100%', maxWidth: 728, alignSelf: 'center' },
  bauChefe: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 3, borderRadius: 18, padding: 12, width: '100%', maxWidth: 440 },
  centerRola: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', gap: 16, paddingHorizontal: 24 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 16, padding: 24 },
  h2: { fontSize: 28, fontWeight: '900', textAlign: 'center' },
  sub: { fontSize: 16, fontWeight: '800', textAlign: 'center' },
  record: { color: '#fff', fontWeight: '900', fontSize: 15 },
  recordBox: { flexDirection: 'row', alignItems: 'center', gap: 6, borderRadius: 99, paddingHorizontal: 14, paddingVertical: 6 },
  tiles: { flexDirection: 'row', gap: 10, width: '100%', maxWidth: 440 },
  st: { flex: 1, borderWidth: 2, borderRadius: 14, overflow: 'hidden' },
  stH: { textAlign: 'center', fontSize: 11, fontWeight: '900', letterSpacing: 0.8, paddingVertical: 4, color: '#fff' },
  stV: { textAlign: 'center', fontSize: 22, fontWeight: '900', paddingVertical: 10, fontVariant: ['tabular-nums'] },
  wide: { width: '100%', maxWidth: 440 },
});
