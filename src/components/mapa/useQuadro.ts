import { useEffect, useRef, useState } from 'react';
import { AccessibilityInfo } from 'react-native';
import type { BossMood } from '../boss-art';

/** Duração do ciclo de ataque (prepara, golpeia, volta). O golpe cai em 50% a 62% do ciclo (veja attackPose em boss-art.ts). */
export const ATAQUE_MS = 800;
export const ATAQUE_GOLPE_MS = ATAQUE_MS * 0.5;

/**
 * Quadro atual de um monstro numa luta: ataca (se mexe) quando `ataque` muda e fica ferido quando `golpe` muda.
 * Com "reduzir movimento" ligado no celular, mostra uma pose parada em vez de animar.
 */
export function useQuadro(golpe: number, ataque: number): { mood: BossMood; t: number } {
  const [q, setQ] = useState<{ mood: BossMood; t: number }>({ mood: 'normal', t: 0 });
  const raf = useRef<number | null>(null);
  const reduzir = useRef(false);

  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then((r) => { reduzir.current = r; }).catch(() => {});
  }, []);

  const parar = () => { if (raf.current !== null) { cancelAnimationFrame(raf.current); raf.current = null; } };

  useEffect(() => {
    if (!ataque) return;
    parar();
    if (reduzir.current) {
      setQ({ mood: 'attack', t: 0.6 });
      const fim = setTimeout(() => setQ({ mood: 'normal', t: 0 }), 500);
      return () => clearTimeout(fim);
    }
    const inicio = Date.now();
    let ultimo = 0;
    const passo = () => {
      const agora = Date.now();
      const t = (agora - inicio) / ATAQUE_MS;
      if (t >= 1) { setQ({ mood: 'normal', t: 0 }); raf.current = null; return; }
      if (agora - ultimo >= 33) { ultimo = agora; setQ({ mood: 'attack', t }); } // ~30 quadros por segundo
      raf.current = requestAnimationFrame(passo);
    };
    passo();
    return parar;
  }, [ataque]);

  useEffect(() => {
    if (!golpe) return;
    parar();
    setQ({ mood: 'hurt', t: 0 });
    const fim = setTimeout(() => setQ({ mood: 'normal', t: 0 }), 550);
    return () => clearTimeout(fim);
  }, [golpe]);

  return q;
}
