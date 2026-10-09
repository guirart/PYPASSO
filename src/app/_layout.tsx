import { DarkTheme, DefaultTheme, router, Stack, ThemeProvider } from 'expo-router';
import { useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import * as SystemUI from 'expo-system-ui';
import { useTheme, useEscuro } from '@/lib/theme';
import { LeagueResult } from '@/components/LeagueResult';
import { AvisosHost } from '@/components/Avisos';
import { agendarLembretes } from '@/lib/lembretes';
import { PythonHost, warmUpPython } from '@/lib/python/runner';
import { LEGACY_IDS } from '@/content';
import { atualizarPlus, ligarContaNaLoja } from '@/lib/plus';
import { contaDoPerfilAtivo, iniciarPerfis, perfisProntos, useProfiles } from '@/lib/profiles';
import { useGame } from '@/lib/store';
import { checkLeagueResult, pullProfile } from '@/lib/sync';
import { supabase } from '@/lib/supabase';

export default function RootLayout() {
  const escuro = useEscuro();
  const t = useTheme();
  // Fundo da janela (aparece atrás das telas e no teclado) acompanha o tema escolhido.
  useEffect(() => { SystemUI.setBackgroundColorAsync(t.bg).catch(() => {}); }, [t.bg]);
  const tick = useGame((s) => s.tick);

  useEffect(() => {
    let vivo = true;
    let unPerfil: (() => void) | undefined;
    let sub: { data: { subscription: { unsubscribe: () => void } } } | undefined;
    const id = setInterval(() => useGame.getState().tick(), 60_000);
    warmUpPython();
    // Depois que tudo carregar: perfis (último perfil usado), ids antigos e conta online.
    perfisProntos().then(async () => {
      unPerfil = await iniciarPerfis();
      if (!vivo) return;
      useGame.getState().migrateIds(LEGACY_IDS);
      tick();
      useGame.getState().verificar();
      agendarLembretes();
      const { perfis, perguntar } = useProfiles.getState();
      if (perfis.length > 1 && perguntar) setTimeout(() => router.push('/perfis'), 0);
      atualizarPlus().catch(() => {});
      sub = supabase?.auth.onAuthStateChange((event, session) => {
        const pf = useProfiles.getState();
        // A compra na loja fica ligada à conta: assim o Plus vale na web e no celular.
        if (event === 'SIGNED_IN' || event === 'INITIAL_SESSION') ligarContaNaLoja(session?.user.id ?? null);
        if (event === 'SIGNED_OUT') ligarContaNaLoja(null);
        if (event === 'SIGNED_IN' && !pf.perfis.some((p) => p.conta)) pf.ligarConta(pf.ativo);
        if (event === 'SIGNED_OUT') pf.ligarConta(null);
        if ((event === 'SIGNED_IN' || event === 'INITIAL_SESSION') && contaDoPerfilAtivo()) pullProfile().then(checkLeagueResult).catch(() => {});
      });
    });
    return () => { vivo = false; clearInterval(id); unPerfil?.(); sub?.data.subscription.unsubscribe(); };
  }, [tick]);

  return (
    <ThemeProvider value={escuro
      ? { ...DarkTheme, colors: { ...DarkTheme.colors, background: t.bg, card: t.bg, border: t.line, text: t.ink, primary: t.brand } }
      : { ...DefaultTheme, colors: { ...DefaultTheme.colors, background: t.bg, card: t.bg, border: t.line, text: t.ink, primary: t.brand } }}>
      <StatusBar style={escuro ? 'light' : 'dark'} />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="lesson/[id]" options={{ presentation: 'fullScreenModal', gestureEnabled: false }} />
        <Stack.Screen name="login" options={{ presentation: 'modal' }} />
        <Stack.Screen name="biblioteca/[id]" />
        <Stack.Screen name="avatar" options={{ presentation: 'modal' }} />
        <Stack.Screen name="especial/[id]" options={{ presentation: 'fullScreenModal', gestureEnabled: false }} />
        <Stack.Screen name="perfis" options={{ presentation: 'fullScreenModal' }} />
        <Stack.Screen name="plus" options={{ presentation: 'modal' }} />
        <Stack.Screen name="prova" options={{ presentation: 'fullScreenModal', gestureEnabled: false }} />
        <Stack.Screen name="loja" options={{ presentation: 'modal' }} />
        <Stack.Screen name="missoes" options={{ presentation: 'modal' }} />
        <Stack.Screen name="privacidade" options={{ presentation: 'modal' }} />
        <Stack.Screen name="personagem" options={{ presentation: 'modal' }} />
        <Stack.Screen name="resumo" options={{ presentation: 'modal' }} />
        <Stack.Screen name="museu" options={{ presentation: 'modal' }} />
        <Stack.Screen name="detetive" options={{ presentation: 'modal' }} />
        <Stack.Screen name="certificado" options={{ presentation: 'modal' }} />
        <Stack.Screen name="logica" options={{ presentation: 'modal' }} />
        <Stack.Screen name="prolog" options={{ presentation: 'modal' }} />
        <Stack.Screen name="duelo" options={{ presentation: 'fullScreenModal', gestureEnabled: false }} />
        <Stack.Screen name="projetos" />
        <Stack.Screen name="projeto/[id]" options={{ presentation: 'fullScreenModal', gestureEnabled: false }} />
        <Stack.Screen name="teste" options={{ presentation: 'modal' }} />
      </Stack>
      <PythonHost />
      <LeagueResult />
      <AvisosHost />
    </ThemeProvider>
  );
}
