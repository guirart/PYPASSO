from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_random", titulo="random",
               descricao="Sorteios, dados, embaralhar listas e resultados que se repetem com seed.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Números quebrados: random",
      "O módulo random sorteia coisas: números, itens de uma lista, a ordem de um baralho. É só import random. random.random() devolve um float entre 0 e 1 (o 1 nunca sai), e random.uniform(a, b) um float entre a e b. Aqui usamos random.seed(1) antes para o sorteio sair sempre igual, já explicamos o porquê.",
      'import random\nrandom.seed(1)\n\nprint(random.random())\nprecos = random.uniform(10, 20)\nprint(round(precos, 2))',
      [MC("Qual destes valores random.random() NUNCA devolve?", "1.0", ["0.5", "0.999", "0.0001"], "random() sorteia de 0 até quase 1: o 1 em si fica de fora."),
       OUT('import random\nrandom.seed(1)\nx = random.uniform(5, 8)\nprint(5 <= x <= 8)', ["False", "6.5", "Erro"], "uniform(5, 8) sempre devolve um número entre 5 e 8, então a comparação dá True."),
       FILL("Complete para sortear uma temperatura decimal entre 18 e 30.", 'import random\nrandom.seed(2)\ntemp = random.___(18, 30)\nprint(round(temp, 1))', "uniform", ["random", "float", "between"], "uniform(a, b) sorteia um float entre a e b. random() não recebe argumentos."),
       TYPE('import random\nrandom.seed(5)\nprint(type(random.random()).__name__)', "random() sempre devolve um número decimal.")]),
    # lição 2
    L("Inteiros: randint e randrange",
      "random.randint(a, b) sorteia um inteiro de a até b, incluindo os dois: randint(1, 6) é um dado. random.randrange funciona como range: randrange(10) vai de 0 a 9, e randrange(0, 10, 2) sorteia só pares. Ótimo para dados, senhas numéricas e notas de teste.",
      'import random\nrandom.seed(3)\n\ndado = random.randint(1, 6)\nprint("Dado:", dado)\npar = random.randrange(0, 10, 2)\nprint("Par:", par)',
      [MC("Quais valores random.randint(1, 3) pode sortear?", "1, 2 ou 3", ["1 ou 2", "0, 1, 2 ou 3", "Qualquer número entre 1 e 3, como 2.5"], "Em randint, os dois extremos entram."),
       MC("Qual valor random.randrange(1, 10) NUNCA sorteia?", "10", ["1", "9", "5"], "randrange funciona como range: o fim fica de fora."),
       OUT('import random\nrandom.seed(4)\nn = random.randrange(0, 100, 5)\nprint(n % 5)', ["5", "1", "100"], "Com passo 5, só saem múltiplos de 5 (0, 5, 10...). O resto da divisão por 5 é sempre 0."),
       CODE("Crie a função rolar_d20() que devolve um número inteiro de 1 a 20, como o dado de RPG.",
            "import random\n\ndef rolar_d20():\n    return 0\n\nprint(rolar_d20())\n",
            'import random\n\ndef rolar_d20():\n    return random.randint(1, 20)\n\nprint(rolar_d20())',
            'import random\nrandom.seed(0)\nr = [rolar_d20() for _ in range(500)]\nassert all(isinstance(x, int) for x in r), "Devolva um número inteiro"\nassert min(r) == 1, "O 1 também precisa poder sair"\nassert max(r) == 20, "O 20 também precisa poder sair"',
            'return random.randint(1, 20)')]),
    # lição 3
    L("Escolhendo: choice e choices",
      "random.choice(lista) sorteia um item da lista, como tirar um papelzinho do pote. random.choices(lista, k=3) sorteia 3 vezes devolvendo o papel ao pote, então pode repetir. Com weights você dá pesos: itens com peso maior saem mais.",
      'import random\nrandom.seed(5)\n\njantar = random.choice(["pizza", "sushi", "taco", "salada"])\nprint(jantar)\nprint(random.choices(["cara", "coroa"], k=3))',
      [OUT('import random\nrandom.seed(7)\nlanche = random.choice(["pão", "bolo", "fruta"])\nprint(lanche in ["pão", "bolo", "fruta"])', ["False", "pão", "['pão', 'bolo', 'fruta']"], "choice sempre devolve um item da lista, então está na lista: True."),
       OUT('import random\nrandom.seed(2)\nmoedas = random.choices(["cara", "coroa"], k=4)\nprint(len(moedas))', ["2", "1", "3"], "k=4 pede 4 sorteios, então a lista tem 4 itens."),
       MC("Numa roleta de prêmios, o chocolate deve sair 3 vezes mais que o carro. O que usar?", 'random.choices(["chocolate", "carro"], weights=[3, 1])', ['random.choice(["chocolate", "carro"], 3)', 'random.randint(["chocolate", "carro"])', 'random.choices(["chocolate", "carro"], k=3)'], "weights dá o peso de cada item. k só diz quantos sorteios fazer."),
       FILL("Complete para sortear quem lava a louça hoje.", 'import random\nrandom.seed(1)\ncasa = ["Ana", "Caio", "Bia"]\nprint(random.___(casa))', "choice", ["choices", "randint", "shuffle"], "choice pega um item. choices devolveria uma lista.")]),
    # lição 4
    L("Embaralhar: shuffle e sample",
      "random.shuffle(lista) embaralha a própria lista, como um baralho, e devolve None. random.sample(lista, k) sorteia k itens diferentes, sem repetir, e não mexe na lista original: perfeito para loteria, sorteio de brindes e quiz.",
      'import random\nrandom.seed(4)\n\ncartas = [1, 2, 3, 4, 5]\nrandom.shuffle(cartas)\nprint(cartas)\nprint(sorted(random.sample(range(1, 61), 6)))',
      [OUT('import random\nrandom.seed(3)\nfila = ["a", "b", "c"]\nx = random.shuffle(fila)\nprint(x)', ["['c', 'a', 'b']", "['a', 'b', 'c']", "Erro"], "shuffle mexe na lista e devolve None. A resposta está em fila, não em x."),
       OUT('import random\nrandom.seed(8)\nnums = random.sample([1, 2, 3, 4, 5], 5)\nprint(sorted(nums))', ["[1, 1, 2, 3, 5]", "[5, 4, 3, 2, 1]", "[1, 2, 3, 4]"], "sample nunca repete: sorteando 5 de 5, saem todos, e sorted coloca em ordem."),
       MC("Você vai sortear 3 ganhadores diferentes entre 50 inscritos. Qual comando?", "random.sample(inscritos, 3)", ["random.choices(inscritos, k=3)", "random.shuffle(inscritos, 3)", "random.choice(inscritos, 3)"], "choices pode repetir a mesma pessoa; sample garante 3 diferentes."),
       TYPE('import random\nrandom.seed(1)\nletras = ["x", "y", "z"]\nrandom.shuffle(letras)\nprint(len(letras))', "Embaralhar muda a ordem, não o tamanho.")]),
    # lição 5
    L("Repetindo o sorteio: seed",
      "Os números do random são pseudoaleatórios: saem de uma conta que começa numa semente. random.seed(42) fixa essa semente, e aí a sequência de sorteios se repete igualzinha toda vez. Isso é ótimo para testar programas, repetir uma fase de jogo ou comparar resultados com colegas.",
      'import random\n\nrandom.seed(10)\nprint(random.randint(1, 100))\nrandom.seed(10)\nprint(random.randint(1, 100))',
      [OUT('import random\nrandom.seed(9)\na = random.randint(1, 1000)\nrandom.seed(9)\nb = random.randint(1, 1000)\nprint(a == b)', ["False", "9", "Depende da sorte"], "Mesma semente, mesma sequência: a e b são iguais."),
       MC("Para que serve random.seed(123)?", "Fazer os sorteios saírem sempre na mesma sequência", ["Sortear o número 123", "Deixar os sorteios mais aleatórios", "Limitar os sorteios até 123"], "A semente define o ponto de partida; o mesmo ponto gera a mesma sequência."),
       ORDER("Monte o programa que rola um dado e dá sempre o mesmo resultado, em qualquer computador.", ["import random", "random.seed(7)", "dado = random.randint(1, 6)", "print(dado)"], "Primeiro o import, depois a semente, e só então o sorteio. Seed depois do sorteio não adianta."),
       CODE("Use random.seed(42) e depois guarde em dados uma lista com 3 sorteios de randint(1, 6). Mostre a lista com print.",
            "import random\ndados = []\nprint(dados)\n",
            'import random\nrandom.seed(42)\ndados = [random.randint(1, 6) for _ in range(3)]\nprint(dados)',
            'import random\nrandom.seed(42)\nesperado = [random.randint(1, 6) for _ in range(3)]\nassert dados == esperado, f"Com seed 42, a lista deve ser {esperado}"\nassert __stdout__.strip() == str(esperado), "Mostre a lista com print"',
            'random.seed(42)\ndados = [random.randint(1, 6) for _ in range(3)]')]),
    # lição 6
    L("Desafio: jogo de dados",
      "Juntando tudo: randint para os dados, choice para sortear quem começa, sample para os brindes e seed para poder repetir a partida e conferir o resultado.",
      'import random\nrandom.seed(42)\n\njogadores = ["Ana", "Caio", "Bia"]\nprint("Começa:", random.choice(jogadores))\nd1 = random.randint(1, 6)\nd2 = random.randint(1, 6)\nprint(f"Dados: {d1} + {d2} = {d1 + d2}")',
      [MC("A soma de dois dados (randint(1, 6) + randint(1, 6)) pode dar quais valores?", "De 2 a 12", ["De 1 a 12", "De 0 a 12", "De 2 a 6"], "O menor é 1 + 1 = 2 e o maior é 6 + 6 = 12."),
       OUT('import random\nrandom.seed(42)\nprint([random.randint(1, 6) for _ in range(3)])', ["[6, 1, 2]", "[1, 1, 6]", "[4, 4, 4]"], "Com seed 42, a sequência é sempre a mesma: 6, 1, 1."),
       FILL("Complete para sortear 2 brindes diferentes.", 'import random\nrandom.seed(7)\nbrindes = ["caneca", "boné", "chaveiro", "adesivo"]\nprint(random.___(brindes, 2))', "sample", ["choice", "shuffle", "randint"], "sample sorteia vários sem repetir."),
       CODE("Crie a função jogar(semente) que chama random.seed(semente), rola dois dados com randint(1, 6) e devolve a soma.",
            "import random\n\ndef jogar(semente):\n    return 7\n\nprint(jogar(42))\n",
            'import random\n\ndef jogar(semente):\n    random.seed(semente)\n    d1 = random.randint(1, 6)\n    d2 = random.randint(1, 6)\n    return d1 + d2\n\nprint(jogar(42))',
            'import random\nfor s in (1, 2, 3, 42):\n    random.seed(s)\n    esperado = random.randint(1, 6) + random.randint(1, 6)\n    assert jogar(s) == esperado, f"Com semente {s}, a soma deveria ser {esperado}"\nassert jogar(5) == jogar(5), "A mesma semente deve dar a mesma soma"',
            'random.seed(semente)\nd1 = random.randint(1, 6)\nd2 = random.randint(1, 6)\nreturn d1 + d2')]),
]

BUGS = r'''
@lib_random 3
import random
random.seed(1)
print(random.randint(1, 6, 2))
>>> print(random.randint(1, 6))
!! randint recebe só o início e o fim. Para usar passo, é randrange.

@lib_random 4
import random
random.seed(3)
cartas = [1, 2, 3]
cartas = random.shuffle(cartas)
print(len(cartas))
>>> random.shuffle(cartas)
!! shuffle devolve None. Ele embaralha a lista ali mesmo, sem atribuir.

@lib_random 3
import random
random.seed(2)
print(random.choice("Ana", "Caio", "Bia"))
>>> print(random.choice(["Ana", "Caio", "Bia"]))
!! choice recebe UMA lista. Coloque os nomes entre colchetes.

@lib_random 3
import random
random.seed(5)
ganhadores = random.sample(["Ana", "Caio"], 3)
print(len(ganhadores))
>>> ganhadores = random.sample(["Ana", "Caio"], 2)
!! sample não repete: não dá para sortear 3 pessoas de uma lista com 2.

@lib_random 4
import random
random.seed(9)
n = random.randint(1, 1000)
random.seed(8)
print(n == random.randint(1, 1000))  # esperado: True
>>> random.seed(9)
!! Para repetir o sorteio, use a mesma semente nas duas vezes.

@lib_random 3
import random
random.seed(9)
vez = random.randint(0, 3)
nomes = ["Ana", "Caio", "Bia"]
print(nomes[vez])
>>> vez = random.randint(0, 2)
!! randint inclui o fim: 3 pode sair e não existe nomes[3]. Use 0 a 2 ou random.choice.
'''
