import { useEffect, useState } from 'react';
import { Image, Platform, View, type ImageSourcePropType } from 'react-native';
import { SvgXml } from 'react-native-svg';
import { ARCO_H, ARCO_W, arcoSvg } from '../arco-art';
import { visualDe } from '@/lib/itens';
import { ANIMS, CENTRO, duracao, FRENTE, PES, type Anim, type AnimHeroi, type LookHeroi } from '@/lib/heroi';
import { MANA, type PaginaMana } from '../mana-sprites';
import { AREA_H, AREA_W } from './SpriteQuadro';

export const ATAQUE_HEROI_MS = duracao('golpe1');
export const DANO_HEROI_MS = duracao('dano');
export const SACAR_MS = duracao('sacar');

/** Em que quadro está uma animação, `ms` depois do começo. Repetidas voltam ao início; as outras param no último quadro. */
function quadroDe(a: Anim, ms: number): number {
  const total = a.ms.reduce((s, x) => s + x, 0);
  let t = a.loop ? ms % total : Math.min(ms, total - 1);
  for (let i = 0; i < a.ms.length; i++) { if (t < a.ms[i]) return i; t -= a.ms[i]; }
  return a.ms.length - 1;
}

/** Baixa de antemão as camadas do visual em todas as páginas, para a troca de animação não piscar com a imagem ainda carregando. */
function precarregar(look: LookHeroi) {
  (Object.keys(MANA) as PaginaMana[]).forEach((pg) => {
    const M = MANA[pg];
    const srcs = [
      M.bas[look.pele], M.out[`${look.roupa.estilo}_${look.roupa.cor}`],
      look.cabelo ? M.har[`${look.cabelo.estilo}_${look.cabelo.cor}`] : undefined,
      look.chapeu ? M.hat[`${look.chapeu.estilo}_${look.chapeu.cor}`] : undefined,
      pg !== 'p1' ? M.tla[`${look.arma.estilo}_${look.arma.cor}`] : undefined,
      pg !== 'p1' && look.escudo ? M.tlb[`${look.escudo.estilo}_${look.escudo.cor}`] : undefined,
    ];
    for (const s of srcs) {
      // no celular a imagem é um número (resolvido pelo RN); na web já vem como objeto com `uri`
      const uri = !s ? undefined : typeof s === 'number' ? (typeof Image.resolveAssetSource === 'function' ? Image.resolveAssetSource(s)?.uri : undefined) : (s as { uri?: string }).uri;
      if (uri) Image.prefetch(uri).catch(() => {});
    }
  });
}

/**
 * Personagem em camadas (corpo, roupa, cabelo, chapéu, arma e escudo) do Mana Seed. Cada camada é uma folha de 8x8 quadros
 * de 64x64; recortamos o mesmo quadro de todas e as empilhamos. Arma e escudo ficam na frente ou atrás do corpo conforme
 * o quadro (tabela FRENTE, lida dos guias do pacote). `desde` é o instante (ms) em que a animação começou.
 */
export function HeroiMana({ look, anim, desde, escala = 3, areaW = AREA_W, areaH = AREA_H, estatico = false }: { look: LookHeroi; anim: AnimHeroi; desde: number; escala?: number; areaW?: number; areaH?: number; estatico?: boolean }) {
  const [agora, setAgora] = useState(() => Date.now());
  useEffect(() => {
    if (estatico) return; // miniatura: fica no 1º quadro, sem relógio
    const iv = setInterval(() => setAgora(Date.now()), 40);
    return () => clearInterval(iv);
  }, []);
  const chave = JSON.stringify(look);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { if (!estatico) precarregar(look); }, [chave]);
  const arco = look.arma.estilo === 'arco';
  const mira = arco && (anim === 'golpe1' || anim === 'golpe2');
  // O arco não tem quadros próprios no pacote gratuito: ao atirar, usa a pose de braço esticado e o arco é desenhado por cima.
  const a = mira ? { ...ANIMS.golpe1, pg: 'pONE1' as const, cols: [3, 3, 3, 3] } : ANIMS[anim];
  const i = quadroDe(a, Math.max(0, agora - desde));
  const col = a.cols[i];
  const row = a.row;
  const M = MANA[a.pg];
  const combate = a.pg !== 'p1';
  const tabela = combate ? FRENTE[a.pg as 'pONE1' | 'pONE2' | 'pONE3'] : null;
  const armaNaFrente = tabela ? tabela.sw[row][col] === 'F' : false;
  const escudoNaFrente = tabela ? tabela.sh[row][col] === 'F' : false;

  const corpo: (ImageSourcePropType | undefined)[] = [
    M.bas[look.pele],
    M.out[`${look.roupa.estilo}_${look.roupa.cor}`],
    look.cabelo && look.chapeu?.estilo !== 'pfht' ? M.har[`${look.cabelo.estilo}_${look.cabelo.cor}`] : undefined, // a touca cobre o cabelo
    look.chapeu ? M.hat[`${look.chapeu.estilo}_${look.chapeu.cor}`] : undefined,
  ];
  const arma = combate && !arco ? M.tla[`${look.arma.estilo}_${look.arma.cor}`] : undefined;
  const escudo = combate && look.escudo ? M.tlb[`${look.escudo.estilo}_${look.escudo.cor}`] : undefined;
  // De baixo para cima: o que fica atrás do corpo, o corpo com suas peças, e o que fica na frente.
  const pilha = [
    !escudoNaFrente ? escudo : undefined, !armaNaFrente ? arma : undefined,
    ...corpo,
    escudoNaFrente ? escudo : undefined, armaNaFrente ? arma : undefined,
  ];

  const arcoHex = arco ? visualDe('arma', 'arco', look.arma.cor)?.hex ?? '#a8754a' : '';
  const puxado = mira && i < 2; // corda puxada antes de soltar
  // posição do arco no quadro de 64x64 (canto de cima à esquerda da arte): na mira fica na frente do braço esticado
  const pos = mira ? { x: 34, y: 18 } : { x: 30, y: 19 };
  const S = 64 * escala;
  const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;
  return (
    <View style={{ width: areaW, height: areaH }} pointerEvents="none">
      <View style={{ position: 'absolute', width: S, height: S, overflow: 'hidden', left: areaW / 2 - (CENTRO + 0.5) * escala, top: areaH - (PES + 1) * escala }}>
        {pilha.map((src, k) => src ? (
          <Image key={k} source={src} resizeMode="stretch" resizeMethod="scale" style={[{ position: 'absolute', width: 512 * escala, height: 512 * escala, left: -col * S, top: -row * S }, pixelado]} />
        ) : null)}
        {arco && combate && (
          <View style={{ position: 'absolute', left: (pos.x - 6) * escala, top: pos.y * escala, width: ARCO_W * escala, height: ARCO_H * escala }}>
            <SvgXml xml={arcoSvg(arcoHex, puxado)} width={ARCO_W * escala} height={ARCO_H * escala} />
          </View>
        )}
      </View>
    </View>
  );
}
