from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ------------------------------------------------------------------ int
    "int": [
        # lição 2
        L("Bases, sinais e espaços",
          "int ignora espaços nas pontas e entende sinais + e -. O segundo argumento é a base: 2 para binário, 8 para octal, 16 para hexadecimal. Sem nada dentro, int() devolve 0.",
          'print(int("  -15 "))\nprint(int("+7"))\nprint(int("1010", 2))\nprint(int("17", 8))\nprint(int())',
          [OUT('print(int("  -8  ") * 2)', ["-8-8", "Erro", "16"], "Os espaços somem e o sinal fica: -8 * 2 = -16."),
           TYPE('print(int("17", 8))', "Na base 8, 17 vale 1 * 8 + 7 = 15."),
           MC("Quanto vale int() sem nada dentro?", "0", ["None", "Dá erro", "1"], "Sem argumento, int devolve zero."),
           FILL('Complete para ler "1010" como binário e obter 10.', 'print(int("1010", ___))', "2", ["10", "8", "16"], "Binário é a base 2.")]),
        # lição 3
        L("Texto que vira conta",
          "Números que chegam como texto (de um formulário ou arquivo) precisam de int antes de fazer contas. Sem converter, o + só cola os textos.",
          'texto = "25"\nidade = int(texto)\nprint(idade + 1)\nprecos = ["10", "20", "5"]\ntotal = 0\nfor p in precos:\n    total += int(p)\nprint(total)',
          [OUT('notas = ["7", "8", "10"]\nprint(notas[0] + notas[1])', ["15", "7 8", "Erro"], "São textos, então o + cola: \"7\" + \"8\" dá 78."),
           TYPE('print(int("7") + int("8"))', "Agora são números: 7 + 8."),
           OUT('print(int(9.99) + int(-9.99))', ["1", "-1", "20"], "int corta a parte decimal: 9 + (-9) = 0."),
           CODE('A lista pedidos = ["3", "5", "2"] tem quantidades em texto. Some tudo como número na variável total e mostre total.',
                'pedidos = ["3", "5", "2"]\ntotal = 0\n# some as quantidades aqui\nprint(total)',
                'pedidos = ["3", "5", "2"]\ntotal = 0\nfor p in pedidos:\n    total += int(p)\nprint(total)',
                'assert total == 10, "total deve ser 10"\nassert __stdout__.strip() == "10", "Mostre o total: 10"',
                "for p in pedidos: total += int(p)")]),
        # lição 4
        L("Quando int dá erro",
          "int só aceita texto com algarismos inteiros. Texto vazio, com ponto, vírgula ou letras dá ValueError. Para \"3.5\", passe antes por float. Para None, o erro é TypeError.",
          'try:\n    int("dez")\nexcept ValueError:\n    print("dez não é número")\nprint(int(float("3.5")))\nprint("12".isdigit())',
          [MC("Qual destes dá ValueError?", 'int("")', ['int("0")', 'int(" 5 ")', "int(5.9)"], "Texto vazio não tem número nenhum para ler."),
           OUT('try:\n    print(int("4,5"))\nexcept ValueError:\n    print("inválido")', ["4", "45", "4.5"], "A vírgula não é aceita, então cai no except."),
           TYPE('print(int(float("7.9")))', "float lê 7.9 e int corta para 7."),
           OUT('try:\n    print(int(None))\nexcept Exception as e:\n    print(type(e).__name__)', ["ValueError", "0", "None"], "None nem é texto nem número: o erro é TypeError.")]),
        # lição 5
        L("int junto com outras funções",
          "int combina bem com str (para separar dígitos), com split e map (para ler vários números de uma vez) e com round (quando você quer arredondar em vez de cortar).",
          'n = 472\nsoma = 0\nfor d in str(n):\n    soma += int(d)\nprint(soma)\nnums = list(map(int, "4 8 15".split()))\nprint(nums)',
          [OUT('print(list(map(int, "1 2 3".split())))', ["['1', '2', '3']", "[123]", "1 2 3"], "map aplica int em cada pedaço do split."),
           TYPE('print(int(str(5) + str(3)) + 1)', "\"5\" + \"3\" é \"53\"; como número, 53 + 1."),
           MC("Para transformar 2.7 em 3, use…", "round(2.7)", ["int(2.7)", 'int("2.7")', "float(2.7)"], "int corta (daria 2); round arredonda."),
           ORDER("Monte o programa que soma os dígitos de 305.", ['soma = 0', 'for d in "305":', '    soma += int(d)', 'print(soma)'], "Comece do zero, some cada dígito convertido e mostre no fim.")]),
        # lição 6
        L("Desafio: etiquetas da loja",
          "Juntando tudo: separe o texto, pegue o pedaço com o número e converta com int. Se algo não for número, try/except evita que o programa quebre.",
          'etiqueta = "Preço: 35 reais"\npartes = etiqueta.split()\nvalor = int(partes[1])\nprint(valor * 2)',
          [OUT('print(int("0012") + 1)', ["0013", "121", "Erro"], "Zeros à esquerda são ignorados: 12 + 1."),
           TYPE('print(int("11", 2) + int("11", 10))', "\"11\" em binário é 3; em decimal é 11. 3 + 11."),
           CODE("Crie a função somar_digitos(n) que devolve a soma dos dígitos do inteiro n. Ex.: somar_digitos(472) devolve 13.",
                'def somar_digitos(n):\n    pass\n',
                'def somar_digitos(n):\n    soma = 0\n    for d in str(n):\n        soma += int(d)\n    return soma',
                'assert somar_digitos(472) == 13, "somar_digitos(472) deve devolver 13"\nassert somar_digitos(5) == 5, "somar_digitos(5) deve devolver 5"\nassert somar_digitos(0) == 0, "somar_digitos(0) deve devolver 0"',
                "Transforme n em texto, percorra os dígitos e some int(d)."),
           CODE('Crie a função para_inteiros(textos) que devolve uma lista só com os textos que viram int, já convertidos. Ex.: para_inteiros(["3", "x", "10"]) devolve [3, 10].',
                'def para_inteiros(textos):\n    pass\n',
                'def para_inteiros(textos):\n    nums = []\n    for t in textos:\n        try:\n            nums.append(int(t))\n        except ValueError:\n            pass\n    return nums',
                'assert para_inteiros(["3", "x", "10"]) == [3, 10], "Esperado [3, 10]"\nassert para_inteiros([]) == [], "Lista vazia deve devolver []"\nassert para_inteiros(["a", "b"]) == [], "Sem números, devolva []"',
                "Use try/except ValueError em volta do int(t).")]),
    ],
    # ------------------------------------------------------------------ float
    "float": [
        # lição 2
        L("Formatos que float entende",
          "float aceita \".5\" (sem o zero), notação científica como \"2e3\" (2 vezes 10 elevado a 3) e números negativos. float() sem nada dá 0.0, e float(True) dá 1.0.",
          'print(float(".5"))\nprint(float("-2.5e2"))\nprint(float())\nprint(float(True))',
          [OUT('print(float("3"))', ["3", "3,0", "Erro"], "Todo float aparece com ponto e casa decimal: 3.0."),
           TYPE('print(float("2e3"))', "2e3 é 2 * 1000, como float."),
           MC("O que float() sem nada devolve?", "0.0", ["0", "None", "Dá erro"], "Sem argumento, float devolve zero com ponto."),
           FILL("Complete para obter 1.5 a partir de um texto.", 'print(float(___))', '"1.5"', ['"1,5"', '"1 .5"', '"um e meio"'], "Só o texto com ponto e sem espaço no meio funciona.")]),
        # lição 3
        L("Preços e médias",
          "Preços e notas costumam ter casas decimais, então use float. Lembre: a divisão com / sempre devolve float, mesmo quando a conta é exata.",
          'precos = ["4.50", "3.25", "2.25"]\ntotal = 0.0\nfor p in precos:\n    total += float(p)\nprint(total)\nprint(f"R$ {total:.2f}")',
          [OUT('print(float("2.5") + float("2.5"))', ["2.52.5", "5", "Erro"], "Convertidos, viram números: 2.5 + 2.5 = 5.0."),
           TYPE('print(10 / 4)', "A barra simples faz a divisão com decimais."),
           OUT('print(type(8 / 2).__name__)', ["int", "4", "4.0"], "Mesmo dando conta exata, / devolve float."),
           CODE('Converta o texto preco = "19.90" em número e guarde em novo_preco o preço com 10% de desconto (multiplique por 0.9).',
                'preco = "19.90"\nnovo_preco = preco\n',
                'preco = "19.90"\nnovo_preco = float(preco) * 0.9',
                'assert isinstance(novo_preco, float), "novo_preco precisa ser um número float"\nassert round(novo_preco, 2) == 17.91, "Com 10% de desconto, 19.90 vira 17.91"',
                "novo_preco = float(preco) * 0.9")]),
        # lição 4
        L("Cuidados com float",
          "O computador guarda floats em binário, então algumas contas saem com um restinho, como 0.30000000000000004. Para comparar, arredonde antes. E float(\"nan\") é diferente até dele mesmo.",
          'x = 0.1 + 0.2\nprint(x)\nprint(round(x, 2) == 0.3)\nnan = float("nan")\nprint(nan == nan)',
          [OUT('print(0.1 * 3)', ["0.3", "0.30", "Erro"], "Aparece o restinho do binário: 0.30000000000000004."),
           MC("Qual é o jeito seguro de comparar 0.1 + 0.2 com 0.3?", "round(0.1 + 0.2, 2) == 0.3", ["0.1 + 0.2 == 0.3", "float(0.1 + 0.2) == 0.3", "int(0.1 + 0.2) == 0.3"], "Arredondar tira o restinho antes de comparar."),
           TYPE('print(float("inf") > 10 ** 100)', "Infinito é maior que qualquer número."),
           OUT('try:\n    float("R$ 5")\nexcept ValueError:\n    print("não deu")\nelse:\n    print("deu")', ["deu", "5.0", "R$ 5.0"], "O símbolo R$ não é número, então dá ValueError.")]),
        # lição 5
        L("float com outras funções",
          "Para ler números com vírgula, troque por ponto com replace antes do float. round arredonda o resultado, map converte vários de uma vez e .is_integer() diz se não há parte decimal.",
          'texto = "3,75"\nvalor = float(texto.replace(",", "."))\nprint(valor)\nprint(round(valor, 1))\nprint((4.0).is_integer())',
          [OUT('print(float("2,5".replace(",", ".")) * 2)', ["2,52,5", "Erro", "5"], "Depois do replace, \"2.5\" vira 2.5; vezes 2 dá 5.0."),
           TYPE('print(sum(map(float, ["1.5", "2.5"])))', "map converte os dois e sum soma: 1.5 + 2.5."),
           MC("Como saber se 6.0 não tem parte decimal?", "(6.0).is_integer()", ["int(6.0)", "float(6)", "round(6.0)"], "is_integer devolve True quando a parte decimal é zero."),
           ORDER('Monte o programa que lê a nota "8,5" e mostra o dobro.', ['nota = "8,5"', 'nota = nota.replace(",", ".")', 'valor = float(nota)', 'print(valor * 2)'], "Primeiro troque a vírgula, depois converta, depois calcule.")]),
        # lição 6
        L("Desafio: média da turma",
          "Juntando tudo: separe as notas do texto, converta cada uma com float, calcule a média e mostre com casas decimais controladas.",
          'notas = "7.5 8 9.5"\nlista = [float(n) for n in notas.split()]\nmedia = sum(lista) / len(lista)\nprint(f"Média: {media:.1f}")',
          [OUT('print(float(int(7.8)))', ["7.8", "8.0", "7"], "int corta para 7 e float devolve 7.0."),
           TYPE('print(float("1.25") * 4)', "1.25 * 4 é 5, mas como float: 5.0."),
           CODE('Crie a função media(textos) que recebe notas em texto, como ["7", "8.5"], e devolve a média como float.',
                'def media(textos):\n    pass\n',
                'def media(textos):\n    nums = [float(t) for t in textos]\n    return sum(nums) / len(nums)',
                'assert media(["7", "8"]) == 7.5, "media([\\"7\\", \\"8\\"]) deve ser 7.5"\nassert media(["10"]) == 10.0, "media([\\"10\\"]) deve ser 10.0"\nassert isinstance(media(["6", "9"]), float), "Devolva um float"',
                "Converta cada nota com float, some e divida pela quantidade.")]),
    ],
    # ------------------------------------------------------------------ str
    "str": [
        # lição 2
        L("O que cada tipo vira",
          "str funciona com qualquer valor: None vira \"None\", True vira \"True\" e 2.50 vira \"2.5\" (zeros finais somem). Uma lista vira o texto com colchetes e aspas. str() sem nada dá texto vazio.",
          'print(str(None))\nprint(str(True) + "!")\nprint(str(2.50))\nprint(len(str()))',
          [OUT('print(str(2.50))', ["2.50", "2,5", "Erro"], "O float 2.50 é o mesmo que 2.5, e é assim que vira texto."),
           TYPE('print(str(False) + str(0))', "\"False\" + \"0\" são colados."),
           MC("Quanto vale len(str())?", "0", ["1", "None", "Dá erro"], "str() é o texto vazio, com 0 caracteres."),
           OUT('print(str(["a", "b"]))', ["a b", "ab", "[a, b]"], "A lista vira texto do jeito que aparece no código: ['a', 'b'].")]),
        # lição 3
        L("Montando mensagens",
          "Com str você junta números a textos usando +. Depois de virar texto, o número ganha métodos de texto, como zfill (zeros à esquerda) e fatias [ ].",
          'pedido = 7\nprint("Pedido #" + str(pedido).zfill(3))\nano = 2026\nprint(str(ano)[-2:])',
          [OUT('print(str(5).zfill(3))', ["5", "500", "00 5"], "zfill completa com zeros à esquerda até 3 caracteres."),
           TYPE('print(str(2026)[:2])', "Os dois primeiros caracteres de \"2026\"."),
           FILL("Complete para mostrar: Nível 3", 'nivel = 3\nprint("Nível " + ___(nivel))', "str", ["int", "float", "print"], "Para colar com +, o número precisa virar texto."),
           CODE("Com pontos = 42, monte na variável msg o texto Você fez 42 pontos usando + e str(), e mostre msg.",
                'pontos = 42\nmsg = ""\nprint(msg)',
                'pontos = 42\nmsg = "Você fez " + str(pontos) + " pontos"\nprint(msg)',
                'assert msg == "Você fez 42 pontos", "msg deve ser: Você fez 42 pontos"\nassert "Você fez 42 pontos" in __stdout__, "Mostre msg com print"',
                'msg = "Você fez " + str(pontos) + " pontos"')]),
        # lição 4
        L("Pegadinhas do str",
          "Texto e número nunca são iguais: str(10) == 10 é False. Textos com + se colam, com * se repetem, e são comparados letra a letra, por isso \"10\" < \"9\" é True.",
          'print("10" + "5")\nprint(str(10) == 10)\nprint("10" < "9")',
          [OUT('print(str(7) * 3)', ["21", "7 7 7", "Erro"], "Texto vezes 3 repete o texto: 777."),
           MC('Por que "10" < "9" é True?', 'Textos são comparados letra a letra, e "1" vem antes de "9"', ["Porque 10 é menor que 9", "É um erro do Python", 'Porque "10" tem mais letras'], "Para comparar como número, converta com int."),
           OUT('try:\n    print("Vidas: " + 3)\nexcept Exception as e:\n    print(type(e).__name__)', ["Vidas: 3", "ValueError", "SyntaxError"], "Texto + número dá TypeError: faltou str(3)."),
           TYPE('print(str(10) == "10")', "Agora os dois lados são texto.")]),
        # lição 5
        L("str com outras funções",
          "join só junta textos, então use map(str, lista) para converter os números antes. E len(str(n)) conta quantos dígitos um número tem.",
          'nums = [3, 1, 2]\nprint(", ".join(map(str, nums)))\nprint(len(str(1000000)))',
          [OUT('print("-".join(map(str, [1, 2, 3])))', ["1 2 3", "6", "Erro"], "Cada número vira texto e o join põe - entre eles."),
           TYPE('print(len(str(2 ** 10)))', "2 ** 10 é 1024, que tem 4 dígitos."),
           MC('Por que ", ".join([1, 2]) dá erro?', "join só aceita textos; use map(str, ...)", ["Falta o print", "A vírgula é proibida", "join só funciona com tuplas"], "Os itens precisam ser textos."),
           CODE("Crie a função digitos(n) que devolve quantos dígitos tem o inteiro positivo n. Ex.: digitos(2026) devolve 4.",
                'def digitos(n):\n    pass\n',
                'def digitos(n):\n    return len(str(n))',
                'assert digitos(2026) == 4, "digitos(2026) deve devolver 4"\nassert digitos(7) == 1, "digitos(7) deve devolver 1"\nassert digitos(100000) == 6, "digitos(100000) deve devolver 6"',
                "return len(str(n))")]),
        # lição 6
        L("Desafio: gerador de cupom",
          "Juntando tudo: converta números com str, complete com zfill e cole as partes com + para criar códigos com formato fixo.",
          'codigo = 7\nano = 26\ncupom = "PY" + str(ano) + "-" + str(codigo).zfill(4)\nprint(cupom)',
          [OUT('print(str(12) + str(3) == str(123))', ["False", "Erro", "15"], "\"12\" + \"3\" é \"123\", igual a str(123)."),
           TYPE('print(str(3.0) + str(3))', "\"3.0\" + \"3\" são colados."),
           CODE('Crie a função cupom(numero) que devolve "CUP-" seguido do número com 4 dígitos (zeros à esquerda). Ex.: cupom(42) devolve "CUP-0042".',
                'def cupom(numero):\n    return "CUP-" + numero\n',
                'def cupom(numero):\n    return "CUP-" + str(numero).zfill(4)',
                'assert cupom(42) == "CUP-0042", "cupom(42) deve devolver CUP-0042"\nassert cupom(7) == "CUP-0007", "cupom(7) deve devolver CUP-0007"\nassert cupom(1234) == "CUP-1234", "cupom(1234) deve devolver CUP-1234"',
                'return "CUP-" + str(numero).zfill(4)')]),
    ],
    # ------------------------------------------------------------------ bool
    "bool": [
        # lição 2
        L("True e False são números",
          "No Python, True vale 1 e False vale 0 nas contas. Por isso sum() de uma lista de comparações conta quantas deram True. bool() sem nada dá False, e qualquer número diferente de zero, até negativo, é True.",
          'print(bool())\nprint(bool(-1))\nprint(True + True)\nprint(sum([True, False, True]))',
          [OUT('print(bool(-0.5))', ["False", "-0.5", "Erro"], "Só o zero é falso; -0.5 não é zero."),
           TYPE('print(True * 10)', "True vale 1 nas contas."),
           MC("Qual destes é False?", "bool(0.0)", ["bool(-1)", 'bool("0")', "bool([[]])"], "0.0 é zero. \"0\" é texto com conteúdo e [[]] é uma lista com um item."),
           FILL("Complete para contar quantas notas são 7 ou mais.", 'notas = [5, 8, 9, 6]\nprint(___(n >= 7 for n in notas))', "sum", ["len", "bool", "max"], "Cada True vale 1, então sum conta os aprovados.")]),
        # lição 3
        L("Tem alguma coisa aí?",
          "O if usa bool sozinho: if lista: é o mesmo que if bool(lista):. É o jeito mais curto de saber se um texto foi preenchido ou se uma lista tem itens.",
          'nome = ""\nif not nome:\n    print("Digite um nome!")\ncarrinho = ["pão"]\nif carrinho:\n    print("Itens:", len(carrinho))',
          [OUT('fila = []\nif fila:\n    print("tem gente")\nelse:\n    print("vazia")', ["tem gente", "[]", "False"], "Lista vazia é falsa, então vai para o else."),
           TYPE('print(bool("  "))', "Espaços são caracteres; o texto não está vazio."),
           MC('"if lista:" é o mesmo que…', "if bool(lista):", ["if lista == True:", "if lista is None:", "if len(lista) == 1:"], "O if chama bool() por baixo dos panos."),
           CODE("Crie a função tem_texto(s) que devolve True se s tiver algum caractere e False se for vazio. Use bool().",
                'def tem_texto(s):\n    return s\n',
                'def tem_texto(s):\n    return bool(s)',
                'assert tem_texto("oi") is True, "tem_texto(\\"oi\\") deve devolver True"\nassert tem_texto("") is False, "tem_texto(\\"\\") deve devolver False"',
                "return bool(s)")]),
        # lição 4
        L("Pegadinhas do bool",
          "bool não lê o significado do texto: bool(\"False\") e bool(\"0\") são True, porque não estão vazios. Para transformar \"sim\" ou \"True\" em booleano, compare com ==.",
          'resposta = "False"\nprint(bool(resposta))\nprint(resposta == "True")\nprint(bool("0"), bool(0))',
          [OUT('print(bool("0") and bool(0))', ["True", "0", "Erro"], "bool(\"0\") é True, mas bool(0) é False; True and False dá False."),
           MC('Quer transformar a resposta "sim" ou "não" em True/False. Qual é o certo?', 'resposta == "sim"', ["bool(resposta)", 'bool("sim")', "int(resposta)"], "bool(\"não\") também seria True. Compare o texto."),
           TYPE('print(bool([None]))', "A lista tem um item (mesmo que seja None), então não está vazia."),
           OUT('print(bool(0) == bool(""))', ["False", "0", "Erro"], "Os dois são False, e False == False é True.")]),
        # lição 5
        L("bool com outras funções",
          "filter(bool, lista) fica só com os itens verdadeiros, tirando vazios e zeros. sum(map(bool, lista)) conta os preenchidos. any e all também usam bool em cada item.",
          'nomes = ["Ana", "", "Teo", ""]\nprint(list(filter(bool, nomes)))\nprint(sum(map(bool, nomes)))',
          [OUT('print(list(filter(bool, [0, 1, 2, 0])))', ["[0, 0]", "[0, 1, 2, 0]", "3"], "Os zeros são falsos e saem."),
           TYPE('print(sum(map(bool, ["a", "", "b"])))', "Dois textos preenchidos: True + False + True."),
           MC("any(lista) é True quando…", "pelo menos um item é verdadeiro", ["todos os itens são True", "a lista não está vazia", "a lista tem True escrito"], "any([0]) é False: a lista tem item, mas ele é falso."),
           ORDER("Monte o programa que mostra só as respostas preenchidas.", ['respostas = ["sim", "", "talvez"]', 'preenchidas = list(filter(bool, respostas))', 'print(preenchidas)'], "Crie a lista, filtre com bool e mostre.")]),
        # lição 6
        L("Desafio: formulário",
          "Juntando tudo: num formulário, campos vazios ou zerados são falsos. Com bool você descobre o que falta preencher.",
          'form = {"nome": "Bia", "email": "", "idade": 0}\nfaltando = [campo for campo, v in form.items() if not bool(v)]\nprint(faltando)',
          [OUT('print(bool(None) + bool("x") + bool([0]))', ["3", "1", "Erro"], "0 + 1 + 1: None é falso, os outros dois são verdadeiros."),
           TYPE('print(not bool(""))', "bool(\"\") é False, e not inverte."),
           CODE('Crie a função contar_vazios(campos) que devolve quantos itens da lista são falsos ("", 0, None, []...). Ex.: contar_vazios(["Ana", "", 0, 5]) devolve 2.',
                'def contar_vazios(campos):\n    return len(campos)\n',
                'def contar_vazios(campos):\n    return sum(1 for c in campos if not bool(c))',
                'assert contar_vazios(["Ana", "", 0, 5]) == 2, "Esperado 2"\nassert contar_vazios([]) == 0, "Lista vazia: 0"\nassert contar_vazios([None, [], ""]) == 3, "Esperado 3"',
                "Conte os itens em que not bool(c) é True.")]),
    ],
    # ------------------------------------------------------------------ complex
    "complex": [
        # lição 2
        L("Jeitos de criar",
          "Você pode escrever o número direto, como 3 + 2j, ou usar complex. complex(5) tem parte imaginária 0, complex() é 0j, e complex também lê texto, desde que sem espaços: \"1+2j\".",
          'print(complex(5))\nprint(complex("1+2j"))\nprint(complex())\nprint(3 + 2j)',
          [OUT('print(complex(2))', ["2", "(2j)", "2+0"], "Só a parte real: (2+0j)."),
           TYPE('print(complex("3-1j").imag)', "A parte imaginária é -1, mostrada como float."),
           MC("Qual texto complex() aceita?", '"1+2j"', ['"1 + 2j"', '"1+2i"', '"(1, 2)"'], "Sem espaços e com j."),
           FILL("Complete para criar o número 5j (parte real 0).", 'z = complex(0, ___)\nprint(z)', "5", ['"5j"', "5i", "0"], "O segundo argumento é a parte imaginária, um número.")]),
        # lição 3
        L("Contas com complexos",
          "Somar junta as partes reais e as imaginárias separadamente. A regra especial é j * j = -1. O método conjugate() troca o sinal da parte imaginária.",
          'a = 1 + 2j\nb = 3 - 1j\nprint(a + b)\nprint(1j * 1j)\nprint(a.conjugate())',
          [OUT('print((1 + 1j) + (2 + 3j))', ["(3+3j)", "(1+1j)(2+3j)", "7"], "Reais: 1 + 2 = 3. Imaginárias: 1 + 3 = 4."),
           TYPE('print((2j * 2j).real)', "2j * 2j = 4 * j * j = -4."),
           MC("Quanto é 1j * 1j?", "(-1+0j)", ["1", "(1+0j)", "Dá erro"], "j ao quadrado é -1."),
           CODE("Crie z = complex(6, 8) e guarde em tamanho o abs(z), a distância até a origem. Mostre tamanho.",
                'z = complex(6, 8)\ntamanho = 0\nprint(tamanho)',
                'z = complex(6, 8)\ntamanho = abs(z)\nprint(tamanho)',
                'assert tamanho == 10.0, "abs(6+8j) é 10.0"\nassert "10.0" in __stdout__, "Mostre o tamanho com print"',
                "tamanho = abs(z)")]),
        # lição 4
        L("Cuidados com complexos",
          "Complexos não têm maior ou menor: z < 5 dá TypeError. Também não dá para usar int() ou float() direto num complexo. Pegue .real ou .imag (que são floats) antes.",
          'z = 3 + 4j\nprint(z == 3 + 4j)\ntry:\n    print(z < 5)\nexcept TypeError:\n    print("complexos não têm maior ou menor")',
          [OUT('try:\n    print(int(2 + 0j))\nexcept Exception as e:\n    print(type(e).__name__)', ["2", "2.0", "ValueError"], "int não aceita complexo, mesmo com parte imaginária 0: TypeError."),
           OUT('try:\n    print(complex("1 + 2j"))\nexcept ValueError:\n    print("texto inválido")', ["(1+2j)", "1 + 2j", "Erro de sintaxe"], "Os espaços no meio do texto não são aceitos."),
           TYPE('print(type((5 + 0j).real).__name__)', "As partes de um complexo são sempre float."),
           MC("Para pegar a parte real de 4+0j como inteiro, use…", "int((4 + 0j).real)", ["int(4 + 0j)", "(4 + 0j).int", "round(4 + 0j)"], "Primeiro .real (float), depois int.")]),
        # lição 5
        L("Pontos no mapa",
          "Um complexo pode guardar um ponto (x, y): x na parte real, y na imaginária. Assim, b - a é o caminho entre dois pontos, abs(b - a) é a distância e sum soma vários passos.",
          'casa = complex(0, 0)\nescola = complex(3, 4)\nprint(abs(escola - casa))\npassos = [1 + 0j, 0 + 2j, 1 + 1j]\nprint(sum(passos))',
          [OUT('print(sum([1j, 2j, 3]))', ["6j", "6", "(3+6j)"], "Parte real: 3. Parte imaginária: 1j + 2j = 3j. Juntando: (3+3j)."),
           TYPE('print(abs(complex(1, 1) - complex(4, 5)))', "A diferença é (-3-4j), e abs dá 5.0."),
           ORDER("Monte o programa que mostra a distância entre os pontos (1, 1) e (4, 5).", ['a = complex(1, 1)', 'b = complex(4, 5)', 'print(abs(b - a))'], "Crie os dois pontos e use abs na diferença."),
           MC("Num robô que anda no mapa, o que abs(destino - posicao) dá?", "A distância em linha reta até o destino", ["A soma das coordenadas", "O ângulo do robô", "Sempre um número negativo"], "abs de um complexo é o seu tamanho.")]),
        # lição 6
        L("Desafio: robô no mapa",
          "Juntando tudo: andar para o norte soma 1j, para o leste soma 1. No fim, .real e .imag dizem onde o robô está e abs diz a distância da largada.",
          'pos = 0j\nfor passo in ["N", "N", "L"]:\n    if passo == "N":\n        pos += 1j\n    elif passo == "L":\n        pos += 1\nprint(pos)\nprint(pos.real, pos.imag)',
          [OUT('pos = 0j\npos += 2\npos += 3j\nprint(pos)', ["5", "(2, 3)", "5j"], "O 2 vai para a parte real e o 3j para a imaginária."),
           TYPE('print((3 + 4j).conjugate())', "conjugate troca o sinal da parte imaginária."),
           CODE("Crie a função distancia(x1, y1, x2, y2) que usa complex e abs para devolver a distância entre os pontos. Ex.: distancia(0, 0, 3, 4) devolve 5.0.",
                'def distancia(x1, y1, x2, y2):\n    pass\n',
                'def distancia(x1, y1, x2, y2):\n    return abs(complex(x2, y2) - complex(x1, y1))',
                'assert distancia(0, 0, 3, 4) == 5.0, "distancia(0, 0, 3, 4) deve ser 5.0"\nassert distancia(1, 1, 4, 5) == 5.0, "distancia(1, 1, 4, 5) deve ser 5.0"\nassert distancia(2, 2, 2, 2) == 0.0, "Mesmo ponto: 0.0"',
                "return abs(complex(x2, y2) - complex(x1, y1))")]),
    ],
    # ------------------------------------------------------------------ repr
    "repr": [
        # lição 2
        L("repr de cada tipo",
          "Para números, repr e str dão o mesmo texto. A diferença aparece nos textos: repr põe aspas. Se o texto já tiver aspas simples, repr usa aspas duplas por fora.",
          'print(repr(42))\nprint(repr("Ana"))\nprint(repr([1, "a"]))\nprint(repr("d\'água"))',
          [OUT('print(repr(7))', ["'7'", '"7"', "repr(7)"], "Número não ganha aspas: repr(7) é 7."),
           TYPE('print(repr("sol"))', "Texto ganha aspas simples."),
           MC('Qual é a diferença entre repr("Ana") e str("Ana")?', "repr mostra as aspas", ["str mostra as aspas", "Nada, são iguais", "repr deixa em maiúsculas"], "str dá Ana; repr dá 'Ana'."),
           OUT('print(repr("it\'s"))', ["'it's'", "it's", "'it\\'s'"], "Como o texto tem aspas simples, repr usa aspas duplas por fora.")]),
        # lição 3
        L("Caçando espaços escondidos",
          "Quando uma comparação falha sem motivo, use repr para ver espaços, tabulações (\\t) e quebras de linha (\\n). Na f-string, {x!r} faz o mesmo que repr(x).",
          'senha = "abc "\nprint(senha == "abc")\nprint(repr(senha))\nnome = "Teo"\nprint(f"Nome: {nome!r}")',
          [OUT('x = "a\\tb"\nprint(repr(x))', ["a    b", "'a    b'", "a\\tb"], "repr mostra a tabulação como \\t e põe aspas."),
           TYPE('s = "ok"\nprint(f"[{s!r}]")', "!r põe o texto com aspas dentro dos colchetes."),
           MC("Numa f-string, o que {x!r} faz?", "Mostra x usando repr", ["Mostra x ao contrário", "Arredonda x", "Mostra x em maiúsculas"], "!r chama repr no valor."),
           CODE('A variável cidade = " Recife" tem um espaço escondido no começo. Mostre com print o repr de cidade, para enxergar o espaço.',
                'cidade = " Recife"\nprint(cidade)',
                'cidade = " Recife"\nprint(repr(cidade))',
                'assert __stdout__.strip() == "\' Recife\'", "A saída deve ser \' Recife\' (com aspas e o espaço)"',
                "print(repr(cidade))")]),
        # lição 4
        L("Pegadinhas do repr",
          "repr devolve um texto, então repr(repr(x)) ganha outra camada de aspas. len(repr(texto)) conta as aspas e as barras. E listas mostram seus itens com repr: por isso aparecem as aspas.",
          'print(["oi", "tchau"])\nprint(repr(repr("a")))\nprint(len(repr("a\\n")))',
          [OUT('print(repr(repr(1)))', ["1", "\"'1'\"", "repr(1)"], "repr(1) é o texto \"1\"; o repr dele tem aspas: '1'."),
           TYPE('print(len(repr("oi\\n")))', "repr é 'oi\\n': 2 aspas, o, i, \\ e n."),
           MC('Por que print(["a"]) mostra as aspas?', "Listas mostram seus itens usando repr", ["É um erro", "print sempre mostra aspas", 'Porque "a" é uma letra'], "Cada item da lista aparece com repr."),
           OUT('print(str(0.5) == repr(0.5))', ["False", "0.5", "Erro"], "Para números, str e repr dão o mesmo texto.")]),
        # lição 5
        L("repr nas suas classes",
          "Ao criar o método __repr__ numa classe, você decide como o objeto aparece no repr, no print de listas e no terminal. A boa prática é imitar o código que cria o objeto.",
          'class Pet:\n    def __init__(self, nome):\n        self.nome = nome\n    def __repr__(self):\n        return f"Pet({self.nome!r})"\n\nprint(repr(Pet("Rex")))\nprint([Pet("Mia"), Pet("Bob")])',
          [OUT('class Carta:\n    def __repr__(self):\n        return "Carta()"\n\nprint([Carta()])', ["[]", "Carta()", "[<Carta>]"], "A lista usa o __repr__ de cada item: [Carta()]."),
           MC("Depois de criar __repr__ numa classe, quem passa a usar ele?", "repr(), o print de listas e o terminal >>>", ["Só o int()", "Ninguém, é só um comentário", "Apenas o len()"], "Todos que precisam mostrar o objeto \"como no código\"."),
           TYPE('x = [1, "2"]\nprint(eval(repr(x)) == x)', "O repr de uma lista é código Python válido que recria a lista."),
           CODE("Na classe Ponto, crie o método __repr__ para que repr(Ponto(1, 2)) devolva o texto Ponto(1, 2).",
                'class Ponto:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n',
                'class Ponto:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n    def __repr__(self):\n        return f"Ponto({self.x}, {self.y})"',
                'assert repr(Ponto(1, 2)) == "Ponto(1, 2)", "repr(Ponto(1, 2)) deve ser Ponto(1, 2)"\nassert repr(Ponto(0, 5)) == "Ponto(0, 5)", "repr(Ponto(0, 5)) deve ser Ponto(0, 5)"',
                'def __repr__(self): return f"Ponto({self.x}, {self.y})"')]),
        # lição 6
        L("Desafio: log de depuração",
          "Juntando tudo: um log que mostra nome = repr(valor) deixa claro se o valor é texto ou número e se há espaços escondidos.",
          'def log(nome, valor):\n    print(f"{nome} = {valor!r}")\n\nlog("idade", 30)\nlog("nome", "Ana ")\nlog("itens", [])',
          [OUT('print(len(repr("")))', ["0", "1", "Erro"], "O repr do texto vazio é '': duas aspas."),
           TYPE('v = "5"\nprint(f"v={v!r}")', "!r mostra o texto com aspas."),
           CODE("Crie a função log(nome, valor) que MOSTRA o texto nome = repr(valor). Ex.: log(\"cor\", \"azul\") mostra cor = 'azul'.",
                'def log(nome, valor):\n    print(nome, "=", valor)\n\nlog("cor", "azul")',
                'def log(nome, valor):\n    print(f"{nome} = {valor!r}")\n\nlog("cor", "azul")',
                'assert "cor = \'azul\'" in __stdout__, "Esperado: cor = \'azul\'"',
                'print(f"{nome} = {valor!r}")')]),
    ],
}

BUGS = r'''
@fn_int 2
idade = "15"
print(idade + 1)
>>> print(int(idade) + 1)
!! idade é texto. Converta com int antes de somar.

@fn_int 1
nota = int("7.5")
print(nota)
>>> nota = int(float("7.5"))
!! int não lê texto com ponto. Passe antes por float.

@fn_int 2
binario = "1010"
print(int(binario))  # esperado: 10
>>> print(int(binario, 2))  # esperado: 10
!! Sem a base, int lê como decimal. Binário é base 2.

@fn_int 4
precos = ["10", "25", "5"]
total = 0
for p in precos:
    total += p
print(total)
>>> total += int(p)
!! Os preços são textos. Converta cada um com int.

@fn_int 2
media = 7.9
print(int(media))  # esperado: 8
>>> print(round(media))  # esperado: 8
!! int corta a parte decimal. Para arredondar, use round.

@fn_int 1
pontos = int("1.000")
print(pontos + 1)
>>> pontos = int("1.000".replace(".", ""))
!! O ponto de milhar atrapalha o int. Tire o ponto antes.

@fn_float 1
preco = float("4,90")
print(preco * 2)
>>> preco = float("4.90")
!! O Python usa ponto como separador decimal, não vírgula.

@fn_float 3
a = "2.5"
b = "1.5"
print(a + b)  # esperado: 4.0
>>> print(float(a) + float(b))  # esperado: 4.0
!! Textos com + são colados. Converta com float antes.

@fn_float 2
total = 0.1 + 0.2
if total == 0.3:
    print("certo")
else:
    print("errado")  # esperado: certo
>>> if round(total, 2) == 0.3:
!! Floats têm restinhos. Arredonde antes de comparar.

@fn_float 1
valor = float("R$ 12.50")
print(valor)
>>> valor = float("R$ 12.50".replace("R$ ", ""))
!! float não entende o R$. Tire o símbolo primeiro.

@fn_float 2
nota = float("8.5")
print("Nota: " + nota)
>>> print("Nota: " + str(nota))
!! Texto + float dá erro. Converta a nota com str.

@fn_float 1
metade = float(7 // 2)
print(metade)  # esperado: 3.5
>>> metade = 7 / 2
!! // corta a parte decimal antes do float. Use / para dividir.

@fn_str 2
vidas = 3
print("Vidas: " + vidas)
>>> print("Vidas: " + str(vidas))
!! Para colar com +, o número precisa virar texto com str.

@fn_str 3
a = str(10)
b = str(5)
print(a + b)  # esperado: 15
>>> print(int(a) + int(b))  # esperado: 15
!! Textos com + são colados ("105"). Para somar, converta para int.

@fn_str 2
codigo = 42
print(str(codigo).zfill(2))  # esperado: 0042
>>> print(str(codigo).zfill(4))  # esperado: 0042
!! zfill recebe o tamanho final do texto: 4 caracteres.

@fn_str 2
n = 2026
print(len(n))
>>> print(len(str(n)))
!! Números não têm len. Converta para texto para contar os dígitos.

@fn_str 2
nums = [1, 2, 3]
print(", ".join(nums))
>>> print(", ".join(map(str, nums)))
!! join só junta textos. Converta os números com map(str, ...).

@fn_str 2
ano = 2026
fim = str(ano)[2]
print(fim)  # esperado: 26
>>> fim = str(ano)[2:]
!! [2] pega um só caractere. Para ir até o fim, use [2:].

@fn_bool 2
resposta = "False"
ativo = bool(resposta)
print(ativo)  # esperado: False
>>> ativo = resposta == "True"
!! bool de um texto não vazio é sempre True. Compare o texto com ==.

@fn_bool 2
nomes = ["Ana"]
if nomes == True:
    print("tem nomes")
else:
    print("vazia")  # esperado: tem nomes
>>> if bool(nomes):
!! Uma lista nunca é igual a True. Use bool(nomes) ou só if nomes.

@fn_bool 2
nome = ""
if bool(nome):
    print("Preencha o nome!")  # esperado: Preencha o nome!
>>> if not bool(nome):
!! O aviso deve aparecer quando o nome está vazio: faltou o not.

@fn_bool 2
notas = [8, 5, 9]
aprovados = sum(bool(n) for n in notas)
print(aprovados)  # esperado: 2
>>> aprovados = sum(n >= 7 for n in notas)
!! bool(n) é True para qualquer nota diferente de zero. Teste n >= 7.

@fn_bool 2
saldo = "0"
if bool(saldo):
    print("tem saldo")
else:
    print("sem saldo")  # esperado: sem saldo
>>> if bool(int(saldo)):
!! "0" é um texto não vazio, então é True. Converta para int antes.

@fn_bool 2
estoque = 0
tem = bool("estoque")
print(tem)  # esperado: False
>>> tem = bool(estoque)
!! Com aspas, "estoque" é um texto não vazio. Passe a variável, sem aspas.

@fn_complex 1
z = complex("2 + 3j")
print(z)
>>> z = complex("2+3j")
!! O texto do complex não pode ter espaços.

@fn_complex 2
z = complex(3, 4)
print(z.imaginary)
>>> print(z.imag)
!! O nome do atributo é imag.

@fn_complex 1
z = 1 + 2i
print(z * 2)
>>> z = 1 + 2j
!! Em Python, a parte imaginária usa j, não i.

@fn_complex 2
a = complex(3, 4)
print(a.real())
>>> print(a.real)
!! real é um valor, não um método. Tire os parênteses.

@fn_complex 3
p = complex(0, 0)
q = complex(3, 4)
print(q - p)  # esperado: 5.0
>>> print(abs(q - p))  # esperado: 5.0
!! A diferença é um complexo. A distância é o abs dela.

@fn_complex 2
z = complex(5, 2)
print(int(z))
>>> print(int(z.real))
!! int não aceita complexo. Pegue a parte real primeiro.

@fn_complex 3
a = 3 + 4j
b = 1 + 1j
if a > b:
    print("a está mais longe")
>>> if abs(a) > abs(b):
!! Complexos não têm maior ou menor. Compare os tamanhos com abs.

@fn_repr 2
senha = "abc\n"
print(senha)  # esperado: 'abc\n'
>>> print(repr(senha))  # esperado: 'abc\n'
!! print esconde o \n. Use repr para ver o texto como ele é.

@fn_repr 5
class Pet:
    def __init__(self, nome):
        self.nome = nome
    def __repr__(self):
        print(f"Pet({self.nome!r})")
print(repr(Pet("Rex")))
>>> return f"Pet({self.nome!r})"
!! __repr__ precisa devolver o texto com return, não mostrar com print.

@fn_repr 4
class Ponto:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __rep__(self):
        return f"Ponto({self.x}, {self.y})"
print([Ponto(1, 2)])  # esperado: [Ponto(1, 2)]
>>> def __repr__(self):
!! O nome do método é __repr__, com r no final.

@fn_repr 2
nome = "Bia"
print(f"nome={nome!s}")  # esperado: nome='Bia'
>>> print(f"nome={nome!r}")  # esperado: nome='Bia'
!! !s usa str, sem aspas. Para o repr, use !r.

@fn_repr 2
texto = "oi"
print(len(repr(texto)))  # esperado: 2
>>> print(len(texto))  # esperado: 2
!! repr conta as aspas também. O tamanho do texto é len(texto).

@fn_repr 2
cidade = " Recife"
print(rep(cidade))
>>> print(repr(cidade))
!! O nome da função é repr, com r no final.
'''
