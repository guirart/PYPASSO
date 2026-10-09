import { missoesDoDia, nivelDe } from '@/lib/gamificacao';
import { router } from 'expo-router';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Modal, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import Svg, { Polygon } from 'react-native-svg';
import { Button3D } from '@/components/Button3D';
import { Mascot } from '@/components/Characters';
import { Icone } from '@/components/Icone';
import { disponiveis, MapaZona } from '@/components/mapa/MapaZona';
import { NoHex } from '@/components/mapa/NoHex';
import { CartaoReliquia, NoSheet } from '@/components/mapa/NoSheet';
import { Moeda } from '@/components/Moeda';
import { HudTopo } from '@/components/HudTopo';
import { TopStats } from '@/components/TopStats';
import { LESSONS_BY_TRACK, TRACKS, courseOf } from '@/content';
import { PROJETOS } from '@/content/projetos';
import { gerarMapa, INFO_NO, RELIQUIAS, reliquia, type Mapa, type No, type TipoNo } from '@/lib/mapa';
import { vencidos } from '@/lib/revisao';
import { dayKey, rotaVazia, useGame, yesterdayKey, type Rota } from '@/lib/store';
import { metaDiaria, META_PADRAO } from '@/lib/metas';
import { EVENTO_NIVEL, META_EVENTO } from '@/lib/evento';
import { weekId } from '@/lib/leagues';
import { serieAtual } from '@/lib/desafio';
import { useEscuro, useTheme } from '@/lib/theme';

/** Avança sozinho por lições que a pessoa já tinha feito antes do mapa existir. */
function autoAvanco(m: Mapa, rota: Rota, done: Record<string, number>, chefeVencido: boolean): Rota | null {
  const r: Rota = { ...rota, visitados: [...rota.visitados] };
  let mudou = false;
  const linhasLicao = m.linhas.map((l) => l[0]?.licao ?? null);
  for (let passo = 0; passo < 40; passo++) {
    const pos = r.pos && m.nos[r.pos] ? m.nos[r.pos] : m.entrada;
    const filhos = pos.liga.map((k) => m.nos[k]);
    if (!filhos.length) break;
    if (filhos[0].tipo === 'chefe') {
      if (chefeVencido && !r.visitados.includes(filhos[0].id)) { r.visitados.push(filhos[0].id); r.pos = filhos[0].id; mudou = true; }
      break;
    }
    const linha = filhos[0].linha;
    const lic = linhasLicao[linha];
    const proxLicao = linhasLicao.slice(linha).find((x) => x) ?? null;
    const pode = lic ? lic in done : proxLicao ? proxLicao in done : chefeVencido;
    if (!pode) break;
    const escolha = filhos.find((f) => f.tipo === 'batalha' || f.tipo === 'cura') ?? filhos[0];
    r.visitados.push(escolha.id); r.pos = escolha.id; mudou = true;
  }
  return mudou ? r : null;
}

export default function AprenderScreen() {
  const t = useTheme();
  const escuro = useEscuro();
  const insets = useSafeAreaInsets();
  const g = useGame();
  const { done, dayXP, track, setTrack, fire, revisao, projetos, rotas, semente } = g;
  const course = courseOf(track);
  const units = course.units;
  const fireBest = Math.max(0, ...Object.values(fire ?? {}));
  const nRev = vencidos(revisao).length;
  const DAILY_GOAL = metaDiaria(g.xpDias, dayKey()); // meta adaptativa: a média dos seus últimos dias de estudo
  const recDuelos = Object.values(g.duelos ?? {}).reduce((s, r) => ({ v: s.v + r.v, d: s.d + r.d }), { v: 0, d: 0 });
  const desafioFeito = !!g.desafio?.feito && g.desafio.dia === dayKey();
  const serieDesafio = serieAtual(g.desafio, dayKey(), yesterdayKey());
  const projLivres = PROJETOS.filter((p) => p.requer in done).length;
  const projFeitos = PROJETOS.filter((p) => projetos?.[p.id]?.feito).length;
  const anyDone = Object.keys(done).length > 0;

  const aberta = (i: number) => i === 0 || `fogo-${units[i - 1].id}` in done;
  const vencida = (i: number) => `fogo-${units[i].id}` in done;
  const primeiraAberta = units.findIndex((_, i) => aberta(i) && !vencida(i));
  const zonaAtual = primeiraAberta === -1 ? units.length - 1 : primeiraAberta;
  const [sel, setSel] = useState<number | null>(null);
  useEffect(() => { setSel(null); }, [track]);
  const zi = Math.min(sel ?? zonaAtual, units.length - 1);
  const unit = units[zi];
  const rota = rotas?.[unit.id] ?? rotaVazia();
  const licoes = useMemo(() => LESSONS_BY_TRACK[track].filter((l) => l.unitIndex === zi).map((l) => l.id), [track, zi]);
  const mapa = useMemo(() => gerarMapa(unit.id, licoes, `${semente ?? 'x'}:${rota.exp}`), [unit.id, licoes, semente, rota.exp]);
  const zonaAberta = aberta(zi);
  const chefeVencido = vencida(zi);

  // Progresso antigo (antes do mapa): o personagem já começa depois das lições feitas.
  useEffect(() => {
    const novo = autoAvanco(mapa, rota, done, chefeVencido);
    if (novo) useGame.setState((s) => ({ rotas: { ...(s.rotas ?? {}), [unit.id]: novo } }));
  }, [mapa, rota, done, chefeVencido, unit.id]);

  const [no, setNo] = useState<No | null>(null);
  const [info, setInfo] = useState(false);
  const missoesProntas = (() => {
    const h = g.hoje;
    if (!h) return 0;
    const ev = nivelDe(g.xp).nivel >= EVENTO_NIVEL && g.evento?.semana === weekId() && g.evento.pontos >= META_EVENTO && !g.evento.resgatado ? 1 : 0; // evento liberado e pronto
    return missoesDoDia(h.dia).filter((x) => !h.resgatadas.includes(x.id) && (h.c[x.evento] ?? 0) >= x.meta).length + (h.resgatadas.length >= 3 && !h.bau ? 1 : 0) + ev;
  })();
  const [ultimaPython, setUltimaPython] = useState<'main' | 'builtins' | 'libs'>('main'); // última trilha de Python aberta
  useEffect(() => { if (track !== 'logica') setUltimaPython(track); }, [track]);
  const topico = track === 'logica' ? 'logica' : 'python';
  const [mais, setMais] = useState(false); // seção "Mais atividades" recolhida para a tela ficar limpa
  const livres = disponiveis(mapa, rota);
  const feitasZona = licoes.filter((l) => l in done).length;

  return (
    <View style={{ flex: 1, backgroundColor: t.bg }}>
      <View style={[styles.header, { paddingTop: insets.top + 8, borderBottomColor: t.line, backgroundColor: t.bg }]}>
        <View style={styles.logo}><Mascot size={34} animated={false} /><Text style={[styles.logoText, { color: t.brand }]}>PyPasso</Text></View>
        <TopStats />
      </View>

      <ScrollView contentContainerStyle={styles.scroll}>
        <HudTopo />
        <View style={[styles.tracks, { backgroundColor: t.surface, borderColor: t.line }]} accessibilityRole="tablist">
          {([['python', 'Python', ultimaPython], ['logica', 'Lógica', 'logica']] as const).map(([k, nome, destino]) => {
            const on = topico === k;
            const lic = (k === 'python' ? ['main', 'builtins', 'libs'] as const : ['logica'] as const).flatMap((id) => LESSONS_BY_TRACK[id]);
            return (
              <Pressable key={k} onPress={() => setTrack(destino)} accessibilityRole="tab" accessibilityLabel={`Tópico: ${nome}`} accessibilityState={{ selected: on }}
                style={[styles.trackBtn, on && { backgroundColor: t.brand }]}>
                <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '900', fontSize: 16 }}>{nome}</Text>
                <Text style={{ color: on ? 'rgba(255,255,255,0.85)' : t.muted, fontWeight: '700', fontSize: 11 }}>{lic.filter((l) => l.id in done).length}/{lic.length} lições</Text>
              </Pressable>
            );
          })}
        </View>
        {topico === 'python' && (
          <View style={[styles.tracks, { backgroundColor: t.surface, borderColor: t.line }]} accessibilityRole="tablist">
            {TRACKS.filter((tr) => tr.id !== 'logica').map((tr) => {
              const on = tr.id === track;
              const n = LESSONS_BY_TRACK[tr.id].filter((l) => l.id in done).length;
              return (
                <Pressable key={tr.id} onPress={() => setTrack(tr.id)} accessibilityRole="tab" accessibilityState={{ selected: on }}
                  style={[styles.trackBtn, on && { backgroundColor: t.brand }]}>
                  <Text style={{ color: on ? '#fff' : t.ink, fontWeight: '900', fontSize: 14 }}>{tr.short}</Text>
                  <Text style={{ color: on ? 'rgba(255,255,255,0.85)' : t.muted, fontWeight: '700', fontSize: 11 }}>{n}/{LESSONS_BY_TRACK[tr.id].length} lições</Text>
                </Pressable>
              );
            })}
          </View>
        )}

        <View style={styles.meta} accessibilityLabel={`Meta diária: ${Math.min(dayXP, DAILY_GOAL)} de ${DAILY_GOAL} XP`}>
          <Icone nome="alvo" size={18} color={t.sunDeep} />
          <Text style={[styles.metaTxt, { color: t.ink }]}>{DAILY_GOAL === META_PADRAO ? 'Meta diária' : 'Sua meta'}</Text>
          <View style={[styles.bar, { backgroundColor: t.line }]}>
            <View style={[styles.barFill, { backgroundColor: t.sun, width: `${Math.min(100, (dayXP / DAILY_GOAL) * 100)}%` }]} />
          </View>
          <Text style={[styles.metaNum, { color: t.muted }]}>{Math.min(dayXP, DAILY_GOAL)}/{DAILY_GOAL} XP</Text>
        </View>

        {track === 'logica' ? <ListaLogica /> : (
        <View style={[styles.zona, { borderColor: t.line, backgroundColor: t.surface }]}>
          <View style={styles.zonaTopo}>
            <HexNumero n={zi + 1} cor={chefeVencido ? '#E0A21C' : zonaAberta ? '#3FB85A' : '#8592A3'} />
            <View style={{ flex: 1 }}>
              <Text style={[styles.eyebrow, { color: t.muted }]} numberOfLines={1}>{(unit.group ?? `ZONA ${zi + 1} DE ${units.length}`).toUpperCase()}</Text>
              <Text style={[styles.zonaNome, { color: t.ink }]} numberOfLines={1}>{unit.title}</Text>
              <Text style={[styles.zonaSub, { color: chefeVencido ? t.sunDeep : zonaAberta ? t.good : t.muted }]}>
                {chefeVencido ? 'Zona conquistada' : zonaAberta ? `Em andamento · ${feitasZona}/${licoes.length} lições` : `Derrote o chefe da zona ${zi} para entrar`}
              </Text>
            </View>
            <Pressable onPress={() => setInfo(true)} accessibilityRole="button" accessibilityLabel="Legenda do mapa" style={[styles.infoBtn, { borderColor: t.line, backgroundColor: t.bg }]}>
              <Icone nome="info" size={18} color={t.brand} /><Text style={{ color: t.ink, fontWeight: '900', fontSize: 13 }}>Legenda</Text>
            </Pressable>
          </View>

          <View style={styles.mapaLinha}>
            <View style={{ flex: 1, borderRadius: 18, overflow: 'hidden' }}>
              <MapaZona mapa={mapa} rota={rota} indice={zi} zonaAberta={zonaAberta} chefeVencido={chefeVencido} escuro={escuro}
                avatar={g.avatarSeed} moldura={g.moldura} onNo={(n) => setNo(n)} />
            </View>
            <TrilhoZonas total={units.length} atual={zi} aberta={aberta} vencida={vencida} onZona={setSel} />
          </View>

          <View style={styles.expedicao}>
            <View style={{ flex: 1, gap: 6 }}>
              <Text style={[styles.cap, { color: t.muted }]}>RELÍQUIAS DA EXPEDIÇÃO</Text>
              <View style={{ flexDirection: 'row', gap: 6 }}>
                {[0, 1, 2].map((k) => {
                  const r = reliquia(rota.reliquias[k] ?? '');
                  return (
                    <Pressable key={k} onPress={() => setInfo(true)} accessibilityLabel={r ? r.nome : 'Espaço vazio de relíquia'}
                      style={[styles.slot, { borderColor: r ? '#C8961E' : t.line, backgroundColor: r ? '#FFD86B' : t.bg, borderStyle: r ? 'solid' : 'dashed' }]}>
                      {r ? <Icone nome={r.icone} size={24} color="#7A5300" /> : null}
                    </Pressable>
                  );
                })}
              </View>
            </View>
            <View style={[styles.premio, { borderColor: rota.premiada ? t.good : t.sun, backgroundColor: t.bg }]}>
              <Text style={[styles.cap, { color: t.muted }]}>RECOMPENSA DA ZONA</Text>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 6 }}>
                <Moeda size={20} /><Text style={{ color: t.ink, fontWeight: '900' }}>50</Text>
                <Text style={{ color: t.muted, fontWeight: '800', fontSize: 12 }}>+ próxima zona</Text>
              </View>
              <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4 }}>
                {rota.premiada && <Icone nome="check" size={14} color={t.good} />}
                <Text style={{ color: rota.premiada ? t.good : t.muted, fontWeight: '800', fontSize: 11 }}>{rota.premiada ? 'Resgatada' : 'Vença o chefe'}</Text>
              </View>
            </View>
          </View>
          {chefeVencido && (
            <Button3D label="Nova expedição nesta zona" variant="ghost" onPress={() => g.novaExpedicao(unit.id)} />
          )}
        </View>
        )}

        <View style={styles.atalhos}>
          <Pressable onPress={() => { g.prepararDesafio(); router.push('/lesson/desafio'); }} accessibilityRole="button"
            accessibilityLabel={desafioFeito ? `Desafio do dia resolvido. ${serieDesafio} dias seguidos` : 'Desafio do dia: um exercício de código novo por dia'}
            style={({ pressed }) => [styles.atalho, { backgroundColor: desafioFeito ? t.surface : t.brand, borderColor: desafioFeito ? t.good : t.brandDeep, borderBottomWidth: pressed ? 2 : 5 }]}>
            <Icone nome={desafioFeito ? 'check' : 'alvo'} size={26} color={desafioFeito ? t.good : '#fff'} />
            <View style={{ flex: 1 }}>
              <Text style={[styles.atalhoT, { color: desafioFeito ? t.ink : '#fff' }]}>Desafio do dia</Text>
              <Text style={[styles.atalhoS, { color: desafioFeito ? t.muted : 'rgba(255,255,255,0.9)' }]}>
                {desafioFeito ? `feito · ${serieDesafio} ${serieDesafio === 1 ? 'dia' : 'dias'}` : serieDesafio ? `sequência de ${serieDesafio}` : 'um código por dia'}
              </Text>
            </View>
          </Pressable>
          <Pressable onPress={() => (nRev ? router.push('/lesson/revisao') : router.push('/missoes'))} accessibilityRole="button"
            accessibilityLabel={nRev ? `Revisão: ${nRev} exercícios para revisar hoje` : 'Revisão: nada para revisar hoje'}
            style={({ pressed }) => [styles.atalho, { backgroundColor: nRev ? t.brand : t.surface, borderColor: nRev ? t.brandDeep : t.line, borderBottomWidth: pressed ? 2 : 5 }]}>
            <Icone nome="cerebro" size={26} color={nRev ? '#fff' : '#E05B8C'} />
            <View style={{ flex: 1 }}>
              <Text style={[styles.atalhoT, { color: nRev ? '#fff' : t.ink }]}>Revisão</Text>
              <Text style={[styles.atalhoS, { color: nRev ? 'rgba(255,255,255,0.9)' : t.muted }]}>{nRev ? `${nRev} para hoje` : 'em dia'}</Text>
            </View>
          </Pressable>
        </View>

        <View style={[styles.mais, { backgroundColor: t.surface, borderColor: t.line }]}>
          <Pressable onPress={() => setMais((m) => !m)} accessibilityRole="button" accessibilityState={{ expanded: mais }} accessibilityLabel="Mais atividades" style={styles.maisCab}>
            <Text style={[styles.maisTit, { color: t.ink }]}>Mais atividades</Text>
            <Text style={{ color: t.muted, fontWeight: '700', fontSize: 13, flex: 1 }} numberOfLines={1}>{mais ? 'Ocultar' : missoesProntas ? `${missoesProntas} missão pronta para resgatar` : 'missões, duelo, projetos e mais'}</Text>
            <Text style={{ color: t.muted, fontSize: 18, fontWeight: '900' }}>{mais ? '−' : '+'}</Text>
          </Pressable>
          {mais && (
            <View style={styles.maisGrade}>
              {([
                { k: 'missoes', nome: 'Missões', icone: 'alvo', cor: '#2F6FD6', nota: missoesProntas ? `${missoesProntas} ${missoesProntas > 1 ? 'prontas' : 'pronta'}` : '', ir: () => router.push('/missoes') },
                { k: 'duelo', nome: 'Duelo', icone: 'espada', cor: '#E05B8C', nota: recDuelos.v + recDuelos.d ? `${recDuelos.v}V ${recDuelos.d}D` : '', ir: () => router.push('/duelo') },
                { k: 'proj', nome: 'Projetos', icone: 'martelo', cor: '#B07A3F', nota: projLivres ? `${projFeitos}/${PROJETOS.length}` : 'zona 6', ir: () => router.push('/projetos') },
                { k: 'fogo', nome: 'Prova de fogo', icone: 'labareda', cor: '#F2742B', nota: fireBest > 0 ? String(fireBest) : '', ir: () => router.push('/prova') },
                { k: 'treino', nome: 'Treino rápido', icone: 'raio', cor: '#2F6FD6', nota: '', ir: () => router.push('/lesson/pratica'), off: !anyDone },
                { k: 'resumo', nome: 'Resumo semanal', icone: 'calendario', cor: '#3FA9D6', nota: '', ir: () => router.push('/resumo') },
                { k: 'museu', nome: 'Museu dos erros', icone: 'inseto', cor: '#E1474C', nota: '', ir: () => router.push('/museu') },
                { k: 'detetive', nome: 'Detetive de bugs', icone: 'lupa', cor: '#8C6CF2', nota: '', ir: () => router.push('/detetive') },
                { k: 'logica', nome: 'Calculadora de lógica', icone: 'lupa', cor: '#2F6FD6', nota: '', ir: () => router.push('/logica') },
                { k: 'prolog', nome: 'Laboratório Prolog', icone: 'raio', cor: '#8C6CF2', nota: '', ir: () => router.push('/prolog') },
                { k: 'cert', nome: 'Certificados', icone: 'medalha-estrela', cor: '#E0A21C', nota: '', ir: () => router.push('/certificado') },
              ] as const).map((m) => (
                <Pressable key={m.k} onPress={m.ir} disabled={'off' in m && m.off} accessibilityRole="button" accessibilityLabel={m.nome === 'Resumo semanal' ? 'Resumo da semana' : m.nome}
                  style={({ pressed }) => [styles.maisItem, { backgroundColor: pressed ? t.line : t.bg, opacity: 'off' in m && m.off ? 0.45 : 1 }]}>
                  <Icone nome={m.icone} size={20} color={m.cor} />
                  <Text style={[styles.maisNome, { color: t.ink }]} numberOfLines={1}>{m.nome}</Text>
                  {!!m.nota && <Text style={{ color: t.muted, fontWeight: '800', fontSize: 11 }}>{m.nota}</Text>}
                </Pressable>
              ))}
            </View>
          )}
        </View>
      </ScrollView>

      {no && <NoSheet no={no} mapa={mapa} unit={unit} indice={zi} livre={zonaAberta && livres.has(no.id)} fechar={() => setNo(null)} />}
      <Legenda visivel={info} fechar={() => setInfo(false)} reliquias={rota.reliquias} />
    </View>
  );
}

/** Trilha de Lógica: lista simples de unidades e lições, sem mapa, chefes nem batalhas. */
function ListaLogica() {
  const t = useTheme();
  const done = useGame((s) => s.done);
  return (
    <View style={{ gap: 12 }}>
      {courseOf('logica').units.map((u, ui) => {
        const lic = LESSONS_BY_TRACK.logica.filter((l) => l.unitIndex === ui);
        const feitas = lic.filter((l) => l.id in done).length;
        return (
          <View key={u.id} style={[styles.zona, { borderColor: t.line, backgroundColor: t.surface, gap: 8 }]}>
            <View style={styles.zonaTopo}>
              <HexNumero n={ui + 1} cor={feitas === lic.length ? '#E0A21C' : '#3FB85A'} />
              <View style={{ flex: 1 }}>
                <Text style={[styles.zonaNome, { color: t.ink }]}>{u.title}</Text>
                <Text style={[styles.zonaSub, { color: t.muted }]}>{u.description} · {feitas}/{lic.length} lições</Text>
              </View>
            </View>
            {lic.map((l) => {
              const ok = l.id in done;
              return (
                <Pressable key={l.id} onPress={() => router.push(`/lesson/${l.id}`)} accessibilityRole="button" accessibilityLabel={`Lição: ${l.title}`}
                  style={({ pressed }) => [{ flexDirection: 'row', alignItems: 'center', gap: 10, padding: 12, borderRadius: 14, borderWidth: 2, borderColor: ok ? t.good : t.line, backgroundColor: pressed ? t.line : t.bg }]}>
                  <Icone nome={ok ? 'check' : 'alvo'} size={18} color={ok ? t.good : t.brand} />
                  <Text style={{ flex: 1, color: t.ink, fontWeight: '800' }}>{l.title}</Text>
                  <Text style={{ color: t.muted, fontWeight: '800', fontSize: 12 }}>{l.exercises.length} passos</Text>
                </Pressable>
              );
            })}
          </View>
        );
      })}
    </View>
  );
}

function HexNumero({ n, cor, size = 44 }: { n: number; cor: string; size?: number }) {
  const r = size / 2;
  const pts = [-90, -30, 30, 90, 150, 210].map((a) => `${r + r * 0.95 * Math.cos((a * Math.PI) / 180)},${r + r * 0.95 * Math.sin((a * Math.PI) / 180)}`).join(' ');
  return (
    <View style={{ width: size, height: size, alignItems: 'center', justifyContent: 'center' }}>
      <Svg width={size} height={size} style={StyleSheet.absoluteFill}><Polygon points={pts} fill={cor} stroke="rgba(0,0,0,0.28)" strokeWidth={2} /></Svg>
      <Text style={{ color: '#fff', fontWeight: '900', fontSize: size * 0.38 }}>{n}</Text>
    </View>
  );
}

/** Seletor de zonas na lateral (como os números de zona da referência). */
function TrilhoZonas({ total, atual, aberta, vencida, onZona }: { total: number; atual: number; aberta: (i: number) => boolean; vencida: (i: number) => boolean; onZona: (i: number) => void }) {
  const t = useTheme();
  const ref = useRef<ScrollView>(null);
  useEffect(() => { ref.current?.scrollTo({ y: Math.max(0, atual * 40 - 120), animated: false }); }, [atual]);
  return (
    <ScrollView ref={ref} style={styles.trilho} contentContainerStyle={{ gap: 4, paddingVertical: 4, alignItems: 'center' }} showsVerticalScrollIndicator={false}>
      {Array.from({ length: total }, (_, i) => {
        const on = i === atual;
        const cor = !aberta(i) ? t.lineDeep : vencida(i) ? '#E0A21C' : '#3FB85A';
        return (
          <Pressable key={i} onPress={() => onZona(i)} accessibilityRole="button" accessibilityState={{ selected: on }}
            accessibilityLabel={`Zona ${i + 1}${vencida(i) ? ', conquistada' : aberta(i) ? '' : ', bloqueada'}`}
            style={{ transform: [{ scale: on ? 1.1 : 1 }], opacity: on || aberta(i) ? 1 : 0.7 }}>
            <View style={on ? styles.trilhoOn : undefined}><HexNumero n={i + 1} cor={cor} size={32} /></View>
          </Pressable>
        );
      })}
    </ScrollView>
  );
}

function Legenda({ visivel, fechar, reliquias }: { visivel: boolean; fechar: () => void; reliquias: string[] }) {
  const t = useTheme();
  const tipos: TipoNo[] = ['batalha', 'elite', 'cura', 'misterio', 'tesouro', 'chefe'];
  return (
    <Modal visible={visivel} transparent animationType="fade" onRequestClose={fechar}>
      <Pressable style={styles.fundo} onPress={fechar}>
        <Pressable style={[styles.legenda, { backgroundColor: t.bg, borderColor: t.line }]} onPress={() => {}}>
          <ScrollView contentContainerStyle={{ gap: 12 }}>
            <Text style={[styles.h2, { color: t.ink }]}>Como funciona o mapa</Text>
            <Text style={{ color: t.muted, fontWeight: '600', lineHeight: 20 }}>
              Cada unidade é uma zona. Escolha um caminho ligado ao seu personagem: todo caminho passa por todas as lições da zona, mas os desvios mudam o que você ganha. No fim, derrote o chefe para liberar a próxima zona.
            </Text>
            {tipos.map((k) => (
              <View key={k} style={styles.legItem}>
                <NoHex tipo={k} size={46} estado="futuro" />
                <View style={{ flex: 1 }}>
                  <Text style={{ color: t.ink, fontWeight: '900' }}>{INFO_NO[k].nome}</Text>
                  <Text style={{ color: t.muted, fontWeight: '600', fontSize: 13 }}>{INFO_NO[k].texto}</Text>
                </View>
              </View>
            ))}
            <Text style={[styles.h2, { color: t.ink, marginTop: 6 }]}>Relíquias</Text>
            <Text style={{ color: t.muted, fontWeight: '600' }}>Você ganha em tesouros, elites e com o mercador. Valem até o fim da expedição (no máximo 3).</Text>
            {RELIQUIAS.map((r) => (
              <View key={r.id} style={{ opacity: reliquias.includes(r.id) ? 1 : 0.6 }}><CartaoReliquia id={r.id} /></View>
            ))}
            <Button3D label="Entendi" onPress={fechar} />
          </ScrollView>
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const styles = StyleSheet.create({
  mais: { borderWidth: 2, borderRadius: 18, padding: 6 },
  maisCab: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingVertical: 8, paddingHorizontal: 10 },
  maisTit: { fontSize: 16, fontWeight: '900', flexShrink: 0 },
  maisGrade: { flexDirection: 'row', flexWrap: 'wrap', gap: 6, padding: 4, paddingTop: 0 },
  maisItem: { flexGrow: 1, flexBasis: '47%', flexDirection: 'row', alignItems: 'center', gap: 8, borderRadius: 12, paddingVertical: 11, paddingHorizontal: 12 },
  maisNome: { flex: 1, fontSize: 14, fontWeight: '800' },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 2 },
  logo: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  logoText: { fontSize: 22, fontWeight: '900', letterSpacing: -0.3 },
  scroll: { paddingHorizontal: 12, paddingTop: 14, paddingBottom: 60, gap: 14, maxWidth: 640, width: '100%', alignSelf: 'center' },
  tracks: { flexDirection: 'row', borderWidth: 2, borderRadius: 16, padding: 4, gap: 4 },
  trackBtn: { flex: 1, alignItems: 'center', borderRadius: 12, paddingVertical: 7, gap: 1 },
  meta: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 4 },
  metaTxt: { fontWeight: '900', fontSize: 14 },
  metaNum: { fontWeight: '800', fontSize: 12, fontVariant: ['tabular-nums'] },
  bar: { flex: 1, height: 10, borderRadius: 99, overflow: 'hidden' },
  barFill: { height: '100%', borderRadius: 99 },
  zona: { borderWidth: 2, borderRadius: 22, padding: 10, gap: 10 },
  zonaTopo: { flexDirection: 'row', alignItems: 'center', gap: 10, paddingHorizontal: 2 },
  eyebrow: { fontSize: 11, fontWeight: '900', letterSpacing: 1 },
  zonaNome: { fontSize: 20, fontWeight: '900' },
  zonaSub: { fontSize: 12, fontWeight: '800' },
  infoBtn: { flexDirection: 'row', alignItems: 'center', gap: 4, borderWidth: 2, borderRadius: 99, paddingVertical: 5, paddingHorizontal: 10 },
  mapaLinha: { flexDirection: 'row', gap: 6 },
  trilho: { width: 40, flexGrow: 0 },
  trilhoOn: { borderRadius: 99, borderWidth: 2, borderColor: '#7FE7FF' },
  expedicao: { flexDirection: 'row', gap: 10, alignItems: 'stretch' },
  cap: { fontSize: 10, fontWeight: '900', letterSpacing: 0.8 },
  slot: { width: 42, height: 42, borderRadius: 12, borderWidth: 2, alignItems: 'center', justifyContent: 'center' },
  premio: { borderWidth: 2, borderRadius: 14, padding: 8, gap: 3, minWidth: 150 },
  atalhos: { flexDirection: 'row', gap: 10 },
  atalho: { flex: 1, flexDirection: 'row', alignItems: 'center', gap: 10, borderWidth: 2, borderRadius: 16, padding: 10 },
  atalhoT: { fontSize: 16, fontWeight: '900' },
  atalhoS: { fontSize: 12, fontWeight: '700' },
  fire: { flexDirection: 'row', alignItems: 'center', gap: 12, backgroundColor: '#FF6B1A', borderBottomColor: '#B8420A', borderRadius: 18, padding: 14 },
  fireIc: { width: 48, height: 48, borderRadius: 14, backgroundColor: 'rgba(0,0,0,0.15)', alignItems: 'center', justifyContent: 'center' },
  fireTitle: { color: '#fff', fontSize: 19, fontWeight: '900' },
  fireSub: { color: 'rgba(255,255,255,0.95)', fontSize: 13, fontWeight: '700' },
  fireBadge: { alignItems: 'center', backgroundColor: 'rgba(0,0,0,0.18)', borderRadius: 12, paddingVertical: 5, paddingHorizontal: 10, minWidth: 64 },
  fireBadgeTop: { color: '#fff', fontSize: 10, fontWeight: '900', letterSpacing: 0.8 },
  fireBadgeNum: { color: '#fff', fontSize: 18, fontWeight: '900' },
  card: { borderWidth: 2, borderRadius: 18, padding: 16, gap: 10 },
  cardTitle: { fontSize: 18, fontWeight: '800' },
  fundo: { flex: 1, backgroundColor: 'rgba(0,0,0,0.45)', alignItems: 'center', justifyContent: 'center', padding: 16 },
  legenda: { width: '100%', maxWidth: 460, maxHeight: '88%', borderRadius: 20, borderWidth: 2, padding: 18 },
  legItem: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  h2: { fontSize: 20, fontWeight: '900' },
});
