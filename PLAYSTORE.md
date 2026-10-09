# Como publicar o PyPasso na Google Play

Tudo o que o app precisa já está no projeto. Este guia cobre o que só você pode fazer, porque depende da sua conta, do seu documento e do seu cartão.

Tempo total esperado: cerca de 3 a 4 semanas, quase todo de espera (o teste fechado obrigatório dura 14 dias).

O que já está pronto:
- Build Android de produção configurado (`eas.json`, pacote `com.pypasso.app`, Android 16 / API 36, que é o mínimo exigido hoje).
- Exclusão de conta dentro do app e pela web, exigida pela Google para apps com login.
- Botão de denúncia de respostas da IA, exigido para apps com IA generativa.
- Política de privacidade (LGPD), textos da loja, respostas dos formulários, ícone, gráfico de destaque e 6 capturas de tela, na pasta `store/`.

---

## Antes de tudo: duas decisões que não têm volta

1. **Nome do pacote**: `com.pypasso.app` (em `app.json`). Depois do primeiro envio ele nunca mais muda. Se preferir outro, troque agora.
2. **Tipo de conta de desenvolvedor**:
   - *Pessoal*: mais simples, mas exige o teste fechado com 12 testadores por 14 dias antes de publicar.
   - *Organização*: exige CNPJ e número D-U-N-S, e não tem o teste obrigatório.

## Passo 1 — Criar a conta de desenvolvedor (1 a 3 dias)

1. Acesse https://play.google.com/console e entre com a conta Google que será dona do app.
2. Pague a taxa única de US$ 25.
3. Faça a verificação de identidade (documento oficial e cartão no seu nome).
4. Instale o app **Google Play Console** num celular Android e verifique o aparelho por ele (exigência para contas pessoais novas).

## Passo 2 — Ligar o servidor (Supabase), 30 minutos

Siga a seção "Ativar contas e liga" do README e depois:

```bash
npx supabase login
npx supabase link --project-ref SEU-PROJETO
npx supabase secrets set ANTHROPIC_API_KEY=sua-chave      # Pipo com IA
npx supabase functions deploy pipo-assistente
npx supabase functions deploy excluir-conta
```

- Rode de novo o `supabase/schema.sql` no SQL Editor (ele agora cria a tabela de denúncias).
- Crie a **conta de demonstração** para o revisor: Authentication → Users → Add user (e-mail + senha).
- Preencha o `.env` (copie de `.env.example`).

Notificações: o app pede permissão para os lembretes diários só quando a pessoa liga em Perfil → Lembretes (avisos locais, nada sai do aparelho). Teste com usuários: só quando a pessoa liga "Participar do teste" e o Supabase está configurado, as tabelas `teste_licoes` e `teste_relatos` recebem dados de uso anônimos (exercícios errados, tempo, relatos). No formulário de Segurança dos dados, declare "Atividade no app: interações no app" para análise e melhoria, não compartilhada, sem identificar a pessoa.

Sem o Supabase o app também funciona, só que sem login, liga e IA. Nesse caso, no formulário de Segurança dos dados, declare que nenhum dado é coletado e remova da política as partes sobre conta e IA.

## Passo 3 — Publicar a política de privacidade

1. Abra `store/politica-de-privacidade.html` e preencha tudo que está entre colchetes: nome, CPF/CNPJ, e-mail, encarregado, data e região do Supabase.
2. Hospede a página num endereço público, por exemplo:
   - **GitHub Pages**: crie um repositório público, envie o arquivo e ative Pages; ou
   - **Netlify Drop** (https://app.netlify.com/drop): arraste a pasta com o arquivo.
3. Coloque o endereço no `.env`, em `EXPO_PUBLIC_PRIVACY_URL`. O link aparece no Perfil do app.

## Passo 4 — Gerar o arquivo do app (.aab), 20 a 40 minutos

O build roda na nuvem da Expo (o plano gratuito basta). Não precisa de Android Studio.

```bash
npm install
npx eas-cli@latest login          # crie uma conta grátis em expo.dev se não tiver
npx eas-cli@latest init           # liga o projeto à sua conta Expo
npx eas-cli@latest build --platform android --profile production
```

Na primeira vez, aceite quando o EAS oferecer **gerar uma chave de assinatura** (keystore). Ela fica guardada na sua conta Expo. Ao terminar, baixe o arquivo `.aab` pelo link mostrado.

Dica: antes, gere uma versão de teste para instalar direto no seu celular:
`npx eas-cli@latest build --platform android --profile preview` (gera um `.apk`).

## Passo 5 — Criar o app no Play Console

1. **Criar app** → nome "PyPasso: Aprenda Python", idioma Português (Brasil), tipo App, Gratuito. Aceite as declarações.
2. **Ficha principal da loja**: copie os textos de `store/ficha-da-loja.md` e envie as imagens de `store/imagens/`.
3. **Conteúdo do app**: responda cada item com `store/conteudo-do-app.md` (política, anúncios, acesso ao app com a conta de demonstração, classificação, público-alvo 13+, segurança dos dados, exclusão de conta).

## Passo 6 — Teste fechado (14 dias, obrigatório para conta pessoal)

1. Testar → **Teste fechado** → criar faixa → **Criar versão** → envie o `.aab` (o primeiro envio precisa ser manual, pelo navegador).
2. Testadores: crie um **Grupo do Google** e adicione pelo menos **12 pessoas** (amigos, colegas, alunos) que usem Android.
3. Envie a elas o **link de participação** do teste. Cada uma precisa aceitar, instalar pela Play Store e **continuar no teste por 14 dias seguidos**. Quem sai antes não conta, então chame umas 15 pessoas por segurança.
4. Peça que elas usem o app de verdade e mandem opiniões. A Google pergunta sobre isso no próximo passo.

## Passo 7 — Pedir acesso à produção

Depois dos 14 dias, o Console libera **Solicitar acesso à produção**. Responda com sinceridade como foi o teste, o que você melhorou e quem é o público. A análise leva até cerca de 7 dias.

## Passo 8 — Publicar

1. Produção → Criar versão → escolha a mesma versão do teste (ou envie uma nova).
2. Recomendo **lançamento gradual** (por exemplo 20% dos usuários) e acompanhar avaliações e erros antes de ir a 100%.
3. A primeira revisão da versão pode levar de algumas horas a alguns dias.

## Atualizações futuras

```bash
npx eas-cli@latest build --platform android --profile production   # o número da versão sobe sozinho
npx eas-cli@latest submit --platform android --profile production  # envia para o teste fechado
```

Para o `submit` automático, crie uma **conta de serviço** do Google Cloud com acesso ao Play Console, baixe a chave JSON e salve como `google-play-service-account.json` na raiz do projeto (o arquivo já está no `.gitignore`).

## Assinatura Plus

Antes de ligar o Plus pago, siga o `PAGAMENTOS.md`: crie a assinatura `plus` no Play Console
(planos `mensal` e `anual`, com 7 dias grátis), ligue o RevenueCat e, no formulário de Segurança
dos dados, declare "Histórico de compras". Sem as chaves, o app vai para a loja com o Plus em
modo demonstração. Nesse caso, esconda a tela do Plus ou deixe o aviso, porque a Play não aceita
um botão de compra que não cobra.

## Motivos comuns de rejeição (já tratados)

| Exigência | Onde está no projeto |
|---|---|
| Exclusão de conta no app | Perfil → Excluir minha conta (`supabase/functions/excluir-conta`) |
| Exclusão de conta pela web | `politica-de-privacidade.html#excluir-conta` |
| Denúncia de conteúdo de IA | Painel do Pipo → Denunciar esta resposta (tabela `ai_reports`) |
| Revisor conseguir entrar | Login com senha + conta de demonstração |
| API alvo atual | Expo SDK 57 → targetSdk 36 |
| Política de privacidade | `store/politica-de-privacidade.html` |
