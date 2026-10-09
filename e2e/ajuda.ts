import type { Page } from '@playwright/test';

/** Começa com um progresso de teste já salvo no navegador (a semente fixa deixa o mapa sempre igual). */
export async function comProgresso(page: Page, estado: Record<string, unknown> = {}) {
  await page.addInitScript((s) => {
    if (!localStorage.getItem('pypasso-game')) localStorage.setItem('pypasso-game', JSON.stringify({ state: s, version: 2 }));
  }, { xp: 120, nivelVisto: 2, semente: 'e2e', ...estado });
}

export const lerEstado = (page: Page) => page.evaluate(() => JSON.parse(localStorage.getItem('pypasso-game') ?? '{}').state ?? {});

/** Abre a seção "Mais atividades" da tela Aprender (ela começa recolhida). */
export const abrirMais = (page: Page) => page.getByRole('button', { name: 'Mais atividades' }).click();
