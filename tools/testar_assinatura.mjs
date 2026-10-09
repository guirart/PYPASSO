// Testes da lógica da assinatura Plus (supabase/functions/_shared/assinatura.ts).
// Rode:  node --experimental-strip-types tools/testar_assinatura.mjs
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { linhaDoRevenueCat, linhaDoStripe, paramsCheckout, plusAtivo, usuarioDoEvento, verificarStripe } from '../supabase/functions/_shared/assinatura.ts';

let n = 0;
const ok = async (nome, f) => { await f(); n++; console.log('✓', nome); };
const U = '6f1c2a10-1b2c-4d5e-8f90-123456789abc';

await ok('Stripe: assinatura válida passa', async () => {
  const corpo = '{"id":"evt_1"}', t = Math.floor(Date.now() / 1000);
  const sig = createHmac('sha256', 'whsec_x').update(`${t}.${corpo}`).digest('hex');
  assert.equal(await verificarStripe(corpo, `t=${t},v1=${sig}`, 'whsec_x'), true);
  assert.equal(await verificarStripe(corpo, `t=${t},v0=abc,v1=${sig}`, 'whsec_x'), true);
});
await ok('Stripe: corpo alterado, segredo errado, evento velho e cabeçalho vazio falham', async () => {
  const corpo = '{"id":"evt_1"}', t = Math.floor(Date.now() / 1000);
  const sig = createHmac('sha256', 'whsec_x').update(`${t}.${corpo}`).digest('hex');
  assert.equal(await verificarStripe(corpo + ' ', `t=${t},v1=${sig}`, 'whsec_x'), false);
  assert.equal(await verificarStripe(corpo, `t=${t},v1=${sig}`, 'whsec_y'), false);
  const velho = t - 3600, sigV = createHmac('sha256', 'whsec_x').update(`${velho}.${corpo}`).digest('hex');
  assert.equal(await verificarStripe(corpo, `t=${velho},v1=${sigV}`, 'whsec_x'), false);
  assert.equal(await verificarStripe(corpo, null, 'whsec_x'), false);
});
await ok('Stripe: período no item (API nova), teste, cancelada e expirada', () => {
  const base = { id: 'sub_1', customer: 'cus_1', items: { data: [{ current_period_end: 1893456000, price: { recurring: { interval: 'year' } } }] } };
  const l = linhaDoStripe({ ...base, status: 'trialing' }, U);
  assert.deepEqual([l.status, l.ciclo, l.expira_em, l.stripe_subscription_id], ['teste', 'anual', '2030-01-01T00:00:00.000Z', 'sub_1']);
  assert.equal(linhaDoStripe({ ...base, status: 'active', cancel_at_period_end: true }, U).status, 'cancelada');
  assert.equal(linhaDoStripe({ ...base, status: 'canceled' }, U).status, 'expirada');
  assert.equal(linhaDoStripe({ ...base, status: 'incomplete' }, U), null);
  assert.equal(linhaDoStripe({ id: 's', customer: 'c', status: 'active', current_period_end: 1893456000 }, U).expira_em, '2030-01-01T00:00:00.000Z');
});
await ok('Checkout: Pix Automático no ciclo certo e teste grátis só na primeira vez', () => {
  const p = paramsCheckout({ ciclo: 'anual', priceId: 'price_a', customer: 'cus_1', userId: U, site: 'https://x.app', teste: true });
  assert.equal(p.get('mode'), 'subscription');
  assert.equal(p.get('payment_method_options[pix][mandate_options][payment_schedule]'), 'yearly');
  assert.equal(p.get('payment_method_options[pix][mandate_options][amount]'), '17985');
  assert.equal(p.get('subscription_data[trial_period_days]'), '7');
  assert.equal(p.get('success_url'), 'https://x.app/plus?status=ok');
  const q = paramsCheckout({ ciclo: 'mensal', priceId: 'price_m', customer: 'cus_1', userId: U, site: 'https://x.app', teste: false });
  assert.equal(q.get('payment_method_options[pix][mandate_options][payment_schedule]'), 'monthly');
  assert.equal(q.has('subscription_data[trial_period_days]'), false);
});
await ok('RevenueCat: eventos viram status certos; compra sem conta é ignorada', () => {
  const e = { app_user_id: U, store: 'PLAY_STORE', product_id: 'plus_anual:anual', expiration_at_ms: 1893456000000, entitlement_ids: ['plus'] };
  assert.equal(linhaDoRevenueCat({ ...e, type: 'INITIAL_PURCHASE', period_type: 'TRIAL' }).status, 'teste');
  const r = linhaDoRevenueCat({ ...e, type: 'RENEWAL', period_type: 'NORMAL' });
  assert.deepEqual([r.status, r.origem, r.ciclo], ['ativa', 'play_store', 'anual']);
  assert.equal(linhaDoRevenueCat({ ...e, type: 'CANCELLATION' }).status, 'cancelada');
  assert.equal(linhaDoRevenueCat({ ...e, type: 'BILLING_ISSUE' }).status, 'atrasada');
  assert.equal(linhaDoRevenueCat({ ...e, type: 'EXPIRATION' }).status, 'expirada');
  assert.equal(linhaDoRevenueCat({ ...e, type: 'TEST' }), null);
  assert.equal(linhaDoRevenueCat({ ...e, app_user_id: '$RCAnonymousID:abc', type: 'RENEWAL' }), null);
  assert.equal(usuarioDoEvento({ app_user_id: '$RCAnonymousID:abc', aliases: ['$RCAnonymousID:abc', U] }), U);
  assert.equal(linhaDoRevenueCat({ ...e, type: 'RENEWAL', entitlement_ids: ['outra'] }), null);
  assert.equal(linhaDoRevenueCat({ ...e, store: 'APP_STORE', type: 'RENEWAL' }).origem, 'app_store');
});
await ok('plusAtivo: vale até expirar, inclusive cancelada e atrasada', () => {
  const fut = new Date(Date.now() + 864e5).toISOString(), pas = new Date(Date.now() - 1000).toISOString();
  assert.equal(plusAtivo({ status: 'cancelada', expira_em: fut }), true);
  assert.equal(plusAtivo({ status: 'atrasada', expira_em: fut }), true);
  assert.equal(plusAtivo({ status: 'ativa', expira_em: pas }), false);
  assert.equal(plusAtivo({ status: 'expirada', expira_em: fut }), false);
  assert.equal(plusAtivo({ status: 'nenhuma', expira_em: null }), false);
  assert.equal(plusAtivo(null), false);
});
console.log(`\n${n} grupos de testes passaram`);
