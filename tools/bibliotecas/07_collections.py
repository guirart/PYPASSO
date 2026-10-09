from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_collections", titulo="collections",
               descricao="Estruturas extras: contar, agrupar, filas e tuplas com nomes.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Contando com Counter",
      "O módulo collections já vem com o Python e traz estruturas de dados extras, prontas para tarefas do dia a dia. A primeira é o Counter: você passa uma lista (ou um texto) e ele conta quantas vezes cada item aparece. O método most_common(n) devolve os n itens mais frequentes, como numa votação.",
      """from collections import Counter
votos = ["pizza", "sushi", "pizza", "taco", "pizza", "sushi"]
contagem = Counter(votos)
print(contagem)
print(contagem["pizza"])
print(contagem.most_common(1))""",
      [OUT('from collections import Counter\nc = Counter("banana")\nprint(c["a"])',
           ["2", "6", "{'a': 3}"],
           "Counter conta cada letra do texto: banana tem três letras a."),
       TYPE('from collections import Counter\npets = Counter(["gato", "cão", "gato"])\nprint(pets["peixe"])',
            "Um item que não apareceu vale 0 no Counter, sem dar KeyError."),
       MC("O que contagem.most_common(2) devolve?",
          "Uma lista com os 2 pares (item, quantidade) mais frequentes",
          ["Os 2 itens que aparecem menos vezes", "Um dicionário só com 2 chaves", "O número 2"],
          "most_common devolve uma lista de tuplas, do mais frequente para o menos frequente."),
       CODE("Crie a função mais_vendido(vendas) que recebe uma lista de produtos vendidos e devolve o produto que mais aparece. Use Counter.",
            "from collections import Counter\n\ndef mais_vendido(vendas):\n    pass\n",
            "from collections import Counter\n\ndef mais_vendido(vendas):\n    return Counter(vendas).most_common(1)[0][0]",
            'assert mais_vendido(["café", "pão", "café"]) == "café", "Em [café, pão, café] o mais vendido é café"\n'
            'assert mais_vendido(["bolo", "suco", "suco", "suco"]) == "suco", "Em [bolo, suco, suco, suco] o mais vendido é suco"',
            "most_common(1) devolve [(produto, quantidade)]; [0][0] pega só o nome do produto.")]),
    # lição 2
    L("defaultdict: agrupar sem KeyError",
      "Num dicionário comum, mexer numa chave que não existe dá KeyError. O defaultdict cria a chave sozinho com um valor inicial: defaultdict(list) começa com lista vazia e defaultdict(int) começa com 0. É perfeito para agrupar coisas, como alunos por sala.",
      """from collections import defaultdict
turma = [("Ana", "A"), ("Caio", "B"), ("Bia", "A")]
salas = defaultdict(list)
for nome, sala in turma:
    salas[sala].append(nome)
print(dict(salas))""",
      [OUT('from collections import defaultdict\nd = defaultdict(int)\nd["x"] += 1\nd["x"] += 1\nprint(d["x"], d["y"])',
           ["2 None", "1 0", "KeyError"],
           "defaultdict(int) começa cada chave nova em 0: x foi somado duas vezes e y vale 0."),
       FILL("Complete para agrupar as palavras pela primeira letra.",
            'from collections import defaultdict\ngrupos = defaultdict(___)\nfor p in ["sol", "sal", "mar"]:\n    grupos[p[0]].append(p)\nprint(dict(grupos))',
            "list", ["int", "[]", "str"],
            "Para usar append, cada chave nova precisa começar como lista vazia. Passe o nome list, sem parênteses."),
       MC("Por que defaultdict(list) evita o KeyError?",
          "Porque cria a chave que falta com uma lista vazia",
          ["Porque ignora as chaves que não existem", "Porque transforma o erro em None", "Porque já vem com todas as chaves possíveis"],
          "Quando você acessa uma chave nova, ele chama list() e guarda o resultado nessa chave."),
       CODE("Crie a função agrupar_por_tamanho(palavras) que devolve um dicionário {tamanho: [palavras com esse tamanho]}, na ordem em que aparecem.",
            "from collections import defaultdict\n\ndef agrupar_por_tamanho(palavras):\n    pass\n",
            "from collections import defaultdict\n\ndef agrupar_por_tamanho(palavras):\n    grupos = defaultdict(list)\n    for p in palavras:\n        grupos[len(p)].append(p)\n    return grupos",
            'r = agrupar_por_tamanho(["oi", "sol", "ar", "mar"])\n'
            'assert r is not None, "A função precisa devolver o dicionário com return"\n'
            'assert dict(r) == {2: ["oi", "ar"], 3: ["sol", "mar"]}, "Esperado: {2: [\'oi\', \'ar\'], 3: [\'sol\', \'mar\']}"',
            "grupos[len(p)].append(p) funciona mesmo na primeira vez, porque o defaultdict cria a lista vazia.")]),
    # lição 3
    L("namedtuple: tuplas com nomes",
      "Uma namedtuple é uma tupla em que cada posição tem um nome. Em vez de lembrar que p[0] é o x, você escreve p.x. Ela continua sendo tupla: não dá para alterar os valores depois de criada.",
      """from collections import namedtuple
Ponto = namedtuple("Ponto", ["x", "y"])
p = Ponto(3, 4)
print(p.x, p.y)
print(p)""",
      [OUT('from collections import namedtuple\nProduto = namedtuple("Produto", "nome preco")\nitem = Produto("caneta", 2.5)\nprint(item.preco)',
           ["caneta", "preco", "('caneta', 2.5)"],
           "Os nomes podem vir num texto separado por espaços; item.preco é o segundo valor."),
       TYPE('from collections import namedtuple\nProduto = namedtuple("Produto", "nome preco")\nitem = Produto("caderno", 15)\nprint(item[0])',
            "Ela ainda é uma tupla, então a posição 0 também funciona."),
       MC("O que acontece com p.x = 10, se p é uma namedtuple?",
          "Dá erro, porque namedtuple não pode ser alterada",
          ["O x passa a valer 10", "Cria um novo campo chamado x", "Nada acontece"],
          "Como toda tupla, ela é imutável. Para um valor novo, crie outra: p._replace(x=10)."),
       ORDER("Monte o programa que cria um pet e mostra o nome dele.",
             ["from collections import namedtuple",
              'Pet = namedtuple("Pet", "nome especie")',
              'rex = Pet("Rex", "cachorro")',
              "print(rex.nome)"],
             "Primeiro importa, depois define o molde, cria o pet e só então usa os campos.")]),
    # lição 4
    L("deque: filas e pilhas",
      "A deque é uma lista feita para entrar e sair pelas duas pontas bem rápido: append e pop no fim, appendleft e popleft no começo. Serve para filas de atendimento (entra no fim, sai do começo). Com maxlen ela guarda só os últimos itens, como um histórico.",
      """from collections import deque
fila = deque(["Ana", "Caio"])
fila.append("Bia")
primeiro = fila.popleft()
print(primeiro)
print(fila)
ultimas = deque(maxlen=3)
for musica in ["A", "B", "C", "D"]:
    ultimas.append(musica)
print(ultimas)""",
      [OUT('from collections import deque\nd = deque([1, 2, 3])\nd.appendleft(0)\nd.pop()\nprint(list(d))',
           ["[1, 2, 3]", "[0, 1, 2, 3]", "[1, 2]"],
           "appendleft põe o 0 no começo e pop tira do fim (o 3)."),
       TYPE('from collections import deque\nhist = deque(maxlen=2)\nfor pagina in ["a", "b", "c"]:\n    hist.append(pagina)\nprint(list(hist))',
            "Com maxlen=2, quando entra o c o item mais antigo (a) sai."),
       MC("Numa fila de banco, quem chegou primeiro é atendido primeiro. Qual método tira o próximo da fila?",
          "popleft()", ["pop()", "appendleft()", "remove()"],
          "Os clientes entram no fim com append e saem do começo com popleft."),
       CODE("Crie a função atender(fila) que tira o primeiro cliente da deque e devolve o texto Atendendo: <nome>.",
            "from collections import deque\n\ndef atender(fila):\n    pass\n",
            'from collections import deque\n\ndef atender(fila):\n    nome = fila.popleft()\n    return f"Atendendo: {nome}"',
            'f = deque(["Ana", "Bia"])\n'
            'assert atender(f) == "Atendendo: Ana", "O primeiro da fila é a Ana: Atendendo: Ana"\n'
            'assert list(f) == ["Bia"], "A Ana precisa sair da fila, sobrando só a Bia"',
            "popleft remove e devolve o primeiro da fila.")]),
    # lição 5
    L("OrderedDict e ChainMap",
      "O ChainMap junta vários dicionários e procura a chave em ordem: ótimo para configurações do usuário por cima das configurações padrão. O dict comum já guarda a ordem de inserção, mas o OrderedDict tem extras como move_to_end, que leva uma chave para o fim (ou para o começo, com last=False).",
      """from collections import OrderedDict, ChainMap
padrao = {"tema": "claro", "som": True}
usuario = {"tema": "escuro"}
config = ChainMap(usuario, padrao)
print(config["tema"], config["som"])
tarefas = OrderedDict(lavar=1, estudar=2, jogar=3)
tarefas.move_to_end("lavar")
print(list(tarefas))""",
      [OUT('from collections import ChainMap\nc = ChainMap({"a": 1}, {"a": 2, "b": 3})\nprint(c["a"], c["b"])',
           ["2 3", "1 None", "[1, 2] 3"],
           "O a é encontrado primeiro no primeiro dicionário; o b só existe no segundo."),
       TYPE('from collections import OrderedDict\nod = OrderedDict()\nod["b"] = 1\nod["a"] = 2\nod.move_to_end("b")\nprint(list(od))',
            "move_to_end leva o b para o fim, então a ordem fica a, b."),
       FILL("Complete para levar a tarefa urgente para o COMEÇO.",
            'from collections import OrderedDict\nt = OrderedDict(ler=1, urgente=2)\nt.move_to_end("urgente", last=___)\nprint(list(t))',
            "False", ["True", "first", "-1"],
            "last=False move para o começo; o padrão (True) move para o fim."),
       MC("Hoje em dia, um dict comum guarda a ordem em que as chaves entraram?",
          "Sim, desde o Python 3.7",
          ["Não, só o OrderedDict guarda", "Só se as chaves forem números", "Só se você ordenar antes"],
          "O dict comum já mantém a ordem; o OrderedDict continua útil pelos extras, como move_to_end.")]),
    # lição 6
    L("Desafio: placar do campeonato",
      "Juntando tudo: namedtuple organiza os dados, Counter conta e defaultdict agrupa. Counters também podem ser somados: as contagens de cada item se juntam.",
      """from collections import Counter, defaultdict, namedtuple
Jogo = namedtuple("Jogo", "vencedor perdedor")
jogos = [Jogo("Leões", "Tigres"), Jogo("Leões", "Águias"), Jogo("Águias", "Tigres")]
vitorias = Counter(j.vencedor for j in jogos)
derrotas = defaultdict(list)
for j in jogos:
    derrotas[j.perdedor].append(j.vencedor)
print(vitorias.most_common(1))
print(dict(derrotas))""",
      [OUT('from collections import Counter\nsegunda = Counter(maçã=2)\nterca = Counter(maçã=1, uva=3)\nprint(segunda + terca)',
           ["Counter({'maçã': 2, 'uva': 3})", "Counter({'uva': 3, 'maçã': 1})", "TypeError"],
           "Somar Counters soma as contagens: maçã fica 2 + 1 = 3 e uva fica 3."),
       MC("Você quer guardar só as 5 últimas buscas do usuário. Qual estrutura usar?",
          "deque(maxlen=5)", ["Counter()", "namedtuple", "ChainMap"],
          "Com maxlen, a deque descarta sozinha os itens mais antigos."),
       TYPE('from collections import defaultdict\nnotas = defaultdict(list)\nnotas["Ana"].append(8)\nnotas["Ana"].append(10)\nprint(sum(notas["Ana"]) / len(notas["Ana"]))',
            "A Ana tem as notas 8 e 10, e a média é 9.0."),
       CODE("Crie a função analisar(pedidos) que recebe uma lista de tuplas (mesa, prato) e devolve DUAS coisas: o prato mais pedido e um dicionário {mesa: [pratos]}.",
            "from collections import Counter, defaultdict\n\ndef analisar(pedidos):\n    pass\n",
            "from collections import Counter, defaultdict\n\ndef analisar(pedidos):\n    contagem = Counter(prato for mesa, prato in pedidos)\n    mesas = defaultdict(list)\n    for mesa, prato in pedidos:\n        mesas[mesa].append(prato)\n    return contagem.most_common(1)[0][0], mesas",
            'r = analisar([(1, "pizza"), (2, "lasanha"), (1, "suco"), (3, "pizza")])\n'
            'assert r is not None, "Devolva as duas coisas: return prato, mesas"\n'
            'top, mesas = r\n'
            'assert top == "pizza", "O prato mais pedido é pizza"\n'
            'assert dict(mesas) == {1: ["pizza", "suco"], 2: ["lasanha"], 3: ["pizza"]}, "A mesa 1 pediu pizza e suco, a 2 lasanha e a 3 pizza"',
            "Counter acha o prato campeão e defaultdict(list) agrupa os pratos por mesa.")]),
]

BUGS = r'''
@lib_collections 3
from collections import Counter
frutas = Counter(["uva", "maçã", "uva"])
print(frutas.most_comon(1))
>>> print(frutas.most_common(1))
!! O método se chama most_common, com dois m.

@lib_collections 2
from collections import defaultdict
grupos = {}
for nome in ["Ana", "Alice", "Bruno"]:
    grupos[nome[0]].append(nome)
print(dict(grupos))
>>> grupos = defaultdict(list)
!! Num dict comum a chave "A" ainda não existe. defaultdict(list) cria a lista vazia sozinho.

@lib_collections 2
from collections import defaultdict
contagem = defaultdict(int())
contagem["gol"] += 1
print(contagem["gol"])
>>> contagem = defaultdict(int)
!! Passe o nome int, sem parênteses: o defaultdict é que vai chamar int() quando precisar.

@lib_collections 4
from collections import namedtuple
Aluno = namedtuple("Aluno", "nome nota")
a = Aluno("Bia", 7)
a.nota = 9
print(a.nota)
>>> a = a._replace(nota=9)
!! namedtuple não pode ser alterada. _replace cria uma cópia com o valor novo.

@lib_collections 3
from collections import deque
fila = deque(["Ana", "Caio", "Bia"])
atendido = fila.pop()
print(atendido)  # esperado: Ana
>>> atendido = fila.popleft()
!! pop tira do fim. Numa fila, quem sai primeiro é quem está no começo: popleft.

@lib_collections 3
from collections import Counter
votos = Counter(["sim", "não", "sim"])
vencedor = votos.most_common(1)
print(vencedor)  # esperado: sim
>>> vencedor = votos.most_common(1)[0][0]
!! most_common devolve uma lista de tuplas, como [('sim', 2)]. Use [0][0] para pegar só o item.
'''
