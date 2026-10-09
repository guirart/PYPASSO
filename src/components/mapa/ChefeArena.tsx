import { useEffect, useRef, useState } from 'react';
import { Animated, Easing, Image, Platform, StyleSheet, Text, View } from 'react-native';
import type { BossMood } from '../boss-art';
import { SPRITES_CHEFES } from '../chefes-sprites';
import { SpriteQuadro } from './SpriteQuadro';
import { Icone } from '../Icone';
import { BarraVida, Coracoes } from '../crimson';
import { ATAQUE_HEROI_MS, DANO_HEROI_MS, HeroiMana } from './HeroiMana';
import { Slash } from './Slash';
import type { AnimHeroi } from '@/lib/heroi';
import type { Chefe } from '@/lib/mapa';
import { useHeroiVisual } from '@/lib/store';
import { useTheme } from '@/lib/theme';
import { ATAQUE_GOLPE_MS, useQuadro } from './useQuadro';

const nd = Platform.OS !== 'web';
const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

// Fundos de castelo (pixel art, Craftpix "Free Castle Interior Pixel Game Backgrounds"): um por chefe, em rodízio.
const FUNDOS = [
  require('../../../assets/castelo/fundo1.png'), require('../../../assets/castelo/fundo2.png'),
  require('../../../assets/castelo/fundo3.png'), require('../../../assets/castelo/fundo4.png'),
];
const ORDEM_CHEFES = ['aranha', 'besouro', 'escaravelho', 'centopeia', 'gosma', 'diabrete', 'caveira', 'lodo', 'golem', 'dragao'];

function PalcoCastelo({ id, altura, raio, children }: { id: string; altura: number; raio: number; children?: React.ReactNode }) {
  const fundo = FUNDOS[Math.max(0, ORDEM_CHEFES.indexOf(id)) % FUNDOS.length];
  return (
    <View style={{ height: altura, borderRadius: raio, overflow: 'hidden', backgroundColor: '#2B2A28' }}>
      <Image source={fundo} resizeMode="cover" style={[StyleSheet.absoluteFill, pixelado]} />
      <View pointerEvents="none" style={[StyleSheet.absoluteFill, { backgroundColor: 'rgba(8,6,12,0.28)' }]} />
      {children}
    </View>
  );
}

/** O chefe desenhado como personagem. `mood` e `t` escolhem a expressão e o quadro do ataque. */
export function ChefeArte({ chefe, size = 150, mood = 'normal', t = 0.6, morto = false }: { chefe: Chefe; size?: number; mood?: BossMood; t?: number; morto?: boolean }) {
  const sp = SPRITES_CHEFES[chefe.id];
  const [agora, setAgora] = useState(() => Date.now());
  const inicioDano = useRef(0);
  const inicioMorte = useRef(0);
  useEffect(() => { if (morto) inicioMorte.current = Date.now(); }, [morto]);
  useEffect(() => {
    const iv = setInterval(() => setAgora(Date.now()), 60);
    return () => clearInterval(iv);
  }, []);
  useEffect(() => { if (mood === 'hurt') inicioDano.current = Date.now(); }, [mood]);
  // ampliação inteira (pixels nítidos) que cabe na caixa; a caixa é mais larga que alta para os chefes de asas e armas grandes
  const areaW = Math.round(size * 1.45);
  const esc = Math.max(1, Math.floor(Math.min((size * 0.94) / sp.alt, areaW / sp.larg)));
  const folha = morto ? sp.morte : mood === 'attack' ? sp.ataque : mood === 'hurt' ? sp.dano : sp.idle;
  const n = folha.quadros;
  const quadro = morto ? Math.min(n - 1, Math.floor((agora - inicioMorte.current) / 130)) : mood === 'attack' ? Math.floor(t * n) : mood === 'hurt' ? Math.floor(((agora - inicioDano.current) / 550) * n) : Math.floor(agora / 130) % n;
  return (
    <View style={{ width: areaW, height: size }} accessibilityLabel={chefe.nome}>
      <SpriteQuadro folha={folha} escala={esc} cx={sp.cx} pe={sp.pe} quadro={quadro} espelhar areaW={areaW} areaH={size} />
    </View>
  );
}

/** Chefe que reage à luta: ataca (se mexe) quando `ataque` muda e fica ferido quando `golpe` muda. */
function ChefeAnimado({ chefe, size, golpe, ataque, furia, morto }: { chefe: Chefe; size: number; golpe: number; ataque: number; furia?: boolean; morto?: boolean }) {
  const q = useQuadro(golpe, ataque);
  // Em fúria (fase 2 e 3), parado ele fica com a cara brava em vez da neutra
  return <ChefeArte chefe={chefe} size={size} mood={furia && q.mood === 'normal' ? 'attack' : q.mood} t={q.t} morto={morto} />;
}

/**
 * Arena da luta: o chefe em cima com a barra de vida e o personagem da pessoa embaixo.
 * `golpe` e `ataque` são contadores: cada vez que mudam, toca a animação de dano.
 */
export function ChefeArena({ chefe, hp, hpMax, golpe, dano, ataque, bloqueou, vidas, vidasMax, fase = 1, fraco = false, fraqueza, nomeFraqueza }: {
  chefe: Chefe; hp: number; hpMax: number; golpe: number; dano: number; ataque: number; bloqueou: boolean;
  vidas: number; vidasMax: number; fase?: number; fraco?: boolean; fraqueza?: string; nomeFraqueza?: string;
}) {
  const t = useTheme();
  const tremor = useRef(new Animated.Value(0)).current;
  const flash = useRef(new Animated.Value(0)).current;
  const sobe = useRef(new Animated.Value(0)).current;
  const investida = useRef(new Animated.Value(0)).current;
  const vida = useRef(new Animated.Value(hp / hpMax)).current;
  const visual = useHeroiVisual();
  const [morto, setMorto] = useState(false); // cai depois que o último golpe acerta
  useEffect(() => {
    if (hp > 0) { setMorto(false); return; }
    const tm = setTimeout(() => setMorto(true), 450);
    return () => clearTimeout(tm);
  }, [hp]);
  const [heroi, setHeroi] = useState<{ estado: AnimHeroi; desde: number }>(() => ({ estado: 'idle', desde: Date.now() }));

  // O herói golpeia quando a pessoa acerta e se encolhe quando o chefe ataca.
  useEffect(() => {
    if (!golpe) return;
    setHeroi({ estado: golpe % 2 ? 'golpe1' : 'golpe2', desde: Date.now() });
    const tm = setTimeout(() => setHeroi({ estado: 'idle', desde: Date.now() }), ATAQUE_HEROI_MS);
    return () => clearTimeout(tm);
  }, [golpe]);
  useEffect(() => {
    if (!ataque) return;
    const t1 = setTimeout(() => setHeroi({ estado: 'dano', desde: Date.now() }), ATAQUE_GOLPE_MS - 60);
    const t2 = setTimeout(() => setHeroi({ estado: 'idle', desde: Date.now() }), ATAQUE_GOLPE_MS - 60 + DANO_HEROI_MS);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [ataque]);

  useEffect(() => {
    if (!golpe) return;
    tremor.setValue(0); flash.setValue(1); sobe.setValue(0);
    Animated.parallel([
      Animated.sequence([
        Animated.timing(tremor, { toValue: 1, duration: 50, useNativeDriver: nd }),
        Animated.timing(tremor, { toValue: -1, duration: 70, useNativeDriver: nd }),
        Animated.timing(tremor, { toValue: 1, duration: 70, useNativeDriver: nd }),
        Animated.timing(tremor, { toValue: 0, duration: 50, useNativeDriver: nd }),
      ]),
      Animated.timing(flash, { toValue: 0, duration: 450, useNativeDriver: nd }),
      Animated.timing(sobe, { toValue: 1, duration: 900, easing: Easing.out(Easing.cubic), useNativeDriver: nd }),
    ]).start();
  }, [golpe, tremor, flash, sobe]);

  useEffect(() => {
    if (!ataque) return;
    investida.setValue(0);
    Animated.sequence([
      Animated.delay(ATAQUE_GOLPE_MS - 80), // o avanço coincide com o golpe do personagem
      Animated.timing(investida, { toValue: 1, duration: 160, easing: Easing.in(Easing.quad), useNativeDriver: nd }),
      Animated.timing(investida, { toValue: 0, duration: 260, easing: Easing.out(Easing.quad), useNativeDriver: nd }),
    ]).start();
  }, [ataque, investida]);

  useEffect(() => {
    Animated.timing(vida, { toValue: hp / hpMax, duration: 500, easing: Easing.out(Easing.cubic), useNativeDriver: false }).start();
  }, [hp, hpMax, vida]);

  return (
    <PalcoCastelo id={chefe.id} altura={262} raio={20}>
      {fase >= 2 && <View pointerEvents="none" style={[StyleSheet.absoluteFill, { backgroundColor: fase >= 3 ? 'rgba(225,20,30,0.30)' : 'rgba(225,20,30,0.14)' }]} />}
      <View style={styles.topo}>
        <Text style={styles.nome} numberOfLines={1}>{chefe.nome}</Text>
        <BarraVida ratio={vida} hp={hp} hpMax={hpMax} estilo="ornada" esc={3} texto={`${Math.max(0, hp)}/${hpMax}`} rotulo={`Vida do chefe: ${hp} de ${hpMax}`} />
      </View>
      <Animated.View pointerEvents="none" style={[styles.boss, {
        transform: [
          { translateX: tremor.interpolate({ inputRange: [-1, 1], outputRange: [-10, 10] }) },
          { translateY: investida.interpolate({ inputRange: [0, 1], outputRange: [0, 20] }) },
          { scale: investida.interpolate({ inputRange: [0, 1], outputRange: [1, 1.12] }) },
        ],
      }]}>
        <View style={styles.sombra} />
        <View style={{ width: 190, height: 140 }}>
          <ChefeAnimado chefe={chefe} size={140} golpe={golpe} ataque={ataque} furia={fase >= 2} morto={morto} />
          <Animated.View style={[StyleSheet.absoluteFill, { backgroundColor: '#fff', borderRadius: 99, opacity: flash.interpolate({ inputRange: [0, 1], outputRange: [0, 0.55] }) }]} />
          <Slash golpe={golpe} size={128} />
        </View>
      </Animated.View>
      {!!fraqueza && <Text style={[styles.fraca, visual.arma.estilo === fraqueza && styles.fracaOn]}>{visual.arma.estilo === fraqueza ? '★ PONTO FRACO: ' : 'fraco contra: '}{nomeFraqueza}</Text>}
      {golpe > 0 && (
        <Animated.Text pointerEvents="none" style={[styles.dano, {
          opacity: sobe.interpolate({ inputRange: [0, 0.7, 1], outputRange: [1, 1, 0] }),
          transform: [{ translateY: sobe.interpolate({ inputRange: [0, 1], outputRange: [0, -50] }) }, { scale: sobe.interpolate({ inputRange: [0, 0.15, 1], outputRange: [0.6, 1.25, 1] }) }],
        }]}>-{dano}{fraco ? ' ★' : ''}</Animated.Text>
      )}
      <View style={styles.heroi}>
        <View style={{ width: 110, height: 100, marginBottom: -4 }}><HeroiMana look={visual} anim={heroi.estado} desde={heroi.desde} escala={3} areaW={110} areaH={100} /></View>
        <Coracoes vidas={vidas} max={vidasMax} esc={2} />
        {bloqueou && <View style={[styles.escudo, { borderColor: t.sun }]}><Icone nome="escudo" size={18} color="#FFD86B" /></View>}
      </View>
    </PalcoCastelo>
  );
}

const styles = StyleSheet.create({
  topo: { alignItems: 'center', paddingTop: 10, paddingHorizontal: 12, gap: 4 },
  nome: { color: '#fff', fontSize: 16, fontWeight: '900', textShadowColor: 'rgba(0,0,0,0.7)', textShadowRadius: 4, textShadowOffset: { width: 0, height: 1 }, maxWidth: '100%' },
  hpBar: { width: 210, maxWidth: '100%', height: 18, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.45)', overflow: 'hidden', justifyContent: 'center', borderWidth: 2, borderColor: 'rgba(0,0,0,0.6)' },
  hpFill: { position: 'absolute', left: 0, top: 0, bottom: 0, backgroundColor: '#F2545B' },
  hpTxt: { color: '#fff', fontSize: 11, fontWeight: '900', textAlign: 'center', fontVariant: ['tabular-nums'] },
  boss: { position: 'absolute', left: 0, right: 0, bottom: 50, alignItems: 'center' },
  sombra: { position: 'absolute', bottom: -4, width: 96, height: 14, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.3)' },
  fraca: { position: 'absolute', top: 70, alignSelf: 'center', color: 'rgba(255,255,255,0.85)', fontSize: 11, fontWeight: '800', textShadowColor: 'rgba(0,0,0,0.9)', textShadowRadius: 3 },
  fracaOn: { color: '#7EE2FF', fontWeight: '900' },
  dano: { position: 'absolute', top: 100, right: '24%', color: '#FFD86B', fontSize: 34, fontWeight: '900', textShadowColor: '#000', textShadowRadius: 6, textShadowOffset: { width: 0, height: 2 } },
  heroi: { position: 'absolute', left: 6, bottom: 6, alignItems: 'flex-start', gap: 2 },
  heroiAv: { borderRadius: 99, borderWidth: 3, borderColor: '#fff', overflow: 'hidden', backgroundColor: '#fff' },
  vidas: { flexDirection: 'row', gap: 2, backgroundColor: 'rgba(0,0,0,0.3)', borderRadius: 99, paddingHorizontal: 8, paddingVertical: 4 },
  escudo: { borderWidth: 2, borderRadius: 99, padding: 4, backgroundColor: 'rgba(0,0,0,0.3)' },
});