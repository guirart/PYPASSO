// Edge Function: recebe os eventos do RevenueCat (compras no Google Play e na App Store)
// e atualiza public.assinaturas. No RevenueCat: Integrations > Webhooks, URL
//   https://<projeto>.supabase.co/functions/v1/revenuecat-webhook
// e em "Authorization header" o mesmo valor do segredo REVENUECAT_WEBHOOK_AUTH.
// Implante sem exigir login do Supabase: npx supabase functions deploy revenuecat-webhook --no-verify-jwt
import { linhaDoRevenueCat } from '../_shared/assinatura.ts';
import { admin, env, json } from '../_shared/http.ts';

Deno.serve(async (req) => {
  const esperado = env('REVENUECAT_WEBHOOK_AUTH');
  const veio = req.headers.get('Authorization') ?? '';
  if (veio !== esperado && veio !== `Bearer ${esperado}`) return json({ error: 'não autorizado' }, 401);
  const { event } = await req.json();
  if (!event) return json({ ok: true });
  const db = admin();
  if (event.id) {
    const { error: dup } = await db.from('webhook_eventos').insert({ id: `rc_${event.id}`, origem: 'revenuecat' });
    if (dup) return json({ ok: true, repetido: true });
  }
  const linha = linhaDoRevenueCat(event);
  if (!linha) return json({ ok: true, ignorado: event.type });
  // Não deixa o fim de uma assinatura da loja apagar uma assinatura ativa feita pela web.
  const { data: atual } = await db.from('assinaturas').select('origem, status').eq('user_id', linha.user_id).maybeSingle();
  if (atual && atual.origem !== linha.origem && linha.status === 'expirada' && atual.status !== 'expirada' && atual.status !== 'nenhuma') {
    return json({ ok: true, mantido: atual.origem });
  }
  await db.from('assinaturas').upsert({ ...linha, atualizado_em: new Date().toISOString() });
  return json({ ok: true });
});
