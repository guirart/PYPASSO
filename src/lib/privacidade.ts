import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { initialPlayground, usePlayground } from './playground';
import { supabase } from './supabase';
import { useGame } from './store';
import { useTeste } from './teste';

/**
 * Central de privacidade: o que a pessoa escolheu compartilhar, a cópia dos dados dela e a limpeza.
 * Os textos mostrados ao usuário seguem a Política de Privacidade (store/politica-de-privacidade.html).
 */
export const PRIVACY_URL = process.env.EXPO_PUBLIC_PRIVACY_URL ?? '';
/** E-mail do encarregado/contato (preencha em .env: EXPO_PUBLIC_PRIVACY_EMAIL). Vazio = não aparece na tela. */
export const CONTATO_EMAIL = process.env.EXPO_PUBLIC_PRIVACY_EMAIL ?? '';

export type Consentimento = 'teste' | 'ia';
export type Registro = { item: Consentimento; valor: boolean; em: number };

type State = { ia: boolean; registros: Registro[] };
export const usePrivacidade = create<State>()(
  persist((): State => ({ ia: true, registros: [] }), { name: 'pypasso-privacidade', storage: createJSONStorage(() => AsyncStorage) }),
);

/** Liga ou desliga uma escolha e guarda quando isso aconteceu (prova do consentimento e da revogação). */
export function mudarConsentimento(item: Consentimento, valor: boolean) {
  if (item === 'teste') useTeste.getState().setEnviar(valor);
  else usePrivacidade.setState({ ia: valor });
  usePrivacidade.setState((s) => ({ registros: [{ item, valor, em: Date.now() }, ...s.registros].slice(0, 50) }));
}

/** Última vez que a pessoa mexeu numa escolha. */
export const ultimoRegistro = (registros: Registro[], item: Consentimento) => registros.find((r) => r.item === item);

/** Tudo o que o app guarda neste aparelho e, se houver conta, o que está na nuvem em nome da pessoa. */
export async function exportarDados(): Promise<{ texto: string; campos: number; nuvem: boolean }> {
  const chaves = (await AsyncStorage.getAllKeys()).filter((k) => k.startsWith('pypasso'));
  const pares = await AsyncStorage.multiGet(chaves);
  const aparelho: Record<string, unknown> = {};
  for (const [k, v] of pares) {
    try { aparelho[k] = v ? JSON.parse(v) : null; } catch { aparelho[k] = v; }
  }
  const saida: Record<string, unknown> = { geradoEm: new Date().toISOString(), app: 'PyPasso', neste_aparelho: aparelho };
  let nuvem = false;
  if (supabase) {
    const { data } = await supabase.auth.getUser();
    const u = data.user;
    if (u) {
      nuvem = true;
      const dela: Record<string, unknown> = { email: u.email, id: u.id, criada_em: u.created_at };
      const consulta = async (tabela: string, coluna: string) => {
        const r = await supabase!.from(tabela).select('*').eq(coluna, u.id).limit(5000);
        dela[tabela] = r.error ? `não foi possível ler (${r.error.message})` : r.data;
      };
      await Promise.allSettled([
        consulta('profiles', 'id'), consulta('lesson_progress', 'user_id'), consulta('xp_events', 'user_id'),
        consulta('league_history', 'user_id'), consulta('ai_reports', 'user_id'),
      ]);
      saida.na_nuvem = dela;
    }
  }
  return { texto: JSON.stringify(saida, null, 2), campos: Object.keys(aparelho).length, nuvem };
}

/** Apaga o que o app guardou neste aparelho: progresso, registros do teste e arquivos da aba Código do perfil em uso. */
export function apagarDadosDoAparelho() {
  useGame.getState().reset();
  useTeste.getState().limpar();
  usePlayground.setState(initialPlayground());
}
