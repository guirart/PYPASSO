# PyPasso

App para aprender Python em lições curtas, no formato de trilha com vidas, XP, sequência de dias e liga semanal. Um único código gera a versão web, Android e iPhone (Expo + React Native).

## O que já está pronto

- Trilha com 13 unidades e 27 lições, do `print` a classes e objetos (passando por dicionários, strings, um módulo inteiro de métodos de string, exceções e arquivos): 77 cartões de "Novo conceito" que ensinam cada função antes de ela ser cobrada, e 145 exercícios.
- Segunda trilha **71 funções embutidas**: começa com a seção "Antes dos built-ins" (3 unidades de 6 lições: valores e textos; coleções e repetição; funções, erros e classes), para quem nunca programou. `tools/conferir_ordem.py` garante que nenhum conceito (string, lista, if, def, try, class…) aparece antes da lição que o ensina, e o gerador recusa a trilha se aparecer. Depois, cada uma das 71 funções built-in do Python (de `abs` a `zip`, incluindo `aiter`, `memoryview`, `__import__`…) é uma unidade com 6 lições (o básico, parâmetros, usos práticos, pegadinhas, combinações e um desafio de código) e uma Prova de fogo própria. Depois vêm 6 unidades que combinam as funções. Total: 80 unidades, 464 lições e 1.780 exercícios. As lições 2 a 6 ficam em `tools/builtins_licoes/` (formato em `LEIA.md`); `tools/validar_builtins.py` roda cada exemplo, resposta, solução e bug, e `tools/gerar_builtins.py` monta `src/content/builtins.json`.
- Seis tipos de exercício: múltipla escolha, prever a saída, completar lacunas, ordenar linhas, digitar a saída e **escrever e rodar código Python de verdade** (Pyodide, corrigido por testes automáticos).
- Personagens que apresentam cada exercício num balão de fala e reagem a acertos e erros: a mascote Pipo e o elenco de bichinhos Ana, Caio, Bia e Téo.
- Aba **Biblioteca**: 151 funções e recursos do Python (print, len, strip, center, join, sort, dict.get, enumerate, zip, open, try, random…) explicados para iniciantes, com como escrever, parâmetros, o que devolve, exemplo com a saída real, "Cuidado" com as pegadinhas e funções relacionadas. Busca sem acento, categorias, filtro "71 built-ins" (de A a Z), favoritos, botão "Testar no editor" e "Fazer a lição" para abrir a lição da função.
- Aba **Código**: editor no estilo VS Code (abas de arquivo, cores, números de linha, recuo automático), terminal com `>>>`, `input()` interativo (o programa pausa e o terminal pede a resposta, como no VS Code; a caixa Entrada é opcional), `import` entre arquivos e exemplos prontos.
- **Pipo assistente de código**, um personagem flutuante que pode ser arrastado pela tela: quando o programa dá erro, ele fica triste, abre uma caixa de diálogo, marca a linha no editor, explica em português o que aconteceu e por quê, mostra como o código fica corrigido (com diferença linha a linha) e aplica a correção com um toque. Mesmo sem erro, ele dá dicas de estilo e aponta bugs escondidos. Funciona offline; com IA configurada, oferece também uma explicação completa e o código reescrito. Nos exercícios das lições ele explica o erro sem entregar a resposta.
- **Editor de avatar** (Perfil → Editar avatar): monte seu bichinho escolhendo corpo, cabeça, olhos, boca, desenho, bochechas e três cores, vendo cada opção em miniatura; botão Sortear. Peças raras (Coroa, Quatro olhos, Barbatana) são liberadas ao subir de liga.
- Terceira trilha **Bibliotecas do Python**: 17 unidades, uma por biblioteca, com 6 lições cada (uma por funcionalidade) e Prova de fogo própria. Começa com "Usando bibliotecas" (import, pip, módulos e pacotes). Biblioteca padrão: `math`, `random`, `statistics`, `datetime`, `decimal`/`fractions`, `collections`, `itertools`, `functools`, `re`, `json`, `csv`, `os`/`pathlib`. Externas: NumPy, pandas, Matplotlib e Requests (sem exercícios de código, porque o app não instala pacotes dentro dos exercícios). São 102 lições e 408 exercícios, em `tools/bibliotecas/` (formato em `LEIA.md`), conferidos por `tools/validar_bibliotecas.py` e montados por `tools/gerar_bibliotecas.py`. Na aba Código, `import numpy`/`pandas` baixa o pacote automaticamente quando há internet.
- **Mapa roguelite** (tela Aprender): cada unidade é uma **zona** com um mapa de nós hexagonais, no estilo dos mapas de Slay the Spire. O personagem da pessoa (o avatar dela, com moldura) fica no nó atual e ela escolhe por qual caminho ligado seguir. Tipos de nó: **Batalha** (uma lição), **Elite** (a mesma lição no modo difícil: cada erro custa 2 vidas, mas rende o triplo de moedas, +50% de XP e uma relíquia), **Fogueira** (descansar +2 vidas, treinar a Revisão ou fazer o exercício especial de Leitura/Digitação de código), **Mistério** (pergaminho com desafio do Pipo, mercador de relíquias ou baú suspeito) e **Tesouro** (moedas e relíquia). Todo caminho passa por todas as lições da zona, na ordem, e sempre há uma fogueira antes do chefe. O gerador (`src/lib/mapa.ts`) usa uma semente por perfil e expedição: o mapa é fixo durante a expedição e muda em "Nova expedição". Quem já tinha progresso começa com o personagem depois das lições feitas. Seletor de zonas na lateral, legenda do mapa e painel com as relíquias e a recompensa da zona.
- **Relíquias** (no máximo 3 por expedição): Pato de borracha (o 1º erro de cada lição não custa vida), Café do programador (+5 XP por batalha), Teclado mecânico (+10 de dano no chefe), Escudo try/except (bloqueia o 1º ataque do chefe) e Lupa de depuração (+5 s por bug no chefe).
- **Chefe da zona** (antiga Prova de fogo da unidade): um bug-monstro por zona (Aranha do SyntaxError, Besouro do IndentationError, Centopeia do Loop Infinito...) com barra de vida. Cada linha com bug que a pessoa acha tira vida do chefe (mais rápido e mais acertos seguidos = mais dano); errar ou deixar o tempo acabar faz o chefe atacar (3 vidas por luta). Vencer libera a próxima zona e dá 50 moedas na primeira vitória. São 31 bancos de bugs, um por unidade das trilhas (`tools/provas_unidades.txt`).
- **Prova de fogo livre** (no fim da tela Aprender): cada código tem um erro e você precisa tocar na linha errada antes do cronômetro zerar. Três níveis (Faísca 20s, Chama 15s, Inferno 10s), 10 bugs por prova, 3 chamas, combo que multiplica os pontos, recorde por nível e XP no fim. Depois de cada resposta aparece o erro real do Python, a explicação e a linha corrigida. Banco de 827 bugs em `src/content/provas.json`, gerado por `tools/gerar_provas.py`, que roda cada código com e sem a correção para garantir que o erro existe e que a correção funciona.
- **Vários perfis no aparelho** ("Quem está estudando?"): até 5 perfis, cada um com progresso, vidas, liga e arquivos da aba Código próprios. Quem já usava o app vira o primeiro perfil sem perder nada. A conta online fica ligada a um perfil; os outros estudam offline.
- **PyPasso Plus**: vidas ilimitadas para todos os perfis do aparelho, R$ 14,90/mês ou R$ 119,90/ano com 7 dias grátis. No celular a compra é pelo Google Play/App Store (RevenueCat); na web, pelo Stripe com cartão ou Pix Automático. Sem chaves configuradas, fica em modo demonstração. Configuração completa em `PAGAMENTOS.md`.
- **Exercícios especiais do Pipo**: Leitura de código (5 trechos da zona para prever a saída) e Digitação de código (copiar 3 trechos, valendo velocidade e precisão), abertos pela Fogueira ou pelo pergaminho do Mistério no mapa. Não gastam vidas e valem até 3 estrelas.
- **Comemoração no fim da lição** de acordo com o desempenho: 0 erros traz o Pipo de óculos escuros ("MR. PERFEITO", "ZERO BUGS"); terminar muito rápido, "SPEEDRUN!" com raio; 1 ou 2 erros, chapéu de festa e confete; muitos erros, faixa na testa e suor ("NA RAÇA"). Cada visual tem frases engraçadas sorteadas (`src/lib/comemoracao.ts`, desenhos em `src/components/pipo-poses.ts`). Também aparece ao passar na Prova de fogo da unidade.
- **Conceitos voando para a Biblioteca**: ao tocar em "Entendi, continuar" num cartão de Novo conceito, o cartão do conceito sai voando da tela para dentro de um livro de capa dura bege, que abre a capa, recebe o conteúdo, fecha, pula com "+1" e vai para o canto. Tocar no livro do canto abre o livro no meio da tela e mostra de novo os conceitos da lição (explicação, exemplo e saída), com setas para passar entre eles. Na Biblioteca, a seção "✨ Novos para você" destaca em dourado, com o selo NOVO, o que você acabou de aprender, até abrir cada um; a aba mostra quantos são. O fim da lição lista os conceitos novos. A ligação entre cartões e entradas é gerada por `tools/gerar_conceitos.py` (`src/content/conceitos.json`).
- **Gamificação**: nível do jogador (barra de XP até o próximo, títulos de "Ovo de Python" a "Lenda do PyPasso" e moedas a cada nível), **moedas** (lições, lições sem erro, revisões, projetos, Provas de fogo e exercícios especiais), **aba Missões** com 3 missões diárias sorteadas por dia, **baú do dia** (abre quando as 3 são resgatadas), **23 conquistas** com progresso, combo de acertos seguidos (🔥 na lição) e avisos animados de nível novo e conquista. Regras e tabelas em `src/lib/gamificacao.ts`.
- **Loja** (toque nas moedas): congelador de sequência (protege um dia sem estudo, até 2 guardados), recarga de vidas, XP em dobro por 15 minutos e 5 molduras para o avatar.
- **Revisão espaçada**: todo exercício errado entra num baralho e volta nos dias seguintes (1, 2, 4, 7 e 15 dias, caixas de Leitner). Acertou, demora mais para voltar; errou, volta amanhã. Atalho "🧠 Revisão" na tela Aprender e na aba Missões; não custa vidas.
- **Projetos guiados** (atalho "🛠️ Projetos" na tela Aprender): 6 programas de verdade construídos passo a passo, cada um liberado por uma lição da trilha: Adivinhe o número, Calculadora, Lista de tarefas, Jogo da forca, Quiz de Python e Aventura RPG de texto (39 passos). Cada passo tem explicação do Pipo, tarefa, editor, testes automáticos, dica e, depois de 2 tentativas, a solução. No fim, "Jogar no editor" abre o programa na aba Código. O conteúdo fica em `tools/projetos/` (formato em `LEIA.md`); `tools/validar_projetos.py` roda cada passo no mesmo Python do app e gera `src/content/projetos.json`.
- **Lembretes diários** (Perfil → Lembretes, só no celular): o Pipo avisa no horário escolhido se você ainda não estudou, citando sua sequência. Usa `expo-notifications` com avisos agendados para os próximos 7 dias, reagendados a cada lição.
- **Teste com usuários**: botão 🚩 "Travei aqui" em cada exercício, registro de erros, tempo e abandonos, e o relatório em Perfil → Teste com usuários. Roteiro, termo de consentimento e o script `tools/relatorio_teste.py` em `TESTE-COM-USUARIOS.md`.
- **Sem emojis prontos**: ícones desenhados de game-icons.net e Phosphor Icons (veja Créditos), escolhidos em `tools/gerar_icones.py`.
- 5 vidas (uma volta a cada 30 min), XP, meta diária de 30 XP, sequência de dias, treino rápido que devolve uma vida.
- Exercícios errados voltam no fim da lição até sair certo.
- **10 ligas de evolução**, cada uma com troféu e título: Noob (Bronze), Vibecoder (Prata), Caçador de Bugs (Ouro), Rei do print() (Safira), Domador de Indentação (Rubi), Mago dos Laços (Esmeralda), Lorde das Funções (Ametista), Arquiteto de Classes (Pérola), Sênior Movido a Café (Obsidiana) e Lenda Pythônica (Diamante). Toda semana, 15 pessoas por liga: os 5 primeiros sobem, os 3 últimos caem. Tela de resultado no fim da semana, medalhas de pódio e estante de troféus no Perfil.
- Funciona offline (a liga vira uma "liga de treino" com a turma do PyPasso). Com o Supabase configurado, ganha login, sincronização entre aparelhos e liga com pessoas de verdade, fechada automaticamente toda segunda às 00:05 (horário de Brasília).
- **Modo escuro**: em Perfil → Aparência, escolha Automático (segue o celular/computador), Claro ou Escuro. A escolha fica salva no aparelho e vale para todos os perfis; a barra de status e o fundo do sistema acompanham o tema.

## Rodar no seu computador

Pré-requisito: Node.js 20 ou mais recente.

```bash
npm install
npx expo start
```

- Tecle `w` para abrir no navegador.
- No celular, instale o app **Expo Go** e leia o QR code que aparece no terminal.

## Ativar contas e liga (Supabase)

1. Crie um projeto gratuito em https://supabase.com.
2. No painel, abra **SQL Editor**, cole o conteúdo de `supabase/schema.sql` e execute.
3. Em **Authentication → Providers → Email**, deixe o login por e-mail ligado. Em **Email Templates → Magic Link**, inclua `{{ .Token }}` no corpo para o e-mail trazer o código de 6 dígitos.
4. Copie `.env.example` para `.env` e preencha a URL e a chave `anon` (em **Project Settings → API**).
5. Reinicie `npx expo start`.

## Ativar o Pipo com IA

O Pipo local (análise e correções automáticas) já funciona sem nada configurado. Para a explicação completa com IA:

1. Crie uma chave em https://console.anthropic.com.
2. Instale a CLI do Supabase e, na pasta do projeto:
   ```bash
   npx supabase login
   npx supabase link --project-ref SEU-PROJETO
   npx supabase secrets set ANTHROPIC_API_KEY=sua-chave
   npx supabase functions deploy pipo-assistente
   ```
3. Pronto: usuários logados veem o botão "Explicar com IA" no painel do Pipo. A chave fica só no servidor.

O modelo padrão é o Claude Haiku 4.5 (rápido e barato). Para trocar: `npx supabase secrets set PIPO_MODEL=outro-modelo`. O prompt fica em `supabase/functions/_shared/pipo-prompt.ts`.

## Publicar

**Google Play:** siga o passo a passo em [PLAYSTORE.md](PLAYSTORE.md). Textos, imagens, política de privacidade e respostas dos formulários estão em `store/`.


- **Web:** `npx expo export --platform web` gera a pasta `dist/`, que pode ir para Vercel, Netlify ou Cloudflare Pages.
- **Android e iPhone:** use o EAS (build na nuvem, sem precisar de Xcode ou Android Studio):
  ```bash
  npx eas-cli@latest login
  npx eas-cli@latest build --platform all
  npx eas-cli@latest submit --platform all
  ```
  Antes, troque `com.seunome.pypasso` em `app.json` pelo identificador da sua conta. É preciso ter conta de desenvolvedor no Google Play (taxa única) e na Apple (anuidade).

## Onde mexer

| O quê | Arquivo |
|---|---|
| Lições e exercícios | `src/content/course.json` |
| Personagens | `src/components/Characters.tsx` |
| Cores e modo escuro (paletas `light`/`dark`, preferência `useAparencia`) | `src/lib/theme.ts` |
| Regras de vidas, XP, sequência, revisão e moedas | `src/lib/store.ts` |
| Níveis, missões, conquistas e Loja | `src/lib/gamificacao.ts` |
| Mapa roguelite (gerador, nós, relíquias, chefes) | `src/lib/mapa.ts`, `src/components/mapa/` |
| Ícones (trocar ou adicionar) | `tools/gerar_icones.py` → `src/components/icones-data.ts` |
| Projetos guiados | `tools/projetos/` → `python3 tools/validar_projetos.py` |
| Lembretes | `src/lib/lembretes.ts` (celular), `src/lib/lembretes-prefs.ts` |
| Teste com usuários | `src/lib/teste.ts`, `TESTE-COM-USUARIOS.md` |
| Execução de Python | `src/lib/python/` |
| Ligas, títulos e troféus | `src/lib/leagues.ts` |
| Biblioteca de funções | `src/content/library.json` (gerado por script; cada exemplo é rodado para obter a saída) |
| Pipo assistente (análise local) | `src/lib/python/assistant-py.ts` |
| Pipo com IA | `src/lib/assistant/`, `supabase/functions/` |
| Telas | `src/app/` |

Formato de um exercício de código em `course.json`:

```json
{ "k": "code", "id": "u6l1e5", "host": "bia",
  "q": "Escreva a função dobro(n).",
  "starter": "def dobro(n):\n    pass\n",
  "tests": "assert dobro(3) == 6, \"dobro(3) deve ser 6\"",
  "e": "Basta return n * 2." }
```

Nos testes, a variável `__stdout__` traz tudo o que o código do aluno imprimiu.

## Próximos passos sugeridos

1. Rodar o teste com 5 a 8 iniciantes (`TESTE-COM-USUARIOS.md`) e corrigir o que mais travou.
2. Missões semanais e eventos de fim de semana (XP em dobro para todos).
3. Amigos: seguir pessoas, ver a sequência delas e mandar um "bora estudar".
4. Mais projetos guiados (agenda de contatos com arquivos, análise de dados com pandas).
5. Notificação de "sua liga está acabando" no domingo à noite.

## Créditos e licenças

- Elenco e avatares dos usuários: estilo **Critters** do [DiceBear](https://www.dicebear.com/styles/critters/), em domínio público ([CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)).
- Biblioteca DiceBear: MIT.
- Ícones do mapa, dos chefes, das relíquias, das missões e da loja: [game-icons.net](https://game-icons.net) (Lorc, Delapouite e outros), [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/). O crédito aparece em Perfil → Elenco.
- Ícones da interface: [Phosphor Icons](https://phosphoricons.com), MIT.
- Os dois conjuntos vêm do npm (`@iconify-json/game-icons`, `@iconify-json/ph`); `tools/gerar_icones.py` copia só os ícones usados para `src/components/icones-data.ts`.
- Python no navegador: [Pyodide](https://pyodide.org) (MPL 2.0), carregado do jsDelivr.
- Mascote Pipo e ícone do app: originais deste projeto.

O PyPasso não usa personagens, nomes ou marcas do Duolingo.
