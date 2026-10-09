import { Image, Platform, View } from 'react-native';
import type { Folha } from '../inimigos-sprites';

/** Área onde um personagem "pisa": os pés ficam no meio da base e o resto cresce para cima. */
export const AREA_W = 150;
export const AREA_H = 124;

/**
 * Mostra um quadro de uma folha de sprites (quadros de 100x100 lado a lado), ampliado por um número inteiro
 * para os pixels ficarem nítidos. `cx` e `pe` são a coluna do centro e a linha dos pés do personagem no quadro.
 */
export function SpriteQuadro({ folha, escala, cx, pe, quadro, espelhar, areaW = AREA_W, areaH = AREA_H }: { folha: Folha; escala: number; cx: number; pe: number; quadro: number; espelhar?: boolean; areaW?: number; areaH?: number }) {
  const S = 100 * escala;
  const n = folha.quadros;
  // Espelhado, a coluna do centro vira (99 - cx)
  const col = espelhar ? 99 - cx : cx;
  const pixelado = Platform.OS === 'web' ? ({ imageRendering: 'pixelated' } as object) : null;
  return (
    <View style={{ width: areaW, height: areaH }} pointerEvents="none">
      <View style={{ position: 'absolute', width: S, height: S, overflow: 'hidden', left: areaW / 2 - (col + 0.5) * escala, top: areaH - (pe + 1) * escala, transform: espelhar ? [{ scaleX: -1 }] : undefined }}>
        <Image source={folha.src} resizeMode="stretch" resizeMethod="scale" style={[{ position: 'absolute', width: S * n, height: S, left: -Math.max(0, Math.min(n - 1, quadro)) * S }, pixelado]} />
      </View>
    </View>
  );
}
