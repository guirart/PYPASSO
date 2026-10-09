import type { User } from '@supabase/supabase-js';
import { router, useFocusEffect } from 'expo-router';
import { useCallback, useState } from 'react';
import { Linking, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { AvatarMoldura, CAST, CastFace, HostFace } from '@/components/Characters';
import { LESSONS_BY_TRACK } from '@/content';
import { Trophy } from '@/components/Trophy';
import { LEAGUES, leagueOf } from '@/lib/leagues';
import { usePlus } from '@/lib/plus';
import { useProfiles } from '@/lib/profiles';
import { useGame } from '@/lib/store';
import { supabase } from '@/lib/supabase';
import { saveProfileRemote } from '@/lib/sync';
import { deleteAccount } from '@/lib/account';
import { PRIVACY_URL } from '@/lib/privacidade';
import { useAparencia, useTheme, type Tema } from '@/lib/theme';
import { NivelBar } from '@/components/NivelBar';
import { Icone } from '@/components/Icone';
import { fmtHora, HORARIOS, useLembretes } from '@/lib/lembretes-prefs';
import { agendarLembretes, LEMBRETES_SUPORTADOS, pedirPermissao, testarLembrete } from '@/lib/lembretes';

/** Endereço público da política de privacidade (EXPO_PUBLIC_PRIVACY_URL no .env). */

export default function ProfileScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const [user, setUser] = useState<User | null>(null);
  const [confirmReset, setConfirmReset] = useState(false);
  const [del, setDel] = useState<'idle' | 'confirm' | 'busy' | 'done'>('idle');
  const [delMsg, setDelMsg] = useState<string | null>(null);

  useFocusEffect(useCallback(() => {
    supabase?.auth.getUser().then(({ data }) => setUser(data.user));
  }, []));

  const nPerfis = useProfiles((s) => s.perfis.length);
  const plus = usePlus((s) => s.ativo);
  const { tema, setTema } = useAparencia();
  const contaAqui = useProfiles((s) => { const dono = s.perfis.find((p) => p.conta); return !dono || dono.id === s.ativo; });
  const donoConta = useProfiles((s) => s.perfis.find((p) => p.conta)?.nome);

  return (
    <ScrollView style={{ backgroundColor: t.bg }} contentContainerStyle={[styles.wrap, { paddingTop: insets.top + 16 }]}>
      <View style={styles.hero}>
        <Pressable onPress={() => router.push('/avatar')} accessibilityLabel="Editar avatar">
          <AvatarMoldura seed={g.avatarSeed} size={112} moldura={g.moldura} />
          {plus && <View style={[styles.plusBadge, { flexDirection: 'row', alignItems: 'center', gap: 4 }]} accessibilityLabel="Assinante Plus"><Icone nome="diamante" size={14} color="#fff" /><Text style={{ color: '#fff', fontWeight: '900', fontSize: 12 }}>PLUS</Text></View>}
        </Pressable>
        <View style={{ flexDirection: 'row', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
          <Pressable onPress={() => router.push('/avatar')} accessibilityRole="button" style={[styles.editBtn, { borderColor: t.brand }]}>
            <Icone nome="lapis" size={15} color={t.brand} /><Text style={{ color: t.brand, fontWeight: '900' }}>Editar avatar</Text>
          </Pressable>
          <Pressable onPress={() => router.push('/personagem')} accessibilityRole="button" accessibilityLabel="Aparência do meu herói" style={[styles.editBtn, { borderColor: t.good }]}>
            <Icone nome="espada" size={16} color={t.good} /><Text style={{ color: t.good, fontWeight: '900' }}>Aparência</Text>
          </Pressable>
          <Pressable onPress={() => router.push('/perfis')} accessibilityRole="button" accessibilityLabel="Trocar perfil" style={[styles.editBtn, { borderColor: t.line }]}>
            <Icone nome="usuarios" size={16} color={t.ink} /><Text style={{ color: t.ink, fontWeight: '900' }}>Trocar perfil{nPerfis > 1 ? ` (${nPerfis})` : ''}</Text>
          </Pressable>
        </View>
      </View>

      <View style={{ gap: 6 }}>
        <Text style={[styles.label, { color: t.muted }]}>SEU NOME</Text>
        <TextInput
          value={g.name} placeholder="Como quer aparecer na liga" placeholderTextColor={t.muted}
          onChangeText={(name) => g.setProfile({ name })} onBlur={() => saveProfileRemote().catch(() => {})}
          style={[styles.input, { borderColor: t.line, backgroundColor: t.surface, color: t.ink }]}
        />
      </View>

      <NivelBar xp={g.xp} />

      <View style={styles.grid}>
        <Box label="Dias seguidos" value={g.streak} />
        <Box label="XP total" value={g.xp} />
        <Box label="Lições (do zero)" value={`${LESSONS_BY_TRACK.main.filter((l) => l.id in g.done).length}/${LESSONS_BY_TRACK.main.length}`} />
        <Box label="Built-ins" value={`${LESSONS_BY_TRACK.builtins.filter((l) => l.id in g.done).length}/${LESSONS_BY_TRACK.builtins.length}`} />
        <Box label="Bibliotecas" value={`${LESSONS_BY_TRACK.libs.filter((l) => l.id in g.done).length}/${LESSONS_BY_TRACK.libs.length}`} />
        <Box label="Vidas" value={plus ? '∞' : g.hearts} />
      </View>

      <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <Text style={[styles.h3, { color: t.ink }]}>Estante de troféus</Text>
        <Text style={{ color: t.muted, fontWeight: '600' }}>
          Você é <Text style={{ color: t.brand, fontWeight: '900' }}>{leagueOf(g.league).title}</Text> (Liga {leagueOf(g.league).gem}).
          {g.bestLeague > g.league ? ` Seu recorde: ${leagueOf(g.bestLeague).title}.` : ''}
        </Text>
        <View style={styles.shelf}>
          {LEAGUES.map((lg) => {
            const got = lg.tier <= Math.max(g.bestLeague, g.league);
            return (
              <View key={lg.tier} style={styles.shelfItem} accessibilityLabel={`${lg.title}${got ? ', conquistado' : ', ainda não conquistado'}`}>
                <Trophy tier={lg.tier} size={50} locked={!got} />
                <Text style={{ color: got ? t.ink : t.muted, fontSize: 11, fontWeight: '700', textAlign: 'center' }} numberOfLines={2}>{got ? lg.title : '???'}</Text>
              </View>
            );
          })}
        </View>
        <View style={styles.medals}>
          <Medalha cor="#E0A21C" n={g.medals?.ouro ?? 0} rotulo="ouro" />
          <Medalha cor="#8E99A4" n={g.medals?.prata ?? 0} rotulo="prata" />
          <Medalha cor="#B0703A" n={g.medals?.bronze ?? 0} rotulo="bronze" />
          <Text style={{ color: t.muted, fontSize: 12, flexBasis: '100%', textAlign: 'center' }}>medalhas por terminar a semana no pódio</Text>
        </View>
      </View>

      <Pressable onPress={() => router.push('/plus')} accessibilityRole="button" accessibilityLabel={plus ? 'Minha assinatura Plus' : 'Conhecer o PyPasso Plus'}
        style={[styles.card, { backgroundColor: '#5B3CC4', borderColor: '#35208A', flexDirection: 'row', alignItems: 'center', gap: 12 }]}>
        <Icone nome="diamante" size={36} color="#fff" />
        <View style={{ flex: 1 }}>
          <Text style={{ color: '#fff', fontWeight: '900', fontSize: 18 }}>{plus ? 'Você é Plus' : 'PyPasso Plus'}</Text>
          <Text style={{ color: 'rgba(255,255,255,0.9)', fontWeight: '700' }}>{plus ? 'Vidas ilimitadas em todos os perfis. Toque para gerenciar.' : 'Vidas ilimitadas. 7 dias grátis.'}</Text>
        </View>
        <Text style={{ color: '#FFC83D', fontWeight: '900', fontSize: 20 }}>›</Text>
      </Pressable>

      <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <Text style={[styles.h3, { color: t.ink }]}>Aparência</Text>
        <View style={[styles.temas, { borderColor: t.line, backgroundColor: t.bg }]} accessibilityRole="radiogroup">
          {([['auto', 'celular', 'Automático'], ['claro', 'sol', 'Claro'], ['escuro', 'lua', 'Escuro']] as [Tema, 'celular' | 'sol' | 'lua', string][]).map(([id, icone, nome]) => {
            const on = tema === id;
            return (
              <Pressable key={id} onPress={() => setTema(id)} accessibilityRole="radio" accessibilityState={{ checked: on }} accessibilityLabel={`Tema ${nome}`}
                style={[styles.tema, on && { backgroundColor: t.brand }]}>
                <Icone nome={icone} size={20} color={on ? '#fff' : t.muted} />
                <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '800', fontSize: 13 }}>{nome}</Text>
              </Pressable>
            );
          })}
        </View>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>
          {tema === 'auto' ? 'Segue o modo claro ou escuro do seu celular.' : 'Vale para todos os perfis deste aparelho.'}
        </Text>
      </View>

      <Lembretes />

      <Pressable onPress={() => router.push('/privacidade')} accessibilityRole="button" style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <View style={styles.tit}><Icone nome="cadeado" size={20} color={t.brand} /><Text style={[styles.h3, { color: t.ink }]}>Privacidade e dados</Text></View>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>Veja o que o app guarda, escolha o que compartilha, copie seus dados ou apague tudo. ›</Text>
      </Pressable>

      <Pressable onPress={() => router.push('/teste')} accessibilityRole="button" style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <View style={styles.tit}><Icone nome="frasco" size={20} color={t.brand} /><Text style={[styles.h3, { color: t.ink }]}>Teste com usuários</Text></View>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>
          Veja onde errou mais, onde desistiu e os relatos do botão "Travei aqui" nas lições. Copie o relatório para quem está testando o app. ›
        </Text>
      </Pressable>

      <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <Text style={[styles.h3, { color: t.ink }]}>Conta</Text>
        {!supabase && <Text style={{ color: t.muted, fontWeight: '600' }}>Seu progresso fica salvo neste aparelho.</Text>}
        {supabase && user && !contaAqui && (
          <Text style={{ color: t.muted, fontWeight: '600' }}>
            A conta {user.email} deste aparelho está no perfil {donoConta}. Este perfil estuda offline, na liga de treino. Para usar a conta, troque para o perfil {donoConta}.
          </Text>
        )}
        {supabase && user && contaAqui && (
          <>
            <Text style={{ color: t.muted, fontWeight: '600' }}>Conectado como {user.email}. Seu progresso é sincronizado entre web e celular.</Text>
            <Button3D label="Sair" variant="ghost" onPress={async () => { await supabase!.auth.signOut(); useGame.setState({ online: false }); setUser(null); }} />
            {del === 'idle' && (
              <Pressable onPress={() => { setDel('confirm'); setDelMsg(null); }} accessibilityLabel="Excluir minha conta">
                <Text style={{ color: t.bad, fontWeight: '700', textAlign: 'center' }}>Excluir minha conta</Text>
              </Pressable>
            )}
            {(del === 'confirm' || del === 'busy') && (
              <View style={{ gap: 10, borderWidth: 2, borderColor: t.bad, borderRadius: 14, padding: 12 }}>
                <Text style={{ color: t.ink, fontWeight: '700' }}>Excluir a conta apaga para sempre seu perfil, progresso, XP e posição na liga. Isso não pode ser desfeito.</Text>
                <Button3D label={del === 'busy' ? 'Excluindo…' : 'Sim, excluir minha conta'} variant="bad" disabled={del === 'busy'}
                  onPress={async () => { setDel('busy'); const r = await deleteAccount(); if (r.ok) { setDel('done'); setUser(null); } else { setDel('idle'); setDelMsg(r.message ?? null); } }} />
                <Button3D label="Cancelar" variant="ghost" disabled={del === 'busy'} onPress={() => setDel('idle')} />
              </View>
            )}
            {delMsg && <Text style={{ color: t.bad }}>{delMsg}</Text>}
          </>
        )}
        {del === 'done' && <Text style={{ color: t.good, fontWeight: '700' }}>Sua conta e seus dados foram excluídos.</Text>}
        {supabase && !user && (
          <>
            <Text style={{ color: t.muted, fontWeight: '600' }}>Entre para salvar o progresso na nuvem e competir na liga.</Text>
            <Button3D label="Entrar ou criar conta" onPress={() => router.push('/login')} />
          </>
        )}
      </View>

      <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
        <Text style={[styles.h3, { color: t.ink }]}>Elenco</Text>
        <View style={styles.cast}>
          <View style={styles.castItem}><HostFace host="pipo" size={56} /><Text style={[styles.castName, { color: t.ink }]}>Pipo</Text></View>
          {(Object.keys(CAST) as (keyof typeof CAST)[]).map((id) => (
            <View key={id} style={styles.castItem}><CastFace id={id} size={56} /><Text style={[styles.castName, { color: t.ink }]}>{CAST[id].name}</Text></View>
          ))}
        </View>
        <Text style={{ color: t.muted, fontSize: 13 }}>
          Personagens e avatares: estilo “Critters” do DiceBear, em domínio público (CC0 1.0).
        </Text>
        <Pressable onPress={() => Linking.openURL('https://www.dicebear.com/styles/critters/')}>
          <Text style={{ color: t.brand, fontWeight: '700', fontSize: 13 }}>dicebear.com/styles/critters</Text>
        </Pressable>
        <Text style={{ color: t.muted, fontSize: 13 }}>
          Ícones do mapa, chefes e relíquias: Lorc, Delapouite e outros autores do game-icons.net (CC BY 3.0). Ícones da interface: Phosphor Icons (MIT).
        </Text>
        <Text style={{ color: t.muted, fontSize: 13 }}>
          Inimigos das batalhas: Tiny RPG Character Asset Pack 02 (pixel art). Personagem das batalhas: Mana Seed Character Base (demo), de Seliel the Shaper. Cenários das batalhas: Luis Zuno (@ansimuz), via OpenGameArt (GothicVania Cemetery, CC-BY 3.0; Junk Wasteland, Mountain at Dusk e Forest Background, CC0). Ícones dos itens: Raven Fantasy Icons. Barras de vida, corações e molduras do inventário: Crimson Fantasy GUI. Fundos de castelo do mapa e das lutas de chefe: Craftpix (Free Castle Interior Pixel Game Backgrounds).
        </Text>
        <Pressable onPress={() => Linking.openURL('https://game-icons.net')}>
          <Text style={{ color: t.brand, fontWeight: '700', fontSize: 13 }}>game-icons.net</Text>
        </Pressable>
      </View>

      {PRIVACY_URL ? (
        <Pressable onPress={() => Linking.openURL(PRIVACY_URL)} accessibilityRole="link">
          <Text style={{ color: t.brand, fontWeight: '700', textAlign: 'center' }}>Política de privacidade</Text>
        </Pressable>
      ) : null}

      <Pressable onPress={() => { if (!confirmReset) { setConfirmReset(true); setTimeout(() => setConfirmReset(false), 3000); return; } g.reset(); setConfirmReset(false); }}>
        <Text style={{ color: confirmReset ? t.bad : t.muted, fontWeight: '700', textAlign: 'center', textDecorationLine: 'underline' }}>
          {confirmReset ? 'Toque de novo para apagar o progresso deste aparelho' : 'Zerar progresso'}
        </Text>
      </Pressable>
    </ScrollView>
  );
}

function Box({ label, value }: { label: string; value: string | number }) {
  const t = useTheme();
  return (
    <View style={[styles.box, { borderColor: t.line, backgroundColor: t.surface }]}>
      <Text style={[styles.boxV, { color: t.ink }]}>{value}</Text>
      <Text style={{ color: t.muted, fontWeight: '700' }}>{label}</Text>
    </View>
  );
}

/** Lembrete diário para não perder a sequência (no app do celular). */
function Lembretes() {
  const t = useTheme();
  const { ativo, hora, minuto, set } = useLembretes();
  const [aviso, setAviso] = useState('');
  const ligar = async (v: boolean) => {
    if (v && !(await pedirPermissao())) { setAviso('O celular não deu permissão para notificações. Libere nas configurações do aparelho.'); return; }
    set({ ativo: v }); setAviso(''); await agendarLembretes();
  };
  const escolher = async (h: number, m: number) => { set({ hora: h, minuto: m }); await agendarLembretes(); };
  return (
    <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
      <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
        <View style={styles.tit}><Icone nome="sino" size={20} color={t.brand} /><Text style={[styles.h3, { color: t.ink }]}>Lembretes</Text></View>
        {LEMBRETES_SUPORTADOS && (
          <Pressable onPress={() => ligar(!ativo)} accessibilityRole="switch" accessibilityState={{ checked: ativo }} accessibilityLabel="Lembrete diário"
            style={[styles.switch, { backgroundColor: ativo ? t.good : t.line }]}>
            <View style={[styles.knob, { alignSelf: ativo ? 'flex-end' : 'flex-start' }]} />
          </Pressable>
        )}
      </View>
      {LEMBRETES_SUPORTADOS ? (
        <>
          <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>
            {ativo ? `Todo dia às ${fmtHora(hora, minuto)} o Pipo lembra você, a não ser que já tenha estudado.` : 'O Pipo avisa na hora que você escolher se você ainda não estudou no dia.'}
          </Text>
          {ativo && (
            <View style={styles.horas}>
              {HORARIOS.map(([h, m]) => {
                const on = h === hora && m === minuto;
                return (
                  <Pressable key={`${h}${m}`} onPress={() => escolher(h, m)} accessibilityRole="radio" accessibilityState={{ checked: on }}
                    style={[styles.hora, { borderColor: on ? t.brand : t.line, backgroundColor: on ? t.brand : t.bg }]}>
                    <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '800' }}>{fmtHora(h, m)}</Text>
                  </Pressable>
                );
              })}
            </View>
          )}
          {ativo && <Pressable onPress={() => testarLembrete().then((ok) => setAviso(ok ? 'Pronto! O lembrete de teste chega em 5 segundos.' : 'Sem permissão para notificações.'))}>
            <Text style={{ color: t.brand, fontWeight: '800' }}>Testar agora</Text>
          </Pressable>}
        </>
      ) : (
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>Os lembretes diários funcionam no app para celular (Android e iPhone). No navegador não dá para avisar com o site fechado.</Text>
      )}
      {!!aviso && <Text style={{ color: t.sunDeep, fontWeight: '700', fontSize: 13 }}>{aviso}</Text>}
    </View>
  );
}

/** Medalha de pódio desenhada (sem emoji). */
function Medalha({ cor, n, rotulo }: { cor: string; n: number; rotulo: string }) {
  const t = useTheme();
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }} accessibilityLabel={`${n} medalhas de ${rotulo}`}>
      <View style={{ width: 26, height: 26, borderRadius: 13, backgroundColor: cor, borderWidth: 3, borderColor: 'rgba(255,255,255,0.6)', alignItems: 'center', justifyContent: 'center' }}><Icone nome="estrela" size={12} color="#fff" /></View>
      <Text style={[styles.medal, { color: t.ink }]}>{n}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  tit: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  switch: { width: 52, height: 30, borderRadius: 99, padding: 3, justifyContent: 'center' },
  knob: { width: 24, height: 24, borderRadius: 12, backgroundColor: '#fff' },
  horas: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  hora: { borderWidth: 2, borderRadius: 12, paddingVertical: 6, paddingHorizontal: 12 },
  wrap: { padding: 16, paddingBottom: 60, gap: 20, maxWidth: 620, width: '100%', alignSelf: 'center' },
  hero: { alignItems: 'center', gap: 8 },
  temas: { flexDirection: 'row', borderWidth: 2, borderRadius: 14, padding: 4, gap: 4 },
  tema: { flex: 1, alignItems: 'center', borderRadius: 10, paddingVertical: 8, gap: 2 },
  plusBadge: { position: 'absolute', bottom: -6, alignSelf: 'center', backgroundColor: '#5B3CC4', color: '#FFC83D', fontWeight: '900', fontSize: 12, paddingHorizontal: 10, paddingVertical: 3, borderRadius: 99, overflow: 'hidden' },
  editBtn: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 14, paddingVertical: 6 },
  label: { fontSize: 12, fontWeight: '800', letterSpacing: 1 },
  input: { borderWidth: 2, borderRadius: 14, paddingVertical: 12, paddingHorizontal: 14, fontSize: 17, fontWeight: '700' },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  box: { flexGrow: 1, flexBasis: '45%', borderWidth: 2, borderRadius: 16, padding: 14, gap: 2 },
  boxV: { fontSize: 24, fontWeight: '900', fontVariant: ['tabular-nums'] },
  card: { borderWidth: 2, borderRadius: 18, padding: 16, gap: 12 },
  h3: { fontSize: 19, fontWeight: '900' },
  cast: { flexDirection: 'row', flexWrap: 'wrap', gap: 14 },
  castItem: { alignItems: 'center', gap: 4 },
  castName: { fontWeight: '800' },
  shelf: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between', rowGap: 10 },
  shelfItem: { width: '19%', minWidth: 58, alignItems: 'center', gap: 2 },
  medals: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center', gap: 18 },
  medal: { fontSize: 20, fontWeight: '900', fontVariant: ['tabular-nums'] },
});
