import { supabase } from './supabase';
import { contaDoPerfilAtivo } from './profiles';
import { useGame } from './store';

/** Envia o resultado de uma lição. Falhas de rede são ignoradas: o progresso local continua valendo. */
export async function pushLessonResult(lessonId: string | null, xp: number, accuracy: number) {
  if (!supabase || !contaDoPerfilAtivo()) return; // outros perfis do aparelho estudam offline
  const { data } = await supabase.auth.getUser();
  const user = data.user;
  if (!user) return;
  const s = useGame.getState();
  await Promise.allSettled([
    supabase.from('xp_events').insert({ user_id: user.id, amount: xp, lesson_id: lessonId }),
    lessonId
      ? supabase.from('lesson_progress').upsert({ user_id: user.id, lesson_id: lessonId, best_accuracy: s.done[lessonId] ?? accuracy })
      : Promise.resolve(),
    supabase.from('profiles').update({ xp: s.xp, streak: s.streak, last_day: s.lastDay }).eq('id', user.id),
  ]);
}

/** Depois do login: junta o que está na nuvem com o que está no aparelho. */
export async function pullProfile() {
  if (!supabase || !contaDoPerfilAtivo()) return; // outros perfis do aparelho estudam offline
  const { data: auth } = await supabase.auth.getUser();
  if (!auth.user) return;
  const [{ data: profile }, { data: progress }] = await Promise.all([
    supabase.from('profiles').select('display_name, avatar_seed, xp, streak, last_day, league, best_league').eq('id', auth.user.id).single(),
    supabase.from('lesson_progress').select('lesson_id, best_accuracy').eq('user_id', auth.user.id),
  ]);
  const done: Record<string, number> = {};
  progress?.forEach((p) => { done[p.lesson_id] = p.best_accuracy; });
  const local = useGame.getState();
  useGame.setState({ online: true });
  local.mergeRemote({
    name: profile?.display_name || local.name,
    avatarSeed: profile?.avatar_seed || local.avatarSeed,
    xp: profile?.xp ?? 0,
    streak: profile?.streak ?? 0,
    done,
    league: profile?.league ?? undefined,
    bestLeague: profile?.best_league ?? undefined,
  });
  const merged = useGame.getState();
  await supabase.from('profiles').update({
    display_name: merged.name, avatar_seed: merged.avatarSeed, xp: merged.xp, streak: merged.streak, last_day: merged.lastDay,
  }).eq('id', auth.user.id);
  if (Object.keys(merged.done).length) {
    await supabase.from('lesson_progress').upsert(
      Object.entries(merged.done).map(([lesson_id, best_accuracy]) => ({ user_id: auth.user!.id, lesson_id, best_accuracy })),
    );
  }
}

export async function saveProfileRemote() {
  if (!supabase || !contaDoPerfilAtivo()) return; // outros perfis do aparelho estudam offline
  const { data } = await supabase.auth.getUser();
  if (!data.user) return;
  const s = useGame.getState();
  await supabase.from('profiles').update({ display_name: s.name, avatar_seed: s.avatarSeed }).eq('id', data.user.id);
}


/** Com conta, o servidor fecha a semana; aqui buscamos o resultado ainda não visto. */
export async function checkLeagueResult() {
  if (!supabase || !contaDoPerfilAtivo()) return; // outros perfis do aparelho estudam offline
  const { data: auth } = await supabase.auth.getUser();
  if (!auth.user) return;
  const { data } = await supabase.from('league_history')
    .select('week_start, from_league, to_league, rank, xp')
    .eq('user_id', auth.user.id).eq('visto', false)
    .order('week_start', { ascending: false }).limit(1);
  const r = data?.[0];
  if (!r) return;
  await supabase.from('league_history').update({ visto: true }).eq('user_id', auth.user.id).eq('visto', false);
  useGame.setState((s) => ({
    league: r.to_league,
    bestLeague: Math.max(s.bestLeague, r.to_league),
    pendingResult: { week: r.week_start, from: r.from_league, to: r.to_league, rank: r.rank, xp: r.xp },
    history: [{ week: r.week_start, from: r.from_league, to: r.to_league, rank: r.rank, xp: r.xp }, ...s.history].slice(0, 30),
    medals: r.rank <= 3 && r.xp > 0
      ? { ...s.medals, [(['ouro', 'prata', 'bronze'] as const)[r.rank - 1]]: s.medals[(['ouro', 'prata', 'bronze'] as const)[r.rank - 1]] + 1 }
      : s.medals,
  }));
}
