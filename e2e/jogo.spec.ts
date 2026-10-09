import { expect, test } from '@playwright/test';
import { abrirMais, comProgresso, lerEstado } from './ajuda';

test.describe('PyPasso', () => {
  test('abre no mapa da primeira zona', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await expect(page.getByText('Primeiros passos').first()).toBeVisible({ timeout: 20_000 });
    await expect(page.getByText('Python do zero').first()).toBeVisible();
  });

  test('batalha: acertar tira vida do inimigo', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/lesson/u0l0?zona=u0&no=u0:1:0');
    const vida = page.getByText(/^\d+\/\d+$/).first();
    await expect(vida).toBeVisible({ timeout: 20_000 });
    const antes = Number((await vida.innerText()).split('/')[0]);
    await page.getByText('ENTENDI, CONTINUAR').click();
    await expect(page.getByText(/escolha a resposta/i)).toBeVisible();
    await expect(page.getByText(/Guardando na sua Biblioteca/)).toBeHidden({ timeout: 10_000 }); // a animação do livro cobre a tela por uns segundos
    await page.getByText('print()', { exact: true }).last().click();
    await page.getByRole('button', { name: 'VERIFICAR' }).click();
    await expect(page.getByText(/Perfeito|Isso aí|Mandou bem|Excelente|Muito bem/)).toBeVisible();
    await expect(async () => expect(Number((await vida.innerText()).split('/')[0])).toBeLessThan(antes)).toPass({ timeout: 5000 });
  });

  test('duelo: joga as 5 rodadas e guarda o recorde', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Duelo', exact: true }).click();
    await page.getByRole('button', { name: /Duelo contra Ana/ }).click();
    for (let r = 0; r < 5; r++) {
      await page.getByRole('button').nth(1).click(); // 1ª alternativa
      await page.getByRole('button', { name: /pr.xima|ver resultado/i }).click();
    }
    await expect(page.getByText(/Você venceu!|Empate!|Ana venceu/)).toBeVisible();
    const e = await lerEstado(page);
    const ana = (e.duelos as Record<string, { v: number; d: number; e: number }>).ana;
    expect(ana.v + ana.d + ana.e).toBe(1);
  });

  test('museu dos erros mostra o erro do primeiro chefe', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Museu dos erros' }).click();
    await expect(page.getByText('Diabrete do SyntaxError')).toBeVisible();
    await expect(page.getByText('O QUE O PYTHON DIZ')).toBeVisible();
  });

  test('privacidade: copia os dados e apaga os do aparelho', async ({ page, context }) => {
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
    await comProgresso(page, { name: 'Teste', xp: 200 });
    await page.goto('/');
    await page.getByText('Perfil', { exact: true }).last().click();
    await page.getByText('Privacidade e dados', { exact: true }).first().click();
    await page.getByRole('button', { name: 'COPIAR MEUS DADOS' }).click();
    await expect(page.getByText(/Copiei seus dados/)).toBeVisible();
    const copia = JSON.parse(await page.evaluate(() => navigator.clipboard.readText()));
    expect(copia.neste_aparelho['pypasso-game']).toBeTruthy();
    await page.getByRole('button', { name: /APAGAR OS DADOS DESTE APARELHO/ }).click();
    await page.getByRole('button', { name: /SIM, APAGAR/ }).click();
    await expect.poll(async () => (await lerEstado(page)).xp).toBe(0);
  });

  test('desafio do dia: resolve com o Python do navegador', async ({ page }) => {
    test.skip(!!process.env.E2E_SEM_PYTHON, 'Esse teste baixa o Python (Pyodide) da internet.');
    await comProgresso(page);
    await page.goto('/');
    await page.getByText('Desafio do dia', { exact: true }).first().click();
    await page.locator('textarea').fill('print("Olá, Python!")');
    await page.getByRole('button', { name: 'VERIFICAR' }).click();
    await expect(page.getByRole('button', { name: 'CONTINUAR' })).toBeVisible({ timeout: 60_000 });
    await page.getByRole('button', { name: 'CONTINUAR' }).click();
    await expect.poll(async () => (await lerEstado(page)).desafio?.feito).toBe(true);
  });

  test('tela de resultado rola: o botão Continuar fica ao alcance numa tela baixa', async ({ page }) => {
    test.skip(!!process.env.E2E_SEM_PYTHON, 'Esse teste baixa o Python (Pyodide) da internet.');
    await page.setViewportSize({ width: 360, height: 380 }); // baixa o bastante para o resultado não caber
    await comProgresso(page);
    await page.goto('/');
    await page.getByText('Desafio do dia', { exact: true }).first().click();
    await page.locator('textarea').fill('print("Olá, Python!")');
    await page.getByRole('button', { name: 'VERIFICAR' }).click();
    const continuar = page.getByRole('button', { name: 'CONTINUAR' });
    await expect(continuar).toBeVisible({ timeout: 60_000 });
    await continuar.scrollIntoViewIfNeeded();
    await expect(continuar).toBeInViewport();
    await continuar.click();
    await expect.poll(async () => (await lerEstado(page)).desafio?.feito).toBe(true);
  });
});
