import { RUN_TIMEOUT_MS, TIMEOUT_RESULT, workerSrc, type PyOp, type RunResult } from './harness';

let worker: Worker | null = null;
let seq = 0;
let booted = false;
const pending = new Map<number, (r: RunResult) => void>();

function boot() {
  const url = URL.createObjectURL(new Blob([workerSrc()], { type: 'text/javascript' }));
  worker = new Worker(url, { type: 'module' });
  booted = false;
  worker.onmessage = (ev) => {
    const { id, result, ready } = ev.data ?? {};
    if (ready) booted = true;
    if (id != null && pending.has(id)) { pending.get(id)!(result); pending.delete(id); }
  };
}

/** Na web o Python roda num Web Worker do próprio navegador. */
function call(op: PyOp, args: (string | number)[]): Promise<RunResult> {
  if (!worker) boot();
  const id = ++seq;
  return new Promise((resolve) => {
    // O primeiro carregamento baixa ~13 MB; damos mais tempo enquanto o Python não está pronto.
    const timer = setTimeout(() => {
      if (!pending.has(id)) return;
      pending.delete(id);
      worker?.terminate(); worker = null;
      resolve(TIMEOUT_RESULT);
    }, booted ? RUN_TIMEOUT_MS : RUN_TIMEOUT_MS * 8);
    pending.set(id, (r) => { clearTimeout(timer); resolve(r); });
    worker!.postMessage({ id, op, args });
  });
}

export const runPython = (code: string, tests = '', modname = '__main__') => call('test', [code, tests, modname]);
export const runProject = (files: Record<string, string>, entry: string, stdin: string, seed = 0) => call('project', [JSON.stringify(files), entry, stdin, seed]);
export const runRepl = (src: string) => call('repl', [src]);
export const resetRepl = () => call('reset', []);
/** O Pipo analisa o código e o erro; a resposta vem em JSON no campo stdout. */
export const analyzeCode = async (files: Record<string, string>, entry: string, error: string) => {
  const r = await call('analyze', [JSON.stringify(files), entry, error]);
  return r as unknown as import('../assistant/types').LocalAnalysis | RunResult;
};
export const checkSyntax = (code: string) => call('syntax', [code]);

/** Pré-carrega o Pyodide em segundo plano. */
export function warmUpPython() { if (!worker) boot(); }

export function PythonHost() { return null; }
