import { expect, test, type Page } from '@playwright/test';
import curso from '../src/content/course.json';
import projetos from '../src/content/projetos.json';
import provas from '../src/content/provas.json';
import { abrirMais, comProgresso, lerEstado } from './ajuda';

type Bug = { id: string; linhas: string[]; linha: number; correcao: string; u: string | null };
const BUGS = (provas as { bugs: Bug[] }).bugs;

/** Faz os exercícios de escolha de uma lição com a resposta certa (a 1ª alternativa do arquivo de conteúdo). */
async function responderEscolha(page: Page, certa: string) {
  await page.getByText(certa, { exact: true }).last().click();
  await page.getByRole('button', { name: 'VERIFICAR' }).click();
  await page.getByRole('button', { name: 'CONTINUAR' }).click();
}

test.describe('Novidades', () => {
  test('dica do Pipo custa 2 XP cada e aparece no exercício de código', async ({ page }) => {
    test.skip(!!process.env.E2E_SEM_PYTHON, 'A 2ª dica usa o Python do navegador (baixado da internet).');
    await comProgresso(page);
    await page.goto('/lesson/desafio');
    const dica = page.getByRole('button', { name: /Pedir dica ao Pipo/ });
    await dica.click();
    await expect(page.getByText(/Rode seu código com RODAR/)).toBeVisible();
    await dica.click();
    await expect(page.getByText(/O Pipo olhou seu código/)).toBeVisible({ timeout: 60_000 });
    await dica.click();
    await expect(page.getByText(/Explicação da resposta/)).toBeVisible();
    await expect(dica).toBeHidden(); // 3 de 3
    await page.locator('textarea').fill('print("Olá, Python!")');
    await page.getByRole('button', { name: 'VERIFICAR' }).click();
    await expect(page.getByRole('button', { name: 'CONTINUAR' })).toBeVisible({ timeout: 60_000 });
    await page.getByRole('button', { name: 'CONTINUAR' }).click();
    // desafio de 1ª vez: 15 XP + 5 de "sem erros" - 3 dicas x 2 XP = 14 XP (120 de antes)
    await expect.poll(async () => (await lerEstado(page)).xp).toBe(134);
  });

  test('inimigo que esconde código: exercício de completar avisa o golpe em cheio', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/lesson/u0l0?zona=u0&no=u0:1:0');
    const ex = curso.units[0].lessons[0].exercises as { k: string; o?: string[] }[];
    for (let i = 0; i < ex.length && ex[i].k !== 'fill'; i++) {
      if (ex[i].k === 'learn') {
        await page.getByText('ENTENDI, CONTINUAR').click();
        await expect(page.getByText(/Guardando na sua Biblioteca/)).toBeHidden({ timeout: 10_000 });
      } else await responderEscolha(page, ex[i].o![0]);
    }
    await expect(page.getByText(/Escondeu parte do código/)).toBeVisible();
  });

  test('chefe da zona: a fase 2 pede o conserto da linha', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/prova?unit=u0');
    await page.getByRole('button', { name: 'LUTAR' }).click();
    // acha o bug na tela pelo texto das linhas e toca na linha certa
    const achaBug = async () => {
      const rotulos = await page.locator('[aria-label^="Linha "]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') ?? ''));
      const linhas = rotulos.map((r) => r.replace(/^Linha \d+: /, '').replace(/^vazia$/, ''));
      const bug = BUGS.find((b) => b.u === 'u0' && b.linhas.length === linhas.length && b.linhas.every((l, i) => l.trim() === linhas[i].trim()));
      expect(bug, 'bug da tela não encontrado no banco').toBeTruthy();
      return bug!;
    };
    // Cada acerto tira de 22 a 40 de vida. A fase 2 começa com a vida em 60 ou menos, então aparece
    // a partir do 2º ou 3º acerto: toca nas linhas certas até o chefe pedir o conserto.
    const fase = page.getByText(/Agora, como fica o conserto\?/);
    let b!: Bug;
    for (let rodada = 0; rodada < 4 && !(await fase.isVisible()); rodada++) {
      b = await achaBug();
      await page.locator('[aria-label^="Linha "]').nth(b.linha).click();
      if (await fase.isVisible().catch(() => false)) break;
      await page.getByRole('button', { name: /pr.ximo ataque|ver resultado/i }).click();
    }
    await expect(fase).toBeVisible();
    await expect(page.getByText(/FASE [23]/)).toBeVisible();
    // a linha pode começar com espaços (recuo do Python); por isso a busca é pelo texto do botão, sem depender deles
    await page.locator('[aria-label^="Conserto:"]').filter({ hasText: b.correcao.trim() }).first().click();
    await expect(page.getByText(/Acertou! -\d+ de vida do chefe/)).toBeVisible();
  });

  const BASICOS = [
    { id: 'basico-arma', slot: 'arma', estilo: 'sw01', cor: 'v01', raridade: 'comum', hab: [] },
    { id: 'basico-escudo', slot: 'escudo', estilo: 'sh01', cor: 'v01', raridade: 'comum', hab: [] },
    { id: 'basico-roupa', slot: 'roupa', estilo: 'fstr', cor: 'v01', raridade: 'comum', hab: [] },
  ];
  const ARCO = { id: 't-arco', slot: 'arma', estilo: 'arco', cor: 'v03', raridade: 'epico', hab: [{ id: 'crit', v: 12 }, { id: 'xp', v: 9 }] };
  const CHAPEU = { id: 't-chapeu', slot: 'chapeu', estilo: 'pnty', cor: 'v01', raridade: 'raro', hab: [{ id: 'dica', v: 1 }] };

  test('inventário: equipa o arco, soma as habilidades e desmonta uma peça', async ({ page }) => {
    await comProgresso(page, { moedas: 10, inv: [...BASICOS, ARCO, CHAPEU] });
    await page.goto('/inventario');
    // equipar o arco muda a arma e liga as habilidades dele
    await page.getByRole('button', { name: /^Arco de Ébano da Precisão, Épico$/ }).click();
    await page.getByRole('button', { name: /^Equipar Arco/ }).click();
    await expect.poll(async () => (await lerEstado(page)).equip.arma).toBe('t-arco');
    await expect(page.getByText('+12% de chance de golpe crítico').first()).toBeVisible();
    await expect(page.getByText('+9% de XP nas lições').first()).toBeVisible();
    await expect(page.getByText(/Arco: Ataca de longe/).first()).toBeVisible();
    await expect(page.getByText(/Passiva: A partir de 3 acertos seguidos/).first()).toBeVisible();
    // chapéu é opcional: dá para vestir e tirar
    await page.getByRole('button', { name: /^Chapéu de Mago Azul do Pipo, Raro$/ }).click();
    await page.getByRole('button', { name: /^Equipar Chapéu/ }).click();
    expect((await lerEstado(page)).equip.chapeu).toBe('t-chapeu');
    await page.getByRole('button', { name: /^Tirar Chapéu/ }).click();
    expect((await lerEstado(page)).equip.chapeu).toBeNull();
    // desmontar devolve moedas e volta ao item básico se era a peça vestida
    await page.getByRole('button', { name: /^Arco de Ébano da Precisão, Épico$/ }).click();
    await page.getByRole('button', { name: /^Desmontar Arco/ }).click();
    await expect.poll(async () => (await lerEstado(page)).moedas).toBe(70);
    expect((await lerEstado(page)).equip.arma).toBe('basico-arma');
    expect((await lerEstado(page)).inv.some((i: { id: string }) => i.id === 't-arco')).toBe(false);
  });

  test('inventário: baú só vem de chefe (não há como comprar baú)', async ({ page }) => {
    await comProgresso(page, { moedas: 999 });
    await page.goto('/inventario');
    await expect(page.getByText('MOCHILA')).toBeVisible();
    await expect(page.getByRole('button', { name: /Abrir o baú/ })).toBeHidden();
    await expect(page.getByText('MOCHILA · 3')).toBeVisible(); // só os 3 itens básicos
  });

  test('habilidade Pipo: a dica sai de graça e a seguinte custa XP', async ({ page }) => {
    await comProgresso(page, { inv: [...BASICOS, CHAPEU], equip: { arma: 'basico-arma', escudo: 'basico-escudo', roupa: 'basico-roupa', chapeu: 't-chapeu' } });
    await page.goto('/lesson/desafio');
    const dica = page.getByRole('button', { name: /Pedir dica ao Pipo/ });
    await expect(dica).toContainText('grátis');
    await dica.click();
    await expect(dica).toContainText('-2 XP');
  });

  test('inventário: as habilidades novas (Vitalidade, Relógio, Fúria) somam na ficha', async ({ page }) => {
    const ESCUDO = { id: 't-esc', slot: 'escudo', estilo: 'sh02', cor: 'v01', raridade: 'epico', hab: [{ id: 'vida', v: 6 }, { id: 'protecao', v: 2 }] };
    const CHAP = { id: 't-cha', slot: 'chapeu', estilo: 'pfht', cor: 'v02', raridade: 'raro', hab: [{ id: 'tempo', v: 3 }, { id: 'dano', v: 18 }] };
    await comProgresso(page, { inv: [...BASICOS, ESCUDO, CHAP], equip: { arma: 'basico-arma', escudo: 't-esc', roupa: 'basico-roupa', chapeu: 't-cha' } });
    await page.goto('/inventario');
    await expect(page.getByText('Recupera 1 vida a cada 6 acertos seguidos')).toBeVisible();
    await expect(page.getByText('+3s por bug nas lutas de chefe')).toBeVisible();
    await expect(page.getByText('+18% de dano nos chefes')).toBeVisible();
    await expect(page.getByText('Ignora 2 erros por lição (sem perder vida)')).toBeVisible();
    await expect(page.getByText('✦ +5% de chance de golpe crítico')).toBeVisible(); // passiva da espada
  });

  test('primeira página: painel de nível e vidas, e o evento da semana fica escondido', async ({ page }) => {
    await comProgresso(page, { xp: 200, hearts: 4 }); // 200 XP já é nível 3 ou mais
    await page.goto('/');
    await expect(page.getByRole('button', { name: /^Nível \d+, .*XP para o próximo nível/ })).toBeVisible();
    await expect(page.getByRole('button', { name: /4 de 5 vidas/ })).toBeVisible();
    await expect(page.getByText(/Evento: /)).toBeHidden(); // o evento não fica jogado na tela
    await page.goto('/missoes');
    await expect(page.getByText(/Evento da semana: /)).toBeVisible(); // liberado no nível 3, dentro das Missões
  });

  test('evento da semana continua escondido antes do nível 3', async ({ page }) => {
    await comProgresso(page, { xp: 10 });
    await page.goto('/missoes');
    await expect(page.getByText('Missões do dia')).toBeVisible();
    await expect(page.getByText(/Evento da semana: /)).toBeHidden();
  });

  test('inimigo da lição: a vida acompanha o nível do herói e o 1º golpe não derruba', async ({ page }) => {
    await comProgresso(page, { xp: 600 }); // nível alto: antes o inimigo tinha sempre 7 de vida
    await page.goto('/lesson/u0l0?zona=u0&no=u0:1:0');
    const barra = page.getByLabel(/de \d+ de vida/).first();
    const vida = async () => { const m = /: (\d+) de (\d+) de vida/.exec((await barra.getAttribute('aria-label')) ?? '')!; return { hp: +m[1], max: +m[2] }; };
    const antes = await vida();
    expect(antes.max).toBeGreaterThan(50); // escala do nível, não os 7 de antes
    const ex = curso.units[0].lessons[0].exercises as { k: string; o?: string[] }[];
    for (let i = 0; i < ex.length; i++) { // passa pelos cartões de conceito e responde o primeiro exercício
      if (ex[i].k === 'learn') {
        await page.getByText('ENTENDI, CONTINUAR').click();
        await expect(page.getByText(/Guardando na sua Biblioteca/)).toBeHidden({ timeout: 10_000 });
      } else { await responderEscolha(page, ex[i].o![0]); break; }
    }
    const depois = await vida();
    expect(depois.hp).toBeLessThan(depois.max); // levou dano
    expect(depois.hp).toBeGreaterThanOrEqual(depois.max * 0.6); // e o golpe sozinho não tira mais de 40%
  });

  test('inventário: desmontar rende pó e o pó melhora a peça', async ({ page }) => {
    const RARA = { id: 't-rara', slot: 'arma', estilo: 'ax01', cor: 'v01', raridade: 'raro', hab: [{ id: 'crit', v: 10 }] };
    const COMUM2 = { id: 't-c2', slot: 'escudo', estilo: 'sh02', cor: 'v01', raridade: 'epico', hab: [{ id: 'protecao', v: 1 }] };
    await comProgresso(page, { inv: [...BASICOS, RARA, COMUM2], poeira: 0 });
    await page.goto('/inventario');
    // sem pó: avisa quanto falta
    await page.getByRole('button', { name: /^Machado de Aço da Precisão, Raro$/ }).click();
    await page.getByRole('button', { name: /^Melhorar Machado/ }).click();
    await expect(page.getByText(/Faltam \d+ de pó de forja/)).toBeVisible();
    // desmontar o escudo épico rende 8 de pó (e moedas)
    await page.getByRole('button', { name: /Escudo Escuro de Prata da Guarda, Épico/ }).or(page.getByRole('button', { name: /^Escudo Escuro .*, Épico$/ })).first().click();
    await page.getByRole('button', { name: /^Desmontar / }).click();
    await expect.poll(async () => (await lerEstado(page)).poeira).toBe(8);
    // o machado raro custa 5 de pó no nível 0: melhora para +1 e o crítico sobe de 10% para 12%
    await page.getByRole('button', { name: /^Machado de Aço da Precisão, Raro$/ }).click();
    await page.getByRole('button', { name: /^Melhorar Machado/ }).click();
    await expect.poll(async () => (await lerEstado(page)).poeira).toBe(3);
    const mel = (await lerEstado(page)).inv.find((i: { id: string }) => i.id === 't-rara').mel;
    expect(mel).toBe(1);
  });

  test('aparência: troca pele e cabelo', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/personagem');
    await page.getByRole('button', { name: 'Cabelo: Bob' }).click();
    await page.getByRole('button', { name: 'Pele, cor 3' }).click();
    await expect.poll(async () => (await lerEstado(page)).heroi).toMatchObject({ cabelo: { estilo: 'bob1' }, pele: 'v04' });
  });

  test('missões ficam em Mais atividades (a aba agora é o Inventário)', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await expect(page.getByText('Inventário', { exact: true }).first()).toBeVisible();
    await abrirMais(page);
    await page.getByRole('button', { name: 'Missões', exact: true }).click();
    await expect(page.getByText('Missões do dia')).toBeVisible();
  });

  test('chefe derrotado deixa cair uma peça no inventário', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/prova?unit=u0');
    await page.getByRole('button', { name: 'LUTAR' }).click();
    let b!: Bug;
    const achaBug = async () => {
      const rotulos = await page.locator('[aria-label^="Linha "]').evaluateAll((els) => els.map((e) => e.getAttribute('aria-label') ?? ''));
      const linhas = rotulos.map((r) => r.replace(/^Linha \d+: /, '').replace(/^vazia$/, ''));
      return BUGS.find((x) => x.u === 'u0' && x.linhas.length === linhas.length && x.linhas.every((l, i) => l.trim() === linhas[i].trim()))!;
    };
    for (let i = 0; i < 40 && !(await page.getByText('O CHEFE DEIXOU CAIR UM BAÚ').isVisible()); i++) {
      const proximo = page.getByRole('button', { name: /pr.ximo ataque|ver resultado/i });
      if (await proximo.isVisible().catch(() => false)) { await proximo.click(); continue; }
      const conserto = page.locator('[aria-label^="Conserto:"]');
      if (await conserto.first().isVisible().catch(() => false)) { await conserto.filter({ hasText: b.correcao.trim() }).first().click(); continue; }
      if (await page.locator('[aria-label^="Linha "]').first().isVisible().catch(() => false)) {
        b = await achaBug();
        await page.locator('[aria-label^="Linha "]').nth(b.linha).click();
      } else await page.waitForTimeout(200);
    }
    await expect(page.getByText('O CHEFE DEIXOU CAIR UM BAÚ')).toBeVisible();
    await page.getByRole('button', { name: 'Abrir o baú do chefe' }).click();
    await page.getByRole('button', { name: 'Pular a animação' }).click();
    await page.getByRole('button', { name: 'Pegar a peça' }).click();
    await expect(page.getByText('O CHEFE DEIXOU CAIR UMA PEÇA')).toBeVisible();
    await page.getByRole('button', { name: 'CONTINUAR' }).click();
    const st = await lerEstado(page);
    expect(st.inv.length).toBe(4); // 3 básicos + a peça
    const peca = st.inv.find((i: { id: string }) => !i.id.startsWith('basico-'));
    expect(peca.novo).toBe(true);
    expect(peca.raridade).not.toBe('comum'); // chefes não deixam cair peça comum
  });

  test('duelo: o adversário comenta no começo da rodada', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Duelo', exact: true }).click();
    await page.getByRole('button', { name: /Duelo contra Bia/ }).click();
    await expect(page.getByText(/^Bia: “/)).toBeVisible();
  });

  test('resumo da semana, certificado e detetive abrem', async ({ page }) => {
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Resumo da semana' }).click();
    await expect(page.getByText('DIAS ESTUDADOS')).toBeVisible();
    await page.goBack();
    await abrirMais(page);
    await page.getByRole('button', { name: 'Certificados' }).click();
    await page.getByRole('button', { name: 'VER EXEMPLO' }).first().click();
    await expect(page.getByText('CERTIFICADO DE CONCLUSÃO')).toBeVisible();
    await page.goBack();
    await abrirMais(page);
    await page.getByRole('button', { name: 'Detetive de bugs' }).click();
    await expect(page.getByRole('button', { name: 'ANALISAR MEU CÓDIGO' })).toBeVisible();
  });

  test('detetive de bugs: aponta o erro do código', async ({ page }) => {
    test.skip(!!process.env.E2E_SEM_PYTHON, 'Usa o Python do navegador (baixado da internet).');
    await comProgresso(page);
    await page.goto('/');
    await abrirMais(page);
    await page.getByRole('button', { name: 'Detetive de bugs' }).click();
    await page.getByRole('button', { name: 'ANALISAR MEU CÓDIGO' }).click();
    await expect(page.getByText('O programa deu erro')).toBeVisible({ timeout: 60_000 });
    await expect(page.getByText(/SyntaxError/).first()).toBeVisible();
  });

  test('projeto concluído: copia o cartão para compartilhar', async ({ page, context }) => {
    test.skip(!!process.env.E2E_SEM_PYTHON, 'O cartão roda o programa com o Python do navegador.');
    await context.grantPermissions(['clipboard-read', 'clipboard-write']);
    const P = projetos.projetos[0];
    await comProgresso(page, { done: { [P.requer]: 100 }, projetos: { [P.id]: { passo: P.passos.length - 1, codigo: 'print("oi")', feito: true } } });
    await page.goto(`/projeto/${P.id}`);
    await page.getByRole('button', { name: /compartilhar meu projeto/i }).click();
    await expect.poll(() => page.evaluate(() => navigator.clipboard.readText()), { timeout: 60_000 }).toContain(`Fiz o projeto “${P.titulo}” no PyPasso!`);
  });
});
