import { expect, test } from '@playwright/test';
import { danoDoGolpe, danoNoBoss, escalaBoss, FRAQUEZA_CHEFE, FRAQUEZA_INIMIGO, LIMITE_GOLPE, vidaBoss, vidaDoInimigo } from '../src/lib/batalha';
import { custoMelhoria, MAX_MEL, poeiraDeDesmontar, valorMelhorado } from '../src/lib/melhoria';

test.describe('Lutas acompanham o nível do herói', () => {
  test('a vida do inimigo cresce com o nível, com a zona e na elite (antes era sempre 7)', () => {
    const base = vidaDoInimigo(7, 1, 0);
    expect(vidaDoInimigo(7, 5, 0)).toBeGreaterThan(base * 1.5);
    expect(vidaDoInimigo(7, 20, 0)).toBeGreaterThan(vidaDoInimigo(7, 10, 0));
    expect(vidaDoInimigo(7, 5, 12)).toBeGreaterThan(vidaDoInimigo(7, 5, 0));
    expect(vidaDoInimigo(7, 5, 3, true)).toBeGreaterThan(vidaDoInimigo(7, 5, 3));
  });

  test('nenhum golpe tira mais que 34% da vida: nunca dá para acabar a luta com um hit só', () => {
    for (const nivel of [1, 3, 8, 15, 30]) {
      for (const unidades of [5, 7, 10, 16]) {
        const vidaMax = vidaDoInimigo(unidades, nivel, 5);
        // golpe com TODOS os bônus: crítico, machado, arco, ponto fraco
        const dano = danoDoGolpe({ unidades: 2, nivel, mult: 1 + 0.5 + 0.25 + 0.25 + 0.25, vidaMax });
        expect(dano / vidaMax).toBeLessThanOrEqual(LIMITE_GOLPE + 1e-9);
        expect(Math.ceil(vidaMax / dano)).toBeGreaterThanOrEqual(3);
      }
    }
  });

  test('sem bônus, acertar tudo derruba o inimigo mais ou menos no fim da lição', () => {
    const unidades = 8, nivel = 6;
    const vidaMax = vidaDoInimigo(unidades, nivel, 0);
    let total = 0;
    for (let i = 0; i < unidades; i++) total += danoDoGolpe({ unidades: 1, nivel, mult: 1, vidaMax });
    expect(total).toBeGreaterThanOrEqual(vidaMax * 0.95); // zona 0: acaba no último acerto
  });

  test('o chefe da zona cresce com o nível e continua exigindo vários golpes', () => {
    expect(vidaBoss(1, 0)).toBe(100);
    expect(vidaBoss(10, 5)).toBeGreaterThan(vidaBoss(5, 5));
    expect(escalaBoss(10, 5)).toBeGreaterThan(escalaBoss(10, 0));
    for (const nivel of [1, 6, 15, 25]) {
      const hp = vidaBoss(nivel, 6);
      // o melhor golpe possível: bruto alto, Fúria alta e ponto fraco
      const melhor = danoNoBoss({ bruto: 60, nivel, zona: 6, furiaPct: 80, fraco: true });
      expect(Math.ceil(hp / melhor)).toBeGreaterThanOrEqual(4);
    }
  });

  test('o ponto fraco dá mais dano e todo inimigo e chefe tem um', () => {
    const normal = danoNoBoss({ bruto: 15, nivel: 3, zona: 2, furiaPct: 0, fraco: false });
    const fraco = danoNoBoss({ bruto: 15, nivel: 3, zona: 2, furiaPct: 0, fraco: true });
    expect(fraco).toBeGreaterThan(normal);
    for (const id of ['morcego', 'fogofatuo', 'bruxo', 'olho', 'cao', 'lodo', 'monstro', 'golem']) expect(FRAQUEZA_INIMIGO[id]).toBeTruthy();
    for (const id of ['aranha', 'besouro', 'escaravelho', 'centopeia', 'gosma', 'diabrete', 'caveira', 'lodo', 'golem', 'dragao']) expect(FRAQUEZA_CHEFE[id]).toBeTruthy();
  });
});

test.describe('Melhoria de peças com pó de forja', () => {
  test('desmontar peça rara rende mais pó e cada nível custa mais que o anterior', () => {
    for (let r = 2; r <= 5; r++) expect(poeiraDeDesmontar(r)).toBeGreaterThan(poeiraDeDesmontar(r - 1));
    for (let r = 1; r <= 5; r++) for (let m = 1; m < MAX_MEL; m++) expect(custoMelhoria(r, m)).toBeGreaterThan(custoMelhoria(r, m - 1));
    expect(custoMelhoria(5, 0)).toBeGreaterThan(custoMelhoria(1, 0));
  });

  test('a melhoria reforça cada habilidade sem passar dos limites', () => {
    expect(valorMelhorado('crit', 10, 0)).toBe(10);
    expect(valorMelhorado('crit', 10, 5)).toBe(18); // +75%
    expect(valorMelhorado('dano', 20, 2)).toBe(26);
    expect(valorMelhorado('tempo', 2, 4)).toBe(4);
    expect(valorMelhorado('vida', 6, 4)).toBe(4);
    expect(valorMelhorado('vida', 4, 5)).toBe(3); // nunca abaixo de 3 acertos seguidos
    expect(valorMelhorado('dica', 3, 5)).toBe(3); // teto de 3 dicas
    expect(valorMelhorado('protecao', 1, 3)).toBe(2);
    expect(valorMelhorado('protecao', 3, 5)).toBe(3);
  });
});
