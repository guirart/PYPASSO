import { useEffect, useMemo, useRef, useState } from 'react';
import { Animated, Easing, Pressable, StyleSheet, Text, View } from 'react-native';
import type { ModeloBau } from '@/lib/baus';
import { RARIDADE, type ItemInst } from '@/lib/itens';
import { ALT_BAU, ImagemBau, LARG_BAU } from './baus-sprites';
import { DetalheItem } from './CartaoItem';

const ARCO_IRIS = ['#FF4D4D', '#FF9F43', '#FFE14D', '#4DDB6A', '#3CC8FF', '#4D6BFF', '#B14DFF', '#FF4DC8'];
const VOLTAS = 4;
const DURACAO_CORES = 3200;
const ESC = 6; // ampliação do baú (pixels inteiros)

/**
 * A abertura do baú: ele treme e brilha passando por várias cores, a troca de cor vai desacelerando até parar na cor da
 * raridade da peça; aí o baú abre numa explosão de luz e a peça aparece. O sorteio já foi feito: a animação só revela.
 */
export function BauAnimado({ item, bau, onFim }: { item: ItemInst; bau: ModeloBau; onFim: () => void }) {
  const r = RARIDADE[item.raridade];
  const cores = useMemo(() => [...Array.from({ length: VOLTAS }, () => ARCO_IRIS).flat(), r.cor], [r.cor]);
  const ciclo = useRef(new Animated.Value(0)).current;
  const treme = useRef(new Animated.Value(0)).current;
  const giro = useRef(new Animated.Value(0)).current;
  const pulo = useRef(new Animated.Value(0)).current;
  const clarao = useRef(new Animated.Value(0)).current;
  const peca = useRef(new Animated.Value(0)).current;
  const [fase, setFase] = useState<'brilhando' | 'aberto'>('brilhando');
  const feito = useRef(false);

  const cor = ciclo.interpolate({ inputRange: cores.map((_, i) => i), outputRange: cores });

  const abrir = () => {
    if (feito.current) return;
    feito.current = true;
    setFase('aberto');
    clarao.setValue(1);
    Animated.parallel([
      Animated.sequence([
        Animated.timing(pulo, { toValue: 1, duration: 140, easing: Easing.out(Easing.quad), useNativeDriver: false }),
        Animated.timing(pulo, { toValue: 0, duration: 220, easing: Easing.in(Easing.quad), useNativeDriver: false }),
      ]),
      Animated.timing(clarao, { toValue: 0, duration: 650, useNativeDriver: false }),
      Animated.sequence([Animated.delay(350), Animated.spring(peca, { toValue: 1, friction: 6, tension: 80, useNativeDriver: false })]),
    ]).start();
  };

  useEffect(() => {
    giro.setValue(0);
    const gira = Animated.loop(Animated.timing(giro, { toValue: 1, duration: 9000, easing: Easing.linear, useNativeDriver: false }));
    gira.start();
    const sacode = Animated.loop(Animated.sequence([
      Animated.timing(treme, { toValue: 1, duration: 60, useNativeDriver: false }),
      Animated.timing(treme, { toValue: -1, duration: 60, useNativeDriver: false }),
    ]));
    sacode.start();
    // as cores passam depressa e vão desacelerando até parar na cor da raridade
    Animated.timing(ciclo, { toValue: cores.length - 1, duration: DURACAO_CORES, easing: Easing.out(Easing.cubic), useNativeDriver: false }).start(({ finished }) => {
      if (!finished) return;
      sacode.stop(); treme.setValue(0);
      abrir();
    });
    return () => { gira.stop(); sacode.stop(); ciclo.stopAnimation(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const pular = () => {
    ciclo.stopAnimation(); ciclo.setValue(cores.length - 1); treme.setValue(0);
    abrir();
  };

  const raios = Array.from({ length: 12 }, (_, i) => i);

  return (
    <View style={styles.fundo} accessibilityViewIsModal>
      <View style={styles.palco}>
        <View style={styles.centro}>
          {/* aura e raios na cor que está passando */}
          <Animated.View pointerEvents="none" style={[styles.aura, { backgroundColor: cor, opacity: fase === 'aberto' ? 0.28 : 0.4 }]} />
          <Animated.View pointerEvents="none" style={[styles.aura2, { backgroundColor: cor, opacity: 0.35 }]} />
          <Animated.View pointerEvents="none" style={[styles.raios, { transform: [{ rotate: giro.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] }) }] }]}>
            {raios.map((i) => (
              <View key={i} style={[styles.raioBase, { transform: [{ rotate: `${i * 30}deg` }] }]}>
                <Animated.View style={[styles.raio, { backgroundColor: cor, opacity: fase === 'aberto' ? 0.45 : 0.3 }]} />
              </View>
            ))}
          </Animated.View>

          {/* o baú: fechado até a cor assentar, depois o quadro aberto */}
          <Animated.View style={{ alignItems: 'center', transform: [{ translateX: treme.interpolate({ inputRange: [-1, 1], outputRange: [-4, 4] }) }, { translateY: pulo.interpolate({ inputRange: [0, 1], outputRange: [0, -16] }) }] }}>
            <View style={{ width: LARG_BAU * ESC, height: ALT_BAU * ESC }}><ImagemBau modelo={bau} aberto={fase === 'aberto'} esc={ESC} /></View>
            <View style={styles.sombra} />
          </Animated.View>
        </View>

        {/* clarão branco na abertura */}
        <Animated.View pointerEvents="none" style={[StyleSheet.absoluteFill, { backgroundColor: '#fff', opacity: clarao }]} />

        {/* a peça sobe do baú */}
        {fase === 'aberto' && (
          <Animated.View style={[styles.peca, { opacity: peca, transform: [{ translateY: peca.interpolate({ inputRange: [0, 1], outputRange: [60, 0] }) }, { scale: peca.interpolate({ inputRange: [0, 1], outputRange: [0.6, 1] }) }] }]}>
            <Text style={[styles.titulo, { color: r.cor }]} accessibilityLiveRegion="polite">PEÇA {r.nome.toUpperCase()}!</Text>
            <DetalheItem item={item} escuro />
            <Pressable onPress={onFim} accessibilityRole="button" accessibilityLabel="Pegar a peça" style={[styles.btn, { backgroundColor: r.cor }]}>
              <Text style={{ color: '#1B1208', fontWeight: '900', fontSize: 16 }}>PEGAR</Text>
            </Pressable>
          </Animated.View>
        )}
      </View>

      {fase === 'brilhando' && (
        <View style={styles.rodape}>
          <Text style={{ color: '#EFE3C2', fontWeight: '900', fontSize: 16 }}>Abrindo {bau.nome.toLowerCase().replace('baú', 'o baú')}…</Text>
          <Pressable onPress={pular} accessibilityRole="button" accessibilityLabel="Pular a animação" style={styles.pular}>
            <Text style={{ color: '#EFE3C2', fontWeight: '800', fontSize: 13 }}>Pular</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  fundo: { position: 'absolute', left: 0, right: 0, top: 0, bottom: 0, backgroundColor: 'rgba(6,10,14,0.94)', zIndex: 50, alignItems: 'center', justifyContent: 'center' },
  palco: { width: '100%', maxWidth: 460, minHeight: 560, alignItems: 'center', justifyContent: 'center', overflow: 'hidden' },
  centro: { width: '100%', height: 340, alignItems: 'center', justifyContent: 'center', transform: [{ translateY: -110 }] },
  aura: { position: 'absolute', width: 300, height: 300, borderRadius: 150 },
  aura2: { position: 'absolute', width: 190, height: 190, borderRadius: 95 },
  raios: { position: 'absolute', width: 340, height: 340, alignItems: 'center', justifyContent: 'center' },
  raioBase: { position: 'absolute', width: 340, height: 340, alignItems: 'center' },
  raio: { width: 8, height: 170, borderTopLeftRadius: 4, borderTopRightRadius: 4 },
  sombra: { width: 130, height: 12, borderRadius: 99, backgroundColor: 'rgba(0,0,0,0.5)', marginTop: 4 },
  peca: { position: 'absolute', left: 12, right: 12, bottom: 18, alignItems: 'center', gap: 12 },
  titulo: { fontSize: 22, fontWeight: '900', letterSpacing: 1.5, textShadowColor: 'rgba(0,0,0,0.8)', textShadowRadius: 6 },
  btn: { borderRadius: 14, paddingVertical: 12, paddingHorizontal: 40 },
  rodape: { position: 'absolute', bottom: 30, alignItems: 'center', gap: 10 },
  pular: { borderWidth: 2, borderColor: '#6E5E48', borderRadius: 99, paddingHorizontal: 18, paddingVertical: 6 },
});
