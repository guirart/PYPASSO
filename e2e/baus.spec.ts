import { expect, test } from '@playwright/test';
import { BAUS_BOSS, BAUS_NORMAIS, FORCA_MAX, forcaBoss, forcaNormal, pesosPorForca, raridadePorForca, sortearBau, ZONAS } from '../src/lib/baus';

/** Gerador de números repetível (mulberry32), para a simulação dar sempre o mesmo resultado. */
function semente(a: number) {
  return () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
const N = 20000;
/** Fração de peças raras ou melhores (e épicas ou melhores) em N baús de uma zona. */
function simula(zona: number, tipo: 'normal' | 'boss', sorteio: () => number) {
  let raras = 0, epicas = 0;
  const modelos = new Set<string>();
  for (let i = 0; i < N; i++) {
    const { modelo, forca } = sortearBau(sorteio, zona, tipo);
    modelos.add(modelo.id);
    const r = raridadePorForca(sorteio, forca, 0, tipo === 'boss' ? 'incomum' : 'comum');
    if (r === 'raro' || r === 'epico' || r === 'lendario') raras++;
    if (r === 'epico' || r === 'lendario') epicas++;
  }
  return { raras: raras / N, epicas: epicas / N, modelos };
}

test.describe('Baús: quanto mais fundo, melhor', () => {
  test('a tabela de raridades soma 100 e a força cresce com a zona', () => {
    for (const f of [0, 0.7, 1, 2.35, 3.9, FORCA_MAX]) expect(pesosPorForca(f).reduce((s, p) => s + p, 0)).toBeCloseTo(100, 5);
    for (let z = 1; z < ZONAS; z++) {
      expect(forcaNormal(z)).toBeGreaterThan(forcaNormal(z - 1));
      expect(forcaBoss(z)).toBeGreaterThanOrEqual(forcaBoss(z - 1)); // o baú de chefe evolui junto
    }
  });

  test('nas zonas altas os baús raros e as peças raras aparecem muito mais', () => {
    const rnd = semente(1);
    const z0 = simula(0, 'normal', rnd), z6 = simula(6, 'normal', rnd), z12 = simula(12, 'normal', rnd);
    expect(z6.raras).toBeGreaterThan(z0.raras + 0.1);
    expect(z12.raras).toBeGreaterThan(z6.raras + 0.1);
    expect(z12.epicas).toBeGreaterThan(z0.epicas * 5);
    // baús raros (Místico e Ornado) só ficam comuns lá no fim
    expect(z0.modelos.has('n4')).toBe(false);
    expect(z12.modelos.has('n4')).toBe(true);
    expect(z0.modelos.has('n0')).toBe(true);
  });

  test('o baú de chefe é sempre melhor que o normal da zona, mas abaixo dos mais fortes', () => {
    const rnd = semente(2);
    for (const z of [0, 3, 6, 9, 12]) {
      const normal = simula(z, 'normal', rnd), boss = simula(z, 'boss', rnd);
      expect(boss.raras).toBeGreaterThan(normal.raras); // chances superiores às do baú normal
      expect(forcaBoss(z)).toBeGreaterThan(forcaNormal(z));
    }
    // o teto do baú de chefe fica abaixo do melhor baú possível, que só sai nas zonas finais
    expect(forcaBoss(ZONAS - 1)).toBeLessThan(FORCA_MAX);
    const chefeFinal = simula(12, 'boss', rnd), normalFinal = simula(12, 'normal', rnd);
    const melhorNormal = { epicas: pesosPorForca(FORCA_MAX).slice(3).reduce((s, p) => s + p, 0) / 100 };
    expect(chefeFinal.epicas).toBeLessThan(melhorNormal.epicas);
    expect(chefeFinal.raras).toBeGreaterThan(normalFinal.raras);
  });

  test('a aparência do baú de chefe acompanha a evolução', () => {
    const rnd = semente(3);
    expect(sortearBau(rnd, 0, 'boss').modelo.id).toBe(BAUS_BOSS[0].id);
    expect(sortearBau(rnd, 12, 'boss').modelo.id).toBe(BAUS_BOSS[2].id);
    expect(BAUS_NORMAIS).toHaveLength(5);
    expect(BAUS_BOSS.every((b) => b.boss)).toBe(true);
  });

  test('o chefe nunca deixa peça comum', () => {
    const rnd = semente(4);
    for (let i = 0; i < 3000; i++) expect(raridadePorForca(rnd, forcaBoss(0), 0, 'incomum')).not.toBe('comum');
  });
});
