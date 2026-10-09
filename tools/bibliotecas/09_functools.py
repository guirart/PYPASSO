from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_functools", titulo="functools",
               descricao="Ferramentas para funções: reduzir, pré-preencher, memorizar e decorar.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("reduce: juntar tudo num valor",
      "O módulo functools já vem com o Python e traz ferramentas para trabalhar com funções. reduce(funcao, lista) junta os itens dois a dois até sobrar um só valor, como ir somando o carrinho de compras item por item. Um terceiro argumento opcional diz o valor inicial.",
      """from functools import reduce
def somar(a, b):
    return a + b
precos = [10, 25, 5]
print(reduce(somar, precos))
print(reduce(somar, precos, 100))""",
      [OUT("from functools import reduce\ndef mult(a, b):\n    return a * b\nprint(reduce(mult, [2, 3, 4]))",
           ["9", "[2, 6, 24]", "6"],
           "Primeiro 2 * 3 = 6, depois 6 * 4 = 24."),
       TYPE("from functools import reduce\ndef maior(a, b):\n    return a if a > b else b\nprint(reduce(maior, [7, 3, 9, 2]))",
            "Comparando dois a dois e ficando com o maior, sobra o 9."),
       MC("O que reduce(somar, [], 0) devolve?",
          "0, o valor inicial", ["Dá erro", "None", "[]"],
          "Com a lista vazia não há nada para juntar, então sai o valor inicial."),
       CODE("Crie a função juntar(palavras) que usa reduce para juntar as palavras com um espaço entre elas.",
            "from functools import reduce\n\ndef juntar(palavras):\n    pass\n",
            'from functools import reduce\n\ndef unir(a, b):\n    return a + " " + b\n\ndef juntar(palavras):\n    return reduce(unir, palavras)',
            'assert juntar(["bom", "dia", "Ana"]) == "bom dia Ana", "juntar([bom, dia, Ana]) deve ser: bom dia Ana"\n'
            'assert juntar(["oi"]) == "oi", "Com uma palavra só, devolve a própria palavra"',
            "Crie uma função que une duas palavras com espaço e passe para o reduce.")]),
    # lição 2
    L("partial: funções pré-preenchidas",
      "partial cria uma nova função com alguns argumentos já preenchidos. É como um botão de atalho: em vez de repetir desconto=0.5 em toda chamada, você cria a função black_friday uma vez e só passa o preço.",
      """from functools import partial
def preco_final(preco, desconto):
    return preco - preco * desconto
black_friday = partial(preco_final, desconto=0.5)
print(black_friday(100))
print(black_friday(30))""",
      [OUT("from functools import partial\ndef potencia(base, exp):\n    return base ** exp\nquadrado = partial(potencia, exp=2)\nprint(quadrado(5))",
           ["10", "32", "7"],
           "quadrado(5) vira potencia(5, exp=2), que é 5 ** 2."),
       TYPE('from functools import partial\ndef saudar(saudacao, nome):\n    return f"{saudacao}, {nome}!"\noi = partial(saudar, "Oi")\nprint(oi("Teo"))',
            "O primeiro argumento (saudacao) já veio preenchido com Oi."),
       FILL("Complete para criar a função dobro a partir de multiplicar.",
            "from functools import partial\ndef multiplicar(a, b):\n    return a * b\ndobro = ___(multiplicar, 2)\nprint(dobro(7))",
            "partial", ["reduce", "lambda", "def"],
            "partial(multiplicar, 2) fixa o a em 2; dobro(7) vira multiplicar(2, 7)."),
       MC("Para que serve o partial?",
          "Criar uma versão de uma função com alguns argumentos já fixos",
          ["Rodar uma função só pela metade", "Dividir uma função em duas", "Deixar uma função mais rápida"],
          "Ele não muda a função original: cria um atalho com valores já preenchidos.")]),
    # lição 3
    L("cache: memorizar resultados",
      "@cache, escrito em cima de uma função, faz o Python lembrar das respostas: se a função for chamada de novo com os mesmos argumentos, ele devolve o resultado guardado sem recalcular. Isso deixa o Fibonacci recursivo instantâneo. @lru_cache(maxsize=100) faz o mesmo, mas guarda só os últimos resultados, e cache_info() mostra quantas vezes a memória foi usada (hits).",
      """from functools import cache
@cache
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
print(fib(10))
print(fib(80))""",
      [OUT("from functools import cache\nlog = []\n@cache\ndef dobro(n):\n    log.append(n)\n    return n * 2\ndobro(3)\ndobro(3)\ndobro(4)\nprint(len(log))",
           ["3", "1", "0"],
           "A segunda chamada com 3 usa a memória e nem roda a função. Só 3 e 4 entram no log."),
       TYPE("from functools import lru_cache\n@lru_cache(maxsize=100)\ndef quadrado(n):\n    return n * n\nquadrado(2)\nquadrado(2)\nquadrado(3)\nprint(quadrado.cache_info().hits)",
            "hits conta as vezes em que a resposta veio da memória: só o segundo quadrado(2)."),
       MC("Em qual função NÃO faz sentido usar @cache?",
          "Uma função que sorteia um número diferente a cada chamada",
          ["Uma função que calcula Fibonacci", "Uma função que calcula o frete por CEP", "Uma função que converte Celsius para Fahrenheit"],
          "Com cache, o sorteio sairia sempre igual. Use cache só quando os mesmos argumentos sempre dão o mesmo resultado."),
       CODE("Esta função fib é lentíssima para números grandes. Coloque @cache em cima dela para que fib(60) responda na hora.",
            "from functools import cache\n\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n",
            "from functools import cache\n\n@cache\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)",
            'assert hasattr(fib, "cache_info"), "Coloque @cache na linha logo acima de def fib"\n'
            'assert fib(60) == 1548008755920, "fib(60) deve ser 1548008755920"',
            "Com @cache, cada fib(n) é calculado uma vez só.")]),
    # lição 4
    L("Decoradores e wraps",
      "Um decorador é uma função que embrulha outra para acrescentar algo (um aviso, um log, um formato) sem mexer no código dela; escrever @gritar em cima de def saudar é o mesmo que saudar = gritar(saudar). Dentro do decorador, criamos uma função interna (o embrulho) que chama a original. Coloque @wraps(func) no embrulho para a função manter o nome original.",
      """from functools import wraps
def gritar(func):
    @wraps(func)
    def embrulho(texto):
        return func(texto).upper() + "!"
    return embrulho

@gritar
def saudar(nome):
    return "oi, " + nome

print(saudar("ana"))
print(saudar.__name__)""",
      [OUT('def gritar(func):\n    def embrulho(texto):\n        return func(texto).upper()\n    return embrulho\n\n@gritar\ndef saudar(nome):\n    return "oi, " + nome\n\nprint(saudar.__name__)',
           ["saudar", "gritar", "None"],
           "Sem @wraps, a função decorada passa a se chamar como o embrulho. É isso que o wraps conserta."),
       MC("Escrever @gritar em cima de def saudar(...) é o mesmo que…",
          "saudar = gritar(saudar)",
          ["gritar = saudar(gritar)", "saudar = gritar", "saudar(gritar())"],
          "O decorador recebe a função e devolve o embrulho, que passa a ocupar o nome saudar."),
       ORDER("Monte o decorador dobrar, que dobra o resultado da função.",
             ["from functools import wraps",
              "def dobrar(func):",
              "    @wraps(func)",
              "    def embrulho(n):",
              "        return func(n) * 2",
              "    return embrulho"],
             "O embrulho fica dentro do decorador, e o decorador devolve o embrulho sem chamá-lo."),
       CODE("Complete o decorador com_reais(func) para que a função decorada devolva o resultado como texto no formato R$ <valor>.",
            "from functools import wraps\n\ndef com_reais(func):\n    @wraps(func)\n    def embrulho(n):\n        return func(n)\n    return embrulho\n",
            'from functools import wraps\n\ndef com_reais(func):\n    @wraps(func)\n    def embrulho(n):\n        return f"R$ {func(n)}"\n    return embrulho',
            '@com_reais\ndef total(n):\n    return n * 3\n'
            'assert total(5) == "R$ 15", "total(5) deve devolver o texto R$ 15"\n'
            'assert total.__name__ == "total", "Mantenha o @wraps(func) para a função continuar se chamando total"',
            'O embrulho chama a função original e monta o texto: return f"R$ {func(n)}".')]),
    # lição 5
    L("Ordenar com cmp_to_key",
      "Às vezes a regra de ordenação é difícil de escrever só com key. Com cmp_to_key, você escreve uma função comparar(a, b) que devolve um número negativo se a vem antes, positivo se a vem depois e 0 se empatam. Depois é só usar sorted(lista, key=cmp_to_key(comparar)).",
      """from functools import cmp_to_key
def comparar(a, b):
    if a[1] != b[1]:
        return b[1] - a[1]
    if a[0] < b[0]:
        return -1
    if a[0] > b[0]:
        return 1
    return 0
jogadores = [("Teo", 5), ("Ana", 8), ("Bia", 5)]
print(sorted(jogadores, key=cmp_to_key(comparar)))""",
      [OUT("from functools import cmp_to_key\ndef comparar(a, b):\n    return a - b\nprint(sorted([3, 1, 2], key=cmp_to_key(comparar)))",
           ["[3, 2, 1]", "[3, 1, 2]", "TypeError"],
           "a - b é negativo quando a é menor, então os menores vêm antes: ordem crescente."),
       TYPE("from functools import cmp_to_key\ndef comparar(a, b):\n    return b - a\nprint(sorted([5, 2, 9], key=cmp_to_key(comparar)))",
            "Invertendo para b - a, os maiores vêm primeiro."),
       MC("Se comparar(a, b) devolve um número negativo, isso significa que…",
          "a deve vir antes de b", ["b deve vir antes de a", "a e b são iguais", "a deve ser removido"],
          "Negativo: a primeiro. Positivo: b primeiro. Zero: empate."),
       CODE("Crie comparar(a, b) para ordenar palavras pelo tamanho (menores primeiro) e, em caso de empate, em ordem alfabética.",
            "from functools import cmp_to_key\n\ndef comparar(a, b):\n    return 0\n",
            "from functools import cmp_to_key\n\ndef comparar(a, b):\n    if len(a) != len(b):\n        return len(a) - len(b)\n    if a < b:\n        return -1\n    if a > b:\n        return 1\n    return 0",
            'r = sorted(["pera", "uva", "kiwi", "abacaxi"], key=cmp_to_key(comparar))\n'
            'assert r == ["uva", "kiwi", "pera", "abacaxi"], "Esperado: uva, kiwi, pera, abacaxi"',
            "Compare primeiro os tamanhos; se forem iguais, compare as palavras com < e >.")]),
    # lição 6
    L("Desafio: conta do restaurante",
      "Juntando tudo: reduce soma os pedidos, partial cria a função de taxa de serviço já pronta e cache evita recalcular contas repetidas. Cada ferramenta resolve um pedaço do problema.",
      """from functools import reduce, partial
def somar(a, b):
    return a + b
def aplicar_taxa(valor, taxa):
    return round(valor * (1 + taxa), 2)
com_servico = partial(aplicar_taxa, taxa=0.1)
pedidos = [20, 35, 15]
total = reduce(somar, pedidos)
print(total, com_servico(total))""",
      [OUT('from functools import partial, reduce\ndef juntar(sep, a, b):\n    return a + sep + b\ncom_hifen = partial(juntar, "-")\nprint(reduce(com_hifen, ["a", "b", "c"]))',
           ["abc", "a-b-c-", "-a-b-c"],
           "com_hifen(a, b) vira juntar(\"-\", a, b); o reduce junta a com b e depois com c."),
       MC("Uma função calcula o frete pelo CEP e é chamada muitas vezes com os mesmos CEPs. O que ajuda?",
          "Colocar @cache na função",
          ["Usar reduce na função", "Usar cmp_to_key no CEP", "Trocar a função por partial"],
          "O cache guarda o frete de cada CEP e devolve na hora nas próximas vezes."),
       TYPE("from functools import reduce\nprint(reduce(max, [3, 8, 1]))",
            "max(3, 8) dá 8, e depois max(8, 1) dá 8."),
       CODE("Crie total_carrinho(precos, desconto) que soma os preços com reduce, aplica o desconto (0.1 = 10%) e devolve o valor arredondado com round(..., 2). Depois crie com_cupom = partial(total_carrinho, desconto=0.2).",
            "from functools import reduce, partial\n\ndef total_carrinho(precos, desconto):\n    pass\n\ncom_cupom = None\n",
            "from functools import reduce, partial\n\ndef somar(a, b):\n    return a + b\n\ndef total_carrinho(precos, desconto):\n    total = reduce(somar, precos)\n    return round(total * (1 - desconto), 2)\n\ncom_cupom = partial(total_carrinho, desconto=0.2)",
            'assert total_carrinho([10, 20], 0.1) == 27.0, "total_carrinho([10, 20], 0.1) deve ser 27.0"\n'
            'assert com_cupom is not None, "Crie com_cupom com partial"\n'
            'assert com_cupom([50, 50]) == 80.0, "com_cupom([50, 50]) deve ser 80.0 (20% de desconto)"',
            "reduce soma, o desconto multiplica por (1 - desconto) e partial fixa desconto=0.2.")]),
]

BUGS = r'''
@lib_functools 4
import functools
def somar(a, b):
    return a + b
print(reduce(somar, [1, 2, 3]))
>>> print(functools.reduce(somar, [1, 2, 3]))
!! reduce não é uma função pronta do Python: ela mora no functools.

@lib_functools 4
from functools import partial
def preco_final(preco, desconto):
    return preco - preco * desconto
metade = partial(preco_final(desconto=0.5))
print(metade(100))
>>> metade = partial(preco_final, desconto=0.5)
!! Passe a função sem chamá-la: partial(preco_final, desconto=0.5).

@lib_functools 5
from functools import cache
def total(precos):
    return sum(precos)
total = cache(total)
print(total([10, 20]))
>>> print(total((10, 20)))
!! O cache guarda as respostas pelos argumentos, e lista não pode ser chave. Use uma tupla.

@lib_functools 5
from functools import wraps
def dobrar(func):
    @wraps(func)
    def embrulho(n):
        func(n) * 2
    return embrulho
def mais_um(n):
    return n + 1
mais_um = dobrar(mais_um)
print(mais_um(3))  # esperado: 8
>>> return func(n) * 2
!! Faltou o return no embrulho: sem ele, a função decorada devolve None.

@lib_functools 7
from functools import wraps
def avisar(func):
    @wraps(func)
    def embrulho(x):
        print("rodando...")
        return func(x)
    return embrulho()
def dobro(x):
    return 2 * x
dobro = avisar(dobro)
print(dobro(4))
>>> return embrulho
!! O decorador devolve a função embrulho, sem chamá-la (sem parênteses).

@lib_functools 4
from functools import cmp_to_key
def comparar(a, b):
    return a - b
print(sorted([3, 1, 2], key=comparar))
>>> print(sorted([3, 1, 2], key=cmp_to_key(comparar)))
!! key espera uma função de um argumento. Converta a função de comparar com cmp_to_key.
'''
