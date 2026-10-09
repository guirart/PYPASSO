import { useEffect, useRef, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, Text, View } from 'react-native';
import { CENARIO_DO_INIMIGO } from '../cenarios';
import { ENEMIES, type EnemyId } from '../enemy-art';
import { BarraVida } from '../crimson';
import { Icone } from '../Icone';
import { CenaPixel } from './CenaPixel';
import { AREA_H, AREA_W, SpriteInimigo } from './SpriteInimigo';
import { ATAQUE_HEROI_MS, DANO_HEROI_MS, HeroiMana, SACAR_MS } from './HeroiMana';
import { SvgXml } from 'react-native-svg';
import { FLECHA_H, FLECHA_SVG, FLECHA_W } from '../arco-art';
import { type AnimHeroi } from '@/lib/heroi';
import { ATAQUE } from '@/lib/itens';
import { useHeroiVisual } from '@/lib/store';
import { Critico, Slash } from './Slash';
import { ATAQUE_GOLPE_MS, useQuadro } from './useQuadro';

const nd = Platform.OS !== 'web';
const ALTURA = 224;
const CHAO = 30; // distância do chão (onde os pés pisam) até a base da cena
const CHEGADA_MS = 2100; // tempo que o herói anda até encontrar o inimigo
// O inimigo só sente o golpe quando a arma (ou a flecha) chega nele. Cada tipo de arma ataca de um jeito.
const SEGURA_MS = { corte: 200, pesado: 260, atordoa: 210, distancia: 500 } as const;
const FLECHA_SAI_MS = 230; // a flecha é solta quando a corda termina de ser puxada
const FLECHA_VOO_MS = 270;

/** Repete um contador com atraso: serve para o inimigo reagir quando a espada do herói o alcança. */
function useAtraso(valor: number, ms: number) {
  const [x, setX] = useState(valor);
  useEffect(() => { const t = setTimeout(() => setX(valor), ms); return () => clearTimeout(t); }, [valor, ms]);
  return x;
}

/**
 * A batalha no alto da lição, em pixel art: o herói anda pelo cenário, encontra o inimigo e os dois lutam.
 * A cada exercício certo o herói avança e golpeia (o inimigo perde vida e fica ferido); a cada erro o inimigo ataca.
 * `golpe` e `ataque` são contadores: cada vez que mudam, toca a animação.
 */
export function InimigoBarra({ id, elite, hp, hpMax, golpe, ataque, critico, escondeu, dano, pontoFraco, fraqueza, nomeFraqueza }: { id: EnemyId; elite?: boolean; hp: number; hpMax: number; golpe: number; ataque: number; critico?: boolean; escondeu?: boolean; dano?: number; pontoFraco?: boolean; fraqueza?: string; nomeFraqueza?: string }) {
  const [larg, setLarg] = useState(380);
  const [andando, setAndando] = useState(true);
  const visual = useHeroiVisual(); // o herói com as peças equipadas no Inventário
  const modo = ATAQUE[visual.arma.estilo]?.modo ?? 'corte';
  const [heroi, setHeroi] = useState<{ estado: AnimHeroi; desde: number }>(() => ({ estado: 'andar', desde: Date.now() }));
  const golpeInimigo = useAtraso(golpe, SEGURA_MS[modo]);
  const hpAtraso = useAtraso(hp, SEGURA_MS[modo]); // o inimigo só cai depois do último golpe chegar
  const morto = hpAtraso <= 0 && hpMax > 0;
  const sobeDano = useRef(new Animated.Value(0)).current;
  const [tonto, setTonto] = useState(false); // maça: o inimigo fica atordoado
  const tremor = useRef(new Animated.Value(0)).current; // machado: a tela treme no impacto
  const flecha = useRef(new Animated.Value(0)).current; // arco: 0 = na mão, 1 = acertou
  const [flechaVoa, setFlechaVoa] = useState(false);
  const q = useQuadro(golpeInimigo, ataque);
  const entra = useRef(new Animated.Value(1)).current; // 1 = inimigo fora da cena (à direita), 0 = no lugar
  const avanco = useRef(new Animated.Value(0)).current; // o quanto o herói avançou no golpe
  const vida = useRef(new Animated.Value(hp / Math.max(1, hpMax))).current;
  const heroiX = larg * 0.2;
  const inimigoX = larg * 0.74;
  const distancia = (inimigoX - heroiX) * (modo === 'pesado' ? 0.5 : modo === 'atordoa' ? 0.38 : modo === 'distancia' ? 0 : 0.4);

  // Chegada: o herói anda, o cenário desliza e o inimigo vem ao encontro dele.
  useEffect(() => {
    setAndando(true); setHeroi({ estado: 'andar', desde: Date.now() });
    entra.setValue(1);
    Animated.timing(entra, { toValue: 0, duration: CHEGADA_MS - 100, easing: Easing.out(Easing.cubic), useNativeDriver: nd }).start();
    // Encontrou o inimigo: para de andar, saca a arma e fica em guarda.
    const t1 = setTimeout(() => { setAndando(false); setHeroi({ estado: 'sacar', desde: Date.now() }); }, CHEGADA_MS);
    const t2 = setTimeout(() => setHeroi({ estado: 'idle', desde: Date.now() }), CHEGADA_MS + SACAR_MS);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [id, entra]);

  // Acerto: cada arma ataca de um jeito. Espada e maça avançam (a maça atordoa), o machado avança mais e faz tremer, o arco atira de longe.
  useEffect(() => {
    if (!golpe) return;
    setHeroi({ estado: golpe % 2 ? 'golpe1' : 'golpe2', desde: Date.now() }); // alterna os dois golpes
    avanco.setValue(0);
    const lento = modo === 'pesado' ? 1.3 : 1;
    if (modo !== 'distancia') {
      Animated.sequence([
        Animated.timing(avanco, { toValue: distancia, duration: 160 * lento, easing: Easing.out(Easing.quad), useNativeDriver: nd }),
        Animated.delay(120 * lento),
        Animated.timing(avanco, { toValue: 0, duration: 200, easing: Easing.in(Easing.quad), useNativeDriver: nd }),
      ]).start();
    }
    const timers: ReturnType<typeof setTimeout>[] = [];
    if (modo === 'pesado') {
      timers.push(setTimeout(() => {
        tremor.setValue(0);
        Animated.sequence([6, -5, 4, -3, 0].map((v) => Animated.timing(tremor, { toValue: v, duration: 45, useNativeDriver: nd }))).start();
      }, SEGURA_MS.pesado));
    }
    if (modo === 'atordoa') {
      timers.push(setTimeout(() => setTonto(true), SEGURA_MS.atordoa), setTimeout(() => setTonto(false), SEGURA_MS.atordoa + 950));
    }
    if (modo === 'distancia') {
      flecha.setValue(0);
      timers.push(setTimeout(() => {
        setFlechaVoa(true);
        Animated.timing(flecha, { toValue: 1, duration: FLECHA_VOO_MS, easing: Easing.linear, useNativeDriver: nd }).start(() => setFlechaVoa(false));
      }, FLECHA_SAI_MS));
    }
    timers.push(setTimeout(() => setHeroi({ estado: 'idle', desde: Date.now() }), ATAQUE_HEROI_MS));
    return () => timers.forEach(clearTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [golpe]);

  // Erro: o inimigo ataca e, quando o golpe dele chega, o herói reage.
  useEffect(() => {
    if (!ataque) return;
    const t1 = setTimeout(() => setHeroi({ estado: 'dano', desde: Date.now() }), ATAQUE_GOLPE_MS - 60);
    const t2 = setTimeout(() => setHeroi({ estado: 'idle', desde: Date.now() }), ATAQUE_GOLPE_MS - 60 + DANO_HEROI_MS);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [ataque]);

  // número do dano subindo em cima do inimigo quando o golpe chega
  useEffect(() => {
    if (!golpeInimigo || dano === undefined) return;
    sobeDano.setValue(0);
    Animated.timing(sobeDano, { toValue: 1, duration: 900, easing: Easing.out(Easing.cubic), useNativeDriver: nd }).start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [golpeInimigo]);

  useEffect(() => {
    Animated.timing(vida, { toValue: hp / Math.max(1, hpMax), duration: 450, easing: Easing.out(Easing.cubic), useNativeDriver: false }).start();
  }, [hp, hpMax, vida]);

  const info = ENEMIES[id];
  return (
    <View style={styles.fora} accessibilityLabel={`${info.nome}${elite ? ', elite' : ''}: ${hp} de ${hpMax} de vida`}>
      <View style={styles.cena} onLayout={(e) => setLarg(e.nativeEvent.layout.width)}>
        <Animated.View style={[StyleSheet.absoluteFill, { transform: [{ translateX: tremor }] }]}>
        <CenaPixel cenario={CENARIO_DO_INIMIGO[id]} larg={larg} andando={andando} />

        <View style={[styles.topo, { left: inimigoX - 100 }]}>
          <View style={styles.nomeLinha}>
            {elite && <Icone nome="coroa" size={16} color="#FFD43B" />}
            <Text style={styles.nome} numberOfLines={1}>{info.nome}</Text>
            {elite && <Text style={styles.tag}>ELITE</Text>}
          </View>
          <BarraVida ratio={vida} hp={hp} hpMax={hpMax} estilo="simples" esc={3} texto={`${Math.max(0, hp)}/${hpMax}`} />
          {!!fraqueza && <Text style={[styles.fraco, visual.arma.estilo === fraqueza && styles.fracoOn]}>{visual.arma.estilo === fraqueza ? '★ PONTO FRACO: ' : 'fraco contra: '}{nomeFraqueza}</Text>}
        </View>

        <Animated.View pointerEvents="none" style={[styles.personagem, { left: heroiX - AREA_W / 2, transform: [{ translateX: avanco }] }]}>
          <View style={styles.sombra} />
          <HeroiMana look={visual} anim={heroi.estado} desde={heroi.desde} />
        </Animated.View>

        <Animated.View pointerEvents="none" style={[styles.personagem, { left: inimigoX - AREA_W / 2, transform: [{ translateX: entra.interpolate({ inputRange: [0, 1], outputRange: [0, larg * 0.5] }) }] }]}>
          <View style={styles.sombra} />
          <SpriteInimigo id={id} mood={q.mood} t={q.t} morto={morto} />
          <Slash golpe={golpeInimigo} size={110} forte={critico} />
          {critico && <Slash golpe={golpeInimigo} size={110} forte cruz />}
          {critico && <Critico golpe={golpeInimigo} />}
        </Animated.View>

        {flechaVoa && (
          <Animated.View pointerEvents="none" style={{ position: 'absolute', bottom: CHAO + 36, left: 0, transform: [{ translateX: flecha.interpolate({ inputRange: [0, 1], outputRange: [heroiX + 38, inimigoX - 30] }) }] }}>
            <SvgXml xml={FLECHA_SVG} width={FLECHA_W * 2.5} height={FLECHA_H * 2.5} />
          </Animated.View>
        )}
        {!!golpeInimigo && dano !== undefined && !morto && (
          <Animated.View pointerEvents="none" style={{ position: 'absolute', left: inimigoX - 50, width: 100, bottom: CHAO + 62, alignItems: 'center', opacity: sobeDano.interpolate({ inputRange: [0, 0.7, 1], outputRange: [1, 1, 0] }), transform: [{ translateY: sobeDano.interpolate({ inputRange: [0, 1], outputRange: [0, -34] }) }, { scale: sobeDano.interpolate({ inputRange: [0, 0.15, 1], outputRange: [0.6, 1.2, 1] }) }] }}>
            <Text style={[styles.danoNum, critico && { color: '#FF9F43', fontSize: 26 }]}>-{dano}</Text>
            {pontoFraco && <Text style={styles.danoFraco}>PONTO FRACO!</Text>}
          </Animated.View>
        )}
        {tonto && <Text style={[styles.estrelas, { left: inimigoX - 40, bottom: CHAO + 100 }]}>★ ★ ★</Text>}
        </Animated.View>

        <Text style={styles.fala} numberOfLines={1}>{escondeu ? 'Escondeu parte do código: complete para acertar em cheio (dano x2)!' : `“${info.fala}”`}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  fora: { marginHorizontal: 16, maxWidth: 728, alignSelf: 'center', width: '100%' },
  cena: { height: ALTURA, borderRadius: 18, overflow: 'hidden', backgroundColor: '#0B0A1A' },
  topo: { position: 'absolute', top: 8, width: 200, alignItems: 'center', gap: 4 },
  nomeLinha: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  nome: { color: '#fff', fontSize: 15, fontWeight: '900', flexShrink: 1, textShadowColor: 'rgba(0,0,0,0.85)', textShadowRadius: 4, textShadowOffset: { width: 0, height: 1 } },
  tag: { color: '#fff', backgroundColor: '#F2545B', fontWeight: '900', fontSize: 10, letterSpacing: 1, borderRadius: 6, paddingHorizontal: 6, paddingVertical: 1, overflow: 'hidden' },
  barra: { width: 190, maxWidth: '100%', height: 16, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.55)', overflow: 'hidden', justifyContent: 'center', borderWidth: 2, borderColor: 'rgba(0,0,0,0.7)' },
  cheia: { position: 'absolute', left: 0, top: 0, bottom: 0, backgroundColor: '#F2545B' },
  hpTxt: { color: '#fff', fontSize: 10, fontWeight: '900', textAlign: 'center', fontVariant: ['tabular-nums'] },
  personagem: { position: 'absolute', bottom: CHAO, width: AREA_W, height: AREA_H },
  sombra: { position: 'absolute', bottom: -3, left: AREA_W / 2 - 40, width: 80, height: 10, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.35)' },
  fraco: { color: 'rgba(255,255,255,0.8)', fontSize: 11, fontWeight: '800', textShadowColor: 'rgba(0,0,0,0.9)', textShadowRadius: 3 },
  fracoOn: { color: '#7EE2FF', fontWeight: '900' },
  danoNum: { color: '#FFD86B', fontSize: 22, fontWeight: '900', textShadowColor: '#000', textShadowRadius: 5, textShadowOffset: { width: 0, height: 2 } },
  danoFraco: { color: '#7EE2FF', fontSize: 11, fontWeight: '900', letterSpacing: 1, textShadowColor: '#000', textShadowRadius: 4 },
  estrelas: { position: 'absolute', width: 80, textAlign: 'center', color: '#FFD43B', fontSize: 18, fontWeight: '900', letterSpacing: 2, textShadowColor: 'rgba(0,0,0,0.8)', textShadowRadius: 3 },
  fala: { position: 'absolute', bottom: 6, left: 12, right: 12, textAlign: 'center', color: '#fff', fontSize: 11, fontWeight: '700', fontStyle: 'italic', textShadowColor: 'rgba(0,0,0,0.9)', textShadowRadius: 3, textShadowOffset: { width: 0, height: 1 } },
});
