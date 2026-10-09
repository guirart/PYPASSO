import { router, useFocusEffect } from 'expo-router';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Avatar, CastFace, Mascot } from '@/components/Characters';
import { Trophy } from '@/components/Trophy';
import {
  DEMOTE, GROUP_SIZE, LEAGUES, PROMOTE, leagueOf, pipoLeagueLine, rivalsFor, standings, timeLeft, weekId, zoneOf, type Rival,
} from '@/lib/leagues';
import { useGame } from '@/lib/store';
import { supabase } from '@/lib/supabase';
import { useTheme } from '@/lib/theme';

export default function LeagueScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { name, avatarSeed, weekXP, league, bestLeague, tick } = useGame();
  const [online, setOnline] = useState<Rival[] | null>(null);
  const [now, setNow] = useState(Date.now());
  const ladderRef = useRef<ScrollView>(null);
  const L = leagueOf(league);

  useFocusEffect(useCallback(() => {
    tick();
    setNow(Date.now());
    let alive = true;
    (async () => {
      const user = supabase ? (await supabase.auth.getUser()).data.user : null;
      if (!supabase || !user) { setOnline(null); return; }
      const { data, error } = await supabase.from('weekly_leaderboard')
        .select('user_id, display_name, avatar_seed, week_xp').eq('league', league).limit(50);
      if (!alive) return;
      if (error || !data) { setOnline(null); return; }
      setOnline(data.map((r) => ({ id: r.user_id, name: r.display_name || 'Sem nome', seed: r.avatar_seed || r.user_id, xp: r.week_xp, me: r.user_id === user.id })));
    })();
    const id = setInterval(() => setNow(Date.now()), 60_000);
    return () => { alive = false; clearInterval(id); };
  }, [league, tick]));

  // Sem conta: liga de treino com rivais cujo XP cresce durante a semana
  const table = useMemo<Rival[]>(() => {
    if (online && online.length > 1) return [...online].sort((a, b) => b.xp - a.xp);
    return standings(rivalsFor(weekId(new Date(now)), league), { name: name || 'Você', seed: avatarSeed, xp: weekXP });
  }, [online, now, league, name, avatarSeed, weekXP]);
  const myRank = Math.max(1, table.findIndex((r) => r.me) + 1);
  const size = table.length;

  useEffect(() => {
    const x = Math.max(0, (league - 2) * 84);
    setTimeout(() => ladderRef.current?.scrollTo({ x, animated: false }), 50);
  }, [league]);

  return (
    <ScrollView style={{ backgroundColor: t.bg }} contentContainerStyle={[styles.wrap, { paddingTop: insets.top + 12 }]}>
      {/* Cabeçalho da liga */}
      <View style={[styles.hero, { backgroundColor: L.hero }]}>
        <View style={[styles.heroGlow, { backgroundColor: L.c1 }]} />
        <Trophy tier={league} size={118} celebrate />
        <View style={{ flex: 1, gap: 2 }}>
          <Text style={styles.eyebrow}>LIGA {L.gem.toUpperCase()} · NÍVEL {league} DE {LEAGUES.length}</Text>
          <Text style={styles.heroTitle}>{L.title}</Text>
          <Text style={styles.heroJoke}>{L.joke}</Text>
          <View style={styles.timer}><Text style={styles.timerTxt}>⏱ Termina em {timeLeft(new Date(now))}</Text></View>
        </View>
      </View>

      {/* Trilha das ligas */}
      <ScrollView ref={ladderRef} horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.ladder}>
        {LEAGUES.map((lg) => {
          const cur = lg.tier === league;
          const unlocked = lg.tier <= Math.max(bestLeague, league);
          return (
            <View key={lg.tier} style={[styles.step, cur && { borderColor: lg.c2, backgroundColor: t.surface }]}
              accessibilityLabel={`Liga ${lg.gem}, ${lg.title}${cur ? ', sua liga atual' : unlocked ? ', conquistada' : ', bloqueada'}`}>
              <Trophy tier={lg.tier} size={cur ? 58 : 46} locked={!unlocked} />
              <Text style={[styles.stepTxt, { color: unlocked ? t.ink : t.muted, fontWeight: cur ? '900' : '700' }]} numberOfLines={2}>{lg.title}</Text>
            </View>
          );
        })}
      </ScrollView>

      {/* Comentário do Pipo */}
      <View style={styles.pipoRow}>
        <Mascot size={58} mood={zoneOf(myRank, league, size) === 'demo' ? 'sad' : myRank <= PROMOTE ? 'cheer' : 'think'} />
        <View style={[styles.bubble, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.ink, fontWeight: '700', fontSize: 15, lineHeight: 21 }}>{pipoLeagueLine(myRank, league, table)}</Text>
        </View>
      </View>

      {!online && (
        <Text style={{ color: t.muted, fontSize: 13 }}>
          {supabase ? 'Liga de treino com a turma do PyPasso. Entre na sua conta para disputar com outras pessoas.' : 'Liga de treino com a turma do PyPasso: ganhe XP nas lições e passe todo mundo!'}
        </Text>
      )}
      {!online && supabase && <Button3D label="Entrar e jogar com pessoas" variant="ghost" onPress={() => router.push('/login')} />}

      {/* Classificação */}
      <View style={{ gap: 8 }}>
        {table.map((r, i) => {
          const rank = i + 1;
          const zone = zoneOf(rank, league, size);
          const showPromo = rank === PROMOTE + 1 && league < LEAGUES.length && size > PROMOTE;
          const showDemo = rank === size - DEMOTE + 1 && league > 1 && size > DEMOTE + PROMOTE;
          return (
            <View key={r.id} style={{ gap: 8 }}>
              {showPromo && <Divider color={t.good} label={`▲ Os ${PROMOTE} de cima sobem para ${leagueOf(league + 1).title}`} />}
              {showDemo && <Divider color={t.bad} label={`▼ Os ${DEMOTE} de baixo caem para ${leagueOf(league - 1).title}`} />}
              <View style={[styles.row, {
                backgroundColor: r.me ? t.brandSoft : t.surface,
                borderColor: r.me ? t.brand : zone === 'promo' ? t.good : zone === 'demo' ? t.bad : t.line,
                borderLeftWidth: zone === 'safe' && !r.me ? 2 : 5,
              }]}>
                {rank <= 3 ? (
                  <View style={[styles.pos, { alignItems: 'center' }]} accessibilityLabel={`${rank}º lugar`}>
                    <View style={{ width: 26, height: 26, borderRadius: 13, backgroundColor: ['#E0A21C', '#8E99A4', '#B0703A'][rank - 1], borderWidth: 3, borderColor: 'rgba(255,255,255,0.6)', alignItems: 'center', justifyContent: 'center' }}>
                      <Text style={{ color: '#fff', fontWeight: '900', fontSize: 12 }}>{rank}</Text>
                    </View>
                  </View>
                ) : (
                  <Text style={[styles.pos, { color: t.muted }]}>{rank}</Text>
                )}
                {r.cast ? <CastFace id={r.cast} size={42} /> : <Avatar seed={r.seed} size={42} />}
                <Text style={[styles.name, { color: t.ink }]} numberOfLines={1}>{r.name}{r.me ? ' (você)' : ''}</Text>
                <Text style={[styles.xp, { color: r.me ? t.brand : t.muted }]}>{r.xp} XP</Text>
              </View>
            </View>
          );
        })}
      </View>
      <Text style={{ color: t.muted, fontSize: 12, textAlign: 'center' }}>
        {GROUP_SIZE} pessoas por liga. Toda segunda-feira começa uma semana nova.
      </Text>
    </ScrollView>
  );
}

function Divider({ color, label }: { color: string; label: string }) {
  return (
    <View style={styles.divider}>
      <View style={[styles.line, { backgroundColor: color }]} />
      <Text style={[styles.divTxt, { color }]}>{label}</Text>
      <View style={[styles.line, { backgroundColor: color }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { padding: 16, paddingBottom: 48, gap: 16, maxWidth: 620, width: '100%', alignSelf: 'center' },
  hero: { flexDirection: 'row', alignItems: 'center', gap: 14, borderRadius: 22, padding: 16, overflow: 'hidden' },
  heroGlow: { position: 'absolute', width: 220, height: 220, borderRadius: 110, left: -60, top: -50, opacity: 0.35 },
  eyebrow: { color: 'rgba(255,255,255,0.85)', fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  heroTitle: { color: '#fff', fontSize: 27, fontWeight: '900', lineHeight: 31 },
  heroJoke: { color: 'rgba(255,255,255,0.92)', fontSize: 14, fontWeight: '600', fontStyle: 'italic' },
  timer: { alignSelf: 'flex-start', marginTop: 6, backgroundColor: 'rgba(0,0,0,0.22)', borderRadius: 99, paddingHorizontal: 10, paddingVertical: 4 },
  timerTxt: { color: '#fff', fontWeight: '800', fontSize: 12 },
  ladder: { gap: 8, paddingVertical: 4 },
  step: { width: 76, alignItems: 'center', gap: 4, paddingVertical: 8, paddingHorizontal: 4, borderRadius: 14, borderWidth: 2, borderColor: 'transparent' },
  stepTxt: { fontSize: 11, textAlign: 'center', lineHeight: 13 },
  pipoRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 10 },
  bubble: { flex: 1, borderWidth: 2, borderRadius: 16, paddingVertical: 10, paddingHorizontal: 12 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, paddingVertical: 8, paddingHorizontal: 12 },
  pos: { width: 28, fontWeight: '900', fontSize: 17, textAlign: 'center', fontVariant: ['tabular-nums'] },
  name: { flex: 1, fontWeight: '800', fontSize: 16 },
  xp: { fontWeight: '800', fontVariant: ['tabular-nums'] },
  divider: { flexDirection: 'row', alignItems: 'center', gap: 8, marginVertical: 2 },
  line: { flex: 1, height: 2, borderRadius: 2, opacity: 0.6 },
  divTxt: { fontSize: 12, fontWeight: '900', textAlign: 'center', flexShrink: 1 },
});
