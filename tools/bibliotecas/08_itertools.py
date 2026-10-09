from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_itertools", titulo="itertools",
               descricao="Ferramentas para laços: repetir, juntar, combinar e agrupar.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Iteradores infinitos com islice",
      "O módulo itertools já vem com o Python e traz ferramentas para trabalhar com sequências em laços. count conta sem parar, cycle repete uma lista em rodízio e repeat repete um valor: count e cycle NUNCA acabam sozinhos! Para pegar só os primeiros itens com segurança, use islice(iterador, n).",
      """from itertools import count, cycle, repeat, islice
print(list(islice(count(10), 3)))
print(list(islice(cycle(["vermelho", "verde"]), 4)))
print(list(repeat("oi", 3)))""",
      [OUT("from itertools import count, islice\nprint(list(islice(count(0, 5), 4)))",
           ["[0, 1, 2, 3]", "[5, 10, 15, 20]", "[0, 5, 10, 15, 20]"],
           "count(0, 5) começa no 0 e anda de 5 em 5; islice pega só os 4 primeiros."),
       TYPE('from itertools import cycle, islice\nprint(list(islice(cycle("AB"), 5)))',
            "cycle repete A, B, A, B... e islice para no quinto item."),
       MC("O que acontece ao rodar list(count())?",
          "O programa nunca termina, porque count não acaba",
          ["Cria uma lista vazia", "Cria a lista [0, 1, 2, ..., 9]", "Dá erro na hora"],
          "count é infinito: list tentaria guardar números para sempre. Use islice para limitar."),
       CODE("Crie a função primeiros_pares(n) que devolve uma lista com os n primeiros números pares, começando do 0. Use count e islice.",
            "from itertools import count, islice\n\ndef primeiros_pares(n):\n    pass\n",
            "from itertools import count, islice\n\ndef primeiros_pares(n):\n    return list(islice(count(0, 2), n))",
            'assert primeiros_pares(4) == [0, 2, 4, 6], "primeiros_pares(4) deve ser [0, 2, 4, 6]"\n'
            'assert primeiros_pares(1) == [0], "primeiros_pares(1) deve ser [0]"',
            "count(0, 2) gera 0, 2, 4...; islice pega os n primeiros e list transforma em lista.")]),
    # lição 2
    L("chain: uma sequência após a outra",
      "chain percorre várias sequências em seguida, como se fossem uma só, sem criar uma lista nova no meio do caminho. Funciona com listas, tuplas, textos... Se você tem uma lista de listas, use chain.from_iterable para achatá-la.",
      """from itertools import chain
manha = ["café", "pão"]
tarde = ["suco"]
noite = ["sopa", "chá"]
print(list(chain(manha, tarde, noite)))
turmas = [[1, 2], [3], [4, 5]]
print(list(chain.from_iterable(turmas)))""",
      [OUT('from itertools import chain\nprint(list(chain("ab", [1, 2])))',
           ["['ab', 1, 2]", "['a', 'b', [1, 2]]", "TypeError"],
           "chain percorre cada sequência item por item: o texto vira as letras a e b."),
       TYPE("from itertools import chain\nprint(sum(chain([1, 2], [3], (4,))))",
            "chain passa por 1, 2, 3 e 4, e sum soma tudo."),
       FILL("Complete para juntar todos os alunos das turmas numa lista só.",
            'from itertools import chain\nturmas = [["Ana", "Bia"], ["Caio"]]\nprint(list(chain.___(turmas)))',
            "from_iterable", ["join", "all", "flat"],
            "chain.from_iterable recebe UMA lista que contém outras listas e passa por todas."),
       MC("Qual a vantagem de chain(a, b) em relação a a + b?",
          "Funciona com tipos diferentes e não monta uma lista nova na memória",
          ["Ordena os itens automaticamente", "Remove os itens repetidos", "Só funciona com números"],
          "a + b exige tipos iguais e cria uma lista nova; chain só passa por um e depois pelo outro.")]),
    # lição 3
    L("product, permutations, combinations",
      "product faz todas as combinações entre listas, como montar camisetas com cada tamanho e cada cor. permutations(lista, n) cria arranjos em que a ordem importa (ouro e prata num pódio). combinations(lista, n) cria grupos em que a ordem NÃO importa (duplas para um trabalho).",
      """from itertools import product, permutations, combinations
tamanhos = ["P", "G"]
cores = ["azul", "preto"]
print(list(product(tamanhos, cores)))
print(list(permutations("ABC", 2)))
print(list(combinations("ABC", 2)))""",
      [OUT('from itertools import product\nprint(len(list(product("ab", "xyz"))))',
           ["5", "9", "2"],
           "Cada uma das 2 letras combina com cada uma das 3: 2 x 3 = 6 pares."),
       TYPE('from itertools import combinations\ntime = ["Ana", "Bia", "Caio", "Teo"]\nprint(len(list(combinations(time, 2))))',
            "Com 4 pessoas dá para formar 6 duplas diferentes."),
       MC("Numa corrida com 5 pessoas, você quer listar todos os pódios possíveis de ouro e prata. Qual usar?",
          "permutations(corredores, 2)",
          ["combinations(corredores, 2)", "product(corredores)", "chain(corredores)"],
          "No pódio a ordem importa: Ana ouro e Bia prata é diferente de Bia ouro e Ana prata."),
       CODE("Crie a função duplas(pessoas) que devolve uma lista com todas as duplas possíveis (tuplas), sem importar a ordem.",
            "from itertools import combinations\n\ndef duplas(pessoas):\n    pass\n",
            "from itertools import combinations\n\ndef duplas(pessoas):\n    return list(combinations(pessoas, 2))",
            'assert duplas(["Ana", "Bia", "Caio"]) == [("Ana", "Bia"), ("Ana", "Caio"), ("Bia", "Caio")], "Para Ana, Bia e Caio são 3 duplas"\n'
            'assert len(duplas(["a", "b", "c", "d"])) == 6, "Com 4 pessoas são 6 duplas"',
            "combinations(pessoas, 2) gera os grupos de 2; list transforma em lista.")]),
    # lição 4
    L("groupby: agrupar vizinhos",
      "groupby junta itens IGUAIS QUE ESTÃO LADO A LADO e devolve pares (chave, grupo). Por isso, quase sempre você precisa ordenar os dados antes! Com key=funcao você escolhe o critério, por exemplo a primeira letra.",
      """from itertools import groupby
def primeira_letra(palavra):
    return palavra[0]
compras = ["banana", "abacaxi", "uva", "amora", "batata"]
compras.sort()
for letra, grupo in groupby(compras, key=primeira_letra):
    print(letra, list(grupo))""",
      [OUT('from itertools import groupby\nchaves = []\nfor k, g in groupby("aabbbac"):\n    chaves.append(k)\nprint(chaves)',
           ["['a', 'b', 'c']", "['aa', 'bbb', 'a', 'c']", "['a', 'a', 'b', 'b', 'b', 'a', 'c']"],
           "Sem ordenar, o último a fica num grupo separado, porque não está ao lado dos outros."),
       TYPE('from itertools import groupby\npartes = []\nfor letra, g in groupby(sorted("banana")):\n    partes.append(letra + str(len(list(g))))\nprint("".join(partes))',
            "Ordenado, banana vira aaabnn: três a, um b e dois n."),
       MC("Por que costumamos ordenar os dados antes de usar groupby?",
          "Porque ele só junta itens iguais que estão um ao lado do outro",
          ["Porque ele dá erro com listas fora de ordem", "Porque ele só funciona com números", "Porque ele ordena ao contrário"],
          "Fora de ordem, o mesmo valor aparece em vários grupos separados."),
       ORDER("Monte o programa que mostra cada nota e quantas vezes ela apareceu.",
             ["from itertools import groupby",
              "notas = sorted([7, 9, 7, 10, 9])",
              "for nota, grupo in groupby(notas):",
              "    print(nota, len(list(grupo)))"],
             "Importa, ordena as notas, agrupa e conta o tamanho de cada grupo.")]),
    # lição 5
    L("accumulate: totais acumulados",
      "accumulate vai somando passo a passo e mostra cada total parcial, como o saldo de uma conta depois de cada compra. Você também pode passar uma função como segundo argumento: max dá o recorde até agora, min o menor valor até agora e operator.mul multiplica.",
      """from itertools import accumulate
vendas = [100, 50, 200, 30]
print(list(accumulate(vendas)))
print(list(accumulate(vendas, max)))""",
      [OUT("from itertools import accumulate\nprint(list(accumulate([1, 2, 3, 4])))",
           ["[1, 2, 3, 4]", "[10]", "[3, 5, 7]"],
           "Cada número é a soma de tudo até ali: 1, 1+2, 1+2+3, 1+2+3+4."),
       TYPE("from itertools import accumulate\ntemps = [22, 25, 21, 28, 26]\nprint(list(accumulate(temps, min)))",
            "Com min, cada posição mostra a menor temperatura vista até ali."),
       FILL("Complete para multiplicar acumulando: 2, 2x3, 2x3x4.",
            "import operator\nfrom itertools import accumulate\nprint(list(accumulate([2, 3, 4], operator.___)))",
            "mul", ["add", "sum", "times"],
            "operator.mul é a multiplicação em forma de função; add seria a soma, que já é o padrão."),
       CODE("Crie a função saldos(movimentos) que devolve a lista do saldo depois de cada movimento (positivo é depósito, negativo é saque). O saldo começa em 0.",
            "from itertools import accumulate\n\ndef saldos(movimentos):\n    pass\n",
            "from itertools import accumulate\n\ndef saldos(movimentos):\n    return list(accumulate(movimentos))",
            'assert saldos([100, -30, 50]) == [100, 70, 120], "saldos([100, -30, 50]) deve ser [100, 70, 120]"\n'
            'assert saldos([20]) == [20], "saldos([20]) deve ser [20]"',
            "accumulate soma passo a passo; lembre de transformar em lista com list().")]),
    # lição 6
    L("Desafio: escala de plantão",
      "Juntando tudo: chain une as equipes, cycle faz o rodízio e zip para quando a lista menor (os dias) acaba, então o laço não fica infinito. combinations mostra as duplas possíveis.",
      """from itertools import chain, cycle, combinations
equipe_a = ["Ana", "Caio"]
equipe_b = ["Bia"]
todos = list(chain(equipe_a, equipe_b))
dias = ["seg", "ter", "qua", "qui"]
for dia, pessoa in zip(dias, cycle(todos)):
    print(dia, pessoa)
print(list(combinations(todos, 2)))""",
      [OUT('from itertools import count\nprint(list(zip("abc", count(1))))',
           ["[('a', 0), ('b', 1), ('c', 2)]", "O programa nunca termina", "[('a', 1)]"],
           "count é infinito, mas zip para quando o texto abc acaba, depois de 3 pares."),
       MC("Você quer todas as combinações de sabor e tamanho de sorvete. Qual ferramenta?",
          "product(sabores, tamanhos)",
          ["chain(sabores, tamanhos)", "combinations(sabores, 2)", "groupby(sabores)"],
          "product cruza cada sabor com cada tamanho."),
       TYPE("from itertools import accumulate, chain\nprint(list(accumulate(chain([1], [2, 3]))))",
            "chain passa por 1, 2, 3 e accumulate soma: 1, 3, 6."),
       CODE("Crie a função escala(pessoas, dias) que devolve uma lista de tuplas (dia, pessoa), repetindo as pessoas em rodízio. Use cycle.",
            "from itertools import cycle\n\ndef escala(pessoas, dias):\n    pass\n",
            "from itertools import cycle\n\ndef escala(pessoas, dias):\n    return list(zip(dias, cycle(pessoas)))",
            'assert escala(["Ana", "Bia"], ["seg", "ter", "qua"]) == [("seg", "Ana"), ("ter", "Bia"), ("qua", "Ana")], "Esperado: seg-Ana, ter-Bia, qua-Ana"\n'
            'assert escala(["Teo"], ["sab", "dom"]) == [("sab", "Teo"), ("dom", "Teo")], "Com uma pessoa só, ela pega todos os dias"',
            "zip(dias, cycle(pessoas)) para quando os dias acabam, mesmo com o cycle infinito.")]),
]

BUGS = r'''
@lib_itertools 3
from itertools import groupby
votos = ["sim", "não", "sim", "não"]
for voto, grupo in groupby(votos):
    print(voto, len(list(grupo)))  # esperado: sim 2
>>> for voto, grupo in groupby(sorted(votos)):
!! groupby só junta vizinhos iguais. Ordene antes com sorted.

@lib_itertools 1
from itertools import count
print(list(islice(count(5), 3)))
>>> from itertools import count, islice
!! islice também precisa ser importado do itertools.

@lib_itertools 3
import itertools
times = ["A", "B", "C"]
jogos = list(itertools.permutations(times, 2))
print(len(jogos))  # esperado: 3
>>> jogos = list(itertools.combinations(times, 2))
!! A x B é o mesmo jogo que B x A: a ordem não importa, então use combinations.

@lib_itertools 2
from itertools import accumulate
saldo = accumulate([10, 20, 30])
print(saldo[-1])
>>> saldo = list(accumulate([10, 20, 30]))
!! accumulate devolve um iterador, que não aceita [-1]. Transforme em lista primeiro.

@lib_itertools 3
from itertools import chain
turmas = [["Ana"], ["Bia", "Caio"]]
todos = list(chain(turmas))
print(len(todos))  # esperado: 3
>>> todos = list(chain.from_iterable(turmas))
!! chain(turmas) vê só uma lista com 2 listas dentro. Para achatar, use chain.from_iterable.

@lib_itertools 2
from itertools import count, islice
senhas = list(count(100)[:3])
print(senhas)
>>> senhas = list(islice(count(100), 3))
!! Não dá para fatiar um iterador com [:3]. Use islice para pegar os primeiros itens.
'''
