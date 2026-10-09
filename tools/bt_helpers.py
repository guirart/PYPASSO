"""Ferramentas comuns para escrever e conferir lições e bugs da trilha de built-ins.

Usado por gerar_builtins.py, gerar_provas.py e validar_builtins.py.
Nada aqui é escrito à mão no JSON final: saídas de exercícios são calculadas rodando
o código, soluções de exercícios de código são testadas, e cada bug é rodado com e
sem a correção.
"""
import builtins as _b, contextlib, io, os, random, re, signal, sys, tempfile

# ------------------------------------------------------------------ helpers de autoria
def OUT(code, errados, e, entrada=""):
    """Qual é a saída? (múltipla escolha). errados = 3 alternativas erradas."""
    return {"k": "out", "c": code, "_wrong": errados, "e": e, "_in": entrada}
def TYPE(code, e, entrada=""):
    """Digite a saída (resposta de UMA linha)."""
    return {"k": "type", "c": code, "e": e, "_in": entrada}
def MC(q, certo, errados, e):
    """Pergunta de múltipla escolha. errados = 2 ou 3 alternativas."""
    return {"k": "mc", "q": q, "o": [certo, *errados], "e": e}
def FILL(q, code, certo, errados, e):
    """Completar a lacuna ___ do código (uma lacuna)."""
    return {"k": "fill", "q": q, "c": code, "b": [certo, *errados], "a": [certo], "e": e}
def ORDER(q, linhas, e):
    """Ordenar linhas: escreva as linhas na ORDEM CERTA (o app embaralha)."""
    return {"k": "order", "q": q, "l": linhas, "e": e}
def CODE(q, starter, solucao, tests, e):
    """Escrever código. tests: asserts com mensagem; __stdout__ tem o que foi impresso."""
    return {"k": "code", "q": q, "starter": starter, "_sol": solucao, "tests": tests, "e": e}
def L(titulo, explica, exemplo, itens, entrada=""):
    """Uma lição: cartão de conceito (explica + exemplo) e depois os exercícios."""
    return dict(titulo=titulo, explica=explica, exemplo=exemplo, itens=itens, entrada=entrada)

# ------------------------------------------------------------------ execução
class Tempo(Exception):
    pass
def _alarme(*_):
    raise Tempo()
signal.signal(signal.SIGALRM, _alarme)

def run(src, entrada="", segundos=8):
    """Roda src num diretório limpo; devolve a saída. input() lê de `entrada`, sem eco."""
    os.chdir(tempfile.mkdtemp())
    buf = io.StringIO()
    respostas = iter(entrada.splitlines())
    def fake_input(prompt=""):
        return next(respostas)
    old_in, old_hook = _b.input, sys.breakpointhook
    _b.input = fake_input
    random.seed(0)
    signal.alarm(segundos)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, "<ex>", "exec"), {"__name__": "__main__"})
    finally:
        signal.alarm(0)
        _b.input = old_in; sys.breakpointhook = old_hook
    return buf.getvalue().rstrip("\n")

def run_err(src, entrada=""):
    try:
        return run(src, entrada), None
    except BaseException as ex:  # noqa: BLE001 (Tempo, SystemExit…)
        if isinstance(ex, KeyboardInterrupt):
            raise
        return None, ex

def _passa(src, tests):
    try:
        out = run(src)
        g = {"__name__": "__main__"}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, "<sol>", "exec"), g)
        g["__stdout__"] = out
        exec(tests, g)
        return True, None
    except BaseException as e:  # noqa: BLE001
        return False, e

HOSTS = ["ana", "caio", "bia", "teo"]

def montar_licao(lid, titulo_card, L_, semente=0):
    """Transforma uma lição de autoria em JSON do app. Devolve (licao, problemas)."""
    problemas = []
    saida, ex = run_err(L_["exemplo"], L_.get("entrada", ""))
    if ex:
        problemas.append((lid, "exemplo do cartão falha", f"{type(ex).__name__}: {ex}")); saida = ""
    ent = L_.get("entrada", "")
    exs = [{"k": "learn", "id": f"{lid}c0", "host": "pipo", "q": titulo_card,
            "body": L_["explica"], "c": L_["exemplo"],
            "out": saida + (f"\n(respostas digitadas: {', '.join(ent.splitlines())})" if ent else ""), "e": ""}]
    graded = 0
    for ei, it in enumerate(L_["itens"]):
        it = dict(it)
        k = it["k"]
        q = "Qual é a saída?" if k == "out" else "Digite a saída." if k == "type" else it.get("q")
        if k in ("out", "type"):
            o, ex = run_err(it["c"], it.pop("_in"))
            if ex:
                problemas.append((lid, f"exercício {ei} dá erro", it["c"], f"{type(ex).__name__}: {ex}")); continue
            if k == "out":
                errados = it.pop("_wrong")
                if o in errados: problemas.append((lid, f"exercício {ei}: um distrator é igual à resposta", o))
                it["o"] = [o, *errados]
                if len(set(it["o"])) != len(it["o"]) or len(it["o"]) < 3: problemas.append((lid, f"exercício {ei}: opções repetidas ou poucas", it["o"]))
            else:
                if "\n" in o or o != o.strip() or not o: problemas.append((lid, f"exercício {ei}: resposta de digitar precisa ser UMA linha sem espaços nas pontas", repr(o)))
                it["a"] = [o]
        elif k == "fill":
            if it["c"].count("___") != 1: problemas.append((lid, f"exercício {ei}: lacuna precisa aparecer uma vez", it["c"]))
            src = it["c"].replace("___", it["a"][0])
            o, ex = run_err(src)
            if ex and not isinstance(ex, (NameError,)): problemas.append((lid, f"exercício {ei}: código completado não roda", src, f"{type(ex).__name__}: {ex}"))
            if len(set(it["b"])) != len(it["b"]): problemas.append((lid, f"exercício {ei}: opções repetidas", it["b"]))
        elif k == "order":
            o, ex = run_err("\n".join(it["l"]))
            if ex: problemas.append((lid, f"exercício {ei}: ordem certa não roda", f"{type(ex).__name__}: {ex}"))
            if len(it["l"]) < 3: problemas.append((lid, f"exercício {ei}: ordenar precisa de 3+ linhas"))
            if len(set(it["l"])) != len(it["l"]): problemas.append((lid, f"exercício {ei}: linhas repetidas confundem a correção"))
        elif k == "code":
            sol = it.pop("_sol")
            ok, err = _passa(sol, it["tests"])
            if not ok: problemas.append((lid, f"exercício {ei}: a solução não passa nos testes", f"{type(err).__name__}: {err}"))
            ok2, _ = _passa(it["starter"], it["tests"])
            if ok2: problemas.append((lid, f"exercício {ei}: o código inicial já passa nos testes"))
        elif k == "mc":
            if len(set(it["o"])) != len(it["o"]) or len(it["o"]) < 3: problemas.append((lid, f"exercício {ei}: opções repetidas ou poucas", it["o"]))
        else:
            problemas.append((lid, f"exercício {ei}: tipo desconhecido {k}"))
        if not it.get("e"): problemas.append((lid, f"exercício {ei}: falta a explicação e"))
        it.update(q=q, id=f"{lid}e{ei}", host=HOSTS[(semente + ei) % 4])
        exs.append(it); graded += 1
    if graded < 3: problemas.append((lid, "a lição precisa de pelo menos 3 exercícios"))
    return {"id": lid, "title": L_["titulo"], "exercises": exs}, problemas

# ------------------------------------------------------------------ bugs (formato @unidade linha)
def ler_bugs(texto):
    """Lê blocos  @unidade linha / código / >>> correção / !! explicação."""
    out, bloco = [], None
    def fecha():
        if not bloco: return
        linhas = bloco["codigo"]
        while linhas and not linhas[-1].strip(): linhas.pop()
        while linhas and not linhas[0].strip(): linhas.pop(0)
        n = bloco["linha"]
        orig = linhas[n - 1] if 0 < n <= len(linhas) else ""
        fix = bloco["fix"] or ""
        if fix and not fix[0].isspace():
            fix = orig[: len(orig) - len(orig.lstrip())] + fix
        out.append(dict(u=bloco["u"], codigo="\n".join(linhas), linha=n, correcao=fix, explica=bloco["explica"]))
    for raw in texto.split("\n"):
        cab = re.fullmatch(r"@([A-Za-z_]\w*) (\d+)\s*", raw)
        if cab:  # "@unidade N" (uma linha só com "@cache" é código: decorador)
            fecha()
            u, n = cab.group(1), cab.group(2)
            bloco = {"u": u, "linha": int(n), "codigo": [], "fix": None, "explica": ""}
        elif bloco is not None:
            if raw.startswith(">>> "): bloco["fix"] = raw[4:]
            elif raw.startswith("!! "): bloco["explica"] = raw[3:]
            elif bloco["fix"] is None: bloco["codigo"].append(raw)
    fecha()
    return out

def conferir_bug(b):
    """Devolve (registro, problema). registro tem tipo e mensagem real do Python."""
    linhas = b["codigo"].split("\n")
    n = b["linha"]
    if not 1 <= n <= len(linhas): return None, "linha fora do código"
    if linhas[n - 1] == b["correcao"]: return None, "correção igual à linha"
    if not b["explica"]: return None, "falta a explicação (!!)"
    certo = linhas[:]; certo[n - 1] = b["correcao"]
    out_ok, err_ok = run_err("\n".join(certo))
    if err_ok: return None, f"o código corrigido falha: {type(err_ok).__name__}: {err_ok}"
    m = re.search(r"# esperado: (.*)$", b["codigo"], re.M)
    if m and out_ok.split("\n")[-1] != m.group(1).strip():
        return None, f"'# esperado' não bate: a correção imprime {out_ok.splitlines()[-1] if out_ok else '(nada)'!r}"
    out_bug, err_bug = run_err(b["codigo"])
    if isinstance(err_bug, Tempo):
        tipo, msg = "Laço infinito", "O programa nunca termina."
    elif err_bug:
        tipo = type(err_bug).__name__
        msg = f"{tipo}: {err_bug.msg if isinstance(err_bug, SyntaxError) else err_bug}"
    elif out_bug != out_ok:
        tipo, msg = "Resultado errado", f"Saiu: {out_bug.splitlines()[-1] if out_bug else '(nada)'}"
    else:
        return None, "o código com bug funciona igual ao corrigido"
    return {"linhas": linhas, "linha": n - 1, "correcao": b["correcao"], "explica": b["explica"], "tipo": tipo, "msg": msg, "u": b["u"]}, None
