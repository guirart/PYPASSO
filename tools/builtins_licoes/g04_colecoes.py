from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ list
    "list": [
        # lição 2
        L("Cópia de verdade",
          "Escrever b = a não copia a lista: só dá outro nome para a MESMA lista. Já list(a) cria uma lista nova, com os mesmos itens, que você pode mudar sem mexer na original.",
          'a = [1, 2]\nb = a\nc = list(a)\na.append(3)\nprint(b)\nprint(c)',
          [OUT('a = [1]\nb = list(a)\nb.append(2)\nprint(a)', ["[1, 2]", "[2]", "[]"], "b é uma cópia: mudar b não muda a."),
           TYPE('x = [5, 6]\ny = x\ny.append(7)\nprint(len(x))', "x e y são a mesma lista, então x também ganhou o 7."),
           MC("Qual a diferença entre b = a e b = list(a)?", "list(a) cria uma lista nova; b = a só dá outro nome",
              ["Nenhuma, as duas copiam", "b = a cria uma lista vazia", "list(a) apaga a lista a"],
              "Com b = a, as duas variáveis apontam para a mesma lista."),
           FILL("Complete para criar uma cópia independente das notas.", 'notas = [7, 8]\ncopia = ___(notas)\ncopia.append(10)\nprint(notas)',
                "list", ["len", "str", "print"], "list(notas) devolve uma lista nova com os mesmos itens.")]),
        # lição 3
        L("Do texto e do dicionário",
          "list() percorre a coleção e guarda cada item. Num texto, cada caractere vira um item (inclusive espaços). Num dicionário, você recebe só as chaves; para os valores, use list(d.values()).",
          'palavra = "pipo"\nprint(list(palavra))\nprecos = {"pão": 2, "leite": 5}\nprint(list(precos))\nprint(list(precos.values()))',
          [OUT('estoque = {"maçã": 3, "uva": 0}\nprint(list(estoque))', ["[3, 0]", "[('maçã', 3), ('uva', 0)]", "['maçã', 3, 'uva', 0]"], "Percorrer um dicionário dá as chaves."),
           OUT('print(list("a b"))', ["['a', 'b']", "['a b']", "['a', 'b', ' ']"], "O espaço também é um caractere, e a ordem é mantida."),
           MC('Para separar "café com leite" em palavras, use…', "texto.split()", ["list(texto)", "tuple(texto)", "list(texto, \" \")"],
              "list(texto) separa letra por letra; split() separa nos espaços."),
           CODE("Transforme o texto codigo em uma lista de caracteres chamada partes e mostre a lista.",
                'codigo = "PY42"\npartes = codigo\nprint(partes)\n',
                'codigo = "PY42"\npartes = list(codigo)\nprint(partes)',
                'assert partes == ["P", "Y", "4", "2"], "partes deve ser [\'P\', \'Y\', \'4\', \'2\']"',
                "partes = list(codigo)")]),
        # lição 4
        L("Cuidados com list()",
          "list() só aceita coisas que dá para percorrer: textos, tuplas, conjuntos, ranges… Um número sozinho dá TypeError. E cuidado: se você criar uma variável chamada list, a função some.",
          'print(list("42"))\ntry:\n    list(42)\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('try:\n    print(list(7))\nexcept TypeError:\n    print("não dá")', ["[7]", "['7']", "[0, 1, 2, 3, 4, 5, 6]"], "Um número não pode ser percorrido, então dá TypeError."),
           OUT('print(list(["abc"]))', ["['a', 'b', 'c']", "[['abc']]", "abc"], "A lista tem um item só: o texto \"abc\". list() não entra dentro dele."),
           MC("Por que list(123) dá erro?", "Números não são coleções para percorrer",
              ["123 é grande demais", "Faltaram os colchetes", "list só aceita textos"],
              "Para pegar os dígitos, converta antes: list(str(123))."),
           MC("Depois de list = [1, 2], o que acontece em list(\"oi\")?", "TypeError: o nome list agora é uma lista",
              ["Mostra ['o', 'i']", "Mostra [1, 2, 'o', 'i']", "Mostra [1, 2]"],
              "A variável escondeu a função. Nunca use list como nome de variável.")]),
        # lição 5
        L("list com outras funções",
          "map, filter, zip e reversed não devolvem listas: devolvem objetos \"preguiçosos\". Para ver ou reaproveitar os itens, embrulhe com list().",
          'n = [3, 1, 2]\nprint(list(reversed(n)))\nprint(list(map(str, n)))\nprint(list(zip("ab", [1, 2])))',
          [TYPE('print(list(map(int, "123")))', "Cada caractere vira número inteiro."),
           OUT('print(list(zip([1, 2], "xy")))', ["[1, 2, 'x', 'y']", "[[1, 'x'], [2, 'y']]", "{1: 'x', 2: 'y'}"], "zip forma pares (tuplas), e list junta os pares numa lista."),
           ORDER("Monte o programa que mostra a lista dos números pares de 0 a 9.",
                 ['numeros = range(10)', 'pares = filter(lambda n: n % 2 == 0, numeros)', 'print(list(pares))'],
                 "filter escolhe os itens; list() transforma o resultado em lista para mostrar."),
           CODE("Crie maiusculas: a lista nomes com todos os nomes em letras maiúsculas. Use list(map(str.upper, nomes)).",
                'nomes = ["ana", "bia", "caio"]\nmaiusculas = nomes\nprint(maiusculas)\n',
                'nomes = ["ana", "bia", "caio"]\nmaiusculas = list(map(str.upper, nomes))\nprint(maiusculas)',
                'assert maiusculas == ["ANA", "BIA", "CAIO"], "maiusculas deve ser [\'ANA\', \'BIA\', \'CAIO\']"\nassert nomes == ["ana", "bia", "caio"], "A lista nomes não deve mudar"',
                "maiusculas = list(map(str.upper, nomes))")]),
        # lição 6
        L("Desafio: lista de compras",
          "Dá para montar listas juntando pedaços: list() converte, + junta e append coloca um item no final. Repare: append de uma lista coloca a lista inteira como UM item.",
          'compras = list(("arroz", "feijão"))\ncompras += list({"ovos": 12})\nprint(compras)\nprint(len(compras))',
          [OUT('a = list(range(3))\na.append(list("x"))\nprint(a)', ["[0, 1, 2, 'x']", "[0, 1, 2, x]", "[1, 2, 3, ['x']]"], "append coloca a lista ['x'] inteira como último item."),
           TYPE('print(list(range(3)) + list("ab"))', "O + junta as duas listas numa só."),
           MC("Qual destas cria [0, 0, 0]?", "[0] * 3", ["list(0, 3)", "list(3)", "list([0, 3])"], "Repetir a lista [0] três vezes. list(3) daria erro."),
           CODE("Crie a função sem_repetir(itens) que devolve uma LISTA sem repetidos, em ordem crescente.",
                "def sem_repetir(itens):\n    return itens\n",
                "def sem_repetir(itens):\n    return sorted(set(itens))",
                'assert sem_repetir([3, 1, 3, 2]) == [1, 2, 3], "sem_repetir([3, 1, 3, 2]) deve ser [1, 2, 3]"\nassert type(sem_repetir((2, 2))) is list, "O resultado deve ser uma lista"\nassert sem_repetir([]) == [], "Lista vazia devolve lista vazia"',
                "set tira os repetidos e sorted devolve uma lista já ordenada: return sorted(set(itens))")]),
    ],

    # ================================================================ tuple
    "tuple": [
        # lição 2
        L("É a vírgula que manda",
          "O que cria a tupla é a vírgula, não os parênteses. Por isso uma tupla de um item precisa de vírgula: (5,). Escrever a = 1, 2 também cria uma tupla.",
          'a = (5,)\nb = 1, 2, 3\nprint(type(a).__name__, len(a))\nprint(b)\nprint(tuple())',
          [OUT('t = 3, 4\nprint(t)', ["3, 4", "[3, 4]", "34"], "Valores separados por vírgula formam uma tupla."),
           TYPE('print(len(("oi",)))', "Com a vírgula, é uma tupla com um item."),
           MC("Qual destas é uma tupla com um só item?", '("a",)', ['("a")', '["a"]', '{"a"}'], "Sem a vírgula, (\"a\") é só um texto entre parênteses."),
           FILL("Complete para criar uma tupla de um item.", 't = (7___)\nprint(len(t))', ",", [".", ";", ":"], "(7,) é uma tupla; (7) é só o número 7.")]),
        # lição 3
        L("Desempacotar valores",
          "Dá para abrir uma tupla em várias variáveis de uma vez: x, y = (3, 8). Funções usam isso para devolver vários valores. E a, b = b, a troca dois valores sem variável extra.",
          'def min_max(n):\n    return min(n), max(n)\n\nmenor, maior = min_max([4, 9, 1])\nprint(menor, maior)\na, b = 1, 2\na, b = b, a\nprint(a, b)',
          [OUT('ponto = (3, 8)\nx, y = ponto\nprint(y)', ["3", "(3, 8)", "x"], "x recebe o primeiro item e y o segundo."),
           TYPE('a, b = "oi", 5\na, b = b, a\nprint(a, b)', "Os valores foram trocados."),
           MC("O que uma função com return 1, 2 devolve?", "A tupla (1, 2)", ["Só o 1", "A lista [1, 2]", "Erro"], "A vírgula junta os valores numa tupla."),
           CODE("Crie a função divide(a, b) que devolve DOIS valores: o quociente inteiro (//) e o resto (%).",
                "def divide(a, b):\n    return a // b\n",
                "def divide(a, b):\n    return a // b, a % b",
                'assert divide(7, 2) == (3, 1), "divide(7, 2) deve devolver (3, 1)"\nassert divide(10, 5) == (2, 0), "divide(10, 5) deve devolver (2, 0)"',
                "return a // b, a % b devolve uma tupla com os dois valores.")]),
        # lição 4
        L("Imutável, mas…",
          "Tupla não tem append nem aceita t[0] = x. Para \"mudar\", você cria outra: t = t + (3,). Atenção: se a tupla guarda uma lista, a lista lá dentro ainda pode mudar.",
          't = (1, 2)\nt = t + (3,)\nprint(t)\ndupla = ([1], "x")\ndupla[0].append(2)\nprint(dupla)',
          [OUT('t = (1, 2)\ntry:\n    t.append(3)\nexcept AttributeError:\n    print("sem append")', ["(1, 2, 3)", "[1, 2, 3]", "None"], "Tuplas não têm o método append."),
           OUT('t = ([0], 5)\nt[0].append(1)\nprint(t)', ["([0], 5)", "Erro", "([1], 5)"], "A tupla continua com os mesmos objetos, mas a lista de dentro mudou."),
           MC("O que acontece em a, b = (1, 2, 3)?", "ValueError: valores demais para desempacotar",
              ["a = 1 e b = 2", "a = 1 e b = (2, 3)", "a = (1, 2) e b = 3"],
              "O número de variáveis tem de ser igual ao de itens."),
           TYPE('t = ("a",)\nt = t * 3\nprint(t)', "* repete os itens e cria uma tupla nova.")]),
        # lição 5
        L("tuple com outras funções",
          "Tuplas aparecem por todo lado: d.items() dá pares (chave, valor), e tuplas podem ser chaves de dicionário porque não mudam. Elas são comparadas item a item, como palavras no dicionário.",
          'notas = {"Ana": 8, "Bia": 9}\nfor par in notas.items():\n    print(par)\nprint(tuple(sorted([3, 1, 2])))\nprint((1, 9) < (2, 0))',
          [OUT('print(tuple(sorted("cab")))', ["('c', 'a', 'b')", "['a', 'b', 'c']", "abc"], "sorted ordena e tuple transforma o resultado em tupla."),
           TYPE('mapa = {(0, 0): "casa"}\nprint(mapa[(0, 0)])', "A tupla (0, 0) funciona como chave."),
           MC("Por que (1, 2) pode ser chave de dicionário e [1, 2] não?", "Tuplas são imutáveis; listas podem mudar",
              ["Tuplas são menores", "Listas não têm índice", "É só uma convenção"],
              "Chaves precisam ser imutáveis para o dicionário achá-las depois."),
           CODE("Percorra alunos desempacotando cada tupla e mostre uma linha por aluno no formato Ana: 7",
                'alunos = [("Ana", 7), ("Bia", 10), ("Caio", 8)]\nfor aluno in alunos:\n    print(aluno)\n',
                'alunos = [("Ana", 7), ("Bia", 10), ("Caio", 8)]\nfor nome, nota in alunos:\n    print(f"{nome}: {nota}")',
                'assert __stdout__.strip().splitlines() == ["Ana: 7", "Bia: 10", "Caio: 8"], "Esperado: Ana: 7, Bia: 10 e Caio: 8, um por linha"',
                'for nome, nota in alunos: print(f"{nome}: {nota}")')]),
        # lição 6
        L("Desafio: coordenadas",
          "Tuplas são ótimas para dados fixos, como pontos (x, y) num jogo. Dá para percorrer uma lista de pontos desempacotando cada um, e min/max comparam pelo primeiro item.",
          'pontos = [(0, 0), (2, 3), (-1, 4)]\nfor x, y in pontos:\n    print(f"x={x} y={y}")\nprint(max(pontos))',
          [OUT('pontos = [(2, 1), (1, 5)]\nprint(min(pontos))', ["(2, 1)", "1", "(1, 1)"], "Compara o primeiro item: 1 < 2."),
           TYPE('p = tuple(range(1, 4))\nprint(sum(p) * len(p))', "(1, 2, 3): soma 6, tamanho 3."),
           ORDER("Monte o programa que troca os valores e mostra 2 1.", ['a, b = 1, 2', 'a, b = b, a', 'print(a, b)'], "Primeiro cria, depois troca, depois mostra."),
           CODE("Crie a função mover(ponto, dx, dy) que recebe uma tupla (x, y) e devolve uma NOVA tupla (x + dx, y + dy).",
                "def mover(ponto, dx, dy):\n    ponto[0] += dx\n    ponto[1] += dy\n    return ponto\n",
                "def mover(ponto, dx, dy):\n    x, y = ponto\n    return (x + dx, y + dy)",
                'assert mover((1, 2), 3, 4) == (4, 6), "mover((1, 2), 3, 4) deve ser (4, 6)"\nassert isinstance(mover((0, 0), 1, 1), tuple), "O resultado deve ser uma tupla"',
                "Tuplas não mudam: desempacote x, y = ponto e devolva (x + dx, y + dy).")]),
    ],

    # ================================================================ dict
    "dict": [
        # lição 2
        L("Formas de criar",
          "dict(outro) copia um dicionário, e você pode acrescentar chaves nomeadas: dict(base, ouro=50). dict.fromkeys(chaves, valor) cria várias chaves com o mesmo valor. Chave repetida? Vale a última.",
          'base = {"vida": 100}\ncopia = dict(base, ouro=50)\nprint(copia)\nprint(dict.fromkeys(["a", "b"], 0))',
          [OUT('print(dict([("x", 1), ("x", 2)]))', ["{'x': 1}", "{'x': 1, 'x': 2}", "Erro"], "A chave x aparece duas vezes; fica o último valor."),
           TYPE('d = dict(a=1)\ne = dict(d)\ne["a"] = 9\nprint(d["a"])', "e é uma cópia: mudar e não muda d."),
           MC("Qual destas NÃO funciona?", 'dict(nome completo="Ana")', ['dict(nome="Ana")', 'dict([("nome", "Ana")])', '{"nome completo": "Ana"}'],
              "Com chave=valor, a chave precisa ser um nome válido de variável, sem espaços."),
           FILL("Complete para criar {'a': 0, 'b': 0}.", 'print(dict.___(["a", "b"], 0))', "fromkeys", ["keys", "items", "values"],
                "fromkeys cria uma chave para cada item, todas com o mesmo valor.")]),
        # lição 3
        L("Contar coisas",
          "d.get(chave, padrão) devolve o valor ou o padrão se a chave não existe, sem dar erro. Com ele dá para contar: contagem[x] = contagem.get(x, 0) + 1.",
          'votos = ["pizza", "sushi", "pizza"]\ncontagem = dict()\nfor v in votos:\n    contagem[v] = contagem.get(v, 0) + 1\nprint(contagem)',
          [OUT('d = {"a": 1}\nprint(d.get("b", 0))', ["None", "Erro", "1"], "A chave b não existe, então vem o padrão 0."),
           TYPE('c = {}\nfor letra in "ovo":\n    c[letra] = c.get(letra, 0) + 1\nprint(c)', "o aparece duas vezes, v uma."),
           MC("O que d.get(\"x\") devolve se a chave x não existe?", "None", ["0", "KeyError", '""'], "Sem padrão, get devolve None."),
           CODE("Conte quantas vezes cada fruta aparece na lista frutas e guarde no dicionário contagem.",
                'frutas = ["uva", "maçã", "uva", "uva"]\ncontagem = dict()\n# conte aqui\nprint(contagem)\n',
                'frutas = ["uva", "maçã", "uva", "uva"]\ncontagem = dict()\nfor f in frutas:\n    contagem[f] = contagem.get(f, 0) + 1\nprint(contagem)',
                'assert contagem == {"uva": 3, "maçã": 1}, "contagem deve ser {\'uva\': 3, \'maçã\': 1}"',
                "for f in frutas: contagem[f] = contagem.get(f, 0) + 1")]),
        # lição 4
        L("Cuidados com chaves",
          "Buscar uma chave que não existe com d[chave] dá KeyError; teste antes com in ou use get. Chaves precisam ser imutáveis: texto, número e tupla podem; lista não.",
          'd = {"a": 1}\nprint("b" in d)\ntry:\n    d[["x"]] = 2\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('d = {"a": 1}\ntry:\n    print(d["b"])\nexcept KeyError:\n    print("não achei")', ["None", "0", "b"], "Com colchetes, chave inexistente dá KeyError."),
           OUT('print(dict(zip("abc", [1, 2])))', ["{'a': 1, 'b': 2, 'c': None}", "Erro", "{'a': 1, 'b': 2, 'c': 2}"], "zip para na coleção mais curta; o c fica de fora."),
           MC("Qual destas pode ser chave de dicionário?", "(1, 2)", ["[1, 2]", "{1, 2}", "{'a': 1}"], "Só a tupla é imutável."),
           TYPE('d = {"x": 1, "x": 5}\nprint(d)', "Chave repetida: o último valor substitui o primeiro.")]),
        # lição 5
        L("dict com outras funções",
          "Funções como sorted, max e len, aplicadas a um dicionário, olham as CHAVES. Para os valores use d.values(); para pares, d.items(). max(d, key=d.get) acha a chave com o maior valor.",
          'precos = {"café": 5, "bolo": 8, "suco": 6}\nprint(sum(precos.values()))\nprint(sorted(precos))\nprint(max(precos, key=precos.get))',
          [TYPE('d = {"b": 2, "a": 1}\nprint(sorted(d))', "sorted devolve a lista das chaves em ordem."),
           OUT('d = {"x": 3, "y": 7}\nprint(max(d))', ["7", "x", "('y', 7)"], "max compara as chaves: \"y\" vem depois de \"x\"."),
           OUT('d = dict(a=2, b=3)\nprint(list(d.items()))', ["['a', 'b']", "[2, 3]", "{'a': 2, 'b': 3}"], "items dá pares (chave, valor) em tuplas."),
           CODE("O dicionário notas guarda a nota de cada aluno. Guarde em media a média das notas (soma dos valores dividida pela quantidade).",
                'notas = {"Ana": 8, "Bia": 10, "Caio": 6}\nmedia = sum(notas)\nprint(media)\n',
                'notas = {"Ana": 8, "Bia": 10, "Caio": 6}\nmedia = sum(notas.values()) / len(notas)\nprint(media)',
                'assert media == 8, "A média de 8, 10 e 6 é 8"',
                "sum(notas) tenta somar os nomes. Use sum(notas.values()) / len(notas).")]),
        # lição 6
        L("Desafio: cardápio",
          "Um dicionário é perfeito para um cardápio: o nome do item é a chave e o preço é o valor. Para somar um pedido, percorra a lista do pedido e busque cada preço.",
          'cardapio = dict(zip(["pão", "café"], [3, 5]))\npedido = ["café", "pão", "café"]\ntotal = 0\nfor item in pedido:\n    total += cardapio[item]\nprint(total)',
          [OUT('d = {"a": 1, "b": 2}\ninv = dict(zip(d.values(), d.keys()))\nprint(inv)', ["{'a': 1, 'b': 2}", "{'a': 'b'}", "[(1, 'a'), (2, 'b')]"], "Os valores viram chaves e as chaves viram valores."),
           TYPE('estoque = dict(ovo=6, leite=0)\nestoque["leite"] += 2\nprint(estoque)', "Só o valor de leite mudou."),
           MC("Como juntar os dicionários a e b num novo (b ganha nas chaves repetidas)?", "a | b", ["a + b", "dict(a, b)", "a & b"],
              "O operador | junta dicionários; + não funciona com dict."),
           CODE("Crie a função preco_total(cardapio, pedido) que devolve a soma dos preços dos itens do pedido. Itens fora do cardápio valem 0.",
                "def preco_total(cardapio, pedido):\n    total = 0\n    for item in pedido:\n        total += cardapio[item]\n    return total\n",
                "def preco_total(cardapio, pedido):\n    total = 0\n    for item in pedido:\n        total += cardapio.get(item, 0)\n    return total",
                'c = {"pão": 3, "café": 5}\nassert preco_total(c, ["café", "pão", "café"]) == 13, "café + pão + café = 13"\nassert preco_total(c, ["bolo", "pão"]) == 3, "Itens fora do cardápio valem 0 (use get)"',
                "Use cardapio.get(item, 0) para não dar KeyError.")]),
    ],

    # ================================================================ set
    "set": [
        # lição 2
        L("Operações de conjunto",
          "Além de | (união), & (interseção) e - (diferença), existe ^ (diferença simétrica): o que está em um OU no outro, mas não nos dois. Use sorted() para ver o resultado em ordem.",
          'a = {1, 2, 3}\nb = {3, 4}\nprint(sorted(a | b))\nprint(sorted(a & b))\nprint(sorted(a - b))\nprint(sorted(a ^ b))',
          [TYPE('print(sorted({1, 2, 3} - {2}))', "Tira o 2 do primeiro conjunto."),
           OUT('print(sorted({1, 2} ^ {2, 3}))', ["[2]", "[1, 2, 3]", "[1, 2, 2, 3]"], "O 2 está nos dois, então sai; sobram 1 e 3."),
           MC("Qual operador dá os itens que estão nos DOIS conjuntos?", "&", ["|", "-", "^"], "& é a interseção."),
           FILL("Complete para juntar os dois conjuntos.", 'a = {"x"}\nb = {"y"}\nprint(sorted(a ___ b))', "|", ["&", "-", "+"],
                "| é a união. Conjuntos não aceitam +.")]),
        # lição 3
        L("Usos do dia a dia",
          "set é ótimo para tirar repetidos (quantos visitantes diferentes?), achar o que duas listas têm em comum e checar rapidinho se algo existe com in.",
          'emails = ["a@x.com", "b@x.com", "a@x.com"]\nunicos = set(emails)\nprint(len(unicos))\nprint("b@x.com" in unicos)',
          [TYPE('visitas = ["ana", "bia", "ana", "ana"]\nprint(len(set(visitas)))', "Só duas pessoas diferentes."),
           OUT('ana = {"rock", "pop"}\nbia = {"pop", "samba"}\nprint(sorted(ana & bia))', ["['rock', 'pop', 'samba']", "pop", "['pop', 'pop']"], "O gosto em comum é só pop, e sorted devolve uma lista."),
           MC("Por que usar set para checar se um item existe numa coleção grande?", "A busca com in é muito rápida",
              ["Ele guarda a ordem", "Ele aceita repetidos", "Ele ordena os itens sozinho"],
              "O set encontra o item direto, sem olhar um por um."),
           CODE("Crie a função comuns(a, b) que recebe duas listas e devolve uma lista ORDENADA com os itens que aparecem nas duas, sem repetir.",
                "def comuns(a, b):\n    return a + b\n",
                "def comuns(a, b):\n    return sorted(set(a) & set(b))",
                'assert comuns([1, 2, 2, 3], [2, 3, 4]) == [2, 3], "comuns([1, 2, 2, 3], [2, 3, 4]) deve ser [2, 3]"\nassert comuns(["x"], ["y"]) == [], "Sem itens em comum, devolva []"',
                "Transforme as duas em set, use & e ordene com sorted.")]),
        # lição 4
        L("Pegadinhas do set",
          "{} cria um dicionário, não um conjunto. set(\"oi\") separa as letras, mas {\"oi\"} guarda o texto inteiro. Conjuntos não têm ordem nem índice: s[0] dá erro.",
          'a = set("oi")\nb = {"oi"}\nprint(len(a), len(b))\nprint(type({}).__name__)',
          [OUT('print(len(set("casa")))', ["4", "1", "2"], "As letras diferentes são c, a e s."),
           OUT('s = {10, 20}\ntry:\n    print(s[0])\nexcept TypeError:\n    print("sem índice")', ["10", "20", "None"], "Conjuntos não têm posição, então não aceitam índice."),
           MC("Por que não confiar na ordem em que um set de textos aparece no print?", "Conjuntos não guardam ordem",
              ["Eles sempre ordenam em ordem alfabética", "Eles mostram na ordem em que foram criados", "Eles sempre invertem a ordem"],
              "Para mostrar em ordem, use sorted()."),
           TYPE('print(type({}).__name__, type(set()).__name__)', "{} é dicionário; conjunto vazio é set().")]),
        # lição 5
        L("set com outras funções",
          "sum, max, min e len funcionam com conjuntos. add coloca um item (se já existe, nada muda) e discard tira um item sem dar erro se ele não estiver lá.",
          'notas = [7, 9, 7, 10, 9]\ndiferentes = set(notas)\nprint(sorted(diferentes))\nprint(sum(diferentes), max(diferentes))\ndiferentes.add(5)\ndiferentes.discard(99)\nprint(len(diferentes))',
          [TYPE('print(sum(set([2, 2, 3])))', "O set fica {2, 3}, que soma 5."),
           OUT('s = set()\ns.add(1)\ns.add(1)\ns.add(2)\nprint(len(s))', ["3", "1", "Erro"], "O segundo add(1) não muda nada."),
           OUT('print(sorted(set(map(len, ["oi", "tchau", "lá"]))))', ["[2, 5, 2]", "[2, 2, 5]", "['lá', 'oi', 'tchau']"], "Os tamanhos são 2, 5 e 2; o set tira o 2 repetido."),
           MC("Qual a diferença entre remove(x) e discard(x)?", "remove dá erro se x não existe; discard não",
              ["São iguais", "discard apaga o conjunto todo", "remove só funciona com números"],
              "Use discard quando não tiver certeza de que o item está lá.")]),
        # lição 6
        L("Desafio: palavras únicas",
          "Juntando split, set e sorted, você descobre quantas palavras diferentes um texto tem e mostra todas em ordem.",
          'frase = "o gato e o rato e o pato"\npalavras = frase.split()\nunicas = set(palavras)\nprint(len(palavras), len(unicas))\nprint(sorted(unicas))',
          [TYPE('print(len(set("a b a".split())))', "As palavras são a, b, a: duas diferentes."),
           OUT('a = set(range(5))\nb = set(range(3, 8))\nprint(sorted(a - b))', ["[5, 6, 7]", "[3, 4]", "[0, 1, 2, 3, 4]"], "Tira de 0..4 os que também estão em 3..7."),
           ORDER("Monte o programa que mostra as vogais da palavra, sem repetir e em ordem.",
                 ['palavra = "abacaxi"', 'vogais = set(palavra) & set("aeiou")', 'print(sorted(vogais))'],
                 "A interseção com as vogais deixa só a e i."),
           CODE("Crie a função letras_unicas(texto) que devolve quantas letras diferentes o texto tem, ignorando espaços e maiúsculas.",
                "def letras_unicas(texto):\n    return len(texto)\n",
                'def letras_unicas(texto):\n    return len(set(texto.lower().replace(" ", "")))',
                'assert letras_unicas("Banana") == 3, "Banana tem 3 letras diferentes: b, a e n"\nassert letras_unicas("Oi oi") == 2, "Oi oi tem 2 letras diferentes (ignore espaço e maiúsculas)"',
                'Deixe tudo minúsculo, tire os espaços e conte com len(set(...)).')]),
    ],

    # ================================================================ frozenset
    "frozenset": [
        # lição 2
        L("Criando e comparando",
          "frozenset() sem nada é um conjunto fixo vazio. Ele faz as mesmas operações que o set (|, &, -), e o resultado também é um frozenset.",
          'vazio = frozenset()\nprint(len(vazio))\nf = frozenset([1, 2, 3])\nprint(f | {4})\nprint(f == {1, 2, 3})',
          [OUT('f = frozenset([1, 2])\nprint(type(f | {3}).__name__)', ["set", "list", "Erro"], "A operação começa num frozenset, então devolve frozenset."),
           TYPE('print(frozenset())', "Assim o Python mostra um frozenset vazio."),
           MC("O que frozenset tem em comum com set?", "Não guarda repetidos e faz união e interseção",
              ["Pode mudar com add", "Guarda a ordem dos itens", "Aceita índice [0]"],
              "A diferença é só que o frozenset não muda."),
           FILL("Complete para criar um conjunto que NÃO pode ser alterado.", 'dias = ___(["sáb", "dom"])\nprint(len(dias))', "frozenset", ["set", "list", "dict"],
                "frozenset cria um conjunto congelado.")]),
        # lição 3
        L("Chave sem ordem",
          "Como não muda, o frozenset pode ser chave de dicionário ou item de outro conjunto. E como não tem ordem, frozenset([\"Ana\", \"Bia\"]) é igual a frozenset([\"Bia\", \"Ana\"]). Ótimo para pares!",
          'amizades = set()\namizades.add(frozenset(["Ana", "Bia"]))\namizades.add(frozenset(["Bia", "Ana"]))\nprint(len(amizades))',
          [TYPE('d = {frozenset([1, 2]): "par"}\nprint(d[frozenset([2, 1])])', "A ordem não importa: é a mesma chave."),
           OUT('s = {frozenset("ab"), frozenset("ba")}\nprint(len(s))', ["2", "4", "Erro"], "Os dois frozensets são iguais, então o set guarda um só."),
           MC("Por que {{1, 2}} (um set dentro de outro) dá TypeError?", "O set de dentro pode mudar, então não pode ser item",
              ["Faltou uma vírgula", "Sets só guardam textos", "Sets não podem ter 2 itens"],
              "Use frozenset({1, 2}) dentro do conjunto."),
           CODE("Guarde em distancias a distância 430 entre São Paulo e Rio usando um frozenset como chave. Depois mostre a distância buscando com as cidades na ordem inversa (Rio, São Paulo).",
                'distancias = {}\ndistancias[("São Paulo", "Rio")] = 430\nprint(distancias[("Rio", "São Paulo")])\n',
                'distancias = {}\ndistancias[frozenset(["São Paulo", "Rio"])] = 430\nprint(distancias[frozenset(["Rio", "São Paulo"])])',
                'assert frozenset(["Rio", "São Paulo"]) in distancias, "A chave deve ser frozenset([\'São Paulo\', \'Rio\'])"\nassert __stdout__.strip() == "430", "Deve mostrar 430"',
                "Com tupla a ordem importa; com frozenset, não.")]),
        # lição 4
        L("Cuidados com frozenset",
          "frozenset não tem add, remove nem discard. Para \"mudar\", crie outro com | ou -. Como o set, ele separa as letras de um texto e não aceita um número sozinho.",
          'f = frozenset([1])\ntry:\n    f.add(2)\nexcept AttributeError as e:\n    print(type(e).__name__)\nf = f | {2}\nprint(sorted(f))',
          [OUT('f = frozenset("ovo")\nprint(len(f))', ["3", "1", "Erro"], "As letras diferentes são o e v."),
           OUT('try:\n    frozenset(10)\n    print("ok")\nexcept TypeError:\n    print("erro de tipo")', ["ok", "frozenset({10})", "10"], "Um número sozinho não pode ser percorrido."),
           MC("Como \"adicionar\" um item a um frozenset f?", "Criar outro: f = f | {item}", ["f.add(item)", "f.append(item)", "f[item] = True"],
              "O original não muda; a variável passa a apontar para um novo."),
           TYPE('a = frozenset([1, 2])\nb = a\na = a | {3}\nprint(len(b))', "a virou um frozenset novo; b continua com o antigo.")]),
        # lição 5
        L("frozenset com outras funções",
          "sorted, len e in funcionam normalmente. <= pergunta se um conjunto está todo dentro do outro. E set(f) cria uma cópia que pode mudar.",
          'base = frozenset(["sal", "óleo"])\nreceita = {"sal", "óleo", "ovo"}\nprint(base <= receita)\nprint(sorted(receita - base))\nmutavel = set(base)\nmutavel.add("alho")\nprint(sorted(mutavel))',
          [TYPE('print(frozenset([1, 2]) <= {1, 2, 3})', "1 e 2 estão no outro conjunto."),
           OUT('f = frozenset([3, 1, 2])\nprint(sorted(f))', ["frozenset({1, 2, 3})", "(1, 2, 3)", "[3, 1, 2]"], "sorted sempre devolve uma lista ordenada."),
           MC("Como ter uma versão de f que aceita add?", "set(f)", ["list(f)", "frozenset(f)", "tuple(f)"], "set(f) é um conjunto normal com os mesmos itens."),
           CODE("Usando a constante VOGAIS, crie a função conta_vogais(texto) que devolve quantas letras do texto são vogais (maiúsculas também contam).",
                'VOGAIS = frozenset("aeiou")\n\ndef conta_vogais(texto):\n    return 0\n',
                'VOGAIS = frozenset("aeiou")\n\ndef conta_vogais(texto):\n    total = 0\n    for letra in texto.lower():\n        if letra in VOGAIS:\n            total += 1\n    return total',
                'assert conta_vogais("banana") == 3, "banana tem 3 vogais"\nassert conta_vogais("PIPO") == 2, "Maiúsculas também contam: PIPO tem 2 vogais"\nassert conta_vogais("xyz") == 0, "xyz não tem vogais"',
                "Percorra texto.lower() e some 1 quando a letra estiver em VOGAIS.")]),
        # lição 6
        L("Desafio: times",
          "frozenset é ideal para grupos fixos: dá para comparar se dois grupos têm as mesmas pessoas, sem ligar para ordem nem repetidos.",
          'turma_a = frozenset(["Ana", "Bia", "Caio"])\nturma_b = frozenset(["Bia", "Davi"])\nprint(sorted(turma_a & turma_b))\nprint(len(turma_a | turma_b))',
          [OUT('a = frozenset([1, 2, 3])\nb = frozenset([2, 3, 4])\nprint(sorted(a ^ b))', ["[2, 3]", "[1, 2, 3, 4]", "[]"], "^ fica com o que está em só um dos dois."),
           TYPE('grupos = {frozenset([1, 2]): "A", frozenset([3]): "B"}\nprint(grupos[frozenset([2, 1])] + grupos[frozenset([3])])', "\"A\" + \"B\"."),
           ORDER("Monte o programa: cria o conjunto fixo, faz uma cópia que muda, adiciona o 3 e mostra.",
                 ['fixo = frozenset([1, 2])', 'copia = set(fixo)', 'copia.add(3)', 'print(sorted(copia))'],
                 "Só a cópia (set) aceita add."),
           CODE("Crie a função mesmo_time(a, b) que recebe duas listas de jogadores e devolve True se tiverem os mesmos jogadores, sem ligar para ordem nem repetidos.",
                "def mesmo_time(a, b):\n    return a == b\n",
                "def mesmo_time(a, b):\n    return frozenset(a) == frozenset(b)",
                'assert mesmo_time(["Ana", "Bia"], ["Bia", "Ana"]) is True, "A ordem não importa"\nassert mesmo_time(["Ana"], ["Ana", "Caio"]) is False, "Times diferentes devem dar False"\nassert mesmo_time(["Ana", "Ana"], ["Ana"]) is True, "Repetidos não importam"',
                "return frozenset(a) == frozenset(b)")]),
    ],

    # ================================================================ range
    "range": [
        # lição 2
        L("Pulando e voltando",
          "Com passo negativo o range conta para trás, e o fim continua de fora. Se o início já passou do fim na direção do passo, o range fica vazio, sem erro.",
          'print(list(range(10, 0, -3)))\nprint(list(range(5, 2)))\nprint(list(range(-3, 3, 2)))',
          [OUT('print(list(range(5, 1)))', ["[5, 4, 3, 2]", "[1, 2, 3, 4, 5]", "Erro"], "Sem passo negativo ele só sobe; de 5 até 1 subindo não tem nada."),
           TYPE('print(list(range(20, 0, -5)))', "Desce de 5 em 5; o 0 não entra."),
           MC("Quantos números há em range(2, 12, 2)?", "5", ["6", "10", "12"], "São 2, 4, 6, 8 e 10."),
           FILL("Complete para gerar 1, 4, 7.", 'print(list(range(1, 10, ___)))', "3", ["4", "2", "7"], "De 3 em 3: 1, 4, 7 (10 não entra).")]),
        # lição 3
        L("range nos laços",
          "O uso mais comum do range é no for: repetir algo N vezes ou percorrer as posições de uma lista com range(len(lista)).",
          'frutas = ["uva", "kiwi", "pera"]\nfor i in range(len(frutas)):\n    print(i, frutas[i])',
          [OUT('for i in range(3):\n    print("*" * (i + 1))', ["***\n***\n***", "*\n*\n*", "*\n**"], "i vale 0, 1 e 2, então 1, 2 e 3 estrelas."),
           TYPE('total = 0\nfor n in range(1, 5):\n    total += n\nprint(total)', "1 + 2 + 3 + 4."),
           MC("Para repetir algo 5 vezes, o mais comum é…", "for _ in range(5):", ["for _ in range(1, 5):", "for _ in 5:", "while range(5):"],
              "range(5) tem 5 números (0 a 4). range(1, 5) teria só 4."),
           CODE("Mostre a contagem regressiva de 5 até 1, um número por linha, e depois a palavra Já!",
                'for n in range(1, 6):\n    print(n)\nprint("Já!")\n',
                'for n in range(5, 0, -1):\n    print(n)\nprint("Já!")',
                'assert __stdout__.strip().splitlines() == ["5", "4", "3", "2", "1", "Já!"], "Esperado: 5, 4, 3, 2, 1 e Já!, um por linha"',
                "range(5, 0, -1) conta de 5 até 1.")]),
        # lição 4
        L("Pegadinhas do range",
          "print(range(3)) não mostra os números: mostra range(0, 3). Para ver, use list(). O range só aceita inteiros, e passo 0 dá ValueError.",
          'r = range(3)\nprint(r)\nprint(list(r))\ntry:\n    range(1.5)\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('print(range(4))', ["[0, 1, 2, 3]", "0 1 2 3", "range(4)"], "O print mostra o próprio range, com início e fim."),
           OUT('try:\n    print(list(range(1, 5, 0)))\nexcept ValueError:\n    print("passo zero")', ["[1, 2, 3, 4]", "[]", "Laço infinito"], "Passo 0 nunca chegaria ao fim, então o Python não deixa."),
           MC("Para ter os números de 1 a 10 (incluindo o 10), use…", "range(1, 11)", ["range(1, 10)", "range(10)", "range(0, 10)"], "O fim não entra, então use 11."),
           TYPE('print(len(range(0, 10, 3)))', "São 0, 3, 6 e 9.")]),
        # lição 5
        L("range com outras funções",
          "Um range se comporta como uma lista que não muda: aceita len, in, índice e fatia. E sum, max e reversed funcionam direto nele.",
          'r = range(0, 100, 5)\nprint(len(r))\nprint(35 in r, 36 in r)\nprint(r[3])\nprint(list(reversed(range(3))))',
          [TYPE('print(range(10, 50, 10)[-1])', "Os números são 10, 20, 30 e 40; o último é 40."),
           OUT('print(7 in range(0, 10, 2))', ["True", "7", "Erro"], "Só os pares estão nesse range."),
           OUT('print(list(range(10))[::3])', ["[0, 3, 6]", "[3, 6, 9]", "[0, 1, 2]"], "A fatia pega de 3 em 3, a partir do 0."),
           CODE("Guarde em soma_impares a soma de todos os números ímpares de 1 a 99 (incluindo o 99), usando sum e range.",
                'soma_impares = sum(range(1, 99))\nprint(soma_impares)\n',
                'soma_impares = sum(range(1, 100, 2))\nprint(soma_impares)',
                'assert soma_impares == 2500, "A soma dos ímpares de 1 a 99 é 2500"',
                "range(1, 100, 2) dá 1, 3, 5, …, 99.")]),
        # lição 6
        L("Desafio: desenhos com range",
          "Um range dentro de outro desenha grades: o de fora cuida das linhas e o de dentro, das colunas. Assim dá para fazer tabuleiros, escadas e tabelas.",
          'for linha in range(3):\n    casas = ""\n    for coluna in range(4):\n        casas += "#" if (linha + coluna) % 2 == 0 else "."\n    print(casas)',
          [OUT('for i in range(2):\n    for j in range(2):\n        print(i, j)', ["0 0\n1 1", "0 1\n1 0", "0 0\n0 1"], "Para cada i, o j passa por 0 e 1: são 4 linhas."),
           TYPE('quadrados = []\nfor n in range(1, 5):\n    quadrados.append(n * n)\nprint(quadrados)', "1, 4, 9 e 16."),
           ORDER("Monte o programa que mostra os múltiplos de 3 até 12 numa linha.",
                 ['for n in range(3, 13, 3):', '    print(n, end=" ")', 'print()'],
                 "range(3, 13, 3) dá 3, 6, 9 e 12."),
           CODE("Crie a função escada(n) que MOSTRA n linhas: a linha 1 tem 1 #, a linha 2 tem 2 #, e assim até n.",
                'def escada(n):\n    for i in range(n):\n        print("#" * i)\n\nescada(3)\n',
                'def escada(n):\n    for i in range(1, n + 1):\n        print("#" * i)\n\nescada(3)',
                'assert __stdout__.splitlines() == ["#", "##", "###"], "escada(3) deve mostrar #, ## e ###"',
                "range(n) começa no 0; use range(1, n + 1).")]),
    ],
}

BUGS = r'''
@fn_list 2
precos = [10, 20]
copia = precos
copia.append(30)
print(precos)  # esperado: [10, 20]
>>> copia = list(precos)
!! copia = precos não copia nada. Use list(precos).

@fn_list 2
idade = 25
digitos = list(idade)
print(digitos)
>>> digitos = list(str(idade))
!! Número não se percorre. Converta para texto antes.

@fn_list 1
list = ["a", "b"]
print(list("oi"))
>>> letras = ["a", "b"]
!! A variável list escondeu a função list().

@fn_list 2
numeros = map(int, "321")
print(numeros[0])
>>> print(list(numeros)[0])
!! map não aceita índice. Transforme em lista antes.

@fn_list 1
nomes = list("Ana", "Bia")
print(nomes)
>>> nomes = list(("Ana", "Bia"))
!! list() recebe UMA coleção, não vários valores.

@fn_list 2
texto = "olá mundo"
palavras = list(texto)
print(len(palavras))  # esperado: 2
>>> palavras = texto.split()
!! list() separa letras. Para palavras, use split().

@fn_tuple 2
cores = ("azul", "verde")
cores[0] = "rosa"
print(cores)
>>> cores = ("rosa", "verde")
!! Tuplas não mudam. Crie uma tupla nova.

@fn_tuple 1
t = ("sozinho")
print(len(t))  # esperado: 1
>>> t = ("sozinho",)
!! Sem vírgula é só um texto. Tupla de um item precisa de vírgula.

@fn_tuple 2
ponto = (4, 7)
x, y, z = ponto
print(x + y)
>>> x, y = ponto
!! A tupla tem 2 itens, então são 2 variáveis.

@fn_tuple 2
dados = ("Ana", 30)
dados.append("SP")
print(dados)
>>> dados = dados + ("SP",)
!! Tupla não tem append. Junte com + numa tupla nova.

@fn_tuple 3
def extremos(n):
    return min(n), max(n)
menor = extremos([5, 2, 9])
print(menor)  # esperado: 2
>>> menor, maior = extremos([5, 2, 9])
!! A função devolve uma tupla. Desempacote em duas variáveis.

@fn_tuple 1
t = tuple(1, 2, 3)
print(t)
>>> t = tuple([1, 2, 3])
!! tuple() recebe UMA coleção, não vários números.

@fn_dict 2
idades = {"Ana": 20, "Bia": 22}
print(idades["Caio"])
>>> print(idades.get("Caio", 0))
!! Caio não é chave. Use get com um valor padrão.

@fn_dict 1
aluno = dict(nome completo="Ana Lima")
print(aluno)
>>> aluno = dict(nome_completo="Ana Lima")
!! Com chave=valor, a chave não pode ter espaço.

@fn_dict 4
precos = {"pão": 3, "leite": 5}
total = 0
for item in precos:
    total += item
print(total)
>>> total += precos[item]
!! O for dá as chaves. O preço é precos[item].

@fn_dict 3
contagem = dict()
for letra in "aba":
    contagem[letra] += 1
print(contagem)
>>> contagem[letra] = contagem.get(letra, 0) + 1
!! A chave ainda não existe. Comece do 0 com get.

@fn_dict 1
mapa = {[0, 0]: "início"}
print(mapa)
>>> mapa = {(0, 0): "início"}
!! Lista não pode ser chave. Use uma tupla.

@fn_dict 2
notas = {"Ana": 9, "Bia": 7}
melhor = max(notas)
print(melhor)  # esperado: Ana
>>> melhor = max(notas, key=notas.get)
!! max(notas) compara os nomes. Use key=notas.get para comparar as notas.

@fn_set 1
vazio = {}
vazio.add(5)
print(vazio)
>>> vazio = set()
!! {} é dicionário vazio. Conjunto vazio é set().

@fn_set 2
cores = {"azul", "rosa"}
print(cores[0])
>>> print(sorted(cores)[0])
!! Conjunto não tem índice. Ordene antes com sorted.

@fn_set 1
nomes = set("Ana")
nomes.add("Bia")
print(len(nomes))  # esperado: 2
>>> nomes = {"Ana"}
!! set("Ana") separa as letras. Use {"Ana"}.

@fn_set 3
a = {1, 2}
b = {2, 3}
print(sorted(a + b))
>>> print(sorted(a | b))
!! Conjuntos não somam com +. A união é |.

@fn_set 2
pares = set()
pares.add([1, 2])
print(len(pares))
>>> pares.add((1, 2))
!! Lista não pode entrar num set. Use tupla.

@fn_set 2
itens = {"pão", "leite"}
itens.remove("ovo")
print(len(itens))
>>> itens.discard("ovo")
!! remove dá erro se o item não existe. discard não.

@fn_frozenset 2
dias = frozenset(["seg", "ter"])
dias.add("qua")
print(len(dias))
>>> dias = dias | {"qua"}
!! frozenset não tem add. Crie outro com |.

@fn_frozenset 1
mapa = {{"Ana", "Bia"}: "dupla"}
print(len(mapa))
>>> mapa = {frozenset(["Ana", "Bia"]): "dupla"}
!! set não pode ser chave. frozenset pode.

@fn_frozenset 1
tags = frozenset("python")
print(len(tags))  # esperado: 1
>>> tags = frozenset(["python"])
!! Um texto sozinho vira letras. Coloque-o numa lista.

@fn_frozenset 2
f = frozenset([3, 1, 2])
print(f[0])
>>> print(sorted(f)[0])
!! frozenset não tem índice. Ordene com sorted.

@fn_frozenset 1
pares = frozenset(1, 2)
print(sorted(pares))
>>> pares = frozenset([1, 2])
!! frozenset() recebe UMA coleção, não vários números.

@fn_frozenset 3
a = frozenset(["Ana", "Bia"])
b = frozenset(["Bia", "Caio"])
print(sorted(a | b))  # esperado: ['Bia']
>>> print(sorted(a & b))  # esperado: ['Bia']
!! Quem está nos dois é a interseção &, não a união |.

@fn_frozenset 2
f = frozenset([1, 2])
f.remove(1)
print(sorted(f))
>>> f = f - {1}
!! frozenset não muda. Crie outro com -.

@fn_range 1
for n in range(1, 10):
    print(n)  # esperado: 10
>>> for n in range(1, 11):
!! O fim não entra. Para chegar ao 10, use 11.

@fn_range 1
for i in range(5.0):
    print(i)
>>> for i in range(5):
!! range só aceita números inteiros.

@fn_range 1
for n in range(10, 0):
    print(n)  # esperado: 1
>>> for n in range(10, 0, -1):
!! Para contar para trás, o passo precisa ser -1.

@fn_range 2
nomes = ["Ana", "Bia"]
for i in range(nomes):
    print(nomes[i])
>>> for i in range(len(nomes)):
!! range precisa de um número. Use len(nomes).

@fn_range 2
numeros = range(5)
numeros.append(5)
print(list(numeros))
>>> numeros = list(range(5))
!! range não muda. Transforme em lista para usar append.

@fn_range 1
pares = range(0, 10, 0)
print(list(pares))
>>> pares = range(0, 10, 2)
!! Passo 0 não existe. Para os pares, o passo é 2.

@fn_range 2
total = 0
for n in range(5):
    total += n
print(total)  # esperado: 15
>>> for n in range(1, 6):
!! range(5) vai de 0 a 4. Para somar de 1 a 5, use range(1, 6).
'''
