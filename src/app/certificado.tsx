import { router } from 'expo-router';
import { useEffect, useState } from 'react';
import { Pressable, ScrollView, Share, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { AvatarMoldura, Mascot } from '@/components/Characters';
import { Cross } from '@/components/Icons';
import { LESSONS_BY_TRACK, TRACKS, type TrackId } from '@/content';
import { useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

const dataBR = (ts: number) => new Date(ts).toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' });

/** Certificados: ao concluir todas as lições de uma trilha, ela ganha um certificado com o seu nome, para copiar e compartilhar. */
export default function CertificadoScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const [exemplo, setExemplo] = useState<TrackId | null>(null);
  const [msg, setMsg] = useState('');

  const info = TRACKS.map((tr) => {
    const aulas = LESSONS_BY_TRACK[tr.id];
    const feitas = aulas.filter((l) => l.id in g.done);
    const completa = aulas.length > 0 && feitas.length === aulas.length;
    const precisao = feitas.length ? Math.round(feitas.reduce((s, l) => s + g.done[l.id], 0) / feitas.length) : 0;
    return { ...tr, total: aulas.length, feitas: feitas.length, completa, precisao };
  });

  // Ao ver uma trilha concluída, grava a data de emissão (a primeira vez)
  useEffect(() => { info.filter((i) => i.completa && !g.certs?.[i.id]).forEach((i) => g.emitirCertificado(i.id)); });

  const nome = g.name.trim() || 'Aluno(a) do PyPasso';
  const texto = (titulo: string, feitas: number, precisao: number, quando: number) =>
    `${nome} concluiu a trilha “${titulo}” no PyPasso: ${feitas} lições com ${precisao}% de precisão média, em ${dataBR(quando)}.`;

  const copiar = async (s: string) => {
    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && typeof window !== 'undefined') await navigator.clipboard.writeText(s);
      else await Share.share({ message: s });
      setMsg('Texto copiado. Cole onde quiser compartilhar.');
    } catch { setMsg('Não consegui copiar aqui.'); }
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Certificados</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]}>
        <Text style={{ color: t.muted, fontWeight: '700', lineHeight: 21 }}>Conclua todas as lições de uma trilha para ganhar o certificado dela, com o seu nome.</Text>
        {info.map((i) => {
          const mostrar = i.completa || exemplo === i.id;
          const quando = g.certs?.[i.id] ?? Date.now();
          return (
            <View key={i.id} style={{ gap: 10 }}>
              <View style={[styles.linha, { backgroundColor: t.surface, borderColor: i.completa ? t.good : t.line }]}>
                <View style={{ flex: 1, gap: 4 }}>
                  <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>{i.title}</Text>
                  <View style={[styles.barra, { backgroundColor: t.line }]}><View style={{ height: '100%', width: `${(i.feitas / Math.max(1, i.total)) * 100}%`, backgroundColor: i.completa ? t.good : t.brand }} /></View>
                  <Text style={{ color: t.muted, fontWeight: '700', fontSize: 12 }}>{i.feitas} de {i.total} lições{i.completa ? ' · concluída!' : ''}</Text>
                </View>
                {!i.completa && <Button3D label={exemplo === i.id ? 'Ocultar' : 'Ver exemplo'} variant="ghost" onPress={() => setExemplo(exemplo === i.id ? null : i.id)} />}
              </View>
              {mostrar && (
                <View style={[styles.cert, { borderColor: t.brand, backgroundColor: t.surface }]}>
                  {!i.completa && <Text style={[styles.exemplo, { backgroundColor: t.sun, color: t.sunInk }]}>EXEMPLO</Text>}
                  <Text style={{ color: t.muted, fontWeight: '900', fontSize: 11, letterSpacing: 2 }}>CERTIFICADO DE CONCLUSÃO</Text>
                  <AvatarMoldura seed={g.avatarSeed} size={72} moldura={g.moldura} />
                  <Text style={{ color: t.muted, fontWeight: '700' }}>O PyPasso certifica que</Text>
                  <Text style={{ color: t.ink, fontWeight: '900', fontSize: 26, textAlign: 'center' }}>{nome}</Text>
                  <Text style={{ color: t.muted, fontWeight: '700' }}>concluiu a trilha</Text>
                  <Text style={{ color: t.brand, fontWeight: '900', fontSize: 20, textAlign: 'center' }}>{i.title}</Text>
                  <View style={styles.dados}>
                    <Dado t={t} v={String(i.completa ? i.feitas : i.total)} r="lições" />
                    <Dado t={t} v={`${i.completa ? i.precisao : 100}%`} r="precisão média" />
                    <Dado t={t} v={`${g.xp}`} r="XP total" />
                  </View>
                  <Text style={{ color: t.muted, fontWeight: '700' }}>{dataBR(quando)}</Text>
                  <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}><Mascot size={44} animated={false} mood="cheer" /><Text style={{ color: t.muted, fontWeight: '800', fontStyle: 'italic' }}>Assinado: Pipo</Text></View>
                </View>
              )}
              {i.completa && <Button3D label="Copiar texto para compartilhar" onPress={() => copiar(texto(i.title, i.feitas, i.precisao, quando))} />}
            </View>
          );
        })}
        {!!msg && <Text style={{ color: t.good, fontWeight: '800' }} accessibilityLiveRegion="polite">{msg}</Text>}
      </ScrollView>
    </View>
  );
}

function Dado({ t, v, r }: { t: ReturnType<typeof useTheme>; v: string; r: string }) {
  return <View style={{ alignItems: 'center' }}><Text style={{ color: t.ink, fontWeight: '900', fontSize: 20 }}>{v}</Text><Text style={{ color: t.muted, fontWeight: '700', fontSize: 11 }}>{r}</Text></View>;
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 14, maxWidth: 560, width: '100%', alignSelf: 'center' },
  linha: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, padding: 12 },
  barra: { height: 10, borderRadius: 99, overflow: 'hidden' },
  cert: { borderWidth: 4, borderRadius: 20, padding: 20, alignItems: 'center', gap: 8, borderStyle: 'solid' },
  exemplo: { position: 'absolute', top: 10, right: 10, fontWeight: '900', fontSize: 10, letterSpacing: 1, borderRadius: 6, paddingHorizontal: 8, paddingVertical: 2, overflow: 'hidden' },
  dados: { flexDirection: 'row', gap: 22, marginVertical: 4 },
});
