// Edge Function do Supabase: o Pipo com IA.
// O app manda o código; a função monta o prompt e chama a API do Claude com a
// chave guardada no servidor (nunca no celular).
//
// Implantação:
//   npx supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
//   npx supabase functions deploy pipo-assistente
// Opcional: PIPO_MODEL (padrão claude-haiku-4-5-20251001).
import { buildPipoPrompt, type PipoPromptInput } from '../_shared/pipo-prompt.ts';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: cors });
  if (req.method !== 'POST') return json({ error: 'Use POST.' }, 405);
  // A verificação do JWT (usuário logado) é feita pelo Supabase antes de chegar aqui.
  let body: PipoPromptInput;
  try {
    body = await req.json();
  } catch {
    return json({ error: 'Corpo inválido.' }, 400);
  }
  if (!body?.files || typeof body.entry !== 'string' || typeof body.files[body.entry] !== 'string') {
    return json({ error: 'Envie files e entry.' }, 400);
  }
  const total = Object.values(body.files).reduce((n, c) => n + String(c).length, 0);
  if (total > 30000) return json({ error: 'Código grande demais para revisar de uma vez.' }, 413);

  const key = Deno.env.get('ANTHROPIC_API_KEY');
  if (!key) return json({ error: 'ANTHROPIC_API_KEY não configurada.' }, 500);

  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({
      model: Deno.env.get('PIPO_MODEL') ?? 'claude-haiku-4-5-20251001',
      max_tokens: 4000,
      messages: [{ role: 'user', content: buildPipoPrompt(body) }],
    }),
  });
  if (!r.ok) return json({ error: `A IA respondeu ${r.status}.` }, 502);
  const data = await r.json();
  const text: string = (data.content ?? []).map((c: { text?: string }) => c.text ?? '').join('');
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  try {
    return json({ review: JSON.parse(text.slice(start, end + 1)) });
  } catch {
    return json({ error: 'A IA não devolveu JSON válido.', raw: text.slice(0, 2000) }, 502);
  }
});
