"""Confere as unidades da trilha "Bibliotecas" (tools/bibliotecas/NN_slug.py).

Uso:  python3 tools/validar_bibliotecas.py tools/bibliotecas/02_math.py [...]
      python3 tools/validar_bibliotecas.py            (confere todas)
Mostra cada problema; termina com OK quando está tudo certo.
"""
import glob, importlib.util, os, sys

os.environ.setdefault("MPLBACKEND", "Agg")  # Matplotlib sem tela
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from bt_helpers import montar_licao, ler_bugs, conferir_bug  # noqa: E402

PASTA = os.path.join(AQUI, "bibliotecas")

def carregar(caminho):
    spec = importlib.util.spec_from_file_location("lib_" + os.path.basename(caminho)[:-3], caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validar(caminho):
    """Devolve (unidade_json, bugs, problemas)."""
    mod = carregar(caminho)
    problemas, bugs = [], []
    U = getattr(mod, "UNIDADE", None)
    if not U or not all(k in U for k in ("id", "titulo", "descricao", "externa")):
        return None, [], [("arquivo", "falta UNIDADE = dict(id=..., titulo=..., descricao=..., externa=...)")]
    uid, externa = U["id"], U["externa"]
    licoes = getattr(mod, "LICOES", [])
    if len(licoes) != 6:
        problemas.append((uid, f"precisa de 6 lições, tem {len(licoes)}"))
    prontas = []
    for i, L_ in enumerate(licoes):
        licao, p = montar_licao(f"{uid}_l{i}", L_["titulo"], L_, semente=i)
        problemas += p
        prontas.append(licao)
    n_code = sum(1 for l in prontas for e in l["exercises"] if e["k"] == "code")
    if externa and n_code:
        problemas.append((uid, "biblioteca externa não pode ter CODE (o app não instala pacotes nos exercícios)"))
    if not externa:
        if n_code < 2: problemas.append((uid, f"precisa de pelo menos 2 exercícios CODE (tem {n_code})"))
        if prontas and not any(e["k"] == "code" for e in prontas[-1]["exercises"]):
            problemas.append((uid, "a lição 6 (desafio) precisa de um exercício CODE"))
    conta = 0
    for b in ler_bugs(getattr(mod, "BUGS", "")):
        if b["u"] != uid:
            problemas.append(("bug", f"use @{uid} (veio @{b['u']})")); continue
        reg, p = conferir_bug(b)
        if p:
            problemas.append((uid, "bug", p, b["codigo"][:80])); continue
        bugs.append(reg); conta += 1
    if conta < 5:
        problemas.append((uid, f"precisa de 5+ bugs válidos, tem {conta}"))
    unidade = {"id": uid, "title": U["titulo"], "description": U["descricao"], "group": U.get("grupo"), "lessons": prontas}
    return unidade, bugs, problemas

def arquivos():
    return sorted(glob.glob(os.path.join(PASTA, "[0-9][0-9]_*.py")))

if __name__ == "__main__":
    for caminho in [os.path.abspath(c) for c in sys.argv[1:]] or arquivos():
        unidade, bugs, problemas = validar(caminho)
        for p in problemas:
            print("PROBLEMA:", *p)
        n_ex = sum(1 for l in (unidade or {}).get("lessons", []) for e in l["exercises"] if e["k"] != "learn")
        print(("OK" if not problemas else f"{len(problemas)} PROBLEMA(S)"), "|", os.path.basename(caminho), "|",
              len((unidade or {}).get("lessons", [])), "lições,", n_ex, "exercícios,", len(bugs), "bugs")
