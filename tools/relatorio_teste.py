"""Junta os relatórios do teste com usuários (Perfil → Teste com usuários → Copiar).

Cada arquivo é o texto copiado do app: o resumo legível seguido de uma linha JSON com os dados.
Uso:  python3 tools/relatorio_teste.py testes/*.txt
"""
import json, os, sys
from collections import Counter, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
CONTEUDO = os.path.join(AQUI, "..", "src", "content")

# Índice dos exercícios (todas as trilhas) para mostrar a pergunta e a explicação.
EX = {}
for arq in ("course.json", "builtins.json", "bibliotecas.json"):
    for u in json.load(open(os.path.join(CONTEUDO, arq), encoding="utf8"))["units"]:
        for l in u["lessons"]:
            for e in l["exercises"]:
                EX[e["id"]] = (u["title"], l["title"], e)

def dados(caminho):
    for linha in reversed(open(caminho, encoding="utf8").read().splitlines()):
        linha = linha.strip()
        if linha.startswith("{") and linha.endswith("}"):
            return json.loads(linha)
    raise SystemExit(f"{caminho}: não achei a linha de dados (JSON). Copie o relatório inteiro do app.")

if len(sys.argv) < 2:
    raise SystemExit(__doc__)

erros, tent, pessoas_erraram = Counter(), Counter(), defaultdict(set)
abandonos, feitas = Counter(), Counter()
relatos = []
for caminho in sys.argv[1:]:
    d = dados(caminho)
    quem = os.path.splitext(os.path.basename(caminho))[0]
    for ex_id, s in d.get("ex", {}).items():
        erros[ex_id] += s["erros"]; tent[ex_id] += s["tent"]
        if s["erros"]:
            pessoas_erraram[ex_id].add(quem)
    for lic, s in d.get("licoes", {}).items():
        abandonos[lic] += s["abandonou"]; feitas[lic] += s["fez"]
    relatos += [(quem, r) for r in d.get("relatos", [])]

n = len(sys.argv) - 1
print(f"=== {n} pessoa(s) ===\n")
print("Exercícios mais difíceis (ordenados por quantas pessoas erraram, depois por erros):")
ordem = sorted(erros, key=lambda i: (-len(pessoas_erraram[i]), -erros[i]))
for ex_id in [i for i in ordem if erros[i]][:20]:
    unidade, licao, e = EX.get(ex_id, ("?", "?", {}))
    print(f"\n- {ex_id}  [{unidade} › {licao}]  {len(pessoas_erraram[ex_id])}/{n} pessoa(s), {erros[ex_id]} erro(s) em {tent[ex_id]} tentativa(s)")
    if e:
        print(f"  Pergunta: {e.get('q', '')}")
        if e.get("c"):
            print("  Código:   " + e["c"].replace("\n", "\n            "))
        print(f"  Explicação: {e.get('e', '')}")

print("\nLições abandonadas no meio:")
for lic, a in abandonos.most_common():
    if a:
        print(f"- {lic}: {a} abandono(s), {feitas[lic]} conclusão(ões)")

print("\nRelatos do botão Travei aqui:")
for quem, r in relatos:
    print(f"- {quem} · {r['tipo']} · {r.get('exId') or r.get('licao') or ''}: {r.get('texto', '')}")
