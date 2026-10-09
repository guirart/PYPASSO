import { memo, useMemo } from 'react';
import { View } from 'react-native';
import { SvgXml } from 'react-native-svg';
import { ICONES, type NomeIcone } from './icones-data';

export type { NomeIcone };

/**
 * Ícone desenhado (sem emoji). Fontes: game-icons.net (CC BY 3.0) e Phosphor Icons (MIT),
 * escolhidos em tools/gerar_icones.py.
 */
export const Icone = memo(function Icone({ nome, size = 22, color = '#000' }: { nome: NomeIcone; size?: number; color?: string }) {
  const i = ICONES[nome];
  const xml = useMemo(
    () => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${i.w} ${i.h}">${i.b.replace(/currentColor/g, color)}</svg>`,
    [i, color],
  );
  return <SvgXml xml={xml} width={size} height={size} />;
});

/** Ícone branco num quadradinho colorido (missões, loja, conquistas, opções). */
export function IconeTile({ nome, cor, size = 44, apagado }: { nome: NomeIcone; cor: string; size?: number; apagado?: boolean }) {
  return (
    <View style={{
      width: size, height: size, borderRadius: size * 0.3, backgroundColor: apagado ? '#B8C2CE' : cor,
      borderBottomWidth: Math.max(2, size * 0.07), borderBottomColor: 'rgba(0,0,0,0.22)', alignItems: 'center', justifyContent: 'center',
    }}>
      <Icone nome={nome} size={size * 0.58} color="#fff" />
    </View>
  );
}
