import { Modal, StyleSheet, Text, View } from 'react-native';
import { leagueOf } from '@/lib/leagues';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';
import { Button3D } from './Button3D';
import { Mascot } from './Characters';
import { Trophy } from './Trophy';

/** Tela que aparece quando a semana da liga termina. */
export function LeagueResult() {
  const t = useTheme();
  const res = useGame((s) => s.pendingResult);
  const dismiss = useGame((s) => s.dismissResult);
  if (!res) return null;
  const up = res.to > res.from, down = res.to < res.from;
  const L = leagueOf(res.to);
  const title = up ? `Você subiu para a Liga ${L.gem}!` : down ? `Você caiu para a Liga ${L.gem}` : `Você continua na Liga ${L.gem}`;
  const sub = up ? `Agora você é ${L.title}!` : down ? `De volta a ${L.title}. Semana que vem você recupera!` : `Você ainda é ${L.title}.`;
  return (
    <Modal transparent animationType="fade" visible onRequestClose={dismiss}>
      <View style={styles.back}>
        <View style={[styles.card, { backgroundColor: t.surface }]}>
          <View style={[styles.top, { backgroundColor: L.hero }]}>
            <Trophy tier={res.to} size={140} celebrate={up} locked={false} />
          </View>
          <View style={styles.body}>
            <Text style={[styles.title, { color: t.ink }]}>{title}</Text>
            <Text style={[styles.sub, { color: t.brand }]}>{sub}</Text>
            <Text style={[styles.joke, { color: t.muted }]}>“{L.joke}”</Text>
            <View style={styles.pipo}>
              <Mascot size={56} mood={up ? 'cheer' : down ? 'sad' : 'happy'} />
              <Text style={[styles.stat, { color: t.ink }]}>
                Você terminou a semana em {res.rank}º lugar com {res.xp} XP.
                {res.rank <= 3 && res.xp > 0 ? ` Ganhou uma medalha de ${['ouro', 'prata', 'bronze'][res.rank - 1]}!` : ''}
              </Text>
            </View>
            <Button3D label={up ? 'Bora pra próxima!' : 'Continuar'} onPress={dismiss} style={{ alignSelf: 'stretch' }} />
          </View>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  back: { flex: 1, backgroundColor: 'rgba(0,0,0,0.55)', alignItems: 'center', justifyContent: 'center', padding: 20 },
  card: { width: '100%', maxWidth: 400, borderRadius: 24, overflow: 'hidden' },
  top: { alignItems: 'center', paddingVertical: 22 },
  body: { padding: 20, gap: 10, alignItems: 'center' },
  title: { fontSize: 22, fontWeight: '900', textAlign: 'center' },
  sub: { fontSize: 17, fontWeight: '800', textAlign: 'center' },
  joke: { fontSize: 14, fontStyle: 'italic', textAlign: 'center' },
  pipo: { flexDirection: 'row', alignItems: 'center', gap: 10, marginVertical: 6 },
  stat: { flex: 1, fontSize: 14, fontWeight: '600' },
});
