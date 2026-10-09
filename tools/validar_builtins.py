"""Confere um arquivo de lições de built-ins (tools/builtins_licoes/gNN_*.py).

Uso:  python3 tools/validar_builtins.py tools/builtins_licoes/g01_primeiros.py
Mostra cada problema encontrado; termina com OK quando está tudo certo.
"""
import importlib.util, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from bt_helpers import montar_licao, ler_bugs, conferir_bug  # noqa: E402

# Grupos na ordem da trilha. Cada função vira uma unidade de 6 lições:
# a lição 1 já existe (gerar_builtins.py); os arquivos de grupo trazem as lições 2 a 6.
GRUPOS = {
    "g01": ["print", "input", "len", "type", "help", "id"],
    "g02": ["int", "float", "str", "bool", "complex", "repr"],
    "g03": ["abs", "round", "pow", "divmod", "sum", "min", "max"],
    "g04": ["list", "tuple", "dict", "set", "frozenset", "range"],
    "g05": ["sorted", "reversed", "enumerate", "zip", "map", "filter"],
    "g06": ["all", "any", "callable", "isinstance", "issubclass", "hasattr"],
    "g07": ["ord", "chr", "bin", "oct", "hex", "ascii", "format"],
    "g08": ["iter", "next", "slice", "aiter", "anext"],
    "g09": ["bytes", "bytearray", "memoryview", "hash"],
    "g10": ["object", "getattr", "setattr", "delattr", "vars", "dir"],
    "g11": ["property", "staticmethod", "classmethod", "super"],
    "g12": ["eval", "exec", "compile", "globals", "locals", "__import__", "breakpoint", "open"],
}
uid = lambda nome: f"fn_{nome}"

# Unidades de base, antes das funções: ensinam o que a trilha usa (strings, números,
# coleções, if/for, def, erros, arquivos, classes). Arquivos base1.py, base2.py, base3.py,
# com LICOES = {"base1": [6 lições]} e bugs @base1.
BASE = {
    "base1": ("Valores e textos", "funções, variáveis, strings, números, True, False e None"),
    "base2": ("Coleções e repetição", "listas, tuplas, dicionários, conjuntos, if, while e for"),
    "base3": ("Funções, erros e classes", "def, return, lambda, try, import, with e class"),
}

def carregar(caminho):
    spec = importlib.util.spec_from_file_location(os.path.basename(caminho)[:-3], caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def validar(caminho):
    """Devolve (unidades, bugs, problemas) de um arquivo de grupo."""
    g = os.path.basename(caminho)[:3]
    mod = carregar(caminho)
    problemas, unidades, bugs = [], {}, []
    base = os.path.basename(caminho).startswith("base")
    esperadas = [os.path.basename(caminho)[:-3]] if base else GRUPOS[g]
    n_licoes, inicio = (6, 0) if base else (5, 1)
    _uid = (lambda n: n) if base else uid
    for nome in esperadas:
        licoes = mod.LICOES.get(nome)
        if not licoes:
            problemas.append((nome, "faltam as lições")); continue
        if len(licoes) != n_licoes:
            problemas.append((nome, f"precisa de {n_licoes} lições, tem {len(licoes)}"))
        prontas = []
        for i, L_ in enumerate(licoes):
            lid = f"{_uid(nome)}_l{i + inicio}"
            licao, p = montar_licao(lid, L_["titulo"], L_, semente=i)
            problemas += p
            prontas.append(licao)
        n_code = sum(1 for l in prontas for e in l["exercises"] if e["k"] == "code")
        if n_code < 2:
            problemas.append((nome, f"precisa de pelo menos 2 exercícios CODE (tem {n_code})"))
        if prontas and not any(e["k"] == "code" for e in prontas[-1]["exercises"]):
            problemas.append((nome, "a lição 6 (desafio) precisa de um exercício CODE"))
        unidades[nome] = prontas
    extras = set(mod.LICOES) - set(esperadas)
    if extras: problemas.append(("arquivo", "funções que não são deste grupo", sorted(extras)))
    conta = {}
    for b in ler_bugs(mod.BUGS):
        if b["u"] not in {_uid(n) for n in esperadas}:
            problemas.append(("bug", f"unidade desconhecida @{b['u']}")); continue
        reg, p = conferir_bug(b)
        if p:
            problemas.append((b["u"], "bug", p, b["codigo"][:80])); continue
        bugs.append(reg); conta[b["u"]] = conta.get(b["u"], 0) + 1
    for nome in esperadas:
        if conta.get(_uid(nome), 0) < 5:
            problemas.append((_uid(nome), f"precisa de 5+ bugs, tem {conta.get(_uid(nome), 0)}"))
    return unidades, bugs, problemas

if __name__ == "__main__":
    for caminho in sys.argv[1:]:
        unidades, bugs, problemas = validar(caminho)
        for p in problemas:
            print("PROBLEMA:", *p)
        n_ex = sum(1 for ls in unidades.values() for l in ls for e in l["exercises"] if e["k"] != "learn")
        print(("OK" if not problemas else f"{len(problemas)} PROBLEMA(S)"), "|", os.path.basename(caminho), "|",
              len(unidades), "funções,", sum(len(v) for v in unidades.values()), "lições,", n_ex, "exercícios,", len(bugs), "bugs")
