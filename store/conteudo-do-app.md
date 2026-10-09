# Respostas para "Conteúdo do app" (Play Console → Política → Conteúdo do app)

Estas respostas descrevem o PyPasso como ele está no código deste projeto. Se você mudar o app (anúncios, analytics, novos dados), revise.

## Política de privacidade
Cole a URL pública de `store/politica-de-privacidade.html` depois de preencher os campos entre colchetes e hospedar a página (veja PLAYSTORE.md).

## Anúncios
O app contém anúncios? **Não.**

## Acesso ao app
Escolha **"Todas ou algumas funcionalidades estão restritas"** e informe:

- Instruções: "O app funciona sem login. Para testar a sincronização, a liga e o Pipo com IA, toque em Perfil → Entrar ou criar conta → Já tenho senha, e use as credenciais abaixo."
- Usuário: [E-MAIL DA CONTA DE DEMONSTRAÇÃO]
- Senha: [SENHA DA CONTA DE DEMONSTRAÇÃO]

Crie essa conta no painel do Supabase (Authentication → Users → Add user, com e-mail e senha). Use um e-mail que você controla e uma senha só para isso.

## Classificação de conteúdo (questionário IARC)
- Categoria: **Referência, notícias ou educação**
- Violência, sexo, linguagem imprópria, drogas, jogos de azar: **Não** em todas.
- Os usuários podem interagir ou trocar conteúdo? **Não há chat nem mensagens.** Se perguntado se o app compartilha informações do usuário com outros usuários: **Sim** (nome de exibição e avatar aparecem na liga).
- Conteúdo gerado por IA: **Sim** (explicações do Pipo com IA, apenas quando o usuário pede).
- Compras digitais: **Não.**

## Público-alvo
- Faixas etárias: **13 a 15, 16 a 17, 18 ou mais**. Não marque faixas abaixo de 13 anos: isso colocaria o app no programa "Feito para famílias", com exigências extras (inclusive sobre IA).
- O app pode atrair crianças sem querer? **Não** (visual amigável, mas o conteúdo é programação para iniciantes a partir de 13 anos).

## Segurança dos dados (Data safety)

Perguntas gerais:
- O app coleta ou compartilha algum dos tipos de dados obrigatórios? **Sim.**
- Todos os dados são criptografados em trânsito? **Sim.**
- Você oferece uma forma de os usuários solicitarem a exclusão dos dados? **Sim** (no app: Perfil → Excluir minha conta; na web: URL da política com `#excluir-conta`).
- Link de exclusão de conta: `[URL DA POLÍTICA]#excluir-conta`

Tipos de dados coletados (nenhum é "compartilhado" no sentido da Google, porque Supabase e o provedor de IA tratam os dados em seu nome):

| Categoria → tipo | Coletado | Opcional? | Processado de forma temporária? | Finalidades |
|---|---|---|---|---|
| Informações pessoais → Endereço de e-mail | Sim | Sim (login é opcional) | Não | Gerenciamento da conta |
| Informações pessoais → Nome (nome de exibição) | Sim | Sim | Não | Funcionalidade do app, gerenciamento da conta |
| Atividade no app → Interações com o app (progresso, XP, sequência) | Sim | Sim (só com conta) | Não | Funcionalidade do app |
| Atividade no app → Outro conteúdo gerado pelo usuário (código enviado ao Pipo com IA, motivo das denúncias) | Sim | Sim | Sim para o código (não é guardado) | Funcionalidade do app; denúncias: segurança e conformidade |

Não coletados: localização, contatos, fotos e vídeos, áudio, arquivos, calendário, informações financeiras, saúde, mensagens, histórico de navegação, IDs de dispositivo ou de publicidade, registros de falhas e diagnósticos.

## IA generativa
Se o Console perguntar sobre recursos de IA generativa: o app gera texto (explicações e sugestões de código) com IA quando o usuário pede, e oferece denúncia de conteúdo dentro do app (botão "Denunciar esta resposta" no painel do Pipo). As denúncias ficam na tabela `ai_reports` do Supabase; revise-as periodicamente.

## Outros
- App de governo, finanças, saúde, notícias, VPN: **Não.**
- Permissões sensíveis: nenhuma. O app só usa internet e vibração.
