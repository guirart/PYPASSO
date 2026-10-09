import { router } from 'expo-router';
import { useState } from 'react';
import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { Button3D } from '../Button3D';
import { Icone } from '../Icone';
import { Moeda } from '../Moeda';
import { NoHex } from './NoHex';
import { lessonById } from '@/content';
import type { Unit } from '@/content/types';
import { cenaDaUnidade, especialId, TITULOS } from '@/lib/especiais';
import { chefeDaZona, hash, INFO_NO, MAX_RELIQUIAS, misterioDoNo, reliquia, sortearReliquia, type Mapa, type No } from '@/lib/mapa';
import { usePlus } from '@/lib/plus';
import { vencidos } from '@/lib/revisao';
import { MAX_HEARTS, rotaVazia, useGame } from '@/lib/store';
import { useTheme } from '@/lib/theme';

type Resultado = { titulo: string; texto: string; moedas?: number; reliquia?: string | null };

/** Folha de baixo ao tocar num nó: explica o nó e resolve fogueira, mistério e tesouro. */
export function NoSheet({ no, unit, indice, livre, fechar }: {
  no: No | null; mapa: Mapa; unit: Unit; indice: number; livre: boolean; fechar: () => void;
}) {
  const t = useTheme();
  const g = useGame();
  const plus = usePlus((s) => s.ativo);
  const [res, setRes] = useState<Resultado | null>(null);
  if (!no) return null;
  const info = INFO_NO[no.tipo];
  const rota = g.rotas?.[unit.id] ?? rotaVazia();
  const visitado = rota.visitados.includes(no.id) || (no.tipo === 'chefe' && `fogo-${unit.id}` in g.done);
  const licao = no.licao ? lessonById(no.licao) : null;
  const sair = () => { setRes(null); fechar(); };
  const chegar = () => g.visitar(unit.id, no.id);
  const relNova = (sufixo: string) => sortearReliquia(rota.reliquias, `${no.id}${sufixo}`);

  const entrarLicao = () => {
    if (!no.licao) return;
    sair();
    if (!plus && g.hearts <= 0) { router.push('/plus'); return; }
    router.push({ pathname: '/lesson/[id]', params: { id: no.licao, zona: unit.id, no: no.id, ...(no.tipo === 'elite' ? { modo: 'elite' } : {}) } });
  };

  // ---------------- eventos
  const descansar = () => {
    chegar();
    if (plus || g.hearts >= MAX_HEARTS) { g.ganharMoedas(15); setRes({ titulo: 'Descanso tranquilo', texto: 'Suas vidas já estavam cheias, então o Pipo te deu umas moedas.', moedas: 15 }); return; }
    const novas = Math.min(MAX_HEARTS, g.hearts + 2);
    useGame.setState({ hearts: novas, heartTs: novas >= MAX_HEARTS ? 0 : g.heartTs });
    setRes({ titulo: 'Você descansou', texto: `+${novas - g.hearts} vidas. Bora pro próximo desafio!` });
  };
  const treinar = () => { chegar(); sair(); router.push(vencidos(g.revisao).length ? '/lesson/revisao' : '/lesson/pratica'); };
  const lerCodigo = () => { chegar(); sair(); router.push(`/especial/${especialId(cenaDaUnidade(indice), unit.id)}`); };
  const abrirTesouro = () => {
    chegar();
    const m = 25 + (hash(no.id) % 5) * 5;
    g.ganharMoedas(m);
    const r = relNova('t');
    if (r) g.ganharReliquia(unit.id, r);
    setRes({ titulo: 'Baú aberto!', texto: r ? 'Moedas e uma relíquia para esta expedição.' : 'Moedas para a sua bolsa.', moedas: m, reliquia: r });
  };
  const comprarReliquia = (r: string) => {
    chegar();
    g.ganharMoedas(-40);
    g.ganharReliquia(unit.id, r);
    setRes({ titulo: 'Negócio fechado', texto: 'O mercador piscou e sumiu na névoa.', reliquia: r });
  };
  const bauSuspeito = () => {
    chegar();
    g.ganharMoedas(40);
    if (!plus) g.loseHeart();
    setRes({ titulo: 'Tinha um bug dentro!', texto: plus ? '+40 moedas. O bug tentou morder, mas o Plus protegeu suas vidas.' : '+40 moedas, mas o bug te mordeu: -1 vida.', moedas: 40 });
  };
  const seguir = () => { chegar(); setRes({ titulo: 'Você seguiu viagem', texto: 'Às vezes o melhor é não mexer em código que você não conhece.' }); };

  const chefe = no.tipo === 'chefe' ? chefeDaZona(indice) : null;

  return (
    <Modal visible transparent animationType="slide" onRequestClose={sair}>
      <Pressable style={styles.fundo} onPress={sair} accessibilityLabel="Fechar">
        <Pressable style={[styles.folha, { backgroundColor: t.bg, borderColor: t.line }]} onPress={() => {}}>
          <ScrollView contentContainerStyle={{ gap: 12 }}>
            <View style={styles.topo}>
              <NoHex tipo={no.tipo} size={64} estado={visitado ? 'visitado' : 'futuro'} />
              <View style={{ flex: 1 }}>
                <Text style={[styles.eyebrow, { color: info.cor[1] }]}>{info.nome.toUpperCase()}{licao ? ` · LIÇÃO ${licao.lessonIndex + 1}` : ''}</Text>
                <Text style={[styles.h, { color: t.ink }]}>{chefe ? chefe.nome : licao ? licao.title : info.nome}</Text>
              </View>
            </View>

            {res ? (
              <View style={{ gap: 10 }}>
                <Text style={[styles.h2, { color: t.ink }]}>{res.titulo}</Text>
                <Text style={[styles.txt, { color: t.muted }]}>{res.texto}</Text>
                {!!res.moedas && <View style={styles.linha}><Moeda size={22} /><Text style={[styles.h2, { color: t.sunDeep }]}>+{res.moedas}</Text></View>}
                {res.reliquia && <CartaoReliquia id={res.reliquia} />}
                <Button3D label="Continuar" onPress={sair} />
              </View>
            ) : (
              <>
                <Text style={[styles.txt, { color: t.muted }]}>{chefe ? `"${chefe.fala}" Ache o bug em cada código antes do tempo acabar: cada acerto tira vida do chefe.` : info.texto}</Text>
                {!livre && !visitado && <Text style={[styles.aviso, { color: t.sunDeep, borderColor: t.sun }]}>Siga um caminho ligado ao seu personagem para chegar aqui.</Text>}

                {(no.tipo === 'batalha' || no.tipo === 'elite') && (
                  <>
                    {no.tipo === 'elite' && <Premios itens={['3x moedas', '+50% XP', 'relíquia']} />}
                    {(livre || visitado) && <Button3D label={visitado ? 'Refazer lição' : no.tipo === 'elite' ? 'Enfrentar elite' : 'Entrar na batalha'} variant={no.tipo === 'elite' ? 'bad' : 'brand'} onPress={entrarLicao} />}
                  </>
                )}

                {no.tipo === 'cura' && livre && (
                  <View style={{ gap: 8 }}>
                    <Opcao icone="coracao" titulo="Descansar" texto={plus ? 'Vidas ilimitadas: ganhe 15 moedas.' : '+2 vidas agora.'} onPress={descansar} />
                    <Opcao icone="cerebro" titulo="Treinar" texto={vencidos(g.revisao).length ? 'Faça a Revisão do que você errou.' : 'Um treino rápido com o que você já viu.'} onPress={treinar} />
                    <Opcao icone="livro" titulo={TITULOS[cenaDaUnidade(indice)]} texto="Um exercício especial do Pipo com esta zona." onPress={lerCodigo} />
                  </View>
                )}

                {no.tipo === 'tesouro' && livre && <Button3D label="Abrir o baú" variant="sun" onPress={abrirTesouro} />}

                {no.tipo === 'misterio' && livre && (() => {
                  const ev = misterioDoNo(no.id);
                  if (ev === 'pergaminho') return (
                    <View style={{ gap: 8 }}>
                      <Text style={[styles.h2, { color: t.ink }]}>Um pergaminho antigo</Text>
                      <Text style={[styles.txt, { color: t.muted }]}>Tem código escrito nele, meio apagado. O Pipo quer ver se você consegue ler.</Text>
                      <Button3D label={TITULOS[cenaDaUnidade(indice)]} onPress={lerCodigo} />
                      <Button3D label="Seguir viagem" variant="ghost" onPress={seguir} />
                    </View>
                  );
                  if (ev === 'mercador') {
                    const r = relNova('m');
                    return (
                      <View style={{ gap: 8 }}>
                        <Text style={[styles.h2, { color: t.ink }]}>Um mercador encapuzado</Text>
                        <Text style={[styles.txt, { color: t.muted }]}>{r ? 'Ele oferece uma relíquia por 40 moedas.' : 'Ele não tem nada que você ainda não tenha.'}</Text>
                        {r && <CartaoReliquia id={r} />}
                        {r && <Button3D label={g.moedas >= 40 ? 'Comprar por 40 moedas' : `Faltam ${40 - g.moedas} moedas`} variant="sun" disabled={g.moedas < 40} onPress={() => comprarReliquia(r)} />}
                        <Button3D label="Seguir viagem" variant="ghost" onPress={seguir} />
                      </View>
                    );
                  }
                  return (
                    <View style={{ gap: 8 }}>
                      <Text style={[styles.h2, { color: t.ink }]}>Um baú suspeito</Text>
                      <Text style={[styles.txt, { color: t.muted }]}>Dá para ouvir algo se mexendo lá dentro. Pode ter moedas... ou um bug.</Text>
                      <Button3D label="Abrir mesmo assim" variant="bad" onPress={bauSuspeito} />
                      <Button3D label="Deixar pra lá" variant="ghost" onPress={seguir} />
                    </View>
                  );
                })()}

                {no.tipo === 'chefe' && (
                  <>
                    <Premios itens={['50 moedas na 1ª vitória', 'libera a próxima zona']} />
                    {(livre || visitado) && <Button3D label={visitado ? 'Lutar de novo' : 'Enfrentar o chefe'} variant="bad" onPress={() => { sair(); router.push({ pathname: '/prova', params: { unit: unit.id } }); }} />}
                  </>
                )}

                {(no.tipo === 'cura' || no.tipo === 'tesouro' || no.tipo === 'misterio') && visitado && (
                  <Text style={[styles.txt, { color: t.muted }]}>Você já passou por aqui nesta expedição.</Text>
                )}
              </>
            )}
            <Text style={[styles.rel, { color: t.muted }]}>Relíquias: {rota.reliquias.length}/{MAX_RELIQUIAS}</Text>
          </ScrollView>
        </Pressable>
      </Pressable>
    </Modal>
  );
}

function Opcao({ icone, titulo, texto, onPress }: { icone: 'coracao' | 'cerebro' | 'livro'; titulo: string; texto: string; onPress: () => void }) {
  const t = useTheme();
  return (
    <Pressable onPress={onPress} accessibilityRole="button" style={({ pressed }) => [styles.opcao, { borderColor: t.line, backgroundColor: t.surface, borderBottomWidth: pressed ? 2 : 4 }]}>
      <View style={[styles.opIc, { backgroundColor: t.brand }]}><Icone nome={icone} size={22} color="#fff" /></View>
      <View style={{ flex: 1 }}>
        <Text style={{ color: t.ink, fontWeight: '900', fontSize: 16 }}>{titulo}</Text>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{texto}</Text>
      </View>
    </Pressable>
  );
}

function Premios({ itens }: { itens: string[] }) {
  const t = useTheme();
  return (
    <View style={styles.premios}>
      {itens.map((i) => <Text key={i} style={[styles.premio, { color: t.sunDeep, borderColor: t.sun, backgroundColor: t.surface }]}>{i}</Text>)}
    </View>
  );
}

export function CartaoReliquia({ id }: { id: string }) {
  const t = useTheme();
  const r = reliquia(id);
  if (!r) return null;
  return (
    <View style={[styles.relCard, { borderColor: t.sun, backgroundColor: t.surface }]}>
      <View style={styles.relIc}><Icone nome={r.icone} size={30} color="#7A5300" /></View>
      <View style={{ flex: 1 }}>
        <Text style={{ color: t.ink, fontWeight: '900' }}>{r.nome}</Text>
        <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{r.texto}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  fundo: { flex: 1, backgroundColor: 'rgba(0,0,0,0.45)', justifyContent: 'flex-end' },
  folha: { borderTopLeftRadius: 24, borderTopRightRadius: 24, borderWidth: 2, padding: 18, paddingBottom: 32, maxHeight: '85%', width: '100%', maxWidth: 560, alignSelf: 'center' },
  topo: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  eyebrow: { fontSize: 12, fontWeight: '900', letterSpacing: 1 },
  h: { fontSize: 22, fontWeight: '900' },
  h2: { fontSize: 18, fontWeight: '900' },
  txt: { fontSize: 15, fontWeight: '600', lineHeight: 21 },
  aviso: { borderWidth: 2, borderRadius: 12, padding: 10, fontWeight: '800' },
  linha: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  opcao: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, padding: 12 },
  opIc: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  premios: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  premio: { borderWidth: 2, borderRadius: 99, paddingHorizontal: 10, paddingVertical: 4, fontWeight: '900', fontSize: 12, overflow: 'hidden' },
  rel: { fontSize: 12, fontWeight: '700', textAlign: 'center' },
  relCard: { flexDirection: 'row', alignItems: 'center', gap: 12, borderWidth: 2, borderRadius: 16, padding: 12 },
  relIc: { width: 48, height: 48, borderRadius: 14, backgroundColor: '#FFD86B', alignItems: 'center', justifyContent: 'center' },
});
