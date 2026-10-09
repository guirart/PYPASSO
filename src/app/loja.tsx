import { router } from 'expo-router';
import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { AvatarMoldura } from '@/components/Characters';
import { Cross } from '@/components/Icons';
import { Icone, IconeTile } from '@/components/Icone';
import { Moeda } from '@/components/Moeda';
import { LOJA, type ItemLoja } from '@/lib/gamificacao';
import { usePlus } from '@/lib/plus';
import { MAX_HEARTS, useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

const COR_ITEM: Record<string, string> = { congelador: '#3FA9D6', vidas: '#E5383B', xp2: '#E0A21C' };

/** Loja: troca moedas por ajudas (congelador, vidas, XP em dobro) e molduras para o avatar. */
export default function LojaScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const plus = usePlus((s) => s.ativo);
  const [msg, setMsg] = useState<{ id: string; ok: boolean; texto: string } | null>(null);
  const ajudas = LOJA.filter((i) => i.tipo !== 'moldura');
  const molduras = LOJA.filter((i) => i.tipo === 'moldura');

  const comprar = (it: ItemLoja) => {
    const erro = g.comprar(it.id);
    setMsg({ id: it.id, ok: !erro, texto: erro ?? (it.tipo === 'moldura' ? 'Moldura comprada e já em uso!' : 'Comprado!') });
  };

  const estado = (it: ItemLoja): string | null => {
    if (it.tipo === 'congelador') return `Guardados: ${g.congelador}/${it.max}`;
    if (it.tipo === 'vidas') return plus ? 'Você tem vidas ilimitadas (Plus)' : `Vidas: ${g.hearts}/${MAX_HEARTS}`;
    if (it.tipo === 'xp2' && g.xp2Ate > Date.now()) return `Ativo por mais ${Math.ceil((g.xp2Ate - Date.now()) / 60000)} min`;
    return null;
  };

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar a Loja" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Loja</Text>
        <View style={[styles.saldo, { borderColor: t.line, backgroundColor: t.surface }]} accessibilityLabel={`${g.moedas} moedas`}>
          <Moeda size={22} /><Text style={[styles.saldoN, { color: t.sunDeep }]}>{g.moedas}</Text>
        </View>
      </View>
      <ScrollView contentContainerStyle={styles.scroll}>
        <Text style={[styles.dica, { color: t.muted }]}>
          Ganhe moedas terminando lições (+5, +10 sem erros), revisões, projetos, missões do dia, o baú, conquistas e subindo de nível.
        </Text>

        <Text style={[styles.sec, { color: t.ink }]}>Ajudas</Text>
        {ajudas.map((it) => (
          <Item key={it.id} it={it} estado={estado(it)} msg={msg?.id === it.id ? msg : null} pode={g.moedas >= it.preco} comprar={() => comprar(it)} />
        ))}

        <Text style={[styles.sec, { color: t.ink }]}>Molduras para o avatar</Text>
        <View style={styles.grid}>
          {molduras.map((it) => {
            const tem = g.molduras.includes(it.id), usando = g.moldura === it.id;
            return (
              <View key={it.id} style={[styles.mold, { backgroundColor: t.surface, borderColor: usando ? t.brand : t.line }]}>
                <AvatarMoldura seed={g.avatarSeed} size={64} moldura={it.id} />
                <View style={{ flexDirection: 'row', alignItems: 'center', gap: 5 }}><Icone nome={it.icone} size={16} color={it.cores?.[0] ?? t.ink} /><Text style={[styles.nome, { color: t.ink }]}>{it.nome.replace('Moldura ', '')}</Text></View>
                {tem ? (
                  <Pressable onPress={() => g.usarMoldura(usando ? '' : it.id)} accessibilityRole="button" style={[styles.btn, { borderColor: t.brand, backgroundColor: usando ? t.brand : t.bg }]}>
                    <Text style={{ color: usando ? '#fff' : t.brand, fontWeight: '900' }}>{usando ? 'Em uso' : 'Usar'}</Text>{usando && <Icone nome="check" size={14} color="#fff" />}
                  </Pressable>
                ) : (
                  <Preco it={it} pode={g.moedas >= it.preco} comprar={() => comprar(it)} />
                )}
                {msg?.id === it.id && !msg.ok && <Text style={{ color: t.bad, fontWeight: '700', fontSize: 12, textAlign: 'center' }}>{msg.texto}</Text>}
              </View>
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}

function Item({ it, estado, msg, pode, comprar }: { it: ItemLoja; estado: string | null; msg: { ok: boolean; texto: string } | null; pode: boolean; comprar: () => void }) {
  const t = useTheme();
  return (
    <View style={[styles.item, { backgroundColor: t.surface, borderColor: t.line }]}>
      <IconeTile nome={it.icone} cor={COR_ITEM[it.id] ?? t.brand} size={48} />
      <View style={{ flex: 1, gap: 2 }}>
        <Text style={[styles.nome, { color: t.ink }]}>{it.nome}</Text>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{it.texto}</Text>
        {estado && <Text style={{ color: t.brand, fontWeight: '800', fontSize: 12 }}>{estado}</Text>}
        {msg && <Text style={{ color: msg.ok ? t.good : t.bad, fontWeight: '800', fontSize: 13 }}>{msg.texto}</Text>}
      </View>
      <Preco it={it} pode={pode} comprar={comprar} />
    </View>
  );
}

function Preco({ it, pode, comprar }: { it: ItemLoja; pode: boolean; comprar: () => void }) {
  const t = useTheme();
  return (
    <Pressable onPress={comprar} accessibilityRole="button" accessibilityLabel={`Comprar ${it.nome} por ${it.preco} moedas`}
      style={({ pressed }) => [styles.btn, { borderColor: pode ? t.sunDeep : t.line, backgroundColor: pode ? t.sun : t.bg, borderBottomWidth: pressed ? 2 : 4 }]}>
      <Moeda size={18} /><Text style={{ color: pode ? t.sunInk : t.muted, fontWeight: '900', fontVariant: ['tabular-nums'] }}>{it.preco}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  h1: { fontSize: 24, fontWeight: '900', flex: 1 },
  saldo: { flexDirection: 'row', alignItems: 'center', gap: 6, borderWidth: 2, borderRadius: 14, paddingVertical: 5, paddingHorizontal: 10 },
  saldoN: { fontSize: 18, fontWeight: '900', fontVariant: ['tabular-nums'] },
  scroll: { padding: 16, paddingBottom: 50, gap: 12, maxWidth: 620, width: '100%', alignSelf: 'center' },
  dica: { fontWeight: '600', lineHeight: 20 },
  sec: { fontSize: 20, fontWeight: '900', marginTop: 8 },
  item: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 18, padding: 14 },
  emoji: { fontSize: 32 },
  nome: { fontSize: 16, fontWeight: '900' },
  btn: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 5, borderWidth: 2, borderBottomWidth: 4, borderRadius: 12, paddingVertical: 7, paddingHorizontal: 12, minWidth: 76 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  mold: { width: '47%', flexGrow: 1, alignItems: 'center', gap: 8, borderWidth: 2, borderRadius: 18, padding: 12 },
});
