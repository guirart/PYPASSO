from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_matplotlib", titulo="Matplotlib (gráficos)",
               descricao="Gráficos de linha e de barras, com título, legenda e cores.",
               externa=True, grupo="Bibliotecas externas")

# Aqui tudo roda sem tela: em vez de ver a imagem, conferimos o gráfico com print
# (quantas linhas, quantas barras, qual o título...).

LICOES = [
    # lição 1
    L("Seu primeiro gráfico",
      "O Matplotlib transforma listas de números em gráficos: vendas do mês, notas da turma, peso do pet. Ele não vem com o Python; instale no terminal com pip install matplotlib. No código, importe a parte de desenhar com import matplotlib.pyplot as plt, crie uma figura com plt.figure() e desenhe uma linha com plt.plot(x, y). No seu computador, plt.show() abre uma janela com o gráfico.",
      'import matplotlib.pyplot as plt\n\nfig = plt.figure()\nlinhas = plt.plot([1, 2, 3], [2, 4, 3])\nprint(type(fig).__name__)\nprint(len(linhas), "linha desenhada")\n# no seu computador: plt.show()',
      [MC("Como você instala o Matplotlib no seu computador?",
          "pip install matplotlib (no terminal)",
          ["import matplotlib (já instala sozinho)", "pip install pyplot", "Ele já vem junto com o Python"],
          "Bibliotecas externas se instalam com pip no terminal. Depois disso o import funciona."),
       FILL("Complete o import do jeito que todo mundo usa.",
            'import matplotlib.pyplot as ___\n\nplt.figure()\nplt.plot([1, 2], [3, 4])',
            "plt", ["pyplot", "mpl", "graf"],
            "O apelido plt é o padrão. Assim o código fica curto: plt.plot, plt.show..."),
       OUT('import matplotlib.pyplot as plt\n\nplt.figure()\nlinhas = plt.plot([1, 2, 3], [5, 7, 6])\nprint(len(linhas))',
           ["3", "2", "0"],
           "Três pontos, mas uma linha só ligando todos eles."),
       MC("O que plt.show() faz?",
          "Abre uma janela mostrando o gráfico",
          ["Salva o gráfico num arquivo", "Imprime os números no terminal", "Apaga o gráfico"],
          "show() mostra o gráfico na tela. Para salvar num arquivo existe o savefig.")]),
    # lição 2
    L("Gráfico de linhas",
      "plt.plot(x, y) liga pontos: x é a lista do eixo de baixo e y a dos valores, com o mesmo tamanho. Cada plt.plot acrescenta uma linha nova, ótimo para comparar. Use marker=\"o\" para marcar os pontos e linestyle=\"--\" para uma linha tracejada.",
      'import matplotlib.pyplot as plt\n\nplt.figure()\nmeses = ["jan", "fev", "mar"]\nplt.plot(meses, [10, 15, 12], marker="o")\nplt.plot(meses, [8, 9, 14], linestyle="--")\nprint(len(plt.gca().lines), "linhas no gráfico")',
      [OUT('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.plot([1, 2, 3], [4, 5, 6])\nplt.plot([1, 2, 3], [6, 5, 4])\nprint(len(plt.gca().lines))',
           ["1", "6", "3"],
           "Cada plt.plot desenha uma linha. plt.gca() pega o gráfico atual, e .lines são as linhas dele."),
       TYPE('import matplotlib.pyplot as plt\n\nplt.figure()\nlinha, = plt.plot([0, 1, 2, 3], [3, 1, 2, 5])\nprint(len(linha.get_xdata()))',
            "A linha tem 4 pontos, então 4 valores de x."),
       MC("O que acontece com plt.plot([1, 2, 3], [4, 5])?",
          "Dá ValueError, porque x e y têm tamanhos diferentes",
          ["Desenha só os 2 primeiros pontos", "Completa o y com zero", "Desenha 5 pontos"],
          "Cada x precisa de um y. Listas de tamanhos diferentes dão ValueError."),
       FILL("Complete para marcar cada dia com uma bolinha.",
            'import matplotlib.pyplot as plt\n\nplt.figure()\ndias = [1, 2, 3]\ntemps = [28, 31, 27]\nplt.plot(dias, temps, marker=___)',
            '"o"', ['"bola"', '"dot"', '"circulo"'],
            'marker="o" desenha um círculo em cada ponto.')]),
    # lição 3
    L("Gráfico de barras",
      "plt.bar(categorias, valores) desenha uma barra para cada categoria. É o gráfico certo para comparar coisas separadas: votos por sabor, gastos por mês, gols por jogador. Para barras deitadas, use plt.barh.",
      'import matplotlib.pyplot as plt\n\nplt.figure()\nsabores = ["chocolate", "morango", "creme"]\nvotos = [12, 7, 9]\nbarras = plt.bar(sabores, votos)\nprint(len(barras), "barras")\nprint("Mais alta:", max(b.get_height() for b in barras))',
      [OUT('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.bar(["seg", "ter", "qua", "qui"], [3, 5, 2, 4])\nprint(len(plt.gca().patches))',
           ["14", "1", "8"],
           "Cada barra é uma peça (patch) do gráfico: 4 dias, 4 barras."),
       TYPE('import matplotlib.pyplot as plt\n\nplt.figure()\nbarras = plt.bar(["gato", "cão", "peixe"], [5, 8, 2])\nprint(barras[1].get_height())',
            "barras[1] é a segunda barra, a do cão, com altura 8."),
       FILL("Complete para desenhar um gráfico de BARRAS com os pets da clínica.",
            'import matplotlib.pyplot as plt\n\nplt.figure()\nplt.___(["gato", "cão"], [5, 8])',
            "bar", ["bars", "barra", "column"],
            "O nome da função é bar, em inglês e no singular."),
       MC("Qual gráfico combina melhor com \"quantos alunos tiraram cada nota: A, B, C\"?",
          "Barras, com plt.bar",
          ["Linha, com plt.plot", "Nenhum, isso só dá para fazer com tabela", "Barras, com plt.show"],
          "Categorias separadas (A, B, C) pedem barras. Linhas servem melhor para algo que muda ao longo do tempo.")]),
    # lição 4
    L("Títulos, rótulos e cores",
      "Um gráfico sem nome confunde. plt.title dá o título, plt.xlabel e plt.ylabel nomeiam os eixos e color= escolhe a cor (\"red\", \"blue\", \"green\"...). Dê label= a cada linha e chame plt.legend() para aparecer a legenda dizendo quem é quem.",
      'import matplotlib.pyplot as plt\n\nplt.figure()\nplt.plot([1, 2, 3], [30, 31, 29], color="red", label="Recife")\nplt.plot([1, 2, 3], [18, 15, 17], color="blue", label="Curitiba")\nplt.title("Temperatura da semana")\nplt.xlabel("Dia")\nplt.ylabel("Graus")\nplt.legend()\nax = plt.gca()\nprint(ax.get_title())\nprint(ax.get_xlabel(), "|", ax.get_ylabel())\nprint([t.get_text() for t in ax.get_legend().get_texts()])',
      [OUT('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.title("Notas da turma")\nprint(plt.gca().get_title())',
           ["title", "Notas", "None"],
           "get_title devolve o texto que você deu em plt.title."),
       TYPE('import matplotlib.pyplot as plt\n\nplt.figure()\nplt.xlabel("Mês")\nplt.ylabel("Reais")\nprint(plt.gca().get_xlabel())',
            "xlabel é o nome do eixo de baixo (x)."),
       MC("De onde plt.legend() tira os nomes que aparecem na legenda?",
          "Do label= que você deu em cada plt.plot",
          ["Do título do gráfico", "Dos nomes das variáveis no código", "Do plt.xlabel"],
          "Sem label=, a legenda não sabe o nome de cada linha."),
       FILL("Complete para a linha ficar verde.",
            'import matplotlib.pyplot as plt\n\nplt.figure()\nplt.plot([1, 2, 3], [2, 3, 5], ___="green")',
            "color", ["cor", "fill", "paint"],
            "O parâmetro é color, em inglês.")]),
    # lição 5
    L("Vários gráficos: subplots",
      "fig, ax = plt.subplots() cria a figura (fig, a folha) e o gráfico (ax, a área de desenho). Com ax os nomes mudam um pouco: ax.plot, ax.bar, ax.set_title, ax.set_xlabel. Com plt.subplots(1, 2) você ganha dois gráficos lado a lado, para comparar coisas na mesma imagem.",
      'import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.plot([1, 2, 3], [3000, 5200, 4100])\nax.set_title("Passos por dia")\nprint(type(fig).__name__, type(ax).__name__)\n\nfig2, (esquerda, direita) = plt.subplots(1, 2)\nesquerda.plot([1, 2, 3], [1, 4, 9])\ndireita.bar(["A", "B"], [3, 5])\nprint(len(fig2.axes), "gráficos lado a lado")',
      [OUT('import matplotlib.pyplot as plt\n\nfig, axs = plt.subplots(2, 2)\nprint(len(fig.axes))',
           ["2", "1", "22"],
           "2 linhas por 2 colunas dá 4 gráficos na mesma figura."),
       TYPE('import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.set_title("Vendas")\nprint(ax.get_title())',
            "ax.set_title dá o título; ax.get_title lê de volta."),
       MC("Usando fig, ax = plt.subplots(), como você dá título ao gráfico?",
          'ax.set_title("Meu gráfico")',
          ['ax.title("Meu gráfico")', 'fig.set_title("Meu gráfico")', 'ax.titulo("Meu gráfico")'],
          "Com ax, as funções de enfeite ganham set_: set_title, set_xlabel, set_ylabel."),
       ORDER("Monte o programa que faz um gráfico de barras com ax e mostra quantas barras ele tem.",
             ['import matplotlib.pyplot as plt',
              'fig, ax = plt.subplots()',
              'ax.bar(["pão", "bolo", "torta"], [30, 12, 8])',
              'ax.set_ylabel("Vendidos")',
              'print(len(ax.patches))'],
             "Import, cria fig e ax, desenha as barras, enfeita e só então confere.")]),
    # lição 6
    L("Desafio: salvar e mostrar",
      "Hora de juntar tudo e guardar o resultado: fig.savefig(\"vendas.png\") salva o gráfico como imagem (dá para mandar no WhatsApp ou pôr num relatório), e plt.show() mostra na tela. Chame savefig ANTES do show, porque depois que a janela fecha o gráfico pode sair em branco.",
      'import matplotlib.pyplot as plt\nfrom pathlib import Path\n\nfig, ax = plt.subplots()\nax.bar(["jan", "fev", "mar"], [120, 95, 150], color="purple")\nax.set_title("Vendas da loja")\nax.set_xlabel("Mês")\nfig.savefig("vendas.png")\nprint(Path("vendas.png").exists())\nprint(len(ax.patches), "barras em", ax.get_title())\n# no seu computador: plt.show()',
      [OUT('import matplotlib.pyplot as plt\n\nfig, (a1, a2) = plt.subplots(1, 2)\na1.plot([1, 2], [3, 4])\na1.plot([1, 2], [4, 3])\na2.bar(["x", "y", "z"], [1, 2, 3])\nprint(len(a1.lines), len(a2.patches))',
           ["1 3", "2 1", "5 5"],
           "a1 tem duas linhas e a2 tem três barras."),
       MC("Você quer salvar o gráfico E vê-lo na tela. Qual a ordem certa?",
          "Primeiro fig.savefig(...), depois plt.show()",
          ["Primeiro plt.show(), depois fig.savefig(...)", "Só plt.show(), que já salva sozinho", "Só fig.savefig(...), que já abre a janela"],
          "show() pode limpar a figura quando a janela fecha. Salve antes de mostrar."),
       FILL("Complete para salvar o gráfico como imagem.",
            'import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots()\nax.plot([1, 2, 3], [2, 1, 3])\nfig.___("grafico.png")',
            "savefig", ["save", "show", "export"],
            "savefig salva a figura num arquivo; o formato vem da extensão (.png, .pdf...)."),
       ORDER("Monte o programa completo: gráfico de linha com título, legenda e salvo em arquivo.",
             ['import matplotlib.pyplot as plt',
              'fig, ax = plt.subplots()',
              'ax.plot([1, 2, 3], [7, 8, 10], color="green", label="Bia")',
              'ax.set_title("Notas da Bia")',
              'ax.legend()',
              'fig.savefig("notas.png")'],
             "Cria, desenha (com label), enfeita, liga a legenda e por último salva.")]),
]

BUGS = r'''
@lib_matplotlib 1
import matplotlib as plt

plt.figure()
plt.plot([1, 2, 3], [4, 5, 6])
>>> import matplotlib.pyplot as plt
!! As funções de desenhar ficam em matplotlib.pyplot.

@lib_matplotlib 4
import matplotlib.pyplot as plt

plt.figure()
plt.plot([1, 2, 3], [10, 20])
print("pronto")
>>> plt.plot([1, 2, 3], [10, 20, 30])
!! x tem 3 valores e y só 2. As listas precisam ter o mesmo tamanho.

@lib_matplotlib 5
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [5, 3, 4])
ax.title("Peso do Rex")
print(ax.get_title())
>>> ax.set_title("Peso do Rex")
!! Com ax, o título se dá com set_title.

@lib_matplotlib 4
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2], [3, 4], legenda="Ana")
ax.legend()
>>> ax.plot([1, 2], [3, 4], label="Ana")
!! O nome da linha para a legenda vai em label=.

@lib_matplotlib 5
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(["A", "B"], [7, 9])
print(len(ax.lines))  # esperado: 2
>>> print(len(ax.patches))  # esperado: 2
!! Barras ficam em ax.patches; ax.lines guarda só linhas.

@lib_matplotlib 4
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 2)
ax.plot([1, 2], [3, 4])
print(len(fig.axes))
>>> ax[0].plot([1, 2], [3, 4])
!! Com subplots(1, 2), ax é uma lista de dois gráficos. Escolha um: ax[0].

@lib_matplotlib 4
import matplotlib.pyplot as plt

plt.figure()
plt.bar(["pão", "bolo"], [30, 12], color="vermelho")
>>> plt.bar(["pão", "bolo"], [30, 12], color="red")
!! As cores têm nome em inglês: "red", não "vermelho".
'''
