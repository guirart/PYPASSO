import { router, useFocusEffect } from 'expo-router';
import { useCallback, useMemo, useState } from 'react';
import { Image, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { CartaoItem, DetalheItem, ItemIcone } from '@/components/CartaoItem';
import { Coracoes, CRIMSON, pixelado } from '@/components/crimson';
import { InimigoBarra } from '@/components/mapa/InimigoBarra';
import { Moeda } from '@/components/Moeda';
import { Moldura } from '@/components/Moldura';
import { ATAQUE, HABS, nomeDe, ORDEM_RARIDADE, poderDoEquipamento, RARIDADE, SLOTS, type HabId, type ItemInst, type Slot } from '@/lib/itens';
import { custoMelhoria, MAX_MEL, poeiraDeDesmontar } from '@/lib/melhoria';
import { usePlus } from '@/lib/plus';
import { MAX_HEARTS, useGame, useHeroiVisual } from '@/lib/store';

// Visual de RPG com as molduras do Crimson Fantasy GUI recoloridas para o azul-escuro do tema do app (bordas creme originais).
const C = { fundo: '#0F161C', painel: '#18222B', creme: '#EBDDB5', cremeEsc: '#B89A6A', texto: '#EAF0F5', fraco: '#93A3B0', linha: '#2A3743' };
const COLUNAS = 4;

type Filtro = Slot | 'tudo';

/** Inventário: ficha do herói com o equipamento, mochila de peças (drops de chefe e baú), habilidades ativas e teste de ataque. */
export default function InventarioScreen() {
  const insets = useSafeAreaInsets();
  const g = useGame();
  const visual = useHeroiVisual();
  const plusOn = usePlus((s) => s.ativo);
  const [filtro, setFiltro] = useState<Filtro>('tudo');
  const [selId, setSelId] = useState<string | null>(null);
  const [golpe, setGolpe] = useState(0);
  const [aviso, setAviso] = useState<string | null>(null);

  // ao sair da aba, as peças deixam de ser "novas"
  useFocusEffect(useCallback(() => () => useGame.getState().vistoInventario(), []));

  const inv = g.inv ?? [];
  const equip = g.equip;
  const sel = inv.find((i) => i.id === selId) ?? null;
  const bonus = g.bonus();
  const poder = poderDoEquipamento(inv, equip);
  const arma = ATAQUE[visual.arma.estilo];
  const lista = useMemo(
    () => inv.filter((i) => filtro === 'tudo' || i.slot === filtro)
      .sort((a, b) => ORDEM_RARIDADE.indexOf(b.raridade) - ORDEM_RARIDADE.indexOf(a.raridade) || Number(!!b.novo) - Number(!!a.novo)),
    [inv, filtro],
  );
  const vazios = Math.max(COLUNAS * 3, Math.ceil(lista.length / COLUNAS) * COLUNAS) - lista.length; // a mochila sempre mostra pelo menos 3 fileiras de slots
  const ativos = (Object.keys(HABS) as HabId[]).filter((h) => bonus[h] > 0);

  const desmontar = (it: ItemInst) => {
    const ganho = g.desmontar(it.id);
    setSelId(null);
    setAviso(ganho ? `${nomeDe(it)} desmontado: +${ganho} moedas e +${poeiraDeDesmontar(RARIDADE[it.raridade].nivel)} de pó de forja.` : null);
  };
  const melhorar = (it: ItemInst) => {
    const erro = g.melhorar(it.id);
    setAviso(erro ?? `${nomeDe({ ...it, mel: (it.mel ?? 0) + 1 })}: melhoria concluída!`);
  };

  const slotDe = (id: Slot) => {
    const s = SLOTS.find((x) => x.id === id)!;
    const it = inv.find((i) => i.id === equip[id]);
    return (
      <Pressable key={id} onPress={() => it && setSelId(it.id)} accessibilityRole="button" accessibilityLabel={`${s.nome}: ${it ? nomeDe(it) : 'vazio'}`} style={styles.slotCol}>
        <ItemIcone item={it} tamanho={80} vazio={s.nome.toUpperCase()} selecionado={!!it && selId === it.id} />
        <Text numberOfLines={2} style={[styles.slotItem, { color: it ? RARIDADE[it.raridade].cor : C.fraco }]}>{it ? nomeDe(it) : '—'}</Text>
      </Pressable>
    );
  };

  return (
    <View style={{ flex: 1, backgroundColor: C.fundo }}>
      <View style={[styles.header, { paddingTop: insets.top + 8 }]}>
        <Text style={styles.h1} accessibilityRole="header">INVENTÁRIO</Text>
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
        <View style={styles.poeira} accessibilityLabel={`${g.poeira ?? 0} de pó de forja`}><Text style={{ color: '#9EE7FF', fontWeight: '900', fontSize: 15 }}>✦ {g.poeira ?? 0}</Text><Text style={{ color: C.fraco, fontWeight: '800', fontSize: 11 }}>PÓ</Text></View>
        <Pressable onPress={() => router.push('/loja')} accessibilityLabel={`${g.moedas} moedas. Abrir a Loja`} style={styles.moedas}>
          <Moeda size={22} /><Text style={{ color: C.creme, fontWeight: '900', fontSize: 17 }}>{g.moedas ?? 0}</Text>
          <Text style={{ color: C.texto, fontWeight: '900' }}>Loja ›</Text>
        </Pressable>
        </View>
      </View>
      <Image source={CRIMSON.divisor} resizeMode="stretch" style={[styles.divisor, pixelado]} />

      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: (sel ? 330 : 40) + insets.bottom }]}>
        <Moldura tipo="crimsonB" esc={2} style={{ padding: 14 }}>
          <InimigoBarra id="lodo" hp={7} hpMax={7} golpe={golpe} ataque={0} />
        </Moldura>
        <View style={styles.linha}>
          <Pressable onPress={() => setGolpe((x) => x + 1)} accessibilityRole="button" accessibilityLabel="Testar o ataque da arma" style={[styles.btn, { backgroundColor: C.creme }]}>
            <Text style={{ color: '#0F161C', fontWeight: '900', fontSize: 13 }}>⚔ TESTAR ATAQUE</Text>
          </Pressable>
          <Pressable onPress={() => router.push('/personagem')} accessibilityRole="button" accessibilityLabel="Aparência do herói" style={styles.btn}>
            <Text style={{ color: C.texto, fontWeight: '900', fontSize: 13 }}>APARÊNCIA</Text>
          </Pressable>
        </View>

        {/* ficha do herói */}
        <Moldura tipo="crimsonA" esc={2} style={{ gap: 12, padding: 20 }}>
          <View style={styles.tituloLinha}>
            <Text style={styles.titulo} accessibilityLabel={`Equipamento ${poder.pontos} de ${poder.max}`}>FICHA DO HERÓI · ★ {poder.pontos}/{poder.max}</Text>
            {!plusOn && <Coracoes vidas={g.hearts} max={MAX_HEARTS} esc={1} />}
          </View>
          <View style={styles.cruz}>
            <View style={styles.cruzLinha}><View style={{ width: 90 }} />{slotDe('chapeu')}<View style={{ width: 90 }} /></View>
            <View style={styles.cruzLinha}>{slotDe('arma')}{slotDe('roupa')}{slotDe('escudo')}</View>
          </View>
          <View style={[styles.stats, { borderColor: C.linha }]}>
            {ativos.length > 0
              ? ativos.map((h) => <Text key={h} style={styles.stat}>✦ {HABS[h].texto(bonus[h])}</Text>)
              : <Text style={{ color: C.fraco, fontWeight: '700', fontSize: 13 }}>Nenhuma habilidade ativa. Vença os chefes das zonas: cada um deixa cair um baú com uma peça.</Text>}
            {arma && <Text style={[styles.stat, { color: C.fraco }]}>{arma.nome}: {arma.texto} Passiva: {arma.passiva}.</Text>}
          </View>
        </Moldura>

        {!!aviso && <Text style={{ color: C.creme, fontWeight: '800', textAlign: 'center' }} accessibilityLiveRegion="polite">{aviso}</Text>}

        {/* mochila */}
        <Moldura tipo="crimsonA" esc={2} style={{ gap: 10, padding: 18 }}>
          <Text style={styles.titulo}>MOCHILA · {inv.length}</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filtros}>
            {([{ id: 'tudo', nome: 'Tudo' }, ...SLOTS] as { id: Filtro; nome: string }[]).map((f) => {
              const n = inv.filter((i) => f.id === 'tudo' || i.slot === f.id).length;
              const on = filtro === f.id;
              return (
                <Pressable key={f.id} onPress={() => setFiltro(f.id)} accessibilityRole="button" accessibilityState={{ selected: on }} accessibilityLabel={`Filtro ${f.nome}`}
                  style={[styles.aba, { borderBottomColor: on ? C.creme : 'transparent' }]}>
                  <Text style={{ color: on ? C.creme : C.fraco, fontWeight: '900', fontSize: 13 }}>{f.nome.toUpperCase()} {n}</Text>
                </Pressable>
              );
            })}
          </ScrollView>
          <View style={styles.grade}>
            {lista.map((it) => <CartaoItem key={it.id} item={it} equipado={equip[it.slot] === it.id} selecionado={selId === it.id} onPress={() => setSelId(it.id)} />)}
            {Array.from({ length: vazios }, (_, i) => <View key={`v${i}`} style={styles.vazio}><ItemIcone tamanho={80} /></View>)}
          </View>
        </Moldura>
      </ScrollView>

      {sel && (
        <View style={[styles.barra, { paddingBottom: insets.bottom + 62 }]}>
          <DetalheItem item={sel} escuro />
          <View style={styles.acoes}>
            {equip[sel.slot] === sel.id
              ? (SLOTS.find((s) => s.id === sel.slot)!.opcional
                ? <Pressable onPress={() => g.desequipar(sel.slot)} accessibilityRole="button" accessibilityLabel={`Tirar ${nomeDe(sel)}`} style={[styles.btn, { borderColor: C.linha }]}><Text style={{ color: C.texto, fontWeight: '900' }}>TIRAR</Text></Pressable>
                : <View style={[styles.btn, { borderColor: '#2FA84F' }]}><Text style={{ color: '#5FD07F', fontWeight: '900' }}>EQUIPADO</Text></View>)
              : <Pressable onPress={() => g.equipar(sel.id)} accessibilityRole="button" accessibilityLabel={`Equipar ${nomeDe(sel)}`} style={[styles.btn, { backgroundColor: C.creme }]}><Text style={{ color: '#0F161C', fontWeight: '900' }}>EQUIPAR</Text></Pressable>}
            {!sel.id.startsWith('basico-') && sel.hab.length > 0 && (
              (sel.mel ?? 0) >= MAX_MEL
                ? <View style={[styles.btn, { borderColor: C.linha }]}><Text style={{ color: C.fraco, fontWeight: '900' }}>NÍVEL MÁXIMO +{MAX_MEL}</Text></View>
                : <Pressable onPress={() => melhorar(sel)} accessibilityRole="button" accessibilityLabel={`Melhorar ${nomeDe(sel)} por ${custoMelhoria(RARIDADE[sel.raridade].nivel, sel.mel ?? 0)} de pó`} style={[styles.btn, { borderColor: '#7EE2FF' }]}>
                    <Text style={{ color: '#9EE7FF', fontWeight: '900' }}>MELHORAR · ✦{custoMelhoria(RARIDADE[sel.raridade].nivel, sel.mel ?? 0)}</Text>
                  </Pressable>
            )}
            {!sel.id.startsWith('basico-') && (
              <Pressable onPress={() => desmontar(sel)} accessibilityRole="button" accessibilityLabel={`Desmontar ${nomeDe(sel)} por ${RARIDADE[sel.raridade].venda} moedas`} style={styles.btn}>
                <Text style={{ color: C.creme, fontWeight: '900' }}>DESMONTAR +{RARIDADE[sel.raridade].venda}</Text>
              </Pressable>
            )}
            <Pressable onPress={() => setSelId(null)} accessibilityRole="button" accessibilityLabel="Fechar detalhes" style={[styles.btn, { borderColor: C.linha }]}><Text style={{ color: C.fraco, fontWeight: '900' }}>FECHAR</Text></Pressable>
          </View>
        </View>
      )}

    </View>
  );
}

const styles = StyleSheet.create({
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingBottom: 6 },
  h1: { fontSize: 24, fontWeight: '900', color: C.creme, letterSpacing: 3 },
  poeira: { flexDirection: 'row', alignItems: 'center', gap: 5, borderWidth: 2, borderColor: C.linha, backgroundColor: C.painel, borderRadius: 12, paddingVertical: 5, paddingHorizontal: 9 },
  moedas: { flexDirection: 'row', alignItems: 'center', gap: 6, borderWidth: 2, borderColor: C.cremeEsc, backgroundColor: C.painel, borderRadius: 12, paddingVertical: 5, paddingHorizontal: 10 },
  divisor: { width: 234, height: 36, alignSelf: 'center', marginBottom: 2 },
  scroll: { padding: 16, gap: 14, maxWidth: 680, width: '100%', alignSelf: 'center' },
  linha: { flexDirection: 'row', gap: 10, justifyContent: 'center', flexWrap: 'wrap' },
  btn: { borderWidth: 2, borderColor: C.cremeEsc, backgroundColor: C.painel, borderRadius: 10, paddingHorizontal: 14, paddingVertical: 9, alignItems: 'center' },
  titulo: { color: C.creme, fontSize: 12, fontWeight: '900', letterSpacing: 1.6 },
  tituloLinha: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: 8, flexWrap: 'wrap' },
  cruz: { alignItems: 'center', gap: 6 },
  cruzLinha: { flexDirection: 'row', gap: 10, justifyContent: 'center' },
  slotCol: { alignItems: 'center', gap: 3, width: 90 },
  slotItem: { fontSize: 11, fontWeight: '800', textAlign: 'center', minHeight: 28 },
  stats: { borderTopWidth: 1, paddingTop: 10, gap: 3 },
  stat: { color: C.texto, fontWeight: '800', fontSize: 13 },
  preco: { flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: C.creme, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 8 },
  filtros: { flexDirection: 'row', gap: 14, paddingVertical: 2 },
  aba: { borderBottomWidth: 3, paddingBottom: 4 },
  grade: { flexDirection: 'row', flexWrap: 'wrap', gap: 2, justifyContent: 'center' },
  vazio: { padding: 3, opacity: 0.8 },
  barra: { position: 'absolute', left: 0, right: 0, bottom: 0, backgroundColor: C.painel, borderTopWidth: 2, borderTopColor: C.cremeEsc, paddingHorizontal: 16, paddingTop: 12, gap: 10, alignItems: 'center' },
  acoes: { flexDirection: 'row', gap: 8, flexWrap: 'wrap', justifyContent: 'center' },
});
