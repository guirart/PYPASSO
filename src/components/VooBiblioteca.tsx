import * as Haptics from 'expo-haptics';
import { forwardRef, useImperativeHandle, useRef, useState } from 'react';
import { AccessibilityInfo, Animated, Easing, Platform, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { highlight } from './CodeBlock';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { SvgXml } from 'react-native-svg';
import { mono, useTheme } from '@/lib/theme';
import { LIVRO_BASE, LIVRO_CAPA, LIVRO_CAPA_DENTRO, LIVRO_H, LIVRO_W } from './livro-art';

export type Conceito = { titulo: string; nomes: string[]; corpo?: string; codigo?: string; saida?: string };
export type VooRef = { voar: (c: Conceito) => void };

const nativo = Platform.OS !== 'web';
const LW = LIVRO_W; // livro no meio da tela
const LH = LIVRO_H;
const NO_CANTO = 0.48; // tamanho do livro quando fica no canto

const rodar = (a: Animated.CompositeAnimation) => new Promise<void>((ok) => a.start(() => ok()));
const esperar = (ms: number) => new Promise<void>((ok) => setTimeout(ok, ms));

/**
 * Quando a pessoa aprende um conceito novo, o cartão dele sai voando da tela para dentro de
 * um livro: a capa abre, o cartão mergulha nas páginas, a capa fecha, o livro pula com "+1"
 * e vai para o canto (onde mostra quantos conceitos entraram na Biblioteca nesta lição).
 * Tocar no livro do canto abre o livro no meio da tela e mostra de novo os conceitos
 * guardados nesta lição. Fora isso, fica por cima da lição sem bloquear toques.
 */
export const VooBiblioteca = forwardRef<VooRef>(function VooBiblioteca(_props, ref) {
  const t = useTheme();
  const insets = useSafeAreaInsets();
  const { width, height } = useWindowDimensions();
  const [cartao, setCartao] = useState<Conceito | null>(null);
  const [rotulo, setRotulo] = useState('');
  const [total, setTotal] = useState(0);
  const [guardados, setGuardados] = useState<Conceito[]>([]);
  const [noCanto, setNoCanto] = useState(false); // livro parado no canto (pode ser tocado)
  const [aberto, setAberto] = useState(false); // revendo os conceitos
  const [pagina, setPagina] = useState(0);
  const revisao = useRef(new Animated.Value(0)).current; // cartão de revisão saindo do livro
  const fundo = useRef(new Animated.Value(0)).current; // tela escurecida

  const aparece = useRef(new Animated.Value(0)).current; // livro surge
  const canto = useRef(new Animated.Value(0)).current; // 0 = meio da tela, 1 = canto
  const tampa = useRef(new Animated.Value(0)).current; // 0 = fechado, 1 = aberto
  const brilho = useRef(new Animated.Value(0)).current;
  const pulo = useRef(new Animated.Value(1)).current;
  const voo = useRef(new Animated.Value(0)).current; // cartão: 0 = na tela, 1 = dentro do livro
  const cartaoIn = useRef(new Animated.Value(0)).current;
  const sobe = useRef(new Animated.Value(0)).current;
  const fila = useRef<Conceito[]>([]);
  const rodando = useRef(false);
  const jaApareceu = useRef(false);

  // posições
  const largura = Math.min(width, 760);
  const margem = (width - largura) / 2;
  const meioX = width / 2;
  const meioY = height * 0.62;
  const cantoX = width - margem - 16 - (LW * NO_CANTO) / 2;
  const cantoY = insets.top + 62 + (LH * NO_CANTO) / 2;
  const cartaoY = height * 0.27;

  async function processar() {
    if (rodando.current) return;
    rodando.current = true;
    setNoCanto(false);
    while (fila.current.length) {
      const c = fila.current.shift()!;
      // 1. o livro vem para o meio da tela (ou surge, na primeira vez) e o cartão aparece
      voo.setValue(0); cartaoIn.setValue(0); tampa.setValue(0);
      setCartao(c);
      await rodar(Animated.parallel([
        jaApareceu.current
          ? Animated.timing(canto, { toValue: 0, duration: 380, easing: Easing.out(Easing.cubic), useNativeDriver: nativo })
          : Animated.spring(aparece, { toValue: 1, friction: 7, tension: 140, useNativeDriver: nativo }),
        Animated.spring(cartaoIn, { toValue: 1, friction: 7, tension: 160, useNativeDriver: nativo }),
      ]));
      jaApareceu.current = true;
      // 2. a capa abre e as páginas brilham
      await rodar(Animated.parallel([
        Animated.timing(tampa, { toValue: 1, duration: 360, easing: Easing.out(Easing.back(1.4)), useNativeDriver: nativo }),
        Animated.timing(brilho, { toValue: 1, duration: 360, useNativeDriver: nativo }),
      ]));
      await esperar(180);
      // 3. o cartão sai voando para dentro do livro
      await rodar(Animated.timing(voo, { toValue: 1, duration: 640, easing: Easing.in(Easing.cubic), useNativeDriver: nativo }));
      setCartao(null);
      setGuardados((g) => [...g, c]);
      // 4. a capa fecha, o livro pula e mostra "+1"
      if (nativo) Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium).catch(() => {});
      setTotal((n) => n + c.nomes.length);
      setRotulo(`+${c.nomes.length} ${c.nomes.join(', ')}`);
      sobe.setValue(0);
      Animated.timing(sobe, { toValue: 1, duration: 1100, easing: Easing.out(Easing.quad), useNativeDriver: nativo }).start();
      await rodar(Animated.parallel([
        Animated.timing(tampa, { toValue: 0, duration: 260, easing: Easing.in(Easing.quad), useNativeDriver: nativo }),
        Animated.timing(brilho, { toValue: 0, duration: 260, useNativeDriver: nativo }),
      ]));
      pulo.setValue(1.25);
      Animated.spring(pulo, { toValue: 1, friction: 3, tension: 170, useNativeDriver: nativo }).start();
      await esperar(fila.current.length ? 250 : 650);
      // 5. o livro vai para o canto (se não houver outro conceito na fila)
      if (!fila.current.length) {
        await rodar(Animated.timing(canto, { toValue: 1, duration: 460, easing: Easing.inOut(Easing.cubic), useNativeDriver: nativo }));
      }
    }
    rodando.current = false;
    setNoCanto(true);
  }

  /** Toque no livro do canto: ele vem para o meio, abre e mostra os conceitos de novo. */
  async function abrirLivro() {
    if (rodando.current || aberto || !guardados.length) return;
    rodando.current = true;
    setPagina(guardados.length - 1);
    setAberto(true);
    if (nativo) Haptics.selectionAsync().catch(() => {});
    await rodar(Animated.parallel([
      Animated.timing(fundo, { toValue: 1, duration: 300, useNativeDriver: nativo }),
      Animated.timing(canto, { toValue: 0, duration: 420, easing: Easing.out(Easing.cubic), useNativeDriver: nativo }),
    ]));
    await rodar(Animated.parallel([
      Animated.timing(tampa, { toValue: 1, duration: 360, easing: Easing.out(Easing.back(1.4)), useNativeDriver: nativo }),
      Animated.timing(brilho, { toValue: 1, duration: 360, useNativeDriver: nativo }),
    ]));
    await rodar(Animated.spring(revisao, { toValue: 1, friction: 7, tension: 90, useNativeDriver: nativo }));
    rodando.current = false;
  }

  /** "Fechar livro": o cartão volta para as páginas, a capa fecha e o livro volta ao canto. */
  async function fecharLivro() {
    if (rodando.current) return;
    rodando.current = true;
    await rodar(Animated.timing(revisao, { toValue: 0, duration: 420, easing: Easing.in(Easing.cubic), useNativeDriver: nativo }));
    await rodar(Animated.parallel([
      Animated.timing(tampa, { toValue: 0, duration: 260, easing: Easing.in(Easing.quad), useNativeDriver: nativo }),
      Animated.timing(brilho, { toValue: 0, duration: 260, useNativeDriver: nativo }),
    ]));
    await rodar(Animated.parallel([
      Animated.timing(canto, { toValue: 1, duration: 420, easing: Easing.inOut(Easing.cubic), useNativeDriver: nativo }),
      Animated.timing(fundo, { toValue: 0, duration: 420, useNativeDriver: nativo }),
    ]));
    setAberto(false);
    rodando.current = false;
  }

  useImperativeHandle(ref, () => ({
    voar(c) {
      if (!c.nomes.length) return;
      AccessibilityInfo.announceForAccessibility?.(`Novo na sua biblioteca: ${c.nomes.join(', ')}`);
      fila.current.push(c);
      processar();
    },
  }));

  // a frente da capa (emblema) só aparece enquanto ela não passou da metade da abertura
  const frente = tampa.interpolate({ inputRange: [0, 0.45, 0.55, 1], outputRange: [1, 1, 0, 0] });
  // capa: gira pela lombada (lado esquerdo do livro)
  const capaRot = tampa.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '-168deg'] });
  const livroX = canto.interpolate({ inputRange: [0, 1], outputRange: [0, cantoX - meioX] });
  const livroY = canto.interpolate({ inputRange: [0, 1], outputRange: [0, cantoY - meioY] });
  const livroEscala = Animated.multiply(Animated.multiply(aparece, pulo), canto.interpolate({ inputRange: [0, 1], outputRange: [1, NO_CANTO] }));

  return (
    <View pointerEvents="box-none" style={StyleSheet.absoluteFill}>
      {/* fundo escurecido enquanto o livro está aberto para revisão */}
      {aberto && (
        <Animated.View style={[StyleSheet.absoluteFill, { backgroundColor: 'rgba(10, 20, 30, 0.55)', opacity: fundo }]}>
          <Pressable style={StyleSheet.absoluteFill} onPress={fecharLivro} accessibilityLabel="Fechar o livro" />
        </Animated.View>
      )}
      {/* o cartão do conceito, saindo da tela */}
      {cartao && (
        <Animated.View style={[styles.cartao, {
          top: cartaoY - 70, left: width / 2 - Math.min(340, width - 40) / 2, width: Math.min(340, width - 40),
          backgroundColor: t.surface, borderColor: t.sun,
          opacity: voo.interpolate({ inputRange: [0, 0.85, 1], outputRange: [1, 1, 0] }),
          transform: [
            { translateY: voo.interpolate({ inputRange: [0, 0.3, 1], outputRange: [0, -30, meioY - cartaoY - 4] }) },
            { scale: Animated.multiply(cartaoIn, voo.interpolate({ inputRange: [0, 1], outputRange: [1, 0.1] })) },
            { rotate: voo.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '8deg'] }) },
          ],
        }]}>
          <Text style={[styles.eyebrow, { color: t.sunDeep }]}>NOVO CONCEITO</Text>
          <Text style={[styles.titulo, { color: t.ink }]} numberOfLines={2}>{cartao.titulo}</Text>
          <View style={styles.chips}>
            {cartao.nomes.map((n) => (
              <Text key={n} style={[styles.chip, { color: t.brand, borderColor: t.line, fontFamily: mono }]}>{n}</Text>
            ))}
          </View>
          <Text style={[styles.dica, { color: t.muted }]}>Guardando na sua Biblioteca…</Text>
        </Animated.View>
      )}

      {/* o livro */}
      <Animated.View pointerEvents={noCanto && !aberto ? 'auto' : 'none'} style={[styles.livro, {
        left: meioX - LW / 2, top: meioY - LH / 2,
        opacity: aparece,
        transform: [{ translateX: livroX }, { translateY: livroY }, { scale: livroEscala }],
      }]}>
        {/* brilho saindo das páginas */}
        <Animated.View style={[styles.brilho, { opacity: brilho, transform: [{ scale: brilho.interpolate({ inputRange: [0, 1], outputRange: [0.6, 1.25] }) }] }]} />
        {/* contracapa, páginas (com texto e código) e fitinha */}
        <View style={styles.base}><SvgXml xml={LIVRO_BASE} width={LW} height={LW * 104 / 118} /></View>
        {/* capa dura bege: abre e fecha pela lombada */}
        <Animated.View style={[styles.capa, { transform: [{ perspective: 700 }, { rotateY: capaRot }] }]}>
          <SvgXml xml={LIVRO_CAPA_DENTRO} width={LW} height={LH} />
          <Animated.View style={[StyleSheet.absoluteFill, { opacity: frente }]}>
            <SvgXml xml={LIVRO_CAPA} width={LW} height={LH} />
          </Animated.View>
        </Animated.View>
        {total > 0 && <Text style={[styles.conta, { backgroundColor: t.brand }]}>{total}</Text>}
        {!!rotulo && (
          <Animated.Text numberOfLines={1} style={[styles.rotulo, { color: t.sunDeep, backgroundColor: t.surface, borderColor: t.sun,
            opacity: sobe.interpolate({ inputRange: [0, 0.1, 0.75, 1], outputRange: [0, 1, 1, 0] }),
            transform: [{ translateY: sobe.interpolate({ inputRange: [0, 1], outputRange: [0, -34] }) }] }]}>
            {rotulo}
          </Animated.Text>
        )}
        {/* área de toque por cima do desenho */}
        <Pressable onPress={abrirLivro} accessibilityRole="button" style={StyleSheet.absoluteFill} hitSlop={12}
          accessibilityLabel={`Abrir o livro da Biblioteca: ${total} ${total === 1 ? 'conceito novo' : 'conceitos novos'} nesta lição`} />
      </Animated.View>

      {/* revisão: o conceito sai do livro aberto e aparece de novo */}
      {aberto && guardados[pagina] && (() => {
        const c = guardados[pagina];
        const topo = insets.top + 24;
        const altura = meioY - LH / 2 - 24 - topo;
        return (
          <Animated.View style={[styles.revisao, {
            top: topo, maxHeight: altura, left: width / 2 - Math.min(380, width - 32) / 2, width: Math.min(380, width - 32),
            backgroundColor: t.surface, borderColor: '#B98B3A',
            opacity: revisao.interpolate({ inputRange: [0, 0.2, 1], outputRange: [0, 1, 1] }),
            transform: [
              { translateY: revisao.interpolate({ inputRange: [0, 1], outputRange: [meioY - topo - 40, 0] }) },
              { scale: revisao.interpolate({ inputRange: [0, 1], outputRange: [0.12, 1] }) },
            ],
          }]}>
            <View style={styles.revTopo}>
              <Text style={[styles.eyebrow, { color: '#8A6428' }]}>NA SUA BIBLIOTECA</Text>
              {guardados.length > 1 && <Text style={{ color: t.muted, fontWeight: '800' }}>{pagina + 1} de {guardados.length}</Text>}
            </View>
            <ScrollView style={{ flexGrow: 0 }} contentContainerStyle={{ gap: 8 }}>
              <Text style={[styles.titulo, { color: t.ink }]}>{c.titulo}</Text>
              <View style={styles.chips}>
                {c.nomes.map((n) => <Text key={n} style={[styles.chip, { color: t.brand, borderColor: t.line, fontFamily: mono }]}>{n}</Text>)}
              </View>
              {!!c.corpo && <Text style={{ color: t.ink, fontSize: 15, lineHeight: 21, fontWeight: '600' }}>{c.corpo}</Text>}
              {!!c.codigo && (
                <View style={[styles.codigo, { backgroundColor: t.codeBg }]}>
                  <Text style={{ color: t.codeFg, fontFamily: mono, fontSize: 14, lineHeight: 21 }}>{highlight(c.codigo, t)}</Text>
                </View>
              )}
              {!!c.saida && (
                <View style={[styles.saida, { borderColor: t.line }]}>
                  <Text style={{ color: t.muted, fontWeight: '900', fontSize: 11, letterSpacing: 1 }}>SAÍDA</Text>
                  <Text style={{ color: t.ink, fontFamily: mono, fontSize: 14 }}>{c.saida}</Text>
                </View>
              )}
            </ScrollView>
            <View style={styles.revBotoes}>
              {guardados.length > 1 && (
                <Pressable onPress={() => setPagina((p) => Math.max(0, p - 1))} disabled={pagina === 0} accessibilityLabel="Conceito anterior"
                  style={[styles.seta, { borderColor: t.line, opacity: pagina === 0 ? 0.35 : 1 }]}><Text style={[styles.setaTxt, { color: t.ink }]}>‹</Text></Pressable>
              )}
              <Pressable onPress={fecharLivro} accessibilityRole="button" style={[styles.fechar, { backgroundColor: '#B98B3A' }]}>
                <Text style={styles.fecharTxt}>Fechar livro</Text>
              </Pressable>
              {guardados.length > 1 && (
                <Pressable onPress={() => setPagina((p) => Math.min(guardados.length - 1, p + 1))} disabled={pagina === guardados.length - 1} accessibilityLabel="Próximo conceito"
                  style={[styles.seta, { borderColor: t.line, opacity: pagina === guardados.length - 1 ? 0.35 : 1 }]}><Text style={[styles.setaTxt, { color: t.ink }]}>›</Text></Pressable>
              )}
            </View>
          </Animated.View>
        );
      })()}
    </View>
  );
});

const styles = StyleSheet.create({
  cartao: { position: 'absolute', borderWidth: 3, borderBottomWidth: 6, borderRadius: 20, padding: 16, gap: 6, shadowColor: '#000', shadowOpacity: 0.2, shadowRadius: 16, shadowOffset: { width: 0, height: 8 }, elevation: 8 },
  eyebrow: { fontSize: 12, fontWeight: '900', letterSpacing: 1.2 },
  titulo: { fontSize: 20, fontWeight: '900' },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  chip: { borderWidth: 2, borderRadius: 10, paddingHorizontal: 8, paddingVertical: 3, fontSize: 16, fontWeight: '800', overflow: 'hidden' },
  dica: { fontSize: 12, fontWeight: '700' },
  livro: { position: 'absolute', width: LW, height: LH },
  brilho: { position: 'absolute', left: -LW - 10, right: -14, top: -26, bottom: -10, borderRadius: 90, backgroundColor: 'rgba(255, 226, 150, 0.6)' },
  base: { position: 'absolute', left: 0, top: -4 },
  revisao: { position: 'absolute', borderWidth: 3, borderBottomWidth: 6, borderRadius: 20, padding: 16, gap: 10, shadowColor: '#000', shadowOpacity: 0.25, shadowRadius: 18, shadowOffset: { width: 0, height: 8 }, elevation: 10 },
  revTopo: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  codigo: { borderRadius: 12, padding: 12 },
  saida: { borderWidth: 2, borderRadius: 12, padding: 10, gap: 2 },
  revBotoes: { flexDirection: 'row', gap: 8, alignItems: 'center' },
  seta: { width: 44, height: 44, borderWidth: 2, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  setaTxt: { fontSize: 26, fontWeight: '900', marginTop: -3 },
  fechar: { flex: 1, height: 44, borderRadius: 12, alignItems: 'center', justifyContent: 'center', borderBottomWidth: 4, borderBottomColor: '#8A6428' },
  fecharTxt: { color: '#fff', fontWeight: '900', fontSize: 15, letterSpacing: 0.6, textTransform: 'uppercase' },
  capa: { position: 'absolute', left: 0, top: 0, width: LW, height: LH, transformOrigin: 'left center', backfaceVisibility: 'visible' },
  conta: { position: 'absolute', top: -10, right: -10, minWidth: 30, height: 30, borderRadius: 15, color: '#fff', fontWeight: '900', fontSize: 16, textAlign: 'center', lineHeight: 30, overflow: 'hidden', paddingHorizontal: 6 },
  rotulo: { position: 'absolute', top: -40, alignSelf: 'center', fontWeight: '900', fontSize: 15, borderWidth: 2, borderRadius: 99, paddingHorizontal: 10, paddingVertical: 3, overflow: 'hidden', maxWidth: 240 },
});
