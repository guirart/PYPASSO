import { router } from 'expo-router';
import { ScrollView, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { Cross } from '@/components/Icons';
import { exercicioPorId } from '@/content';
import { serieAtual } from '@/lib/desafio';
import { eventoDaSemana, META_EVENTO } from '@/lib/evento';
import { weekId } from '@/lib/leagues';
import { metaDiaria } from '@/lib/metas';
import { dayKey, useGame, yesterdayKey } from '@/lib/store';
import { useTheme } from '@/lib/theme';

const DIAS = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D'];

/** Resumo da semana: o que foi estudado, onde mais errou e o que o Pipo recomenda. Tudo calculado no aparelho. */
export default function ResumoScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const semId = weekId();
  const sem = g.sem?.id === semId ? g.sem : { id: semId, licoes: 0, dias: [] as string[], precSoma: 0, precN: 0 };
  const [y, m, d] = semId.split('-').map(Number);
  const dias = Array.from({ length: 7 }, (_, i) => { const x = new Date(y, m - 1, d + i); return { chave: `${x.getFullYear()}-${x.getMonth() + 1}-${x.getDate()}`, ehHoje: i === (new Date().getDay() + 6) % 7 }; });
  const precisao = sem.precN ? Math.round(sem.precSoma / sem.precN) : null;
  const duelos = Object.values(g.duelos ?? {}).reduce((s, r) => ({ v: s.v + r.v, d: s.d + r.d }), { v: 0, d: 0 });
  const serieDesafio = serieAtual(g.desafio, dayKey(), yesterdayKey());
  const evento = eventoDaSemana(semId);
  const pontosEvento = g.evento?.semana === semId ? g.evento.pontos : 0;

  // Onde mais errou: soma dos erros por lição, vindos da Revisão espaçada
  const porLicao = new Map<string, number>();
  for (const [id, c] of Object.entries(g.revisao ?? {})) {
    const l = exercicioPorId(id)?.lesson.title;
    if (l && c.erros > 0) porLicao.set(l, (porLicao.get(l) ?? 0) + c.erros);
  }
  const dificeis = [...porLicao.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3);

  const mood = sem.dias.length >= 4 ? 'cheer' : sem.dias.length === 0 ? 'sad' : 'happy';
  const recomenda = sem.dias.length === 0
    ? 'Você ainda não estudou nesta semana. Comece pelo Desafio do dia: é rápido e já conta na sua sequência.'
    : dificeis.length
      ? `Eu revisaria “${dificeis[0][0]}” primeiro: é onde você mais errou (${dificeis[0][1]} ${dificeis[0][1] === 1 ? 'erro' : 'erros'}).`
      : sem.dias.length < 3
        ? 'Bom começo! Estudar um pouquinho em mais dias vale mais do que muito em um dia só.'
        : 'Semana consistente! Que tal tentar um duelo ou uma Prova de fogo para testar o que aprendeu?';

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Resumo da semana</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]}>
        <View style={[styles.pipo, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Mascot size={70} mood={mood} />
          <Text style={{ color: t.ink, fontWeight: '800', lineHeight: 21, flex: 1 }}>{recomenda}</Text>
        </View>

        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={[styles.rot, { color: t.muted }]}>DIAS ESTUDADOS</Text>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between' }}>
            {dias.map((x, i) => {
              const fez = sem.dias.includes(x.chave);
              return (
                <View key={i} style={{ alignItems: 'center', gap: 4 }} accessibilityLabel={`${DIAS[i]}: ${fez ? 'estudou' : 'não estudou'}`}>
                  <View style={[styles.dia, { backgroundColor: fez ? t.good : t.line, borderColor: x.ehHoje ? t.brand : 'transparent' }]} />
                  <Text style={{ color: x.ehHoje ? t.brand : t.muted, fontWeight: '900', fontSize: 12 }}>{DIAS[i]}</Text>
                </View>
              );
            })}
          </View>
          <Text style={{ color: t.ink, fontWeight: '800' }}>{sem.dias.length} de 7 dias · sequência de {g.streak} {g.streak === 1 ? 'dia' : 'dias'}</Text>
        </View>

        <View style={styles.grade}>
          <Box t={t} rot="XP DA SEMANA" valor={String(g.weekXP ?? 0)} />
          <Box t={t} rot="LIÇÕES" valor={String(sem.licoes)} />
          <Box t={t} rot="PRECISÃO" valor={precisao === null ? '-' : `${precisao}%`} />
          <Box t={t} rot="DUELOS" valor={`${duelos.v}V ${duelos.d}D`} />
          <Box t={t} rot="DESAFIO DO DIA" valor={serieDesafio ? `${serieDesafio} seguidos` : '-'} />
          <Box t={t} rot={evento.nome.toUpperCase()} valor={`${Math.min(pontosEvento, META_EVENTO)}/${META_EVENTO}`} />
        </View>

        <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={[styles.rot, { color: t.muted }]}>ONDE VOCÊ MAIS ERROU</Text>
          {dificeis.length ? dificeis.map(([titulo, n]) => (
            <View key={titulo} style={{ flexDirection: 'row', justifyContent: 'space-between', gap: 8 }}>
              <Text style={{ color: t.ink, fontWeight: '800', flex: 1 }}>{titulo}</Text>
              <Text style={{ color: t.bad, fontWeight: '900' }}>{n} {n === 1 ? 'erro' : 'erros'}</Text>
            </View>
          )) : <Text style={{ color: t.muted, fontWeight: '600' }}>Nenhum erro guardado na Revisão. Ótimo sinal!</Text>}
          {dificeis.length > 0 && <Button3D label="Revisar agora" onPress={() => router.replace('/lesson/revisao')} />}
        </View>

        <Text style={{ color: t.muted, fontSize: 13, lineHeight: 18 }}>
          Sua meta diária está em {metaDiaria(g.xpDias, dayKey())} XP, calculada pela média dos seus últimos dias de estudo.
        </Text>
      </ScrollView>
    </View>
  );
}

function Box({ t, rot, valor }: { t: ReturnType<typeof useTheme>; rot: string; valor: string }) {
  return (
    <View style={[styles.box, { backgroundColor: t.surface, borderColor: t.line }]}>
      <Text style={{ color: t.ink, fontWeight: '900', fontSize: 20, fontVariant: ['tabular-nums'] }}>{valor}</Text>
      <Text style={[styles.rot, { color: t.muted }]} numberOfLines={2}>{rot}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 640, width: '100%', alignSelf: 'center' },
  pipo: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 18, padding: 12 },
  card: { borderWidth: 2, borderRadius: 16, padding: 14, gap: 10 },
  rot: { fontWeight: '900', fontSize: 11, letterSpacing: 0.8 },
  dia: { width: 30, height: 30, borderRadius: 15, borderWidth: 3 },
  grade: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  box: { flexGrow: 1, flexBasis: '30%', minWidth: 96, borderWidth: 2, borderRadius: 14, padding: 12, gap: 2 },
});
