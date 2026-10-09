import { useState, type ReactNode } from 'react';
import { Image, Platform, StyleSheet, View, type ImageSourcePropType, type StyleProp, type ViewStyle } from 'react-native';

// Molduras do pacote "Crimson Fantasy GUI" (pixel art, vermelho e creme), recortadas em assets/crimson.
const MOLDURAS = {
  crimsonA: { src: require('../../assets/crimson/painel_a.png') as ImageSourcePropType, tam: 54, corte: 9 },
  crimsonB: { src: require('../../assets/crimson/painel_b.png') as ImageSourcePropType, tam: 48, corte: 9 },
  crimsonC: { src: require('../../assets/crimson/painel_c.png') as ImageSourcePropType, tam: 64, corte: 14 },
};
export type TipoMoldura = keyof typeof MOLDURAS;

const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;

/** Um pedaço da imagem (sx,sy,sw,sh) esticado para a caixa (dx,dy,dw,dh). */
function Fatia({ src, tam, sx, sy, sw, sh, dx, dy, dw, dh }: { src: ImageSourcePropType; tam: number; sx: number; sy: number; sw: number; sh: number; dx: number; dy: number; dw: number; dh: number }) {
  const kx = dw / sw, ky = dh / sh;
  return (
    <View style={{ position: 'absolute', left: dx, top: dy, width: dw, height: dh, overflow: 'hidden' }}>
      <Image source={src} resizeMode="stretch" resizeMethod="scale" style={[{ position: 'absolute', width: tam * kx, height: tam * ky, left: -sx * kx, top: -sy * ky }, pixelado]} />
    </View>
  );
}

/**
 * Moldura de 9 partes: os cantos ficam do tamanho original e as bordas/miolo se esticam, então serve para qualquer tamanho
 * de cartão. `esc` amplia os cantos (inteiro, para os pixels ficarem nítidos). O conteúdo ganha uma folga interna da borda.
 */
export function Moldura({ tipo = 'crimsonA', esc = 1, style, children }: { tipo?: TipoMoldura; esc?: number; style?: StyleProp<ViewStyle>; children?: ReactNode }) {
  const [tamanho, setTamanho] = useState({ w: 0, h: 0 });
  const { src, tam, corte } = MOLDURAS[tipo];
  const c = corte * esc;
  const { w, h } = tamanho;
  const meio = tam - 2 * corte;
  const ok = w > 2 * c && h > 2 * c;
  return (
    <View onLayout={(e) => setTamanho({ w: e.nativeEvent.layout.width, h: e.nativeEvent.layout.height })} style={[{ padding: Math.round(c * 0.75) }, style]}>
      {ok && (
        <View style={StyleSheet.absoluteFill} pointerEvents="none">
          {/* miolo e bordas primeiro, cantos por cima */}
          <Fatia src={src} tam={tam} sx={corte} sy={corte} sw={meio} sh={meio} dx={c} dy={c} dw={w - 2 * c} dh={h - 2 * c} />
          <Fatia src={src} tam={tam} sx={corte} sy={0} sw={meio} sh={corte} dx={c} dy={0} dw={w - 2 * c} dh={c} />
          <Fatia src={src} tam={tam} sx={corte} sy={tam - corte} sw={meio} sh={corte} dx={c} dy={h - c} dw={w - 2 * c} dh={c} />
          <Fatia src={src} tam={tam} sx={0} sy={corte} sw={corte} sh={meio} dx={0} dy={c} dw={c} dh={h - 2 * c} />
          <Fatia src={src} tam={tam} sx={tam - corte} sy={corte} sw={corte} sh={meio} dx={w - c} dy={c} dw={c} dh={h - 2 * c} />
          <Fatia src={src} tam={tam} sx={0} sy={0} sw={corte} sh={corte} dx={0} dy={0} dw={c} dh={c} />
          <Fatia src={src} tam={tam} sx={tam - corte} sy={0} sw={corte} sh={corte} dx={w - c} dy={0} dw={c} dh={c} />
          <Fatia src={src} tam={tam} sx={0} sy={tam - corte} sw={corte} sh={corte} dx={0} dy={h - c} dw={c} dh={c} />
          <Fatia src={src} tam={tam} sx={tam - corte} sy={tam - corte} sw={corte} sh={corte} dx={w - c} dy={h - c} dw={c} dh={c} />
        </View>
      )}
      {children}
    </View>
  );
}

