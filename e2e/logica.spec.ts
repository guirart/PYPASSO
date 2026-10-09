import { expect, test } from '@playwright/test';
import { classificar, equivalentes, lerFormula, mostrar, validade } from '../src/lib/logica/proposicional';
import { Prolog } from '../src/lib/logica/prolog';

const v = (p: string[], c: string) => validade(p.map(lerFormula), lerFormula(c));

test.describe('lógica proposicional', () => {
  test('modus ponens e modus tollens são válidos', () => {
    expect(v(['P -> Q', 'P'], 'Q').valido).toBe(true);
    expect(v(['P -> Q', '~Q'], '~P').valido).toBe(true);
  });
  test('falácias: afirmar o consequente e negar o antecedente são inválidas', () => {
    const a = v(['P -> Q', 'Q'], 'P');
    expect(a.valido).toBe(false);
    expect(a.contraExemplo).toEqual({ P: false, Q: true });
    expect(v(['P -> Q', '~P'], '~Q').valido).toBe(false);
  });
  test('silogismo disjuntivo e hipotético', () => {
    expect(v(['P | Q', '~P'], 'Q').valido).toBe(true);
    expect(v(['P -> Q', 'Q -> R'], 'P -> R').valido).toBe(true);
  });
  test('equivalências e classificação', () => {
    expect(equivalentes(lerFormula('P -> Q'), lerFormula('~Q -> ~P'))).toBe(true);
    expect(equivalentes(lerFormula('P -> Q'), lerFormula('Q -> P'))).toBe(false);
    expect(classificar(lerFormula('P | ~P'))).toBe('tautologia');
    expect(classificar(lerFormula('P & ~P'))).toBe('contradicao');
    expect(classificar(lerFormula('P -> Q'))).toBe('contingencia');
  });
  test('precedência, símbolos e erros', () => {
    expect(mostrar(lerFormula('~P ∧ Q ∨ R → S'))).toBe('¬P ∧ Q ∨ R → S');
    expect(mostrar(lerFormula('P -> Q -> R'))).toBe('P → Q → R');
    expect(() => lerFormula('P Q')).toThrow();
    expect(() => lerFormula('(P & Q')).toThrow();
  });
});

const consulta = (p: Prolog, q: string, max = 20) => p.consultar(q, max);

test.describe('mini-Prolog', () => {
  test('fatos, regras e consulta com variável', () => {
    const p = new Prolog();
    expect(p.carregar('pai(joao, maria). pai(joao, pedro). avo(X, Z) :- pai(X, Y), pai(Y, Z). pai(maria, ana).')).toEqual([]);
    expect(consulta(p, 'pai(joao, X).').solucoes.map((s) => s.X)).toEqual(['maria', 'pedro']);
    expect(consulta(p, 'avo(joao, Z).').solucoes).toEqual([{ Z: 'ana' }]);
    expect(consulta(p, 'pai(ana, _).').solucoes).toEqual([]);
  });
  test('listas, aritmética e corte', () => {
    const p = new Prolog();
    p.carregar('max(X, Y, X) :- X >= Y, !. max(_, Y, Y).');
    expect(consulta(p, 'append(X, Y, [1,2]).').solucoes.length).toBe(3);
    expect(consulta(p, 'length([a,b,c], N).').solucoes).toEqual([{ N: '3' }]);
    expect(consulta(p, 'X is 2 + 3 * 4.').solucoes).toEqual([{ X: '14' }]);
    expect(consulta(p, 'max(3, 7, M).').solucoes).toEqual([{ M: '7' }]);
    expect(consulta(p, 'reverse([1,2,3], R).').solucoes).toEqual([{ R: '[3,2,1]' }]);
    expect(consulta(p, 'sum_list([1,2,3], S), msort([c,a,b], L).').solucoes).toEqual([{ S: '6', L: '[a,b,c]' }]);
  });
  test('negação, se-então-senão, findall, forall, assert', () => {
    const p = new Prolog();
    p.carregar('gosta(a, b). gosta(b, a). gosta(c, a). ciumento(X) :- gosta(X, Y), gosta(Y, Z), X \\= Z, \\+ gosta(X, X).');
    expect(consulta(p, 'findall(X, gosta(X, a), L).').solucoes).toEqual([{ L: '[b,c]', X: '_' }]);
    expect(consulta(p, '( gosta(a, b) -> R = sim ; R = nao ).').solucoes).toEqual([{ R: 'sim' }]);
    expect(consulta(p, 'forall(member(X, [1,2,3]), X > 0).').solucoes.length).toBe(1);
    consulta(p, 'assert(contador(0)).');
    expect(consulta(p, 'retract(contador(N)), N1 is N+1, assert(contador(N1)).').solucoes.length).toBe(1);
    expect(consulta(p, 'contador(X).').solucoes).toEqual([{ X: '1' }]);
  });
  test('saída de texto e erros claros', () => {
    const p = new Prolog();
    expect(consulta(p, "format('Oi ~w!~n', [mundo]).").saida).toBe('Oi mundo!\n');
    expect(consulta(p, 'naoexiste(1).').erro).toMatch(/naoexiste\/1/);
    expect(consulta(p, 'foo(.').erro).toMatch(/sintaxe/i);
    p.carregar('loop :- loop.');
    expect(consulta(p, 'loop.').erro).toBeTruthy();
  });
  test('rainhas pequenas (permutation e backtracking)', () => {
    const p = new Prolog();
    p.carregar(`
      queens(N, Qs) :- numlist(1, N, Ns), permutation(Ns, Qs), seguro(Qs).
      seguro([]). seguro([Q|Qs]) :- sem_ataque(Q, Qs, 1), seguro(Qs).
      sem_ataque(_, [], _).
      sem_ataque(Q, [Q1|Qs], D) :- Q =\\= Q1 + D, Q =\\= Q1 - D, D1 is D+1, sem_ataque(Q, Qs, D1).`);
    expect(consulta(p, 'queens(6, Qs).', 10).solucoes.length).toBe(4);
  });
});

test('exemplos do laboratório Prolog dão o resultado anunciado', async () => {
  const { EXEMPLOS_PROLOG } = await import('../src/lib/logica/exemplos');
  for (const ex of EXEMPLOS_PROLOG) {
    const p = new Prolog();
    expect(p.carregar(ex.programa), ex.nome).toEqual([]);
    const r = p.consultar(ex.consulta, 1);
    expect(r.erro, ex.nome).toBeUndefined();
    const primeira = Object.entries(r.solucoes[0] ?? {}).map(([k, v]) => `${k} = ${v}`).join(', ');
    expect(primeira, ex.nome).toBe(ex.esperado);
  }
});

import { abrirMais, comProgresso } from './ajuda';

test.describe('Módulo de Lógica (telas)', () => {
  test('trilha Lógica abre uma lição com cartão de conceito', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/lesson/lg0l0');
    await expect(page.getByText('Enunciado: frase que pode ser verdadeira ou falsa')).toBeVisible();
    await expect(page.getByText('EXEMPLO', { exact: true })).toBeVisible();
    await page.getByRole('button', { name: /CONTINUAR|VERIFICAR/ }).first().click();
    await expect(page.getByText('Qual destas frases é um enunciado')).toBeVisible();
  });

  test('calculadora: afirmar o consequente é inválido e mostra contra-exemplo', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Calculadora de lógica' }).click();
    await expect(page.getByText('Argumento INVÁLIDO')).toBeVisible();
    await expect(page.getByText(/P = F, Q = V/)).toBeVisible();
    await page.getByRole('button', { name: 'Exemplo: Modus ponens' }).click();
    await expect(page.getByText('Argumento VÁLIDO')).toBeVisible();
    await page.getByLabel('Conclusão').fill('Q &');
    await expect(page.getByRole('alert')).toBeVisible();
  });

  test('laboratório Prolog roda o exemplo e responde', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Laboratório Prolog' }).click();
    await page.getByRole('button', { name: 'Rodar a pergunta' }).click();
    await expect(page.getByLabel('Resultado')).toContainText('X = maria');
    await page.getByRole('button', { name: 'Exemplo: Cavaleiros e patifes' }).click();
    await expect(page.getByLabel('Resultado')).toContainText('A = cavaleiro');
  });

  test('aba Lógica é uma lista simples, sem mapa', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await page.getByRole('tab', { name: /Lógica/ }).click();
    await expect(page.getByText('Legenda do mapa')).toHaveCount(0);
    await page.getByRole('button', { name: 'Lição: O que é um argumento' }).click();
    await expect(page.getByText('Enunciado: frase que pode ser verdadeira ou falsa')).toBeVisible();
  });
});
