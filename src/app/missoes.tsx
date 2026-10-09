import { router } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { Cross } from '@/components/Icons';
import { Animated, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Icone, IconeTile } from '@/components/Icone';
import { Moeda } from '@/components/Moeda';
import { NivelBar } from '@/components/NivelBar';
import { CONQUISTAS, missoesDoDia, nivelDe } from '@/lib/gamificacao';
import { EVENTO_NIVEL, eventoDaSemana, META_EVENTO, PREMIO_EVENTO } from '@/lib/evento';
import { weekId } from '@/lib/leagues';
import { proximoVencimento, vencidos } from '@/lib/revisao';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

const COR_EVENTO: Record<string, string> = { xp: '#2F6FD6', licoes: '#3FA34D', perfeitas: '#E0457B', revisoes: '#C2569F', combo: '#FF7A1A', provas: '#E5383B', especiais: '#7B5CE0', codigo: '#1F9BB5', passos: '#B07A3F' };

const ate = (ms: number) => {
  const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000);
  return h > 0 ? `${h}h ${m}min` : `${m}min`;
};

/** Missões diárias, baú, revisão, conquistas e atalho para a Loja. */
export default function MissoesScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  useEffect(() => { g.tick(); g.verificar(); /* eslint-disable-next-line react-hooks/exhaustive-deps */ }, []);
  const missoes = missoesDoDia(g.hoje?.dia ?? '');
  const resgatadas = g.hoje?.resgatadas ?? [];
  const fimDoDia = new Date(); fimDoDia.setHours(24, 0, 0, 0);
  const nRev = vencidos(g.revisao).length;
  const totalRev = Object.keys(g.revisao ?? {}).length;
  const prox = proximoVencimento(g.revisao);
  const fonte = { ...(g.stats ?? {}), nivel: nivelDe(g.xp).nivel, streak: g.streak, aprendidos: Object.keys(g.aprendidos ?? {}).length, liga: g.bestLeague ?? 1 };
  const nConq = CONQUISTAS.filter((c) => g.conquistas?.[c.id]).length;
  // Evento da semana: escondido até a pessoa chegar ao nível 3 (EVENTO_NIVEL); depois mora aqui, e não na primeira página
  const eventoLiberado = nivelDe(g.xp).nivel >= EVENTO_NIVEL;
  const evento = eventoDaSemana(weekId());
  const pontosEvento = g.evento?.semana === weekId() ? g.evento.pontos : 0;
  const eventoPronto = pontosEvento >= META_EVENTO;
  const eventoResgatado = g.evento?.semana === weekId() && g.evento.resgatado;
  const [bauAberto, setBauAberto] = useState(0);
  const xp2 = g.xp2Ate > Date.now() ? g.xp2Ate - Date.now() : 0;

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.header, { paddingTop: insets.top + 8, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar as Missões" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink, flex: 1 }]}>Missões</Text>
        <Pressable onPress={() => router.push('/loja')} accessibilityLabel={`${g.moedas} moedas. Abrir a Loja`} style={[styles.moedas, { borderColor: t.line, backgroundColor: t.surface }]}>
          <Moeda size={22} /><Text style={[styles.moedasN, { color: t.sunDeep }]}>{g.moedas ?? 0}</Text>
          <Text style={{ color: t.brand, fontWeight: '900' }}>Loja ›</Text>
        </Pressable>
      </View>
      <ScrollView contentContainerStyle={styles.scroll}>
        <NivelBar xp={g.xp} />
        {eventoLiberado && (
          <View style={[styles.evento, { borderColor: evento.cor, backgroundColor: t.surface }]} accessibilityLabel={`Evento da semana, ${evento.nome}: ${pontosEvento} de ${META_EVENTO} pontos`}>
            <View style={[styles.eventoIco, { backgroundColor: evento.cor }]}><Icone nome={evento.icone} size={24} color="#fff" /></View>
            <View style={{ flex: 1, gap: 4 }}>
              <Text style={{ color: t.ink, fontWeight: '900', fontSize: 15 }}>Evento da semana: {evento.nome}</Text>
              <Text style={{ color: t.muted, fontWeight: '600', fontSize: 12.5 }}>{evento.texto} Todo mundo joga o mesmo tema esta semana.</Text>
              <View style={styles.eventoBarra}><View style={{ height: '100%', width: `${Math.min(100, (pontosEvento / META_EVENTO) * 100)}%`, backgroundColor: evento.cor, borderRadius: 99 }} /></View>
              <Text style={{ color: t.muted, fontWeight: '800', fontSize: 12 }}>{Math.min(pontosEvento, META_EVENTO)}/{META_EVENTO} pontos</Text>
            </View>
            {eventoPronto && !eventoResgatado && (
              <Pressable onPress={() => g.resgatarEvento()} accessibilityRole="button" accessibilityLabel={`Resgatar ${PREMIO_EVENTO} moedas do evento`} style={[styles.eventoBtn, { backgroundColor: t.sun, borderColor: t.sunDeep }]}>
                <Text style={{ color: t.sunInk, fontWeight: '900', fontSize: 12 }}>+{PREMIO_EVENTO}</Text>
              </Pressable>
            )}
            {eventoResgatado && <Icone nome="check" size={22} color={t.good} />}
          </View>
        )}
        {xp2 > 0 && <View style={[styles.boost, { backgroundColor: t.sun }]}><Icone nome="raio" size={18} color={t.sunInk} /><Text style={{ color: t.sunInk, fontWeight: '900' }}>XP em dobro ativo por mais {ate(xp2)}</Text></View>}

        {/* Revisão espaçada */}
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: nRev ? t.brand : t.line }]}>
          <View style={styles.row}>
            <IconeTile nome="cerebro" cor="#C2569F" size={46} />
            <View style={{ flex: 1 }}>
              <Text style={[styles.h2, { color: t.ink }]}>Revisão</Text>
              <Text style={[styles.sub, { color: t.muted }]}>
                {nRev ? `${nRev} ${nRev === 1 ? 'exercício que você errou volta' : 'exercícios que você errou voltam'} hoje. Acertou, ele demora mais para voltar.`
                  : totalRev ? `Tudo revisado! Próxima revisão ${prox && prox - Date.now() < 86400000 ? 'amanhã' : 'em breve'} (${totalRev} no baralho).`
                  : 'Quando você errar um exercício, ele volta aqui nos dias seguintes até ficar fácil.'}
              </Text>
            </View>
          </View>
          {nRev > 0 && <Button3D label={`Revisar agora (${Math.min(nRev, 10)})`} onPress={() => router.push('/lesson/revisao')} />}
        </View>

        {/* Missões do dia */}
        <View style={styles.secRow}>
          <Text style={[styles.sec, { color: t.ink }]}>Missões do dia</Text>
          <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}><Icone nome="ampulheta" size={14} color={t.muted} /><Text style={{ color: t.muted, fontWeight: '800' }}>{ate(fimDoDia.getTime() - Date.now())}</Text></View>
        </View>
        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line, gap: 16 }]}>
          {missoes.map((m) => {
            const v = Math.min(g.hoje?.c?.[m.evento] ?? 0, m.meta);
            const ok = v >= m.meta, pego = resgatadas.includes(m.id);
            return (
              <View key={m.id} style={styles.missao} accessibilityLabel={`${m.texto}: ${v} de ${m.meta}${pego ? ', resgatada' : ok ? ', pronta para resgatar' : ''}`}>
                <IconeTile nome={m.icone} cor={COR_EVENTO[m.evento] ?? '#2F6FD6'} size={42} />
                <View style={{ flex: 1, gap: 6 }}>
                  <Text style={[styles.mTexto, { color: t.ink }]}>{m.texto}</Text>
                  <View style={[styles.bar, { backgroundColor: t.line }]}>
                    <View style={[styles.fill, { width: `${(v / m.meta) * 100}%`, backgroundColor: ok ? t.good : t.sun }]} />
                    <Text style={[styles.barTxt, { color: t.ink }]}>{v}/{m.meta}</Text>
                  </View>
                </View>
                {pego ? <View style={styles.pego}><Icone nome="check" size={24} color={t.good} /></View>
                  : <Pressable disabled={!ok} onPress={() => g.resgatarMissao(m.id)} accessibilityRole="button" accessibilityLabel={`Resgatar ${m.moedas} moedas`}
                      style={[styles.premio, { backgroundColor: ok ? t.sun : t.bg, borderColor: ok ? t.sunDeep : t.line }]}>
                      <Moeda size={18} /><Text style={{ color: ok ? t.sunInk : t.muted, fontWeight: '900' }}>{ok ? `Pegar ${m.moedas}` : m.moedas}</Text>
                    </Pressable>}
              </View>
            );
          })}
        </View>

        <Bau prontos={resgatadas.length} aberto={g.hoje?.bau || bauAberto} abrir={() => setBauAberto(g.abrirBau())} />

        {/* Conquistas */}
        <View style={styles.secRow}>
          <Text style={[styles.sec, { color: t.ink }]}>Conquistas</Text>
          <Text style={{ color: t.muted, fontWeight: '800' }}>{nConq}/{CONQUISTAS.length}</Text>
        </View>
        <View style={styles.grid}>
          {CONQUISTAS.map((c) => {
            const tem = !!g.conquistas?.[c.id];
            const v = Math.min(c.valor(fonte), c.meta);
            return (
              <View key={c.id} style={[styles.conq, { backgroundColor: t.surface, borderColor: tem ? t.sun : t.line }]}
                accessibilityLabel={`${c.nome}: ${c.texto}. ${tem ? 'Conquistada' : `${v} de ${c.meta}`}`}>
                <IconeTile nome={c.icone} cor="#E0A21C" size={46} apagado={!tem} />
                <Text style={[styles.conqNome, { color: tem ? t.ink : t.muted }]} numberOfLines={2}>{c.nome}</Text>
                <Text style={[styles.conqTxt, { color: t.muted }]} numberOfLines={2}>{c.texto}</Text>
                {tem ? <View style={{ flexDirection: 'row', alignItems: 'center', gap: 3 }}><Icone nome="check" size={12} color={t.sunDeep} /><Text style={{ color: t.sunDeep, fontWeight: '900', fontSize: 12 }}>+{c.moedas}</Text></View>
                  : <View style={[styles.miniBar, { backgroundColor: t.line }]}><View style={[styles.fill, { width: `${(v / c.meta) * 100}%`, backgroundColor: t.brand }]} /></View>}
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

/** Baú do dia: libera com as 3 missões resgatadas e balança quando está pronto. */
function Bau({ prontos, aberto, abrir }: { prontos: number; aberto: number; abrir: () => void }) {
  const t = useTheme();
  const giro = useRef(new Animated.Value(0)).current;
  const pronto = prontos >= 3 && !aberto;
  useEffect(() => {
    if (!pronto) return;
    const a = Animated.loop(Animated.sequence([
      Animated.timing(giro, { toValue: 1, duration: 120, useNativeDriver: Platform.OS !== 'web' }),
      Animated.timing(giro, { toValue: -1, duration: 240, useNativeDriver: Platform.OS !== 'web' }),
      Animated.timing(giro, { toValue: 0, duration: 120, useNativeDriver: Platform.OS !== 'web' }),
      Animated.delay(900),
    ]));
    a.start();
    return () => a.stop();
  }, [pronto, giro]);
  return (
    <Pressable disabled={!pronto} onPress={abrir} accessibilityRole="button"
      accessibilityLabel={aberto ? `Baú aberto: ${aberto} moedas` : pronto ? 'Abrir o baú do dia' : `Baú do dia: resgate as 3 missões (${prontos} de 3)`}
      style={[styles.bau, { backgroundColor: pronto ? t.sun : t.surface, borderColor: pronto ? t.sunDeep : t.line }]}>
      <Animated.View style={{ transform: [{ rotate: giro.interpolate({ inputRange: [-1, 1], outputRange: ['-12deg', '12deg'] }) }] }}>
        <Icone nome={aberto ? 'tesouro' : 'bau-fechado'} size={54} color={pronto ? '#7A5300' : aberto ? t.sunDeep : t.muted} />
      </Animated.View>
      <View style={{ flex: 1 }}>
        <Text style={[styles.h2, { color: pronto ? t.sunInk : t.ink }]}>{aberto ? `+${aberto} moedas!` : 'Baú do dia'}</Text>
        <Text style={[styles.sub, { color: pronto ? t.sunInk : t.muted }]}>
          {aberto ? 'Volte amanhã para um baú novo.' : pronto ? 'Toque para abrir!' : `Resgate as 3 missões para abrir (${prontos}/3).`}
        </Text>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  evento: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 18, padding: 12 },
  eventoIco: { width: 46, height: 46, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  eventoBarra: { height: 10, borderRadius: 99, backgroundColor: 'rgba(120,135,150,0.25)', overflow: 'hidden' },
  eventoBtn: { borderWidth: 2, borderRadius: 12, paddingHorizontal: 10, paddingVertical: 8 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  h1: { fontSize: 26, fontWeight: '900' },
  moedas: { flexDirection: 'row', alignItems: 'center', gap: 6, borderWidth: 2, borderRadius: 14, paddingVertical: 5, paddingHorizontal: 10 },
  moedasN: { fontSize: 17, fontWeight: '900', fontVariant: ['tabular-nums'] },
  scroll: { padding: 16, paddingBottom: 60, gap: 16, maxWidth: 620, width: '100%', alignSelf: 'center', alignItems: 'stretch' },
  boost: { borderRadius: 12, padding: 10, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 6 },
  card: { borderWidth: 2, borderRadius: 18, padding: 16, gap: 12 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  big: { fontSize: 30 },
  h2: { fontSize: 18, fontWeight: '900' },
  sub: { fontSize: 14, fontWeight: '600', lineHeight: 19 },
  secRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'baseline', marginTop: 4 },
  sec: { fontSize: 20, fontWeight: '900' },
  missao: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  mTexto: { fontSize: 15, fontWeight: '800' },
  bar: { height: 18, borderRadius: 99, overflow: 'hidden', justifyContent: 'center' },
  fill: { position: 'absolute', left: 0, top: 0, bottom: 0, borderRadius: 99 },
  barTxt: { textAlign: 'center', fontSize: 11, fontWeight: '900', fontVariant: ['tabular-nums'] },
  premio: { flexDirection: 'row', alignItems: 'center', gap: 4, borderWidth: 2, borderBottomWidth: 4, borderRadius: 12, paddingVertical: 6, paddingHorizontal: 8, minWidth: 64, justifyContent: 'center' },
  pego: { width: 64, alignItems: 'center' },
  bau: { flexDirection: 'row', alignItems: 'center', gap: 14, borderWidth: 2, borderBottomWidth: 5, borderRadius: 18, padding: 16 },
  bauEmoji: { fontSize: 46 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  conq: { width: '31%', flexGrow: 1, minWidth: 100, borderWidth: 2, borderRadius: 16, padding: 10, alignItems: 'center', gap: 3 },
  conqEmoji: { fontSize: 30 },
  conqNome: { fontSize: 13, fontWeight: '900', textAlign: 'center' },
  conqTxt: { fontSize: 11, fontWeight: '600', textAlign: 'center' },
  miniBar: { height: 6, borderRadius: 99, overflow: 'hidden', alignSelf: 'stretch', marginTop: 4 },
});
