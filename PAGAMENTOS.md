# PyPasso Plus: como ligar os pagamentos de verdade

O Plus dá **vidas ilimitadas** para todos os perfis do aparelho. Preços: **R$ 14,90/mês** ou
**R$ 119,90/ano** (33% mais barato), com **7 dias grátis** na primeira assinatura.

Enquanto as chaves abaixo não estiverem configuradas, o app fica em **modo demonstração**:
a tela do Plus funciona, mas nada é cobrado (um aviso deixa isso claro).

## Como funciona

| Onde a pessoa assina | Como paga | Quem cobra | Como o app fica sabendo |
|---|---|---|---|
| App Android | Google Play | Google Play Billing, via RevenueCat | SDK do RevenueCat no aparelho + webhook `revenuecat-webhook` |
| App iPhone | App Store | Apple, via RevenueCat | idem |
| Site (versão web) | Cartão ou **Pix Automático** | Stripe Checkout | webhook `stripe-webhook` |

- No Android e no iPhone, as lojas **exigem** o sistema de pagamento delas para liberar recursos
  dentro do app. Usar Stripe ou Mercado Pago lá dentro faz o app ser recusado. Por isso, no
  celular o botão abre a compra da loja, e o Stripe fica só na web.
- Com conta (login), a assinatura fica gravada no servidor (`public.assinaturas`). Quem assinou na
  web tem Plus no celular, e vice-versa. O id do usuário no RevenueCat é o id do Supabase.
- Pix Automático: a pessoa autoriza uma vez no app do banco; o banco avisa 3 dias antes de cada
  cobrança, e ela pode cancelar pelo banco. O teto do mandato é 1,5x o preço, para um reajuste
  futuro não exigir nova autorização.

Arquivos: `src/lib/plus.ts` (regras no app), `src/lib/loja.ts` (lojas, RevenueCat),
`src/lib/loja.web.ts` (Stripe), `src/app/plus.tsx` (tela),
`supabase/functions/{plus-checkout,plus-portal,stripe-webhook,revenuecat-webhook}`,
`supabase/functions/_shared/assinatura.ts` (regras do servidor, testadas em
`tools/testar_assinatura.mjs`).

## 1. Banco de dados (Supabase)

Rode de novo o `supabase/schema.sql` no SQL Editor (ele cria `assinaturas`, `webhook_eventos` e a
função `plus_ativo`). As tabelas só podem ser escritas pelo servidor.

## 2. Stripe (web: cartão e Pix)

1. Crie a conta Stripe **do Brasil** e ative **Pix** em Configurações > Formas de pagamento
   (o Pix Automático para assinaturas aparece ali).
2. Produtos > Criar produto "PyPasso Plus" com dois preços recorrentes em BRL:
   R$ 14,90 mensal e R$ 119,90 anual. Anote os dois `price_...`.
3. Configurações > Portal do cliente: permita cancelar e trocar a forma de pagamento.
4. Desenvolvedores > Webhooks > Adicionar endpoint:
   `https://SEU-PROJETO.supabase.co/functions/v1/stripe-webhook`, com os eventos
   `checkout.session.completed`, `customer.subscription.created`,
   `customer.subscription.updated`, `customer.subscription.deleted`. Anote o `whsec_...`.
5. Segredos e implantação:
   ```bash
   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_... STRIPE_WEBHOOK_SECRET=whsec_... \
     STRIPE_PRICE_MENSAL=price_... STRIPE_PRICE_ANUAL=price_... SITE_URL=https://seu-site
   npx supabase functions deploy plus-checkout
   npx supabase functions deploy plus-portal
   npx supabase functions deploy stripe-webhook --no-verify-jwt
   ```
6. No `.env` do app: `EXPO_PUBLIC_PLUS_WEB=1`.
7. Teste no modo de teste do Stripe (chaves `sk_test_`): no Pix, use o CPF `000.000.000-00` e
   "Simular leitura"; no cartão, `4242 4242 4242 4242`.

## 3. Google Play (Android)

1. Play Console > Monetizar > Produtos > **Assinaturas** > Criar assinatura `plus`.
2. Dois planos básicos: `mensal` (renova a cada mês, R$ 14,90) e `anual` (a cada ano, R$ 119,90).
3. Em cada plano, uma **oferta** de teste sem custo de 7 dias, para "Novos clientes".
4. O app precisa estar numa faixa de teste (o SDK já adiciona a permissão de faturamento).
   Adicione seu e-mail em Configurações > Teste de licença para comprar sem ser cobrado.

## 4. App Store (iPhone), se for publicar lá

App Store Connect > Assinaturas: grupo "PyPasso Plus" com `pypasso.plus.mensal` e
`pypasso.plus.anual`, cada um com oferta introdutória gratuita de 7 dias.

## 5. RevenueCat (une Google Play e App Store)

1. Crie o projeto e adicione os apps: Android (credencial JSON da conta de serviço do Google
   Cloud com acesso ao Play Console) e iOS (chave de compras no app da App Store).
2. Importe os produtos. Crie o **entitlement `plus`** e ligue todos os produtos a ele.
3. **Offering** padrão com os pacotes **Monthly** e **Annual** (o app procura por esses tipos).
4. Project settings > API keys: copie as chaves públicas para o `.env`
   (`EXPO_PUBLIC_RC_ANDROID_KEY`, `EXPO_PUBLIC_RC_IOS_KEY`).
5. Integrations > Webhooks: URL `https://SEU-PROJETO.supabase.co/functions/v1/revenuecat-webhook`
   e um valor secreto em "Authorization header". Depois:
   ```bash
   npx supabase secrets set REVENUECAT_WEBHOOK_AUTH=o-mesmo-valor
   npx supabase functions deploy revenuecat-webhook --no-verify-jwt
   ```

## 6. Testar compras no celular

Compras reais não funcionam no Expo Go (o SDK entra em modo de prévia). Gere um
**development build**: `npx eas-cli@latest build --profile development --platform android`.

## 7. Regras e obrigações

- **Play Store:** mostre o preço e a renovação automática antes da compra (a tela do Plus já
  mostra, usando o preço que vem da loja), e um jeito de cancelar ("Gerenciar assinatura").
  No formulário de **Segurança dos dados**, declare "Histórico de compras" (finalidade:
  funcionalidade do app). Na política de privacidade, cite Google, Apple, Stripe e RevenueCat
  como processadores de pagamento.
- **Direito de arrependimento (CDC, art. 49):** em compras feitas fora de estabelecimento
  comercial, como na web, a pessoa pode desistir em até 7 dias e receber o valor de volta. Pelo
  Stripe, faça o reembolso no painel; nas lojas, o reembolso segue a política do Google/Apple.
- **IOF no Pix:** o Stripe trata o IOF de cada cobrança (o padrão é o cliente pagar).
- Emissão de nota fiscal e tributos dependem do seu enquadramento: confirme com seu contador.
