from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    "print": [
        # lição 2 (a lição 1 já existe: o básico de print, sep e end)
        L("Vários valores de uma vez",
          "print aceita quantos valores você quiser, de tipos diferentes. Ele converte cada um em texto e coloca um espaço entre eles. Sem nada dentro, print() só pula uma linha.",
          'nome = "Ana"\nidade = 30\nprint("Nome:", nome, "Idade:", idade)\nprint()\nprint(1, 2.5, True, None)',
          [OUT('print("x", 1, [2])', ["x1[2]", "x, 1, [2]", "Erro"], "Cada valor vira texto, separado por espaço."),
           TYPE('print(10, "+", 5, "=", 15)', "Os cinco valores separados por espaço."),
           MC("O que print() sem nada dentro faz?", "Mostra uma linha vazia", ["Dá erro", "Mostra None", "Não faz nada"], "Ele só imprime o final, que por padrão é a quebra de linha."),
           FILL("Complete para mostrar: Total: 3", 'qtd = 3\nprint("Total:"___ qtd)', ",", ["+", ";", "."], "A vírgula separa os valores dentro do print.")]),
        # lição 3
        L("f-strings no print",
          "Uma f-string tem um f antes das aspas e põe valores dentro de chaves {}. É o jeito mais fácil de montar frases com variáveis. Dentro das chaves dá até para fazer contas.",
          'nome = "Bia"\npontos = 7\nprint(f"{nome} fez {pontos} pontos")\nprint(f"Dobro: {pontos * 2}")',
          [OUT('x = 4\nprint(f"{x} ao quadrado é {x ** 2}")', ["x ao quadrado é x ** 2", "{x} ao quadrado é {x ** 2}", "4 ao quadrado é 8"], "As chaves calculam as expressões."),
           TYPE('a, b = 2, 3\nprint(f"{a}+{b}={a + b}")', "Sem espaços, como está na f-string."),
           MC('O que sai de print("Oi, {nome}") sem o f?', "Oi, {nome}", ["Oi, Ana", "Erro", "Oi,"], "Sem o f, as chaves são texto comum."),
           CODE("Crie as variáveis produto = \"café\" e preco = 5 e mostre exatamente: café custa 5 reais",
                "produto = \"café\"\npreco = 5\n# escreva o print aqui\n",
                'produto = "café"\npreco = 5\nprint(f"{produto} custa {preco} reais")',
                'assert __stdout__.strip() == "café custa 5 reais", "A saída deve ser exatamente: café custa 5 reais"',
                'print(f"{produto} custa {preco} reais")')]),
        # lição 4
        L("Formatando números",
          "Dentro das chaves, depois de dois-pontos, você controla o formato: :.2f mostra 2 casas decimais, :5 reserva 5 espaços e :, separa milhares.",
          'preco = 3.14159\nprint(f"{preco:.2f}")\nprint(f"[{7:5}]")\nprint(f"{1234567:,}")',
          [OUT('print(f"{2.5:.1f}")', ["2.50", "3", "2"], ".1f mostra uma casa decimal."),
           TYPE('print(f"{10 / 3:.2f}")', "Duas casas decimais, arredondado."),
           OUT('print(f"[{42:>5}]")', ["[42   ]", "[42]", "[ 42 ]"], ">5 alinha à direita num espaço de 5."),
           MC("Qual formato mostra 9.5 como 9.50?", ":.2f", [":2", ":.2", ":f2"], "O f diz que é número decimal, e .2 dá duas casas.")]),
        # lição 5
        L("print em laços",
          "Dentro de um for, cada print mostra uma linha. Com end=\" \" você mantém tudo na mesma linha, e um print() no final pula a linha.",
          'for i in range(1, 4):\n    print(i, end=" ")\nprint()\nprint("fim")',
          [OUT('for c in "oi":\n    print(c)', ["oi", "o i", "['o', 'i']"], "Cada letra num print, então uma por linha."),
           TYPE('for n in range(3):\n    print(n, end="-")', "Tudo na mesma linha, com - depois de cada número."),
           ORDER("Monte o programa que mostra 1 2 3 numa linha e depois pula a linha.", ['for n in [1, 2, 3]:', '    print(n, end=" ")', 'print()'], "O print() fora do laço pula a linha no final."),
           CODE("Mostre a tabuada do 3 de 1 a 5, uma conta por linha, no formato 3 x 1 = 3",
                "# use um for com range\n",
                'for i in range(1, 6):\n    print(f"3 x {i} = {3 * i}")',
                'linhas = __stdout__.strip().splitlines()\nassert len(linhas) == 5, "Devem ser 5 linhas"\nassert linhas[0] == "3 x 1 = 3", "A primeira linha deve ser: 3 x 1 = 3"\nassert linhas[-1] == "3 x 5 = 15", "A última linha deve ser: 3 x 5 = 15"',
                'for i in range(1, 6): print(f"3 x {i} = {3 * i}")')]),
        # lição 6
        L("Desafio: painel de jogo",
          "Juntando tudo: f-strings, formatação e sep/end ajudam a montar telas bonitas no terminal, como o placar de um jogo.",
          'jogador = "Rafa"\nvida = 87.5\nouro = 1200\nprint("=" * 20)\nprint(f"{jogador:^20}")\nprint(f"Vida: {vida:.0f}%  Ouro: {ouro:,}")\nprint("=" * 20)',
          [OUT('print("-" * 3, "x", "-" * 3)', ["---x---", "-x-", "- - - x - - -"], "\"-\" * 3 é ---, e o print separa com espaço."),
           TYPE('print(f"{"ok":*^6}")', "^6 centraliza em 6 espaços, preenchendo com *."),
           MC("Para mostrar 0.756 como 75.6%, use…", 'f"{0.756:.1%}"', ['f"{0.756:%}"', 'f"{0.756 * 100}"', 'f"{0.756:.1f}%"'], "O formato % multiplica por 100 e põe o símbolo."),
           CODE("Crie a função placar(nome, pontos) que MOSTRA (com print) o texto Jogador: <nome> | Pontos: <pontos>",
                "def placar(nome, pontos):\n    pass\n\nplacar(\"Ana\", 10)\n",
                'def placar(nome, pontos):\n    print(f"Jogador: {nome} | Pontos: {pontos}")\n\nplacar("Ana", 10)',
                'assert "Jogador: Ana | Pontos: 10" in __stdout__, "Esperado: Jogador: Ana | Pontos: 10"',
                'print(f"Jogador: {nome} | Pontos: {pontos}")')]),
    ],
}

BUGS = r'''
@fn_print 2
nome = "Ana"
print(f"Oi, {Nome}")
>>> print(f"Oi, {nome}")
!! A variável se chama nome, com n minúsculo.

@fn_print 1
print("a", "b", sep="-" end="!")
>>> print("a", "b", sep="-", end="!")
!! Faltou a vírgula entre sep e end.

@fn_print 2
preco = 9.5
print(f"R$ {preco:.2}")  # esperado: R$ 9.50
>>> print(f"R$ {preco:.2f}")  # esperado: R$ 9.50
!! Sem o f, .2 conta algarismos, não casas decimais.

@fn_print 2
pontos = 10
print("Pontos: " + pontos)
>>> print("Pontos: " + str(pontos))
!! Texto + número dá erro. Use str() ou vírgula.

@fn_print 1
print(1, 2, 3, sep="")  # esperado: 1-2-3
>>> print(1, 2, 3, sep="-")  # esperado: 1-2-3
!! sep="" cola os números. O separador pedido é o hífen.

@fn_print 1
print("Total: {10 + 5}")  # esperado: Total: 15
>>> print(f"Total: {10 + 5}")  # esperado: Total: 15
!! Faltou o f antes das aspas.
'''
