import { router } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Avatar, CastFace } from '@/components/Characters';
import { CodeBlock } from '@/components/CodeBlock';
import { Cross } from '@/components/Icons';
import { Icone } from '@/components/Icone';
import { Moeda } from '@/components/Moeda';
import { ADVERSARIOS, falaDaRodada, pontos, RODADAS, simularAdversario, sortearPerguntas, TEMPO_S, type Adversario, type Pergunta, type Resultado } from '@/lib/duelo';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

type Fase = 'escolha' | 'jogo' | 'revela' | 'fim';
type Rodada = { escolha: string | null; pEu: number; pEle: number; eleAcertou: boolean; eleSeg: number };

/** Duelo contra o elenco: 5 perguntas, 15 segundos cada. O adversário é simulado e responde no ritmo dele. */
export default function DueloScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const [fase, setFase] = useState<Fase>('escolha');
  const [adv, setAdv] = useState<Adversario>(ADVERSARIOS[1]);
  const [perguntas, setPerguntas] = useState<Pergunta[]>([]);
  const [i, setI] = useState(0);
  const [placar, setPlacar] = useState({ eu: 0, ele: 0 });
  const [acertos, setAcertos] = useState(0);
  const [rod, setRod] = useState<Rodada | null>(null);
  const [left, setLeft] = useState(TEMPO_S * 1000);
  const [fala, setFala] = useState('');
  const [premio, setPremio] = useState<{ xp: number; moedas: number } | null>(null);
  const prazo = useRef(0);
  const ele = useRef({ acertou: false, segundos: 5 });
  const pago = useRef(false);

  const comecarRodada = (a: Adversario, p: Pergunta, n: number) => {
    setFala(falaDaRodada(a, p, n));
    ele.current = simularAdversario(a);
    prazo.current = Date.now() + TEMPO_S * 1000;
    setLeft(TEMPO_S * 1000);
    setRod(null);
    setFase('jogo');
  };

  const iniciar = (a: Adversario) => {
    setAdv(a);
    const ps = sortearPerguntas(g.done);
    setPerguntas(ps);
    setI(0); setPlacar({ eu: 0, ele: 0 }); setAcertos(0); setPremio(null);
    pago.current = false;
    comecarRodada(a, ps[0], 0);
  };

  const responder = (escolha: string | null) => {
    if (fase !== 'jogo') return;
    const p = perguntas[i];
    const rest = Math.max(0, prazo.current - Date.now()) / 1000;
    const certa = escolha !== null && escolha === p.certa;
    const eleResp = ele.current.segundos <= TEMPO_S; // o adversário também pode ficar sem tempo
    const eleAcertou = eleResp && ele.current.acertou;
    const pEu = pontos(certa, rest);
    const pEle = pontos(eleAcertou, TEMPO_S - ele.current.segundos);
    setPlacar((s) => ({ eu: s.eu + pEu, ele: s.ele + pEle }));
    if (certa) setAcertos((a) => a + 1);
    setRod({ escolha, pEu, pEle, eleAcertou, eleSeg: ele.current.segundos });
    setLeft(rest * 1000);
    setFase('revela');
  };

  // Cronômetro da rodada
  useEffect(() => {
    if (fase !== 'jogo') return;
    const id = setInterval(() => {
      const rest = prazo.current - Date.now();
      if (rest <= 0) { clearInterval(id); responder(null); } else setLeft(rest);
    }, 100);
    return () => clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fase, i]);

  const resultado: Resultado = placar.eu > placar.ele ? 'v' : placar.eu < placar.ele ? 'd' : 'e';

  const proxima = () => {
    if (i + 1 >= RODADAS) {
      if (!pago.current) { pago.current = true; setPremio(g.fimDoDuelo(adv.id, resultado, acertos, RODADAS)); }
      setFase('fim');
      return;
    }
    setI(i + 1);
    comecarRodada(adv, perguntas[i + 1], i + 1);
  };

  const head = (titulo: string) => (
    <View style={[styles.head, { paddingTop: insets.top + 10 }]}>
      <Pressable onPress={() => router.back()} accessibilityLabel="Sair do duelo" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
      <Text style={[styles.titulo, { color: t.ink }]}>{titulo}</Text>
      <View style={{ width: 26 }} />
    </View>
  );

  // ------------------------------------------------------------------ escolha do adversário
  if (fase === 'escolha') {
    return (
      <View style={{ flex: 1, backgroundColor: t.bg }}>
        {head('Duelo')}
        <ScrollView contentContainerStyle={[styles.wrap, { paddingBottom: insets.bottom + 24 }]}>
          <Text style={{ color: t.muted, fontWeight: '700', fontSize: 15, lineHeight: 21 }}>
            {RODADAS} perguntas, {TEMPO_S} segundos cada. Acertar vale 100 pontos mais 5 por segundo que sobrar: quem somar mais vence. Escolha contra quem jogar.
          </Text>
          {ADVERSARIOS.map((a) => {
            const r = g.duelos?.[a.id] ?? { v: 0, d: 0, e: 0 };
            return (
              <Pressable key={a.id} onPress={() => iniciar(a)} accessibilityRole="button" accessibilityLabel={`Duelo contra ${a.nome}. ${a.estilo}`}
                style={({ pressed }) => [styles.adv, { backgroundColor: t.surface, borderColor: t.line, borderBottomWidth: pressed ? 2 : 5 }]}>
                <CastFace id={a.id} size={64} />
                <View style={{ flex: 1, gap: 2 }}>
                  <Text style={{ color: t.ink, fontWeight: '900', fontSize: 18 }}>{a.nome}</Text>
                  <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{a.estilo}</Text>
                  <Text style={{ color: t.sunDeep, fontWeight: '800', fontSize: 12 }}>{r.v} vitórias · {r.d} derrotas · {r.e} empates</Text>
                </View>
                <Icone nome="espada" size={24} color={t.brand} />
              </Pressable>
            );
          })}
        </ScrollView>
      </View>
    );
  }

  // ------------------------------------------------------------------ fim
  if (fase === 'fim') {
    const humor = resultado === 'v' ? 'sad' : resultado === 'd' ? 'cheer' : 'think';
    const titulo = resultado === 'v' ? 'Você venceu!' : resultado === 'd' ? `${adv.nome} venceu` : 'Empate!';
    const fala = (resultado === 'v' ? adv.perdeu : adv.ganhou)[acertos % 2];
    return (
      <View style={[styles.centro, { backgroundColor: t.bg, paddingTop: insets.top + 12, paddingBottom: insets.bottom + 20 }]}>
        <CastFace id={adv.id} size={120} mood={resultado === 'e' ? 'think' : humor} />
        <Text style={[styles.h2, { color: t.ink }]}>{titulo}</Text>
        {resultado !== 'e' && <Text style={{ color: t.muted, fontWeight: '700', fontStyle: 'italic' }}>{adv.nome}: “{fala}”</Text>}
        <View style={styles.placarFim}>
          <Placar nome="Você" pts={placar.eu} cor={t.brand} ganhou={resultado === 'v'} />
          <Placar nome={adv.nome} pts={placar.ele} cor={t.bad} ganhou={resultado === 'd'} />
        </View>
        <Text style={{ color: t.muted, fontWeight: '800' }}>Você acertou {acertos} de {RODADAS} perguntas</Text>
        {premio && (
          <View style={[styles.premio, { borderColor: t.sun, backgroundColor: t.surface }]}>
            <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>+{premio.xp} XP</Text>
            <Moeda size={22} /><Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>+{premio.moedas}</Text>
          </View>
        )}
        <Button3D label="Revanche" style={styles.wide} onPress={() => iniciar(adv)} />
        <Button3D label="Outro adversário" variant="ghost" style={styles.wide} onPress={() => setFase('escolha')} />
        <Button3D label="Voltar" variant="ghost" style={styles.wide} onPress={() => router.back()} />
      </View>
    );
  }

  // ------------------------------------------------------------------ rodada
  const p = perguntas[i];
  if (!p) return <View style={{ flex: 1, backgroundColor: t.bg }}>{head('Duelo')}</View>;
  const decorrido = (TEMPO_S * 1000 - left) / 1000;
  const eleJa = fase === 'revela' || decorrido >= ele.current.segundos;
  const frac = Math.max(0, Math.min(1, left / (TEMPO_S * 1000)));
  const cor = frac > 0.5 ? t.good : frac > 0.25 ? t.sun : t.bad;
  const reacao = rod ? (rod.pEu > rod.pEle ? adv.perdeu : rod.pEu < rod.pEle ? adv.ganhou : adv.perdeu)[i % 2] : '';

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10 }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Sair do duelo" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <View style={[styles.barra, { backgroundColor: t.line }]} accessibilityLabel={`${Math.ceil(left / 1000)} segundos restantes`}>
          <View style={[styles.barraCheia, { width: `${frac * 100}%`, backgroundColor: cor }]} />
        </View>
        <Text style={{ color: t.ink, fontWeight: '900', fontVariant: ['tabular-nums'], minWidth: 30, textAlign: 'right' }}>{Math.ceil(left / 1000)}s</Text>
      </View>

      <View style={styles.placarTopo}>
        <View style={[styles.lado, { backgroundColor: t.surface, borderColor: t.brand }]}>
          <Avatar seed={g.avatarSeed} size={40} />
          <View><Text style={styles.ladoNome}>Você</Text><Text style={[styles.ladoPts, { color: t.brand }]}>{placar.eu}</Text></View>
        </View>
        <Text style={{ color: t.muted, fontWeight: '900' }}>{i + 1}/{RODADAS}</Text>
        <View style={[styles.lado, { backgroundColor: t.surface, borderColor: t.bad }]}>
          <View><Text style={[styles.ladoNome, { textAlign: 'right' }]}>{adv.nome}</Text><Text style={[styles.ladoPts, { color: t.bad, textAlign: 'right' }]}>{placar.ele}</Text></View>
          <CastFace id={adv.id} size={40} mood={eleJa ? 'cheer' : 'think'} />
        </View>
      </View>
      <Text style={{ color: eleJa ? t.good : t.muted, fontWeight: '800', fontSize: 12, textAlign: 'center', marginTop: 2 }} accessibilityLiveRegion="polite">
        {eleJa ? `${adv.nome} já respondeu` : `${adv.nome}: “${fala}”`}
      </Text>

      <ScrollView contentContainerStyle={styles.corpo}>
        <Text style={[styles.pergunta, { color: t.ink }]}>{p.ex.q}</Text>
        {!!p.ex.c && <View style={{ marginTop: 8 }}><CodeBlock code={p.ex.c} /></View>}
        <View style={{ gap: 10, marginTop: 14 }}>
          {p.opcoes.map((o, k) => {
            const revela = fase === 'revela';
            const certa = o === p.certa;
            const escolhida = rod?.escolha === o;
            const bg = revela ? (certa ? t.goodBg : escolhida ? t.badBg : t.surface) : t.surface;
            const borda = revela ? (certa ? t.good : escolhida ? t.bad : t.line) : t.line;
            return (
              <Pressable key={`${i}-${k}`} onPress={() => responder(o)} disabled={revela} accessibilityRole="button" accessibilityLabel={o}
                style={({ pressed }) => [styles.opcao, { backgroundColor: bg, borderColor: borda, borderBottomWidth: pressed && !revela ? 2 : 4, opacity: revela && !certa && !escolhida ? 0.6 : 1 }]}>
                <Text style={{ color: t.ink, fontWeight: '800', fontSize: 16, flex: 1 }}>{o}</Text>
                {revela && certa && <Icone nome="check" size={20} color={t.good} />}
                {revela && escolhida && !certa && <Icone nome="x" size={20} color={t.bad} />}
              </Pressable>
            );
          })}
        </View>
      </ScrollView>

      {fase === 'revela' && rod && (
        <View style={[styles.foot, { backgroundColor: t.surface, borderTopColor: t.line, paddingBottom: insets.bottom + 14 }]}>
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <View style={[styles.res, { backgroundColor: rod.pEu ? t.goodBg : t.badBg }]}>
              <Text style={{ color: rod.pEu ? t.goodInk : t.badInk, fontWeight: '900' }}>Você {rod.pEu ? `+${rod.pEu}` : rod.escolha === null ? 'sem tempo' : 'errou'}</Text>
            </View>
            <View style={[styles.res, { backgroundColor: rod.pEle ? t.goodBg : t.badBg }]}>
              <Text style={{ color: rod.pEle ? t.goodInk : t.badInk, fontWeight: '900' }}>{adv.nome} {rod.pEle ? `+${rod.pEle}` : 'errou'}</Text>
            </View>
          </View>
          <Text style={{ color: t.muted, fontWeight: '700', fontStyle: 'italic', textAlign: 'center' }}>{adv.nome}: “{reacao}”</Text>
          <Button3D label={i + 1 >= RODADAS ? 'Ver resultado' : 'Próxima'} onPress={proxima} />
        </View>
      )}
    </View>
  );
}

function Placar({ nome, pts, cor, ganhou }: { nome: string; pts: number; cor: string; ganhou: boolean }) {
  const t = useTheme();
  return (
    <View style={[styles.pFim, { borderColor: ganhou ? cor : t.line, backgroundColor: t.surface }]}>
      <Text style={{ color: t.muted, fontWeight: '800', fontSize: 12 }}>{nome.toUpperCase()}</Text>
      <Text style={{ color: cor, fontWeight: '900', fontSize: 30, fontVariant: ['tabular-nums'] }}>{pts}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 10, maxWidth: 760, width: '100%', alignSelf: 'center' },
  titulo: { flex: 1, textAlign: 'center', fontSize: 20, fontWeight: '900' },
  wrap: { padding: 16, gap: 12, maxWidth: 560, width: '100%', alignSelf: 'center' },
  adv: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 18, padding: 12 },
  barra: { flex: 1, height: 14, borderRadius: 99, overflow: 'hidden' },
  barraCheia: { height: '100%', borderRadius: 99 },
  placarTopo: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, gap: 8, maxWidth: 560, width: '100%', alignSelf: 'center' },
  lado: { flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 16, paddingVertical: 4, paddingHorizontal: 8 },
  ladoNome: { color: '#6B7886', fontWeight: '800', fontSize: 11 },
  ladoPts: { fontWeight: '900', fontSize: 20, fontVariant: ['tabular-nums'] },
  corpo: { padding: 16, paddingBottom: 24, maxWidth: 560, width: '100%', alignSelf: 'center' },
  pergunta: { fontSize: 20, fontWeight: '900', lineHeight: 27 },
  opcao: { flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 14, paddingVertical: 14, paddingHorizontal: 14 },
  foot: { borderTopWidth: 2, paddingHorizontal: 16, paddingTop: 12, gap: 10 },
  res: { flex: 1, borderRadius: 12, paddingVertical: 8, alignItems: 'center' },
  centro: { flex: 1, alignItems: 'center', gap: 12, paddingHorizontal: 20 },
  h2: { fontSize: 30, fontWeight: '900', textAlign: 'center' },
  placarFim: { flexDirection: 'row', gap: 12, width: '100%', maxWidth: 360 },
  pFim: { flex: 1, borderWidth: 3, borderRadius: 16, alignItems: 'center', paddingVertical: 10 },
  premio: { flexDirection: 'row', alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 14, paddingVertical: 8, paddingHorizontal: 16 },
  wide: { width: '100%', maxWidth: 440 },
});
