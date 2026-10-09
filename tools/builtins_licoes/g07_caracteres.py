from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ ord
    "ord": [
        # lição 2
        L("Letras, espaços e símbolos",
          "Todo caractere tem código, não só as letras: o espaço é 32, a quebra de linha é 10 e os dígitos vão de 48 a 57. As maiúsculas vêm antes das minúsculas, e a distância entre A e a é sempre 32.",
          'print(ord(" "))\nprint(ord("Z"))\nprint(ord("a"))\nprint(ord("a") - ord("A"))',
          [OUT('print(ord("b") - ord("B"))', ["1", "0", "-32"], "Minúscula menos maiúscula da mesma letra dá sempre 32."),
           TYPE('print(ord(" "))', "O espaço também é um caractere, com código 32."),
           MC('ord("Z") < ord("a") dá…', "True", ["False", "Erro", "None"], "Z é 90 e a é 97: as maiúsculas vêm primeiro."),
           FILL("Complete para mostrar 67.", 'print(ord(___))', '"C"', ['C', '"c"', '67'], "ord recebe um texto de 1 caractere, com aspas. C maiúsculo é 67.")]),
        # lição 3
        L("Posição no alfabeto",
          "Como as letras têm códigos seguidos, dá para fazer contas: ord(letra) - ord(\"a\") + 1 diz a posição da letra no alfabeto. Com dígitos funciona igual: ord(\"7\") - ord(\"0\") dá 7.",
          'letra = "d"\nprint(ord(letra) - ord("a") + 1)\ndigito = "7"\nprint(ord(digito) - ord("0"))',
          [OUT('print(ord("e") - ord("a") + 1)', ["4", "6", "101"], "e é a 5ª letra: 101 - 97 + 1."),
           TYPE('print(ord("9") - ord("0"))', "Os dígitos têm códigos seguidos, de 48 a 57."),
           MC('Por que "B" < "a" dá True em Python?', "Porque ord(\"B\") é menor que ord(\"a\")", ["Porque B vem antes no alfabeto", "Porque maiúsculas valem mais", "Dá erro"], "Textos são comparados pelos códigos dos caracteres."),
           CODE("Crie a função posicao(letra) que devolve a posição de uma letra minúscula no alfabeto (a = 1, b = 2, …, z = 26).",
                "def posicao(letra):\n    return ord(letra)\n",
                'def posicao(letra):\n    return ord(letra) - ord("a") + 1',
                'assert posicao("a") == 1, "posicao(\'a\') deve ser 1"\nassert posicao("c") == 3, "posicao(\'c\') deve ser 3"\nassert posicao("z") == 26, "posicao(\'z\') deve ser 26"',
                'return ord(letra) - ord("a") + 1')]),
        # lição 4
        L("Cuidados com ord",
          "ord só aceita UM caractere de texto. Texto vazio, texto com duas letras ou um número dão TypeError. E lembre: o código do caractere \"7\" é 55, não 7.",
          'print(ord("7"))\ntry:\n    ord(7)\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('print(ord("7") == 7)', ["True", "Erro", "55"], "ord(\"7\") é 55, então a comparação dá False."),
           MC("ord(7), com o número sem aspas, dá…", "TypeError", ["55", "7", "ValueError"], "ord espera texto, não número."),
           TYPE('print(ord("😀") > 1000)', "Emojis têm códigos bem altos (128512)."),
           MC("Como pegar o código da primeira letra de nome?", "ord(nome[0])", ["ord(nome)", "ord[nome[0]]", "nome.ord()"], "Primeiro pegue um único caractere com [0], depois use ord.")]),
        # lição 5
        L("ord com laços e map",
          "Para pegar o código de cada caractere de um texto, use um for, uma compreensão de lista ou map(ord, texto). Somar os códigos é um truque simples para criar um número a partir de um texto.",
          'print([ord(c) for c in "oi"])\nprint(list(map(ord, "AB")))\nprint(sum(ord(c) for c in "abc"))',
          [OUT('print(list(map(ord, "Py")))', ["['P', 'y']", "[80, 89]", "80121"], "P é 80 e y é 121."),
           TYPE('print(sum(ord(c) for c in "aa"))', "97 + 97."),
           ORDER("Monte o programa que mostra o código de cada letra de \"ok\", um por linha.",
                 ['palavra = "ok"', 'for letra in palavra:', '    print(ord(letra))'],
                 "Primeiro a variável, depois o for, e dentro dele o print."),
           CODE("Crie a função codigos(texto) que devolve a lista com o código de cada caractere do texto.",
                "def codigos(texto):\n    return ord(texto)\n",
                'def codigos(texto):\n    return [ord(c) for c in texto]',
                'assert codigos("AB") == [65, 66], "codigos(\'AB\') deve ser [65, 66]"\nassert codigos("") == [], "Texto vazio deve dar lista vazia"',
                'return [ord(c) for c in texto]')]),
        # lição 6
        L("Desafio: código verificador",
          "Lojas e bancos usam dígitos verificadores para pegar erros de digitação. Uma versão simples: somar os códigos dos caracteres e ficar com o resto da divisão por 100.",
          'senha = "gato"\ntotal = sum(ord(c) for c in senha)\nprint(total)\nprint(total % 100)',
          [OUT('print(sum(ord(c) for c in "AB") % 100)', ["131", "65", "13"], "65 + 66 = 131, e o resto por 100 é 31."),
           MC("Qual texto tem a MAIOR soma de códigos?", '"ab"', ['"AB"', '"a"', '"B"'], "Minúsculas têm códigos maiores e \"ab\" tem duas letras."),
           FILL("Complete para contar quantas letras maiúsculas o texto tem.",
                'texto = "PyPasso"\nprint(sum(1 for c in texto if 65 <= ___ <= 90))', 'ord(c)', ['c', 'ord(texto)', 'chr(c)'],
                "As maiúsculas vão de 65 (A) a 90 (Z)."),
           CODE("Crie a função verificador(texto) que devolve a soma dos códigos de todos os caracteres, com resto da divisão por 100.",
                "def verificador(texto):\n    return 0\n",
                'def verificador(texto):\n    return sum(ord(c) for c in texto) % 100',
                'assert verificador("AB") == 31, "verificador(\'AB\') deve ser 31"\nassert verificador("gato") == 27, "verificador(\'gato\') deve ser 27"\nassert verificador("") == 0, "Texto vazio deve dar 0"',
                'return sum(ord(c) for c in texto) % 100')]),
    ],
    # ================================================================ chr
    "chr": [
        # lição 2
        L("Faixas de códigos",
          "Alguns intervalos são bons de decorar: 48 a 57 são os dígitos, 65 a 90 as maiúsculas e 97 a 122 as minúsculas. chr(32) é o espaço e chr(10) é a quebra de linha.",
          'print(chr(48))\nprint(chr(90))\nprint("a" + chr(32) + "b")\nprint("um" + chr(10) + "dois")',
          [OUT('print(chr(49) + chr(50))', ["3", "99", "4950"], "49 é o caractere 1 e 50 é o 2; somar textos junta."),
           TYPE('print(chr(122))', "122 é a última minúscula."),
           MC("Qual chr devolve a letra a?", "chr(97)", ["chr(65)", "chr(1)", "chr(0)"], "As minúsculas começam em 97."),
           OUT('print("x" + chr(10) + "y")', ["x10y", "x y", "xy"], "chr(10) é a quebra de linha, então y vai para a linha de baixo.")]),
        # lição 3
        L("Gerando sequências",
          "Com range e chr você gera letras sem digitar uma por uma. \"\".join junta tudo num texto só.",
          'print("".join(chr(c) for c in range(65, 70)))\nletras = [chr(97 + i) for i in range(3)]\nprint(letras)',
          [OUT('print("".join(chr(c) for c in range(97, 100)))', ["abcd", "979899", "['a', 'b', 'c']"], "range(97, 100) vai até 99, então a, b, c."),
           TYPE('print("-".join(chr(65 + i) for i in range(4)))', "A, B, C e D, separados por hífen."),
           FILL("Complete para mostrar as 26 letras maiúsculas.", 'print("".join(chr(c) for c in range(65, ___)))', '91', ['90', '26', '122'], "O range para antes do fim: para incluir 90 (Z), use 91."),
           CODE("Crie a função alfabeto(n) que devolve um texto com as n primeiras letras minúsculas. Exemplo: alfabeto(3) devolve abc.",
                "def alfabeto(n):\n    return chr(n)\n",
                'def alfabeto(n):\n    return "".join(chr(97 + i) for i in range(n))',
                'assert alfabeto(3) == "abc", "alfabeto(3) deve ser abc"\nassert alfabeto(1) == "a", "alfabeto(1) deve ser a"\nassert len(alfabeto(26)) == 26 and alfabeto(26).endswith("z"), "alfabeto(26) deve ir de a até z"',
                'return "".join(chr(97 + i) for i in range(n))')]),
        # lição 4
        L("Cuidados com chr",
          "chr recebe um número inteiro. Texto como \"65\" ou número quebrado como 65.0 dão TypeError, e número negativo dá ValueError. O resultado é sempre um texto, não um número.",
          'print(chr(65))\nprint(type(chr(65)).__name__)\ntry:\n    chr(-1)\nexcept ValueError as e:\n    print(type(e).__name__)',
          [MC('chr("65") dá…', "TypeError", ['"A"', "65", "ValueError"], "O código precisa ser número inteiro, sem aspas."),
           OUT('print(chr(int("66")))', ["66", "Erro", "b"], "int(\"66\") vira o número 66, e chr(66) é B."),
           TYPE('print(chr(55) + "1")', "chr(55) é o caractere 7, e texto + texto junta."),
           MC("chr(-1) dá…", "ValueError", ["TypeError", '""', "None"], "Não existe caractere com código negativo.")]),
        # lição 5
        L("chr e ord juntos",
          "ord leva para número, a conta acontece, e chr volta para letra. Assim dá para pegar a próxima letra ou trocar maiúscula por minúscula (diferença de 32).",
          'letra = "c"\nprint(chr(ord(letra) + 1))\nprint(chr(ord("g") - 32))',
          [OUT('print(chr(ord("A") + 32))', ["A", "a32", "B"], "Somar 32 a uma maiúscula dá a minúscula."),
           TYPE('print(chr(ord("m") - 1))', "A letra antes de m."),
           ORDER("Monte o programa que mostra a letra seguinte de \"p\".",
                 ['letra = "p"', 'codigo = ord(letra)', 'print(chr(codigo + 1))'],
                 "Pegue o código, some 1 e volte para caractere."),
           CODE("Crie a função proxima(letra) que devolve a letra seguinte. Exemplo: proxima(\"a\") devolve \"b\".",
                "def proxima(letra):\n    return letra + 1\n",
                'def proxima(letra):\n    return chr(ord(letra) + 1)',
                'assert proxima("a") == "b", "proxima(\'a\') deve ser b"\nassert proxima("Y") == "Z", "proxima(\'Y\') deve ser Z"',
                'return chr(ord(letra) + 1)')]),
        # lição 6
        L("Desafio: cifra de César",
          "A cifra de César troca cada letra pela que está n posições depois, voltando ao começo depois do z. O truque é usar % 26 na posição: (posição + n) % 26.",
          'letra = "y"\nn = 3\npos = (ord(letra) - ord("a") + n) % 26\nprint(chr(ord("a") + pos))',
          [OUT('print(chr(ord("a") + (25 + 2) % 26))', ["|", "a", "c"], "25 + 2 = 27; 27 % 26 = 1; ord(\"a\") + 1 é b."),
           MC("Sem o % 26, avançar z em 1 dá…", "{", ["a", "Erro", "z"], "Depois do z (122) vem o { (123)."),
           TYPE('print("".join(chr(ord(c) + 1) for c in "hal"))', "Cada letra avança uma posição."),
           CODE("Crie a função cesar(texto, n) que avança cada letra minúscula n posições, voltando ao início depois do z. Os outros caracteres (espaço, pontuação) ficam iguais.",
                "def cesar(texto, n):\n    return texto\n",
                'def cesar(texto, n):\n    saida = ""\n    for c in texto:\n        if "a" <= c <= "z":\n            pos = (ord(c) - ord("a") + n) % 26\n            saida += chr(ord("a") + pos)\n        else:\n            saida += c\n    return saida',
                'assert cesar("abc", 1) == "bcd", "cesar(\'abc\', 1) deve ser bcd"\nassert cesar("xyz", 3) == "abc", "Depois do z volta para o a: cesar(\'xyz\', 3) deve ser abc"\nassert cesar("oi, pipo", 2) == "qk, rkrq", "Espaço e vírgula não mudam"',
                'Use pos = (ord(c) - ord("a") + n) % 26 e chr(ord("a") + pos) só para letras de a a z.')]),
    ],
    # ================================================================ bin
    "bin": [
        # lição 2
        L("Voltando para decimal",
          "bin vai do decimal para o binário; int(texto, 2) faz o caminho de volta. Números negativos ganham um sinal de menos na frente: bin(-5) é -0b101.",
          'print(bin(10))\nprint(int("1010", 2))\nprint(bin(0))\nprint(bin(-5))',
          [OUT('print(int("110", 2))', ["110", "3", "5"], "1×4 + 1×2 + 0×1 = 6."),
           TYPE('print(bin(-3))', "O sinal vem antes do 0b."),
           OUT('print(bin(0))', ["0", "0b", "Erro"], "Zero em binário também ganha o prefixo: 0b0."),
           MC('Qual expressão transforma "1111" em 15?', 'int("1111", 2)', ['bin("1111")', 'int("1111")', 'bin(1111)'], "int com base 2 lê o texto como binário.")]),
        # lição 3
        L("Contando bits",
          "Como bin devolve texto, dá para usar métodos de texto. bin(n).count(\"1\") conta os bits ligados e len(bin(n)) - 2 diz quantos bits o número usa (tirando o 0b).",
          'n = 13\nprint(bin(n))\nprint(bin(n).count("1"))\nprint(len(bin(n)) - 2)',
          [OUT('print(bin(7).count("1"))', ["7", "1", "0b111"], "7 é 111: três bits ligados."),
           TYPE('print(len(bin(16)) - 2)', "16 é 10000 em binário: 5 algarismos."),
           MC("Todo número par termina em binário com…", "0", ["1", "b", "10"], "O último bit vale 1; se ele está ligado, o número é ímpar."),
           CODE("Crie a função bits_ligados(n) que devolve quantos algarismos 1 o número tem em binário.",
                "def bits_ligados(n):\n    return bin(n)\n",
                'def bits_ligados(n):\n    return bin(n).count("1")',
                'assert bits_ligados(7) == 3, "7 é 111: deve dar 3"\nassert bits_ligados(8) == 1, "8 é 1000: deve dar 1"\nassert bits_ligados(0) == 0, "0 não tem bits ligados"',
                'return bin(n).count("1")')]),
        # lição 4
        L("Cuidados com bin",
          "bin só aceita inteiros: bin(2.5) e bin(\"5\") dão TypeError. O resultado é texto, então bin(5) + 1 dá erro. E com negativos, [2:] corta o lugar errado: bin(-5)[2:] dá b101.",
          'print(bin(5)[2:])\nprint(bin(-5)[2:])\ntry:\n    bin(2.5)\nexcept TypeError as e:\n    print(type(e).__name__)',
          [MC("bin(5) + 1 dá…", "TypeError", ['"0b110"', "6", '"0b1011"'], "bin devolve texto; texto + número dá erro."),
           OUT('print(bin(-2)[2:])', ["10", "-10", "0b10"], "bin(-2) é -0b10; cortando 2 caracteres sobra b10."),
           TYPE('print(type(bin(9)).__name__)', "bin sempre devolve texto (str)."),
           MC('Para converter o texto "12" para binário…', 'bin(int("12"))', ['bin("12")', 'int(bin("12"))', 'bin(12.0)'], "Primeiro vire número com int, depois use bin.")]),
        # lição 5
        L("bin, format e zfill",
          "format(n, \"b\") dá o binário sem o 0b, e format(n, \"08b\") completa com zeros até 8 algarismos, como um byte. Em f-strings, é {n:08b}.",
          'print(format(5, "b"))\nprint(format(5, "08b"))\nprint(f"{200:08b}")\nprint(bin(5)[2:].zfill(4))',
          [OUT('print(format(3, "04b"))', ["0b11", "11", "0003"], "3 é 11; com 4 algarismos fica 0011."),
           TYPE('print(f"{10:b}")', "10 em binário, sem prefixo."),
           FILL("Complete para mostrar 00000110.", 'print(format(6, ___))', '"08b"', ['"8b"', '"b8"', '"08"'], "08b: 8 algarismos, completando com 0, em binário."),
           CODE("Crie a função byte(n) que devolve o número em binário com exatamente 8 algarismos, sem o 0b. Exemplo: byte(5) devolve 00000101.",
                "def byte(n):\n    return bin(n)\n",
                'def byte(n):\n    return format(n, "08b")',
                'assert byte(5) == "00000101", "byte(5) deve ser 00000101"\nassert byte(255) == "11111111", "byte(255) deve ser 11111111"\nassert byte(0) == "00000000", "byte(0) deve ser 00000000"',
                'return format(n, "08b")')]),
        # lição 6
        L("Desafio: potências de 2",
          "Potências de 2 (1, 2, 4, 8, 16…) têm um padrão em binário: um único 1 seguido de zeros. Contar os 1 com bin resolve o problema.",
          'for n in [1, 2, 4, 6, 8]:\n    print(n, bin(n), bin(n).count("1") == 1)',
          [OUT('print(bin(32))', ["0b11111", "0b10000", "0b100001"], "32 é 2 elevado a 5: um 1 e cinco zeros."),
           MC("Qual destes NÃO é potência de 2?", "12", ["16", "64", "1"], "12 é 1100: tem dois bits ligados."),
           TYPE('print(bin(1024).count("0") - 1)', "1024 é 1 seguido de 10 zeros; tiramos o 0 do prefixo 0b."),
           CODE("Crie a função potencia_de_2(n) que devolve True se n (maior que zero) é potência de 2 e False se não for. Use bin.",
                "def potencia_de_2(n):\n    return n % 2 == 0\n",
                'def potencia_de_2(n):\n    return bin(n).count("1") == 1',
                'assert potencia_de_2(1) is True, "1 é 2 elevado a 0"\nassert potencia_de_2(64) is True, "64 é potência de 2"\nassert potencia_de_2(12) is False, "12 não é potência de 2"\nassert potencia_de_2(7) is False, "7 não é potência de 2"',
                'return bin(n).count("1") == 1')]),
    ],
    # ================================================================ oct
    "oct": [
        # lição 2
        L("Ida e volta do octal",
          "oct vai do decimal para o octal, e int(texto, 8) volta. Na base 8 só existem os algarismos de 0 a 7. Você também pode escrever o número direto no código com 0o.",
          'print(oct(20))\nprint(int("24", 8))\nprint(0o24)\nprint(oct(-8))',
          [OUT('print(int("17", 8))', ["17", "0o17", "71"], "1×8 + 7 = 15."),
           TYPE('print(oct(16))', "16 = 2×8 + 0."),
           OUT('print(0o7 + 1)', ["0o10", "71", "Erro"], "0o7 é o número 7; a conta dá 8, mostrado em decimal."),
           MC("Quais algarismos existem na base 8?", "De 0 a 7", ["De 0 a 8", "De 1 a 8", "De 0 a 9"], "A base 8 tem 8 algarismos, começando no zero.")]),
        # lição 3
        L("Permissões de arquivos",
          "No Linux, permissões como 755 são números octais. Cada algarismo junta leitura (4), escrita (2) e execução (1): 7 = 4+2+1 (tudo), 5 = 4+1, 4 = só leitura.",
          'modo = 0o755\nprint(modo)\nprint(oct(modo))\nprint(oct(modo)[2:])',
          [OUT('print(oct(420))', ["0o420", "0o664", "644"], "420 em octal é 644: a permissão comum de arquivos."),
           TYPE('print(oct(0o700)[2:])', "oct mostra de volta o valor octal; [2:] tira o 0o."),
           MC("Na permissão 6, o dono pode…", "Ler e escrever", ["Só executar", "Ler, escrever e executar", "Nada"], "6 = 4 (leitura) + 2 (escrita)."),
           CODE("Crie a função permissao(modo) que recebe um número (como 493) e devolve o texto da permissão octal sem o 0o (como \"755\").",
                "def permissao(modo):\n    return oct(modo)\n",
                'def permissao(modo):\n    return oct(modo)[2:]',
                'assert permissao(493) == "755", "permissao(493) deve ser 755"\nassert permissao(0o644) == "644", "permissao(0o644) deve ser 644"',
                'return oct(modo)[2:]')]),
        # lição 4
        L("Cuidados com o octal",
          "Algarismos 8 e 9 não existem em octal: int(\"8\", 8) dá ValueError. oct só aceita inteiros e devolve texto. E 0o10 não é dez: é oito.",
          'print(0o10)\ntry:\n    int("19", 8)\nexcept ValueError as e:\n    print(type(e).__name__)',
          [MC('int("9", 8) dá…', "ValueError", ["9", "11", "0o11"], "9 não é um algarismo válido em octal."),
           OUT('print(0o10 == 10)', ["True", "Erro", "8"], "0o10 vale 8, então a comparação é False."),
           TYPE('print(oct(8) + "!")', "oct devolve texto, então dá para juntar com outro texto."),
           MC("oct(3.0) dá…", "TypeError", ['"0o3"', '"3"', "ValueError"], "oct, como bin e hex, só aceita inteiros.")]),
        # lição 5
        L("Octal com format",
          "format(n, \"o\") mostra o octal sem prefixo, e \"#o\" coloca o 0o. Dá para comparar o mesmo número em várias bases de uma vez.",
          'n = 64\nprint(format(n, "o"))\nprint(format(n, "#o"))\nprint(bin(n), oct(n), hex(n))',
          [OUT('print(format(9, "o"))', ["0o11", "9", "1001"], "9 = 1×8 + 1, sem o prefixo."),
           TYPE('print(f"{8:#o}")', "O # coloca o prefixo 0o."),
           FILL("Complete para mostrar 0o17.", 'print(format(15, ___))', '"#o"', ['"o"', '"0o"', '"#x"'], "# pede o prefixo e o diz octal."),
           CODE("Crie a função tabela(n) que devolve uma lista com o número em binário, octal e hexadecimal, sem prefixos. Exemplo: tabela(8) devolve [\"1000\", \"10\", \"8\"].",
                "def tabela(n):\n    return [bin(n), oct(n), hex(n)]\n",
                'def tabela(n):\n    return [format(n, "b"), format(n, "o"), format(n, "x")]',
                'assert tabela(8) == ["1000", "10", "8"], "tabela(8) deve ser [\'1000\', \'10\', \'8\']"\nassert tabela(255) == ["11111111", "377", "ff"], "tabela(255) deve ser [\'11111111\', \'377\', \'ff\']"',
                'return [format(n, "b"), format(n, "o"), format(n, "x")]')]),
        # lição 6
        L("Desafio: lendo permissões",
          "Cada algarismo da permissão é uma pessoa: dono, grupo e outros. Depois de oct(modo)[2:], basta transformar cada caractere em número.",
          'modo = 0o751\ndigitos = [int(d) for d in oct(modo)[2:]]\nprint(digitos)\nprint("Dono pode tudo:", digitos[0] == 7)',
          [OUT('print([int(d) for d in oct(0o640)[2:]])', ["['6', '4', '0']", "[640]", "[0, 4, 6]"], "Cada algarismo vira um número na lista."),
           TYPE('print(oct(0o755)[-1])', "O último algarismo é a permissão dos outros."),
           MC("A permissão 0o600 deixa os outros usuários…", "Sem nenhum acesso", ["Ler o arquivo", "Fazer tudo", "Só executar"], "O último algarismo é 0: nenhuma permissão."),
           CODE("Crie a função digitos(modo) que devolve a lista com os algarismos da permissão. Exemplo: digitos(0o754) devolve [7, 5, 4].",
                "def digitos(modo):\n    return oct(modo)\n",
                'def digitos(modo):\n    return [int(d) for d in oct(modo)[2:]]',
                'assert digitos(0o754) == [7, 5, 4], "digitos(0o754) deve ser [7, 5, 4]"\nassert digitos(420) == [6, 4, 4], "420 é 0o644: deve dar [6, 4, 4]"',
                'return [int(d) for d in oct(modo)[2:]]')]),
    ],
    # ================================================================ hex
    "hex": [
        # lição 2
        L("Letras e volta para decimal",
          "hex usa letras minúsculas (a até f). Se quiser maiúsculas, use .upper(). Para voltar, int(texto, 16) aceita maiúsculas, minúsculas e até o prefixo 0x.",
          'print(hex(171))\nprint(hex(171).upper())\nprint(int("AB", 16))\nprint(int("0xab", 16))',
          [OUT('print(hex(11))', ["0x11", "0xB", "11"], "11 em hexadecimal é b, minúsculo."),
           TYPE('print(int("1F", 16))', "1×16 + 15."),
           OUT('print(hex(-255))', ["0x-ff", "-255", "0xff"], "O sinal de menos vem antes do 0x."),
           MC('int("ff") (sem a base) dá…', "ValueError", ["255", '"ff"', "TypeError"], "Sem a base 16, int só entende algarismos decimais.")]),
        # lição 3
        L("Cores na web",
          "Uma cor como #FF8800 tem três pares hexadecimais: vermelho, verde e azul, cada um de 0 a 255. int(par, 16) lê cada pedaço.",
          'cor = "#FF8800"\nr = int(cor[1:3], 16)\ng = int(cor[3:5], 16)\nb = int(cor[5:7], 16)\nprint(r, g, b)',
          [OUT('cor = "#00FF80"\nprint(int(cor[3:5], 16))', ["0", "128", "FF"], "cor[3:5] é FF, o verde: 255."),
           TYPE('print(int("80", 16))', "8×16 + 0."),
           MC("Qual cor é o branco?", "#FFFFFF", ["#000000", "#FF0000", "#111111"], "Tudo no máximo (255) dá branco."),
           CODE("Crie a função rgb(cor) que recebe um texto como \"#FF8800\" e devolve a tupla (255, 136, 0).",
                "def rgb(cor):\n    return cor\n",
                'def rgb(cor):\n    return (int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16))',
                'assert rgb("#FF8800") == (255, 136, 0), "rgb(\'#FF8800\') deve ser (255, 136, 0)"\nassert rgb("#000000") == (0, 0, 0), "Preto deve ser (0, 0, 0)"\nassert rgb("#0a0b0c") == (10, 11, 12), "Minúsculas também valem"',
                'return (int(cor[1:3], 16), int(cor[3:5], 16), int(cor[5:7], 16))')]),
        # lição 4
        L("Cuidados com hex",
          "hex não completa com zeros: hex(5) é 0x5, não 0x05. Isso quebra cores, que precisam de 2 algarismos por pedaço. hex também só aceita inteiros e devolve texto.",
          'print(hex(5))\nprint(hex(5)[2:])\nprint(format(5, "02x"))',
          [OUT('print(hex(10)[2:])', ["0a", "10", "0xa"], "hex não completa com zero: sobra só a."),
           MC("hex(2.5) dá…", "TypeError", ['"0x2.8"', '"0x2"', "ValueError"], "hex só aceita inteiros."),
           TYPE('print(len(hex(255)))', "0xff tem 4 caracteres."),
           MC('Para ter "0f" a partir de 15, use…', 'format(15, "02x")', ['hex(15)', 'hex(15)[2:]', 'str(15)'], "02x pede 2 algarismos hexadecimais, completando com zero.")]),
        # lição 5
        L("hex com ord e format",
          "Os códigos Unicode costumam aparecer em hexadecimal, como U+00E9 para é. Junte ord com hex ou com format(..., \"04X\") para descobrir.",
          'print(hex(ord("A")))\nprint(format(ord("é"), "04X"))\nprint(f"U+{ord("😀"):04X}")',
          [OUT('print(hex(ord("a")))', ["0x97", "0x41", "97"], "ord(\"a\") é 97, que em hexadecimal é 61."),
           TYPE('print(format(255, "X"))', "X maiúsculo deixa as letras maiúsculas."),
           FILL("Complete para mostrar 0x1a.", 'print(format(26, ___))', '"#x"', ['"x"', '"0x"', '"#X"'], "# coloca o prefixo; x minúsculo deixa tudo minúsculo."),
           CODE("Crie a função unicode(c) que devolve o código do caractere no formato U+XXXX, com 4 algarismos maiúsculos. Exemplo: unicode(\"é\") devolve U+00E9.",
                "def unicode(c):\n    return hex(c)\n",
                'def unicode(c):\n    return f"U+{ord(c):04X}"',
                'assert unicode("é") == "U+00E9", "unicode(\'é\') deve ser U+00E9"\nassert unicode("A") == "U+0041", "unicode(\'A\') deve ser U+0041"',
                'return f"U+{ord(c):04X}"')]),
        # lição 6
        L("Desafio: montar cores",
          "Agora o caminho inverso: de três números (0 a 255) para o texto da cor. Cada pedaço precisa de 2 algarismos hexadecimais.",
          'r, g, b = 255, 136, 0\nprint("#" + format(r, "02X") + format(g, "02X") + format(b, "02X"))',
          [OUT('print("#" + hex(0)[2:] * 3)', ["#000000", "#0x00x00x0", "#0"], "hex(0)[2:] é só 0; repetido 3 vezes dá 000."),
           TYPE('print(f"#{16:02x}{0:02x}{255:02x}")', "Cada número vira 2 algarismos hexadecimais."),
           MC("Por que format(n, \"02X\") e não hex(n)?", "Porque garante 2 algarismos e não tem 0x", ["Porque hex dá erro", "Porque hex devolve número", "Não há diferença"], "hex(5) é 0x5; as cores precisam de 05."),
           CODE("Crie a função cor_hex(r, g, b) que devolve a cor em texto, com # e letras maiúsculas. Exemplo: cor_hex(255, 136, 0) devolve #FF8800.",
                "def cor_hex(r, g, b):\n    return \"#\" + hex(r) + hex(g) + hex(b)\n",
                'def cor_hex(r, g, b):\n    return f"#{r:02X}{g:02X}{b:02X}"',
                'assert cor_hex(255, 136, 0) == "#FF8800", "cor_hex(255, 136, 0) deve ser #FF8800"\nassert cor_hex(0, 0, 0) == "#000000", "Preto deve ser #000000"\nassert cor_hex(10, 11, 12) == "#0A0B0C", "Números pequenos precisam do zero na frente"',
                'return f"#{r:02X}{g:02X}{b:02X}"')]),
    ],
    # ================================================================ ascii
    "ascii": [
        # lição 2
        L("Tipos de escape",
          "ascii escolhe o escape pelo tamanho do código: \\xNN até 255 (como é), \\uNNNN até 65535 (como 中) e \\UNNNNNNNN acima disso (como emojis). Funciona também dentro de listas e dicionários.",
          'print(ascii("é"))\nprint(ascii("中"))\nprint(ascii("😀"))\nprint(ascii(["olá", 1]))',
          [OUT('print(ascii(["pão"]))', ["['pão']", "['pao']", "['p\\\\xe3o']"], "ã vira \\xe3 dentro da lista."),
           TYPE('print(ascii(42))', "Números já são ASCII: nada muda."),
           MC("Qual escape ascii usa para um emoji?", "\\U seguido de 8 algarismos", ["\\x seguido de 2 algarismos", "Nenhum, o emoji aparece", "\\e"], "Códigos acima de 65535 usam \\U."),
           OUT('print(ascii({"nº": 1}))', ["{'nº': 1}", "{'n': 1}", "{nº: 1}"], "º tem código 186, então vira \\xba.")]),
        # lição 3
        L("Enxergando o invisível",
          "ascii (como repr) mostra caracteres invisíveis: tab vira \\t e quebra de linha vira \\n. Isso ajuda a achar espaços estranhos em dados digitados.",
          'nome = "Ana\\t"\nprint(nome + "|")\nprint(ascii(nome))\nprint(ascii("linha1\\nlinha2"))',
          [OUT('print(ascii("a b"))', ["a b", "'a\\\\sb'", "'ab'"], "Espaço normal é ASCII e aparece como espaço."),
           TYPE('print(ascii("oi\\n"))', "A quebra de linha aparece como \\n."),
           MC("Para descobrir se um texto tem um tab escondido, o melhor é…", "print(ascii(texto))", ["print(texto)", "print(len(texto))", "print(str(texto))"], "ascii mostra o \\t; o print normal só mostra um espaço grande."),
           CODE("Crie a função tem_especial(texto) que devolve True se o texto tem algum caractere fora do ASCII (acento, emoji…) e False se não tem. Dica: compare ascii(texto) com repr(texto).",
                "def tem_especial(texto):\n    return False\n",
                'def tem_especial(texto):\n    return ascii(texto) != repr(texto)',
                'assert tem_especial("café") is True, "café tem acento"\nassert tem_especial("cafe") is False, "cafe não tem acento"\nassert tem_especial("ok 👍") is True, "Emoji não é ASCII"',
                'return ascii(texto) != repr(texto)')]),
        # lição 4
        L("Cuidados com ascii",
          "ascii não tira acentos: ele troca o caractere por um código. O resultado também vem com as aspas, então o tamanho muda: ascii(\"é\") tem 6 caracteres.",
          'print(ascii("é"))\nprint(len(ascii("é")))\nprint(ascii("é") == "e")',
          [OUT('print(len(ascii("a")))', ["1", "2", "Erro"], "O resultado é 'a', com as duas aspas: 3 caracteres."),
           MC('ascii("ação") devolve…', "'a\\xe7\\xe3o'", ["acao", "'acao'", "ação"], "Cada letra especial vira seu código, e as aspas ficam."),
           TYPE('print(ascii("ok") == "ok")', "O resultado tem aspas, então não é igual a ok."),
           MC("Para escrever o texto sem as aspas extras, você usaria…", "print(texto)", ["print(ascii(texto))", "print(repr(texto))", "print(ascii(texto[0]))"], "str/print mostram o texto puro; ascii e repr colocam aspas.")]),
        # lição 5
        L("ascii, repr e !a",
          "Em f-strings, !a aplica ascii e !r aplica repr. E o resultado de ascii é código Python válido: eval(ascii(texto)) devolve o texto original.",
          'nome = "José"\nprint(f"{nome}")\nprint(f"{nome!r}")\nprint(f"{nome!a}")\nprint(eval(ascii(nome)) == nome)',
          [OUT('x = "ñ"\nprint(f"[{x!a}]")', ["[ñ]", "['ñ']", "[n]"], "!a aplica ascii: ñ vira \\xf1 com aspas."),
           TYPE('print(f"{"oi"!a}")', "Sem acentos, só ganha as aspas."),
           FILL("Complete para mostrar 'ma\\xe7\\xe3'.", 'fruta = "maçã"\nprint(f"{fruta___}")', '!a', ['!r', '!s', ':a'], "!a chama ascii dentro da f-string."),
           CODE("Crie a função log(nome) que devolve o texto usuario=<nome em ascii>. Exemplo: log(\"Zé\") devolve usuario='Z\\xe9'.",
                "def log(nome):\n    return \"usuario=\" + nome\n",
                'def log(nome):\n    return f"usuario={nome!a}"',
                'assert log("Zé") == "usuario=\'Z\\\\xe9\'", "log(\'Zé\') deve ser usuario=\'Z\\\\xe9\'"\nassert log("Bia") == "usuario=\'Bia\'", "log(\'Bia\') deve ser usuario=\'Bia\'"',
                'return f"usuario={nome!a}"  (ou "usuario=" + ascii(nome))')]),
        # lição 6
        L("Desafio: relatório seguro",
          "Sistemas antigos às vezes só aceitam ASCII. Passar cada valor por ascii garante que nada quebre, e você ainda consegue recuperar o original com eval.",
          'itens = ["pão", "café", "leite"]\nfor item in itens:\n    print(ascii(item))',
          [OUT('print(sum(1 for p in ["pão", "leite", "maçã"] if ascii(p) != repr(p)))', ["3", "1", "0"], "pão e maçã têm caracteres especiais: 2."),
           TYPE('print(ascii("§")[1:-1])', "O [1:-1] tira as aspas: sobra o escape de § (código 167)."),
           MC("Qual expressão recupera o texto original a partir de s = ascii(\"Zé\")?", "eval(s)", ["str(s)", "s.strip()", "ascii(s)"], "ascii gera código Python válido."),
           CODE("Crie a função limpar(lista) que devolve uma NOVA lista só com os textos que são 100% ASCII (sem acentos nem emojis).",
                "def limpar(lista):\n    return lista\n",
                'def limpar(lista):\n    return [t for t in lista if ascii(t) == repr(t)]',
                'assert limpar(["pão", "leite", "maçã", "ovo"]) == ["leite", "ovo"], "Devem sobrar leite e ovo"\nassert limpar([]) == [], "Lista vazia devolve lista vazia"',
                'return [t for t in lista if ascii(t) == repr(t)]')]),
    ],
    # ================================================================ format
    "format": [
        # lição 2
        L("Alinhar e preencher",
          "< alinha à esquerda, > à direita e ^ no centro; o número diz a largura. Antes do sinal, você pode pôr um caractere para preencher, como * ou -.",
          'print(format("oi", "<6") + "|")\nprint(format("oi", ">6") + "|")\nprint(format("oi", "^6") + "|")\nprint(format(42, "*^8"))',
          [OUT('print(format("ab", "-^6"))', ["ab----", "----ab", "-ab-"], "^6 centraliza em 6 caracteres, preenchendo com -."),
           TYPE('print("|" + format(7, ">3") + "|")', "Dois espaços antes do 7, ocupando 3 caracteres."),
           MC("Sem alinhamento, format(42, \"5\") alinha…", "À direita", ["À esquerda", "No centro", "Não alinha"], "Números vão para a direita por padrão; textos, para a esquerda."),
           FILL("Complete para mostrar oi.....", 'print(format("oi", ___))', '".<7"', ['"<7."', '".>7"', '"7<."'], "Primeiro o preenchimento (.), depois o alinhamento (<), depois a largura.")]),
        # lição 3
        L("Dinheiro e porcentagem",
          "\",.2f\" junta separador de milhar e 2 casas. \"+d\" mostra o sinal sempre. \".1%\" multiplica por 100 e põe o %. Para o padrão brasileiro, troque vírgula e ponto depois.",
          'print(format(1234.5, ",.2f"))\nprint(format(5, "+d"))\nprint(format(0.075, ".1%"))\nv = format(1234.5, ",.2f")\nprint(v.replace(",", "_").replace(".", ",").replace("_", "."))',
          [OUT('print(format(2500, ",.2f"))', ["2.500,00", "2500.00", "2,500"], "Formato americano: vírgula no milhar, ponto nos centavos."),
           TYPE('print(format(0.5, ".0%"))', "0.5 vezes 100, sem casas decimais."),
           OUT('print(format(-3, "+d"), format(3, "+d"))', ["3 +3", "-3 3", "+-3 +3"], "Com +, o sinal aparece nos dois."),
           CODE("Crie a função reais(valor) que devolve o valor no formato brasileiro. Exemplo: reais(1234.5) devolve R$ 1.234,50.",
                "def reais(valor):\n    return \"R$ \" + str(valor)\n",
                'def reais(valor):\n    t = format(valor, ",.2f")\n    t = t.replace(",", "_").replace(".", ",").replace("_", ".")\n    return "R$ " + t',
                'assert reais(1234.5) == "R$ 1.234,50", "reais(1234.5) deve ser R$ 1.234,50"\nassert reais(9.9) == "R$ 9,90", "reais(9.9) deve ser R$ 9,90"\nassert reais(1000000) == "R$ 1.000.000,00", "reais(1000000) deve ser R$ 1.000.000,00"',
                'Use format(valor, ",.2f") e troque vírgula por ponto e ponto por vírgula (passando por um caractere temporário).')]),
        # lição 4
        L("Cuidados com format",
          "A especificação precisa combinar com o tipo: format(\"5\", \".2f\") e format(3.7, \"d\") dão ValueError. Inteiros aceitam \"f\" numa boa. E o resultado é sempre texto.",
          'print(format(5, ".2f"))\nprint(format(3.7))\ntry:\n    format(3.7, "d")\nexcept ValueError as e:\n    print(type(e).__name__)',
          [MC('format("5", ".2f") dá…', "ValueError", ['"5.00"', '"5"', "TypeError"], "\"5\" é texto; .2f é só para números."),
           OUT('print(format(8, ".1f"))', ["8", "Erro", "8.10"], "Inteiros podem ser mostrados como decimal: 8.0."),
           TYPE('print(format(2, "03d") + format(5, "03d"))', "format devolve texto, e texto + texto junta."),
           MC("format(x) sem especificação é igual a…", "str(x)", ["repr(x)", "Erro", "int(x)"], "Sem formato, format só converte para texto.")]),
        # lição 5
        L("Tabelas e bases",
          "format também converte bases (\"b\", \"o\", \"x\") e, com larguras fixas, monta tabelas alinhadas num laço. O método \"{:>5}\".format(x) usa a mesma mini-linguagem.",
          'produtos = [("pão", 0.5), ("queijo", 12.9)]\nfor nome, preco in produtos:\n    print(format(nome, "<8") + format(preco, ">6.2f"))\nprint("{:>5}|".format("ok"))\nprint(format(10, "b"), format(10, "x"))',
          [OUT('print(format(10, "o"))', ["10", "0o12", "a"], "10 = 1×8 + 2, sem prefixo."),
           TYPE('print("|" + "{:^7}".format("py") + "|")', "^7 centraliza py em 7 caracteres."),
           ORDER("Monte o programa que mostra cada nota com 1 casa decimal.",
                 ['notas = [7, 8.25]', 'for n in notas:', '    print(format(n, ".1f"))'],
                 "Lista, laço e o print com format dentro."),
           CODE("Crie a função linha(item, preco) que devolve o item alinhado à esquerda em 10 caracteres, seguido do preço alinhado à direita em 8 caracteres com 2 casas. Exemplo: linha(\"pão\", 0.5) devolve 'pão           0.50'.",
                "def linha(item, preco):\n    return item + str(preco)\n",
                'def linha(item, preco):\n    return format(item, "<10") + format(preco, ">8.2f")',
                'assert linha("pão", 0.5) == "pão           0.50", "linha(\'pão\', 0.5) deve ter 18 caracteres: pão + 7 espaços + 4 espaços + 0.50"\nassert len(linha("x", 1)) == 18, "A linha deve ter 18 caracteres"\nassert linha("leite", 12.9).endswith("   12.90"), "O preço deve ficar à direita com 2 casas"',
                'return format(item, "<10") + format(preco, ">8.2f")')]),
        # lição 6
        L("Desafio: boletim",
          "Juntando tudo: largura, alinhamento, casas decimais e preenchimento deixam um boletim com cara de profissional.",
          'notas = {"Ana": 9.5, "Caio": 7.25}\nprint(format(" BOLETIM ", "=^20"))\nfor nome, nota in notas.items():\n    print(format(nome, ".<14") + format(nota, ">6.1f"))',
          [OUT('print(format("Teo", ".<6") + format(8, ">4.1f"))', ["Teo...8.0", "Teo... 8", "...Teo 8.0"], "Teo... ocupa 6, e \" 8.0\" ocupa 4: Teo... 8.0."),
           TYPE('print(format(" X ", "-^9"))', "Três caracteres centralizados em 9, com hífens dos lados."),
           MC('Qual especificação mostra 0.875 como 87.5%?', '".1%"', ['".1f"', '"%"', '"1%"'], "% multiplica por 100; .1 deixa uma casa."),
           CODE("Crie a função boletim(nome, nota) que devolve o nome com pontos à direita até 10 caracteres, seguido da nota com 1 casa decimal à direita em 5 caracteres. Exemplo: boletim(\"Ana\", 9.5) devolve Ana.......  9.5",
                "def boletim(nome, nota):\n    return nome + \" \" + str(nota)\n",
                'def boletim(nome, nota):\n    return format(nome, ".<10") + format(nota, ">5.1f")',
                'assert boletim("Ana", 9.5) == "Ana.......  9.5", "boletim(\'Ana\', 9.5) deve ser Ana.......  9.5"\nassert boletim("Bia", 10) == "Bia....... 10.0", "boletim(\'Bia\', 10) deve ser Bia....... 10.0"',
                'return format(nome, ".<10") + format(nota, ">5.1f")')]),
    ],
}

BUGS = r'''
@fn_ord 2
letra = "c"
print(ord(letra) - ord("a"))  # esperado: 3
>>> print(ord(letra) - ord("a") + 1)  # esperado: 3
!! Para a ser 1 e não 0, some 1 no final.

@fn_ord 2
idade = 7
print(ord(idade))
>>> print(ord(str(idade)))
!! ord recebe texto de 1 caractere, não um número.

@fn_ord 2
nome = "Bia"
print(ord(nome))  # esperado: 66
>>> print(ord(nome[0]))  # esperado: 66
!! ord aceita só UM caractere. Pegue a primeira letra com [0].

@fn_ord 2
digito = "8"
print(ord(digito) * 2)  # esperado: 16
>>> print(int(digito) * 2)  # esperado: 16
!! ord("8") é 56, o código do caractere. Para o valor do dígito, use int.

@fn_ord 3
total = 0
for c in "ab":
    total = ord(c)
print(total)  # esperado: 195
>>> total += ord(c)
!! Com = você troca o total a cada volta. Use += para somar.

@fn_ord 1
print(ord("A") - ord("a"))  # esperado: 32
>>> print(ord("a") - ord("A"))  # esperado: 32
!! As minúsculas têm códigos maiores: a (97) menos A (65).

@fn_chr 2
codigo = "65"
print(chr(codigo))
>>> print(chr(int(codigo)))
!! chr precisa de um número inteiro, não de texto.

@fn_chr 1
letras = "".join(chr(c) for c in range(65, 90))
print(letras[-1])  # esperado: Z
>>> letras = "".join(chr(c) for c in range(65, 91))
!! O range para antes do fim: para incluir o Z (90), vá até 91.

@fn_chr 2
letra = "a"
print(chr(letra + 1))
>>> print(chr(ord(letra) + 1))
!! Não dá para somar número em texto. Passe por ord primeiro.

@fn_chr 2
letra = "g"
print(chr(ord(letra) + 32))  # esperado: G
>>> print(chr(ord(letra) - 32))  # esperado: G
!! Para ir de minúscula para maiúscula, subtraia 32.

@fn_chr 2
pos = (ord("z") - ord("a") + 1) % 26
print(chr(pos))  # esperado: a
>>> print(chr(ord("a") + pos))  # esperado: a
!! pos é a posição (0 a 25). Some ord("a") para chegar ao código da letra.

@fn_chr 2
media = 65.0
print(chr(media))
>>> print(chr(int(media)))
!! chr não aceita número com ponto decimal. Converta com int.

@fn_bin 2
n = 5
print(bin(n) + 1)
>>> print(bin(n + 1))
!! bin devolve texto. Faça a conta antes de converter.

@fn_bin 2
binario = "1010"
print(int(binario))  # esperado: 10
>>> print(int(binario, 2))
!! Sem a base 2, int lê 1010 como mil e dez.

@fn_bin 1
print(bin(8)[3:])  # esperado: 1000
>>> print(bin(8)[2:])  # esperado: 1000
!! O prefixo 0b tem 2 caracteres. Corte a partir do índice 2.

@fn_bin 2
n = 13
print(bin(n).count(1))
>>> print(bin(n).count("1"))
!! bin devolve texto; o count de texto precisa de "1" com aspas.

@fn_bin 2
valor = "12"
print(bin(valor))
>>> print(bin(int(valor)))
!! bin só aceita inteiros. Converta o texto com int antes.

@fn_bin 1
print(format(5, "8b"))  # esperado: 00000101
>>> print(format(5, "08b"))  # esperado: 00000101
!! Sem o 0, format completa com espaços. Use 08b.

@fn_oct 1
modo = 755
print(oct(modo)[2:])  # esperado: 755
>>> modo = 0o755
!! 755 sem prefixo é decimal. Para escrever em octal, use 0o755.

@fn_oct 1
print(int("17"))  # esperado: 15
>>> print(int("17", 8))  # esperado: 15
!! Para ler o texto como octal, passe a base 8.

@fn_oct 2
n = 8
print(oct(n) + 1)
>>> print(oct(n + 1))
!! oct devolve texto. Some antes de converter.

@fn_oct 1
print(int("19", 8))
>>> print(int("17", 8))
!! O algarismo 9 não existe na base 8 (só de 0 a 7).

@fn_oct 2
modo = 0o644
print(oct(modo)[0])  # esperado: 6
>>> print(oct(modo)[2])  # esperado: 6
!! As duas primeiras posições são o prefixo 0o. O primeiro algarismo está no índice 2.

@fn_oct 1
print(oct(9.0))
>>> print(oct(9))
!! oct, como bin e hex, só aceita inteiros.

@fn_hex 1
print(int("ff"))
>>> print(int("ff", 16))
!! Sem a base 16, int não entende as letras de a a f.

@fn_hex 2
r, g, b = 255, 8, 0
print("#" + hex(r)[2:] + hex(g)[2:] + hex(b)[2:])  # esperado: #ff0800
>>> print("#" + format(r, "02x") + format(g, "02x") + format(b, "02x"))  # esperado: #ff0800
!! hex não completa com zero: 8 vira 8, e não 08. Use format com 02x.

@fn_hex 1
print(hex(255).upper())  # esperado: 0xFF
>>> print("0x" + hex(255)[2:].upper())  # esperado: 0xFF
!! upper deixa o x do prefixo maiúsculo também (0XFF). Converta só a parte depois do 0x.

@fn_hex 2
cor = "#00FF80"
verde = int(cor[2:4], 16)
print(verde)  # esperado: 255
>>> verde = int(cor[3:5], 16)
!! O verde é o segundo par: posições 3 e 4, depois do # e do vermelho.

@fn_hex 2
preco = 2.5
print(hex(preco))
>>> print(hex(int(preco)))
!! hex só aceita inteiros.

@fn_hex 1
print(hex("A"))
>>> print(hex(ord("A")))
!! Para ver o código de um caractere em hexadecimal, use ord antes.

@fn_ascii 2
nome = "José"
print(ascii(nome) == "Jose")  # esperado: True
>>> print(ascii(nome) == "'Jos\\xe9'")  # esperado: True
!! ascii não tira o acento: troca o é pelo escape \xe9 e coloca aspas.

@fn_ascii 2
texto = "olá"
print(len(ascii(texto)))  # esperado: 3
>>> print(len(texto))  # esperado: 3
!! ascii acrescenta aspas e escapes; o tamanho do texto original é len(texto).

@fn_ascii 2
palavra = "cafe"
print(ascii(palavra) == palavra)  # esperado: True
>>> print(ascii(palavra) == repr(palavra))  # esperado: True
!! ascii sempre tem aspas, então nunca é igual ao texto puro. Para saber se o texto é só ASCII, compare com repr.

@fn_ascii 2
x = "ñ"
print(f"{x!r}")  # esperado: '\xf1'
>>> print(f"{x!a}")  # esperado: '\xf1'
!! !r usa repr, que mostra o ñ. Para escapar, use !a.

@fn_ascii 2
seguro = ascii("Zé")
print(seguro[1:-1] == "Zé")  # esperado: True
>>> print(eval(seguro) == "Zé")  # esperado: True
!! Tirar as aspas não desfaz o escape. Use eval para recuperar o texto.

@fn_ascii 2
nomes = ["Ana", "Zé"]
print(ascii(nomes[0]))  # esperado: 'Z\xe9'
>>> print(ascii(nomes[1]))  # esperado: 'Z\xe9'
!! O índice 0 é Ana. O Zé está no índice 1.

@fn_format 2
preco = 9.5
print(format(preco, ".2"))  # esperado: 9.50
>>> print(format(preco, ".2f"))  # esperado: 9.50
!! Sem o f, .2 conta algarismos, não casas decimais.

@fn_format 2
valor = "3.5"
print(format(valor, ".2f"))
>>> print(format(float(valor), ".2f"))
!! .2f é só para números. Converta o texto com float.

@fn_format 2
nota = 7.8
print(format(nota, "d"))
>>> print(format(nota, ".0f"))
!! d é só para inteiros. Para um número com ponto, use .0f.

@fn_format 1
print(format("ab", "^6", "*"))
>>> print(format("ab", "*^6"))
!! O preenchimento vai dentro da especificação, antes do alinhamento.

@fn_format 2
total = 1500
print(format(total, ".") + " reais")  # esperado: 1,500 reais
>>> print(format(total, ",") + " reais")  # esperado: 1,500 reais
!! O separador de milhar do format é a vírgula.

@fn_format 1
print(format(0.25, ".0f%"))  # esperado: 25%
>>> print(format(0.25, ".0%"))  # esperado: 25%
!! O % já multiplica por 100 e coloca o símbolo; não use f junto.
'''
