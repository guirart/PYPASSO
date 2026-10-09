from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ------------------------------------------------------------------ abs
    "abs": [
        L("Inteiros, decimais e complexos",
          "abs mantém o tipo do número: inteiro continua inteiro e decimal continua decimal. Com número complexo, abs devolve o tamanho dele (a distância até o zero), sempre como float.",
          'print(abs(-3))\nprint(abs(-2.5))\nprint(abs(3 + 4j))\nprint(type(abs(-3)).__name__)',
          [OUT('print(abs(-7.0))', ["7", "-7.0", "7.00"], "Decimal continua decimal: 7.0."),
           TYPE('print(abs(6 - 8j))', "O tamanho de 6 - 8j é a raiz de 36 + 64, ou seja, 10.0."),
           MC("Qual é o tipo de abs(-4)?", "int", ["float", "str", "bool"], "abs só tira o sinal; o tipo continua int."),
           FILL("Complete para mostrar 8.", 'x = -8\nprint(___(x))', "abs", ["round", "int", "str"], "abs(-8) tira o sinal e dá 8.")]),
        L("Diferenças e distâncias",
          "No dia a dia, abs aparece quando só importa o tamanho da diferença: quanto faltou para a meta, quanto a temperatura mudou, quanto alguém deve.",
          'alvo = 50\nchute = 42\nprint("Ficou a", abs(alvo - chute), "do alvo")\nontem, hoje = 18, 25\nprint("Mudou", abs(hoje - ontem), "graus")',
          [OUT('a, b = 3, 10\nprint(abs(a - b), abs(b - a))', ["-7 7", "7 -7", "13 13"], "Não importa a ordem: a distância é 7 nos dois casos."),
           TYPE('saldo = -150\nprint(f"Você deve R$ {abs(saldo)}")', "abs(-150) é 150."),
           MC("Num jogo de adivinhar, como medir o quão perto o chute ficou do número secreto?", "abs(secreto - chute)", ["secreto - chute", "abs(secreto) - abs(chute)", "round(chute)"], "A diferença pode ser negativa; abs deixa só o tamanho dela."),
           CODE("Crie a função distancia(a, b) que devolve a distância entre os números a e b (sempre positiva).",
                "def distancia(a, b):\n    return a - b\n",
                "def distancia(a, b):\n    return abs(a - b)",
                'assert distancia(2, 9) == 7, "distancia(2, 9) deve ser 7"\nassert distancia(9, 2) == 7, "distancia(9, 2) deve ser 7"\nassert distancia(-3, 3) == 6, "distancia(-3, 3) deve ser 6"',
                "return abs(a - b): primeiro a diferença, depois tira o sinal.")]),
        L("Cuidados com abs",
          "abs(a) - abs(b) NÃO é a distância entre a e b: calcule a diferença primeiro. abs não aceita texto, então converta antes com int() ou float(). E para forçar um número a ficar negativo, use -abs(x).",
          'print(abs(-3) - abs(5))\nprint(abs(-3 - 5))\ntry:\n    abs("-5")\nexcept TypeError as e:\n    print(type(e).__name__)\nprint(abs(int("-5")))',
          [OUT('print(abs(2 - 9), abs(2) - abs(9))', ["7 7", "-7 -7", "7 11"], "abs(2 - 9) é 7, mas abs(2) - abs(9) é 2 - 9 = -7."),
           OUT('try:\n    print(abs("-3"))\nexcept TypeError:\n    print("erro de tipo")', ["3", "-3", "'3'"], "Texto não tem valor absoluto: dá TypeError."),
           TYPE('print(-abs(-9))', "abs(-9) é 9, e o sinal de fora deixa negativo."),
           MC('Como pegar o valor absoluto do texto t = "-12"?', "abs(int(t))", ["int(abs(t))", "abs(t)", "t.abs()"], "Primeiro converta o texto para número, depois use abs.")]),
        L("abs com outras funções",
          "Como key, abs faz min, max e sorted compararem pelo tamanho do número, sem olhar o sinal. Com sum, dá para somar só os tamanhos.",
          'nums = [-7, 3, -1, 5]\nprint(min(nums, key=abs))\nprint(sorted(nums, key=abs))\nprint(sum(abs(n) for n in nums))',
          [OUT('print(sorted([-5, 2, -1], key=abs))', ["[-5, -1, 2]", "[1, 2, 5]", "[2, -1, -5]"], "Pelos tamanhos 1, 2 e 5, mas os números continuam com sinal."),
           TYPE('print(sum(abs(n) for n in [-2, 3, -4]))', "2 + 3 + 4."),
           FILL("Complete para achar o número mais perto de zero.", 'nums = [8, -2, 5]\nprint(min(nums, key=___))', "abs", ["max", "round", "sum"], "key=abs compara pelo tamanho: -2 é o mais perto de zero."),
           MC("round(abs(-2.567), 1) dá…", "2.6", ["-2.6", "2.5", "2.567"], "abs tira o sinal (2.567) e round deixa uma casa (2.6).")]),
        L("Desafio: o mais perto do alvo",
          "Para achar quem chegou mais perto de um alvo, compare abs(alvo - palpite). Com min, use key=lambda p: abs(alvo - p): lambda é uma mini-função que mede a distância de cada palpite.",
          'alvo = 100\npalpites = {"Ana": 90, "Caio": 104, "Bia": 120}\nfor nome, p in palpites.items():\n    print(nome, "errou por", abs(alvo - p))',
          [OUT('alvo = 10\nprint(min([7, 12, 15], key=lambda p: abs(alvo - p)))', ["7", "15", "2"], "As distâncias são 3, 2 e 5: o 12 é o mais perto."),
           TYPE('print(max(abs(-3), abs(2), abs(-8)))', "Os tamanhos são 3, 2 e 8."),
           MC("Por que usar abs(alvo - p) e não só alvo - p?", "Para palpites acima e abaixo do alvo contarem igual", ["Para arredondar o palpite", "Porque alvo - p dá erro", "Para o resultado virar texto"], "Sem abs, quem passou do alvo teria diferença negativa e pareceria melhor."),
           CODE("Crie a função mais_perto(alvo, palpites) que devolve o palpite da lista que ficou mais perto do alvo.",
                "def mais_perto(alvo, palpites):\n    return min(palpites)\n",
                "def mais_perto(alvo, palpites):\n    return min(palpites, key=lambda p: abs(alvo - p))",
                'assert mais_perto(10, [7, 12, 15]) == 12, "mais_perto(10, [7, 12, 15]) deve ser 12"\nassert mais_perto(0, [-5, 3, 8]) == 3, "mais_perto(0, [-5, 3, 8]) deve ser 3"\nassert mais_perto(50, [49, 60]) == 49, "mais_perto(50, [49, 60]) deve ser 49"',
                "min(palpites, key=lambda p: abs(alvo - p)) escolhe o palpite com a menor distância.")]),
    ],
    # ------------------------------------------------------------------ round
    "round": [
        L("O tipo do resultado",
          "round(x) sem casas devolve int. Com casas, mesmo round(x, 0), o resultado é float. Se o número já é inteiro, round devolve um inteiro. Negativos também arredondam para o mais próximo.",
          'print(round(7.8))\nprint(round(7.8, 0))\nprint(round(15, 2))\nprint(round(-2.7))',
          [OUT('print(round(9.99, 0))', ["10", "9.9", "9"], "Com o segundo argumento, o resultado é float: 10.0."),
           TYPE('print(round(42, 3))', "42 já é inteiro: continua 42."),
           MC("Qual é o tipo de round(3.7)?", "int", ["float", "str"], "Sem casas, round devolve inteiro: 4."),
           OUT('print(round(-2.7))', ["-2", "2", "3"], "-2.7 está mais perto de -3.")]),
        L("Médias e dinheiro",
          "Contas com decimais costumam ter muitos dígitos. Use round(valor, 1) para médias e round(valor, 2) para dinheiro, sempre no resultado final.",
          'notas = [7.5, 8.0, 9.0]\nmedia = sum(notas) / len(notas)\nprint(media)\nprint(round(media, 1))\nprint(round(19.9 * 3, 2))',
          [TYPE('print(round(10 / 3, 2))', "10 / 3 é 3.333..., com duas casas fica 3.33."),
           OUT('preco = 49.9\nprint(round(preco * 0.9, 2))', ["44.9", "45", "44.910000000000004"], "Com 10% de desconto e duas casas: 44.91."),
           MC("Para mostrar a média 7.6666... como 7.7, use…", "round(media, 1)", ["round(media)", "round(1, media)", "int(media)"], "Primeiro o número, depois as casas."),
           CODE("Crie a função media(notas) que devolve a média da lista arredondada com 1 casa decimal.",
                "def media(notas):\n    return sum(notas) / len(notas)\n",
                "def media(notas):\n    return round(sum(notas) / len(notas), 1)",
                'assert media([7, 8, 8]) == 7.7, "media([7, 8, 8]) deve ser 7.7"\nassert media([10, 9]) == 9.5, "media([10, 9]) deve ser 9.5"\nassert media([6, 7, 7]) == 6.7, "media([6, 7, 7]) deve ser 6.7"',
                "return round(sum(notas) / len(notas), 1)")]),
        L("Pegadinhas do round",
          "Empates vão para o número par: round(2.5) dá 2. Alguns decimais não são guardados exatos no computador, então round(2.675, 2) dá 2.67. E round não escreve zeros no final: para ver 3.00, formate com :.2f.",
          'print(round(0.5), round(1.5), round(2.5))\nprint(round(2.675, 2))\nprint(round(3.0, 2))\nprint(f"{3.0:.2f}")',
          [OUT('print(round(6.5))', ["7", "6.5", "7.0"], "Empate vai para o par: 6."),
           OUT('print(round(1.10, 2))', ["1.10", "1.1000", "1"], "round não guarda zeros no final: 1.1."),
           MC("Por que round(2.675, 2) dá 2.67 e não 2.68?", "O computador guarda 2.675 como 2.67499...", ["round sempre arredonda para baixo", "É um bug do Python", "round ignora a última casa"], "Os decimais são guardados em binário, quase nunca exatos."),
           FILL("Complete para mostrar 5.00.", 'x = 5\nprint(f"{x:___}")', ".2f", [".2", "2f", "2."], ".2f mostra sempre duas casas decimais.")]),
        L("round com outras funções",
          "Dá para arredondar uma lista inteira com uma list comprehension ou com map(round, lista). E combine round com sum, abs e divisões para limpar o resultado.",
          'precos = [1.234, 5.678, 9.999]\nprint([round(p, 1) for p in precos])\nprint(round(sum(precos), 2))\nprint(list(map(round, precos)))',
          [OUT('print(list(map(round, [1.4, 2.6, 3.5])))', ["[1, 3, 3]", "[1.4, 2.6, 3.5]", "[1, 2, 4]"], "1.4 vira 1, 2.6 vira 3 e 3.5 vai para o par, 4."),
           TYPE('print(round(0.1 + 0.2, 2))', "0.1 + 0.2 dá 0.30000000000000004; round limpa para 0.3."),
           ORDER("Monte o programa que mostra a média arredondada.", ['notas = [8, 7, 10]', 'media = sum(notas) / len(notas)', 'print(round(media, 1))'], "Primeiro a lista, depois a média, e por fim o round no print."),
           MC("round(abs(-4.6)) dá…", "5", ["-5", "4", "4.6"], "abs dá 4.6 e round arredonda para 5.")]),
        L("Desafio: conta do restaurante",
          "Na hora de dividir a conta, junte tudo: some a gorjeta, divida pelas pessoas e só no fim arredonde para centavos com round(valor, 2).",
          'conta = 80\ntotal = conta * 1.1\npor_pessoa = total / 3\nprint(round(total, 2))\nprint(round(por_pessoa, 2))',
          [TYPE('print(round(1234.5678, -2))', "-2 arredonda para centenas; com casas, o resultado é float."),
           OUT('print(round(19.999, 2))', ["19.99", "20", "19.999"], "19.999 com duas casas vira 20.0."),
           MC("Para dividir R$ 100 entre 3 pessoas mostrando centavos, use…", "round(100 / 3, 2)", ["round(100 // 3, 2)", "round(100 / 3)", "round(2, 100 / 3)"], "Divisão normal e duas casas: 33.33."),
           CODE("Crie dividir_conta(total, pessoas): some 10% de gorjeta ao total, divida pelas pessoas e devolva o valor arredondado com 2 casas.",
                "def dividir_conta(total, pessoas):\n    return total / pessoas\n",
                "def dividir_conta(total, pessoas):\n    return round(total * 1.1 / pessoas, 2)",
                'assert dividir_conta(100, 4) == 27.5, "dividir_conta(100, 4) deve ser 27.5"\nassert dividir_conta(90, 3) == 33.0, "dividir_conta(90, 3) deve ser 33.0"\nassert dividir_conta(50, 3) == 18.33, "dividir_conta(50, 3) deve ser 18.33"',
                "return round(total * 1.1 / pessoas, 2)")]),
    ],
    # ------------------------------------------------------------------ pow
    "pow": [
        L("Os três argumentos",
          "pow(base, expoente) dá int se os dois são inteiros e o expoente é positivo; com decimal ou expoente negativo, dá float. O terceiro argumento, o módulo, calcula o resto: pow(a, b, m) é (a ** b) % m.",
          'print(pow(2, 3))\nprint(pow(2.0, 3))\nprint(pow(10, -2))\nprint(pow(7, 2, 5))',
          [OUT('print(pow(3.0, 2))', ["9", "6.0", "3.0"], "A base é decimal, então o resultado é float: 9.0."),
           TYPE('print(pow(5, 2, 3))', "5 ** 2 é 25, e o resto de 25 por 3 é 1."),
           MC("pow(2, 3, 5) calcula…", "(2 ** 3) % 5", ["2 ** (3 % 5)", "(2 * 3) % 5", "2 ** 3 ** 5"], "Primeiro a potência, depois o resto da divisão."),
           FILL("Complete para calcular a raiz quadrada de 16.", 'print(pow(16, ___))', "0.5", ["2", "-2", "16"], "Elevar a 0.5 é o mesmo que tirar a raiz quadrada.")]),
        L("Áreas, juros e dobras",
          "Potência aparece em áreas (lado ao quadrado), volumes (lado ao cubo), juros compostos (capital vezes (1 + taxa) elevado aos anos) e em coisas que dobram.",
          'lado = 5\nprint("Área:", pow(lado, 2))\ndinheiro = 1000\nprint(round(dinheiro * pow(1.1, 2), 2))\nprint(pow(2, 10), "bactérias depois de 10 dobras")',
          [TYPE('print(pow(2, 8))', "2 multiplicado por ele mesmo 8 vezes."),
           OUT('print(round(100 * pow(1.5, 2)))', ["150", "300", "200"], "1.5 ao quadrado é 2.25; vezes 100 dá 225."),
           MC("Um cubo tem lado 3. Qual expressão dá o volume?", "pow(3, 3)", ["pow(3, 2)", "3 * 3", "pow(2, 3)"], "Volume do cubo é lado ao cubo."),
           CODE("Crie juros(capital, taxa, anos) que devolve capital * (1 + taxa) elevado a anos, arredondado com 2 casas. Use pow.",
                "def juros(capital, taxa, anos):\n    return capital * taxa * anos\n",
                "def juros(capital, taxa, anos):\n    return round(capital * pow(1 + taxa, anos), 2)",
                'assert juros(1000, 0.1, 2) == 1210.0, "juros(1000, 0.1, 2) deve ser 1210.0"\nassert juros(500, 0.05, 1) == 525.0, "juros(500, 0.05, 1) deve ser 525.0"\nassert juros(200, 0.5, 3) == 675.0, "juros(200, 0.5, 3) deve ser 675.0"',
                "return round(capital * pow(1 + taxa, anos), 2)")]),
        L("Cuidados com pow",
          "Em Python, ^ não é potência (é uma operação de bits). -2 ** 2 dá -4, porque a potência é feita antes do sinal; pow(-2, 2) dá 4. E zero elevado a negativo dá ZeroDivisionError.",
          'print(2 ^ 3)\nprint(pow(2, 3))\nprint(-2 ** 2, pow(-2, 2))\ntry:\n    pow(0, -1)\nexcept ZeroDivisionError:\n    print("não dá: divisão por zero")',
          [OUT('print(-3 ** 2)', ["9", "-6", "6"], "É -(3 ** 2): -9."),
           OUT('print(pow(-3, 2))', ["-9", "-6", "6"], "O -3 inteiro é a base: (-3) × (-3) = 9."),
           MC("O que 5 ^ 2 faz em Python?", "Uma operação de bits (XOR), não potência", ["Calcula 25", "Dá erro", "Calcula 10"], "Para potência, use pow(5, 2) ou 5 ** 2."),
           TYPE('try:\n    print(pow(0, -2))\nexcept ZeroDivisionError:\n    print("deu ZeroDivisionError")', "0 elevado a -2 seria 1 / 0.")]),
        L("pow com outras funções",
          "pow combina bem com sum e listas: some quadrados, calcule a hipotenusa ou use map(pow, bases, expoentes) para várias potências de uma vez.",
          'nums = [1, 2, 3, 4]\nprint([pow(n, 2) for n in nums])\nprint(sum(pow(n, 2) for n in nums))\nprint(list(map(pow, [2, 3], [3, 2])))',
          [OUT('print(list(map(pow, [2, 5], [2, 1])))', ["[4, 10]", "[2, 5]", "[32, 1]"], "pow(2, 2) é 4 e pow(5, 1) é 5."),
           TYPE('print(sum(pow(n, 3) for n in range(1, 4)))', "1 + 8 + 27."),
           FILL("Complete para checar se 49 é quadrado perfeito.", 'n = 49\nraiz = int(pow(n, ___))\nprint(raiz * raiz == n)', "0.5", ["2", "-1", "n"], "pow(49, 0.5) é 7.0, e 7 × 7 é 49."),
           ORDER("Monte o cálculo da hipotenusa de um triângulo de lados 3 e 4.", ['a, b = 3, 4', 'soma = pow(a, 2) + pow(b, 2)', 'print(pow(soma, 0.5))'], "Some os quadrados e tire a raiz: 5.0.")]),
        L("Desafio: potências em série",
          "Num laço, pow gera sequências: potências de 2, de 10, quadrados… Guarde os resultados numa lista para usar depois.",
          'for n in range(1, 6):\n    print(f"2 elevado a {n} = {pow(2, n)}")',
          [OUT('print(pow(10, 3) - pow(10, 2))', ["10", "100", "1"], "1000 - 100 = 900."),
           TYPE('print(pow(2, 10, 7))', "2 ** 10 é 1024, e o resto de 1024 por 7 é 2."),
           MC("Qual destes é igual a pow(9, 0.5)?", "9 ** 0.5", ["9 / 2", "9 ** 2", "9 // 2"], "Os dois dão a raiz: 3.0."),
           CODE("Crie quadrados(n) que devolve a lista com os quadrados de 1 até n. Ex.: quadrados(3) → [1, 4, 9].",
                "def quadrados(n):\n    return []\n",
                "def quadrados(n):\n    return [pow(i, 2) for i in range(1, n + 1)]",
                'assert quadrados(4) == [1, 4, 9, 16], "quadrados(4) deve ser [1, 4, 9, 16]"\nassert quadrados(1) == [1], "quadrados(1) deve ser [1]"\nassert quadrados(0) == [], "quadrados(0) deve ser []"',
                "return [pow(i, 2) for i in range(1, n + 1)]")]),
    ],
    # ------------------------------------------------------------------ divmod
    "divmod": [
        L("Negativos e decimais",
          "divmod funciona com decimais também: o resultado vem em float. Com negativos, a divisão inteira arredonda para baixo e o resto fica com o sinal do divisor: divmod(-7, 2) dá (-4, 1).",
          'print(divmod(7, 2))\nprint(divmod(-7, 2))\nprint(divmod(7.5, 2))',
          [OUT('print(divmod(9, 4))', ["(2, 2)", "(1, 2)", "2.25"], "9 // 4 é 2 e 9 % 4 é 1."),
           OUT('print(divmod(-9, 4))', ["(-2, -1)", "(-2, 1)", "(2, 1)"], "-9 // 4 arredonda para baixo: -3. E -3 × 4 + 3 = -9."),
           TYPE('print(divmod(5.5, 2))', "Com decimal, os dois valores vêm em float."),
           MC("divmod(a, b) é o mesmo que…", "(a // b, a % b)", ["(a / b, a % b)", "(a % b, a // b)", "a // b + a % b"], "Primeiro o quociente inteiro, depois o resto.")]),
        L("Relógios, caixas e ônibus",
          "Sempre que você precisa de \"quantos cabem e quanto sobra\", divmod resolve: segundos em horas e minutos, ovos em caixas, pessoas em ônibus.",
          'segundos = 3725\nhoras, resto = divmod(segundos, 3600)\nminutos, seg = divmod(resto, 60)\nprint(f"{horas}h {minutos}min {seg}s")\ncaixas, sobra = divmod(40, 12)\nprint(caixas, "caixas e", sobra, "ovos soltos")',
          [TYPE('caixas, sobra = divmod(25, 6)\nprint(caixas, sobra)', "Cabem 4 caixas de 6 (24) e sobra 1."),
           OUT('m, s = divmod(150, 60)\nprint(f"{m}:{s}")', ["2:50", "2.5", "150:60"], "150 segundos são 2 minutos e 30 segundos."),
           MC("Um ônibus leva 40 pessoas. Para saber quantos ônibus lotam e quantas pessoas sobram de 130, use…", "divmod(130, 40)", ["divmod(40, 130)", "130 / 40", "round(130 / 40)"], "Dá (3, 10): 3 ônibus cheios e 10 pessoas sobrando."),
           CODE('Crie converter(minutos) que devolve um texto no formato "Xh Ymin". Ex.: converter(135) → "2h 15min".',
                'def converter(minutos):\n    return f"{minutos}min"\n',
                'def converter(minutos):\n    h, m = divmod(minutos, 60)\n    return f"{h}h {m}min"',
                'assert converter(135) == "2h 15min", "converter(135) deve ser 2h 15min"\nassert converter(60) == "1h 0min", "converter(60) deve ser 1h 0min"\nassert converter(45) == "0h 45min", "converter(45) deve ser 0h 45min"',
                'h, m = divmod(minutos, 60) e depois return f"{h}h {m}min".')]),
        L("Cuidados com divmod",
          "A ordem importa: divmod(dividendo, divisor). O resultado é uma tupla de 2 itens, então desempacote em exatamente 2 variáveis. Divisor zero dá ZeroDivisionError, e texto precisa virar número antes.",
          'resultado = divmod(17, 5)\nprint(resultado[0], resultado[1])\ntry:\n    divmod(5, 0)\nexcept ZeroDivisionError:\n    print("não dá para dividir por zero")\nprint(divmod(int("17"), 5))',
          [OUT('print(divmod(3, 10))', ["(3, 0)", "(0, 0)", "(1, 7)"], "10 não cabe em 3: quociente 0 e resto 3."),
           OUT('r = divmod(20, 6)\nprint(r[1])', ["3", "(3, 2)", "6"], "r é (3, 2); o índice 1 é o resto."),
           MC("O que acontece em q, r, x = divmod(10, 3)?", "ValueError: divmod devolve só 2 valores", ["x vira None", "x vira 0", "Funciona normalmente"], "Não dá para tirar 3 variáveis de uma tupla de 2."),
           FILL("Complete para mostrar só o resto.", 'q, r = divmod(23, 5)\nprint(___)', "r", ["q", "divmod", "5"], "O segundo valor, r, é o resto: 3.")]),
        L("divmod com outras funções",
          "divmod num laço while separa os dígitos de um número: divmod(n, 10) tira o último dígito. Com f-strings e :02d, dá para montar relógios como 02:05.",
          'total = 125\nm, s = divmod(total, 60)\nprint(f"{m:02d}:{s:02d}")\nn = 472\nsoma = 0\nwhile n > 0:\n    n, digito = divmod(n, 10)\n    soma += digito\nprint(soma)',
          [TYPE('m, s = divmod(65, 60)\nprint(f"{m:02d}:{s:02d}")', "1 minuto e 5 segundos, com dois dígitos cada."),
           OUT('print(list(map(divmod, [7, 9], [2, 4])))', ["[(3, 1), (2, 2)]", "[3, 2]", "[(1, 3), (1, 2)]"], "divmod(7, 2) é (3, 1) e divmod(9, 4) é (2, 1)."),
           ORDER("Monte o programa que separa 3725 segundos em horas, minutos e segundos.", ['total = 3725', 'h, resto = divmod(total, 3600)', 'm, s = divmod(resto, 60)', 'print(h, m, s)'], "Primeiro as horas; o resto vira minutos e segundos."),
           MC("Com n = 538, o que n, d = divmod(n, 10) faz?", "n vira 53 e d vira 8", ["n vira 8 e d vira 53", "n vira 5 e d vira 38", "n vira 53.8"], "538 // 10 é 53 e 538 % 10 é 8.")]),
        L("Desafio: relógio digital",
          "Encadeando divmod você quebra um valor em várias partes, como notas de troco ou horas, minutos e segundos.",
          'troco = 87\nnotas50, troco = divmod(troco, 50)\nnotas10, troco = divmod(troco, 10)\nprint(notas50, "de 50,", notas10, "de 10, sobram", troco)',
          [OUT('n50, resto = divmod(130, 50)\nprint(n50, resto)', ["2 3", "3 0", "2.6 0"], "Cabem 2 notas de 50 (100) e sobram 30."),
           TYPE('print(sum(divmod(17, 5)))', "divmod(17, 5) é (3, 2), e 3 + 2 = 5."),
           MC("Quantas notas de 20 cabem em 95 reais?", "divmod(95, 20)[0]", ["divmod(95, 20)[1]", "divmod(20, 95)[0]", "95 % 20"], "O primeiro item é o quociente: 4."),
           CODE('Crie relogio(segundos) que devolve o texto "HH:MM:SS" com dois dígitos em cada parte. Ex.: relogio(3725) → "01:02:05".',
                'def relogio(segundos):\n    m, s = divmod(segundos, 60)\n    return f"{m}:{s}"\n',
                'def relogio(segundos):\n    h, resto = divmod(segundos, 3600)\n    m, s = divmod(resto, 60)\n    return f"{h:02d}:{m:02d}:{s:02d}"',
                'assert relogio(3725) == "01:02:05", "relogio(3725) deve ser 01:02:05"\nassert relogio(59) == "00:00:59", "relogio(59) deve ser 00:00:59"\nassert relogio(36000) == "10:00:00", "relogio(36000) deve ser 10:00:00"',
                'Use divmod duas vezes (3600 e 60) e formate com :02d.')]),
    ],
    # ------------------------------------------------------------------ sum
    "sum": [
        L("O valor inicial",
          "O segundo argumento de sum é o ponto de partida, e pode ser escrito como start=. sum também soma True e False, porque True vale 1 e False vale 0: ótimo para contar.",
          'print(sum([10, 20], 5))\nprint(sum([1, 2, 3], start=100))\nprint(sum([True, False, True]))\nprint(sum([1.5, 2.5]))',
          [OUT('print(sum([4, 6], 10))', ["10", "[4, 6, 10]", "46"], "Começa de 10 e soma 4 e 6: 20."),
           TYPE('print(sum([True, True, False, True]))', "Cada True vale 1."),
           MC("sum(numeros, 100) faz o quê?", "Soma os números começando de 100", ["Soma só os 100 primeiros", "Soma e divide por 100", "Dá erro"], "O 100 é o valor inicial da soma."),
           FILL("Complete para somar começando de 50.", 'print(sum([1, 2], ___=50))', "start", ["inicio", "begin", "first"], "O nome do parâmetro é start.")]),
        L("Carrinho, notas e placares",
          "sum resolve o total do carrinho, a média de notas (sum dividido por len) e o placar de um dicionário, somando d.values().",
          'carrinho = [12.5, 30, 7.5]\nprint("Total:", sum(carrinho))\nnotas = [8, 6, 10]\nprint("Média:", sum(notas) / len(notas))\ngols = {"Ana": 3, "Caio": 1, "Bia": 2}\nprint("Gols do time:", sum(gols.values()))',
          [TYPE('pontos = {"fase1": 100, "fase2": 250}\nprint(sum(pontos.values()))', "100 + 250."),
           OUT('notas = [5, 7, 9]\nprint(sum(notas) / len(notas))', ["7", "21", "7.5"], "21 / 3 = 7.0 (a divisão / sempre dá float)."),
           MC("Para somar só os preços acima de 10 da lista p, use…", "sum(x for x in p if x > 10)", ["sum(p > 10)", "sum(p) > 10", "sum(p, 10)"], "O if dentro do gerador filtra os itens."),
           CODE("Crie total_compra(precos, frete) que devolve a soma dos preços mais o frete.",
                "def total_compra(precos, frete):\n    return sum(precos)\n",
                "def total_compra(precos, frete):\n    return sum(precos, frete)",
                'assert total_compra([10, 20], 5) == 35, "total_compra([10, 20], 5) deve ser 35"\nassert total_compra([], 8) == 8, "total_compra([], 8) deve ser 8"\nassert total_compra([2.5, 2.5], 0) == 5.0, "total_compra([2.5, 2.5], 0) deve ser 5.0"',
                "sum(precos, frete) começa a soma pelo frete. sum(precos) + frete também vale.")]),
        L("Cuidados com sum",
          "sum recebe UMA coleção: sum(1, 2, 3) dá erro. Textos não se somam, então converta cada um com int(). E somas de decimais podem ter dígitos estranhos, como 0.30000000000000004.",
          'print(sum([1, 2, 3]))\ntry:\n    sum(1, 2, 3)\nexcept TypeError:\n    print("sum quer uma coleção")\ntextos = ["4", "5"]\nprint(sum(int(t) for t in textos))\nprint(sum([0.1, 0.2]))',
          [OUT('try:\n    print(sum(["1", "2"]))\nexcept TypeError:\n    print("erro")', ["3", "12", "['1', '2']"], "sum não soma textos: dá TypeError."),
           OUT('print(sum([[1], [2]], []))', ["3", "[[1], [2]]", "Erro"], "Começando de [], sum junta as listas: [1, 2]."),
           MC("Por que sum(5, 3) dá erro?", "sum recebe uma coleção, como sum([5, 3])", ["Porque 5 é maior que 3", "sum só soma decimais", "sum precisa de 3 números"], "O segundo argumento é o início, e o primeiro tem de ser uma coleção."),
           TYPE('print(sum(int(c) for c in "2024"))', "2 + 0 + 2 + 4.")]),
        L("sum com outras funções",
          "Com map(int, ...) você soma textos de números. Com len, soma tamanhos. Com zip, multiplica preço por quantidade. E sum(1 for ... if ...) conta quantos itens passam num teste.",
          'print(sum(map(int, "12345")))\npalavras = ["sol", "mar", "praia"]\nprint(sum(len(p) for p in palavras))\nprecos = [10, 5]\nqtds = [2, 3]\nprint(sum(p * q for p, q in zip(precos, qtds)))',
          [OUT('print(sum(map(int, ["3", "4"])))', ["34", "['3', '4']", "Erro"], "map transforma em números, e sum dá 7."),
           TYPE('print(sum(1 for n in [3, 8, 1, 9] if n > 2))', "Conta os maiores que 2: 3, 8 e 9."),
           ORDER("Monte o programa que soma preço vezes quantidade.", ['precos = [2, 5]', 'qtds = [3, 1]', 'print(sum(p * q for p, q in zip(precos, qtds)))'], "As listas vêm antes da soma: 2 × 3 + 5 × 1 = 11."),
           MC('sum(len(p) for p in ["oi", "tchau"]) dá…', "7", ["2", "oitchau", "5"], "2 letras + 5 letras.")]),
        L("Desafio: relatório de vendas",
          "Com sum, len, max e round você monta um relatório completo: total, média e o melhor dia.",
          'vendas = {"seg": 120, "ter": 80, "qua": 150}\ntotal = sum(vendas.values())\nprint("Total:", total)\nprint("Média:", round(total / len(vendas), 1))',
          [OUT('print(sum(range(1, 11)))', ["10", "45", "100"], "1 + 2 + … + 10 = 55."),
           TYPE('v = [10, 20, 30]\nprint(sum(v) - max(v))', "60 - 30."),
           MC("Qual expressão conta quantas notas da lista n são 7 ou mais?", "sum(1 for x in n if x >= 7)", ["sum(n >= 7)", "len(n) >= 7", "sum(n) >= 7"], "Soma 1 para cada nota que passa no teste."),
           CODE("Crie soma_pares(numeros) que devolve a soma só dos números pares da lista.",
                "def soma_pares(numeros):\n    return sum(numeros)\n",
                "def soma_pares(numeros):\n    return sum(n for n in numeros if n % 2 == 0)",
                'assert soma_pares([1, 2, 3, 4]) == 6, "soma_pares([1, 2, 3, 4]) deve ser 6"\nassert soma_pares([1, 3]) == 0, "soma_pares([1, 3]) deve ser 0"\nassert soma_pares([10, -2, 7]) == 8, "soma_pares([10, -2, 7]) deve ser 8"',
                "return sum(n for n in numeros if n % 2 == 0)")]),
    ],
    # ------------------------------------------------------------------ min
    "min": [
        L("Argumentos, coleções e empates",
          "min(4, 9, 1) e min([4, 9, 1]) dão o mesmo resultado. Textos são comparados em ordem alfabética, e tuplas pelo primeiro item. Se houver empate no critério, min devolve o primeiro que aparece.",
          'print(min(4, 9, 1))\nprint(min([4, 9, 1]))\nprint(min("banana", "abacate"))\nprint(min([(2, "b"), (1, "z"), (1, "a")]))',
          [OUT('print(min("zebra", "gato", "pato"))', ["zebra", "pato", "g"], "Em ordem alfabética, gato vem primeiro."),
           TYPE('print(min([(3, "c"), (1, "x"), (2, "a")]))', "As tuplas são comparadas pelo primeiro item: 1."),
           MC("min(7) faz o quê?", "Dá TypeError: um número sozinho não é uma coleção", ["Devolve 7", "Devolve 0", "Devolve None"], "Com um argumento só, min espera uma coleção."),
           OUT('print(min(["kiwi", "figo", "maçã"], key=len))', ["figo", "maçã", "4"], "Todas têm 4 letras: no empate, vale a primeira, kiwi.")]),
        L("Menor preço, mais novo",
          "Num dicionário, min(d) compara as CHAVES. Para o menor valor, use min(d.values()). Para a chave que tem o menor valor, use min(d, key=d.get).",
          'precos = {"arroz": 25, "feijão": 9, "café": 18}\nprint(min(precos.values()))\nprint(min(precos, key=precos.get))\nprint(min(precos))',
          [OUT('idades = {"Rex": 5, "Mia": 2, "Bob": 7}\nprint(min(idades))', ["Mia", "2", "Rex"], "min(d) compara as chaves em ordem alfabética: Bob."),
           TYPE('idades = {"Rex": 5, "Mia": 2, "Bob": 7}\nprint(min(idades, key=idades.get))', "key=idades.get compara as idades: Mia tem 2."),
           MC("Como achar o menor valor do dicionário d?", "min(d.values())", ["min(d)", "d.min()", "min(d.keys())"], "d.values() são os valores; min(d) olha as chaves."),
           CODE("Crie mais_barato(precos), que recebe um dicionário produto → preço e devolve o NOME do produto mais barato.",
                "def mais_barato(precos):\n    return min(precos.values())\n",
                "def mais_barato(precos):\n    return min(precos, key=precos.get)",
                'assert mais_barato({"pão": 8, "leite": 5, "queijo": 30}) == "leite", "Deve devolver leite"\nassert mais_barato({"a": 1}) == "a", "Com um produto só, devolva ele"\nassert mais_barato({"x": 9, "y": 3}) == "y", "Deve devolver y"',
                "min(precos, key=precos.get) devolve a chave com o menor preço.")]),
        L("Cuidados com min",
          "Textos são comparados letra a letra: maiúsculas vêm antes das minúsculas, e \"10\" vem antes de \"9\" porque 1 vem antes de 9. Misturar texto com número dá TypeError. Coleção vazia sem default dá ValueError.",
          'print(min("ana", "Zé"))\nprint(min("10", "9"))\nprint(min(10, 9))\nprint(min([], default=0))',
          [OUT('print(min(["banana", "Abacaxi", "caju"]))', ["banana", "caju", "abacaxi"], "Maiúsculas vêm antes: Abacaxi."),
           OUT('print(min(["30", "4", "100"]))', ["4", "30", "Erro"], "São textos: \"1\" vem antes de \"3\" e \"4\", então 100."),
           MC('O que acontece em min([3, "2", 1])?', "TypeError: não dá para comparar texto com número", ["Devolve 1", 'Devolve "2"', "Devolve 3"], "Python não sabe se 3 é menor que \"2\"."),
           FILL("Complete para não dar erro se a lista estiver vazia.", 'notas = []\nprint(min(notas, ___=0))', "default", ["key", "start", "vazio"], "default é o valor devolvido quando não há itens.")]),
        L("min com outras funções",
          "key=str.lower compara textos sem ligar para maiúsculas. map(int, ...) converte textos antes de comparar. E key=lambda escolhe qual parte do item comparar, como a idade numa tupla.",
          'nomes = ["bia", "Caio", "ana"]\nprint(min(nomes))\nprint(min(nomes, key=str.lower))\nprint(min(map(int, ["8", "3", "5"])))\nalunos = [("Ana", 7), ("Teo", 5)]\nprint(min(alunos, key=lambda a: a[1]))',
          [OUT('print(min(["Uva", "abacaxi", "Banana"], key=str.lower))', ["Banana", "Uva", "Abacaxi"], "Ignorando maiúsculas, abacaxi vem primeiro (e sai como está escrito)."),
           TYPE('print(min(len(p) for p in ["sol", "lua", "estrela"]))', "Os tamanhos são 3, 3 e 7."),
           OUT('pets = [("Rex", 5), ("Mia", 2)]\nprint(min(pets, key=lambda p: p[1])[0])', ["Rex", "2", "('Mia', 2)"], "O mais novo é ('Mia', 2); o [0] pega o nome."),
           ORDER("Monte o programa que mostra o menor número de uma lista de textos.", ['textos = ["12", "7", "30"]', 'numeros = list(map(int, textos))', 'print(min(numeros))'], "Converta para int antes de comparar: 7.")]),
        L("Desafio: recorde de tempo",
          "Em corridas, o menor tempo vence. Junte min com key e default para achar o vencedor e lidar com listas vazias.",
          'tempos = {"Ana": 12.4, "Caio": 11.9, "Bia": 12.1}\nvencedor = min(tempos, key=tempos.get)\nprint(f"{vencedor} venceu com {tempos[vencedor]}s")',
          [OUT('print(min(5, max(2, 8)))', ["2", "8", "5 8"], "max(2, 8) é 8, e min(5, 8) é 5."),
           TYPE('print(min([], default="sem tempos"))', "A lista está vazia, então vale o default."),
           MC("Qual expressão limita x a no máximo 100?", "min(x, 100)", ["max(x, 100)", "min(100)", "x.min(100)"], "Se x passar de 100, min escolhe o 100."),
           CODE("Crie melhor_volta(voltas) que devolve o menor tempo da lista, ou None se a lista estiver vazia.",
                "def melhor_volta(voltas):\n    return min(voltas)\n",
                "def melhor_volta(voltas):\n    return min(voltas, default=None)",
                'assert melhor_volta([62.5, 60.1, 61.0]) == 60.1, "Deve devolver 60.1"\nassert melhor_volta([]) is None, "Lista vazia deve devolver None"\nassert melhor_volta([70]) == 70, "Com uma volta só, devolva ela"',
                "min(voltas, default=None) evita o ValueError da lista vazia.")]),
    ],
    # ------------------------------------------------------------------ max
    "max": [
        L("key e default no max",
          "Como no min, key muda o critério: key=abs compara pelo tamanho e key=len pelo comprimento. No empate, max devolve o primeiro. default evita erro com coleção vazia.",
          'print(max([3, -10, 7], key=abs))\nprint(max(["sol", "mar", "lua"], key=len))\nprint(max([], default="nada"))',
          [OUT('print(max([-8, 5, 3], key=abs))', ["5", "8", "3"], "Pelo tamanho, -8 é o maior, e ele sai com o sinal."),
           TYPE('print(max(["ok", "oi", "ei"], key=len))', "Todas têm 2 letras: vale a primeira."),
           OUT('print(max([], default=0))', ["Erro", "None", "[]"], "Lista vazia com default devolve o default: 0."),
           MC("Quando há empate no critério do key, max devolve…", "O primeiro que aparece", ["O último que aparece", "Uma lista com todos", "Dá erro"], "Ele só troca quando acha um item MAIOR.")]),
        L("Recordes e campeões",
          "max acha o recorde de uma lista e, com key=d.get, o campeão de um dicionário. max(lista) - min(lista) dá a variação entre o maior e o menor.",
          'pontos = [120, 340, 95]\nprint("Recorde:", max(pontos))\nnotas = {"Ana": 8.5, "Caio": 9.7, "Bia": 9.1}\nmelhor = max(notas, key=notas.get)\nprint("Melhor aluno:", melhor, notas[melhor])',
          [TYPE('temps = [28, 31, 25, 33]\nprint(max(temps) - min(temps))', "33 - 25."),
           OUT('vendas = {"jan": 50, "fev": 80, "mar": 70}\nprint(max(vendas))', ["fev", "80", "jan"], "max(d) compara as chaves: mar é a maior em ordem alfabética."),
           MC("Para saber o mês com mais vendas no dicionário v, use…", "max(v, key=v.get)", ["max(v)", "max(v.values())", "v.max()"], "key=v.get compara pelos valores e devolve a chave."),
           CODE("Crie campeao(placar), que recebe um dicionário nome → pontos e devolve o NOME de quem fez mais pontos.",
                "def campeao(placar):\n    return max(placar)\n",
                "def campeao(placar):\n    return max(placar, key=placar.get)",
                'assert campeao({"Ana": 10, "Teo": 15, "Bia": 12}) == "Teo", "Deve devolver Teo"\nassert campeao({"Zeca": 3, "Ana": 9}) == "Ana", "Deve devolver Ana, que tem 9 pontos"\nassert campeao({"Solo": 1}) == "Solo", "Com um jogador só, devolva ele"',
                "max(placar, key=placar.get) compara os pontos e devolve o nome.")]),
        L("Cuidados com max",
          "Com textos, \"9\" é maior que \"10\", porque a comparação é letra a letra; use key=int. Minúsculas são \"maiores\" que maiúsculas. Coleção vazia sem default dá ValueError.",
          'print(max("9", "10"))\nprint(max(9, 10))\nprint(max(["8", "12"], key=int))\ntry:\n    max([])\nexcept ValueError:\n    print("lista vazia: use default")',
          [OUT('print(max(["100", "25", "3"]))', ["100", "25", "Erro"], "São textos: \"3\" vem depois de \"1\" e \"2\"."),
           OUT('print(max(["abacate", "Zebra"]))', ["Zebra", "Erro", "Z"], "Minúsculas vêm depois das maiúsculas: abacate."),
           MC('Como achar o maior número na lista de textos t = ["8", "12"]?', "max(t, key=int)", ["max(t)", "int(max(t))", "max(int(t))"], "key=int compara como número, mas devolve o texto \"12\"."),
           FILL("Complete com o erro que max([]) causa.", 'try:\n    max([])\nexcept ___:\n    print("vazia")', "ValueError", ["TypeError", "IndexError", "KeyError"], "Coleção vazia não tem maior valor: ValueError.")]),
        L("max com outras funções",
          "max(map(len, palavras)) dá o tamanho da maior palavra. max(0, min(x, 100)) prende x entre 0 e 100. E max(zip(pontos, nomes)) acha o maior ponto junto com o dono.",
          'palavras = ["sol", "girassol", "mar"]\nprint(max(map(len, palavras)))\nvida = 120\nprint(max(0, min(vida, 100)))\nnomes = ["Ana", "Caio"]\npontos = [30, 45]\nprint(max(zip(pontos, nomes)))',
          [OUT('print(max(0, min(-20, 100)))', ["-20", "100", "20"], "min(-20, 100) é -20, e max(0, -20) é 0."),
           TYPE('print(max(map(len, ["oi", "tchau", "bom"])))', "Os tamanhos são 2, 5 e 3."),
           OUT('print(max(zip([7, 9], ["Ana", "Teo"]))[1])', ["9", "Ana", "(9, 'Teo')"], "O maior par é (9, 'Teo'); o [1] pega o nome."),
           ORDER("Monte o programa que mostra a palavra mais longa da frase.", ['frase = "o rato roeu a roupa"', 'palavras = frase.split()', 'print(max(palavras, key=len))'], "Divida a frase e compare pelo tamanho: roupa.")]),
        L("Desafio: termômetro",
          "Juntando max, min e key você analisa dados de verdade: o dia mais quente, o mais frio e a variação da semana.",
          'temps = {"seg": 24, "ter": 31, "qua": 27}\ndia = max(temps, key=temps.get)\nprint(f"Dia mais quente: {dia} ({temps[dia]}°C)")\nprint("Variação:", max(temps.values()) - min(temps.values()))',
          [OUT('print(max(min(3, 7), min(5, 2)))', ["7", "2", "5"], "min(3, 7) é 3, min(5, 2) é 2, e o maior dos dois é 3."),
           TYPE('print(max("abacaxi"))', "Num texto, max compara as letras: x vem por último."),
           MC("Qual expressão garante que a vida nunca passe de 100 nem fique abaixo de 0?", "max(0, min(vida, 100))", ["min(0, max(vida, 100))", "max(vida, 100)", "min(vida, 0)"], "min corta o teto em 100 e max corta o piso em 0."),
           CODE("Crie maior_diferenca(numeros) que devolve o maior menos o menor número da lista, ou 0 se a lista estiver vazia.",
                "def maior_diferenca(numeros):\n    return max(numeros)\n",
                "def maior_diferenca(numeros):\n    if not numeros:\n        return 0\n    return max(numeros) - min(numeros)",
                'assert maior_diferenca([3, 9, 1]) == 8, "maior_diferenca([3, 9, 1]) deve ser 8"\nassert maior_diferenca([5]) == 0, "maior_diferenca([5]) deve ser 0"\nassert maior_diferenca([]) == 0, "Lista vazia deve dar 0"',
                "Trate a lista vazia antes e depois devolva max(numeros) - min(numeros).")]),
    ],
}

BUGS = r'''
@fn_abs 3
temp_manha = 15
temp_tarde = 22
print(temp_manha - temp_tarde)  # esperado: 7
>>> print(abs(temp_manha - temp_tarde))  # esperado: 7
!! A diferença deu negativa. Use abs() para tirar o sinal.

@fn_abs 2
valor = "-12"
print(abs(valor))
>>> print(abs(int(valor)))
!! abs não funciona com texto. Converta com int() antes.

@fn_abs 3
a = -4
b = 6
print(abs(a) - abs(b))  # esperado: 10
>>> print(abs(a - b))  # esperado: 10
!! abs(a) - abs(b) não é a distância. Faça a diferença primeiro e depois use abs.

@fn_abs 2
saldo = -50
print("Dívida:", abs saldo)
>>> print("Dívida:", abs(saldo))
!! Faltaram os parênteses na chamada de abs.

@fn_abs 2
def distancia(a, b):
    return abs(a) - b
print(distancia(3, 10))  # esperado: 7
>>> return abs(a - b)
!! O abs tem de envolver a diferença inteira: abs(a - b).

@fn_abs 2
numeros = [-3, 1, -2]
print(abs(numeros))
>>> print([abs(n) for n in numeros])
!! abs trabalha com um número de cada vez. Aplique abs em cada item.

@fn_round 2
media = 7.456
print(round(media 2))
>>> print(round(media, 2))
!! Faltou a vírgula entre o número e as casas.

@fn_round 2
preco = 19.987
print(round(preco))  # esperado: 19.99
>>> print(round(preco, 2))  # esperado: 19.99
!! Sem o segundo argumento, round arredonda para inteiro.

@fn_round 2
nota = "8.76"
print(round(nota, 1))
>>> print(round(float(nota), 1))
!! round não arredonda texto. Converta com float() antes.

@fn_round 2
total = 10 / 3
print(round(2, total))  # esperado: 3.33
>>> print(round(total, 2))  # esperado: 3.33
!! A ordem é round(número, casas): primeiro o número.

@fn_round 2
preco = 9.5
print(round(preco, 2))  # esperado: 9.50
>>> print(f"{preco:.2f}")  # esperado: 9.50
!! round não acrescenta zeros no final. Para mostrar 9.50, formate com :.2f.

@fn_round 2
notas = [7, 8, 8]
media = round(sum(notas)) / len(notas)
print(media)  # esperado: 7.7
>>> media = round(sum(notas) / len(notas), 1)
!! O round foi feito antes da divisão. Arredonde o resultado final, com 1 casa.

@fn_pow 2
lado = 4
print(lado ^ 2)  # esperado: 16
>>> print(pow(lado, 2))  # esperado: 16
!! ^ não é potência em Python. Use pow(lado, 2) ou lado ** 2.

@fn_pow 1
area = pow(5)
print(area)
>>> area = pow(5, 2)
!! pow precisa de dois valores: a base e o expoente.

@fn_pow 1
raiz = pow(25, 1 // 2)
print(raiz)  # esperado: 5.0
>>> raiz = pow(25, 0.5)
!! 1 // 2 é divisão inteira e dá 0, e tudo elevado a 0 é 1. Use 0.5.

@fn_pow 3
capital = 1000
taxa = 0.1
print(round(capital * pow(taxa, 2), 2))  # esperado: 1210.0
>>> print(round(capital * pow(1 + taxa, 2), 2))  # esperado: 1210.0
!! O fator de crescimento é 1 + taxa, não só a taxa.

@fn_pow 2
n = -3
quadrado = -3 ** 2
print(quadrado)  # esperado: 9
>>> quadrado = pow(n, 2)
!! -3 ** 2 vira -(3 ** 2). Com pow(n, 2), o sinal entra na conta.

@fn_pow 2
base = "2"
print(pow(base, 3))
>>> print(pow(int(base), 3))
!! pow precisa de números. Converta o texto com int().

@fn_divmod 2
total = 135
horas, minutos = divmod(60, total)
print(horas, minutos)  # esperado: 2 15
>>> horas, minutos = divmod(total, 60)
!! A ordem é divmod(dividendo, divisor): primeiro o total.

@fn_divmod 2
ovos = 40
caixas, sobra, extra = divmod(ovos, 12)
print(caixas, sobra)
>>> caixas, sobra = divmod(ovos, 12)
!! divmod devolve só dois valores: o quociente e o resto.

@fn_divmod 3
segundos = 200
m, s = divmod(segundos, 60)
print(f"{s}min {m}s")  # esperado: 3min 20s
>>> print(f"{m}min {s}s")  # esperado: 3min 20s
!! O primeiro valor é o quociente (minutos) e o segundo é o resto (segundos).

@fn_divmod 1
pessoas = 0
grupos, sobra = divmod(10, pessoas)
print(grupos, sobra)
>>> pessoas = 3
!! Não dá para dividir por zero: o divisor precisa ser diferente de 0.

@fn_divmod 2
minutos = "90"
h, m = divmod(minutos, 60)
print(h, m)
>>> h, m = divmod(int(minutos), 60)
!! divmod precisa de números. O texto "90" tem de virar int.

@fn_divmod 2
resultado = divmod(17, 5)
print("Resto:", resultado[0])  # esperado: Resto: 2
>>> print("Resto:", resultado[1])  # esperado: Resto: 2
!! O resto é o segundo item da tupla, o de índice 1.

@fn_sum 1
print(sum(1, 2, 3))
>>> print(sum([1, 2, 3]))
!! sum recebe uma coleção. Coloque os números numa lista.

@fn_sum 2
notas = [8, 6, 10]
media = sum(notas) / 2
print(media)  # esperado: 8.0
>>> media = sum(notas) / len(notas)
!! Divida pela quantidade de notas, com len(notas), e não por um número fixo.

@fn_sum 2
precos = ["10", "20"]
print(sum(precos))
>>> print(sum(int(p) for p in precos))
!! Os preços estão como texto. Converta cada um para número.

@fn_sum 2
pontos = [5, 10, 15]
total = sum(pontos, 100)
print(total)  # esperado: 30
>>> total = sum(pontos)
!! O segundo argumento é o valor inicial: com 100, a soma começa de 100.

@fn_sum 1
sum = 10
valores = [1, 2]
print(sum(valores))
>>> extra = 10
!! Uma variável chamada sum apaga a função sum. Use outro nome.

@fn_sum 2
carrinho = {"pão": 8, "leite": 5}
print(sum(carrinho))
>>> print(sum(carrinho.values()))
!! Somar o dicionário tenta somar as chaves (os nomes). Use .values() para somar os preços.

@fn_min 2
idades = []
print(min(idades))
>>> print(min(idades, default=0))
!! min de lista vazia dá ValueError. Use default.

@fn_min 2
tempos = {"Ana": 12, "Caio": 9}
print(min(tempos))  # esperado: Caio
>>> print(min(tempos, key=tempos.get))  # esperado: Caio
!! min(dicionário) compara as chaves. Use key=tempos.get para comparar os tempos.

@fn_min 2
notas = ["9", "10", "7"]
print(min(notas))  # esperado: 7
>>> print(min(notas, key=int))  # esperado: 7
!! Textos são comparados letra a letra. key=int compara como número.

@fn_min 2
a, b, c = 4, 2, 9
print(min[a, b, c])
>>> print(min(a, b, c))
!! min é uma função: use parênteses, não colchetes.

@fn_min 2
palavras = ["sol", "abacaxi", "uva"]
print(min(palavras, key=len()))
>>> print(min(palavras, key=len))
!! Passe len sem parênteses; o min chama a função em cada item.

@fn_min 2
nomes = ["bia", "Caio", "ana"]
print(min(nomes))  # esperado: ana
>>> print(min(nomes, key=str.lower))  # esperado: ana
!! Maiúsculas vêm antes das minúsculas. key=str.lower compara sem ligar para isso.

@fn_max 2
notas = {"Ana": 9, "Bia": 10, "Caio": 7}
print(max(notas))  # esperado: Bia
>>> print(max(notas, key=notas.get))  # esperado: Bia
!! max(dicionário) compara os nomes. Use key=notas.get para comparar as notas.

@fn_max 2
pontos = []
print(max(pontos))
>>> print(max(pontos, default=0))
!! max de lista vazia dá ValueError. Use default.

@fn_max 2
palavras = ["sol", "girassol", "mar"]
print(max(palavras))  # esperado: girassol
>>> print(max(palavras, key=len))  # esperado: girassol
!! Sem key, max compara em ordem alfabética. key=len compara pelo tamanho.

@fn_max 1
numeros = [3, "7", 5]
print(max(numeros))
>>> numeros = [3, 7, 5]
!! Não dá para comparar texto com número. O 7 precisa ser número, sem aspas.

@fn_max 2
vida = 150
vida = max(vida, 100)
print(vida)  # esperado: 100
>>> vida = min(vida, 100)
!! Para limitar a no máximo 100, use min. max(vida, 100) nunca deixa a vida abaixo de 100.

@fn_max 2
temps = [28, 31, 25]
print(max(temps) - max(temps))  # esperado: 6
>>> print(max(temps) - min(temps))  # esperado: 6
!! A variação é o maior menos o MENOR. Troque o segundo max por min.
'''
