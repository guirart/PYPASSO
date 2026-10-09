"""Confere que a trilha de built-ins só usa um conceito depois de ensiná-lo.

Cada conceito tem a lição das unidades de base que o ensina. Se um exercício (ou cartão)
usar o conceito antes dessa lição, aparece um PROBLEMA.
Uso:  python3 tools/conferir_ordem.py
"""
import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TRILHA = os.path.join(AQUI, "..", "src", "content", "builtins.json")

# conceito: (lição que ensina, regex no CÓDIGO, regex no TEXTO)
CONCEITOS = {
    "variável":      ("base1_l1", r"^\s*[A-Za-z_]\w*\s*=[^=]", r"\bvari[aá]ve(l|is)\b"),
    "string":        ("base1_l2", r"", r"\bstrings?\b|\bstr\b|f-string"),
    "f-string":      ("base1_l2", r"\bf\"|\bf'", r"f-string"),
    "índice/fatia":  ("base1_l3", r"\w[\]\)\"']?\[-?\d*:?-?\d*\]", r"\bfatias?\b|\bíndices?\b"),
    "método":        ("base1_l3", r"\w\.[a-z_]+\(", r"\bm[eé]todos?\b"),
    "operadores":    ("base1_l4", r"//|\*\*| % ", r""),
    "int/float":     ("base1_l4", r"", r"\bint\b|\bfloat\b"),
    "bool/None":     ("base1_l5", r"\bTrue\b|\bFalse\b|\bNone\b|==|!=", r"\bbool\b|\bTrue\b|\bFalse\b|\bNone\b"),
    "lista":         ("base2_l0", r"\[[^\]\[]*,[^\]\[]*\]|\.append\(", r"\blistas?\b"),
    "tupla":         ("base2_l1", r"", r"\btuplas?\b"),
    "conjunto":      ("base2_l1", r"\bset\(|\.add\(", r"\bconjuntos?\b"),
    "dicionário":    ("base2_l2", r"\{\s*[\"'\w]+\s*:", r"\bdicion[aá]rios?\b"),
    "if":            ("base2_l3", r"^\s*(if|elif|else)\b", r""),
    "laços":         ("base2_l4", r"^\s*(for|while)\b", r""),
    "compreensão":   ("base2_l5", r"\[[^\]\n]+ for [^\]\n]+ in [^\]\n]+\]", r"compreens[aã]o"),
    "def":           ("base3_l0", r"^\s*def\b|\breturn\b", r""),
    "lambda":        ("base3_l1", r"\blambda\b", r""),
    "try/except":    ("base3_l2", r"^\s*(try|except)\b|\braise\b", r"\bexce[çc][aã]o\b|\bexce[çc][oõ]es\b"),
    "import":        ("base3_l3", r"^\s*(import|from)\b", r""),
    "arquivos":      ("base3_l4", r"\bopen\(|^\s*with\b", r""),
    "classe":        ("base3_l5", r"^\s*class\b", r"\bclasses?\b"),
}

# Prévias aceitas: a lição de strings usa `in`, que responde True/False, e o próprio
# cartão explica na hora ("True (sim) ou False (não)"). bool é ensinado de vez na base1_l5.
PERMITIDO = {("base1_l3", "bool/None")}

def textos(e):
    code = "\n".join(str(e.get(k, "")) for k in ("c", "starter"))
    if e["k"] == "order": code += "\n" + "\n".join(e["l"])
    if e["k"] in ("fill",): code += "\n" + " ".join(e["b"])
    if e["k"] == "mc": code += "\n" + "\n".join(e["o"])
    txt = " ".join(str(e.get(k, "")) for k in ("q", "body", "e"))
    if e["k"] in ("mc",): txt += " " + " ".join(e["o"])
    return code, txt

def conferir():
    c = json.load(open(TRILHA))
    ordem, problemas = {}, []
    seq = [l["id"] for u in c["units"] for l in u["lessons"]]
    pos = {lid: i for i, lid in enumerate(seq)}
    for u in c["units"]:
        for l in u["lessons"]:
            i = pos[l["id"]]
            for e in l["exercises"]:
                code, txt = textos(e)
                for nome, (onde, rc, rt) in CONCEITOS.items():
                    if i >= pos[onde] or (l["id"], nome) in PERMITIDO: continue
                    hit = (rc and re.search(rc, code, re.M)) or (rt and re.search(rt, txt, re.I))
                    if hit:
                        problemas.append((l["id"], e["id"], nome, hit.group(0)[:40]))
    return problemas

if __name__ == "__main__":
    ps = conferir()
    for p in ps: print("PROBLEMA:", *p)
    print("OK" if not ps else f"{len(ps)} PROBLEMA(S)")
