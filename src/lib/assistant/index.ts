import { buildPipoPrompt, type PipoAIReply } from '../../../supabase/functions/_shared/pipo-prompt';
import { analyzeCode, checkSyntax } from '../python/runner';
import { supabase } from '../supabase';
import type { LocalAnalysis, Review, ReviewInput } from './types';

export type { Review, ReviewInput } from './types';

const FAIL_LOCAL: LocalAnalysis = {
  titulo: 'Não consegui analisar agora.', humor: 'think', problemas: [], dicas: [], corrigido: null, mudancas: [],
};

/** Pipo local: sempre disponível, sem internet e sem custo. */
export async function reviewLocal(i: Pick<ReviewInput, 'files' | 'entry' | 'error'>): Promise<Review> {
  const r = (await analyzeCode(i.files, i.entry, i.error)) as LocalAnalysis & { error?: string };
  const ok = r && Array.isArray((r as LocalAnalysis).problemas);
  return { ...(ok ? r : FAIL_LOCAL), fonte: 'local' };
}

// ---------------------------------------------------------------- IA
type SampleFn = { json: <T>(input: string, opts?: { signal?: AbortSignal; modelTier?: string }) => Promise<T> };
type AIProvider = 'artefato' | 'supabase';

let sampleP: Promise<SampleFn | null> | null = null;
function artifactSample(): Promise<SampleFn | null> {
  const c = (globalThis as { claude?: { use?: (n: string) => Promise<unknown> } }).claude;
  if (!c?.use) return Promise.resolve(null);
  sampleP ??= c.use('sample').then((s) => (s as SampleFn) ?? null).catch(() => null);
  return sampleP;
}

/** Qual IA está disponível neste aparelho (ou null). */
export async function aiProvider(): Promise<AIProvider | null> {
  if (await artifactSample()) return 'artefato';
  if (supabase) {
    const { data } = await supabase.auth.getSession();
    if (data.session) return 'supabase';
  }
  return null;
}

export class PipoAIError extends Error {
  constructor(public code: string, message: string) { super(message); }
}

const AI_ERRORS: Record<string, string> = {
  not_granted: 'Você não autorizou o uso da IA nesta página.',
  rate_limited: 'Muitas perguntas seguidas. Espere um pouco e tente de novo.',
  sampling_disabled: 'A IA não está disponível para esta conta.',
  invalid_json: 'A IA respondeu num formato inesperado. Tente de novo.',
  refused: 'A IA não quis responder sobre esse código.',
  session_expired: 'Sua sessão expirou. Entre de novo.',
};

/** Pipo com IA: explicação detalhada e código reescrito. */
export async function reviewAI(i: ReviewInput, signal?: AbortSignal): Promise<Review> {
  const provider = await aiProvider();
  if (!provider) throw new PipoAIError('indisponivel', 'IA indisponível.');
  let reply: PipoAIReply;
  if (provider === 'artefato') {
    const sample = (await artifactSample())!;
    try {
      reply = await sample.json<PipoAIReply>(buildPipoPrompt(i), { signal, modelTier: 'default' });
    } catch (e) {
      const code = (e as { code?: string })?.code ?? 'upstream_error';
      throw new PipoAIError(code, AI_ERRORS[code] ?? 'Não consegui falar com a IA agora. Tente de novo.');
    }
  } else {
    const { data, error } = await supabase!.functions.invoke('pipo-assistente', {
      body: { files: i.files, entry: i.entry, stdin: i.stdin, output: i.output, error: i.error, local: i.local },
    });
    if (error || !data?.review) throw new PipoAIError('upstream_error', data?.error ?? 'Não consegui falar com a IA agora.');
    reply = data.review as PipoAIReply;
  }
  return normalize(reply, i);
}

async function normalize(r: PipoAIReply, i: ReviewInput): Promise<Review> {
  const original = i.files[i.entry] ?? '';
  let corrigido: string | null = typeof r.codigo_melhorado === 'string' ? r.codigo_melhorado.replace(/\s+$/, '') + '\n' : null;
  let aviso: string | undefined;
  if (corrigido && corrigido.trim() === original.trim()) corrigido = null;
  if (corrigido) {
    const check = await checkSyntax(corrigido);
    if (!check.ok) { aviso = `A versão sugerida veio com erro de sintaxe (${check.error}), então não vou aplicá-la.`; corrigido = null; }
  }
  const problemas = (Array.isArray(r.problemas) ? r.problemas : []).map((p) => ({
    linha: typeof p.linha === 'number' ? p.linha : null,
    codigo: typeof p.linha === 'number' ? (original.split('\n')[p.linha - 1] ?? '').trim() : '',
    titulo: String(p.o_que ?? 'Problema'),
    explicacao: String(p.por_que ?? ''),
    como_corrigir: String(p.como_corrigir ?? ''),
  }));
  const dicas = (Array.isArray(r.dicas) ? r.dicas : []).map((d) => ({
    linha: typeof d.linha === 'number' ? d.linha : null,
    titulo: String(d.dica ?? ''),
    explicacao: '',
    antes: d.antes ?? null,
    depois: d.depois ?? null,
  }));
  return {
    fonte: 'ia',
    titulo: String(r.resumo ?? 'Revisei seu código!'),
    humor: i.error ? 'sad' : problemas.length ? 'think' : 'cheer',
    problemas,
    dicas,
    corrigido,
    mudancas: Array.isArray(r.o_que_mudou) ? r.o_que_mudou.map(String) : [],
    aviso,
  };
}
