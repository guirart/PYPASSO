import { PY_ASSISTANT } from './assistant-py';

/**
 * Código compartilhado entre web e celular para rodar Python com Pyodide.
 * O Python roda dentro de um Web Worker para que um laço infinito possa ser
 * interrompido (o worker é encerrado e recriado após o tempo limite).
 */
export const PYODIDE_VERSION = '314.0.7';
const CDN_URL = `https://cdn.jsdelivr.net/npm/pyodide@${PYODIDE_VERSION}/`;
/** Pode ser sobrescrito pela página (window.PYPASSO_PYODIDE_URL) para servir o Pyodide do próprio site. */
export const pyodideUrl = (): string =>
  ((globalThis as { PYPASSO_PYODIDE_URL?: string }).PYPASSO_PYODIDE_URL) || CDN_URL;
export const RUN_TIMEOUT_MS = 6000;

export type RunResult = {
  ok: boolean;
  stdout: string;
  error: string | null;
  /** Aba Código: o programa parou num input() sem resposta. Traz a pergunta (prompt). */
  wait?: string;
};

/** Executa o código do aluno, captura a saída e roda os testes do exercício. */
export const PY_HARNESS = String.raw`
import sys, io, json, traceback

def __pypasso_run(user_code, tests, modname="__main__"):
    # modname="projeto": nos Projetos guiados o arquivo roda como módulo importado,
    # então o bloco  if __name__ == "__main__":  (o jogo em si) não roda nos testes.
    buf = io.StringIO()
    old = sys.stdout
    ns = {"__name__": modname}
    def _input(prompt=""):
        raise RuntimeError("input() não está disponível nos exercícios. Use valores fixos.")
    ns["input"] = _input
    sys.stdout = buf
    try:
        exec(compile(user_code, "seu_codigo.py", "exec"), ns)
    except SyntaxError as e:
        sys.stdout = old
        return json.dumps({"ok": False, "stdout": buf.getvalue(), "error": "".join(traceback.format_exception_only(type(e), e)).rstrip()})
    except Exception as e:
        sys.stdout = old
        frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "seu_codigo.py"]
        tb = ("Traceback (most recent call last):\n" + "".join(traceback.format_list(frames))) if frames else ""
        return json.dumps({"ok": False, "stdout": buf.getvalue(), "error": tb + "".join(traceback.format_exception_only(type(e), e)).rstrip()})
    finally:
        sys.stdout = old
    out = buf.getvalue()
    ns["__stdout__"] = out
    if not tests:
        return json.dumps({"ok": True, "stdout": out, "error": None})
    try:
        exec(tests, ns)
    except AssertionError as e:
        return json.dumps({"ok": False, "stdout": out, "error": str(e) or "Um dos testes falhou."})
    except Exception as e:
        frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == "seu_codigo.py"]
        if frames:  # o erro aconteceu dentro do código do aluno
            tb = "Traceback (most recent call last):\n" + "".join(traceback.format_list(frames))
            return json.dumps({"ok": False, "stdout": out, "error": tb + "".join(traceback.format_exception_only(type(e), e)).rstrip()})
        if isinstance(e, NameError):
            return json.dumps({"ok": False, "stdout": out, "error": f"Faltou definir algo: {e}"})
        return json.dumps({"ok": False, "stdout": out, "error": "".join(traceback.format_exception_only(type(e), e)).strip()})
    return json.dumps({"ok": True, "stdout": out, "error": None})


# ---------- Playground (aba Código) ----------
import builtins, os

_PROJ = "/home/pyodide/projeto"
_repl_ns = {"__name__": "__main__"}
_user_files = set()

def _fmt_error(e):
    """Traceback só com as linhas dos arquivos do aluno, como no terminal."""
    if isinstance(e, SyntaxError):
        return "".join(traceback.format_exception_only(type(e), e)).rstrip()
    frames = [f for f in traceback.extract_tb(e.__traceback__) if os.path.basename(f.filename) in _user_files or f.filename == "<stdin>"]
    out = ""
    if frames:
        out = "Traceback (most recent call last):\n" + "".join(traceback.format_list(frames))
    out += "".join(traceback.format_exception_only(type(e), e)).rstrip()
    return out.replace(_PROJ + "/", "")

def _make_input(buf, lines):
    def _input(prompt=""):
        buf.write(str(prompt))
        try:
            v = next(lines)
        except StopIteration:
            raise EOFError("input() ficou sem resposta. Escreva as respostas na caixa Entrada, uma por linha.")
        buf.write(v + "\n")
        return v
    return _input

class _PedeEntrada(BaseException):
    """input() sem resposta: o programa pausa e o terminal pede a resposta."""
    def __init__(self, prompt):
        self.prompt = prompt

def _make_live_input(buf, lines):
    def _input(prompt=""):
        try:
            v = next(lines)
        except StopIteration:
            raise _PedeEntrada(str(prompt))
        buf.write(str(prompt) + v + "\n")
        return v
    return _input

def __pypasso_project(files_json, entry, stdin, seed=0):
    # Modo interativo (seed > 0): quando acabam as respostas, o programa pausa e devolve
    # a pergunta. Com a resposta, ele roda de novo do começo com as respostas anteriores
    # e a mesma semente do random, então chega no mesmo ponto e continua.
    global _repl_ns, _user_files
    files = json.loads(files_json)
    os.makedirs(_PROJ, exist_ok=True)
    os.chdir(_PROJ)
    if _PROJ not in sys.path:
        sys.path.insert(0, _PROJ)
    _user_files = set(files)
    for name, src in files.items():
        with open(name, "w") as f:
            f.write(src)
        sys.modules.pop(name[:-3], None)
    buf = io.StringIO()
    old_out, old_err, old_in = sys.stdout, sys.stderr, builtins.input
    sys.stdout = sys.stderr = buf
    answers = iter(json.loads(stdin) if seed else [])
    builtins.input = _make_live_input(buf, answers) if seed else _make_input(buf, iter(stdin.splitlines()))
    if seed:
        import random
        random.seed(seed)
    _repl_ns = {"__name__": "__main__", "__file__": entry}
    err = None
    wait = None
    try:
        exec(compile(files[entry], entry, "exec"), _repl_ns)
    except SystemExit:
        pass
    except _PedeEntrada as p:
        wait = p.prompt
    except BaseException as e:
        err = _fmt_error(e)
    finally:
        sys.stdout, sys.stderr, builtins.input = old_out, old_err, old_in
    res = {"ok": err is None, "stdout": buf.getvalue(), "error": err}
    if wait is not None:
        res["wait"] = wait
    return json.dumps(res)

def __pypasso_repl(src):
    buf = io.StringIO()
    old_out, old_err, old_in = sys.stdout, sys.stderr, builtins.input
    sys.stdout = sys.stderr = buf
    builtins.input = _make_input(buf, iter([]))
    err = None
    try:
        try:
            code = compile(src, "<stdin>", "eval")
            is_expr = True
        except SyntaxError:
            code = compile(src, "<stdin>", "exec")
            is_expr = False
        if is_expr:
            r = eval(code, _repl_ns)
            if r is not None:
                print(repr(r))
                _repl_ns["_"] = r
        else:
            exec(code, _repl_ns)
    except SystemExit:
        pass
    except BaseException as e:
        err = _fmt_error(e)
    finally:
        sys.stdout, sys.stderr, builtins.input = old_out, old_err, old_in
    return json.dumps({"ok": err is None, "stdout": buf.getvalue(), "error": err})

def __pypasso_repl_reset():
    global _repl_ns
    _repl_ns = {"__name__": "__main__"}
    return json.dumps({"ok": True, "stdout": "", "error": None})
`;

/** Opcional: biblioteca-padrão em base64 (para hospedagens que não servem .zip). */
const stdlibB64Url = (): string =>
  ((globalThis as { PYPASSO_STDLIB_B64_URL?: string }).PYPASSO_STDLIB_B64_URL) || '';

/** Worker do tipo "module": o Pyodide atual não roda em workers clássicos. */
export const workerSrc = (base = pyodideUrl(), stdlib = stdlibB64Url()) => `
import { loadPyodide } from ${JSON.stringify(base + 'pyodide.mjs')};
const ready = (async () => {
  const opts = { indexURL: ${JSON.stringify(base)} };
  const stdlib = ${JSON.stringify(stdlib)};
  if (stdlib) {
    const b64 = (await (await fetch(stdlib)).text()).trim();
    const bin = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    opts.stdLibURL = URL.createObjectURL(new Blob([bin], { type: 'application/zip' }));
  }
  const py = await loadPyodide(opts);
  py.runPython(${JSON.stringify(PY_HARNESS)});
  py.runPython(${JSON.stringify(PY_ASSISTANT)});
  return py;
})();
const OPS = { test: '__pypasso_run', project: '__pypasso_project', repl: '__pypasso_repl', reset: '__pypasso_repl_reset', analyze: '__pypasso_analyze', syntax: '__pypasso_syntax' };
self.onmessage = async (ev) => {
  const { id, op, args } = ev.data;
  try {
    const py = await ready;
    // Aba Código: se o programa importa numpy, pandas, matplotlib..., baixa o pacote antes.
    if (op === 'project' || op === 'repl') {
      const src = op === 'project' ? Object.values(JSON.parse(args[0])).join(String.fromCharCode(10)) : args[0];
      try { await py.loadPackagesFromImports(src); } catch (e) { /* sem internet: o import vai explicar */ }
    }
    const fn = py.globals.get(OPS[op]);
    const json = fn(...args);
    fn.destroy();
    self.postMessage({ id, result: JSON.parse(json) });
  } catch (e) {
    self.postMessage({ id, result: { ok: false, stdout: '', error: String(e && e.message || e) } });
  }
};
self.postMessage({ boot: true });
ready.then(() => self.postMessage({ ready: true }), (e) => self.postMessage({ fatal: String(e) }));
`;

/** Mensagem enviada ao worker: {id, op, args}. Ele responde {id, result}. */
export type PyOp = 'test' | 'project' | 'repl' | 'reset' | 'analyze' | 'syntax';

export const TIMEOUT_RESULT: RunResult = {
  ok: false,
  stdout: '',
  error: 'O código demorou demais. Verifique se há um laço que nunca termina.',
};
