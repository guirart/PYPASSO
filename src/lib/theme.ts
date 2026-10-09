import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform, useColorScheme } from 'react-native';
import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';

const light = {
  bg: '#F2F5F8', surface: '#FFFFFF', ink: '#16212B', muted: '#5B6B78', line: '#D9E1E8', lineDeep: '#BFCBD5',
  brand: '#2F6FD6', brandDeep: '#1D4C9C', brandSoft: '#E3ECFB',
  sun: '#FFC83D', sunDeep: '#C99200', sunInk: '#4A3600',
  good: '#24A85E', goodDeep: '#17783F', goodBg: '#DDF5E7', goodInk: '#0F5A2F',
  bad: '#E1474C', badDeep: '#A82A2F', badBg: '#FCE3E4', badInk: '#7E1A1E',
  codeBg: '#14202B', codeFg: '#E4ECF2', cKw: '#FF9E64', cStr: '#9ECE6A', cNum: '#7DCFFF', cCom: '#6F8496', cBi: '#FFD866',
};
const dark: typeof light = {
  ...light,
  bg: '#0F161C', surface: '#18222B', ink: '#E5ECF1', muted: '#93A3B0', line: '#2A3743', lineDeep: '#1E2932',
  brand: '#4A8BEE', brandDeep: '#28589F', brandSoft: '#1B2C45',
  sunDeep: '#A87900', sunInk: '#3A2A00',
  good: '#38C277', goodDeep: '#1F7E48', goodBg: '#123122', goodInk: '#9BE5BB',
  bad: '#F0646A', badDeep: '#A3343A', badBg: '#3A181B', badInk: '#FFB7BA',
  codeBg: '#0B1117',
};
export type Palette = typeof light;

/** Aparência escolhida no Perfil: segue o celular, ou fica sempre clara/escura (vale para o aparelho todo). */
export type Tema = 'auto' | 'claro' | 'escuro';
export const useAparencia = create<{ tema: Tema; setTema: (t: Tema) => void }>()(
  persist((set) => ({ tema: 'auto', setTema: (tema) => set({ tema }) }), {
    name: 'pypasso-aparencia',
    version: 3, // v3: volta ao automático (quem foi forçado ao tema escuro da Idade das Trevas)
    migrate: (antigo) => ({ ...(antigo as object), tema: 'auto' }) as { tema: Tema; setTema: (t: Tema) => void },
    storage: createJSONStorage(() => AsyncStorage),
  }),
);

/** true quando o app está no modo escuro (pela escolha da pessoa ou pelo celular). */
export function useEscuro(): boolean {
  const sistema = useColorScheme();
  const tema = useAparencia((s) => s.tema);
  return tema === 'escuro' || (tema === 'auto' && sistema === 'dark');
}

export function useTheme(): Palette {
  return useEscuro() ? dark : light;
}

export const mono = Platform.select({ ios: 'Menlo', android: 'monospace', default: 'ui-monospace, Menlo, Consolas, monospace' });
