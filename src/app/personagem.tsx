import { router } from 'expo-router';
import { useRef, useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Cross } from '@/components/Icons';
import { OPCOES } from '@/components/mana-sprites';
import { CenaPixel } from '@/components/mapa/CenaPixel';
import { HeroiMana } from '@/components/mapa/HeroiMana';
import { duracao, heroiAleatorio, normalizarHeroi, type AnimHeroi } from '@/lib/heroi';
import { useGame, useHeroiVisual } from '@/lib/store';
import { useTheme } from '@/lib/theme';

/** Aparência do herói: pele e cabelo (grátis). As peças de equipamento ficam na aba Inventário. */
export default function PersonagemScreen() {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const base = normalizarHeroi(useGame((s) => s.heroi));
  const visual = useHeroiVisual();
  const setHeroi = useGame((s) => s.setHeroi);
  const [larg, setLarg] = useState(360);
  const [anim, setAnim] = useState<{ a: AnimHeroi; desde: number }>({ a: 'idle', desde: Date.now() });
  const volta = useRef<ReturnType<typeof setTimeout> | null>(null);

  const tocar = (a: AnimHeroi) => {
    if (volta.current) clearTimeout(volta.current);
    setAnim({ a, desde: Date.now() });
    if (a !== 'idle' && a !== 'andar') volta.current = setTimeout(() => setAnim({ a: 'idle', desde: Date.now() }), duracao(a) + 40);
  };

  const Chip = ({ texto, ativo, onPress, rotulo }: { texto: string; ativo: boolean; onPress: () => void; rotulo: string }) => (
    <Pressable onPress={onPress} accessibilityRole="button" accessibilityState={{ selected: ativo }} accessibilityLabel={rotulo}
      style={[styles.chip, { backgroundColor: ativo ? t.brand : t.surface, borderColor: ativo ? t.brand : t.line }]}>
      <Text style={{ color: ativo ? '#fff' : t.ink, fontWeight: '800', fontSize: 13 }}>{texto}</Text>
    </Pressable>
  );
  const Bolinhas = ({ cores, atual, onPress, rotulo }: { cores: { id: string; cor: string }[]; atual?: string; onPress: (id: string) => void; rotulo: string }) => (
    <View style={styles.bolinhas}>
      {cores.map((c, i) => (
        <Pressable key={c.id} onPress={() => onPress(c.id)} accessibilityRole="button" accessibilityState={{ selected: atual === c.id }} accessibilityLabel={`${rotulo}, cor ${i + 1}`}
          style={[styles.bolinha, { backgroundColor: c.cor, borderColor: atual === c.id ? t.brand : t.line, borderWidth: atual === c.id ? 4 : 2 }]} />
      ))}
    </View>
  );

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.head, { paddingTop: insets.top + 10, borderBottomColor: t.line }]}>
        <Pressable onPress={() => router.back()} accessibilityLabel="Fechar" hitSlop={10}><Cross color={t.muted} size={26} /></Pressable>
        <Text style={[styles.h1, { color: t.ink }]}>Aparência</Text>
      </View>
      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 28 }]}>
        <View style={styles.palco} onLayout={(e) => setLarg(e.nativeEvent.layout.width)}>
          <CenaPixel cenario="montanha" larg={larg} andando={anim.a === 'andar'} />
          <View style={styles.heroi}><HeroiMana look={visual} anim={anim.a} desde={anim.desde} escala={5} areaW={260} areaH={190} /></View>
        </View>
        <View style={styles.acoes}>
          <Chip texto="Parado" ativo={anim.a === 'idle'} onPress={() => tocar('idle')} rotulo="Ver parado" />
          <Chip texto="Andar" ativo={anim.a === 'andar'} onPress={() => tocar('andar')} rotulo="Ver andando" />
          <Chip texto="Golpe" ativo={false} onPress={() => tocar(anim.desde % 2 ? 'golpe1' : 'golpe2')} rotulo="Ver golpe" />
          <Chip texto="Sortear" ativo={false} onPress={() => { const a = heroiAleatorio(); setHeroi({ ...base, pele: a.pele, cabelo: a.cabelo }); }} rotulo="Sortear a aparência" />
        </View>

        <View style={[styles.grupo, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.muted, fontWeight: '900', fontSize: 11, letterSpacing: 0.8 }}>PELE</Text>
          <Bolinhas cores={OPCOES.pele} atual={base.pele} onPress={(id) => setHeroi({ ...base, pele: id })} rotulo="Pele" />
        </View>
        <View style={[styles.grupo, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Text style={{ color: t.muted, fontWeight: '900', fontSize: 11, letterSpacing: 0.8 }}>CABELO</Text>
          <View style={styles.chips}>
            <Chip texto="Nenhum" ativo={!base.cabelo} onPress={() => setHeroi({ ...base, cabelo: null })} rotulo="Cabelo: nenhum" />
            {OPCOES.cabelo.estilos.map((e) => <Chip key={e.id} texto={e.nome} ativo={base.cabelo?.estilo === e.id} onPress={() => setHeroi({ ...base, cabelo: { estilo: e.id, cor: base.cabelo?.cor ?? OPCOES.cabelo.cores[0].id } })} rotulo={`Cabelo: ${e.nome}`} />)}
          </View>
          {base.cabelo && <Bolinhas cores={OPCOES.cabelo.cores} atual={base.cabelo.cor} onPress={(id) => setHeroi({ ...base, cabelo: { ...base.cabelo!, cor: id } })} rotulo="Cabelo" />}
          {visual.chapeu?.estilo === 'pfht' && !!base.cabelo && <Text style={{ color: t.muted, fontSize: 12 }}>A touca que você está usando cobre o cabelo.</Text>}
        </View>
        <Text style={{ color: t.muted, fontSize: 12, lineHeight: 17 }}>
          Armas, escudo, roupa e chapéu ficam na aba Inventário. Arte do herói: Mana Seed Character Base (demo), de Seliel the Shaper.
        </Text>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  head: { flexDirection: 'row', alignItems: 'center', gap: 14, paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1 },
  h1: { flex: 1, fontSize: 22, fontWeight: '900' },
  scroll: { padding: 16, gap: 12, maxWidth: 640, width: '100%', alignSelf: 'center' },
  palco: { height: 220, borderRadius: 18, overflow: 'hidden', backgroundColor: '#2B1E3A' },
  heroi: { position: 'absolute', left: 0, right: 0, bottom: 14, alignItems: 'center' },
  acoes: { flexDirection: 'row', gap: 8, flexWrap: 'wrap', justifyContent: 'center' },
  grupo: { borderWidth: 2, borderRadius: 16, padding: 12, gap: 10 },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  chip: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 14, paddingVertical: 7 },
  bolinhas: { flexDirection: 'row', flexWrap: 'wrap', gap: 10 },
  bolinha: { width: 36, height: 36, borderRadius: 18 },
});
