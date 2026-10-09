import { router, useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { ActivityIndicator, Linking, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { Cross } from '@/components/Icons';
import { assinar, atualizarPlus, DIAS_TESTE, gerenciar, modoDemo, nomeDaLoja, PLANOS, precosDaLoja, restaurar, usePlus, type Ciclo } from '@/lib/plus';
import { Icone, type NomeIcone } from '@/components/Icone';
import { useTheme } from '@/lib/theme';

const ROXO = '#5B3CC4';
const ROXO_FUNDO = '#4527A8';
const OURO = '#FFC83D';

const BENEFICIOS = [
  { icone: 'coracao', titulo: 'Vidas ilimitadas', texto: 'Errou? Tenta de novo na hora, sem esperar.' },
  { icone: 'usuarios', titulo: 'Para todos os perfis', texto: 'Vale para cada perfil deste aparelho.' },
  { icone: 'diamante', titulo: 'Selo Plus', texto: 'Um selo brilhante no seu perfil.' },
  { icone: 'broto', titulo: 'Apoia o PyPasso', texto: 'Ajuda a criar mais lições e provas.' },
];

const dataBR = (iso: string | null) => (iso ? new Date(iso).toLocaleDateString('pt-BR') : '');

export default function PlusScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const plus = usePlus();
  const { status } = useLocalSearchParams<{ status?: string }>();
  const [ciclo, setCiclo] = useState<Ciclo>('anual');
  const [precos, setPrecos] = useState<Partial<Record<Ciclo, string>>>({});
  const [ocupado, setOcupado] = useState(false);
  const [msg, setMsg] = useState<{ ok: boolean; texto: string } | null>(null);
  const [confirmando, setConfirmando] = useState(status === 'ok');
  const demo = modoDemo();

  useEffect(() => {
    atualizarPlus().catch(() => {});
    if (!demo) precosDaLoja().then(setPrecos);
  }, [demo]);

  // Volta do Stripe: o webhook leva alguns segundos (no Pix, até a pessoa autorizar no banco).
  useEffect(() => {
    if (status !== 'ok') return;
    let n = 0;
    const id = setInterval(async () => {
      n++;
      const s = await atualizarPlus().catch(() => null);
      if (s?.ativo || n >= 20) { clearInterval(id); setConfirmando(false); }
    }, 3000);
    return () => clearInterval(id);
  }, [status]);

  const agir = async (f: () => Promise<{ ok: boolean; mensagem?: string; redirecionando?: boolean }>) => {
    setOcupado(true); setMsg(null);
    const r = await f();
    setOcupado(false);
    if (r.mensagem) setMsg({ ok: r.ok, texto: r.mensagem });
  };

  const preco = (c: Ciclo) => precos[c] ?? PLANOS[c].preco;

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <ScrollView contentContainerStyle={{ paddingBottom: insets.bottom + 32 }}>
        <View style={[styles.hero, { paddingTop: insets.top + 12 }]}>
          <View style={styles.top}>
            <Pressable onPress={() => (router.canGoBack() ? router.back() : router.replace('/'))} accessibilityLabel="Fechar" hitSlop={10}>
              <Cross color="#fff" size={26} />
            </Pressable>
            <Text style={styles.brand}>PyPasso <Text style={{ color: OURO }}>Plus</Text></Text>
            <View style={{ width: 26 }} />
          </View>
          <View style={styles.heroRow}>
            <Mascot size={110} mood="cheer" />
            <View style={styles.infinity}><Text style={styles.infinityTxt}>∞</Text><View style={styles.heart}><Icone nome="coracao" size={26} color="#FF5A63" /></View></View>
          </View>
          <Text style={styles.h1}>{plus.ativo ? 'Você é Plus!' : 'Vidas ilimitadas.\nErre sem medo.'}</Text>
          <Text style={styles.sub}>{plus.ativo ? 'Pratique quanto quiser: suas vidas não acabam.' : 'Pratique quanto quiser, sem esperar as vidas voltarem.'}</Text>
        </View>

        <View style={styles.body}>
          {demo && (
            <View style={[styles.demo, { borderColor: t.sunDeep, backgroundColor: t.surface }]}>
              <Text style={{ color: t.ink, fontWeight: '900' }}>Modo demonstração</Text>
              <Text style={{ color: t.muted, fontWeight: '600' }}>Nenhum pagamento real acontece aqui. Para cobrar de verdade, configure o Google Play/App Store (RevenueCat) e o Stripe, como explica o PAGAMENTOS.md.</Text>
            </View>
          )}

          {confirmando && !plus.ativo && (
            <View style={[styles.card, { backgroundColor: t.surface, borderColor: t.line, flexDirection: 'row', gap: 12, alignItems: 'center' }]}>
              <ActivityIndicator color={ROXO} />
              <Text style={{ color: t.ink, fontWeight: '700', flex: 1 }}>Confirmando seu pagamento… No Pix, o Plus ativa assim que você autorizar no app do banco.</Text>
            </View>
          )}

          {BENEFICIOS.map((b) => (
            <View key={b.titulo} style={styles.benef}>
              <View style={styles.benefIc}><Icone nome={b.icone as NomeIcone} size={24} color="#FFD86B" /></View>
              <View style={{ flex: 1 }}>
                <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>{b.titulo}</Text>
                <Text style={{ color: t.muted, fontWeight: '600' }}>{b.texto}</Text>
              </View>
            </View>
          ))}

          {plus.ativo ? (
            <View style={[styles.card, { backgroundColor: t.surface, borderColor: ROXO }]}>
              <Text style={{ color: t.ink, fontWeight: '900', fontSize: 17 }}>
                Plus {plus.ciclo ?? ''} {plus.fonte === 'demo' ? '(demonstração)' : ''}
              </Text>
              {!!plus.expiraEm && (
                <Text style={{ color: t.muted, fontWeight: '700' }}>
                  {plus.cancelada ? `Cancelado: vale até ${dataBR(plus.expiraEm)}.` : `Renova em ${dataBR(plus.expiraEm)}.`}
                </Text>
              )}
              <Button3D label={plus.fonte === 'demo' ? 'Desligar a demonstração' : 'Gerenciar assinatura'} variant="ghost" disabled={ocupado} onPress={() => agir(gerenciar)} />
            </View>
          ) : (
            <>
              <View style={styles.planos} accessibilityRole="radiogroup">
                {(['anual', 'mensal'] as const).map((c) => {
                  const on = c === ciclo;
                  return (
                    <Pressable key={c} onPress={() => setCiclo(c)} accessibilityRole="radio" accessibilityState={{ checked: on }}
                      accessibilityLabel={`Plano ${c}, ${preco(c)} ${PLANOS[c].por}`}
                      style={[styles.plano, { borderColor: on ? ROXO : t.line, backgroundColor: on ? 'rgba(91,60,196,0.08)' : t.surface }]}>
                      {c === 'anual' && <Text style={styles.ribbon}>{PLANOS.anual.economia}</Text>}
                      <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16, textTransform: 'capitalize' }}>{c}</Text>
                      <Text style={{ color: t.ink, fontWeight: '900', fontSize: 22 }}>{preco(c)}<Text style={{ fontSize: 14, color: t.muted }}>{PLANOS[c].por}</Text></Text>
                      <Text style={{ color: t.muted, fontWeight: '700', fontSize: 12 }}>{PLANOS[c].detalhe}</Text>
                      <View style={[styles.radio, { borderColor: on ? ROXO : t.line, backgroundColor: on ? ROXO : 'transparent' }]} />
                    </Pressable>
                  );
                })}
              </View>
              <Pressable onPress={() => agir(() => assinar(ciclo))} disabled={ocupado} accessibilityRole="button"
                style={({ pressed }) => [styles.cta, { opacity: ocupado ? 0.6 : 1, transform: [{ translateY: pressed ? 3 : 0 }], borderBottomWidth: pressed ? 2 : 6 }]}>
                <Text style={styles.ctaTxt}>{ocupado ? 'Abrindo…' : demo ? 'Ativar Plus (demonstração)' : `Começar ${DIAS_TESTE} dias grátis`}</Text>
              </Pressable>
              <Text style={[styles.fine, { color: t.muted }]}>
                {DIAS_TESTE} dias grátis na primeira assinatura. Depois, {preco(ciclo)} {ciclo === 'anual' ? 'por ano' : 'por mês'}, cobrado automaticamente
                {Platform.OS === 'web' ? ' no cartão ou no Pix Automático (o banco avisa 3 dias antes de cada cobrança)' : ` pela ${nomeDaLoja()}`} até você cancelar.
                Cancele quando quiser {Platform.OS === 'web' ? 'aqui mesmo, em Gerenciar assinatura' : `em ${nomeDaLoja()} > Assinaturas`}; o Plus continua até o fim do período pago.
              </Text>
            </>
          )}

          {msg && <Text style={[styles.msg, { color: msg.ok ? t.good : t.bad }]}>{msg.texto}</Text>}

          <View style={styles.links}>
            {Platform.OS !== 'web' && !plus.ativo && (
              <Pressable onPress={() => agir(restaurar)} accessibilityRole="button"><Text style={[styles.link, { color: ROXO }]}>Restaurar compras</Text></Pressable>
            )}
            {!!process.env.EXPO_PUBLIC_TERMS_URL && (
              <Pressable onPress={() => Linking.openURL(process.env.EXPO_PUBLIC_TERMS_URL!)}><Text style={[styles.link, { color: t.muted }]}>Termos de uso</Text></Pressable>
            )}
            {!!process.env.EXPO_PUBLIC_PRIVACY_URL && (
              <Pressable onPress={() => Linking.openURL(process.env.EXPO_PUBLIC_PRIVACY_URL!)}><Text style={[styles.link, { color: t.muted }]}>Privacidade</Text></Pressable>
            )}
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  hero: { backgroundColor: ROXO, paddingHorizontal: 20, paddingBottom: 28, borderBottomLeftRadius: 28, borderBottomRightRadius: 28, gap: 8 },
  top: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', maxWidth: 600, width: '100%', alignSelf: 'center' },
  brand: { color: '#fff', fontSize: 18, fontWeight: '900' },
  heroRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8, marginTop: 6 },
  infinity: { width: 96, height: 96, borderRadius: 48, backgroundColor: ROXO_FUNDO, alignItems: 'center', justifyContent: 'center', borderWidth: 3, borderColor: OURO },
  infinityTxt: { color: OURO, fontSize: 48, fontWeight: '900', lineHeight: 54 },
  heart: { marginTop: -8 },
  h1: { color: '#fff', fontSize: 28, fontWeight: '900', textAlign: 'center', lineHeight: 34 },
  sub: { color: 'rgba(255,255,255,0.88)', fontSize: 15, fontWeight: '700', textAlign: 'center' },
  body: { padding: 20, gap: 14, maxWidth: 600, width: '100%', alignSelf: 'center' },
  demo: { borderWidth: 2, borderStyle: 'dashed', borderRadius: 14, padding: 12, gap: 4 },
  card: { borderWidth: 2, borderRadius: 16, padding: 16, gap: 8 },
  benef: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  benefIc: { width: 40, height: 40, borderRadius: 12, backgroundColor: 'rgba(255,255,255,0.12)', alignItems: 'center', justifyContent: 'center' },
  planos: { flexDirection: 'row', gap: 12, marginTop: 6 },
  plano: { flex: 1, borderWidth: 3, borderRadius: 18, padding: 14, paddingTop: 20, gap: 2 },
  ribbon: { position: 'absolute', top: -12, alignSelf: 'center', backgroundColor: OURO, color: '#3A2A00', fontWeight: '900', fontSize: 12, paddingHorizontal: 10, paddingVertical: 3, borderRadius: 99, overflow: 'hidden' },
  radio: { position: 'absolute', top: 12, right: 12, width: 18, height: 18, borderRadius: 9, borderWidth: 2 },
  cta: { backgroundColor: ROXO, borderBottomColor: '#35208A', borderRadius: 16, paddingVertical: 16, alignItems: 'center' },
  ctaTxt: { color: '#fff', fontWeight: '900', fontSize: 17, letterSpacing: 0.5, textTransform: 'uppercase' },
  fine: { fontSize: 12, fontWeight: '600', lineHeight: 17, textAlign: 'center' },
  msg: { fontWeight: '800', textAlign: 'center' },
  links: { flexDirection: 'row', justifyContent: 'center', gap: 18, flexWrap: 'wrap' },
  link: { fontWeight: '800', fontSize: 14 },
});
