import { useEffect, useRef } from 'react';
import { View } from 'react-native';
import { WebView, type WebViewMessageEvent } from 'react-native-webview';
import { RUN_TIMEOUT_MS, TIMEOUT_RESULT, workerSrc, type PyOp, type RunResult } from './harness';

/**
 * No celular o Python roda numa WebView invisível (montada uma vez no layout raiz).
 * Dentro dela, um Web Worker executa o Pyodide; se travar, a página encerra o
 * worker e cria outro.
 */
const HTML = `<!doctype html><html><head><meta charset="utf-8"></head><body><script>
const SRC = ${JSON.stringify(workerSrc())};
let w = null; let ready = false; const timers = {};
function post(m){ window.ReactNativeWebView.postMessage(JSON.stringify(m)); }
function boot(){
  w = new Worker(URL.createObjectURL(new Blob([SRC], {type:'text/javascript'})), { type: 'module' });
  ready = false;
  w.onmessage = (ev) => { const d = ev.data || {}; if (d.ready) ready = true; if (d.id != null) { clearTimeout(timers[d.id]); post(d); } };
}
window.__run = (id, op, args, timeout) => {
  if (!w) boot();
  timers[id] = setTimeout(() => { w.terminate(); w = null; post({ id, result: ${JSON.stringify(TIMEOUT_RESULT)} }); }, ready ? timeout : timeout * 8);
  w.postMessage({ id, op, args });
};
boot();
</script></body></html>`;

let webview: WebView | null = null;
let seq = 0;
const pending = new Map<number, (r: RunResult) => void>();
const queue: string[] = [];

function call(op: PyOp, args: (string | number)[]): Promise<RunResult> {
  const id = ++seq;
  return new Promise((resolve) => {
    pending.set(id, resolve);
    const js = `window.__run(${id}, ${JSON.stringify(op)}, ${JSON.stringify(args)}, ${RUN_TIMEOUT_MS}); true;`;
    if (webview) webview.injectJavaScript(js);
    else queue.push(js);
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

export function warmUpPython() {}

export function PythonHost() {
  const ref = useRef<WebView>(null);
  useEffect(() => () => { webview = null; }, []);
  const onMessage = (e: WebViewMessageEvent) => {
    try {
      const { id, result } = JSON.parse(e.nativeEvent.data);
      const done = pending.get(id);
      if (done) { pending.delete(id); done(result); }
    } catch {}
  };
  return (
    <View style={{ width: 0, height: 0, position: 'absolute', opacity: 0 }} pointerEvents="none">
      <WebView
        ref={ref}
        originWhitelist={['*']}
        source={{ html: HTML, baseUrl: 'https://localhost/' }}
        javaScriptEnabled
        onMessage={onMessage}
        onLoadEnd={() => {
          webview = ref.current;
          while (queue.length) webview?.injectJavaScript(queue.shift()!);
        }}
      />
    </View>
  );
}
