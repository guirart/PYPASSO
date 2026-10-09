from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ all
    "all": [
        # lição 2
        L("Condições dentro do all",
          "O jeito mais comum é escrever uma condição para cada item: all(condição for x in coleção). O all para no primeiro False que encontrar, sem olhar o resto.",
          'idades = [18, 25, 31]\nprint(all(i >= 18 for i in idades))\nprint(all(i >= 21 for i in idades))',
          [OUT('print(all(n % 2 == 0 for n in [2, 4, 7]))', ["True", "[True, True, False]", "7"], "7 é ímpar, então nem todos são pares."),
           TYPE('palavras = ["sol", "mar", "céu"]\nprint(all(len(p) == 3 for p in palavras))', "Todas as palavras têm 3 letras."),
           MC("O all para de verificar quando…", "Encontra o primeiro item falso", ["Encontra o primeiro item verdadeiro", "Sempre vai até o fim", "Encontra um número negativo"], "Um único False já decide a resposta, então o resto nem é olhado."),
           FILL("Complete para conferir se todos os preços são positivos.", 'precos = [5, 12, 3]\nprint(all(p > 0 ___ p in precos))', "for", ["if", "in", "while"], "A estrutura é: condição for item in coleção.")]),
        # lição 3
        L("Validando dados",
          "O all é ótimo para validar: todos os campos foram preenchidos? Todos os caracteres são dígitos? Como texto vazio é falso, all(campos) já confere se nada ficou em branco.",
          'nome, email, cidade = "Ana", "ana@x.com", ""\nprint(all([nome, email, cidade]))\ncep = "12345678"\nprint(all(c.isdigit() for c in cep) and len(cep) == 8)',
          [OUT('notas = [7.5, 6.0, 9.0]\nif all(n >= 6 for n in notas):\n    print("Aprovado")\nelse:\n    print("Recuperação")', ["Recuperação", "True", "Aprovado\nRecuperação"], "Todas as notas são pelo menos 6."),
           TYPE('campos = ["Bia", "", "SP"]\nprint(all(campos))', "O texto vazio do meio é falso."),
           MC("Qual código confere se todos os itens do estoque têm quantidade maior que zero?", "all(q > 0 for q in estoque)", ["all(estoque > 0)", "all(estoque) > 0", "any(q > 0 for q in estoque)"], "A condição vai dentro do gerador, item por item."),
           CODE("Crie a função tudo_preenchido(campos) que devolve True só se nenhum texto da lista estiver vazio.",
                "def tudo_preenchido(campos):\n    pass\n",
                "def tudo_preenchido(campos):\n    return all(campos)\n",
                'assert tudo_preenchido(["a", "b"]) is True, "Com tudo preenchido deve dar True"\nassert tudo_preenchido(["a", ""]) is False, "Com um campo vazio deve dar False"',
                "return all(campos): o texto vazio é falso, então derruba o resultado.")]),
        # lição 4
        L("Cuidados com o all",
          "all(lista) testa se cada item é verdadeiro, não se é positivo: -3 é verdadeiro! Lembre também que a coleção vazia dá True e que all precisa de uma coleção: all(5) dá TypeError.",
          'print(all([-3, -1]))\nprint(all(n > 0 for n in [-3, -1]))\nprint(all([]))',
          [OUT('print(all([-1, -2, -3]))', ["False", "Erro", "-1"], "Qualquer número diferente de zero é verdadeiro, mesmo negativo."),
           OUT('print(all("abc"))', ["False", "Erro", "abc"], "Um texto é uma coleção de letras, e cada letra é um texto não vazio."),
           MC("O que all(10) faz?", "Dá TypeError: um int não é uma coleção", ["Devolve True", "Devolve False", "Devolve 10"], "all precisa de algo que dê para percorrer."),
           TYPE('print(all([[], [1]]))', "A lista vazia é falsa.")]),
        # lição 5
        L("all com zip e map",
          "Com zip, você compara vizinhos: all(a <= b for a, b in zip(l, l[1:])) confere se a lista está em ordem. Com map ou .values(), você testa outras coleções.",
          'l = [1, 3, 3, 8]\nprint(all(a <= b for a, b in zip(l, l[1:])))\nprint(all(map(str.isupper, ["SIM", "NAO"])))',
          [OUT('a = [1, 2, 3]\nb = [1, 2, 4]\nprint(all(x == y for x, y in zip(a, b)))', ["True", "[True, True, False]", "Erro"], "O último par é 3 e 4, que são diferentes."),
           TYPE('estoque = {"maçã": 3, "pera": 0}\nprint(all(estoque.values()))', "A pera tem 0, que é falso."),
           ORDER("Monte o programa que confere se a lista está em ordem crescente.", ['l = [2, 5, 9]', 'pares = zip(l, l[1:])', 'ok = all(a <= b for a, b in pares)', 'print(ok)'], "Primeiro a lista, depois os pares de vizinhos, depois o teste e o print."),
           FILL("Complete para conferir se todos os nomes começam com maiúscula.", 'nomes = ["Ana", "Bia"]\nprint(all(n[0].___() for n in nomes))', "isupper", ["upper", "islower", "title"], "isupper() responde True ou False; upper() devolveria um texto.")]),
        # lição 6
        L("Desafio: regras com all",
          "Juntando tudo: all com geradores, zip e and monta regras completas, como conferir uma senha ou se uma lista está em ordem.",
          'senha = "abc123"\nprint(len(senha) >= 6 and all(c.isalnum() for c in senha))',
          [OUT('print(all(x for x in [1, 2, 0, 4]))', ["True", "0", "[1, 2, 4]"], "O 0 é falso, então nem todos são verdadeiros."),
           MC("Qual a diferença entre all([]) e any([])?", "all([]) é True e any([]) é False", ["Os dois são True", "Os dois são False", "Os dois dão erro"], "Sem itens, não há nenhum falso (all) nem nenhum verdadeiro (any)."),
           TYPE('m = [[1, 2], [3, 4]]\nprint(all(all(linha) for linha in m))', "Nenhum zero em nenhuma linha da matriz."),
           CODE("Crie a função em_ordem(lista) que devolve True se cada número for menor ou igual ao seguinte.",
                "def em_ordem(lista):\n    pass\n",
                "def em_ordem(lista):\n    return all(a <= b for a, b in zip(lista, lista[1:]))\n",
                'assert em_ordem([1, 2, 2, 5]) is True, "[1, 2, 2, 5] está em ordem"\nassert em_ordem([3, 1]) is False, "[3, 1] não está em ordem"\nassert em_ordem([]) is True, "Uma lista vazia conta como em ordem"',
                "return all(a <= b for a, b in zip(lista, lista[1:]))")]),
    ],
    # ================================================================ any
    "any": [
        # lição 2
        L("Condições dentro do any",
          "Como no all, você escreve uma condição para cada item: any(condição for x in coleção). O any para no primeiro True que encontrar.",
          'precos = [12, 45, 8]\nprint(any(p > 40 for p in precos))\nprint(any(p > 100 for p in precos))',
          [OUT('print(any(n < 0 for n in [3, -2, 5]))', ["False", "-2", "[False, True, False]"], "O -2 é menor que zero."),
           TYPE('nomes = ["ana", "bia"]\nprint(any(n.startswith("c") for n in nomes))', "Nenhum nome começa com c."),
           MC("O any para de verificar quando…", "Encontra o primeiro item verdadeiro", ["Encontra o primeiro item falso", "Sempre vai até o fim", "Encontra um zero"], "Um único True já basta para a resposta."),
           FILL("Complete para saber se alguma fruta é uva.", 'frutas = ["maçã", "uva"]\nprint(any(f ___ "uva" for f in frutas))', "==", ["=", "!=", "+"], "== compara; um = sozinho é atribuição.")]),
        # lição 3
        L("Buscas rápidas",
          "O any responde \"existe pelo menos um?\". Serve para saber se a senha tem número, se a frase tem uma palavra proibida ou se algum produto acabou.",
          'senha = "gato123"\nprint(any(c.isdigit() for c in senha))\nproibidas = ["bobo", "chato"]\nfrase = "que jogo chato"\nprint(any(p in frase for p in proibidas))',
          [OUT('estoque = [5, 0, 12]\nif any(q == 0 for q in estoque):\n    print("Repor!")\nelse:\n    print("Tudo ok")', ["Tudo ok", "True", "0"], "Um dos produtos está com 0."),
           TYPE('print(any(c.isupper() for c in "pipoca"))', "Todas as letras são minúsculas."),
           MC("Qual código confere se a senha tem pelo menos uma letra maiúscula?", "any(c.isupper() for c in senha)", ["all(c.isupper() for c in senha)", "senha.isupper()", "any(senha.isupper())"], "senha.isupper() exige o texto todo em maiúsculas."),
           CODE("Crie a função tem_numero(texto) que devolve True se o texto tiver pelo menos um dígito.",
                "def tem_numero(texto):\n    pass\n",
                "def tem_numero(texto):\n    return any(c.isdigit() for c in texto)\n",
                'assert tem_numero("abc1") is True, "abc1 tem um dígito"\nassert tem_numero("abc") is False, "abc não tem dígitos"\nassert tem_numero("") is False, "Texto vazio não tem dígitos"',
                "return any(c.isdigit() for c in texto)")]),
        # lição 4
        L("Cuidados com o any",
          "any testa se algum item é verdadeiro, não se a lista tem itens: any([0, 0]) dá False. A coleção vazia também dá False. E o any devolve só True ou False, nunca o item encontrado.",
          'print(any([0, 0]))\nprint(any([]))\nprint(any(["", "oi"]))',
          [OUT('print(any([None, False, 0]))', ["True", "None", "Erro"], "None, False e 0 são todos falsos."),
           OUT('print(any(["", " "]))', ["False", " ", "Erro"], "Um espaço já é texto não vazio, então é verdadeiro."),
           MC("any([3, 7]) devolve…", "True", ["3", "7", "[3, 7]"], "any sempre devolve True ou False."),
           TYPE('print(any(x > 5 for x in []))', "Sem itens, não existe nenhum verdadeiro.")]),
        # lição 5
        L("any, all e not",
          "not any(...) quer dizer \"nenhum\". E os dois se completam: \"nenhum item é ruim\" é o mesmo que \"todos são bons\". Dá para usar com dicionários via .values().",
          'notas = [7, 8, 5]\nprint(not any(n < 6 for n in notas))\nprint(all(n >= 6 for n in notas))',
          [OUT('erros = []\nprint(not any(erros))', ["False", "[]", "Erro"], "any([]) é False, e o not inverte para True."),
           TYPE('turma = {"Ana": 9, "Caio": 4}\nprint(any(n < 5 for n in turma.values()))', "O Caio tirou 4."),
           MC("not any(x < 0 for x in l) é o mesmo que…", "all(x >= 0 for x in l)", ["any(x >= 0 for x in l)", "all(x < 0 for x in l)", "not all(x < 0 for x in l)"], "Nenhum negativo = todos maiores ou iguais a zero."),
           ORDER("Monte o programa que avisa se algum aluno tirou 10.", ['notas = {"Ana": 10, "Teo": 7}', 'if any(n == 10 for n in notas.values()):', '    print("Temos nota máxima!")'], "Primeiro o dicionário, depois o if com any e, recuado, o print.")]),
        # lição 6
        L("Desafio: senha forte",
          "Juntando tudo: vários any ligados com and checam regras diferentes, como \"tem letra\" e \"tem número\", ao mesmo tempo.",
          'senha = "pipo2026"\ntem_letra = any(c.isalpha() for c in senha)\ntem_num = any(c.isdigit() for c in senha)\nprint(len(senha) >= 8 and tem_letra and tem_num)',
          [OUT('l = [[], [0], []]\nprint(any(l))', ["False", "[0]", "0"], "[0] é uma lista com um item, então é verdadeira."),
           TYPE('print(any(c in "aeiou" for c in "rtm"))', "Nenhuma das letras é vogal."),
           MC("Para a lista [0, 0, 1], qual expressão dá True?", "any([0, 0, 1])", ["all([0, 0, 1])", "all([0, 0, 1]) and any([0, 0, 1])", "not any([0, 0, 1])"], "Só o any se contenta com um verdadeiro."),
           CODE("Crie a função senha_forte(s) que devolve True se a senha tiver 8 ou mais caracteres, alguma letra e algum número.",
                "def senha_forte(s):\n    pass\n",
                "def senha_forte(s):\n    tem_letra = any(c.isalpha() for c in s)\n    tem_num = any(c.isdigit() for c in s)\n    return len(s) >= 8 and tem_letra and tem_num\n",
                'assert senha_forte("pipo2026") is True, "pipo2026 é forte"\nassert senha_forte("pipo1") is False, "pipo1 é curta demais"\nassert senha_forte("12345678") is False, "12345678 não tem letra"\nassert senha_forte("abcdefgh") is False, "abcdefgh não tem número"',
                "Três condições ligadas com and: tamanho, any com isalpha e any com isdigit.")]),
    ],
    # ================================================================ callable
    "callable": [
        # lição 2
        L("Função ou resultado?",
          "Cuidado com os parênteses: f é a função (chamável), mas f() já é o resultado dela. len é chamável; len(\"oi\") é o número 2, que não é.",
          'def dobro(n):\n    return n * 2\n\nprint(callable(dobro))\nprint(callable(dobro(5)))',
          [OUT('print(callable(len("abc")))', ["True", "3", "Erro"], "len(\"abc\") já virou 3, um número."),
           TYPE('f = lambda x: x + 1\nprint(callable(f))', "Uma lambda é uma função."),
           MC("Qual destes é chamável?", "str.upper", ['"oi".upper()', "len([1])", "None"], "Sem parênteses, str.upper é o método; os outros já são resultados."),
           FILL("Complete para guardar a função na variável, sem chamá-la.", 'def oi():\n    return "olá"\n\nacao = ___\nprint(callable(acao))', "oi", ["oi()", '"oi"', '"olá"'], "Sem parênteses você guarda a própria função.")]),
        # lição 3
        L("Funções guardadas em variáveis",
          "Funções podem morar em listas e dicionários. O callable ajuda a decidir: se o valor for chamável, você chama; se não, usa como está.",
          'menu = {"oi": lambda: "Olá!", "versao": "1.0"}\nfor chave, valor in menu.items():\n    if callable(valor):\n        print(chave, "->", valor())\n    else:\n        print(chave, "->", valor)',
          [OUT('coisas = [print, 3, str, "x"]\nprint(sum(callable(c) for c in coisas))', ["4", "0", "True"], "print e str são chamáveis; cada True conta como 1."),
           TYPE('padrao = 10\nvalor = padrao() if callable(padrao) else padrao\nprint(valor)', "10 não é chamável, então é usado como está."),
           MC("Por que conferir callable(x) antes de fazer x()?", "Para evitar TypeError quando x não é chamável", ["Para o código ficar mais rápido", "Porque x() sempre dá erro", "Para transformar x em função"], "Chamar algo que não é função dá TypeError."),
           CODE("Crie a função resolver(valor): se valor for chamável, devolva valor(); senão, devolva o próprio valor.",
                "def resolver(valor):\n    pass\n",
                "def resolver(valor):\n    if callable(valor):\n        return valor()\n    return valor\n",
                'assert resolver(5) == 5, "resolver(5) deve devolver 5"\nassert resolver(lambda: 7) == 7, "resolver(lambda: 7) deve devolver 7"\nassert resolver(list) == [], "resolver(list) deve devolver []"',
                "if callable(valor): return valor(), senão return valor.")]),
        # lição 4
        L("Cuidados com callable",
          "A classe é chamável, mas um objeto comum criado por ela não é. E o resultado de uma função (texto, número, lista) não pode ser chamado: tentar dá TypeError.",
          'class Gato:\n    pass\n\nmimi = Gato()\nprint(callable(Gato))\nprint(callable(mimi))',
          [OUT('class Carro:\n    def buzinar(self):\n        return "bi"\n\nc = Carro()\nprint(callable(c), callable(c.buzinar))', ["True True", "False False", "True False"], "O objeto não é chamável; o método dele é."),
           MC('O que acontece em: nome = "Ana" e depois nome()?', "TypeError: texto não pode ser chamado", ["Mostra Ana", "Devolve None", "NameError"], "Os parênteses tentam chamar o texto como se fosse função."),
           TYPE('print(callable(None))', "None não é função."),
           OUT('lista = [1, 2]\ntry:\n    lista()\nexcept Exception as e:\n    print(type(e).__name__)', ["NameError", "ValueError", "[1, 2]"], "Chamar uma lista dá TypeError.")]),
        # lição 5
        L("Objetos que viram funções",
          "Uma classe pode ensinar seus objetos a serem chamados criando o método __call__. Aí callable(objeto) passa a dar True e objeto() funciona.",
          'class Contador:\n    def __init__(self):\n        self.total = 0\n    def __call__(self):\n        self.total += 1\n        return self.total\n\nc = Contador()\nc()\nprint(c())\nprint(callable(c))',
          [OUT('class Saudar:\n    def __call__(self, nome):\n        return "Oi, " + nome\n\ns = Saudar()\nprint(s("Bia"))', ["Erro", "Oi, ", "Saudar"], "s(\"Bia\") roda o __call__."),
           TYPE('class Caixa:\n    pass\n\nprint(callable(Caixa()))', "Caixa não tem __call__, então o objeto não é chamável."),
           MC("Qual método faz um objeto poder ser chamado com ()?", "__call__", ["__init__", "__str__", "__run__"], "__init__ cria o objeto; __call__ é o que roda ao chamá-lo."),
           FILL("Complete para que dobrar(4) funcione.", 'class Dobrador:\n    def ___(self, n):\n        return n * 2\n\ndobrar = Dobrador()\nprint(dobrar(4))', "__call__", ["__init__", "call", "__dobro__"], "O nome especial é __call__, com dois sublinhados de cada lado.")]),
        # lição 6
        L("Desafio: separar funções",
          "Juntando tudo: numa lista misturada, callable separa o que é função do que é dado. Isso aparece em menus, plugins e configurações.",
          'itens = [len, 42, str.upper, "oi"]\nfuncoes = [i for i in itens if callable(i)]\nprint(len(funcoes))',
          [OUT('print([callable(x) for x in (int, 0, abs)])', ["[False, False, True]", "[True, True, True]", "2"], "int é classe e abs é função; 0 é só um número."),
           TYPE('def f():\n    return g\n\ndef g():\n    return 1\n\nprint(callable(f()))', "f() devolve a função g, que é chamável."),
           MC("callable(type) é…", "True", ["False", "Erro"], "type é uma classe, e toda classe é chamável."),
           CODE("Crie a função contar_funcoes(lista) que devolve quantos itens da lista são chamáveis.",
                "def contar_funcoes(lista):\n    pass\n",
                "def contar_funcoes(lista):\n    return sum(1 for x in lista if callable(x))\n",
                'assert contar_funcoes([len, 1, str]) == 2, "[len, 1, str] tem 2 chamáveis"\nassert contar_funcoes([]) == 0, "Lista vazia tem 0"\nassert contar_funcoes(["a", 3]) == 0, "Texto e número não são chamáveis"',
                "return sum(1 for x in lista if callable(x))")]),
    ],
    # ================================================================ isinstance
    "isinstance": [
        # lição 2
        L("Com as suas classes",
          "isinstance também funciona com classes que você cria. Um objeto é instância da sua classe, das classes-mãe dela e de object.",
          'class Animal:\n    pass\n\nclass Cao(Animal):\n    pass\n\nrex = Cao()\nprint(isinstance(rex, Cao))\nprint(isinstance(rex, Animal))\nprint(isinstance(rex, object))',
          [OUT('class Animal: pass\nclass Gato(Animal): pass\na = Animal()\nprint(isinstance(a, Gato))', ["True", "Erro", "None"], "Todo gato é animal, mas nem todo animal é gato."),
           TYPE('print(isinstance("oi", object))', "Tudo em Python é object."),
           MC("O segundo argumento de isinstance pode ser…", "Um tipo ou uma tupla de tipos", ["Só um texto com o nome do tipo", "Qualquer valor", "Uma lista de valores"], "Por exemplo int ou (int, float)."),
           FILL("Complete para aceitar int ou float.", 'x = 2.5\nprint(isinstance(x, ___))', "(int, float)", ["int or float", '"int, float"', "[int, float]"], "Vários tipos vão numa tupla.")]),
        # lição 3
        L("Cada tipo do seu jeito",
          "Use isinstance para tratar cada tipo de um jeito: somar só os números de uma lista misturada, ou aceitar texto e número na mesma função.",
          'dados = [3, "oi", 4.5, "7", 2]\ntotal = 0\nfor d in dados:\n    if isinstance(d, (int, float)):\n        total += d\nprint(total)',
          [OUT('coisas = [1, "a", [2], "b"]\nprint(sum(isinstance(c, str) for c in coisas))', ["4", "True", "['a', 'b']"], "Só \"a\" e \"b\" são textos."),
           TYPE('def dobro(x):\n    if isinstance(x, str):\n        return x + x\n    return x * 2\n\nprint(dobro("ha"))', "Para texto, a função junta o texto com ele mesmo."),
           MC("Qual código pega só os textos de uma lista chamada itens?", "[i for i in itens if isinstance(i, str)]", ["[i for i in itens if type(i) == 'str']", "[i for i in itens if isinstance(i, 'str')]", "[str(i) for i in itens]"], "O tipo vai sem aspas: str."),
           CODE("Crie a função somar_numeros(lista) que soma só os itens int ou float, ignorando o resto.",
                "def somar_numeros(lista):\n    pass\n",
                "def somar_numeros(lista):\n    return sum(x for x in lista if isinstance(x, (int, float)))\n",
                'assert somar_numeros([1, "2", 3.5]) == 4.5, "[1, \\"2\\", 3.5] deve somar 4.5"\nassert somar_numeros(["a"]) == 0, "Sem números, a soma é 0"',
                "return sum(x for x in lista if isinstance(x, (int, float)))")]),
        # lição 4
        L("Pegadinhas do isinstance",
          "True e False contam como int, então podem entrar onde você esperava só números. O tipo vai sem aspas: isinstance(x, \"int\") dá TypeError. E isinstance(3, float) é False: inteiro não é float.",
          'print(isinstance(False, int))\nprint(isinstance(3, float))\nprint(isinstance(True, bool) and not isinstance(3, bool))',
          [OUT('print(isinstance(5, float))', ["True", "5.0", "Erro"], "5 é int, e int não é float."),
           OUT('try:\n    isinstance(3, "int")\nexcept Exception as e:\n    print(type(e).__name__)', ["NameError", "ValueError", "False"], "Um texto no lugar do tipo dá TypeError."),
           MC("Como aceitar números, mas recusar True e False?", "isinstance(x, (int, float)) and not isinstance(x, bool)", ["isinstance(x, int)", "isinstance(x, (int, bool))", "type(x) == bool"], "Como bool é int, você precisa excluí-lo de propósito."),
           TYPE('print(isinstance(None, object))', "Até None é um objeto.")]),
        # lição 5
        L("Examinando coleções",
          "Combine isinstance com all, any e filter para examinar uma coleção inteira: todos são números? Algum é texto?",
          'valores = [1, 2.5, 3]\nprint(all(isinstance(v, (int, float)) for v in valores))\nmisturada = [1, "dois", 3]\nprint(list(filter(lambda x: isinstance(x, str), misturada)))',
          [OUT('l = [1, 2, "3"]\nprint(all(isinstance(x, int) for x in l))', ["True", "[1, 2]", "Erro"], "\"3\" é texto, não int."),
           TYPE('d = {"a": 1, "b": [2], "c": 3}\nprint([k for k, v in d.items() if isinstance(v, list)])', "Só a chave b guarda uma lista."),
           ORDER("Monte o programa que conta quantos textos há na lista.", ['itens = ["a", 1, "b"]', 'textos = [i for i in itens if isinstance(i, str)]', 'print(len(textos))'], "Lista, depois o filtro com isinstance, depois o len."),
           MC("any(isinstance(x, float) for x in l) responde…", "Se existe pelo menos um float em l", ["Se todos são float", "Quantos floats existem", "Converte tudo para float"], "any pergunta \"existe algum?\".")]),
        # lição 6
        L("Desafio: nomeando tipos",
          "Juntando tudo: uma função pode descrever cada valor em português. Teste bool ANTES de int, porque True também passa como int.",
          'def tipo(x):\n    if isinstance(x, bool):\n        return "lógico"\n    if isinstance(x, int):\n        return "inteiro"\n    return "outro"\n\nprint(tipo(True), tipo(7), tipo("a"))',
          [OUT('def t(x):\n    if isinstance(x, int):\n        return "inteiro"\n    if isinstance(x, bool):\n        return "lógico"\n\nprint(t(False))', ["lógico", "None", "Erro"], "False é int, então o primeiro if já responde."),
           TYPE('print(isinstance([], (str, dict)))', "Uma lista não é texto nem dicionário."),
           MC("isinstance(x, (list, tuple)) é True para…", "[1] e (1,)", ["Só [1]", "Só (1,)", "[1], (1,) e {1}"], "{1} é um set, que não está na tupla."),
           CODE("Crie a função descrever(x) que devolve 'texto' para str, 'número' para int ou float (mas não bool) e 'outro' para o resto.",
                "def descrever(x):\n    pass\n",
                'def descrever(x):\n    if isinstance(x, bool):\n        return "outro"\n    if isinstance(x, str):\n        return "texto"\n    if isinstance(x, (int, float)):\n        return "número"\n    return "outro"\n',
                'assert descrever("a") == "texto", "descrever(\\"a\\") deve ser texto"\nassert descrever(3) == "número", "descrever(3) deve ser número"\nassert descrever(2.5) == "número", "descrever(2.5) deve ser número"\nassert descrever(True) == "outro", "descrever(True) deve ser outro"\nassert descrever([]) == "outro", "descrever([]) deve ser outro"',
                "Trate bool primeiro, depois str, depois (int, float).")]),
    ],
    # ================================================================ issubclass
    "issubclass": [
        # lição 2
        L("Tuplas de classes",
          "Como no isinstance, o segundo argumento pode ser uma tupla: issubclass(C, (A, B)) é True se C herdar de A ou de B.",
          'class Veiculo: pass\nclass Barco: pass\nclass Carro(Veiculo): pass\n\nprint(issubclass(Carro, (Barco, Veiculo)))\nprint(issubclass(Carro, (Barco, str)))',
          [OUT('print(issubclass(bool, (str, int)))', ["False", "Erro", "int"], "bool herda de int, que está na tupla."),
           TYPE('print(issubclass(float, int))', "float não herda de int."),
           MC("issubclass(X, X) dá…", "True", ["False", "Erro"], "Toda classe é subclasse de si mesma."),
           FILL("Complete para perguntar se Gato herda de Animal.", 'class Animal: pass\nclass Gato(Animal): pass\nprint(___(Gato, Animal))', "issubclass", ["isinstance", "hasattr", "type"], "Os dois argumentos são classes, então é issubclass.")]),
        # lição 3
        L("Famílias de classes",
          "issubclass ajuda a organizar famílias de classes: um jogo pode ter Inimigo, e dele saem Zumbi e Chefe. Você confere a família sem criar nenhum objeto.",
          'class Inimigo: pass\nclass Zumbi(Inimigo): pass\nclass Moeda: pass\n\nfor cls in [Zumbi, Moeda]:\n    print(cls.__name__, issubclass(cls, Inimigo))',
          [OUT('class A: pass\nclass B(A): pass\nclass C(A): pass\nprint(issubclass(B, C))', ["True", "Erro", "A"], "B e C são irmãs: nenhuma herda da outra."),
           TYPE('class Ave: pass\nclass Pinguim(Ave): pass\nprint(issubclass(Pinguim, object))', "Toda classe herda de object."),
           MC("Qual a diferença entre isinstance e issubclass?", "isinstance recebe um objeto; issubclass recebe uma classe", ["Nenhuma, são iguais", "issubclass recebe um objeto; isinstance recebe uma classe", "issubclass só funciona com int"], "O primeiro argumento muda: objeto ou classe."),
           CODE("Crie a função eh_inimigo(cls) que devolve True se a classe herdar de Inimigo.",
                "class Inimigo:\n    pass\n\nclass Zumbi(Inimigo):\n    pass\n\ndef eh_inimigo(cls):\n    pass\n",
                "class Inimigo:\n    pass\n\nclass Zumbi(Inimigo):\n    pass\n\ndef eh_inimigo(cls):\n    return issubclass(cls, Inimigo)\n",
                'assert eh_inimigo(Zumbi) is True, "Zumbi herda de Inimigo"\nassert eh_inimigo(int) is False, "int não é inimigo"\nassert eh_inimigo(Inimigo) is True, "Inimigo conta como subclasse de si mesma"',
                "return issubclass(cls, Inimigo)")]),
        # lição 4
        L("Cuidados com issubclass",
          "O primeiro argumento precisa ser uma classe: issubclass(5, int) dá TypeError. Se você tem um objeto, use type(obj) ou, melhor ainda, isinstance. E a ordem é (filha, mãe).",
          'x = 5\nprint(issubclass(type(x), int))\nprint(isinstance(x, int))',
          [OUT('try:\n    print(issubclass(3, int))\nexcept Exception as e:\n    print(type(e).__name__)', ["True", "False", "ValueError"], "3 é um objeto, não uma classe: TypeError."),
           TYPE('print(issubclass(type("oi"), str))', "type(\"oi\") é a classe str."),
           MC("A ordem dos argumentos em issubclass é…", "(filha, mãe)", ["(mãe, filha)", "Tanto faz", "(objeto, classe)"], "Pergunta: a primeira herda da segunda?"),
           OUT('class Mae: pass\nclass Filha(Mae): pass\nprint(issubclass(Mae, Filha))', ["True", "Erro", "Filha"], "A pergunta está ao contrário: a mãe não herda da filha.")]),
        # lição 5
        L("Filtrando classes",
          "Com uma lista de classes, você filtra só as de uma família usando issubclass numa compreensão, ou testa todas de uma vez com all. Até os erros do Python são classes em família.",
          'class Fruta: pass\nclass Maca(Fruta): pass\nclass Pedra: pass\n\nclasses = [Maca, Pedra, Fruta]\nprint([c.__name__ for c in classes if issubclass(c, Fruta)])',
          [OUT('print(all(issubclass(t, object) for t in [int, str, list]))', ["False", "[True, True, True]", "Erro"], "Todas herdam de object."),
           TYPE('print(issubclass(type(True), int))', "type(True) é bool, e bool herda de int."),
           ORDER("Monte o programa que mostra True porque Cao herda de Animal.", ['class Animal: pass', 'class Cao(Animal): pass', 'print(issubclass(Cao, Animal))'], "A mãe precisa existir antes da filha."),
           MC("issubclass(KeyError, Exception) dá…", "True", ["False", "TypeError"], "Os erros do Python são classes, e KeyError herda de Exception.")]),
        # lição 6
        L("Desafio: árvore de erros",
          "Juntando tudo: ZeroDivisionError herda de ArithmeticError, que herda de Exception. Com issubclass você explora essa árvore e filtra listas de classes.",
          'print(issubclass(ZeroDivisionError, ArithmeticError))\nprint(issubclass(ZeroDivisionError, Exception))\nprint(issubclass(ZeroDivisionError, KeyError))',
          [OUT('class A: pass\nclass B(A): pass\nclass C(B): pass\nprint(issubclass(A, C), issubclass(C, A))', ["True True", "True False", "False False"], "C é neta de A, mas A não herda de C."),
           TYPE('print(issubclass(IndexError, LookupError))', "IndexError faz parte da família LookupError."),
           MC("Toda classe que você cria herda de…", "object", ["type", "class", "Nada"], "Mesmo sem escrever, a mãe de todas é object."),
           CODE("Crie a função filtrar(classes, mae) que devolve uma lista com os nomes (__name__) das classes que herdam de mae.",
                "def filtrar(classes, mae):\n    pass\n",
                "def filtrar(classes, mae):\n    return [c.__name__ for c in classes if issubclass(c, mae)]\n",
                'assert filtrar([bool, str, int], int) == ["bool", "int"], "De [bool, str, int], herdam de int: bool e int"\nassert filtrar([], object) == [], "Lista vazia devolve []"',
                "return [c.__name__ for c in classes if issubclass(c, mae)]")]),
    ],
    # ================================================================ hasattr
    "hasattr": [
        # lição 2
        L("Atributos das suas classes",
          "hasattr enxerga os atributos que você cria em self e também os métodos da classe. O nome vai sempre como texto, e maiúsculas fazem diferença.",
          'class Pet:\n    def __init__(self, nome):\n        self.nome = nome\n    def falar(self):\n        return "..."\n\np = Pet("Rex")\nprint(hasattr(p, "nome"))\nprint(hasattr(p, "falar"))\nprint(hasattr(p, "idade"))',
          [OUT('class Jogo:\n    def __init__(self):\n        self.vidas = 3\n\nj = Jogo()\nprint(hasattr(j, "vidas"), hasattr(j, "pontos"))', ["True True", "False False", "3 None"], "vidas foi criado no __init__; pontos não."),
           TYPE('print(hasattr(3.5, "is_integer"))', "Números decimais têm o método is_integer."),
           MC("Com o atributo criado como self.nome, hasattr(p, \"Nome\") dá…", "False", ["True", "Erro"], "Maiúsculas e minúsculas fazem diferença."),
           FILL("Complete para perguntar se a lista tem o método sort.", 'l = [3, 1]\nprint(hasattr(l, ___))', '"sort"', ["sort", '"sort()"', "l.sort"], "O nome vai entre aspas e sem parênteses.")]),
        # lição 3
        L("Conferir antes de usar",
          "Antes de usar algo que talvez não exista, pergunte com hasattr. Assim você evita o AttributeError e escolhe outro caminho.",
          'class Pato:\n    def nadar(self):\n        return "nadando"\n\nclass Pedra:\n    pass\n\nfor coisa in [Pato(), Pedra()]:\n    if hasattr(coisa, "nadar"):\n        print(coisa.nadar())\n    else:\n        print("afunda")',
          [OUT('valor = "abc"\nif hasattr(valor, "upper"):\n    print(valor.upper())\nelse:\n    print(valor)', ["abc", "True", "Erro"], "Texto tem upper, então o if roda valor.upper()."),
           TYPE('x = 10\nprint(x.upper() if hasattr(x, "upper") else "sem upper")', "Números não têm upper."),
           MC("Que erro o hasattr ajuda a evitar?", "AttributeError", ["NameError", "ZeroDivisionError", "SyntaxError"], "AttributeError aparece quando o objeto não tem aquele atributo."),
           CODE("Crie a função falar(obj): se obj tiver o método som, devolva obj.som(); senão, devolva '...'.",
                'class Gato:\n    def som(self):\n        return "miau"\n\ndef falar(obj):\n    pass\n',
                'class Gato:\n    def som(self):\n        return "miau"\n\ndef falar(obj):\n    if hasattr(obj, "som"):\n        return obj.som()\n    return "..."\n',
                'assert falar(Gato()) == "miau", "falar(Gato()) deve devolver miau"\nassert falar(5) == "...", "falar(5) deve devolver ..."',
                'if hasattr(obj, "som"): return obj.som(), senão return "...".')]),
        # lição 4
        L("Cuidados com hasattr",
          "hasattr só pergunta se o nome existe: não chama nada, então o nome vai sem parênteses. Sem aspas, o Python procura uma variável e dá NameError. E chaves de dicionário não são atributos.",
          'print(hasattr("oi", "upper"))\nprint(hasattr("oi", "upper()"))\nprint(hasattr([], "len"))',
          [OUT('print(hasattr([1, 2], "len"))', ["True", "2", "Erro"], "len é uma função embutida, não um método da lista."),
           OUT('try:\n    hasattr("oi", upper)\nexcept Exception as e:\n    print(type(e).__name__)', ["TypeError", "AttributeError", "False"], "Sem aspas, upper vira uma variável que não existe."),
           MC('hasattr("abc", "upper()") dá…', "False", ["True", "ABC", "Erro"], "O nome do atributo não leva parênteses."),
           TYPE('d = {"cor": "azul"}\nprint(hasattr(d, "cor"))', "Chave de dicionário não é atributo; para isso use in.")]),
        # lição 5
        L("hasattr, getattr e callable",
          "hasattr combina com getattr, que pega o atributo pelo nome, e com callable, que diz se dá para chamar. Juntas, permitem usar nomes guardados em texto.",
          'texto = "pipo"\nnome = "upper"\nif hasattr(texto, nome):\n    metodo = getattr(texto, nome)\n    print(callable(metodo), metodo())',
          [OUT('print(getattr("abc", "upper")() if hasattr("abc", "upper") else "?")', ["abc", "?", "True"], "O texto tem upper, então getattr pega o método e () o chama."),
           TYPE('class C:\n    cor = "azul"\n\nprint(hasattr(C, "cor") and callable(C.cor))', "cor existe, mas é um texto, não uma função."),
           ORDER("Monte o programa que chama um método pelo nome guardado em texto.", ['nome = "title"', 'if hasattr("ana bia", nome):', '    print(getattr("ana bia", nome)())'], "Primeiro o nome, depois o if com hasattr e, recuado, o getattr."),
           MC("Qual expressão diz se obj tem um MÉTODO chamado salvar?", 'hasattr(obj, "salvar") and callable(getattr(obj, "salvar"))', ['hasattr(obj, "salvar")', 'callable("salvar")', 'hasattr(obj, salvar())'], "hasattr diz que existe; callable diz que dá para chamar.")]),
        # lição 6
        L("Desafio: tem tudo?",
          "Juntando tudo: para conferir se um objeto tem TODOS os atributos de uma lista, all com hasattr resolve em uma linha.",
          'class Produto:\n    def __init__(self):\n        self.nome = "café"\n        self.preco = 5\n\np = Produto()\nprint(all(hasattr(p, a) for a in ["nome", "preco"]))\nprint(all(hasattr(p, a) for a in ["nome", "estoque"]))',
          [OUT('print([hasattr("x", n) for n in ["upper", "append"]])', ["[True, True]", "[False, True]", "True"], "Texto tem upper, mas não append."),
           TYPE('print(sum(hasattr([], n) for n in ["append", "pop", "add"]))', "Listas têm append e pop, mas não add."),
           MC("hasattr(obj, \"x\") funciona como…", "Tentar obj.x e ver se dá AttributeError", ['Fazer "x" in obj', 'Fazer obj["x"]', "Chamar obj.x()"], "É exatamente o que o hasattr faz por dentro."),
           CODE("Crie a função tem_tudo(obj, nomes) que devolve True se obj tiver todos os atributos da lista nomes.",
                "def tem_tudo(obj, nomes):\n    pass\n",
                "def tem_tudo(obj, nomes):\n    return all(hasattr(obj, n) for n in nomes)\n",
                'assert tem_tudo("a", ["upper", "lower"]) is True, "Texto tem upper e lower"\nassert tem_tudo([], ["append", "upper"]) is False, "Lista não tem upper"\nassert tem_tudo(5, []) is True, "Sem nomes para conferir, deve dar True"',
                "return all(hasattr(obj, n) for n in nomes)")]),
    ],
}

BUGS = r'''
@fn_all 2
notas = [7, 8, 6]
print(all(n > 6 for n in notas))  # esperado: True
>>> print(all(n >= 6 for n in notas))  # esperado: True
!! Nota 6 também aprova. Use >= em vez de >.

@fn_all 2
numeros = [3, -1, 5]
print(all(numeros))  # esperado: False
>>> print(all(n > 0 for n in numeros))  # esperado: False
!! all(numeros) só vê se cada número é diferente de zero. Para "positivo", escreva a condição.

@fn_all 1
print(all(c.isdigit for c in "12a"))  # esperado: False
>>> print(all(c.isdigit() for c in "12a"))  # esperado: False
!! Faltaram os parênteses: c.isdigit sem () é o método, que é sempre verdadeiro.

@fn_all 2
l = [1, 4, 2]
print(all(a <= b for a, b in zip(l, l)))  # esperado: False
>>> print(all(a <= b for a, b in zip(l, l[1:])))  # esperado: False
!! Para comparar cada número com o próximo, junte l com l[1:].

@fn_all 2
estoque = {"maçã": 4, "pera": 0}
print(all(estoque))  # esperado: False
>>> print(all(estoque.values()))  # esperado: False
!! Percorrer o dicionário dá as chaves. Para testar as quantidades, use .values().

@fn_all 3
campos = ["Ana", "ana@x.com", "SP"]
ok = all(campos)
if ok == "True":
    print("Cadastro completo")  # esperado: Cadastro completo
else:
    print("Falta preencher")
>>> if ok:
!! all devolve o valor True, não o texto "True". Use só if ok:.

@fn_any 2
senha = "gato123"
print(all(c.isdigit() for c in senha))  # esperado: True
>>> print(any(c.isdigit() for c in senha))  # esperado: True
!! Queremos saber se tem ALGUM número: isso é any, não all.

@fn_any 2
frutas = ["maçã", "uva"]
print(any(f = "uva" for f in frutas))
>>> print(any(f == "uva" for f in frutas))
!! Para comparar use ==. Um = sozinho é atribuição.

@fn_any 2
numeros = [5, 8, 12]
print(any(numeros > 10))
>>> print(any(n > 10 for n in numeros))
!! Não dá para comparar a lista inteira com 10. Compare item por item.

@fn_any 2
notas = {"Ana": 9, "Caio": 4}
print(any(n < 5 for n in notas))
>>> print(any(n < 5 for n in notas.values()))
!! Percorrer o dicionário dá os nomes, e texto não se compara com número. Use .values().

@fn_any 3
palavras = ["bobo", "chato"]
frase = "que jogo chato"
print(any(frase in p for p in palavras))  # esperado: True
>>> print(any(p in frase for p in palavras))  # esperado: True
!! A ordem está trocada: queremos saber se a palavra está DENTRO da frase.

@fn_any 2
estoque = [3, 5, 7]
print(any(estoque))  # esperado: False
>>> print(any(q == 0 for q in estoque))  # esperado: False
!! any(estoque) só diz se algum número é diferente de zero. Para "algum acabou?", teste q == 0.

@fn_callable 4
def dobro(n):
    return n * 2

print(callable(dobro(3)))  # esperado: True
>>> print(callable(dobro))  # esperado: True
!! dobro(3) já é o resultado (6). Para perguntar sobre a função, tire os parênteses.

@fn_callable 2
nome = "Ana"
print(nome())
>>> print(nome)
!! nome é um texto, não uma função. Texto não pode ser chamado com ().

@fn_callable 1
list = [1, 2, 3]
letras = list("abc")
print(letras)
>>> numeros = [1, 2, 3]
!! Uma variável chamada list esconde a função list. Use outro nome.

@fn_callable 3
acoes = {"pular": lambda: "pulou", "nivel": 3}
for valor in acoes.values():
    print(valor())
>>> print(valor() if callable(valor) else valor)
!! O 3 não é função. Confira com callable antes de chamar.

@fn_callable 1
print(callable("print"))  # esperado: True
>>> print(callable(print))  # esperado: True
!! Com aspas, "print" é só um texto. A função é print, sem aspas.

@fn_callable 4
class Contador:
    def __init__(self):
        self.n = 0
    def call(self):
        self.n += 1
        return self.n

c = Contador()
print(c())
>>> def __call__(self):
!! Para o objeto ser chamável, o método precisa se chamar __call__.

@fn_isinstance 2
x = 5
print(isinstance(x, "int"))
>>> print(isinstance(x, int))
!! O tipo vai sem aspas: int, não "int".

@fn_isinstance 2
valor = 2.5
print(isinstance(valor, int or float))  # esperado: True
>>> print(isinstance(valor, (int, float)))  # esperado: True
!! int or float vale só int. Para vários tipos, use uma tupla.

@fn_isinstance 2
x = 3
print(isinstance(x, [int, float]))
>>> print(isinstance(x, (int, float)))
!! Os tipos vão numa tupla (parênteses), não numa lista.

@fn_isinstance 2
def eh_numero(x):
    return isinstance(x, int)

print(eh_numero(True))  # esperado: False
>>> return isinstance(x, int) and not isinstance(x, bool)
!! True também é int. Exclua bool de propósito.

@fn_isinstance 1
print(isinstance(str, "oi"))
>>> print(isinstance("oi", str))
!! Primeiro vem o valor, depois o tipo.

@fn_isinstance 4
dados = [3, "4", 5]
total = 0
for d in dados:
    if isinstance(d, str):
        total += d
print(total)
>>> if isinstance(d, int):
!! Para somar, queremos os números, não os textos.

@fn_issubclass 4
class Animal: pass
class Gato(Animal): pass
mimi = Gato()
print(issubclass(mimi, Animal))
>>> print(isinstance(mimi, Animal))
!! mimi é um objeto, não uma classe. Para objetos, use isinstance.

@fn_issubclass 3
class Animal: pass
class Gato(Animal): pass
print(issubclass(Animal, Gato))  # esperado: True
>>> print(issubclass(Gato, Animal))  # esperado: True
!! A ordem é (filha, mãe): Gato herda de Animal.

@fn_issubclass 2
class Veiculo: pass
class Carro: pass
print(issubclass(Carro, Veiculo))  # esperado: True
>>> class Carro(Veiculo): pass
!! Carro não colocou a mãe entre parênteses, então não herda de Veiculo.

@fn_issubclass 1
print(issubclass(bool, "int"))
>>> print(issubclass(bool, int))
!! A classe vai sem aspas.

@fn_issubclass 2
x = 5
print(issubclass(x, int))
>>> print(issubclass(type(x), int))
!! x é um número, não uma classe. type(x) dá a classe dele.

@fn_issubclass 3
class Fruta: pass
class Maca(Fruta): pass
print(issubclass(Maca, [Fruta, str]))
>>> print(issubclass(Maca, (Fruta, str)))
!! Várias classes vão numa tupla, não numa lista.

@fn_hasattr 1
print(hasattr("oi", upper))
>>> print(hasattr("oi", "upper"))
!! O nome do atributo vai entre aspas.

@fn_hasattr 1
print(hasattr("oi", "upper()"))  # esperado: True
>>> print(hasattr("oi", "upper"))  # esperado: True
!! O nome do método vai sem parênteses.

@fn_hasattr 2
d = {"cor": "azul"}
print(hasattr(d, "cor"))  # esperado: True
>>> print("cor" in d)  # esperado: True
!! Chaves de dicionário não são atributos. Use in.

@fn_hasattr 3
class Pet:
    def __init__(self, nome):
        self.Nome = nome

p = Pet("Rex")
print(hasattr(p, "nome"))  # esperado: True
>>> self.nome = nome
!! O atributo foi criado com N maiúsculo, e hasattr diferencia maiúsculas.

@fn_hasattr 2
x = 10
if not hasattr(x, "upper"):
    print(x.upper())
else:
    print(x)
>>> if hasattr(x, "upper"):
!! O not inverteu a lógica: só chame upper se ele existir.

@fn_hasattr 2
lista = [1, 2]
print(hasattr(lista, "push"))  # esperado: True
>>> print(hasattr(lista, "append"))  # esperado: True
!! Em Python, listas ganham itens com append, não push.
'''
