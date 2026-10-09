# Teste com pessoas de verdade

Antes de lançar, coloque de 5 a 8 iniciantes para usar o PyPasso e observe onde travam. Com 5 pessoas
você já encontra a maior parte dos problemas de uso. Este roteiro leva uns 40 minutos por pessoa.

## O que o app já faz por você

- **Anota onde a pessoa erra**: cada resposta guarda o exercício, se acertou e quanto tempo levou.
- **Anota onde ela desiste**: sair de uma lição no meio conta como abandono.
- **Botão 🚩 "Travei aqui"** no topo de cada exercício: a pessoa escolhe o que aconteceu (não entendi,
  a resposta certa está errada, o app travou, ficou chato, outro) e pode escrever. Não gasta vidas.
- **Perfil → 🧪 Teste com usuários**: mostra os exercícios com mais erros, as lições abandonadas e os
  relatos. O botão "Copiar / compartilhar relatório" copia tudo (texto + dados) para você colar num
  e-mail ou mensagem.
- **Com o Supabase configurado e a opção "Participar do teste" ligada** (Perfil → Teste com usuários),
  cada lição terminada ou abandonada vai para a tabela `teste_licoes` e cada relato para `teste_relatos` (o SQL está no fim de `supabase/schema.sql`). Sem nome nem e-mail:
  só um código aleatório do aparelho (ex.: `t-k3j9xa`).

## Quem chamar

- Pessoas que **nunca programaram** (é o público principal). Idealmente de idades e celulares variados.
- Evite amigos programadores: eles não travam onde o iniciante trava.
- Se for testar com menores de idade, peça a autorização do responsável (veja o termo abaixo).

## Antes da sessão

1. Instale o app num celular de teste (ou use o link da versão web) e **zere os dados**
   (Perfil → Zerar progresso; e Perfil → Teste com usuários → Apagar dados do teste).
2. Leia o termo de consentimento com a pessoa e peça para ela assinar ou concordar por escrito.
   Se for usar o Supabase, ligue "Participar do teste" no aparelho só depois do aceite.
3. Peça para ela **pensar em voz alta** ("estou procurando onde clica para…", "não sei o que é isso…").
4. Você só observa e anota. Não ajude, a não ser que ela fique parada por mais de 2 minutos.

## Tarefas (na ordem)

| # | Tarefa que você fala | O que observar |
|---|---|---|
| 1 | "Abra o app e comece a aprender Python." | Ela entende a trilha? Acha o primeiro nó? |
| 2 | "Faça as duas primeiras lições." | Onde erra? Lê os cartões de Novo conceito ou pula? |
| 3 | "Agora encontre o que você aprendeu de `print`." | Acha a Biblioteca? Entende o selo NOVO? |
| 4 | "Escreva um programa que pergunta seu nome e diz olá." | Acha a aba Código? Entende o `input` interativo? |
| 5 | "Veja quais missões você tem hoje e pegue uma recompensa." | Acha a aba Missões? Entende moedas e o baú? |
| 6 | "Gaste suas moedas em algo." | Entende a Loja e o congelador de sequência? |
| 7 | "Faça uma Prova de fogo." | O cronômetro assusta? Ela entende que é para tocar na linha? |
| 8 | "Ative um lembrete para amanhã." (só no celular) | Acha em Perfil → Lembretes? |

Se a pessoa já fez a trilha até a unidade 6, inclua: "Comece o projeto Adivinhe o número."

## Perguntas no fim (5 minutos)

1. De 0 a 10, quanto você recomendaria o PyPasso para um amigo que quer aprender a programar? Por quê?
2. Qual foi a parte mais confusa?
3. Teve algum momento em que você quis desistir? Quando?
4. O que você achou das moedas, missões e conquistas? Motivam ou atrapalham?
5. Você pagaria R$ 14,90/mês pelo Plus (vidas ilimitadas)? O que faria você pagar?

## Depois da sessão

1. No celular da pessoa: Perfil → 🧪 Teste com usuários → **Copiar / compartilhar relatório**.
   Salve o que foi copiado num arquivo `.txt` por pessoa (ex.: `testes/ana.txt`).
2. Junte todos com o script:

   ```bash
   python3 tools/relatorio_teste.py testes/*.txt
   ```

   Ele soma os erros de todas as pessoas e lista os 20 exercícios mais difíceis, as lições mais
   abandonadas e todos os relatos, com o texto da pergunta e da explicação para você revisar.
3. Corrija primeiro o que **mais de uma pessoa** travou. Um erro isolado pode ser distração.
4. Para corrigir o conteúdo: lições em `src/content/course.json`, built-ins em `tools/builtins_licoes/`,
   bibliotecas em `tools/bibliotecas/`, projetos em `tools/projetos/` (rode os validadores depois).

## Termo de consentimento (modelo)

> **Teste do aplicativo PyPasso**
>
> Você está sendo convidado(a) a testar o aplicativo PyPasso, que ensina programação em Python.
> O teste dura cerca de 40 minutos. Vamos observar você usando o app e anotar suas falas e
> dificuldades. O aplicativo registra, sem seu nome, quais exercícios você errou, quanto tempo levou
> e o que você relatar no botão "Travei aqui".
>
> **Para que servem os dados:** apenas para melhorar o aplicativo. Eles não serão vendidos nem
> usados para publicidade, e os resultados serão apresentados sem identificar você.
>
> **Seus direitos:** a participação é voluntária. Você pode parar a qualquer momento, sem precisar
> explicar, e pedir que seus dados sejam apagados pelo contato abaixo.
>
> **Gravação:** ( ) autorizo ( ) não autorizo a gravação de áudio/tela durante o teste.
>
> Responsável pelo teste: ______________________  Contato: ______________________
>
> Nome do(a) participante: ______________________  Data: ___/___/______
>
> Assinatura: ______________________
>
> *Se o participante tiver menos de 18 anos:* eu, ______________________, responsável legal,
> autorizo a participação. Assinatura: ______________________

Este modelo é um ponto de partida. Revise o texto à luz da LGPD (Lei 13.709/2018), em especial
os artigos 7º e 14 se houver crianças ou adolescentes, antes de usar.
