from bt_helpers import OUT, TYPE, MC, FILL, ORDER, L

UNIDADE = dict(id="lib_numpy", titulo="NumPy", descricao="Contas rápidas com listas de números: arrays, médias, filtros e matrizes.",
               externa=True, grupo="Bibliotecas externas")

LICOES = [
    L("O que é NumPy e o array",
      "NumPy é a biblioteca de números do Python: ela faz contas com milhares de valores de uma vez, muito rápido. Como não vem com o Python, você instala com pip install numpy e importa com o apelido de costume: import numpy as np. A peça principal é o array, criado com np.array(lista): ele tem shape (o formato), dtype (o tipo dos números) e volta a ser lista com .tolist().",
      'import numpy as np\n\nvendas = np.array([120, 80, 95, 130])\nprint(vendas)\nprint(vendas.shape)\nprint(vendas.dtype)\nprint(vendas.tolist())',
      [MC("Como se instala o NumPy no computador?", "pip install numpy", ["import numpy", "python install numpy", "Ele já vem com o Python"], "pip install baixa e instala o pacote. O import só funciona depois disso."),
       FILL("Complete o import do jeito que todo mundo usa.", 'import numpy ___ np\nnotas = np.array([7, 8, 10])\nprint(notas)', "as", ["like", "to", "from"], "import numpy as np dá o apelido np para a biblioteca."),
       OUT('import numpy as np\nnotas = np.array([6, 8, 9])\nprint(notas)', ["[6, 8, 9]", "(6, 8, 9)", "array(6 8 9)"], "O print de um array mostra os números entre colchetes, separados só por espaço, sem vírgulas."),
       TYPE('import numpy as np\nidades = np.array([12, 15, 11, 14, 13])\nprint(idades.shape)', "shape diz o tamanho de cada dimensão. Um array de 5 números tem shape (5,).")]),
    L("Criando arrays prontos",
      "Nem sempre você digita os números. np.arange(início, fim, passo) funciona como o range e devolve um array. np.linspace(a, b, n) cria n números igualmente espaçados de a até b (incluindo o b). np.zeros(n) e np.ones(n) criam arrays cheios de 0 ou de 1, ótimos para começar uma contagem.",
      'import numpy as np\n\nprint(np.arange(0, 10, 2))\nprint(np.linspace(0, 1, 5))\nprint(np.zeros(3))\nprint(np.ones(4, dtype=int))',
      [OUT('import numpy as np\nprint(np.arange(1, 6).tolist())', ["[1, 2, 3, 4, 5, 6]", "[0, 1, 2, 3, 4, 5]", "[1, 6]"], "Como no range, o fim (6) não entra."),
       TYPE('import numpy as np\nprint(np.linspace(0, 100, 5).tolist())', "5 números igualmente espaçados de 0 até 100, com o 100 incluído. São floats."),
       MC("Qual comando cria um array com 7 zeros, para começar a contar os dias da semana?", "np.zeros(7)", ["np.zero(7)", "np.array(7)", "[0] * np.ones(7)"], "np.zeros(n) cria n zeros (do tipo float)."),
       FILL("Complete para obter os números pares de 0 a 8: [0, 2, 4, 6, 8]", 'import numpy as np\npares = np.___(0, 10, 2)\nprint(pares.tolist())', "arange", ["range", "linspace", "ones"], "np.arange(início, fim, passo) é o range do NumPy.")]),
    L("Contas com o array inteiro",
      "Com listas, para dobrar cada valor você precisa de um for. Com arrays, a conta vale para todos os itens de uma vez: arr * 2, arr + 10, arr + outro_arr (item com item). Comparações também: arr > 100 devolve um array de True e False, chamado máscara.",
      'import numpy as np\n\nprecos = np.array([10, 25, 40])\nprint(precos * 2)\nprint(precos + np.array([1, 2, 3]))\nprint(precos > 20)\n\nlista = [10, 25, 40]\nprint(lista * 2)',
      [OUT('import numpy as np\nprint((np.array([1, 2, 3]) * 3).tolist())', ["[1, 2, 3, 1, 2, 3, 1, 2, 3]", "[3, 6, 9, 3, 6, 9]", "[4, 5, 6]"], "No array, * 3 multiplica cada número. Repetir a sequência é coisa de lista."),
       OUT('print([1, 2] * 2)', ["[2, 4]", "[1, 2, 2]", "Erro"], "Atenção: isso é uma lista comum, não um array. Lista * 2 repete os itens."),
       TYPE('import numpy as np\nloja1 = np.array([5, 8, 2])\nloja2 = np.array([3, 1, 4])\nprint((loja1 + loja2).tolist())', "Arrays do mesmo tamanho se somam item com item: 5+3, 8+1, 2+4."),
       MC("O que np.array([3, 9, 6]) > 5 devolve?", "Um array [False True True]", ["True", "O número 2", "Erro: não dá para comparar array com número"], "A comparação é feita item a item e gera uma máscara de True/False.")]),
    L("Estatísticas: soma, média, máximo",
      "Arrays têm métodos prontos para resumir dados: .sum(), .mean() (média), .max(), .min() e .argmax() (a POSIÇÃO do maior). Em uma tabela (array 2D), axis=0 calcula por coluna e axis=1 por linha. Use round() ou float() para mostrar resultados limpos.",
      'import numpy as np\n\nvendas = np.array([120, 80, 95, 130, 75])\nprint(vendas.sum())\nprint(vendas.mean())\nprint(vendas.max(), vendas.argmax())\n\nnotas = np.array([[7, 8], [9, 6], [5, 10]])\nprint(notas.mean(axis=0).tolist())\nprint(notas.sum(axis=1).tolist())',
      [OUT('import numpy as np\nv = np.array([4, 9, 2, 9])\nprint(v.argmax())', ["9", "3", "[1, 3]"], "argmax devolve a posição do maior. Se houver empate, vale a primeira: posição 1."),
       TYPE('import numpy as np\nnotas = np.array([6, 7, 8, 10])\nprint(notas.mean())', "Média = (6 + 7 + 8 + 10) / 4 = 31 / 4."),
       OUT('import numpy as np\nm = np.array([[1, 2], [3, 4]])\nprint(m.sum(axis=0).tolist())', ["[3, 7]", "10", "[1, 2, 3, 4]"], "axis=0 soma descendo cada coluna: 1+3 e 2+4."),
       MC("Numa tabela com uma linha por aluno e uma coluna por prova, como obter a média de cada aluno?", "notas.mean(axis=1)", ["notas.mean(axis=0)", "notas.mean()", "notas.max(axis=1)"], "axis=1 percorre cada linha, ou seja, cada aluno.")]),
    L("Índices, fatias e filtros",
      "Arrays aceitam índice e fatia como as listas: arr[0], arr[-1], arr[1:3]. A novidade é o filtro com máscara: arr[arr > 5] devolve só os valores que passam no teste. Dá para juntar condições com & (e) e | (ou), cada uma entre parênteses.",
      'import numpy as np\n\ntemps = np.array([18, 25, 31, 22, 35])\nprint(temps[0], temps[-1])\nprint(temps[1:3])\nprint(temps[temps > 24])\nprint(temps[(temps > 20) & (temps < 30)])',
      [TYPE('import numpy as np\nv = np.array([10, 20, 30, 40, 50])\nprint(v[1:4].tolist())', "A fatia 1:4 pega as posições 1, 2 e 3."),
       OUT('import numpy as np\nnotas = np.array([4, 7, 9, 5, 8])\nprint(notas[notas >= 7].tolist())', ["[False, True, True, False, True]", "[4, 5]", "3"], "A máscara escolhe só os valores 7 ou mais."),
       FILL("Complete para contar quantos alunos tiraram nota abaixo de 5.", 'import numpy as np\nnotas = np.array([3, 8, 4, 6])\nabaixo = notas[notas ___ 5]\nprint(len(abaixo))', "<", [">", "=", "=>"], "notas < 5 é a máscara dos que ficaram abaixo de 5."),
       MC("Qual filtro pega as temperaturas entre 20 e 30?", "t[(t > 20) & (t < 30)]", ["t[t > 20 and t < 30]", "t[20 < t < 30]", "t[(t > 20) | (t < 30)]"], "Com arrays, use & entre condições com parênteses. and e a comparação encadeada dão erro, e | pegaria quase tudo.")]),
    L("Desafio: reshape e matrizes",
      "reshape(linhas, colunas) reorganiza os mesmos números numa tabela, sem mudar os valores. Isso é útil, por exemplo, para transformar 12 meses de vendas em 4 trimestres de 3 meses e então somar cada trimestre com axis=1. Juntando tudo: criar, reorganizar, filtrar e resumir.",
      'import numpy as np\n\nmeses = np.arange(1, 13) * 10\ntri = meses.reshape(4, 3)\nprint(tri)\nprint(tri.shape)\nprint(tri.sum(axis=1).tolist())\nprint(int(tri.argmax()))',
      [TYPE('import numpy as np\nm = np.arange(6).reshape(2, 3)\nprint(m.tolist())', "Os números 0 a 5 em 2 linhas de 3, preenchendo linha por linha."),
       OUT('import numpy as np\na = np.arange(12).reshape(3, 4)\nprint(a.shape)', ["(4, 3)", "12", "(3, 4, 12)"], "O shape fica (linhas, colunas) = (3, 4)."),
       MC("O que acontece com np.arange(10).reshape(3, 3)?", "Dá erro: 10 números não cabem em 3 x 3 = 9", ["Cria uma matriz 3 x 3 e descarta o 10º número", "Cria uma matriz 3 x 4 completando com zeros", "Cria uma lista de listas comum"], "O reshape exige o mesmo total de itens: linhas x colunas tem de ser igual ao tamanho."),
       ORDER("Monte o programa que mostra o total vendido nos dias com mais de 100 vendas.",
             ["import numpy as np", "vendas = np.array([90, 150, 80, 120])", "grandes = vendas[vendas > 100]", "print(int(grandes.sum()))"],
             "Primeiro o import, depois o array, o filtro e por fim a soma: 150 + 120 = 270.")]),
]

BUGS = r'''
@lib_numpy 1
import numpy as nb
v = np.array([1, 2, 3])
print(v.sum())
>>> import numpy as np
!! O apelido no import tem de ser o mesmo usado no código: np.

@lib_numpy 2
import numpy as np
notas = np.array(7, 8, 9)
print(notas.mean())
>>> notas = np.array([7, 8, 9])
!! np.array recebe UMA lista: faltaram os colchetes.

@lib_numpy 3
import numpy as np
precos = [10, 20, 30]
dobro = precos * 2
print(dobro[1])  # esperado: 40
>>> dobro = np.array(precos) * 2
!! Lista * 2 repete os itens. Transforme em array para multiplicar cada valor.

@lib_numpy 3
import numpy as np
t = np.array([18, 25, 31, 22])
quentes = t[t > 20 and t < 30]
print(quentes.tolist())
>>> quentes = t[(t > 20) & (t < 30)]
!! Com arrays use & e parênteses, não and.

@lib_numpy 3
import numpy as np
vendas = np.array([50, 90, 70])
print(vendas.max())  # esperado: 1
>>> print(vendas.argmax())  # esperado: 1
!! max devolve o maior valor; para saber a posição do maior use argmax.

@lib_numpy 2
import numpy as np
m = np.arange(8).reshape(3, 3)
print(m.shape)
>>> m = np.arange(9).reshape(3, 3)
!! Uma matriz 3 x 3 precisa de 9 números, e arange(8) só gera 8.
'''
