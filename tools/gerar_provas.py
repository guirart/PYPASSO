"""Banco de bugs da "Prova de fogo" do PyPasso.

Cada item é um trecho com UM erro numa linha. O script confere tudo rodando Python:
- o código com bug tem de falhar (erro de sintaxe ou de execução) ou dar um resultado
  diferente do código corrigido;
- o código corrigido (trocando só aquela linha) tem de rodar sem erro;
- se houver um comentário "# esperado: X", a última linha da saída corrigida tem de ser X.
A mensagem de erro real do Python vai junto, para mostrar na correção.
Rode:  python3 tools/gerar_provas.py
"""
import builtins, contextlib, io, json, os, re, signal, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "src", "content", "provas.json")

BUGS = []
def P(nivel, codigo, linha, correcao, explica, u=None):
    BUGS.append(dict(nivel=nivel, codigo=codigo, linha=linha, correcao=correcao, explica=explica, u=u))

# ============================================================ nível 1 — Faísca: sintaxe, nomes e tipos
P(1, 'idade = 20\nif idade >= 18\n    print("Pode votar")', 2, 'if idade >= 18:', "Faltaram os dois-pontos no fim do if.")
P(1, 'nome = "Ana\nprint("Oi,", nome)', 1, 'nome = "Ana"', "As aspas do texto não foram fechadas.")
P(1, 'x = 5\nprint("Valor:", x\ny = x * 2\nprint(y)', 2, 'print("Valor:", x)', "O parêntese do print não foi fechado.")
P(1, 'nota = 7\nif nota = 7:\n    print("Sete!")', 2, 'if nota == 7:', "Para comparar use ==. Um = só serve para guardar valor.")
P(1, 'for i in range(3):\nprint(i)', 2, '    print(i)', "O que fica dentro do for precisa de recuo (4 espaços).")
P(1, 'mensagem = "oi"\nprint(mensgem)', 2, 'print(mensagem)', "Erro de digitação: a variável se chama mensagem.")
P(1, 'idade = 30\nprint("Idade: " + idade)', 2, 'print("Idade: " + str(idade))', "Não dá para juntar texto com número usando +. Converta com str().")
P(1, 'def saudacao(nome):\n    print("Oi", nome)\n\nsaudacao()', 4, 'saudacao("Ana")', "A função pede um nome, mas foi chamada sem nenhum.")
P(1, 'lista = [1, 2, 3]\nprint(lista[3])', 2, 'print(lista[2])', "Os índices vão de 0 a 2. O último item é lista[2].")
P(1, 'nome = "Bia"\nPrint("Oi", nome)', 2, 'print("Oi", nome)', "Python diferencia maiúsculas: é print, com p minúsculo.")
P(1, 'numeros = [1, 2, 3\ntotal = sum(numeros)\nprint(total)', 1, 'numeros = [1, 2, 3]', "O colchete da lista não foi fechado.")
P(1, 'contador = 0\nwhile contador < 3\n    contador += 1\nprint(contador)', 2, 'while contador < 3:', "Faltaram os dois-pontos no fim do while.")
P(1, 'def dobro(n)\n    return n * 2\n\nprint(dobro(4))', 1, 'def dobro(n):', "Faltaram os dois-pontos no fim do def.")
P(1, 'pessoa = {"nome": "Ana"}\nprint(pessoa["idade"])', 2, 'print(pessoa["nome"])', "O dicionário não tem a chave \"idade\".")
P(1, 'frutas = ["uva", "kiwi"]\nfrutas.add("pera")\nprint(frutas)', 2, 'frutas.append("pera")', "Listas usam append. add é de conjuntos (set).")
P(1, 'if 5 > 3:\n    print("maior")\n  print("fim")', 3, '    print("fim")', "O recuo das linhas do mesmo bloco precisa ser igual.")
P(1, 'total = 10\nmetade = total / 0\nprint(metade)', 2, 'metade = total / 2', "Não existe divisão por zero.")
P(1, 'idade = "20"\nprox = idade + 1\nprint(prox)', 2, 'prox = int(idade) + 1', "idade é texto. Converta com int() antes de somar.")
P(1, 'texto = "python"\nprint(texto.upper)  # esperado: PYTHON', 2, 'print(texto.upper())  # esperado: PYTHON', "Faltaram os parênteses: sem eles o método não é chamado.")
P(1, 'cores = ["azul", "verde"]\nfor cor in cores\n    print(cor)', 2, 'for cor in cores:', "Faltaram os dois-pontos no fim do for.")
P(1, 'preco = 10\ntotal = preco * quantidade\nprint(total)', 2, 'total = preco * 3', "A variável quantidade nunca foi criada.")
P(1, 'print("Olá, mundo!)', 1, 'print("Olá, mundo!")', "As aspas do texto não foram fechadas antes do parêntese.")

# ============================================================ nível 2 — Chama: lógica e erros de execução
P(2, 'total = 0\nfor n in range(1, 5):\n    total += n\nprint(total)  # esperado: 15', 2, 'for n in range(1, 6):', "range(1, 5) para no 4. Para somar até 5, use range(1, 6).")
P(2, 'v = [3, 1, 2]\nordenada = v.sort()\nprint(ordenada)  # esperado: [1, 2, 3]', 2, 'ordenada = sorted(v)', ".sort() ordena a lista e devolve None. sorted(v) devolve a lista nova.")
P(2, 'def soma(a, b):\n    print(a + b)\n\nr = soma(2, 3)\nprint(r * 2)', 2, '    return a + b', "A função só mostra o resultado; sem return, ela devolve None.")
P(2, 'nomes = ["ana", "bia"]\nfor i in range(len(nomes) + 1):\n    print(nomes[i])', 2, 'for i in range(len(nomes)):', "O +1 faz o laço passar do último índice.")
P(2, 'media = (7 + 8 + 9) / 2\nprint(media)  # esperado: 8.0', 1, 'media = (7 + 8 + 9) / 3', "São 3 notas: divida por 3.")
P(2, 'idade = 18\nif idade > 18:\n    print("adulto")\nelse:\n    print("menor")  # 18 já é adulto', 2, 'if idade >= 18:', "Com > o 18 fica de fora. Use >=.")
P(2, 'palavra = "banana"\nprint(palavra.count(a))', 2, 'print(palavra.count("a"))', "Sem aspas, a vira o nome de uma variável que não existe.")
P(2, 'nums = [1, 2, 3]\nnums = nums.append(4)\nprint(nums)  # esperado: [1, 2, 3, 4]', 2, 'nums.append(4)', "append muda a lista e devolve None. Não guarde o resultado.")
P(2, 'texto = "  oi  "\ntexto.strip()\nprint(len(texto))  # esperado: 2', 2, 'texto = texto.strip()', "strip devolve um texto novo. Guarde o resultado.")
P(2, 'def area(base, altura):\n    return base * altura\n\nprint(area(3))', 4, 'print(area(3, 4))', "A função pede dois argumentos e recebeu um só.")
P(2, 'pares = []\nfor n in range(10):\n    if n % 2 == 1:\n        pares.append(n)\nprint(pares)  # esperado: [0, 2, 4, 6, 8]', 3, '    if n % 2 == 0:', "Par é quem tem resto 0 na divisão por 2.")
P(2, 'letras = "abc"\nletras[0] = "A"\nprint(letras)', 2, 'letras = "A" + letras[1:]', "Textos não podem ser alterados por índice. Monte um texto novo.")
P(2, 'd = {"a": 1}\nfor k, v in d:\n    print(k, v)', 2, 'for k, v in d.items():', "Para pegar chave e valor juntos, use d.items().")
P(2, 'idades = [20, 30]\nprint(", ".join(idades))', 2, 'print(", ".join(map(str, idades)))', "join só junta textos. Converta os números com map(str, ...).")
P(2, 'lista = [5, 3, 8]\nmaior = 0\nfor n in lista:\n    if n < maior:\n        maior = n\nprint(maior)  # esperado: 8', 4, '    if n > maior:', "Para achar o maior, troque quando n for MAIOR.")
P(2, 'cont = {"a": 0}\ncont["b"] += 1\nprint(cont)', 2, 'cont["b"] = cont.get("b", 0) + 1', "A chave \"b\" ainda não existe. Use get com valor padrão.")
P(2, 'vogais = 0\nfor c in "arara":\n    if c in "aeiou":\n        vogais = 1\nprint(vogais)  # esperado: 3', 4, '        vogais += 1', "= 1 só guarda 1. Para contar, some com += 1.")
P(2, 'n = 5\nfat = 0\nfor i in range(1, n + 1):\n    fat *= i\nprint(fat)  # esperado: 120', 2, 'fat = 1', "Multiplicar por 0 sempre dá 0. Comece o fatorial em 1.")
P(2, 'nums = [1, 2, 3]\nprint(sum(nums) / len(num))', 2, 'print(sum(nums) / len(nums))', "Erro de digitação: a lista se chama nums.")
P(2, 'nome = "ana"\nnome.upper()\nprint(nome)  # esperado: ANA', 2, 'nome = nome.upper()', "upper devolve um texto novo. Guarde o resultado.")
P(2, 'nome = "Ana"\nprint("Oi, {nome}!")  # esperado: Oi, Ana!', 2, 'print(f"Oi, {nome}!")  # esperado: Oi, Ana!', "Faltou o f antes das aspas para virar f-string.")
P(2, 'def dobro(x):\n    return x * 2\n\nprint(dobro)  # esperado: 10', 4, 'print(dobro(5))  # esperado: 10', "Sem parênteses, a função não é chamada.")
P(2, 'nums = [1, 2, 3]\nquadrados = [n ** 2 for n in nums]\nprint(quadrados[3])', 3, 'print(quadrados[2])', "A lista tem 3 itens: índices 0, 1 e 2.")
P(2, 'def saudar(nome="visitante"):\n    return "Oi, " + nome\n\nprint(saudar(None))', 4, 'print(saudar())', "Passar None anula o valor padrão. Chame sem argumento.")
P(2, 'notas = {"ana": 8}\nprint(notas[ana])', 2, 'print(notas["ana"])', "A chave é um texto: precisa de aspas.")

# ============================================================ nível 3 — Inferno: bugs sutis
P(3, 'def primeiro_par(v):\n    for n in v:\n        if n % 2 == 0:\n            return n\n        return None\n\nprint(primeiro_par([1, 3, 4]))  # esperado: 4', 5, '    return None', "O return None está dentro do for: a função desiste já no primeiro número.")
P(3, 'original = [1, 2]\ncopia = original\ncopia.append(3)\nprint(original)  # esperado: [1, 2]', 2, 'copia = original.copy()', "copia = original não copia: os dois nomes apontam para a mesma lista.")
P(3, 'm = map(int, ["1", "2"])\nprint(sum(m))\nprint(max(m))  # esperado: 2', 1, 'm = list(map(int, ["1", "2"]))', "map se esgota depois do sum. Guarde numa lista para usar duas vezes.")
P(3, 'total = 0.1 + 0.2\nif total == 0.3:\n    print("igual")\nelse:\n    print("diferente")  # esperado: igual', 2, 'if round(total, 2) == 0.3:', "0.1 + 0.2 dá 0.30000000000000004. Compare floats arredondando.")
P(3, 'nomes = ["bia", "Caio", "ana"]\nprint(sorted(nomes))  # esperado: [\'ana\', \'bia\', \'Caio\']', 2, 'print(sorted(nomes, key=str.lower))  # esperado: [\'ana\', \'bia\', \'Caio\']', "Maiúsculas vêm antes na ordenação. key=str.lower ignora isso.")
P(3, 'x = "5"\ny = "3"\nprint(x + y)  # esperado: 8', 3, 'print(int(x) + int(y))  # esperado: 8', "Somar textos junta as letras: \"5\" + \"3\" dá \"53\".")
P(3, 'n = 7\nif n % 2 == 0 or 1:\n    print("par")\nelse:\n    print("ímpar")  # esperado: ímpar', 2, 'if n % 2 == 0:', "or 1 é sempre verdadeiro, então o if sempre entra.")
P(3, 'resposta = "não"\nif resposta == "sim" or "s":\n    print("confirmado")\nelse:\n    print("cancelado")  # esperado: cancelado', 2, 'if resposta in ("sim", "s"):', "or \"s\" é sempre verdadeiro. Compare as duas opções com in.")
P(3, 'notas = [8, 9, 9]\nmedia = sum(notas) // len(notas)\nprint(round(media, 2))  # esperado: 8.67', 2, 'media = sum(notas) / len(notas)', "// é divisão inteira e joga fora as casas decimais.")
P(3, 'texto = "Olá Mundo"\nif texto.find("Olá"):\n    print("achou")\nelse:\n    print("não achou")  # esperado: achou', 2, 'if "Olá" in texto:', "find devolve a posição 0, que conta como falso. Use in.")
P(3, 'palavras = "um dois três".split(",")\nprint(len(palavras))  # esperado: 3', 1, 'palavras = "um dois três".split()', "Não há vírgulas no texto. split() sem argumento separa nos espaços.")
P(3, 'valores = [10, 20, 30]\nprint(valores[1:2])  # esperado: [20, 30]', 2, 'print(valores[1:])  # esperado: [20, 30]', "O fim da fatia não entra: [1:2] pega só o 20.")
P(3, 'dados = {"x": 1, "y": 2}\nfor chave, valor in dados.items:\n    print(chave, valor)', 2, 'for chave, valor in dados.items():', "Faltaram os parênteses: items é um método.")
P(3, 'def maior(a, b):\n    if a > b:\n        return a\n    return a\n\nprint(maior(2, 9))  # esperado: 9', 4, '    return b', "Quando a não é maior, o certo é devolver b.")
P(3, 'nums = [4, 8, 15]\nfor i, n in enumerate(nums, 1):\n    print(i, nums[i])', 3, '    print(i, n)', "Com start=1, i chega a 3 e nums[3] não existe. Use n.")
P(3, 'texto = "a,b,c"\nitens = texto.split(",")\nprint(itens.join("-"))', 3, 'print("-".join(itens))', "join é método do texto separador: \"-\".join(itens).")
P(3, 'v = [1, 2, 3]\nprint(v.reverse())  # esperado: [3, 2, 1]', 2, 'print(v[::-1])  # esperado: [3, 2, 1]', "reverse inverte a lista e devolve None.")
P(3, 'contador = {}\nfor letra in "aba":\n    contador[letra] = contador.get(letra) + 1\nprint(contador)', 3, '    contador[letra] = contador.get(letra, 0) + 1', "get sem padrão devolve None, e None + 1 dá erro.")
P(3, 'idade = 20\nif 18 <= idade < 20:\n    print("jovem adulto")\nelse:\n    print("outro")  # esperado: jovem adulto', 2, 'if 18 <= idade <= 20:', "< 20 deixa o 20 de fora. Use <= 20.")
P(3, 'precos = [10, 20, 30]\nfor i in range(len(precos)):\n    p = precos[i] * 2\nprint(precos)  # esperado: [20, 40, 60]', 3, '    precos[i] = precos[i] * 2', "O dobro foi guardado em p, e a lista nunca mudou.")
P(3, 'linhas = ["a\\n", "b\\n"]\nlimpas = [l.strip for l in linhas]\nprint(limpas)  # esperado: [\'a\', \'b\']', 2, 'limpas = [l.strip() for l in linhas]', "Faltaram os parênteses: sem eles a lista guarda o método, não o texto.")
P(3, 'def conta(lista, alvo):\n    return lista.count(alvo)\n\nprint(conta("banana", "an"))  # esperado: 2\nprint(conta([1, 1, 2], "1"))  # esperado: 2', 5, 'print(conta([1, 1, 2], 1))  # esperado: 2', "\"1\" é texto e a lista tem números. Procure o número 1.")
P(3, 'agenda = {}\nagenda.update("ana", 123)\nprint(agenda)', 2, 'agenda.update({"ana": 123})', "update recebe um dicionário, não chave e valor separados.")
P(3, 'nums = [3, 1, 2]\nmaior = max(nums)\nnums.remove(maior)\nsegundo = max(num)\nprint(segundo)', 4, 'segundo = max(nums)', "Erro de digitação escondido: a lista se chama nums.")

# ============================================================ provas que fecham cada unidade
# Formato em provas_unidades.txt. A linha corrigida herda o recuo da linha com bug
# quando é escrita sem recuo.
NIVEL_UNIDADE = {**{f"u{i}": 1 for i in range(4)}, **{f"u{i}": 2 for i in (4, 5, 6, 7, 8, 12)},
                 **{f"u{i}": 3 for i in (9, 10, 11)}, **{f"b{i}": 2 for i in range(6)}, **{f"b{i}": 3 for i in range(6, 18)}}
def ler_unidades(caminho):
    bloco = None
    for raw in open(caminho, encoding="utf-8").read().split("\n") + ["@fim 0"]:
        if raw.startswith("#") and bloco is None:
            continue
        if raw.startswith("@"):
            if bloco:
                linhas = bloco["codigo"]
                while linhas and not linhas[-1].strip():
                    linhas.pop()
                orig = linhas[bloco["linha"] - 1] if 0 < bloco["linha"] <= len(linhas) else ""
                fix = bloco["fix"]
                if fix and not fix[0].isspace():
                    fix = orig[: len(orig) - len(orig.lstrip())] + fix
                P(NIVEL_UNIDADE[bloco["u"]], "\n".join(linhas), bloco["linha"], fix, bloco["explica"], u=bloco["u"])
            u, n = raw[1:].split()
            bloco = None if u == "fim" else {"u": u, "linha": int(n), "codigo": [], "fix": None, "explica": ""}
        elif bloco is not None:
            if raw.startswith(">>> "):
                bloco["fix"] = raw[4:]
            elif raw.startswith("!! "):
                bloco["explica"] = raw[3:]
            elif bloco["fix"] is None:
                bloco["codigo"].append(raw)
ler_unidades(os.path.join(AQUI, "provas_unidades.txt"))

# Os grupos antigos de built-ins (b0..b11) viraram 71 unidades, uma por função: seus bugs
# ficam só no modo livre, e cada unidade fn_<nome> usa os bugs de tools/builtins_licoes.
for b in BUGS:
    if b["u"] and re.fullmatch(r"b([0-9]|1[01])", b["u"]):
        b["u"] = None
import glob, sys as _sys
_sys.path.insert(0, AQUI)
from bt_helpers import ler_bugs
from validar_builtins import GRUPOS
for g, nomes in GRUPOS.items():
    nivel = 2 if int(g[1:]) <= 6 else 3
    for caminho in glob.glob(os.path.join(AQUI, "builtins_licoes", f"{g}_*.py")):
        texto = open(caminho, encoding="utf-8").read()
        bloco = texto[texto.index("BUGS = r'''") + 11:]
        bloco = bloco[: bloco.index("'''")]
        for b in ler_bugs(bloco):
            P(nivel, b["codigo"], b["linha"], b["correcao"], b["explica"], u=b["u"])
    for nome in nomes:
        NIVEL_UNIDADE[f"fn_{nome}"] = nivel
from validar_builtins import BASE
for key in BASE:
    texto = open(os.path.join(AQUI, "builtins_licoes", f"{key}.py"), encoding="utf-8").read()
    bloco = texto[texto.index("BUGS = r\'\'\'") + 11:]
    bloco = bloco[: bloco.index("\'\'\'")]
    for b in ler_bugs(bloco):
        P(1, b["codigo"], b["linha"], b["correcao"], b["explica"], u=b["u"])
    NIVEL_UNIDADE[key] = 1
# Trilha Bibliotecas: uma prova por biblioteca (padrão = nível 2, externas = nível 3).
from validar_bibliotecas import arquivos as _arqs_libs, carregar as _carregar_lib
for _c in _arqs_libs():
    _m = _carregar_lib(_c)
    _nv = 3 if _m.UNIDADE["externa"] else 2
    for b in ler_bugs(_m.BUGS):
        P(_nv, b["codigo"], b["linha"], b["correcao"], b["explica"], u=b["u"])
    NIVEL_UNIDADE[_m.UNIDADE["id"]] = _nv
for k in [k for k in NIVEL_UNIDADE if re.fullmatch(r"b([0-9]|1[01])", k)]:
    del NIVEL_UNIDADE[k]

# ============================================================ validação
class Tempo(Exception):
    pass
def _alarme(*_):
    raise Tempo()
signal.signal(signal.SIGALRM, _alarme)

def rodar(src):
    os.chdir(tempfile.mkdtemp())
    buf = io.StringIO()
    signal.alarm(2)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, "codigo.py", "exec"), {"__name__": "__main__"})
        return buf.getvalue().rstrip("\n"), None
    except Tempo:
        return buf.getvalue(), "Tempo"
    except Exception as e:
        return buf.getvalue().rstrip("\n"), e
    finally:
        signal.alarm(0)

problemas, saida = [], []
for i, b in enumerate(BUGS):
    linhas = b["codigo"].split("\n")
    n = b["linha"]
    if not 1 <= n <= len(linhas):
        problemas.append((i, "linha fora do código")); continue
    if linhas[n - 1] == b["correcao"]:
        problemas.append((i, "correção igual à linha")); continue
    certo = linhas[:]; certo[n - 1] = b["correcao"]
    out_ok, err_ok = rodar("\n".join(certo))
    if err_ok:
        problemas.append((i, "código corrigido falha", err_ok, b["codigo"])); continue
    m = re.search(r"# esperado: (.*)$", b["codigo"], re.M)
    if m and out_ok.split("\n")[-1] != m.group(1).strip():
        problemas.append((i, "esperado não bate", repr(out_ok), m.group(1))); continue
    out_bug, err_bug = rodar(b["codigo"])
    if err_bug == "Tempo":
        tipo, msg = "Laço infinito", "O programa nunca termina."
    elif err_bug:
        tipo = type(err_bug).__name__
        msg = f"{tipo}: {err_bug.msg if isinstance(err_bug, SyntaxError) else err_bug}"
    elif out_bug != out_ok:
        tipo, msg = "Resultado errado", f"Saiu: {out_bug.splitlines()[-1] if out_bug else '(nada)'}"
    else:
        problemas.append((i, "o código com bug funciona igual", b["codigo"])); continue
    saida.append({"id": f"f{i}", "nivel": b["nivel"], "linhas": linhas, "linha": n - 1, "correcao": b["correcao"],
                  "explica": b["explica"], "tipo": tipo, "msg": msg, "u": b["u"]})

if problemas:
    for p in problemas: print("PROBLEMA:", p)
    raise SystemExit(1)
por_unidade = {}
for b in saida:
    if b["u"]: por_unidade[b["u"]] = por_unidade.get(b["u"], 0) + 1
faltando = [u for u in NIVEL_UNIDADE if por_unidade.get(u, 0) < 5]
if faltando:
    print("PROBLEMA: unidades com menos de 5 bugs:", faltando); raise SystemExit(1)
json.dump({"bugs": saida}, open(SAIDA, "w"), ensure_ascii=False, indent=1)
por_nivel = {n: sum(1 for b in saida if b["nivel"] == n) for n in (1, 2, 3)}
print("OK:", len(saida), "bugs", por_nivel, "| unidades:", len(por_unidade), "| mínimo por unidade:", min(por_unidade.values()))
