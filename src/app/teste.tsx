import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, ScrollView, Share, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Button3D } from '@/components/Button3D';
import { Cross } from '@/components/Icons';
import { relatorio, TIPOS_RELATO, useTeste } from '@/lib/teste';
import { mudarConsentimento } from '@/lib/privacidade';
import { supabase } from '@/lib/supabase';
import { mono, useTheme } from '@/lib/theme';

/** Relatório do teste com usuários: onde a pessoa errou, onde desistiu e o que relatou. */
export default function TesteScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  useTeste((s) => s.ex); // atualiza ao mudar
  const r = relatorio();
  const [copiado, setCopiado] = useState('');
  const limpar = useTeste((s) => s.limpar);
  const enviar = useTeste((s) => s.enviar);

  const compartilhar = async () => {
    try {
      if (typeof navigator !== 'undefined' && navigator.clipboard && typeof window !== 'undefined') {
        await navigator.clipboard.writeText(r.texto + '\n\n' + r.json);
        setCopiado('Relatório copiado. Cole num e-mail ou mensagem.');
        return;
      }
      await Share.share({ message: r.texto + '\n\n' + r.json });
    } catch {
      setCopiado('Não deu para copiar aqui. Selecione o texto abaixo.');
    }
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Relatório de teste</Text>
      </View>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
          O PyPasso anota neste aparelho onde a pessoa errou, onde desistiu de uma lição e o que ela contou no botão "Travei aqui" (a bandeirinha no topo dos exercícios). Use com o roteiro do TESTE-COM-USUARIOS.md. Nada aqui tem nome ou e-mail.
        </Text>
        {supabase && (
          <Pressable onPress={() => mudarConsentimento('teste', !enviar)} accessibilityRole="switch" accessibilityState={{ checked: enviar }}
            style={[styles.card, { backgroundColor: t.surface, borderColor: enviar ? t.good : t.line, flexDirection: 'row', alignItems: 'center', gap: 12 }]}>
            <View style={{ flex: 1, gap: 3 }}>
              <Text style={{ color: t.ink, fontWeight: '900' }}>Participar do teste</Text>
              <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>Envia estes dados, sem nome nem e-mail, para a equipe do PyPasso melhorar os exercícios. Desligue quando quiser.</Text>
            </View>
            <View style={[styles.switch, { backgroundColor: enviar ? t.good : t.line }]}><View style={[styles.knob, { alignSelf: enviar ? 'flex-end' : 'flex-start' }]} /></View>
          </Pressable>
        )}
        <Button3D label="Copiar / compartilhar relatório" onPress={compartilhar} />
        {!!copiado && <Text style={{ color: t.good, fontWeight: '800' }}>{copiado}</Text>}

        <Text style={[styles.sec, { color: t.ink }]}>Onde mais errou</Text>
        {r.dificeis.length ? r.dificeis.map((d) => (
          <View key={d.id} style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={{ color: t.ink, fontWeight: '900' }}>{d.onde} · <Text style={{ fontFamily: mono }}>{d.id}</Text></Text>
            <Text style={{ color: t.muted, fontWeight: '600' }} numberOfLines={2}>{d.pergunta}</Text>
            <Text style={{ color: t.bad, fontWeight: '800' }}>{d.erros} erro(s) em {d.tent} tentativa(s) · {Math.round(d.ms / Math.max(1, d.tent) / 1000)}s por tentativa</Text>
          </View>
        )) : <Text style={{ color: t.muted }}>Nenhum erro anotado ainda.</Text>}

        <Text style={[styles.sec, { color: t.ink }]}>Lições abandonadas</Text>
        {r.abandonos.length ? r.abandonos.map((a) => (
          <Text key={a.id} style={{ color: t.ink, fontWeight: '700' }}>• {a.titulo}: saiu no meio {a.abandonou}x (terminou {a.fez}x)</Text>
        )) : <Text style={{ color: t.muted }}>Nenhuma.</Text>}

        <Text style={[styles.sec, { color: t.ink }]}>Relatos "Travei aqui"</Text>
        {r.relatos.length ? r.relatos.map((x) => (
          <View key={x.ts} style={[styles.card, { backgroundColor: t.surface, borderColor: t.line }]}>
            <Text style={{ color: t.ink, fontWeight: '900' }}>{TIPOS_RELATO.find((k) => k.id === x.tipo)?.texto} · {new Date(x.ts).toLocaleString('pt-BR')}</Text>
            {!!x.texto && <Text style={{ color: t.ink, fontWeight: '600' }}>{x.texto}</Text>}
            <Text style={{ color: t.muted, fontFamily: mono, fontSize: 12 }}>{x.exId ?? x.licao}</Text>
          </View>
        )) : <Text style={{ color: t.muted }}>Nenhum relato ainda.</Text>}

        <Button3D label="Apagar dados do teste" variant="ghost" onPress={limpar} />
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  h1: { fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, paddingBottom: 50, gap: 12, maxWidth: 620, width: '100%', alignSelf: 'center' },
  sec: { fontSize: 19, fontWeight: '900', marginTop: 8 },
  card: { borderWidth: 2, borderRadius: 14, padding: 12, gap: 3 },
  switch: { width: 52, height: 30, borderRadius: 99, padding: 3, justifyContent: 'center' },
  knob: { width: 24, height: 24, borderRadius: 12, backgroundColor: '#fff' },
});
