// Edge Function: exclui a conta do usuário logado e todos os dados ligados a ela
// (perfil, progresso, XP e denúncias são apagados em cascata pelo banco).
// Exigência da Google Play: o usuário precisa poder excluir a conta pelo app.
//
// Implantação: npx supabase functions deploy excluir-conta
import { createClient } from 'npm:@supabase/supabase-js@2';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Use POST.' }, 405);
  const url = Deno.env.get('SUPABASE_URL')!;
  const auth = req.headers.get('Authorization') ?? '';
  // Descobre quem está pedindo, usando o token do próprio usuário
  const asUser = createClient(url, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
  const { data, error } = await asUser.auth.getUser();
  if (error || !data.user) return json({ error: 'Entre na sua conta para excluí-la.' }, 401);
  // Apaga com a chave de serviço (que só existe no servidor)
  const admin = createClient(url, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const { error: delError } = await admin.auth.admin.deleteUser(data.user.id);
  if (delError) return json({ error: 'Não foi possível excluir agora. Tente de novo mais tarde.' }, 500);
  return json({ ok: true });
});
