"""Liga cada cartão de "Novo conceito" às entradas da Biblioteca que ele ensina.

Percorre as duas trilhas na ordem. Cada entrada da Biblioteca é "adicionada" no primeiro
cartão que a ensina (pelo título do cartão; se o título não citar nada, pelo código do
exemplo). Saída: src/content/conceitos.json = { id_do_cartão: [ids da Biblioteca] }.
Rode:  python3 tools/gerar_conceitos.py
"""
import json, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
CONTEUDO = os.path.join(AQUI, "..", "src", "content")
LIB = json.load(open(os.path.join(CONTEUDO, "library.json")))["funcoes"]

# Entradas que não são uma função comum: palavras do título e padrões no código.
ESPECIAIS = {
    "for": (r"\bfor\b|\blaço", r"^\s*for\b"),
    "while": (r"\bwhile\b", r"^\s*while\b"),
    "with": (r"\bwith\b", r"^\s*with\b"),
    "if / elif / else": (r"\bif\b|\belif\b|decis", r"^\s*if\b"),
    "def / return": (r"\bdef\b|\breturn\b|criando funç", r"^\s*def\b"),
    "lambda": (r"\blambda\b", r"\blambda\b"),
    "class": (r"\bclass(e|es)?\b", r"^\s*class\b"),
    "None": (r"\bNone\b", None),
    "pass / break / continue": (r"\bbreak\b|\bcontinue\b|\bpass\b", r"^\s*(break|continue|pass)\b"),
    "global": (r"\bglobal\b", r"^\s*global\b"),
    "try / except": (r"\btry\b|\bexcept\b|exce[çc]", r"^\s*try\b"),
    "raise": (r"\braise\b", r"^\s*raise\b"),
    "assert": (r"\bassert\b", r"^\s*assert\b"),
    "import": (r"\bimport\b|módulo", r"^\s*(import|from)\b"),
    "in": (r"\bin\b para|`in`|\bin\b responde|operador in", None),
    "and / or / not": (r"\band\b|\bor\b|\bnot\b|lógic", None),
    "+ - * / // % **": (r"\bcontas\b|operador|aritm|divis[aã]o", None),
    'f"…{valor}…"': (r"f-string", r"\bf\""),
    "texto[início:fim:passo]": (r"\bfatias?\b|\bíndices?\b|\bposi[çc][õo]es\b", None),
    "[x for x in …]": (r"compreens", None),
    "a, b = …": (r"desempacot", None),
    "dict() e {}": (r"\bdicion[aá]rios?\b", None),
    "tuple() e ( )": (r"\btuplas?\b", None),
    "list()": (r"\blistas?\b", r"(?<![.\w])list\("),
    "set()": (r"\bconjuntos?\b", r"(?<![.\w])set\("),
    "| & - ^": (r"uni[aã]o|interse", None),
    "Erros comuns": (r"mensage(m|ns) de erro|lendo (os )?erros", None),
    "math.sqrt()": (None, r"math\.sqrt\("),
    "math.floor() / math.ceil()": (None, r"math\.(floor|ceil)\("),
    "math.pi": (None, r"math\.pi\b"),
    "random.randint()": (None, r"random\.randint\("),
    "random.choice()": (None, r"random\.choice\("),
    "random.shuffle()": (None, r"random\.shuffle\("),
    "datetime.date": (None, r"datetime"),
    ".read() / .readlines()": (r"\bread\b|ler arquivo|lendo", r"\.read(lines)?\("),
}

def padroes(e):
    n = e["nome"]
    if n in ESPECIAIS:
        t, c = ESPECIAIS[n]
        return (re.compile(t, re.I) if t else None), (re.compile(c, re.M) if c else None)
    m = re.fullmatch(r"\.(\w+)\(\)", n)
    if m:  # método: ".strip()"
        w = re.escape(m.group(1))
        return re.compile(rf"\.?\b{w}\(\)|\.{w}\b"), re.compile(rf"\.{w}\(")
    m = re.fullmatch(r"(\w+)\(\)", n)
    if m:  # função: "print()"
        w = re.escape(m.group(1))
        return re.compile(rf"(?<![.\w]){w}\(\)|^{w}\b"), re.compile(rf"(?<![.\w]){w}\(")
    return None, None

PADROES = [(e["id"], *padroes(e)) for e in LIB]

def conceitos_do_cartao(card, vistos):
    titulo, codigo = card.get("q", ""), card.get("c", "")
    pelo_titulo = [i for i, t, _ in PADROES if t and t.search(titulo)]
    pelo_codigo = [i for i, _, c in PADROES if c and c.search(codigo)]
    novos = [i for i in dict.fromkeys(pelo_titulo + pelo_codigo) if i not in vistos]
    # sem nada no título, só o 1º conceito novo do código (para não "adicionar" coisas de passagem)
    return novos[:3] if any(i in novos for i in pelo_titulo) else novos[:1]

saida, total = {}, 0
for arquivo in ("course.json", "builtins.json", "bibliotecas.json"):
    curso = json.load(open(os.path.join(CONTEUDO, arquivo)))
    vistos = set()
    for u in curso["units"]:
        for l in u["lessons"]:
            for e in l["exercises"]:
                if e["k"] != "learn":
                    continue
                novos = conceitos_do_cartao(e, vistos)
                if novos:
                    saida[e["id"]] = novos
                    vistos.update(novos)
                    total += len(novos)
    print(f"{arquivo}: {len(vistos)} entradas da Biblioteca ligadas a cartões")
json.dump(saida, open(os.path.join(CONTEUDO, "conceitos.json"), "w"), ensure_ascii=False, indent=0)
print(f"OK: {len(saida)} cartões adicionam {total} conceitos")
