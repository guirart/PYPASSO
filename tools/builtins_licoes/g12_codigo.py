from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ eval
    "eval": [
        # lição 2
        L("Escolhendo as variáveis",
          "eval aceita um segundo argumento: um dicionário com as variáveis que a expressão pode usar. Quando você passa esse dicionário, a expressão só enxerga o que está nele, e não as variáveis do seu programa.",
          'print(eval("preco * qtd", {"preco": 5, "qtd": 3}))\nx = 100\nprint(eval("x + 1", {"x": 1}))',
          [OUT('print(eval("a * b", {"a": 3, "b": 4}))', ["a * b", "7", "Erro"], "a vale 3 e b vale 4 dentro do dicionário: 3 * 4 = 12."),
           OUT('x = 10\nprint(eval("x + 1", {"x": 1}))', ["11", "x + 1", "Erro"], "Com o dicionário, vale o x de lá (1), não o x do programa."),
           MC('O que acontece em eval("n + 1", {"m": 5})?', "NameError: n não existe no dicionário", ["Dá 6", "Dá 1", "n vira 0 sozinho"], "A expressão só enxerga os nomes do dicionário, e lá só existe m."),
           FILL("Complete para mostrar 9.", 'print(eval("lado ** 2", ___))', '{"lado": 3}', ['"lado": 3', '[lado, 3]', '(lado=3)'], "O segundo argumento é um dicionário: chaves entre { }, nome entre aspas."),
           TYPE('print(eval("x + y", {"x": 1}, {"y": 2}))', "O terceiro argumento é um segundo dicionário (as variáveis locais). x vem de um, y do outro.")]),
        # lição 3
        L("Contas guardadas em texto",
          "Um uso comum de eval é calcular fórmulas guardadas como texto: numa lista, num arquivo de configuração ou num jogo. eval também desfaz o repr: transforma o texto de uma lista de volta em lista.",
          'formulas = ["2 + 2", "10 / 4", "3 ** 2"]\nfor f in formulas:\n    print(f, "=", eval(f))',
          [TYPE('print(eval("10 / 4"))', "A barra / sempre dá número decimal."),
           OUT('print(eval("[1, 2] * 2"))', ["[2, 4]", "[1, 2] * 2", "Erro"], "Lista vezes 2 repete a lista."),
           OUT('dados = [1, 2, 3]\ntexto = repr(dados)\ncopia = eval(texto)\nprint(copia == dados, type(texto).__name__)', ["False str", "True list", "Erro"], "repr virou texto; eval transformou o texto de volta numa lista igual."),
           CODE('Crie a função aplicar(formula, x) que calcula a fórmula (um texto) usando o valor de x. Exemplo: aplicar("x * 2 + 1", 3) devolve 7.',
                "def aplicar(formula, x):\n    return formula\n",
                'def aplicar(formula, x):\n    return eval(formula, {"x": x})',
                'assert aplicar("x * 2 + 1", 3) == 7, "aplicar(\\"x * 2 + 1\\", 3) deve devolver 7"\nassert aplicar("x ** 2", 5) == 25, "aplicar(\\"x ** 2\\", 5) deve devolver 25"',
                'return eval(formula, {"x": x}) passa o valor de x num dicionário.')]),
        # lição 4
        L("Cuidados com eval",
          "eval só aceita expressões: atribuição como x = 5 dá SyntaxError. E ele roda QUALQUER código, até apagar arquivos. Para ler listas, números e textos escritos em texto, use ast.literal_eval, que só aceita valores simples. Tirar os built-ins com {\"__builtins__\": {}} ajuda, mas não deixa eval 100% seguro.",
          'import ast\ntexto = "[10, 20, 30]"\nlista = ast.literal_eval(texto)\nprint(sum(lista))\ntry:\n    eval("x = 5")\nexcept SyntaxError:\n    print("eval não aceita atribuição")',
          [OUT('try:\n    eval("n = 1")\nexcept Exception as e:\n    print(type(e).__name__)', ["NameError", "ValueError", "None"], "n = 1 é um comando, não uma expressão: SyntaxError."),
           MC('Para transformar o texto "[1, 2, 3]" em lista com segurança, use…', "ast.literal_eval", ["eval", "list", "exec"], "list(\"[1, 2, 3]\") separaria os caracteres; eval funciona, mas não é seguro."),
           OUT('import ast\nprint(ast.literal_eval("(1, 2)")[1])', ["1", "(1, 2)", "Erro"], "literal_eval criou a tupla (1, 2); a posição 1 é o 2."),
           OUT('try:\n    eval("len(\'oi\')", {"__builtins__": {}})\nexcept NameError:\n    print("bloqueado")\nelse:\n    print("rodou")', ["rodou", "2", "Erro"], "Sem os built-ins, nem len existe: NameError."),
           MC("Um programa faz eval(input()) e alguém digita __import__('os').remove('notas.txt'). O que acontece?", "O arquivo notas.txt é apagado", ["Dá SyntaxError", "Nada, eval só faz contas", "O texto é só impresso"], "eval roda qualquer código. Nunca use eval com texto digitado pelo usuário.")]),
        # lição 5
        L("eval com outras funções",
          "Como eval é uma função comum, ele combina com map, sorted, sum e compreensões de lista. Dá até para usar eval como key para ordenar contas pelo resultado.",
          'contas = ["1 + 1", "5 * 5", "9 - 3"]\nresultados = [eval(c) for c in contas]\nprint(resultados)\nprint(max(contas, key=eval))',
          [OUT('print(list(map(eval, ["2*3", "1+1"])))', ["['2*3', '1+1']", "['6', '2']", "8"], "map aplica eval em cada texto: [6, 2]."),
           TYPE('print(sum(eval(c) for c in ["1+2", "3+4"]))', "3 + 7 = 10."),
           OUT('print(sorted(["3*3", "20-19", "2+2"], key=eval))', ["[1, 4, 9]", "['2+2', '20-19', '3*3']", "['3*3', '2+2', '20-19']"], "Ordena pelos resultados (9, 1, 4), mas a lista continua com os textos."),
           CODE("Crie a função avaliar_todas(contas) que recebe uma lista de textos e devolve um dicionário {texto: resultado}.",
                "def avaliar_todas(contas):\n    return {}\n",
                'def avaliar_todas(contas):\n    return {c: eval(c) for c in contas}',
                'assert avaliar_todas(["1+1", "2*5"]) == {"1+1": 2, "2*5": 10}, "Esperado {\'1+1\': 2, \'2*5\': 10}"\nassert avaliar_todas([]) == {}, "Lista vazia deve dar dicionário vazio"',
                "Uma compreensão de dicionário: {c: eval(c) for c in contas}.")]),
        # lição 6
        L("Desafio: calculadora segura",
          "Para uma calculadora, confira ANTES se o texto só tem dígitos, espaços e sinais de conta. set(texto) <= permitidos testa se todos os caracteres estão na lista de permitidos. Só então chame eval, sem built-ins.",
          'PERMITIDOS = set("0123456789+-*/(). ")\ndef calcular(texto):\n    if not set(texto) <= PERMITIDOS:\n        return "conta inválida"\n    return eval(texto, {"__builtins__": {}})\nprint(calcular("(2 + 3) * 4"))\nprint(calcular("__import__(\'os\')"))',
          [OUT('print(set("1+1") <= set("0123456789+"))', ["False", "{'1', '+'}", "Erro"], "Todos os caracteres de 1+1 estão entre os permitidos."),
           MC("Por que conferir os caracteres antes do eval?", "Para só deixar passar contas, sem letras nem comandos", ["Para a conta ficar mais rápida", "Porque eval não aceita espaços", "Para arredondar o resultado"], "Sem letras, ninguém consegue chamar funções perigosas."),
           TYPE('print(eval("(1 + 2) * 3", {"__builtins__": {}}))', "Contas simples não precisam de built-ins: 3 * 3."),
           CODE('Crie calcular(texto) que devolve o resultado da conta, ou o texto "inválido" se tiver algo além de dígitos, espaços, ponto e + - * / ( ).',
                "def calcular(texto):\n    return eval(texto)\n",
                'def calcular(texto):\n    if not set(texto) <= set("0123456789 .+-*/()"):\n        return "inválido"\n    return eval(texto, {"__builtins__": {}})',
                'assert calcular("2 * (3 + 4)") == 14, "calcular(\\"2 * (3 + 4)\\") deve dar 14"\nassert calcular("abs(-1)") == "inválido", "Letras devem dar \\"inválido\\""\nassert calcular("10 / 4") == 2.5, "calcular(\\"10 / 4\\") deve dar 2.5"',
                "Teste set(texto) <= set(\"0123456789 .+-*/()\") antes de chamar eval.")]),
    ],

    # ================================================================ exec
    "exec": [
        # lição 2
        L("O dicionário de variáveis",
          "Passando um dicionário para exec, o código roda \"dentro\" dele: as variáveis que já estão lá podem ser usadas, e as que o código cria (até funções) ficam guardadas nele.",
          'ns = {"base": 10}\nexec("dobro = base * 2\\ntriplo = base * 3", ns)\nprint(ns["dobro"], ns["triplo"])',
          [OUT('ns = {"x": 2}\nexec("x = x + 5", ns)\nprint(ns["x"])', ["2", "x + 5", "Erro"], "x começou com 2 no dicionário e virou 7."),
           TYPE('ns = {}\nexec("def oi():\\n    return \'olá\'", ns)\nprint(ns["oi"]())', "A função oi foi criada dentro de ns e depois chamada."),
           MC('Depois de exec("a = 1", ns), onde fica a variável a?', "Dentro do dicionário ns", ["Solta nas variáveis do programa", "Em lugar nenhum", "Num arquivo"], "Com dicionário, tudo o que o código cria vai para ele."),
           FILL("Complete para mostrar 21.", 'ns = {}\nexec("total = 3 * 7", ___)\nprint(ns["total"])', "ns", ['"ns"', "total", "{}"], "Passe o próprio dicionário, sem aspas.")]),
        # lição 3
        L("Rodando código guardado",
          "exec roda blocos inteiros: várias linhas, laços, if, def. Dá para guardar uma \"receita\" de código num texto e rodar quando quiser.",
          'receita = """\novos = 3\nfarinha = ovos * 100\nprint("Farinha:", farinha, "g")\n"""\nexec(receita)',
          [OUT('linhas = ["a = 2", "b = a * 5", "print(b)"]\nfor l in linhas:\n    exec(l)', ["2", "a * 5", "Erro"], "Cada linha roda em sequência: a = 2, b = 10, print(b)."),
           TYPE('exec("for c in \'abc\':\\n    print(c.upper(), end=\'\')")', "O laço dentro do texto mostra cada letra maiúscula, sem pular linha."),
           MC("Qual destes pode ser rodado com exec, mas NÃO com eval?", "x = 5", ["2 + 2", "len('oi')", "max(1, 2)"], "Atribuição é comando; só exec roda comandos."),
           CODE("Use exec para rodar o texto em programa e depois mostre (com print) a variável resultado que ele cria.",
                'programa = "resultado = sum(range(1, 11))"\n# rode o programa e mostre resultado\n',
                'programa = "resultado = sum(range(1, 11))"\nexec(programa)\nprint(resultado)',
                'assert __stdout__.strip() == "55", "A saída deve ser 55"',
                "exec(programa) cria resultado; depois é só print(resultado).")]),
        # lição 4
        L("Cuidados com exec",
          "Sem dicionário, exec mexe nas SUAS variáveis e pode sobrescrever qualquer uma. Erros de digitação no texto só aparecem quando ele roda. E dentro de funções, exec não cria variáveis locais de verdade: use um dicionário e leia dele.",
          'nome = "Ana"\nexec(\'nome = "Hacker"\')\nprint(nome)\nns = {}\nexec("pontos = 10", ns)\nprint(ns["pontos"])',
          [OUT('x = 1\nexec("x = 99")\nprint(x)', ["1", "x = 99", "Erro"], "Sem dicionário, exec trocou o x do programa."),
           OUT('try:\n    exec("print(\'oi\'")\nexcept SyntaxError:\n    print("código quebrado")', ["oi", "Erro", "None"], "Falta fechar o parêntese dentro do texto: SyntaxError na hora de rodar."),
           MC("Dentro de uma função, qual o jeito seguro de pegar uma variável criada por exec?", "Passar um dicionário e ler dele: exec(cod, ns) e depois ns[\"x\"]", ["Usar a variável direto, como se fosse local", "Chamar exec duas vezes", "Não tem jeito"], "exec não cria variáveis locais de verdade dentro de funções."),
           MC("Um site roda exec no texto que o visitante envia. O problema é…", "O visitante pode rodar qualquer comando no servidor", ["O site fica um pouco mais lento", "Só funciona com números", "exec não aceita textos longos"], "Assim como eval, nunca rode exec com texto de fora.")]),
        # lição 5
        L("Gerando código com f-strings",
          "Com f-strings dá para montar o código antes de rodar, por exemplo para criar várias funções parecidas. Cuidado: isso deixa o programa difícil de ler, então use com moderação.",
          'for n in [2, 3]:\n    exec(f"def vezes{n}(x):\\n    return x * {n}")\nprint(vezes2(5), vezes3(5))',
          [OUT('nome = "pontos"\nexec(f"{nome} = 50")\nprint(pontos)', ["nome", "pontos", "Erro"], "O texto montado foi pontos = 50."),
           TYPE('ns = {}\nfor i in range(3):\n    exec(f"v{i} = {i} * 10", ns)\nprint(ns["v2"])', "Foram criadas v0, v1 e v2; v2 = 2 * 10."),
           OUT('ns = {"total": 0}\nfor n in [5, 10]:\n    exec(f"total += {n}", ns)\nprint(ns["total"])', ["10", "0", "5"], "Os códigos foram total += 5 e total += 10."),
           CODE("Crie a função rodar(codigo, nome) que executa o código num dicionário novo e devolve o valor da variável chamada nome.",
                "def rodar(codigo, nome):\n    return None\n",
                'def rodar(codigo, nome):\n    ns = {}\n    exec(codigo, ns)\n    return ns[nome]',
                'assert rodar("a = 2 + 2", "a") == 4, "rodar(\\"a = 2 + 2\\", \\"a\\") deve dar 4"\nassert rodar("x = \'oi\'\\ny = x * 2", "y") == "oioi", "Deve funcionar com várias linhas"',
                "Crie ns = {}, rode exec(codigo, ns) e devolva ns[nome].")]),
        # lição 6
        L("Desafio: mini roteiro",
          "Rodando vários textos no MESMO dicionário, um passo enxerga o que o anterior criou. Detalhe: exec coloca no dicionário a chave __builtins__, para o código poder usar print, len etc.",
          'roteiro = ["vida = 100", "vida -= 30", "vida -= 25"]\nestado = {}\nfor passo in roteiro:\n    exec(passo, estado)\nprint("Vida final:", estado["vida"])\nprint("__builtins__" in estado)',
          [OUT('estado = {}\nexec("x = 1", estado)\nprint("__builtins__" in estado)', ["False", "Erro", "None"], "exec acrescenta __builtins__ ao dicionário."),
           TYPE('e = {}\nfor p in ["n = 2", "n = n ** 3", "n = n - 1"]:\n    exec(p, e)\nprint(e["n"])', "2 ao cubo é 8; menos 1 dá 7."),
           ORDER("Monte o programa que cria um dicionário, roda um código nele e mostra o resultado.", ['ns = {}', 'exec("moedas = 7 * 3", ns)', 'print(ns["moedas"])'], "Primeiro o dicionário, depois o exec, por fim a leitura."),
           CODE("Crie executar_roteiro(passos) que roda cada texto da lista no mesmo dicionário e devolve o valor final de placar.",
                "def executar_roteiro(passos):\n    estado = {}\n    return 0\n",
                'def executar_roteiro(passos):\n    estado = {}\n    for p in passos:\n        exec(p, estado)\n    return estado["placar"]',
                'assert executar_roteiro(["placar = 0", "placar += 3", "placar *= 2"]) == 6, "Esperado 6"\nassert executar_roteiro(["placar = 10"]) == 10, "Esperado 10"',
                "Um for com exec(p, estado) e, no fim, return estado[\"placar\"].")]),
    ],

    # ================================================================ compile
    "compile": [
        # lição 2
        L("Os três modos",
          "\"eval\" é para UMA expressão (rode com eval). \"exec\" é para comandos e blocos (rode com exec). \"single\" é para uma linha como no terminal: se for uma expressão, o valor aparece sozinho na tela.",
          'c1 = compile("2 + 3", "<conta>", "eval")\nprint(eval(c1))\nc2 = compile("a = 4\\nprint(a * 2)", "<bloco>", "exec")\nexec(c2)\nc3 = compile("7 * 6", "<terminal>", "single")\nexec(c3)',
          [OUT('c = compile("10 - 3", "<t>", "eval")\nprint(eval(c))', ["10 - 3", "None", "Erro"], "O código compilado no modo eval é calculado por eval."),
           OUT('c = compile("5 * 5", "<t>", "single")\nexec(c)', ["Nada aparece", "5 * 5", "None"], "No modo single, o valor de uma expressão aparece como no terminal."),
           MC('Qual modo aceita "for i in range(3): print(i)"?', '"exec"', ['"eval"', '"expr"', '"loop"'], "Laços são comandos: modo exec."),
           TYPE('c = compile("x = 6\\nprint(x // 4)", "<t>", "exec")\nexec(c)', "6 // 4 é 1 (divisão inteira).")]),
        # lição 3
        L("Compilar uma vez, rodar muitas",
          "compile analisa o texto uma vez só. Depois, o mesmo objeto code pode rodar quantas vezes quiser, cada vez com um dicionário de variáveis diferente.",
          'formula = compile("preco * qtd", "<formula>", "eval")\npedidos = [(5, 2), (3, 10)]\nfor preco, qtd in pedidos:\n    print(eval(formula, {"preco": preco, "qtd": qtd}))',
          [OUT('f = compile("n * n", "<f>", "eval")\nprint([eval(f, {"n": n}) for n in range(1, 4)])', ["[1, 2, 3]", "[2, 4, 6]", "['n * n', 'n * n', 'n * n']"], "A mesma fórmula com n = 1, 2 e 3."),
           MC("Qual a vantagem de compilar antes de rodar várias vezes?", "O texto é analisado uma vez só", ["O código fica secreto", "Dispensa eval e exec", "Deixa o eval seguro"], "Sem compile, eval analisaria o texto a cada vez."),
           TYPE('c = compile("total += 1", "<c>", "exec")\nns = {"total": 0}\nfor _ in range(4):\n    exec(c, ns)\nprint(ns["total"])', "O mesmo código rodou 4 vezes no mesmo dicionário."),
           CODE("Crie tabela(formula) que compila a fórmula UMA vez e devolve a lista de resultados para x de 0 a 4.",
                "def tabela(formula):\n    return []\n",
                'def tabela(formula):\n    c = compile(formula, "<formula>", "eval")\n    return [eval(c, {"x": x}) for x in range(5)]',
                'assert tabela("x * 10") == [0, 10, 20, 30, 40], "tabela(\\"x * 10\\") deve dar [0, 10, 20, 30, 40]"\nassert tabela("x + 1") == [1, 2, 3, 4, 5], "tabela(\\"x + 1\\") deve dar [1, 2, 3, 4, 5]"',
                'Compile com o modo "eval" e use eval(c, {"x": x}) para cada x.')]),
        # lição 4
        L("Pegadinhas do compile",
          "compile NÃO roda nada: só confere a sintaxe e prepara. Por isso, erros de sintaxe aparecem já no compile, mas nomes que não existem só dão erro na hora de rodar. O modo errado (comando no modo eval) dá SyntaxError.",
          'try:\n    compile("x = 1", "<t>", "eval")\nexcept SyntaxError:\n    print("atribuição não é expressão")\nc = compile("print(\'rodei\')", "<t>", "exec")\nprint("compilado, mas ainda não rodou")\nexec(c)',
          [OUT('c = compile("print(\'oi\')", "<t>", "exec")\nprint("fim")', ["oi\nfim", "oi", "Erro"], "compile só prepara; o print('oi') nunca rodou."),
           OUT('try:\n    compile("1 +", "<t>", "eval")\nexcept SyntaxError:\n    print("erro de sintaxe")\nprint("seguiu")', ["seguiu", "erro de sintaxe", "1 +\nseguiu"], "A conta está incompleta: o erro é capturado e o programa segue."),
           OUT('c = compile("z + 1", "<t>", "eval")\nprint("compilou")', ["Erro", "NameError", "z + 1"], "z não existe, mas compile não roda o código; só daria erro no eval."),
           OUT('try:\n    compile("x = ", "receita.py", "exec")\nexcept SyntaxError as e:\n    print(e.filename)', ["<t>", "x = ", "SyntaxError"], "O segundo argumento é o nome que aparece nos erros."),
           MC('compile("y = 2", "<t>", "eval") dá SyntaxError porque…', "O modo eval só aceita expressões", ["y não existe", "Falta o print", "O nome <t> é inválido"], 'Para comandos, use o modo "exec".')]),
        # lição 5
        L("Por dentro do objeto code",
          "O resultado de compile é um objeto do tipo code. Ele guarda informações úteis: co_filename é o nome que você deu, e co_names é uma tupla com os nomes que o código usa (sem repetir).",
          'c = compile("total = preco * qtd", "<pedido>", "exec")\nprint(type(c).__name__)\nprint(c.co_filename)\nprint(c.co_names)',
          [TYPE('c = compile("1 + 1", "minha_conta", "eval")\nprint(c.co_filename)', "É o nome passado no segundo argumento."),
           OUT('c = compile("a + b", "<t>", "eval")\nprint(c.co_names)', ["a + b", "['a', 'b']", "2"], "co_names é uma tupla de nomes: ('a', 'b')."),
           OUT('c = compile("x * 2", "<t>", "eval")\nprint(eval(c, {"x": 4}), eval(c, {"x": "ab"}))', ["8 8", "Erro", "8 ab2"], "O mesmo código: 4 * 2 = 8 e \"ab\" * 2 = abab."),
           CODE('Crie variaveis_usadas(formula) que compila a fórmula no modo "eval" e devolve a LISTA em ordem alfabética dos nomes que ela usa (co_names).',
                "def variaveis_usadas(formula):\n    return []\n",
                'def variaveis_usadas(formula):\n    return sorted(compile(formula, "<f>", "eval").co_names)',
                'assert variaveis_usadas("b * a + b") == ["a", "b"], "Esperado [\'a\', \'b\']"\nassert variaveis_usadas("max(x, y)") == ["max", "x", "y"], "Funções chamadas também contam"',
                'sorted(compile(formula, "<f>", "eval").co_names) já devolve uma lista ordenada.')]),
        # lição 6
        L("Desafio: mini terminal",
          "O terminal do Python tenta primeiro o modo \"eval\": se a linha for expressão, mostra o valor. Se der SyntaxError, a linha é um comando e roda no modo \"exec\". Tudo no mesmo dicionário, para lembrar as variáveis.",
          'def rodar(linha, ns):\n    try:\n        c = compile(linha, "<terminal>", "eval")\n        print("=>", eval(c, ns))\n    except SyntaxError:\n        exec(compile(linha, "<terminal>", "exec"), ns)\n\nns = {}\nrodar("x = 5", ns)\nrodar("x * 3", ns)',
          [OUT('ns = {}\nfor linha in ["a = 2", "a + 1"]:\n    try:\n        print(eval(compile(linha, "<t>", "eval"), ns))\n    except SyntaxError:\n        exec(linha, ns)', ["a = 2\n3", "2\n3", "Erro"], "a = 2 não é expressão: roda calado. a + 1 mostra 3."),
           MC("Num terminal de Python, por que tentar primeiro o modo eval?", "Para mostrar o valor quando a linha é uma expressão", ["Porque é mais seguro", "Porque exec não aceita contas", "Para apagar as variáveis"], "Comandos não têm valor; expressões têm."),
           TYPE('ns = {}\nexec(compile("n = 4", "<t>", "single"), ns)\nexec(compile("n * n", "<t>", "single"), ns)', "A atribuição não mostra nada; a expressão n * n aparece sozinha."),
           CODE("Crie mini_terminal(linhas) que roda todas as linhas num mesmo dicionário e devolve a lista dos valores das linhas que são expressões.",
                "def mini_terminal(linhas):\n    valores = []\n    return valores\n",
                'def mini_terminal(linhas):\n    ns = {}\n    valores = []\n    for linha in linhas:\n        try:\n            c = compile(linha, "<t>", "eval")\n        except SyntaxError:\n            exec(compile(linha, "<t>", "exec"), ns)\n        else:\n            valores.append(eval(c, ns))\n    return valores',
                'assert mini_terminal(["x = 2", "x * 5", "y = x + 1", "y"]) == [10, 3], "Esperado [10, 3]"\nassert mini_terminal(["z = 1"]) == [], "Só comandos: lista vazia"',
                'Tente compile no modo "eval"; no except SyntaxError, rode com exec.')]),
    ],

    # ================================================================ globals
    "globals": [
        # lição 2
        L("Criar e mudar pelo nome",
          "globals() devolve o dicionário de verdade das variáveis globais. Então globals()[\"nome\"] = valor cria (ou muda) uma variável pelo nome em texto. E .get(nome, padrão) evita erro quando o nome não existe.",
          'globals()["moedas"] = 30\nprint(moedas)\nglobals()["moedas"] += 5\nprint(moedas)\nprint(globals().get("vidas", "não existe"))',
          [OUT('globals()["cor"] = "azul"\nprint(cor)', ["cor", "Erro", "None"], "A chave \"cor\" virou a variável cor."),
           TYPE('x = 1\nglobals()["x"] = 7\nprint(x * 2)', "x foi trocado para 7 pelo dicionário."),
           OUT('print(globals().get("fantasma", 0))', ["fantasma", "None", "Erro"], "fantasma não existe, então vem o padrão 0."),
           FILL("Complete para mostrar 8.", 'pontos = 8\nprint(globals()[___])', '"pontos"', ["pontos", "8", "[pontos]"], "As chaves do dicionário são os NOMES, em texto.")]),
        # lição 3
        L("globals dentro de funções",
          "Mesmo chamado dentro de uma função, globals() mostra as variáveis do arquivo, não as da função. Um uso prático: chamar uma função cujo nome está num texto, como um comando digitado.",
          'def pular():\n    return "pulou!"\n\ndef correr():\n    return "correu!"\n\ncomando = "pular"\nprint(globals()[comando]())',
          [OUT('nivel = 3\ndef ver():\n    return globals()["nivel"]\nprint(ver())', ["nivel", "Erro", "None"], "Dentro da função, globals() ainda enxerga nivel."),
           OUT('def f():\n    segredo = 1\n    return "segredo" in globals()\nprint(f())', ["True", "1", "Erro"], "segredo é local da função; não está em globals(): False."),
           TYPE('def oi():\n    return "olá"\ndef tchau():\n    return "até mais"\nprint(globals()["tchau"]())', "Pegou a função tchau pelo nome e chamou com ()."),
           CODE('Crie a função chamar(nome) que procura uma função global pelo nome e devolve o resultado dela. Se não existir, devolva "comando desconhecido".',
                'def atacar():\n    return "ataque!"\n\ndef defender():\n    return "escudo!"\n\ndef chamar(nome):\n    return None\n',
                'def atacar():\n    return "ataque!"\n\ndef defender():\n    return "escudo!"\n\ndef chamar(nome):\n    f = globals().get(nome)\n    if f is None:\n        return "comando desconhecido"\n    return f()',
                'assert chamar("atacar") == "ataque!", "chamar(\\"atacar\\") deve dar ataque!"\nassert chamar("defender") == "escudo!", "chamar(\\"defender\\") deve dar escudo!"\nassert chamar("voar") == "comando desconhecido", "Nome inexistente deve dar comando desconhecido"',
                "Use globals().get(nome) e confira se veio None.")]),
        # lição 4
        L("Cuidados com globals",
          "Pedir um nome que não existe dá KeyError. Para mudar uma variável global dentro de uma função, o jeito normal é a palavra global. E não imprima globals() inteiro: ele tem muitas coisas internas do Python, como __name__ e __builtins__.",
          'contador = 0\ndef somar():\n    global contador\n    contador += 1\nsomar()\nsomar()\nprint(contador)\nprint("__name__" in globals())',
          [OUT('try:\n    print(globals()["nada"])\nexcept KeyError:\n    print("não achei")', ["None", "nada", "Erro"], "Chave inexistente no dicionário: KeyError."),
           OUT('contador = 0\ndef somar():\n    contador += 1\ntry:\n    somar()\nexcept UnboundLocalError:\n    print("faltou global")', ["1", "0", "Erro de sintaxe"], "Sem global, o Python acha que contador é local e ainda não tem valor."),
           MC("Por que não é boa ideia fazer print(globals())?", "Mostra um dicionário enorme, com coisas internas do Python", ["Dá erro sempre", "Apaga as variáveis", "Mostra só uma variável"], "Prefira testar com in ou pegar uma chave."),
           TYPE('print(globals()["__name__"])', "No programa principal, __name__ vale __main__.")]),
        # lição 5
        L("Procurando nomes",
          "Como globals() é um dicionário, dá para percorrer os nomes e filtrar. Use list(globals()) para tirar uma cópia dos nomes antes de percorrer, assim nada muda no meio do caminho.",
          'def teste_soma():\n    return 1 + 1 == 2\n\ndef teste_texto():\n    return "a" * 2 == "aa"\n\ntestes = [n for n in list(globals()) if n.startswith("teste_")]\nprint(testes)\nfor n in testes:\n    print(n, globals()[n]())',
          [OUT('preco_cafe = 5\npreco_bolo = 8\ntotal = 0\nprint(sum(v for k, v in list(globals().items()) if k.startswith("preco_")))', ["0", "2", "Erro"], "Soma só as variáveis que começam com preco_: 5 + 8."),
           TYPE('a1 = 10\na2 = 20\nprint(globals()["a" + str(2)])', "O nome montado é a2."),
           OUT('def x_um(): return 1\ndef x_dois(): return 2\nnomes = [n for n in list(globals()) if n.startswith("x_")]\nprint(nomes)', ["['x_dois', 'x_um']", "[1, 2]", "['x_um']"], "Os nomes aparecem na ordem em que foram criados."),
           CODE("Crie a função somar_precos() que soma os valores de todas as variáveis globais cujo nome começa com preco_.",
                'preco_pao = 2\npreco_leite = 5\npreco_queijo = 12\n\ndef somar_precos():\n    return 0\n',
                'preco_pao = 2\npreco_leite = 5\npreco_queijo = 12\n\ndef somar_precos():\n    return sum(v for k, v in globals().items() if k.startswith("preco_"))',
                'assert somar_precos() == 19, "2 + 5 + 12 = 19"',
                'sum(v for k, v in globals().items() if k.startswith("preco_")).')]),
        # lição 6
        L("Desafio: menu de comandos",
          "Juntando tudo: funções com o prefixo cmd_ viram comandos. O texto digitado ganha o prefixo e é procurado em globals(). O prefixo garante que só funções de comando possam ser chamadas.",
          'def cmd_ola():\n    return "Olá!"\n\ndef cmd_soma():\n    return 2 + 2\n\ndef executar(texto):\n    funcao = globals().get("cmd_" + texto)\n    if funcao is None:\n        return "não conheço " + texto\n    return funcao()\n\nprint(executar("ola"))\nprint(executar("soma"))\nprint(executar("voar"))',
          [OUT('def cmd_a():\n    return "A"\nprint(globals().get("cmd_" + "b", lambda: "?")())', ["A", "None", "Erro"], "cmd_b não existe; veio o padrão, uma função que devolve ?."),
           MC("Por que usar o prefixo cmd_ nos nomes?", "Para que só funções de comando possam ser chamadas pelo texto", ["Porque o Python exige", "Para ficar mais rápido", "Para criar variáveis locais"], "Sem prefixo, alguém poderia chamar qualquer função do programa."),
           TYPE('def cmd_dobro():\n    return 21 * 2\nprint(globals()["cmd_" + "dobro"]())', "Montou o nome cmd_dobro e chamou a função."),
           CODE("Crie listar_comandos() que devolve a lista, em ordem alfabética, dos nomes de comando SEM o prefixo cmd_.",
                'def cmd_pular():\n    pass\n\ndef cmd_atacar():\n    pass\n\ndef cmd_fugir():\n    pass\n\ndef listar_comandos():\n    return []\n',
                'def cmd_pular():\n    pass\n\ndef cmd_atacar():\n    pass\n\ndef cmd_fugir():\n    pass\n\ndef listar_comandos():\n    return sorted(n[4:] for n in globals() if n.startswith("cmd_"))',
                'assert listar_comandos() == ["atacar", "fugir", "pular"], "Esperado [\'atacar\', \'fugir\', \'pular\']"',
                'Filtre os nomes com startswith("cmd_"), corte com n[4:] e use sorted.')]),
    ],

    # ================================================================ locals
    "locals": [
        # lição 2
        L("Parâmetros também contam",
          "Os parâmetros são variáveis locais, então já aparecem em locals() logo no começo da função. Cada variável nova criada depois também passa a aparecer.",
          'def pedido(item, qtd=1):\n    print(sorted(locals()))\n    total = qtd * 5\n    print(sorted(locals()))\n\npedido("pão", 3)',
          [OUT('def f(a, b=2):\n    return locals()["b"]\nprint(f(1))', ["1", "b", "Erro"], "b não foi passado, então vale o padrão 2."),
           TYPE('def g(x, y):\n    return len(locals())\nprint(g(1, 2))', "Os dois parâmetros são locais."),
           OUT('def h(n):\n    antes = len(locals())\n    m = n + 1\n    return antes, len(locals())\nprint(h(5))', ["(1, 1)", "(2, 2)", "(2, 3)"], "No começo só existe n (1). No fim: n, antes e m (3)."),
           MC("Logo no começo de uma função, o que locals() já tem?", "Os parâmetros recebidos", ["Nada", "As variáveis globais", "Todas as variáveis que a função vai criar"], "Variáveis criadas depois só aparecem depois.")]),
        # lição 3
        L("Usos práticos",
          "Um atalho comum: .format(**locals()) preenche as chaves {nome} de um texto com as variáveis locais de mesmo nome. Também dá para devolver locals() para ver as opções que a função recebeu.",
          'def ficha(nome, idade):\n    cidade = "Recife"\n    return "{nome}, {idade} anos, de {cidade}".format(**locals())\n\nprint(ficha("Bia", 12))',
          [TYPE('def f(prato, preco):\n    return "{prato}: R$ {preco}".format(**locals())\nprint(f("sopa", 12))', "{prato} e {preco} foram preenchidos com as variáveis locais."),
           OUT('def config(cor="azul", tam=10):\n    return locals()\nc = config(tam=3)\nprint(c["cor"], c["tam"])', ["azul 10", "None 3", "Erro"], "cor ficou com o padrão; tam recebeu 3."),
           MC("Para preencher {nome} e {idade} de um texto com as variáveis locais, um atalho é…", ".format(**locals())", [".format(locals)", ".format(*locals())", ".format(globals)"], "Os dois asteriscos abrem o dicionário em argumentos com nome."),
           CODE('Crie recibo(cliente, valor) que cria desconto = valor // 10 e devolve o texto "<cliente> pagou <valor> com desconto de <desconto>", usando .format(**locals()).',
                'def recibo(cliente, valor):\n    desconto = valor // 10\n    return ""\n',
                'def recibo(cliente, valor):\n    desconto = valor // 10\n    return "{cliente} pagou {valor} com desconto de {desconto}".format(**locals())',
                'assert recibo("Ana", 50) == "Ana pagou 50 com desconto de 5", "Esperado: Ana pagou 50 com desconto de 5"\nassert recibo("Teo", 120) == "Teo pagou 120 com desconto de 12", "Esperado: Teo pagou 120 com desconto de 12"',
                'return "{cliente} pagou {valor} com desconto de {desconto}".format(**locals())')]),
        # lição 4
        L("Cuidados com locals",
          "Dentro de uma função, locals() é uma cópia para consulta: mudar o dicionário NÃO muda a variável. Variáveis globais não aparecem em locals() da função. Fora de funções, locals() é o mesmo que globals().",
          'def teste():\n    x = 1\n    locals()["x"] = 99\n    print(x)\n\nteste()',
          [OUT('def f():\n    v = 5\n    locals()["v"] = 0\n    return v\nprint(f())', ["0", "Erro", "None"], "Mudar o dicionário não muda a variável v."),
           OUT('def f():\n    return "y" in locals()\ny = 3\nprint(f())', ["True", "3", "Erro"], "y é global; não está entre as locais da função."),
           MC('Mudar locals()["x"] dentro de uma função…', "Não muda a variável x de verdade", ["Muda x na hora", "Cria uma variável global", "Apaga x"], "Para mudar x, faça x = novo valor."),
           OUT('print(locals() is globals())', ["False", "Erro", "None"], "No nível de cima do arquivo, os dois são o mesmo dicionário.")]),
        # lição 5
        L("Combinando com outras funções",
          "locals() combina com sum, sorted e dict. Dica: antes de usar compreensões, guarde uma cópia com d = dict(locals()). Assim você não se confunde com as variáveis da própria compreensão.",
          'def filtro(cor=None, tamanho="M", marca=None):\n    opcoes = dict(locals())\n    return {k: v for k, v in opcoes.items() if v is not None}\n\nprint(filtro(cor="verde"))',
          [OUT('def f(a, b, c):\n    return sum(locals().values())\nprint(f(1, 2, 3))', ["3", "abc", "Erro"], "Os valores locais são 1, 2 e 3."),
           TYPE('def f(nome, sobrenome):\n    return " ".join(sorted(locals()))\nprint(f("a", "b"))', "sorted(locals()) dá os NOMES das variáveis em ordem."),
           OUT('def f(p=None, q=1, r=None):\n    d = dict(locals())\n    return [k for k in d if d[k] is None]\nprint(f(q=None))', ["['p', 'r']", "['q']", "[]"], "Com q=None, os três ficaram None."),
           CODE("Crie preenchidos(nome=None, email=None, telefone=None) que devolve a lista dos nomes dos parâmetros que NÃO são None, na ordem dos parâmetros.",
                'def preenchidos(nome=None, email=None, telefone=None):\n    return []\n',
                'def preenchidos(nome=None, email=None, telefone=None):\n    d = dict(locals())\n    return [k for k in d if d[k] is not None]',
                'assert preenchidos(email="a@b.com") == ["email"], "Esperado [\'email\']"\nassert preenchidos("Ana", telefone="9") == ["nome", "telefone"], "Esperado [\'nome\', \'telefone\']"\nassert preenchidos(nome="Bia", email="x") == ["nome", "email"], "Esperado [\'nome\', \'email\']"',
                "Guarde d = dict(locals()) e filtre os que não são None.")]),
        # lição 6
        L("Desafio: espião de variáveis",
          "Um truque de depuração: no fim da função, percorra sorted(locals().items()) e mostre cada nome com seu valor. Você vê tudo o que a função calculou.",
          'def compra(preco, qtd):\n    total = preco * qtd\n    for nome, valor in sorted(locals().items()):\n        print(f"{nome} = {valor}")\n\ncompra(4, 3)',
          [OUT('def f(b, a):\n    return sorted(locals())[0]\nprint(f(1, 2))', ["b", "1", "2"], "Em ordem alfabética, a vem antes de b."),
           TYPE('def f(x):\n    y = x * 2\n    return locals()["y"] + locals()["x"]\nprint(f(4))', "y = 8 e x = 4."),
           MC("Dentro de uma função, qual a diferença entre locals() e globals()?", "locals tem as variáveis da função; globals, as do arquivo", ["São iguais", "globals tem as da função; locals, as do arquivo", "locals só tem os parâmetros"], "Cada função tem o seu próprio espaço local."),
           CODE('Crie resumo(a, b) que calcula soma = a + b e devolve um texto com as variáveis locais em ordem alfabética, no formato "a=1, b=2, soma=3".',
                'def resumo(a, b):\n    soma = a + b\n    return ""\n',
                'def resumo(a, b):\n    soma = a + b\n    d = dict(locals())\n    return ", ".join(f"{k}={d[k]}" for k in sorted(d))',
                'assert resumo(1, 2) == "a=1, b=2, soma=3", "Esperado: a=1, b=2, soma=3"\nassert resumo(5, 5) == "a=5, b=5, soma=10", "Esperado: a=5, b=5, soma=10"',
                "Guarde d = dict(locals()) antes do join: dentro do gerador, locals() seria outro.")]),
    ],

    # ================================================================ __import__
    "__import__": [
        # lição 2
        L("Pacotes e submódulos",
          "Pegadinha: __import__(\"json.decoder\") carrega o submódulo, mas devolve o pacote de cima, json. Para receber o submódulo, passe fromlist com algo que ele tem, ou use importlib.import_module, que já devolve o que você pediu.",
          'a = __import__("collections.abc")\nprint(a.__name__)\nb = __import__("collections.abc", fromlist=["Sized"])\nprint(b.__name__)\nimport importlib\nc = importlib.import_module("collections.abc")\nprint(c.__name__)',
          [OUT('m = __import__("json.decoder")\nprint(m.__name__)', ["json.decoder", "decoder", "Erro"], "Sem fromlist, __import__ devolve o pacote de cima: json."),
           TYPE('m = __import__("json.decoder", fromlist=["JSONDecoder"])\nprint(m.__name__)', "Com fromlist, vem o próprio submódulo."),
           MC("Para receber direto o submódulo json.decoder pelo nome, o mais simples é…", 'importlib.import_module("json.decoder")', ['__import__("json.decoder")', 'eval("json.decoder")', 'open("json.decoder")'], "import_module devolve exatamente o módulo pedido."),
           OUT('import importlib\nm = importlib.import_module("collections.abc")\nprint(m.__name__)', ["collections", "abc", "Erro"], "import_module devolve o submódulo collections.abc.")]),
        # lição 3
        L("Escolhendo o módulo na hora",
          "Com o nome do módulo e o nome da função em textos, __import__ carrega o módulo e getattr pega a função. Assim o programa decide na hora o que usar.",
          'pedidos = [("math", "sqrt", 81), ("math", "factorial", 5)]\nfor modulo, funcao, valor in pedidos:\n    m = __import__(modulo)\n    print(funcao, getattr(m, funcao)(valor))',
          [OUT('m = __import__("math")\nprint(getattr(m, "ceil")(4.1))', ["4", "4.1", "ceil"], "ceil arredonda para cima: 5."),
           TYPE('nome = "statistics"\nest = __import__(nome)\nprint(est.mean([2, 4, 6]))', "A média de 2, 4 e 6."),
           OUT('formatos = {"json": "dumps"}\nm = __import__("json")\nprint(getattr(m, formatos["json"])([1, 2]))', ["[1,2]", "dumps", "Erro"], "json.dumps transforma a lista no texto [1, 2]."),
           CODE("Crie usar(modulo, funcao, valor) que importa o módulo pelo nome, pega a função pelo nome e devolve o resultado dela com valor.",
                "def usar(modulo, funcao, valor):\n    return None\n",
                'def usar(modulo, funcao, valor):\n    return getattr(__import__(modulo), funcao)(valor)',
                'assert usar("math", "sqrt", 49) == 7.0, "usar(\\"math\\", \\"sqrt\\", 49) deve dar 7.0"\nassert usar("math", "floor", 2.7) == 2, "usar(\\"math\\", \\"floor\\", 2.7) deve dar 2"',
                "getattr(__import__(modulo), funcao)(valor).")]),
        # lição 4
        L("Cuidados com __import__",
          "__import__ não cria variável sozinho: guarde o resultado. Nome errado dá ModuleNotFoundError. E cada módulo é carregado uma vez só: importar de novo devolve o mesmo objeto. Nunca importe nomes digitados pelo usuário sem conferir.",
          '__import__("math")\ntry:\n    print(math.pi)\nexcept NameError:\n    print("math não virou variável")\nm = __import__("math")\nprint(round(m.pi, 2))',
          [OUT('try:\n    __import__("modulo_que_nao_existe")\nexcept ModuleNotFoundError:\n    print("não achei")', ["None", "modulo_que_nao_existe", "Erro de sintaxe"], "Módulo inexistente: ModuleNotFoundError."),
           OUT('a = __import__("math")\nb = __import__("math")\nprint(a is b)', ["False", "Erro", "math"], "Módulos ficam guardados depois da primeira carga: é o mesmo objeto."),
           MC('__import__("random") sozinho, sem guardar o resultado…', "Carrega o módulo, mas não cria a variável random", ["Cria a variável random", "Dá erro", "Não faz nada"], "Faça r = __import__(\"random\")."),
           TYPE('m = __import__("string")\nprint(m.ascii_uppercase[:3])', "As três primeiras letras maiúsculas.")]),
        # lição 5
        L("Combinando com outras funções",
          "__import__ é uma função comum: dá para usar com map, numa compreensão de dicionário ou junto com hasattr para conferir se o módulo tem o que você precisa.",
          'nomes = ["math", "json", "string"]\nmodulos = {n: __import__(n) for n in nomes}\nprint(modulos["math"].sqrt(9))\nprint(hasattr(modulos["json"], "dumps"))',
          [OUT('mods = list(map(__import__, ["math", "json"]))\nprint([m.__name__ for m in mods])', ["['math']", "[math, json]", "Erro"], "map importou os dois; os nomes vêm como textos."),
           TYPE('m = __import__("math")\nprint(hasattr(m, "voar"))', "math não tem nada chamado voar."),
           OUT('texto = "a1b2"\nm = __import__("string")\nprint(sum(c in m.digits for c in texto))', ["4", "a1b2", "0"], "Só 1 e 2 são dígitos; cada True conta 1."),
           CODE("Crie disponiveis(nomes) que devolve a lista só com os nomes de módulos que existem (use try/except ModuleNotFoundError).",
                "def disponiveis(nomes):\n    return nomes\n",
                'def disponiveis(nomes):\n    ok = []\n    for n in nomes:\n        try:\n            __import__(n)\n        except ModuleNotFoundError:\n            continue\n        ok.append(n)\n    return ok',
                'assert disponiveis(["math", "xyz_nao_existe", "json"]) == ["math", "json"], "Esperado [\'math\', \'json\']"\nassert disponiveis([]) == [], "Lista vazia deve dar lista vazia"',
                "Tente __import__(n); se der ModuleNotFoundError, pule.")]),
        # lição 6
        L("Desafio: carregador de plugins",
          "Muitos programas recebem textos como \"math:sqrt\" para saber qual função usar. Basta separar com split(\":\"), importar o módulo e pegar a função com getattr.",
          'def carregar(caminho):\n    modulo, funcao = caminho.split(":")\n    m = __import__(modulo)\n    return getattr(m, funcao)\n\nraiz = carregar("math:sqrt")\nprint(raiz(144))',
          [OUT('modulo, funcao = "math:floor".split(":")\nprint(getattr(__import__(modulo), funcao)(7.9))', ["7.9", "8", "floor"], "floor arredonda para baixo: 7."),
           MC('O texto "json:dumps" separado com split(":") vira…', "['json', 'dumps']", ["'json dumps'", "('json:', 'dumps')", "['json:dumps']"], "split devolve uma lista com as partes, sem o separador."),
           TYPE('f = getattr(__import__("math"), "factorial")\nprint(f(4))', "4! = 4 * 3 * 2 * 1."),
           CODE('Crie carregar(caminho) que recebe "modulo:funcao" e devolve a função. Se o módulo não existir, devolva None.',
                'def carregar(caminho):\n    modulo, funcao = caminho.split(":")\n    return None\n',
                'def carregar(caminho):\n    modulo, funcao = caminho.split(":")\n    try:\n        m = __import__(modulo)\n    except ModuleNotFoundError:\n        return None\n    return getattr(m, funcao)',
                'assert carregar("math:sqrt")(25) == 5.0, "carregar(\\"math:sqrt\\") deve devolver a função sqrt"\nassert carregar("naoexiste:x") is None, "Módulo inexistente deve dar None"',
                "Separe com split, importe dentro de try e devolva getattr(m, funcao).")]),
    ],

    # ================================================================ breakpoint
    "breakpoint": [
        # lição 2
        L("O gancho por trás",
          "breakpoint() não faz nada sozinho: ele chama sys.breakpointhook, passando os argumentos que você der. O gancho normal abre o pdb; o original fica guardado em sys.__breakpointhook__. Aqui, sempre trocamos o gancho por uma função que imprime.",
          'import sys\ndef meu_gancho(*args, **kwargs):\n    print("pausa com", args, kwargs)\nsys.breakpointhook = meu_gancho\nbreakpoint()\nbreakpoint("aqui", nivel=2)',
          [OUT('import sys\nsys.breakpointhook = lambda *a: print(len(a))\nbreakpoint(1, 2, 3)', ["1", "(1, 2, 3)", "Erro"], "Os três argumentos chegam ao gancho."),
           TYPE('import sys\nsys.breakpointhook = lambda msg: print("parei:", msg)\nbreakpoint("loja")', "O texto loja foi passado para o gancho."),
           MC("Quando você chama breakpoint(), o Python na verdade chama…", "sys.breakpointhook()", ["pdb.quit()", "print()", "sys.exit()"], "breakpoint só repassa a chamada para o gancho."),
           MC("Onde fica guardado o gancho original do Python?", "sys.__breakpointhook__", ["sys.original", "pdb.hook", "Em lugar nenhum"], "Útil para voltar ao normal depois."),
           FILL("Complete para trocar o gancho.", 'import sys\n___ = lambda: print("pausa")\nbreakpoint()', "sys.breakpointhook", ["breakpoint", "sys.pause", "pdb.hook"], "O gancho mora no módulo sys.")]),
        # lição 3
        L("Pausas no lugar certo",
          "Na prática, você põe breakpoint() bem onde suspeita do problema, muitas vezes dentro de um if, para pausar só no caso estranho. E a variável de ambiente PYTHONBREAKPOINT=0 desliga todos os breakpoint() de uma vez.",
          'import sys\nsys.breakpointhook = lambda: print("  (pausa: algo estranho aqui!)")\nprecos = [10, 25, -3, 8]\nfor p in precos:\n    print("preço", p)\n    if p < 0:\n        breakpoint()',
          [OUT('import sys\nsys.breakpointhook = lambda: print("pausa")\nfor i in range(3):\n    if i == 1:\n        breakpoint()\n    print(i)', ["0\n1\n2", "pausa\n0\n1\n2", "0\npausa"], "A pausa acontece só quando i é 1, antes de mostrar o 1."),
           TYPE('import sys\ncont = []\nsys.breakpointhook = lambda: cont.append(1)\nfor n in [4, 0, 7, 0]:\n    if n == 0:\n        breakpoint()\nprint(len(cont))', "Pausou duas vezes, nos dois zeros."),
           MC("Qual variável de ambiente desliga todos os breakpoint() do programa?", "PYTHONBREAKPOINT=0", ["PYTHONDEBUG=off", "BREAK=False", "PDB=0"], "Com ela, breakpoint() não faz nada."),
           MC("Por que pôr breakpoint() dentro de um if?", "Para pausar só quando a situação suspeita acontece", ["Porque fora do if dá erro", "Para o programa ficar mais rápido", "Para apagar a variável"], "Num laço grande, pausar em toda volta seria cansativo.")]),
        # lição 4
        L("Cuidados com breakpoint",
          "Sem parênteses, breakpoint não é chamado. Ao trocar o gancho, passe a função SEM parênteses: com parênteses, você guarda o resultado dela (None). E nunca esqueça um breakpoint() no programa entregue: ele vai parar esperando comandos.",
          'import sys\ndef avisar():\n    print("pausa!")\nsys.breakpointhook = avisar\nbreakpoint\nbreakpoint()\nprint("fim")',
          [OUT('import sys\nsys.breakpointhook = lambda: print("pausa")\nbreakpoint\nprint("fim")', ["pausa\nfim", "Erro", "pausa"], "Sem parênteses, breakpoint não foi chamado."),
           OUT('import sys\ndef g():\n    print("pausa")\ntry:\n    sys.breakpointhook = g()\n    breakpoint()\nexcept TypeError:\n    print("o gancho virou None")', ["pausa", "o gancho virou None", "pausa\npausa"], "g() rodou na hora (pausa) e devolveu None; chamar None dá TypeError."),
           MC("Você esqueceu um breakpoint() no programa entregue. O que acontece quando ele roda?", "O programa para e fica esperando comandos do depurador", ["Nada, o Python ignora", "O programa apaga a linha", "Aparece um aviso e segue"], "Sempre apague os breakpoint() antes de entregar."),
           MC("No pdb, qual comando mostra o valor de uma variável x?", "p x", ["show x", "x?", "get x"], "p de print. Também existem n (próxima linha), c (continuar) e q (sair).")]),
        # lição 5
        L("Mostrando variáveis na pausa",
          "Um gancho com **kw recebe argumentos com nome. Assim você chama breakpoint(vida=vida) e o gancho mostra cada variável que quiser espiar.",
          'import sys\ndef espiar(**variaveis):\n    for nome, valor in variaveis.items():\n        print(f"  {nome} = {valor}")\nsys.breakpointhook = espiar\nvida = 100\nfor dano in [30, 50]:\n    vida -= dano\n    breakpoint(vida=vida, dano=dano)',
          [OUT('import sys\nsys.breakpointhook = lambda **kw: print(sorted(kw))\nbreakpoint(b=1, a=2)', ["['b', 'a']", "[1, 2]", "{'b': 1, 'a': 2}"], "sorted de um dicionário ordena as chaves."),
           TYPE('import sys\nsys.breakpointhook = lambda **kw: print(sum(kw.values()))\nbreakpoint(x=3, y=4)', "3 + 4."),
           ORDER("Monte o programa que troca o gancho e depois pausa.", ['import sys', 'sys.breakpointhook = lambda: print("pausa")', 'breakpoint()'], "Primeiro importa sys, depois troca o gancho, por fim pausa."),
           CODE("Crie a função espiar(**kw) que mostra cada variável recebida no formato nome=valor (uma por linha), use-a como gancho e chame breakpoint(ouro=ouro).",
                'import sys\nouro = 50\n# crie o gancho, troque e chame breakpoint\n',
                'import sys\nouro = 50\ndef espiar(**kw):\n    for k, v in kw.items():\n        print(f"{k}={v}")\nsys.breakpointhook = espiar\nbreakpoint(ouro=ouro)',
                'assert "ouro=50" in __stdout__, "A saída deve ter ouro=50"',
                "Defina espiar, faça sys.breakpointhook = espiar e chame breakpoint(ouro=ouro).")]),
        # lição 6
        L("Desafio: depurador caseiro",
          "Um gancho pode guardar as pausas numa lista em vez de parar. No fim, você confere quantas vezes o caso estranho apareceu. Para voltar ao normal: sys.breakpointhook = sys.__breakpointhook__.",
          'import sys\npausas = []\nsys.breakpointhook = lambda **kw: pausas.append(kw)\nnotas = [7, 11, 9, 15]\nfor i, n in enumerate(notas):\n    if n > 10:\n        breakpoint(posicao=i, nota=n)\nprint("pausas:", len(pausas))\nprint(pausas[0])',
          [OUT('import sys\nlog = []\nsys.breakpointhook = lambda n: log.append(n)\nfor n in [3, 8, 1, 9]:\n    if n > 5:\n        breakpoint(n)\nprint(log)', ["[3, 8, 1, 9]", "[8]", "2"], "Só 8 e 9 passam do if e vão para a lista."),
           TYPE('import sys\nsys.breakpointhook = lambda: print("original?", sys.breakpointhook is sys.__breakpointhook__)\nbreakpoint()', "O gancho atual é o nosso, não o original."),
           MC("Depois de testar com o seu gancho, como voltar ao depurador normal?", "sys.breakpointhook = sys.__breakpointhook__", ["del breakpoint", "sys.breakpointhook = None", "breakpoint(0)"], "O original fica guardado em sys.__breakpointhook__."),
           CODE("Troque o gancho por uma função que guarda cada valor recebido na lista suspeitos. Percorra saldos chamando breakpoint(s) para cada saldo negativo. No fim, mostre suspeitos.",
                'import sys\nsaldos = [50, -10, 30, -5]\nsuspeitos = []\n# troque o gancho e percorra os saldos\nprint(suspeitos)\n',
                'import sys\nsaldos = [50, -10, 30, -5]\nsuspeitos = []\nsys.breakpointhook = lambda v: suspeitos.append(v)\nfor s in saldos:\n    if s < 0:\n        breakpoint(s)\nprint(suspeitos)',
                'assert __stdout__.strip() == "[-10, -5]", "A saída deve ser [-10, -5]"',
                "sys.breakpointhook = lambda v: suspeitos.append(v), e breakpoint(s) dentro do if s < 0.")]),
    ],

    # ================================================================ open
    "open": [
        # lição 2
        L("Lendo de vários jeitos",
          "read() lê o arquivo todo num texto. readline() lê UMA linha por vez. readlines() devolve a lista de linhas, cada uma com o \\n no fim. E um for direto no arquivo percorre as linhas.",
          'with open("lista.txt", "w", encoding="utf-8") as f:\n    f.write("arroz\\nfeijão\\nbatata\\n")\nwith open("lista.txt", encoding="utf-8") as f:\n    print(f.readline().strip())\n    print(f.readlines())',
          [OUT('with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("um\\ndois\\n")\nwith open("a.txt", encoding="utf-8") as f:\n    print(f.readlines())', ["['um', 'dois']", "um\ndois", "['um\\ndois\\n']"], "readlines devolve uma lista, e cada linha mantém o \\n."),
           TYPE('with open("b.txt", "w", encoding="utf-8") as f:\n    f.write("gato\\ncão\\n")\nwith open("b.txt", encoding="utf-8") as f:\n    f.readline()\n    print(f.readline().strip())', "O primeiro readline leu gato; o segundo lê a próxima linha."),
           OUT('with open("c.txt", "w", encoding="utf-8") as f:\n    f.write("a\\nb\\nc\\n")\nn = 0\nwith open("c.txt", encoding="utf-8") as f:\n    for linha in f:\n        n += 1\nprint(n)', ["1", "6", "0"], "O for passa por cada linha: 3 linhas."),
           MC("Qual método lê só UMA linha por vez?", "readline()", ["read()", "readlines()", "line()"], "readlines (com s) lê todas.")]),
        # lição 3
        L("Salvando dados do dia a dia",
          "Para gravar uma lista, escreva cada item com \"\\n\" no fim. writelines NÃO põe quebras de linha sozinho. Outro jeito prático: print(..., file=f) escreve no arquivo como se fosse na tela.",
          'compras = ["leite", "pão", "café"]\nwith open("compras.txt", "w", encoding="utf-8") as f:\n    for item in compras:\n        f.write(item + "\\n")\nwith open("compras.txt", "a", encoding="utf-8") as f:\n    print("ovos", file=f)\nwith open("compras.txt", encoding="utf-8") as f:\n    print(f.read().splitlines())',
          [OUT('with open("n.txt", "w", encoding="utf-8") as f:\n    f.writelines(["a", "b", "c"])\nwith open("n.txt", encoding="utf-8") as f:\n    print(f.read())', ["a\nb\nc", "['a', 'b', 'c']", "a b c"], "writelines junta tudo, sem quebras de linha."),
           TYPE('with open("p.txt", "w", encoding="utf-8") as f:\n    print("vida", 3, sep=":", file=f)\nwith open("p.txt", encoding="utf-8") as f:\n    print(f.read().strip())', "print com file=f gravou vida:3 no arquivo."),
           MC("Para acrescentar uma linha a um registro sem apagar o que já existe, use o modo…", '"a"', ['"w"', '"r"', '"x"'], '"a" escreve no fim; "w" apaga tudo antes.'),
           CODE('Crie salvar_lista(nome_arquivo, itens) que grava cada item numa linha do arquivo (use encoding="utf-8").',
                "def salvar_lista(nome_arquivo, itens):\n    pass\n",
                'def salvar_lista(nome_arquivo, itens):\n    with open(nome_arquivo, "w", encoding="utf-8") as f:\n        for item in itens:\n            f.write(item + "\\n")',
                'salvar_lista("t.txt", ["maçã", "uva"])\nwith open("t.txt", encoding="utf-8") as f:\n    assert f.read().splitlines() == ["maçã", "uva"], "O arquivo deve ter maçã e uva, uma por linha"',
                'Abra com "w" e faça f.write(item + "\\n") para cada item.')]),
        # lição 4
        L("Cuidados com arquivos",
          "Ler um arquivo que não existe dá FileNotFoundError. write só aceita texto: converta números com str. O modo \"x\" cria um arquivo novo, mas dá FileExistsError se ele já existir. Depois do with, o arquivo está fechado.",
          'try:\n    with open("nao_existe.txt", encoding="utf-8") as f:\n        print(f.read())\nexcept FileNotFoundError:\n    print("arquivo não encontrado")\nwith open("nota.txt", "w", encoding="utf-8") as f:\n    f.write(str(10))',
          [OUT('with open("v.txt", "w", encoding="utf-8") as f:\n    try:\n        f.write(42)\n    except TypeError:\n        print("só aceita texto")', ["42", "Erro", "None"], "write(42) dá TypeError; o certo é write(str(42))."),
           OUT('with open("x.txt", "w", encoding="utf-8") as f:\n    f.write("velho")\ntry:\n    open("x.txt", "x", encoding="utf-8")\nexcept FileExistsError:\n    print("já existe")', ["velho", "Nada aparece", "Erro"], "O modo x se recusa a mexer num arquivo que já existe."),
           OUT('with open("d.txt", "w", encoding="utf-8") as f:\n    f.write("oi")\ntry:\n    f.read()\nexcept ValueError:\n    print("arquivo fechado")', ["oi", "Nada aparece", "None"], "Fora do with, o arquivo já foi fechado: ValueError."),
           MC('Por que usar encoding="utf-8"?', "Para acentos como ç e ã serem gravados e lidos certo em qualquer computador", ["Para o arquivo ficar menor", "Para o arquivo abrir mais rápido", 'É obrigatório só no modo "w"'], "Sem ele, cada computador pode usar uma codificação diferente.")]),
        # lição 5
        L("Combinando com outras funções",
          "Arquivo de texto combina com split, int, sum e enumerate. E o módulo json grava e lê dicionários e listas inteiros com json.dump e json.load.",
          'with open("notas.txt", "w", encoding="utf-8") as f:\n    f.write("Ana;8\\nCaio;6\\nBia;10\\n")\ntotal = 0\nwith open("notas.txt", encoding="utf-8") as f:\n    for linha in f:\n        nome, nota = linha.strip().split(";")\n        total += int(nota)\nprint("Média:", total / 3)',
          [TYPE('with open("q.txt", "w", encoding="utf-8") as f:\n    f.write("3\\n4\\n5\\n")\nwith open("q.txt", encoding="utf-8") as f:\n    print(sum(int(l) for l in f))', "int ignora o \\n do fim: 3 + 4 + 5."),
           OUT('import json\nwith open("d.json", "w", encoding="utf-8") as f:\n    json.dump({"vidas": 3}, f)\nwith open("d.json", encoding="utf-8") as f:\n    dados = json.load(f)\nprint(dados["vidas"] + 1)', ["31", "Erro", "vidas1"], "json.load devolve o dicionário com o número 3."),
           OUT('with open("e.txt", "w", encoding="utf-8") as f:\n    f.write("sol\\nlua\\n")\nwith open("e.txt", encoding="utf-8") as f:\n    for i, linha in enumerate(f, 1):\n        print(i, linha.strip())', ["0 sol\n1 lua", "1 sol\n\n2 lua", "sol\nlua"], "enumerate começa em 1 e strip tira o \\n."),
           CODE('Crie maior_nota(arquivo) que lê um arquivo com linhas no formato nome;nota e devolve o nome de quem tirou a maior nota.',
                "def maior_nota(arquivo):\n    return \"\"\n",
                'def maior_nota(arquivo):\n    melhor, maior = "", -1\n    with open(arquivo, encoding="utf-8") as f:\n        for linha in f:\n            nome, nota = linha.strip().split(";")\n            if int(nota) > maior:\n                melhor, maior = nome, int(nota)\n    return melhor',
                'with open("t.txt", "w", encoding="utf-8") as f:\n    f.write("Ana;7\\nTeo;9\\nBia;8\\n")\nassert maior_nota("t.txt") == "Teo", "Teo tirou 9, a maior nota"',
                "Percorra as linhas, separe com split(\";\") e guarde quem tem a maior nota.")]),
        # lição 6
        L("Desafio: diário de treinos",
          "Juntando tudo: uma função grava cada treino no modo \"a\" (sem apagar os anteriores) e depois o programa lê o arquivo e faz as contas. Cada execução começa numa pasta vazia.",
          'def registrar(km):\n    with open("treinos.txt", "a", encoding="utf-8") as f:\n        f.write(f"{km}\\n")\n\nfor km in [3, 5, 4]:\n    registrar(km)\nwith open("treinos.txt", encoding="utf-8") as f:\n    kms = [int(l) for l in f]\nprint("Treinos:", len(kms), "| Total:", sum(kms), "km")',
          [OUT('for p in ["a", "b"]:\n    with open("log.txt", "a", encoding="utf-8") as f:\n        f.write(p)\nwith open("log.txt", encoding="utf-8") as f:\n    print(f.read())', ["b", "a", "ba"], "O modo a acrescentou b depois de a."),
           TYPE('for p in ["a", "b"]:\n    with open("log.txt", "w", encoding="utf-8") as f:\n        f.write(p)\nwith open("log.txt", encoding="utf-8") as f:\n    print(f.read())', "O modo w apagou o a antes de gravar o b."),
           ORDER("Monte o programa que grava o placar e depois mostra o que foi gravado.", ['with open("placar.txt", "w", encoding="utf-8") as f:', '    f.write("10")', 'with open("placar.txt", encoding="utf-8") as f:', '    print(f.read())'], "Primeiro grava, depois lê."),
           CODE("Crie contar_palavras(arquivo) que devolve quantas palavras o arquivo tem.",
                "def contar_palavras(arquivo):\n    return 0\n",
                'def contar_palavras(arquivo):\n    with open(arquivo, encoding="utf-8") as f:\n        return len(f.read().split())',
                'with open("t.txt", "w", encoding="utf-8") as f:\n    f.write("o gato subiu\\nno telhado\\n")\nassert contar_palavras("t.txt") == 5, "O texto tem 5 palavras"',
                "len(f.read().split()): split sem argumento separa por espaços e quebras de linha.")]),
    ],
}

BUGS = r'''
@fn_eval 1
eval("pontos = 10")
print(pontos)
>>> exec("pontos = 10")
!! eval só calcula expressões. Para atribuir uma variável, use exec.

@fn_eval 1
resultado = eval(3 + 4 * 2)
print(resultado)
>>> resultado = eval("3 + 4 * 2")
!! eval recebe um texto. Ponha a conta entre aspas.

@fn_eval 3
preco = 5
qtd = 3
total = eval("preco * qtd", {"preco": preco})
print(total)
>>> total = eval("preco * qtd", {"preco": preco, "qtd": qtd})
!! Com dicionário, a expressão só enxerga o que está nele. Faltou qtd.

@fn_eval 2
dia = "08"
numero = eval(dia)
print(numero + 1)
>>> numero = int(dia)
!! eval("08") dá SyntaxError: zero à esquerda não vale em Python. Para converter texto em número, use int.

@fn_eval 4
contas = ["1 + 1", "2 * 3"]
total = 0
for c in contas:
    total += eval("c")
print(total)
>>> total += eval(c)
!! eval("c") calcula a variável c, que é um texto. Passe a própria variável: eval(c).

@fn_eval 3
import ast
texto = "[3, 1, 2]"
numeros = list(texto)
print(max(numeros))  # esperado: 3
>>> numeros = ast.literal_eval(texto)
!! list() separa o texto em caracteres. Para ler a lista escrita no texto, use ast.literal_eval (mais seguro que eval).

@fn_exec 1
resultado = exec("3 * 4")
print(resultado)  # esperado: 12
>>> resultado = eval("3 * 4")
!! exec roda comandos e sempre devolve None. Para pegar o valor de uma conta, use eval.

@fn_exec 1
codigo = "for i in range(2):\nprint(i)"
exec(codigo)
>>> codigo = "for i in range(2):\n    print(i)"
!! O código dentro do texto também precisa de recuo depois do for.

@fn_exec 3
ns = {}
exec("total = 10", ns)
print(ns[total])
>>> print(ns["total"])
!! A chave do dicionário é o nome em texto: "total", com aspas.

@fn_exec 3
ns = {}
exec("bonus = 50", ns)
print(bonus)
>>> print(ns["bonus"])
!! Com um dicionário, a variável fica dentro dele, não solta no programa.

@fn_exec 2
ns = {}
exec("x = 2 ** 3", "ns")
print(ns["x"])
>>> exec("x = 2 ** 3", ns)
!! O segundo argumento é o dicionário, não o nome dele em texto.

@fn_exec 3
ns = {"total": 0}
for n in [10, 20]:
    exec("total += {n}", ns)
print(ns["total"])  # esperado: 30
>>> exec(f"total += {n}", ns)
!! Faltou o f: sem ele, {n} não vira o número e o código fica errado.

@fn_compile 1
codigo = compile("vidas = 3", "<jogo>", "eval")
exec(codigo)
print(vidas)
>>> codigo = compile("vidas = 3", "<jogo>", "exec")
!! Atribuição é comando. O modo "eval" só aceita expressões; use "exec".

@fn_compile 1
c = compile("2 + 2", "eval")
print(eval(c))
>>> c = compile("2 + 2", "<conta>", "eval")
!! compile pede três coisas: o código, um nome (como "<conta>") e o modo.

@fn_compile 2
c = compile("print('Olá!')", "<t>", "exec")
c  # esperado: Olá!
>>> exec(c)  # esperado: Olá!
!! compile só prepara o código. Para rodar, use exec(c).

@fn_compile 1
c = compile("x = 5\nprint(x * 2)", "<t>", "exe")
exec(c)
>>> c = compile("x = 5\nprint(x * 2)", "<t>", "exec")
!! Os modos são "exec", "eval" e "single". "exe" não existe.

@fn_compile 1
c = compile("7 * 6", "<t>", "exec")
print(eval(c))  # esperado: 42
>>> c = compile("7 * 6", "<t>", "eval")
!! No modo "exec", o valor da expressão se perde e eval devolve None. Use o modo "eval".

@fn_compile 3
formula = compile("base * altura", "<area>", "eval")
for b in [2, 3]:
    print(eval(formula, {"base": b}))
>>> print(eval(formula, {"base": b, "altura": 10}))
!! A fórmula usa base e altura, mas o dicionário só tem base.

@fn_globals 2
moedas = 10
print(globals["moedas"])
>>> print(globals()["moedas"])
!! globals é uma função: chame com () para receber o dicionário.

@fn_globals 2
moedas = 10
print(globals()[moedas])
>>> print(globals()["moedas"])
!! As chaves de globals() são os nomes em texto. Sem aspas, você passou o valor 10.

@fn_globals 3
pontos = 0
def marcar():
    pontos += 1
marcar()
print(pontos)
>>> globals()["pontos"] += 1
!! Sem global, pontos vira local e ainda não tem valor. Mude pelo dicionário de globais (ou use global pontos).

@fn_globals 2
nivel = 4
print(globals()["Nivel"] * 10)
>>> print(globals()["nivel"] * 10)
!! Maiúscula importa: a variável se chama nivel, com n minúsculo.

@fn_globals 4
def saudar():
    return "Oi!"
nome = "saudar"
resposta = globals()[nome]
print(resposta.upper())
>>> resposta = globals()[nome]()
!! globals()[nome] devolve a função. Faltou chamar com () para receber o texto.

@fn_globals 3
def compra():
    total = 30
    return globals()["total"]
print(compra())
>>> return total
!! total é local da função; globals() só vê as variáveis do arquivo.

@fn_locals 3
def dobro(a):
    b = a * 2
    return locals["b"]
print(dobro(3))
>>> return locals()["b"]
!! locals é uma função: chame com () para receber o dicionário.

@fn_locals 3
taxa = 5
def preco(valor):
    return valor + locals()["taxa"]
print(preco(10))
>>> return valor + globals()["taxa"]
!! taxa é global; locals() da função só tem valor.

@fn_locals 3
def ajustar():
    vida = 10
    locals()["vida"] = 50
    return vida
print(ajustar())  # esperado: 50
>>> vida = 50
!! Mudar o dicionário de locals() não muda a variável. Atribua direto.

@fn_locals 2
def apresentar(nome, idade):
    return "{nome} tem {idade} anos".format(locals())
print(apresentar("Ana", 9))
>>> return "{nome} tem {idade} anos".format(**locals())
!! Faltaram os ** para abrir o dicionário em argumentos com nome.

@fn_locals 3
def resumo(a, b):
    d = dict(locals())
    return ", ".join(f"{k}={locals()[k]}" for k in d)
print(resumo(1, 2))  # esperado: a=1, b=2
>>> return ", ".join(f"{k}={d[k]}" for k in d)
!! Dentro do gerador, locals() é outro (só tem k). Use a cópia d.

@fn_locals 3
def soma(x, y):
    z = x + y
    return sorted(locals)
print(soma(1, 2))
>>> return sorted(locals())
!! Sem parênteses, locals é só a função, e não dá para ordenar uma função.

@fn___import__ 1
__import__("math")
print(math.sqrt(9))
>>> math = __import__("math")
!! __import__ não cria a variável sozinho. Guarde o módulo que ele devolve.

@fn___import__ 1
m = __import__(json)
print(m.dumps([1]))
>>> m = __import__("json")
!! O nome do módulo vai em texto, entre aspas.

@fn___import__ 1
abc = __import__("collections.abc")
print(isinstance([1, 2], abc.Sized))
>>> abc = __import__("collections.abc", fromlist=["Sized"])
!! Sem fromlist, __import__ devolve o pacote de cima (collections), que não tem Sized.

@fn___import__ 1
m = __import__("Math")
print(m.pi > 3)
>>> m = __import__("math")
!! Nomes de módulos diferenciam maiúsculas: é math, tudo minúsculo.

@fn___import__ 3
m = __import__("math")
funcao = "floor"
print(m[funcao](3.7))
>>> print(getattr(m, funcao)(3.7))
!! Módulo não é dicionário. Para pegar algo pelo nome em texto, use getattr.

@fn___import__ 1
m = __import__("string.py")
print(m.digits)
>>> m = __import__("string")
!! Importe pelo nome do módulo, sem o .py.

@fn_breakpoint 4
import sys
def pausa():
    print("pausa")
sys.breakpointhook = pausa()
breakpoint()
>>> sys.breakpointhook = pausa
!! Com (), a função roda na hora e o gancho vira None. Passe a função sem parênteses.

@fn_breakpoint 1
import pdb
sys.breakpointhook = lambda: print("pausa")
breakpoint()
print("fim")
>>> import sys
!! breakpointhook mora no módulo sys, não no pdb.

@fn_breakpoint 3
import sys
sys.breakpointhook = lambda: print("pausa")
breakpoint
print("fim")  # esperado: fim
>>> breakpoint()
!! Sem parênteses, breakpoint não é chamado e não há pausa.

@fn_breakpoint 2
import sys
sys.breakpointhook = lambda: print("pausa")
x = 7
breakpoint(x)
>>> sys.breakpointhook = lambda v: print("pausa com", v)
!! breakpoint(x) passa x para o gancho, mas o gancho não aceita nenhum argumento.

@fn_breakpoint 4
import sys
sys.breakpointhook = lambda **kw: print(kw)
vida = 10
breakpoint(vida)
>>> breakpoint(vida=vida)
!! O gancho só aceita argumentos com nome (**kw). Passe vida=vida.

@fn_breakpoint 2
import sys
sys.breakpointhook = lambda: "pausa"
breakpoint()
print("fim")  # esperado: fim
>>> sys.breakpointhook = lambda: print("pausa")
!! O que o gancho devolve é ignorado. Para a pausa aparecer, use print.

@fn_open 3
with open("nomes.txt", "w", encoding="utf-8") as f:
    f.write("Ana\nCaio\n")
with open("nomes.txt", "w", encoding="utf-8") as f:
    print(f.read())
>>> with open("nomes.txt", encoding="utf-8") as f:
!! O modo "w" é só para escrever (e apaga o conteúdo). Para ler, use "r", o padrão.

@fn_open 3
pontos = 80
with open("placar.txt", "w", encoding="utf-8") as f:
    f.write(pontos)
>>> f.write(str(pontos))
!! write só aceita texto. Converta o número com str.

@fn_open 2
for item in ["pão", "leite"]:
    with open("compras.txt", "w", encoding="utf-8") as f:
        f.write(item + "\n")
with open("compras.txt", encoding="utf-8") as f:
    print(f.read().split())  # esperado: ['pão', 'leite']
>>> with open("compras.txt", "a", encoding="utf-8") as f:
!! O modo "w" apaga o arquivo a cada volta. Para acrescentar, use "a".

@fn_open 2
with open("cores.txt", "w", encoding="utf-8") as f:
    f.writelines(["azul", "verde"])
with open("cores.txt", encoding="utf-8") as f:
    print(len(f.readlines()))  # esperado: 2
>>> f.writelines(["azul\n", "verde\n"])
!! writelines não põe quebra de linha sozinho: as cores ficaram grudadas numa linha só.

@fn_open 5
with open("frase.txt", "w", encoding="utf-8") as f:
    f.write("Bom dia")
with open("frase.txt", encoding="utf-8") as f:
    print("Lendo...")
print(f.read())
>>>     print(f.read())
!! Depois do with o arquivo é fechado. Leia dentro do bloco, com recuo.

@fn_open 3
with open("notas.txt", "w", encoding="utf-8") as f:
    f.write("10")
with open("nota.txt", encoding="utf-8") as f:
    print(f.read())
>>> with open("notas.txt", encoding="utf-8") as f:
!! O arquivo gravado se chama notas.txt, com s. nota.txt não existe.
'''
