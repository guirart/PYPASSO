import AsyncStorage from '@react-native-async-storage/async-storage';
import { useMemo } from 'react';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { closeWeek, weekId, type WeekResult } from './leagues';
import { usePlus } from './plus';
import { CONQUISTAS, itemLoja, missoesDoDia, moedasDoBau, moedasDoNivel, nivelDe, XP2_MS, type Contadores, type Evento } from './gamificacao';
import { avisar } from './avisos';
import { desafioVazio, exercicioDoDesafio, type Desafio } from './desafio';
import { recompensa, type Recorde, type Resultado } from './duelo';
import { HEROI_PADRAO, normalizarHeroi, type LookHeroi } from './heroi';
import { sortearBau, type ModeloBau } from './baus';
import { custoMelhoria, MAX_MEL, poeiraDeDesmontar } from './melhoria';
import { BASICOS, bonusDoEquipamento, EQUIP_PADRAO, RARIDADE, sortearItem, vestirEquipamento, type Bonus, type Equip, type ItemInst, type Slot } from './itens';
import { eventoDaSemana, META_EVENTO, pontosDaLicao, PREMIO_EVENTO } from './evento';
import { podarDias } from './metas';

export const MAX_HEARTS = 5;
export const HEART_REGEN_MS = 30 * 60 * 1000;
export const DAILY_GOAL = 30;

export const dayKey = (d = new Date()) => `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
export const yesterdayKey = () => { const d = new Date(); d.setDate(d.getDate() - 1); return dayKey(d); };
const parseDay = (k: string) => { const [y, m, d] = k.split('-').map(Number); return new Date(y, m - 1, d).getTime(); };
/** Dias inteiros entre dois dayKey (ex.: ontem → hoje = 1). */
const diasEntre = (a: string, b: string) => Math.round((parseDay(b) - parseDay(a)) / 86400000);

/** Revisão espaçada (caixas de Leitner): intervalo em dias de cada caixa. Depois da última, sai do baralho. */
export const CAIXAS_DIAS = [1, 2, 4, 7, 15];
const DIA_MS = 86400000;
/** Vence no começo do dia (quem errou hoje revisa amanhã de manhã). */
const venceEm = (dias: number) => { const d = new Date(); d.setHours(4, 0, 0, 0); return d.getTime() + dias * DIA_MS; };
export type CartaoRevisao = { cx: number; due: number; erros: number };
/** Expedição numa zona do mapa roguelite (src/lib/mapa.ts). pos '' = na entrada. */
export type Rota = { exp: number; pos: string; visitados: string[]; reliquias: string[]; premiada?: boolean };
export const rotaVazia = (exp = 0): Rota => ({ exp, pos: '', visitados: [], reliquias: [] });
export type ProgressoProjeto = { passo: number; codigo?: string; feito?: boolean };
export type Hoje = { dia: string; c: Contadores; resgatadas: string[]; bau: number };
const hojeVazio = (): Hoje => ({ dia: dayKey(), c: {}, resgatadas: [], bau: 0 });

export type GameState = State;
type State = {
  name: string;
  avatarSeed: string;
  xp: number;
  hearts: number;
  heartTs: number; // quando a contagem da próxima vida começou (0 = cheio)
  streak: number;
  lastDay: string; // último dia com lição concluída
  dayKey: string;
  dayXP: number;
  done: Record<string, number>; // lessonId -> melhor precisão (0-100)
  // Ligas
  league: number; // 1 = Bronze (Noob) … 10 = Diamante (Lenda Pythônica)
  bestLeague: number;
  weekId: string;
  weekXP: number;
  medals: { ouro: number; prata: number; bronze: number };
  history: WeekResult[];
  pendingResult: WeekResult | null; // resultado da semana que terminou, ainda não visto
  online: boolean; // com conta: quem fecha a semana é o servidor
  track: 'main' | 'builtins' | 'libs' | 'logica'; // trilha aberta na tela Aprender
  fire: Record<string, number>; // Prova de fogo: nível -> recorde de pontos
  fireRuns: number; // quantas provas de fogo já terminou
  stars: Record<string, number>; // exercícios especiais da trilha (cenas do Pipo): id -> melhor nº de estrelas
  aprendidos: Record<string, number>; // Biblioteca: id da entrada -> quando foi aprendida numa lição
  vistosBib: Record<string, boolean>; // entradas novas que a pessoa já abriu na Biblioteca
  // Gamificação (src/lib/gamificacao.ts)
  moedas: number;
  nivelVisto: number; // último nível comemorado
  stats: Contadores; // contadores da vida toda (conquistas)
  hoje: Hoje; // contadores do dia (missões) e baú
  conquistas: Record<string, number>; // id -> quando desbloqueou
  congelador: number; // congeladores de sequência guardados
  xp2Ate: number; // XP em dobro até este horário (ms)
  molduras: string[]; // molduras compradas
  moldura: string; // moldura em uso ('' = nenhuma)
  revisao: Record<string, CartaoRevisao>; // id do exercício -> caixa e vencimento
  projetos: Record<string, ProgressoProjeto>;
  semente: string; // semente fixa do perfil para gerar os mapas
  rotas: Record<string, Rota>; // zona (unidade) -> expedição atual
  desafio: Desafio; // desafio do dia (src/lib/desafio.ts)
  duelos: Record<string, Recorde>; // adversário do elenco -> vitórias, derrotas e empates
  xpDias: Record<string, number>; // XP por dia, só os 14 mais recentes (meta diária adaptativa)
  sem: Semana; // contadores da semana atual (Resumo da semana)
  evento: { semana: string; pontos: number; resgatado: boolean }; // Evento da semana (src/lib/evento.ts)
  explicacoes: Record<string, number>; // lições em que já ganhou o bônus de "explique com suas palavras"
  certs: Record<string, number>; // trilha -> quando o certificado foi emitido
  heroi: LookHeroi; // o personagem das batalhas (editor em /personagem)
  inv: ItemInst[]; // inventário: peças do herói (lib/itens.ts)
  poeira: number; // pó de forja: sai ao desmontar peças e serve para melhorar outras
  equip: Equip; // id da peça vestida em cada espaço
};
export type Semana = { id: string; licoes: number; dias: string[]; precSoma: number; precN: number };
const semanaVazia = (id = ''): Semana => ({ id, licoes: 0, dias: [], precSoma: 0, precN: 0 });

type Actions = {
  tick: () => void;
  loseHeart: () => void;
  gainHeart: () => void;
  refillHearts: () => void;
  /** Soma XP (com o XP em dobro, se ativo) e conta o dia na sequência. Devolve o XP de verdade. */
  completeLesson: (lessonId: string | null, xp: number, accuracy: number) => number;
  registrar: (e: Evento, n?: number) => void;
  ganharMoedas: (n: number) => void;
  resgatarMissao: (id: string) => boolean;
  abrirBau: () => number;
  comprar: (id: string) => string | null; // null = ok; senão, o motivo
  usarMoldura: (id: string) => void;
  fimDoDuelo: (contra: string, res: Resultado, acertos: number, total: number) => { xp: number; moedas: number };
  setHeroi: (look: LookHeroi) => void;
  equipar: (id: string) => void;
  desequipar: (slot: Slot) => void;
  desmontar: (id: string) => number; // devolve as moedas ganhas (0 = não dá); também rende pó de forja
  melhorar: (id: string) => string | null; // null = melhorou; senão o motivo
  soltarItem: (zona: number, tipo: 'normal' | 'boss') => { item: ItemInst; bau: ModeloBau }; // drop de baú (de elite ou do chefe da zona)
  vistoInventario: () => void; // apaga a marca "novo" das peças
  bonus: () => Bonus; // soma das habilidades equipadas
  emitirCertificado: (trilha: string) => number; // data de emissão (a primeira vez grava)
  resgatarEvento: () => number; // moedas do baú do evento (0 = ainda não dá)
  bonusExplicacao: (lessonId: string) => boolean; // +5 XP, uma vez por lição
  prepararDesafio: () => void; // sorteia o desafio de hoje (uma vez por dia)
  concluirDesafio: () => number; // devolve a sequência de dias
  verificar: () => void; // nível e conquistas novas
  errouExercicio: (exId: string) => void;
  revisou: (exId: string, ok: boolean) => void;
  salvarProjeto: (id: string, p: ProgressoProjeto) => void;
  visitar: (zona: string, no: string) => void;
  ganharReliquia: (zona: string, id: string) => void;
  novaExpedicao: (zona: string) => void;
  premiarZona: (zona: string) => boolean;
  setProfile: (p: Partial<Pick<State, 'name' | 'avatarSeed'>>) => void;
  mergeRemote: (p: Partial<State>) => void;
  dismissResult: () => void;
  setTrack: (t: 'main' | 'builtins' | 'libs' | 'logica') => void;
  finishFire: (level: number, score: number) => boolean; // true = recorde novo
  migrateIds: (map: Record<string, string>) => void;
  setStars: (id: string, n: number) => boolean; // true = melhorou
  aprender: (ids: string[]) => string[]; // devolve só as que são novas
  verNaBiblioteca: (id: string) => void;
  reset: () => void;
};

export const initialGame = (): State => ({
  name: '', avatarSeed: Math.random().toString(36).slice(2, 10),
  xp: 0, hearts: MAX_HEARTS, heartTs: 0, streak: 0, lastDay: '', dayKey: dayKey(), dayXP: 0, done: {},
  league: 1, bestLeague: 1, weekId: weekId(), weekXP: 0, medals: { ouro: 0, prata: 0, bronze: 0 }, history: [], pendingResult: null, online: false, track: 'main', fire: {}, fireRuns: 0, stars: {}, aprendidos: {}, vistosBib: {},
  moedas: 0, nivelVisto: 1, stats: {}, hoje: hojeVazio(), conquistas: {}, congelador: 0, xp2Ate: 0, molduras: [], moldura: '', revisao: {}, projetos: {}, semente: Math.random().toString(36).slice(2, 10), rotas: {},
  desafio: desafioVazio(),
  duelos: {}, xpDias: {}, sem: semanaVazia(), evento: { semana: '', pontos: 0, resgatado: false }, explicacoes: {}, certs: {}, heroi: HEROI_PADRAO, poeira: 0, inv: BASICOS, equip: EQUIP_PADRAO,
});

export const useGame = create<State & Actions>()(
  persist(
    (set, get) => ({
      ...initialGame(),
      tick: () => {
        const s = get();
        const patch: Partial<State> = {};
        if (s.dayKey !== dayKey()) { patch.dayKey = dayKey(); patch.dayXP = 0; }
        if (s.hoje?.dia !== dayKey()) patch.hoje = hojeVazio();
        // Virou a semana: fecha a liga da semana anterior
        const now = weekId();
        if (s.weekId !== now) {
          if (s.weekId && (s.weekXP > 0 || s.league > 1) && !s.online) {
            const res = closeWeek(s.weekId, s.league, { name: s.name, seed: s.avatarSeed, xp: s.weekXP });
            patch.league = res.to;
            patch.bestLeague = Math.max(s.bestLeague ?? 1, res.to);
            patch.history = [res, ...(s.history ?? [])].slice(0, 30);
            patch.pendingResult = res;
            if (res.xp > 0 && res.rank <= 3) {
              const k = (['ouro', 'prata', 'bronze'] as const)[res.rank - 1];
              patch.medals = { ...(s.medals ?? { ouro: 0, prata: 0, bronze: 0 }), [k]: (s.medals?.[k] ?? 0) + 1 };
            }
          }
          patch.weekId = now;
          patch.weekXP = 0;
        }
        if (s.lastDay && s.lastDay !== dayKey() && s.lastDay !== yesterdayKey()) {
          // Ficou dias sem estudar: os congeladores cobrem um dia cada.
          const faltou = diasEntre(s.lastDay, dayKey()) - 1;
          if (s.streak > 0 && faltou > 0 && (s.congelador ?? 0) >= faltou) {
            patch.congelador = s.congelador - faltou;
            patch.lastDay = yesterdayKey();
            avisar({ icone: 'gelo', titulo: 'Sequência salva!', texto: `${faltou === 1 ? 'Um congelador protegeu' : `${faltou} congeladores protegeram`} seus ${s.streak} dias seguidos.` });
          } else patch.streak = 0;
        }
        if (s.hearts < MAX_HEARTS && s.heartTs) {
          const gained = Math.floor((Date.now() - s.heartTs) / HEART_REGEN_MS);
          if (gained > 0) {
            const hearts = Math.min(MAX_HEARTS, s.hearts + gained);
            patch.hearts = hearts;
            patch.heartTs = hearts < MAX_HEARTS ? s.heartTs + gained * HEART_REGEN_MS : 0;
          }
        }
        if (Object.keys(patch).length) set(patch);
      },
      loseHeart: () => { if (usePlus.getState().ativo) return; set((s) => ({
        hearts: Math.max(0, s.hearts - 1),
        heartTs: s.hearts === MAX_HEARTS ? Date.now() : s.heartTs,
      })); },
      gainHeart: () => set((s) => {
        const hearts = Math.min(MAX_HEARTS, s.hearts + 1);
        return { hearts, heartTs: hearts === MAX_HEARTS ? 0 : s.heartTs };
      }),
      refillHearts: () => set({ hearts: MAX_HEARTS, heartTs: 0 }),
      completeLesson: (lessonId, xpBase, accuracy) => {
        get().tick();
        const xp = Date.now() < (get().xp2Ate ?? 0) ? xpBase * 2 : xpBase;
        set((s) => {
          const today = dayKey();
          const streak = s.lastDay === today ? s.streak : s.lastDay === yesterdayKey() ? s.streak + 1 : 1;
          const done = lessonId ? { ...s.done, [lessonId]: Math.max(s.done[lessonId] ?? 0, accuracy) } : s.done;
          const semId = weekId();
          const sem0 = s.sem?.id === semId ? s.sem : semanaVazia(semId);
          const sem: Semana = {
            ...sem0, dias: sem0.dias.includes(today) ? sem0.dias : [...sem0.dias, today],
            licoes: sem0.licoes + (lessonId ? 1 : 0), precSoma: sem0.precSoma + (lessonId ? accuracy : 0), precN: sem0.precN + (lessonId ? 1 : 0),
          };
          // Evento da semana: só a primeira vez que a lição é concluída rende pontos (refazer não vale)
          const ev0 = s.evento?.semana === semId ? s.evento : { semana: semId, pontos: 0, resgatado: false };
          const evento = lessonId && !(lessonId in s.done) ? { ...ev0, pontos: ev0.pontos + pontosDaLicao(lessonId, eventoDaSemana(semId)) } : ev0;
          const xpDias = podarDias({ ...(s.xpDias ?? {}), [today]: (s.xpDias?.[today] ?? 0) + xp });
          return { xp: s.xp + xp, dayXP: s.dayXP + xp, weekXP: (s.weekXP ?? 0) + xp, streak, lastDay: today, done, sem, evento, xpDias };
        });
        get().registrar('xp', xp);
        return xp;
      },
      registrar: (e, n = 1) => {
        get().tick();
        set((s) => {
          const soma = (c: Contadores) => ({ ...c, [e]: e === 'combo' ? Math.max(c[e] ?? 0, n) : (c[e] ?? 0) + n });
          const hoje = s.hoje?.dia === dayKey() ? s.hoje : hojeVazio();
          return { stats: soma(s.stats ?? {}), hoje: { ...hoje, c: soma(hoje.c) } };
        });
        get().verificar();
      },
      ganharMoedas: (n) => set((s) => ({ moedas: (s.moedas ?? 0) + n })),
      resgatarMissao: (id) => {
        get().tick();
        const s = get();
        const m = missoesDoDia(s.hoje.dia).find((x) => x.id === id);
        if (!m || s.hoje.resgatadas.includes(id) || (s.hoje.c[m.evento] ?? 0) < m.meta) return false;
        set({ moedas: s.moedas + m.moedas, hoje: { ...s.hoje, resgatadas: [...s.hoje.resgatadas, id] } });
        return true;
      },
      abrirBau: () => {
        const s = get();
        if (s.hoje.bau || s.hoje.resgatadas.length < 3) return 0;
        const n = moedasDoBau();
        set({ moedas: s.moedas + n, hoje: { ...s.hoje, bau: n } });
        return n;
      },
      comprar: (id) => {
        const s = get();
        const it = itemLoja(id);
        if (!it) return 'Item não encontrado.';
        if (s.moedas < it.preco) return `Faltam ${it.preco - s.moedas} moedas.`;
        if (it.tipo === 'congelador' && s.congelador >= (it.max ?? 2)) return 'Você já tem o máximo guardado.';
        if (it.tipo === 'vidas' && (usePlus.getState().ativo || s.hearts >= MAX_HEARTS)) return 'Suas vidas já estão cheias.';
        if (it.tipo === 'xp2' && Date.now() < s.xp2Ate) return 'O XP em dobro já está ativo.';
        if (it.tipo === 'moldura' && s.molduras.includes(id)) return 'Você já tem esta moldura.';
        const patch: Partial<State> = { moedas: s.moedas - it.preco };
        if (it.tipo === 'congelador') patch.congelador = s.congelador + 1;
        if (it.tipo === 'vidas') { patch.hearts = MAX_HEARTS; patch.heartTs = 0; }
        if (it.tipo === 'xp2') patch.xp2Ate = Date.now() + XP2_MS;
        if (it.tipo === 'moldura') { patch.molduras = [...s.molduras, id]; patch.moldura = id; }
        set(patch);
        get().registrar('compras');
        return null;
      },
      fimDoDuelo: (contra, res, acertos, total) => {
        const r = recompensa(res);
        const antes = get().duelos?.[contra] ?? { v: 0, d: 0, e: 0 };
        set((s) => ({ duelos: { ...(s.duelos ?? {}), [contra]: { v: antes.v + (res === 'v' ? 1 : 0), d: antes.d + (res === 'd' ? 1 : 0), e: antes.e + (res === 'e' ? 1 : 0) } } }));
        const xp = get().completeLesson(null, r.xp, Math.round((acertos / Math.max(1, total)) * 100));
        get().ganharMoedas(r.moedas);
        return { xp, moedas: r.moedas };
      },
      setHeroi: (heroi) => set({ heroi }),
      equipar: (id) => set((s) => {
        const it = s.inv.find((i) => i.id === id);
        return it ? { equip: { ...s.equip, [it.slot]: id }, inv: s.inv.map((i) => (i.id === id ? { ...i, novo: false } : i)) } : {};
      }),
      desequipar: (slot) => set((s) => (slot === 'arma' || slot === 'roupa' ? {} : { equip: { ...s.equip, [slot]: null } })), // arma e roupa sempre ficam vestidas
      desmontar: (id) => {
        const s = get();
        const it = s.inv.find((i) => i.id === id);
        if (!it || it.id.startsWith('basico-')) return 0;
        const ganho = RARIDADE[it.raridade].venda;
        const equip = { ...s.equip };
        // se era a peça vestida, volta ao item básico do espaço (ou fica sem, nos espaços opcionais)
        if (equip[it.slot] === id) equip[it.slot] = BASICOS.find((b) => b.slot === it.slot)?.id ?? null;
        set({ inv: s.inv.filter((i) => i.id !== id), equip, moedas: s.moedas + ganho, poeira: (s.poeira ?? 0) + poeiraDeDesmontar(RARIDADE[it.raridade].nivel) });
        return ganho;
      },
      melhorar: (id) => {
        const s = get();
        const it = s.inv.find((i) => i.id === id);
        if (!it) return 'Peça não encontrada.';
        if (!it.hab.length) return 'Peças sem habilidade não têm o que melhorar.';
        const mel = it.mel ?? 0;
        if (mel >= MAX_MEL) return 'Esta peça já está no nível máximo.';
        const custo = custoMelhoria(RARIDADE[it.raridade].nivel, mel);
        if ((s.poeira ?? 0) < custo) return `Faltam ${custo - (s.poeira ?? 0)} de pó de forja.`;
        set({ poeira: (s.poeira ?? 0) - custo, inv: s.inv.map((i) => (i.id === id ? { ...i, mel: mel + 1 } : i)) });
        return null;
      },
      soltarItem: (zona, tipo) => {
        const { modelo, forca } = sortearBau(Math.random, zona, tipo);
        // chefe nunca deixa peça comum; o resto vem da força do baú
        const item = sortearItem(Math.random, { forca, sorte: get().bonus().sorte, minimo: tipo === 'boss' ? 'incomum' : 'comum' });
        set((s) => ({ inv: [...s.inv, item] }));
        get().registrar('itens');
        return { item, bau: modelo };
      },
      vistoInventario: () => set((s) => (s.inv.some((i) => i.novo) ? { inv: s.inv.map((i) => (i.novo ? { ...i, novo: false } : i)) } : {})),
      bonus: () => bonusDoEquipamento(get().inv ?? BASICOS, get().equip ?? EQUIP_PADRAO),
      emitirCertificado: (trilha) => {
        const antes = get().certs?.[trilha];
        if (antes) return antes;
        const agora = Date.now();
        set((s) => ({ certs: { ...(s.certs ?? {}), [trilha]: agora } }));
        return agora;
      },
      resgatarEvento: () => {
        const s = get();
        const semId = weekId();
        if (s.evento?.semana !== semId || s.evento.resgatado || s.evento.pontos < META_EVENTO) return 0;
        set({ moedas: (s.moedas ?? 0) + PREMIO_EVENTO, evento: { ...s.evento, resgatado: true } });
        return PREMIO_EVENTO;
      },
      bonusExplicacao: (lessonId) => {
        const s = get();
        if (s.explicacoes?.[lessonId]) return false;
        set({ xp: s.xp + 5, dayXP: s.dayXP + 5, weekXP: (s.weekXP ?? 0) + 5, explicacoes: { ...(s.explicacoes ?? {}), [lessonId]: Date.now() } });
        return true;
      },
      prepararDesafio: () => {
        const s = get();
        const d = s.desafio ?? desafioVazio();
        if (d.dia === dayKey() && d.exId) return;
        const ex = exercicioDoDesafio(s.done, d.feitos ?? [], dayKey(), s.semente);
        set({ desafio: { ...d, feitos: d.feitos ?? [], dia: dayKey(), exId: ex?.id ?? '', feito: false } });
      },
      concluirDesafio: () => {
        const d = get().desafio ?? desafioVazio();
        if (d.feito && d.dia === dayKey()) return d.serie;
        const serie = d.ultimo === yesterdayKey() ? d.serie + 1 : 1;
        set({ desafio: { ...d, feito: true, dia: dayKey(), serie, melhor: Math.max(d.melhor, serie), ultimo: dayKey(), feitos: d.feitos.includes(d.exId) ? d.feitos : [...d.feitos, d.exId] } });
        return serie;
      },
      usarMoldura: (id) => set((s) => ({ moldura: id === '' || s.molduras.includes(id) ? id : s.moldura })),
      verificar: () => {
        const s = get();
        const patch: Partial<State> = {};
        let moedas = s.moedas ?? 0;
        const nv = nivelDe(s.xp).nivel;
        if (nv > (s.nivelVisto ?? 1)) {
          let ganho = 0;
          for (let n = (s.nivelVisto ?? 1) + 1; n <= nv; n++) ganho += moedasDoNivel(n);
          moedas += ganho;
          patch.nivelVisto = nv;
          avisar({ icone: nivelDe(s.xp).icone, titulo: `Nível ${nv}!`, texto: `${nivelDe(s.xp).titulo}. +${ganho} moedas`, tipo: 'nivel' });
        }
        const fonte = { ...(s.stats ?? {}), nivel: nv, streak: s.streak, aprendidos: Object.keys(s.aprendidos ?? {}).length, liga: s.bestLeague ?? 1 };
        const novas = CONQUISTAS.filter((c) => !s.conquistas?.[c.id] && c.valor(fonte) >= c.meta);
        if (novas.length) {
          const agora = Date.now();
          patch.conquistas = { ...(s.conquistas ?? {}), ...Object.fromEntries(novas.map((c) => [c.id, agora])) };
          novas.forEach((c) => { moedas += c.moedas; avisar({ icone: c.icone, titulo: `Conquista: ${c.nome}`, texto: `${c.texto}. +${c.moedas} moedas`, tipo: 'conquista' }); });
        }
        if (moedas !== s.moedas) patch.moedas = moedas;
        if (Object.keys(patch).length) set(patch);
      },
      errouExercicio: (exId) => set((s) => {
        const r = s.revisao ?? {};
        const atual = r[exId];
        return { revisao: { ...r, [exId]: { cx: 0, due: venceEm(CAIXAS_DIAS[0]), erros: (atual?.erros ?? 0) + 1 } } };
      }),
      revisou: (exId, ok) => set((s) => {
        const r = { ...(s.revisao ?? {}) };
        const atual = r[exId] ?? { cx: 0, due: 0, erros: 0 };
        if (!ok) r[exId] = { cx: 0, due: venceEm(CAIXAS_DIAS[0]), erros: atual.erros + 1 };
        else if (atual.cx + 1 >= CAIXAS_DIAS.length) delete r[exId]; // aprendido de vez
        else r[exId] = { ...atual, cx: atual.cx + 1, due: venceEm(CAIXAS_DIAS[atual.cx + 1]) };
        return { revisao: r };
      }),
      salvarProjeto: (id, p) => set((s) => ({ projetos: { ...(s.projetos ?? {}), [id]: p } })),
      visitar: (zona, no) => set((s) => {
        const r = s.rotas?.[zona] ?? rotaVazia();
        if (r.visitados.includes(no)) return s; // refazer um nó antigo não volta o personagem
        return { rotas: { ...s.rotas, [zona]: { ...r, pos: no, visitados: [...r.visitados, no] } } };
      }),
      ganharReliquia: (zona, id) => set((s) => {
        const r = s.rotas?.[zona] ?? rotaVazia();
        if (r.reliquias.includes(id)) return s;
        return { rotas: { ...s.rotas, [zona]: { ...r, reliquias: [...r.reliquias, id] } } };
      }),
      novaExpedicao: (zona) => set((s) => ({ rotas: { ...s.rotas, [zona]: { ...rotaVazia((s.rotas?.[zona]?.exp ?? 0) + 1), premiada: s.rotas?.[zona]?.premiada } } })),
      premiarZona: (zona) => {
        const r = get().rotas?.[zona] ?? rotaVazia();
        if (r.premiada) return false;
        set((s) => ({ moedas: s.moedas + 50, rotas: { ...s.rotas, [zona]: { ...r, premiada: true } } }));
        return true;
      },
      setProfile: (p) => set(p),
      mergeRemote: (p) => set((s) => ({
        ...p,
        xp: Math.max(s.xp, p.xp ?? 0),
        streak: Math.max(s.streak, p.streak ?? 0),
        done: { ...(p.done ?? {}), ...s.done },
        league: p.league ?? s.league,
        bestLeague: Math.max(s.bestLeague ?? 1, p.bestLeague ?? 1, p.league ?? 1),
      })),
      dismissResult: () => set({ pendingResult: null }),
      setTrack: (track) => set({ track }),
      aprender: (ids) => {
        const ja = get().aprendidos ?? {};
        const novos = ids.filter((id) => !(id in ja));
        if (novos.length) {
          const agora = Date.now();
          set((s) => ({ aprendidos: { ...(s.aprendidos ?? {}), ...Object.fromEntries(novos.map((id) => [id, agora])) } }));
        }
        return novos;
      },
      verNaBiblioteca: (id) => {
        const s = get();
        if (s.aprendidos?.[id] && !s.vistosBib?.[id]) set({ vistosBib: { ...(s.vistosBib ?? {}), [id]: true } });
      },
      setStars: (id, n) => {
        const antes = get().stars?.[id] ?? 0;
        if (n <= antes) return false;
        set((s) => ({ stars: { ...(s.stars ?? {}), [id]: n } }));
        return true;
      },
      migrateIds: (map) => {
        const done = get().done;
        const old = Object.keys(done).filter((k) => map[k] && !(map[k] in done));
        if (!old.length) return;
        const next = { ...done };
        old.forEach((k) => { next[map[k]] = done[k]; });
        set({ done: next });
      },
      finishFire: (level, score) => {
        const best = get().fire?.[level] ?? 0;
        set((s) => ({ fire: { ...(s.fire ?? {}), [level]: Math.max(best, score) }, fireRuns: (s.fireRuns ?? 0) + 1 }));
        return score > best;
      },
      reset: () => set(initialGame()),
    }),
    {
      name: 'pypasso-game', storage: createJSONStorage(() => AsyncStorage), version: 2,
      // v0 → v1 (gamificação): quem já tinha XP começa no nível certo, sem chuva de comemorações.
      migrate: (old, v) => {
        const o = (old ?? {}) as Partial<State>;
        let n: Partial<State> = o;
        if (v < 1) n = { ...n, nivelVisto: nivelDe(o.xp ?? 0).nivel };
        if (v < 2) n = { ...n, semente: n.semente ?? Math.random().toString(36).slice(2, 10), rotas: n.rotas ?? {} };
        return n as State & Actions;
      },
    },
  ),
);

export const isUnlocked = (order: number, done: Record<string, number>, ids: string[]) =>
  order === 0 || ids[order - 1] in done;

/** O visual do herói: aparência (pele e cabelo) mais as peças equipadas no inventário. */
export function useHeroiVisual(): LookHeroi {
  const heroi = useGame((s) => s.heroi);
  const inv = useGame((s) => s.inv);
  const equip = useGame((s) => s.equip);
  return useMemo(() => vestirEquipamento(normalizarHeroi(heroi), inv ?? BASICOS, equip ?? EQUIP_PADRAO), [heroi, inv, equip]);
}
