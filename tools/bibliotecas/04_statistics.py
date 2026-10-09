from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_statistics", titulo="statistics",
               descricao="Média, mediana, moda e dispersão: resuma listas de números sem fazer conta na mão.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Média: mean e fmean",
      "A biblioteca statistics já vem com o Python e resume listas de números: notas, preços, tempos. Importe com import statistics. A função mean devolve a média (soma dividida pela quantidade); fmean faz o mesmo, mas sempre devolve float e é mais rápida.",
      'import statistics\n\nnotas = [7, 8, 9]\nprint(statistics.mean(notas))\nprint(statistics.fmean(notas))',
      [OUT('import statistics\nprint(statistics.mean([10, 9, 8, 7]))', ["8", "34", "8.0"], "10 + 9 + 8 + 7 = 34, e 34 / 4 = 8.5."),
       TYPE('import statistics\nprint(statistics.fmean([2, 4, 6]))', "fmean sempre devolve float: 12 / 3 vira 4.0."),
       MC("Para que serve a função statistics.mean?", "Calcular a média de uma lista de números", ["Somar todos os números da lista", "Achar o maior número da lista", "Ordenar a lista do menor para o maior"], "mean é a média: soma tudo e divide pela quantidade."),
       CODE("A lista gastos tem o que você gastou de lanche em cada dia da semana. Use statistics.mean para guardar a média na variável media e mostre-a com print.",
            "import statistics\n\ngastos = [12, 15, 9, 20, 14]\nmedia = 0\n",
            "import statistics\n\ngastos = [12, 15, 9, 20, 14]\nmedia = statistics.mean(gastos)\nprint(media)",
            'assert media == 14, "A média de [12, 15, 9, 20, 14] é 14"\nassert __stdout__.strip() == "14", "Mostre a média com print(media)"',
            "media = statistics.mean(gastos) faz a soma (70) dividida por 5.")]),
    # lição 2
    L("O meio da fila: median",
      "A mediana é o valor do meio depois de ordenar a lista. Ela não se deixa enganar por um valor muito fora da curva, como um salário gigante. Com quantidade par, median faz a média dos dois do meio; median_low e median_high escolhem um deles.",
      'import statistics\n\nsalarios = [2000, 2500, 3000, 50000]\nprint(statistics.mean(salarios))\nprint(statistics.median(salarios))\nprint(statistics.median_low([1, 2, 3, 4]))\nprint(statistics.median_high([1, 2, 3, 4]))',
      [OUT('import statistics\nprint(statistics.median([3, 1, 2]))', ["1", "3", "6"], "Ordenando fica [1, 2, 3]; o do meio é 2. A função ordena sozinha."),
       TYPE('import statistics\nprint(statistics.median([1, 2, 3, 4]))', "Quantidade par: média de 2 e 3, que dá 2.5."),
       OUT('import statistics\nprint(statistics.median_high([10, 20, 30, 40]))', ["25.0", "20", "40"], "median_high pega o maior dos dois do meio: 30."),
       MC("Numa rua, as casas custam 300 mil, 320 mil, 350 mil e uma mansão de 5 milhões. Qual número representa melhor o preço típico?", "A mediana", ["A média", "O maior valor", "A soma"], "A mansão puxa a média para cima; a mediana fica no meio e ignora o exagero.")]),
    # lição 3
    L("O mais comum: mode",
      "A moda é o valor que mais aparece. Serve para números e também para textos, como o sabor de pizza mais pedido. Se houver empate, mode devolve o primeiro que apareceu; multimode devolve uma lista com todos os empatados.",
      'import statistics\n\npedidos = ["calabresa", "mussarela", "calabresa", "frango"]\nprint(statistics.mode(pedidos))\nprint(statistics.multimode([1, 1, 2, 2, 3]))',
      [OUT('import statistics\nprint(statistics.mode([3, 5, 3, 7]))', ["5", "7", "4.5"], "O 3 aparece duas vezes, mais que os outros."),
       TYPE('import statistics\nprint(statistics.multimode(["a", "b", "b", "a"]))', "Empate entre a e b: multimode devolve os dois, na ordem em que apareceram."),
       FILL("Complete para descobrir a cor de camiseta mais vendida.", 'import statistics\nvendas = ["azul", "preta", "preta", "branca"]\nprint(statistics.___(vendas))', "mode", ["mean", "median", "max"], "mode devolve o valor que mais se repete: preta."),
       CODE("Os votos da turma para o passeio estão na lista votos. Guarde na variável vencedor o destino mais votado (use statistics.mode) e mostre-o.",
            'import statistics\n\nvotos = ["praia", "zoo", "praia", "museu", "zoo", "praia"]\nvencedor = ""\n',
            'import statistics\n\nvotos = ["praia", "zoo", "praia", "museu", "zoo", "praia"]\nvencedor = statistics.mode(votos)\nprint(vencedor)',
            'assert vencedor == "praia", "O destino mais votado é praia"\nassert "praia" in __stdout__, "Mostre o vencedor com print"',
            'vencedor = statistics.mode(votos) devolve "praia", que tem 3 votos.')]),
    # lição 4
    L("Espalhamento: stdev e variance",
      "Duas turmas podem ter a mesma média e ser bem diferentes: numa todo mundo tirou 7, na outra metade tirou 4 e metade 10. O desvio padrão (stdev) mede o quanto os valores se espalham em volta da média: 0 quer dizer todos iguais. A variância (variance) é o desvio padrão ao quadrado. Use pstdev e pvariance quando a lista tem TODOS os dados (a população inteira).",
      'import statistics\n\nturma_a = [7, 7, 7, 7]\nturma_b = [4, 10, 4, 10]\nprint(statistics.mean(turma_a), statistics.mean(turma_b))\nprint(statistics.pstdev(turma_a), statistics.pstdev(turma_b))\nprint(statistics.pvariance(turma_b))',
      [OUT('import statistics\nprint(statistics.pstdev([5, 5, 5]))', ["5.0", "15", "1.0"], "Todos iguais: não há espalhamento nenhum, então o desvio é 0.0."),
       TYPE('import statistics\nprint(statistics.pstdev([0, 10]))', "A média é 5 e cada valor está a 5 de distância dela."),
       OUT('import statistics\nprint(statistics.pvariance([0, 10]))', ["5", "10", "50"], "A variância é o desvio ao quadrado: 5 × 5 = 25."),
       MC("Dois entregadores levam, em média, 30 minutos. O de desvio padrão 2 e o de desvio padrão 15: qual é mais previsível?", "O de desvio padrão 2", ["O de desvio padrão 15", "Os dois são iguais, porque a média é igual", "Não dá para saber sem a mediana"], "Desvio pequeno quer dizer tempos sempre perto dos 30 minutos.")]),
    # lição 5
    L("Dividindo em partes: quantiles",
      "quantiles corta os dados ordenados em n partes iguais e devolve os pontos de corte. Com n=4 (o padrão) saem os quartis: 3 números que separam os 25% menores, a metade e os 25% maiores. É assim que se diz \"você está entre os 25% mais rápidos\".",
      'import statistics\n\ntempos = [1, 2, 3, 4, 5, 6, 7, 8]\nprint(statistics.quantiles(tempos, n=4))\nprint(statistics.quantiles(tempos, n=2))',
      [MC("Quantos números quantiles(dados, n=4) devolve?", "3", ["4", "2", "5"], "Para cortar em 4 partes, bastam 3 cortes."),
       OUT('import statistics\nprint(statistics.quantiles([2, 4, 6, 8], n=4))', ["[2, 4, 6, 8]", "[4, 6, 8]", "[2.5, 5.0]"], "São 3 pontos de corte: [2.5, 5.0, 7.5]."),
       TYPE('import statistics\nprint(len(statistics.quantiles(range(1, 101), n=10)))', "Dividir em 10 partes (decis) precisa de 9 cortes."),
       FILL("Complete para dividir as alturas em 4 partes (quartis).", 'import statistics\nalturas = [150, 160, 165, 170, 180]\nprint(statistics.quantiles(alturas, ___=4))', "n", ["partes", "k", "size"], "O número de partes vai no parâmetro n.")]),
    # lição 6
    L("Desafio: relatório da turma",
      "Juntando tudo, dá para montar um relatório de notas em poucas linhas: média, mediana, nota mais comum e o quanto as notas variam. Lembre: essas funções dão erro com lista vazia, então confira antes.",
      'import statistics\n\nnotas = [6, 8, 8, 9, 5, 10, 8]\nprint("Média:", round(statistics.mean(notas), 1))\nprint("Mediana:", statistics.median(notas))\nprint("Moda:", statistics.mode(notas))\nprint("Desvio:", round(statistics.pstdev(notas), 2))',
      [OUT('import statistics\nnotas = [4, 6, 8]\nprint(statistics.mean(notas), statistics.median(notas))', ["6 8", "18 6", "6.0 6.0"], "Média: 18 / 3 = 6. Mediana: o do meio de [4, 6, 8], também 6."),
       MC("O que acontece com statistics.mean([])?", "Dá erro (StatisticsError)", ["Devolve 0", "Devolve None", "Devolve uma lista vazia"], "Não existe média de nada, então a biblioteca avisa com um erro."),
       ORDER("Monte o programa que mostra a mediana das idades.", ["import statistics", "idades = [12, 15, 11, 14]", "meio = statistics.median(idades)", "print(meio)"], "Primeiro o import, depois os dados, o cálculo e o print."),
       CODE("Crie a função relatorio(notas) que DEVOLVE um dicionário com as chaves \"media\", \"mediana\" e \"moda\", calculadas com statistics. Se a lista estiver vazia, devolva None.",
            "import statistics\n\ndef relatorio(notas):\n    pass\n",
            'import statistics\n\ndef relatorio(notas):\n    if not notas:\n        return None\n    return {"media": statistics.mean(notas), "mediana": statistics.median(notas), "moda": statistics.mode(notas)}',
            'r = relatorio([6, 8, 8, 9, 9, 8])\nassert r is not None, "Para uma lista com notas, devolva um dicionário"\nassert r["media"] == 8, "A média de [6, 8, 8, 9, 9, 8] é 8"\nassert r["mediana"] == 8, "A mediana de [6, 8, 8, 9, 9, 8] é 8"\nassert r["moda"] == 8, "A moda de [6, 8, 8, 9, 9, 8] é 8"\nr2 = relatorio([5, 7, 10])\nassert r2 == {"media": 22 / 3, "mediana": 7, "moda": 5}, "Confira as três chaves para [5, 7, 10]"\nassert relatorio([]) is None, "Lista vazia deve devolver None"',
            'Teste a lista vazia primeiro (if not notas: return None) e depois monte o dicionário com mean, median e mode.')]),
]

BUGS = r'''
@lib_statistics 2
import statistics
print(statistics.average([7, 8, 9]))
>>> print(statistics.mean([7, 8, 9]))
!! Em statistics, a média se chama mean.

@lib_statistics 2
import statistics
print(statistic.median([3, 1, 2]))
>>> print(statistics.median([3, 1, 2]))
!! O nome da biblioteca termina com s: statistics.

@lib_statistics 2
import statistics
print(statistics.mean(7, 8, 9))
>>> print(statistics.mean([7, 8, 9]))
!! mean recebe UMA lista (ou outra coleção), não números soltos.

@lib_statistics 3
import statistics
notas = []
print(statistics.mean(notas))
>>> print(statistics.mean(notas) if notas else 0)
!! Lista vazia não tem média: confira antes de calcular.

@lib_statistics 3
import statistics
pedidos = ["pizza", "sushi", "pizza", "sushi"]
print(statistics.mode(pedidos))  # esperado: ['pizza', 'sushi']
>>> print(statistics.multimode(pedidos))  # esperado: ['pizza', 'sushi']
!! Com empate, mode devolve só o primeiro. multimode devolve todos os empatados.

@lib_statistics 3
import statistics
tempos = [1, 2, 3, 4, 5, 6, 7, 8]
print(statistics.quantiles(tempos, 4))
>>> print(statistics.quantiles(tempos, n=4))
!! O número de partes precisa ser escrito com o nome: n=4.
'''
