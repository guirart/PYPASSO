"""Confere os Projetos guiados (tools/projetos/*.py) com o MESMO Python que o app usa.

Para cada passo: a solução passa nos testes, o código inicial não passa, o código inicial
continua do passo anterior, e o programa final roda (main) com respostas de exemplo.
Gera src/content/projetos.json.   Rode:  python3 tools/validar_projetos.py
"""
import glob, importlib.util, json, os, re, sys, signal

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
harness_ts = open(os.path.join(RAIZ, "src/lib/python/harness.ts"), encoding="utf8").read()
PY = re.search(r"PY_HARNESS = String\.raw`(.*?)`;", harness_ts, re.S).group(1)
G = {}
exec(PY, G)
import tempfile
G["_PROJ"] = tempfile.mkdtemp()
run = G["__pypasso_run"]

class Tempo(Exception): pass
def _alarme(*_): raise Tempo()
signal.signal(signal.SIGALRM, _alarme)

def roda(code, tests):
    signal.alarm(8)
    try:
        return json.loads(run(code, tests, "projeto"))
    except Tempo:
        return {"ok": False, "error": "laço infinito (passou de 8s)"}
    finally:
        signal.alarm(0)

def sem_todo(s):
    return "\n".join(l for l in s.strip().splitlines() if not l.strip().startswith("# TODO")).strip()

problemas, saida = [], []
for arq in sorted(glob.glob(os.path.join(AQUI, "projetos", "[0-9]*.py"))):
    spec = importlib.util.spec_from_file_location("p", arq); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    P = m.PROJETO; nome = os.path.basename(arq)
    for c in ("id", "titulo", "emoji", "resumo", "requer", "passos"):
        if c not in P: problemas.append((nome, f"falta {c}"))
    if not 5 <= len(P["passos"]) <= 7: problemas.append((nome, f"{len(P['passos'])} passos (use 5 a 7)"))
    anterior = None
    passos = []
    for i, p in enumerate(P["passos"]):
        tag = f"{nome} passo {i+1}"
        for c in ("titulo", "explica", "tarefa", "starter", "solucao", "tests", "dica"):
            if not p.get(c): problemas.append((tag, f"falta {c}"))
        r = roda(p["solucao"], p["tests"])
        if not r["ok"]: problemas.append((tag, "a solução não passa", r.get("error")))
        r2 = roda(p["starter"], p["tests"])
        if r2["ok"]: problemas.append((tag, "o código inicial já passa nos testes"))
        if anterior is not None:
            a = [l.rstrip() for l in sem_todo(anterior).splitlines() if l.strip()]
            b = [l.rstrip() for l in sem_todo(p["starter"]).splitlines() if l.strip()]
            faltam = [l for l in a if l not in b]
            if len(faltam) > 2: problemas.append((tag, "o starter não continua da solução anterior; faltam:", faltam[:4]))
        if "input(" in p["solucao"]:
            for ln in p["solucao"].splitlines():
                if "input(" in ln and not ln.startswith((" ", "\t")):
                    problemas.append((tag, "input() fora de função", ln))
        anterior = p["solucao"]
        passos.append({k: p[k] for k in ("titulo", "explica", "tarefa", "starter", "tests", "dica")} | {"solucao": p["solucao"]})
    final = P["passos"][-1]["solucao"]
    if 'if __name__ == "__main__"' not in final: problemas.append((nome, "o código final precisa do bloco if __name__ == \"__main__\": main()"))
    if P.get("demo_entrada") is not None:
        r = json.loads(G["__pypasso_project"](json.dumps({"main.py": final}), "main.py", P["demo_entrada"], 0))
        if r.get("error"): problemas.append((nome, "o jogo final dá erro com demo_entrada", r["error"]))
        else: print(f"--- {P['id']} (demo) ---\n" + r["stdout"][-600:])
    saida.append({"id": P["id"], "titulo": P["titulo"], "emoji": P["emoji"], "resumo": P["resumo"], "requer": P["requer"],
                  "entrada": P.get("demo_entrada", ""), "passos": passos})

for p in problemas: print("PROBLEMA:", *p)
print(f"{len(saida)} projetos, {sum(len(p['passos']) for p in saida)} passos, {len(problemas)} problemas")
if problemas: sys.exit(1)
json.dump({"projetos": saida}, open(os.path.join(RAIZ, "src/content/projetos.json"), "w"), ensure_ascii=False, indent=1)
print("OK: src/content/projetos.json")
