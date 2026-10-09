// Utilidades das Edge Functions (Deno).
import { createClient } from 'npm:@supabase/supabase-js@2';

export const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
export const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

export const env = (k: string) => {
  const v = Deno.env.get(k);
  if (!v) throw new Error(`Falta a variável ${k} (npx supabase secrets set ${k}=...)`);
  return v;
};

/** Cliente com a chave de serviço: só no servidor. */
export const admin = () => createClient(env('SUPABASE_URL'), env('SUPABASE_SERVICE_ROLE_KEY'));

/** Quem está chamando (pelo token do próprio usuário). */
export async function usuario(req: Request) {
  const c = createClient(env('SUPABASE_URL'), env('SUPABASE_ANON_KEY'), { global: { headers: { Authorization: req.headers.get('Authorization') ?? '' } } });
  const { data } = await c.auth.getUser();
  return data.user;
}

/** Chamada à API do Stripe (form-urlencoded), sem SDK. */
export async function stripe(caminho: string, params?: URLSearchParams, metodo = params ? 'POST' : 'GET') {
  const r = await fetch(`https://api.stripe.com/v1/${caminho}`, {
    method: metodo,
    headers: { Authorization: `Bearer ${env('STRIPE_SECRET_KEY')}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  });
  const dados = await r.json();
  if (!r.ok) throw new Error(dados?.error?.message ?? `Stripe ${r.status}`);
  return dados;
}
