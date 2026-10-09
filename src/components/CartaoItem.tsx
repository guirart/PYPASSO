import { Image, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { ATAQUE, HABS, nomeDe, RARIDADE, valorEfetivo, type ItemInst, type Raridade } from '@/lib/itens';
import { useTheme } from '@/lib/theme';
import { CRIMSON } from './crimson';
import { ICONES } from './icones-item';

const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

/** Ícone do item (arte do Raven Fantasy Icons) dentro de um "slot" de RPG: fundo escuro, borda e brilho na cor da raridade. */
export function ItemIcone({ item, tamanho = 64, selecionado, equipado, vazio, rotulo }: { item?: ItemInst | null; tamanho?: number; selecionado?: boolean; equipado?: boolean; vazio?: string; rotulo?: string }) {
  const r = item ? RARIDADE[item.raridade] : null;
  const cor = r?.cor ?? '#5B4C3A';
  const ico = Math.round(tamanho * 0.6); // o ícone (32px) fica ampliado dentro do slot
  const img = item ? ICONES[`${item.slot}_${item.estilo}_${item.cor}`] : undefined;
  return (
    <View accessibilityLabel={rotulo} style={[styles.slot, {
      width: tamanho, height: tamanho,
      shadowColor: cor, shadowOpacity: item && item.raridade !== 'comum' ? 0.95 : 0, shadowRadius: item ? (item.raridade === 'lendario' ? 14 : item.raridade === 'epico' ? 10 : 7) : 0, shadowOffset: { width: 0, height: 0 },
    }]}>
      {/* slot do Crimson Fantasy GUI */}
      <Image source={CRIMSON.slot} resizeMode="stretch" style={[{ position: 'absolute', left: 0, top: 0, width: tamanho, height: tamanho }, pixelado]} />
      {/* tom da raridade dentro do slot e um aro na mesma cor */}
      {item && <View pointerEvents="none" style={{ position: 'absolute', left: '14%', right: '14%', top: '14%', bottom: '14%', backgroundColor: cor, opacity: item.raridade === 'comum' ? 0.12 : 0.34, borderRadius: 4 }} />}
      <View pointerEvents="none" style={[StyleSheet.absoluteFill, { borderRadius: 9, borderWidth: selecionado ? 3 : item ? 2 : 0, borderColor: selecionado ? '#FFE9A8' : cor }]} />
      {img ? <Image source={img} resizeMode="stretch" style={[{ width: ico, height: ico }, pixelado]} /> : <Text style={{ color: '#E9D6C0', opacity: 0.55, fontWeight: '900', fontSize: 11 }}>{vazio ?? ''}</Text>}
      {equipado && <View style={styles.eq}><Text style={{ color: '#fff', fontWeight: '900', fontSize: 9 }}>E</Text></View>}
      {!!item?.novo && !equipado && <View style={styles.novo}><Text style={{ color: '#3A2A00', fontWeight: '900', fontSize: 8 }}>NOVO</Text></View>}
      {!!item && item.hab.length > 0 && <Text style={[styles.estrelas, { color: cor }]}>{'✦'.repeat(item.hab.length)}</Text>}
    </View>
  );
}

/** Lista das habilidades do item, uma por linha. */
export function Habilidades({ item, tamanho = 13, cor }: { item: ItemInst; tamanho?: number; cor?: string }) {
  const t = useTheme();
  const c = cor ?? t.ink;
  if (!item.hab.length) return <Text style={{ color: cor ? '#A0917A' : t.muted, fontSize: tamanho, fontWeight: '700' }}>Sem habilidades</Text>;
  return (
    <View style={{ gap: 2 }}>
      {item.hab.map((h) => <Text key={h.id} style={{ color: c, fontSize: tamanho, fontWeight: '800' }}>✦ {HABS[h.id].texto(valorEfetivo(item, h))}</Text>)}
    </View>
  );
}

/** Slot da mochila: ícone e o nome embaixo. */
export function CartaoItem({ item, equipado, selecionado, onPress }: { item: ItemInst; equipado?: boolean; selecionado?: boolean; onPress: () => void }) {
  const nome = nomeDe(item);
  return (
    <Pressable onPress={onPress} accessibilityRole="button" accessibilityLabel={`${nome}, ${RARIDADE[item.raridade].nome}`} accessibilityState={{ selected: !!selecionado }} style={styles.cartao}>
      <ItemIcone item={item} selecionado={selecionado} equipado={equipado} />
    </Pressable>
  );
}

export function NomeRaridade({ r }: { r: Raridade }) {
  return <Text style={{ color: RARIDADE[r].cor, fontWeight: '900', fontSize: 11, letterSpacing: 1 }}>{RARIDADE[r].nome.toUpperCase()}</Text>;
}

/** Cartão grande da peça (drop de chefe, baú e detalhes do inventário), com a descrição das habilidades. */
export function DetalheItem({ item, escuro }: { item: ItemInst; escuro?: boolean }) {
  const t = useTheme();
  const r = RARIDADE[item.raridade];
  const atq = item.slot === 'arma' ? ATAQUE[item.estilo] : null;
  const tinta = escuro ? '#EAF0F5' : t.ink;
  const fraco = escuro ? '#93A3B0' : t.muted;
  return (
    <View style={[styles.detalhe, { backgroundColor: escuro ? '#121B23' : t.surface, borderColor: r.cor, shadowColor: r.cor }]} accessibilityLabel={`${nomeDe(item)}, ${r.nome}`}>
      <ItemIcone item={item} tamanho={84} />
      <View style={{ flex: 1, gap: 3 }}>
        <NomeRaridade r={item.raridade} />
        <Text style={{ color: tinta, fontWeight: '900', fontSize: 17 }}>{nomeDe(item)}</Text>
        <Habilidades item={item} cor={tinta} />
        {atq && <Text style={{ color: fraco, fontSize: 12, fontWeight: '700' }}>{atq.nome}: {atq.texto} Passiva: {atq.passiva}.</Text>}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  slot: { borderRadius: 10, alignItems: 'center', justifyContent: 'center', overflow: 'visible' },
  cartao: { padding: 3 },
  eq: { position: 'absolute', top: -4, right: -4, width: 17, height: 17, borderRadius: 9, backgroundColor: '#2FA84F', alignItems: 'center', justifyContent: 'center', borderWidth: 1.5, borderColor: '#17120E' },
  novo: { position: 'absolute', bottom: -4, backgroundColor: '#FFD25C', borderRadius: 6, paddingHorizontal: 4, paddingVertical: 1 },
  estrelas: { position: 'absolute', top: 1, left: 4, fontSize: 9, fontWeight: '900' },
  detalhe: { flexDirection: 'row', gap: 12, borderWidth: 3, borderRadius: 18, padding: 12, alignItems: 'center', width: '100%', maxWidth: 440, shadowOpacity: 0.55, shadowRadius: 12, shadowOffset: { width: 0, height: 0 } },
});
