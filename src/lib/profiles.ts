import AsyncStorage from '@react-native-async-storage/async-storage';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import { LEGACY_IDS } from '@/content';
import { initialPlayground, usePlayground } from './playground';
import { initialGame, useGame } from './store';

/**
 * Vários perfis no mesmo aparelho (estilo "quem está assistindo?").
 * Cada perfil tem progresso, vidas, liga e arquivos da aba Código próprios: os dados ficam
 * em chaves separadas do armazenamento ("pypasso-game:<id>"). O primeiro perfil usa as
 * chaves antigas, então quem já usava o app não perde nada.
 *
 * Conta online: o aparelho tem uma sessão do Supabase. Ela fica ligada ao perfil que
 * entrou (conta: true); os outros perfis estudam offline, na liga de treino.
 */
export type Perfil = { id: string; nome: string; avatar: string; conta?: boolean };
export const MAX_PERFIS = 5;

type State = { perfis: Perfil[]; ativo: string; perguntar: boolean };
type Actions = {
  criar: (nome: string) => string | null;
  editar: (id: string, p: Partial<Pick<Perfil, 'nome' | 'avatar'>>) => void;
  setPerguntar: (v: boolean) => void;
  ligarConta: (id: string | null) => void;
};

const novaSemente = () => Math.random().toString(36).slice(2, 10);

export const useProfiles = create<State & Actions>()(
  persist(
    (set, get) => ({
      perfis: [],
      ativo: 'p1',
      perguntar: true,
      criar: (raw) => {
        const nome = raw.trim().slice(0, 20);
        if (!nome) return null;
        if (get().perfis.length >= MAX_PERFIS) return null;
        const id = `p${Date.now().toString(36)}`;
        set((s) => ({ perfis: [...s.perfis, { id, nome, avatar: novaSemente() }] }));
        return id;
      },
      editar: (id, p) => set((s) => ({ perfis: s.perfis.map((x) => (x.id === id ? { ...x, ...p } : x)) })),
      setPerguntar: (perguntar) => set({ perguntar }),
      ligarConta: (id) => set((s) => ({ perfis: s.perfis.map((x) => ({ ...x, conta: x.id === id })) })),
    }),
    { name: 'pypasso-profiles', storage: createJSONStorage(() => AsyncStorage) },
  ),
);

export const gameKey = (id: string) => (id === 'p1' ? 'pypasso-game' : `pypasso-game:${id}`);
export const playgroundKey = (id: string) => (id === 'p1' ? 'pypasso-playground' : `pypasso-playground:${id}`);

export const perfilAtivo = () => {
  const { perfis, ativo } = useProfiles.getState();
  return perfis.find((p) => p.id === ativo) ?? null;
};

/** A conta online pertence ao perfil ativo? (Sem dono definido ainda, vale para o ativo.) */
export const contaDoPerfilAtivo = () => {
  const { perfis, ativo } = useProfiles.getState();
  const dono = perfis.find((p) => p.conta);
  return !dono || dono.id === ativo;
};

/** Carrega um store com persist a partir de outra chave (ou do estado inicial, se for novo). */
async function carregar<T>(
  store: { persist: { setOptions: (o: { name: string }) => void; rehydrate: () => Promise<void> | void }; setState: (s: Partial<T>) => void },
  key: string,
  inicial: () => Partial<T>,
) {
  const salvo = await AsyncStorage.getItem(key);
  store.persist.setOptions({ name: key });
  if (salvo) await store.persist.rehydrate();
  else store.setState(inicial()); // perfil novo: começa do zero (e isso já salva na chave nova)
}

/** Troca o perfil ativo: o estado do perfil atual já está salvo; carregamos o do outro. */
export async function trocarPerfil(id: string) {
  const p = useProfiles.getState().perfis.find((x) => x.id === id);
  if (!p) return;
  useProfiles.setState({ ativo: id });
  await carregar(useGame, gameKey(id), () => ({ ...initialGame(), name: p.nome, avatarSeed: p.avatar }));
  await carregar(usePlayground, playgroundKey(id), initialPlayground);
  useGame.getState().migrateIds(LEGACY_IDS);
  useGame.getState().tick();
}

/** Apaga um perfil e seus dados. Não apaga o perfil ativo nem o último. */
export async function removerPerfil(id: string) {
  const { perfis, ativo } = useProfiles.getState();
  if (id === ativo || perfis.length <= 1) return false;
  useProfiles.setState({ perfis: perfis.filter((x) => x.id !== id) });
  await AsyncStorage.multiRemove([gameKey(id), playgroundKey(id)]);
  return true;
}

/**
 * Na abertura do app (depois que os dados carregarem): cria o primeiro perfil a partir de
 * quem já usava o app, volta para o último perfil usado e mantém nome/avatar em dia.
 */
export async function iniciarPerfis() {
  const g = useGame.getState();
  const { perfis, ativo } = useProfiles.getState();
  if (!perfis.length) {
    useProfiles.setState({ perfis: [{ id: 'p1', nome: g.name || 'Eu', avatar: g.avatarSeed }], ativo: 'p1' });
  } else if (ativo !== 'p1') {
    await trocarPerfil(ativo);
  }
  // Nome e avatar do perfil seguem o que a pessoa muda no Perfil.
  return useGame.subscribe((s) => {
    const p = perfilAtivo();
    if (p && (p.avatar !== s.avatarSeed || (s.name && p.nome !== s.name))) {
      useProfiles.getState().editar(p.id, { avatar: s.avatarSeed, nome: s.name || p.nome });
    }
  });
}

const esperar = (store: { persist: { hasHydrated: () => boolean; onFinishHydration: (f: () => void) => () => void } }) =>
  new Promise<void>((ok) => {
    if (store.persist.hasHydrated()) return ok();
    const un = store.persist.onFinishHydration(() => { un(); ok(); });
  });

/** Espera os três armazenamentos carregarem. */
export const perfisProntos = () => Promise.all([esperar(useGame), esperar(usePlayground), esperar(useProfiles)]);
