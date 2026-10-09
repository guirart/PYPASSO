import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { exercicioPorId, lessonById } from '@/content';
import { supabase } from './supabase';
import type { NomeIcone } from '@/components/icones-data';

/**
 * Teste com pessoas de verdade (ver TESTE-COM-USUARIOS.md).
 * O app anota, no próprio aparelho, onde a pessoa erra, quanto tempo leva e onde desiste,
 * e guarda o que ela relata no botão "Travei aqui". Só se a pessoa ligar "Participar do
 * teste" (Perfil → Teste com usuários) e o Supabase estiver configurado, cada lição
 * terminada (ou abandonada) e cada relato também vão para as tabelas teste_licoes e
 * teste_relatos, sem nome nem e-mail: só um código aleatório do aparelho.
 */
export type TipoRelato = 'nao_entendi' | 'resposta_errada' | 'bug' | 'chato' | 'outro';
export const TIPOS_RELATO: { id: TipoRelato; icone: NomeIcone; texto: string }[] = [
  { id: 'nao_entendi', icone: 'pergunta', texto: 'Não entendi a explicação' },
  { id: 'resposta_errada', icone: 'x', texto: 'Acho que a resposta certa está errada' },
  { id: 'bug', icone: 'inseto', texto: 'Algo quebrou ou travou no app' },
  { id: 'chato', icone: 'triste', texto: 'Ficou chato ou repetitivo' },
  { id: 'outro', icone: 'conversa', texto: 'Outra coisa' },
];

type ExStat = { tent: number; erros: number; ms: number };
export type Relato = { ts: number; tipo: TipoRelato; texto: string; exId?: string; licao?: string };
type State = {
  codigo: string; // id anônimo do aparelho
  enviar: boolean; // a pessoa aceitou participar do teste (só então algo vai para o servidor)
  ex: Record<string, ExStat>;
  licoes: Record<string, { fez: number; abandonou: number; segundos: number }>;
  relatos: Relato[];
};

const novoCodigo = () => `t-${Math.random().toString(36).slice(2, 8)}`;

export const useTeste = create<State & {
  tentativa: (exId: string, ok: boolean, ms: number) => void;
  fimDeLicao: (licao: string, segundos: number, erros: Record<string, number>, abandonou: boolean) => void;
  relatar: (r: Omit<Relato, 'ts'>) => void;
  limpar: () => void;
  setEnviar: (v: boolean) => void;
}>()(
  persist(
    (set, get) => ({
      codigo: novoCodigo(), enviar: false, ex: {}, licoes: {}, relatos: [],
      setEnviar: (enviar) => set({ enviar }),
      tentativa: (exId, ok, ms) => set((s) => {
        const a = s.ex[exId] ?? { tent: 0, erros: 0, ms: 0 };
        return { ex: { ...s.ex, [exId]: { tent: a.tent + 1, erros: a.erros + (ok ? 0 : 1), ms: a.ms + Math.min(ms, 300_000) } } };
      }),
      fimDeLicao: (licao, segundos, erros, abandonou) => {
        set((s) => {
          const a = s.licoes[licao] ?? { fez: 0, abandonou: 0, segundos: 0 };
          return { licoes: { ...s.licoes, [licao]: { fez: a.fez + (abandonou ? 0 : 1), abandonou: a.abandonou + (abandonou ? 1 : 0), segundos: a.segundos + segundos } } };
        });
        if (get().enviar) supabase?.from('teste_licoes').insert({ aparelho: get().codigo, licao, segundos, erros, abandonou }).then(() => {}, () => {});
      },
      relatar: (r) => {
        set((s) => ({ relatos: [{ ...r, ts: Date.now() }, ...s.relatos].slice(0, 200) }));
        if (get().enviar) supabase?.from('teste_relatos').insert({ aparelho: get().codigo, tipo: r.tipo, texto: r.texto.slice(0, 1000), exercicio: r.exId ?? null, licao: r.licao ?? null }).then(() => {}, () => {});
      },
      limpar: () => set({ ex: {}, licoes: {}, relatos: [] }),
    }),
    { name: 'pypasso-teste', storage: createJSONStorage(() => AsyncStorage) },
  ),
);

/** Resumo legível: os exercícios mais difíceis, onde desistiram e os relatos. */
export function relatorio() {
  const s = useTeste.getState();
  const dificeis = Object.entries(s.ex)
    .filter(([, e]) => e.erros > 0)
    .map(([id, e]) => ({ id, ...e, taxa: e.erros / e.tent, onde: exercicioPorId(id)?.lesson.title ?? '?', pergunta: exercicioPorId(id)?.ex.q ?? '' }))
    .sort((a, b) => b.erros - a.erros || b.taxa - a.taxa)
    .slice(0, 15);
  const abandonos = Object.entries(s.licoes).filter(([, l]) => l.abandonou > 0)
    .map(([id, l]) => ({ id, titulo: lessonById(id)?.title ?? id, ...l })).sort((a, b) => b.abandonou - a.abandonou);
  const totalTent = Object.values(s.ex).reduce((n, e) => n + e.tent, 0);
  const totalErros = Object.values(s.ex).reduce((n, e) => n + e.erros, 0);
  const linhas = [
    `PyPasso, relatório de teste (aparelho ${s.codigo})`,
    `${Object.values(s.licoes).reduce((n, l) => n + l.fez, 0)} lições terminadas, ${abandonos.reduce((n, l) => n + l.abandonou, 0)} abandonadas, ${totalTent} respostas, ${totalErros} erros.`,
    '', 'Exercícios em que mais erraram:',
    ...dificeis.map((d) => `- ${d.id} (${d.onde}): ${d.erros} erro(s) em ${d.tent} tentativa(s). ${d.pergunta}`),
    '', 'Lições abandonadas no meio:',
    ...(abandonos.length ? abandonos.map((a) => `- ${a.id} ${a.titulo}: ${a.abandonou}x`) : ['- nenhuma']),
    '', 'Relatos ("Travei aqui"):',
    ...(s.relatos.length ? s.relatos.map((r) => `- [${TIPOS_RELATO.find((t) => t.id === r.tipo)?.texto}] ${r.exId ?? r.licao ?? ''} ${r.texto}`) : ['- nenhum']),
  ];
  return { dificeis, abandonos, relatos: s.relatos, texto: linhas.join('\n'), json: JSON.stringify({ codigo: s.codigo, ex: s.ex, licoes: s.licoes, relatos: s.relatos }) };
}
