"""Monta a trilha "Bibliotecas" (src/content/bibliotecas.json) a partir de tools/bibliotecas/NN_slug.py.

Cada arquivo é conferido por validar_bibliotecas.py (roda cada exemplo, resposta, solução e bug).
Rode:  python3 tools/gerar_bibliotecas.py
"""
import json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from validar_bibliotecas import arquivos, validar  # noqa: E402

SAIDA = os.path.join(AQUI, "..", "src", "content", "bibliotecas.json")
unidades, problemas = [], []
for caminho in arquivos():
    u, _bugs, probs = validar(caminho)
    problemas += [(os.path.basename(caminho), *p) for p in probs]
    if u:
        unidades.append(u)
if problemas:
    for p in problemas: print("PROBLEMA:", *p)
    raise SystemExit(1)
json.dump({"units": unidades}, open(SAIDA, "w"), ensure_ascii=False, indent=1)
n_l = sum(len(u["lessons"]) for u in unidades)
n_ex = sum(1 for u in unidades for l in u["lessons"] for e in l["exercises"] if e["k"] != "learn")
print(f"OK: {len(unidades)} unidades, {n_l} lições, {n_ex} exercícios")
