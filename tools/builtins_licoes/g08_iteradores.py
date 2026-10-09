from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

# Ajudante usado nos exemplos de aiter/anext: roda a corrotina "na mão", como a lição 1
# (asyncio.run não funciona no navegador).
RODAR = 'def rodar(corrotina):\n    try:\n        corrotina.send(None)\n    except StopIteration:\n        pass\n\n'
# Versão para os testes: devolve o valor de retorno da corrotina.
RODAR_T = 'def rodar(c):\n    try:\n        c.send(None)\n    except StopIteration as fim:\n        return fim.value\n\n'

LICOES = {
    # ================================================================ iter
    "iter": [
        # lição 2
        L("Com sentinela",
          "iter tem um segundo formato: iter(função, sentinela). Ele chama a função várias vezes e para quando ela devolve o valor sentinela. A função não pode ter argumentos, por isso é comum usar lambda.",
          'fila = [5, 8, 0, 4]\nfor n in iter(lambda: fila.pop(0), 0):\n    print(n)\nprint("sobrou:", fila)',
          [OUT('pedidos = ["suco", "bolo", "fim", "café"]\nfor p in iter(lambda: pedidos.pop(0), "fim"):\n    print(p)',
               ["suco\nbolo\nfim", "suco\nbolo\nfim\ncafé", "suco\nbolo\ncafé"],
               'Ao chegar no "fim", o laço para. O sentinela não aparece, e "café" nem é lido.'),
           TYPE('notas = [7, 9, -1, 8]\nboas = list(iter(lambda: notas.pop(0), -1))\nprint(boas)',
                "Pega 7 e 9; quando vem o -1, para."),
           MC("Em iter(f, sentinela), o primeiro argumento precisa ser…", "Uma função que pode ser chamada sem argumentos",
              ["Uma lista", "Um número", "Um texto"], "iter chama f() de novo a cada volta, até f() devolver o sentinela."),
           FILL("Complete para o laço parar quando aparecer \"sair\".",
                'cmds = ["ir", "pular", "sair", "voar"]\nfor c in iter(lambda: cmds.pop(0), ___):\n    print(c)',
                '"sair"', ['"voar"', '"ir"', 'None'], 'O sentinela é o valor que encerra o laço: "sair".')]),
        # lição 3
        L("Pulando o cabeçalho",
          "Um uso prático: pegue o primeiro item com next e deixe o for cuidar do resto. O for continua de onde o iterador parou, então o cabeçalho não se repete.",
          'linhas = iter(["nome,nota", "Ana,9", "Caio,7"])\ncabecalho = next(linhas)\nprint("Colunas:", cabecalho)\nfor linha in linhas:\n    nome, nota = linha.split(",")\n    print(nome, "tirou", nota)',
          [OUT('it = iter([1, 2, 3, 4])\nnext(it)\nprint(sum(it))', ["10", "1", "0"],
               "O 1 já saiu com o next. Sobra 2 + 3 + 4 = 9."),
           TYPE('dias = iter(["seg", "ter", "qua"])\nhoje = next(dias)\nprint(hoje, len(list(dias)))',
                "hoje é seg, e sobram 2 dias no iterador."),
           ORDER("Monte o programa que mostra o título e depois só os itens.",
                 ['compras = iter(["LISTA", "arroz", "feijão"])', 'print(next(compras))', 'for item in compras:', '    print("-", item)'],
                 "Primeiro cria o iterador, depois tira o título com next e o for mostra o resto."),
           CODE("A lista placar tem um título na primeira posição e depois as pontuações. Use iter e next para guardar o título em titulo e some só as pontuações em total.",
                'placar = ["Rodada 1", 10, 25, 5]\ntitulo = None\ntotal = 0\n',
                'placar = ["Rodada 1", 10, 25, 5]\nit = iter(placar)\ntitulo = next(it)\ntotal = sum(it)\nprint(titulo, total)',
                'assert titulo == "Rodada 1", "titulo deve ser o primeiro item: Rodada 1"\nassert total == 40, "total deve ser 10 + 25 + 5 = 40"',
                "it = iter(placar); titulo = next(it); total = sum(it) — o sum começa depois do título.")]),
        # lição 4
        L("Uso único e pegadinhas",
          "Um iterador só anda para frente: depois que chega ao fim, fica vazio para sempre. A lista continua inteira, e cada iter() novo começa do zero. E nem tudo é iterável: iter(42) dá TypeError.",
          'nums = [1, 2, 3]\nit = iter(nums)\nprint(list(it))\nprint(list(it))\nprint(list(iter(nums)))',
          [OUT('it = iter("oi")\nprint(list(it), list(it))', ["['o', 'i'] ['o', 'i']", "[] []", "['o', 'i']"],
               "O primeiro list() esvazia o iterador; o segundo recebe uma lista vazia."),
           MC("O que acontece em iter(42)?", "TypeError: um inteiro não é iterável",
              ["Devolve um iterador com 4 e 2", "Devolve um iterador vazio", "Devolve 42"],
              "Números não são coleções. Para contar até 42, use iter(range(42))."),
           OUT('it = iter([5, 6, 7])\nprint(5 in it)\nprint(list(it))', ["True\n[5, 6, 7]", "True\n[]", "False\n[6, 7]"],
               "O in vai consumindo o iterador até achar o 5. Sobram 6 e 7."),
           TYPE('it = iter([1, 2])\nprint(iter(it) is it)',
                "iter de algo que já é iterador devolve o próprio iterador."),
           OUT('pontos = {"ana": 3, "bia": 5}\nprint(next(iter(pontos)))', ["3", "('ana', 3)", "{'ana': 3}"],
               "Iterar um dicionário percorre as chaves. A primeira é ana.")]),
        # lição 5
        L("Combinando com zip",
          "Um truque famoso: passar o MESMO iterador duas vezes para zip. Como os dois lados puxam do mesmo lugar, os itens saem de dois em dois: zip(it, it) forma pares.",
          'dados = ["Ana", 9, "Caio", 7]\nit = iter(dados)\nfor nome, nota in zip(it, it):\n    print(nome, "->", nota)',
          [OUT('it = iter([1, 2, 3, 4])\nprint(list(zip(it, it)))', ["[(1, 1), (2, 2), (3, 3), (4, 4)]", "[(1, 3), (2, 4)]", "[1, 2, 3, 4]"],
               "Cada tupla puxa dois itens seguidos do mesmo iterador: (1, 2) e (3, 4)."),
           TYPE('it = iter("abcdef")\nprint(["".join(p) for p in zip(it, it, it)])',
                "Três vezes o mesmo iterador: grupos de 3 letras."),
           FILL("Complete para formar pares (chave, valor) e criar o dicionário {'a': 1, 'b': 2}.",
                'itens = ["a", 1, "b", 2]\nit = iter(itens)\nprint(dict(zip(it, ___)))',
                "it", ["itens", "iter(itens)", "next(it)"],
                "Os dois lados do zip precisam ser o mesmo iterador; senão cada um começa do zero."),
           CODE("Crie a função em_pares(lista) que devolve uma lista de tuplas com os itens de dois em dois. Ex.: em_pares([1, 2, 3, 4]) devolve [(1, 2), (3, 4)].",
                'def em_pares(lista):\n    pass\n',
                'def em_pares(lista):\n    it = iter(lista)\n    return list(zip(it, it))',
                'assert em_pares([1, 2, 3, 4]) == [(1, 2), (3, 4)], "em_pares([1, 2, 3, 4]) deve dar [(1, 2), (3, 4)]"\nassert em_pares(["x", "y"]) == [("x", "y")], "Com dois itens deve sair uma tupla só"\nassert em_pares([]) == [], "Lista vazia deve dar []"',
                "it = iter(lista); return list(zip(it, it)).")]),
        # lição 6
        L("Desafio: seu iterador",
          "Você pode criar um iterador com uma classe: __iter__ devolve o próprio objeto e __next__ entrega o próximo item, ou levanta StopIteration quando acabar. É isso que iter() e next() chamam por baixo.",
          'class Contagem:\n    def __init__(self, inicio):\n        self.atual = inicio\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.atual == 0:\n            raise StopIteration\n        self.atual -= 1\n        return self.atual + 1\n\nfor n in Contagem(3):\n    print(n)',
          [OUT('class Dobra:\n    def __init__(self):\n        self.n = 1\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.n > 8:\n            raise StopIteration\n        self.n *= 2\n        return self.n\n\nprint(list(Dobra()))',
               ["[1, 2, 4, 8]", "[2, 4, 8]", "[1, 2, 4, 8, 16]"],
               "Dobra antes de devolver: 2, 4, 8, 16. Quando n passa de 8, para."),
           MC("Para avisar que um iterador acabou, __next__ deve…", "Levantar StopIteration",
              ["Devolver None", "Devolver False", "Usar break"], "O for e o next entendem StopIteration como fim."),
           MC("O que __iter__ de um iterador costuma devolver?", "O próprio objeto (self)",
              ["Uma lista", "O próximo item", "None"], "Assim iter(obj) devolve obj, e o for pode usá-lo."),
           CODE("Complete a classe Pares para que ela entregue os números pares de 0 até limite (sem passar dele). Ex.: list(Pares(6)) dá [0, 2, 4, 6].",
                'class Pares:\n    def __init__(self, limite):\n        self.limite = limite\n        self.atual = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        raise StopIteration  # troque pela sua lógica\n',
                'class Pares:\n    def __init__(self, limite):\n        self.limite = limite\n        self.atual = 0\n    def __iter__(self):\n        return self\n    def __next__(self):\n        if self.atual > self.limite:\n            raise StopIteration\n        valor = self.atual\n        self.atual += 2\n        return valor',
                'assert list(Pares(6)) == [0, 2, 4, 6], "list(Pares(6)) deve dar [0, 2, 4, 6]"\nassert list(Pares(5)) == [0, 2, 4], "list(Pares(5)) deve dar [0, 2, 4]"\nassert list(Pares(0)) == [0], "list(Pares(0)) deve dar [0]"',
                "Se atual passou do limite, levante StopIteration; senão guarde o valor, some 2 e devolva.")]),
    ],

    # ================================================================ next
    "next": [
        # lição 2
        L("O valor padrão",
          "O segundo argumento de next é o padrão: o valor devolvido quando o iterador acaba, em vez de dar erro. Pode ser qualquer coisa: um texto, 0, None… Antes do fim, next entrega os itens normalmente.",
          'it = iter(["pão", "leite"])\nprint(next(it, "nada"))\nprint(next(it, "nada"))\nprint(next(it, "nada"))\nprint(next(it, None))',
          [OUT('it = iter([7])\nprint(next(it, 0) + next(it, 0))', ["14", "0", "Erro"],
               "O primeiro next dá 7; o segundo já não tem nada e devolve o padrão 0. 7 + 0 = 7."),
           TYPE('it = iter([])\nprint(next(it, "vazio"))', "O iterador já começa vazio, então vem o padrão."),
           MC("next(it, None) quando it já acabou devolve…", "None",
              ["StopIteration", "O último item de novo", "Uma lista vazia"], "Com padrão não há erro: vem o padrão."),
           OUT('it = iter("ab")\nprint(next(it, "z"), next(it, "z"), next(it, "z"))', ["a b", "z z z", "a b Erro"],
               "a e b saem normalmente; no terceiro, acabou e vem o padrão z.")]),
        # lição 3
        L("Achar o primeiro",
          "Truque muito usado: next com uma expressão geradora encontra o PRIMEIRO item que obedece a uma condição e para de procurar ali. Com um padrão, você trata o caso de não achar nada.",
          'precos = [12, 45, 8, 60]\ncaro = next((p for p in precos if p > 40), None)\nprint(caro)\nbarato = next((p for p in precos if p < 5), "nenhum")\nprint(barato)',
          [OUT('nomes = ["ana", "bruno", "beto"]\nprint(next(n for n in nomes if n.startswith("b")))', ["ana", "beto", "['bruno', 'beto']"],
               "next devolve só o primeiro que combina: bruno."),
           TYPE('idades = [12, 15, 19, 22]\nprint(next((i for i in idades if i >= 18), "ninguém"))',
                "O primeiro maior ou igual a 18 é 19."),
           FILL("Complete para não dar erro quando ninguém tirar 10.",
                'notas = [7, 8, 9]\nprint(next((n for n in notas if n == 10)___))',
                ', "sem 10"', [' or "sem 10"', ', default="sem 10"', '; "sem 10"'],
                "O padrão vem depois de uma vírgula, sem nome. next não aceita default=."),
           CODE("Crie a função primeiro_negativo(numeros) que devolve o primeiro número negativo da lista, ou 0 se não houver. Use next.",
                'def primeiro_negativo(numeros):\n    pass\n',
                'def primeiro_negativo(numeros):\n    return next((n for n in numeros if n < 0), 0)',
                'assert primeiro_negativo([3, -2, -5]) == -2, "Em [3, -2, -5] o primeiro negativo é -2"\nassert primeiro_negativo([1, 2]) == 0, "Sem negativos, deve devolver 0"\nassert primeiro_negativo([]) == 0, "Lista vazia deve devolver 0"',
                "return next((n for n in numeros if n < 0), 0)")]),
        # lição 4
        L("Cuidados com next",
          "Três armadilhas: next só funciona com iteradores, então next([1, 2]) dá TypeError. next(iter(lista)) cria um iterador novo toda vez e sempre pega o primeiro. E o padrão vai sem nome: next(it, default=0) dá erro.",
          'cores = ["azul", "verde"]\nprint(next(iter(cores)))\nprint(next(iter(cores)))\nit = iter(cores)\nprint(next(it), next(it))',
          [MC("O que acontece em next([1, 2, 3])?", "TypeError: lista não é iterador",
              ["Devolve 1", "Devolve 3", "Devolve [2, 3]"], "Lista é iterável, mas não é iterador. Use next(iter(lista))."),
           OUT('frutas = ["uva", "kiwi"]\nfor _ in range(2):\n    print(next(iter(frutas)))', ["uva\nkiwi", "kiwi\nkiwi", "Erro"],
               "A cada volta nasce um iterador novo, que começa do primeiro item."),
           OUT('it = iter([1, 2])\ntry:\n    next(it)\n    next(it)\n    next(it)\nexcept StopIteration:\n    print("acabou")', ["2", "None", "StopIteration"],
               "O terceiro next não tem item e levanta StopIteration, que o except captura."),
           MC("Qual destas linhas está certa?", "next(it, 0)",
              ["next(it, default=0)", "it.next()", "next(0, it)"],
              "O padrão é passado pela posição. it.next() não existe no Python 3; o método se chama __next__.")]),
        # lição 5
        L("Geradores e arquivos",
          "Geradores (funções com yield) são iteradores: cada next roda a função até o próximo yield e pausa ali. Arquivos abertos também são iteradores: next(arquivo) lê a próxima linha.",
          'def senhas():\n    for n in range(1, 100):\n        yield f"A{n:03d}"\n\npainel = senhas()\nprint(next(painel))\nprint(next(painel))\nprint(next(painel))',
          [OUT('def passos():\n    yield "esquerda"\n    yield "direita"\n\np = passos()\nnext(p)\nprint(next(p))', ["esquerda", "passos", "Erro"],
               "O primeiro next consome esquerda; o segundo pega direita."),
           TYPE('with open("notas.txt", "w", encoding="utf-8") as f:\n    f.write("aluno,nota\\nAna,9\\n")\nwith open("notas.txt", encoding="utf-8") as f:\n    print(next(f).strip())',
                "next(f) lê a primeira linha do arquivo; strip tira a quebra de linha."),
           ORDER("Monte o gerador e mostre os dois primeiros valores.",
                 ['def dobros():', '    for n in range(1, 4):', '        yield n * 2', 'g = dobros()', 'print(next(g), next(g))'],
                 "Primeiro define o gerador, depois cria g e chama next duas vezes: 2 4."),
           CODE('Complete o gerador ficha() para entregar, com yield, "Ficha 1", "Ficha 2" e "Ficha 3". Depois guarde a primeira ficha na variável primeira usando next.',
                'def ficha():\n    yield "Ficha 1"\n\nprimeira = None\n',
                'def ficha():\n    for n in range(1, 4):\n        yield f"Ficha {n}"\n\nprimeira = next(ficha())',
                'assert list(ficha()) == ["Ficha 1", "Ficha 2", "Ficha 3"], "ficha() deve entregar Ficha 1, Ficha 2 e Ficha 3"\nassert primeira == "Ficha 1", "primeira deve ser Ficha 1, pega com next"',
                'Use um for com yield f"Ficha {n}" e primeira = next(ficha()).')]),
        # lição 6
        L("Desafio: fila de atendimento",
          "Vamos simular uma fila: cada next pega a próxima pessoa, e o padrão avisa quando a fila esvaziou. Você vai juntar iter, next, padrão e funções.",
          'fila = iter(["Ana", "Caio", "Bia"])\n\ndef chamar():\n    pessoa = next(fila, None)\n    if pessoa is None:\n        return "Fila vazia"\n    return f"Próximo: {pessoa}"\n\nfor _ in range(4):\n    print(chamar())',
          [OUT('it = iter([3, 1, 2])\nmaior = next(it)\nfor n in it:\n    if n > maior:\n        maior = n\nprint(maior)', ["2", "1", "6"],
               "O primeiro item (3) vira o ponto de partida, e nenhum dos outros é maior."),
           TYPE('it = iter(range(10, 15))\nnext(it)\nnext(it)\nprint(next(it))', "10 e 11 já saíram; o terceiro é 12."),
           CODE('Crie a função chamar(fila) que recebe um iterador e devolve "Próximo: <nome>" com a próxima pessoa, ou "Fila vazia" quando não houver mais ninguém.',
                'def chamar(fila):\n    pass\n',
                'def chamar(fila):\n    pessoa = next(fila, None)\n    if pessoa is None:\n        return "Fila vazia"\n    return f"Próximo: {pessoa}"',
                'f = iter(["Ana", "Caio"])\nassert chamar(f) == "Próximo: Ana", "A primeira chamada deve dar Próximo: Ana"\nassert chamar(f) == "Próximo: Caio", "A segunda chamada deve dar Próximo: Caio"\nassert chamar(f) == "Fila vazia", "Com a fila vazia, deve dar Fila vazia"',
                "Use next(fila, None) e confira se veio None."),
           CODE('Crie a função primeira_longa(palavras) que devolve a primeira palavra com mais de 5 letras, ou "nenhuma" se não houver.',
                'def primeira_longa(palavras):\n    return palavras[0]\n',
                'def primeira_longa(palavras):\n    return next((p for p in palavras if len(p) > 5), "nenhuma")',
                'assert primeira_longa(["gato", "cachorro", "papagaio"]) == "cachorro", "Deve achar cachorro"\nassert primeira_longa(["sol", "lua"]) == "nenhuma", "Sem palavras longas, deve dar nenhuma"',
                'return next((p for p in palavras if len(p) > 5), "nenhuma")')]),
    ],

    # ================================================================ slice
    "slice": [
        # lição 2
        L("Início, fim e passo",
          "slice tem três partes, como [início:fim:passo]. Com um número só, slice(3) é o FIM (igual a [:3]). Use None para deixar uma parte em branco. As partes ficam em .start, .stop e .step.",
          's = slice(3)\nprint(s.start, s.stop, s.step)\nprint("banana"[s])\nt = slice(1, None, 2)\nprint("banana"[t])',
          [OUT('print("abcdefg"[slice(2)])', ["cdefg", "c", "abc"],
               "slice(2) é o mesmo que [:2]: do começo até antes do índice 2."),
           TYPE('s = slice(1, 8, 3)\nprint(s.start, s.stop, s.step)', "Cada atributo guarda uma parte da fatia."),
           OUT('print([0, 1, 2, 3, 4, 5][slice(-2, None)])', ["[0, 1, 2, 3]", "[4]", "[5, 4]"],
               "-2 é o penúltimo, e None no fim vai até o final: [4, 5]."),
           FILL('Complete para pegar uma letra sim, outra não: "pto".',
                'print("python"[slice(None, None, ___)])',
                "2", ["1", "-2", "0"], "Passo 2 pula de duas em duas: p, t, o.")]),
        # lição 3
        L("Fatias com nome",
          "No dia a dia, slice deixa o código legível: em vez de números soltos como [0:4], você dá nome à fatia. Isso ajuda muito com textos de tamanho fixo, como datas, CEPs e códigos.",
          'ANO = slice(0, 4)\nMES = slice(4, 6)\nDIA = slice(6, 8)\ndata = "20261007"\nprint(data[DIA], data[MES], data[ANO], sep="/")',
          [OUT('CEP = "01310100"\nINICIO = slice(0, 5)\nFIM = slice(5, None)\nprint(CEP[INICIO] + "-" + CEP[FIM])', ["01310-1000", "0131-0100", "01310100-"],
               "Os 5 primeiros dígitos, um hífen e o resto."),
           TYPE('placa = "ABC1D23"\nletras = slice(3)\nprint(placa[letras])', "slice(3) pega os 3 primeiros caracteres."),
           MC("Qual a vantagem de escrever NOME = slice(0, 10)?", "Dar um nome à fatia e reutilizá-la em vários lugares",
              ["Deixar o programa mais rápido", "Copiar a lista", "Ordenar os itens"],
              "O código fica mais claro e, se a posição mudar, você corrige num lugar só."),
           CODE('O texto hora está no formato HHMMSS (ex.: "143005"). Crie as fatias H, M e S com slice e mostre a hora no formato 14:30:05.',
                'hora = "143005"\n# crie H, M e S com slice\n',
                'hora = "143005"\nH = slice(0, 2)\nM = slice(2, 4)\nS = slice(4, 6)\nprint(hora[H], hora[M], hora[S], sep=":")',
                'assert isinstance(H, slice) and isinstance(M, slice) and isinstance(S, slice), "H, M e S devem ser criados com slice"\nassert __stdout__.strip() == "14:30:05", "A saída deve ser 14:30:05"',
                'H = slice(0, 2), M = slice(2, 4), S = slice(4, 6) e print com sep=":".')]),
        # lição 4
        L("Cuidados e pegadinhas",
          "slice não é range: ele não gera números, só descreve uma fatia, então for i in slice(3) dá TypeError. Passo 0 dá ValueError na hora de fatiar. E passar do tamanho não dá erro: vem só o que existe.",
          'nums = [1, 2, 3]\nprint(nums[slice(1, 100)])\nprint(nums[slice(5, 9)])\ntry:\n    nums[slice(None, None, 0)]\nexcept ValueError:\n    print("passo 0 não pode")',
          [MC("O que acontece em for i in slice(3): print(i)?", "TypeError: slice não é iterável",
              ["Mostra 0, 1 e 2", "Mostra 3", "Não mostra nada"], "Para contar, use range(3). slice só serve para fatiar."),
           OUT('print("oi"[slice(0, 50)])', ["IndexError", "o", "None"],
               "Fatiar além do fim não dá erro: vem o texto inteiro."),
           OUT('print([1, 2, 3][slice(2, 0)])', ["[3, 2]", "[2]", "Erro"],
               "Com passo positivo, começar no 2 e terminar no 0 não pega nada: []."),
           TYPE('s = slice(1, 3)\nprint([10, 20, 30, 40][s] == [10, 20, 30, 40][1:3])',
                "lista[s] e lista[1:3] são a mesma fatia."),
           MC("Por que lista[slice(None, None, 0)] dá erro?", "O passo não pode ser zero",
              ["None não é permitido", "A lista está vazia", "Falta um import"], "Com passo 0 a fatia nunca andaria.")]),
        # lição 5
        L("Trocar, apagar e indices",
          "Uma fatia também troca ou apaga pedaços de uma lista: lista[s] = [...] e del lista[s]. E s.indices(tamanho) mostra os números reais (início, fim, passo), que combinam com range.",
          'fila = ["a", "b", "c", "d", "e"]\nmeio = slice(1, 4)\nprint(fila[meio])\nfila[meio] = ["X"]\nprint(fila)\nprint(slice(None, None, 2).indices(5))',
          [OUT('nums = [1, 2, 3, 4, 5]\ndel nums[slice(0, 2)]\nprint(nums)', ["[1, 2]", "[1, 2, 3]", "[2, 3, 4, 5]"],
               "del apaga os índices 0 e 1. Sobra [3, 4, 5]."),
           TYPE('print(slice(-2, None).indices(10))', "Num tamanho 10, -2 é o índice 8; o fim é 10 e o passo, 1."),
           TYPE('pares = slice(0, None, 2)\nprint(list(range(*pares.indices(7))))',
                "indices(7) dá (0, 7, 2), e range(0, 7, 2) gera os índices pares."),
           CODE("Use o slice inicio para trocar os 3 primeiros itens da lista notas por um único 0. Ex.: [5, 6, 7, 8] vira [0, 8].",
                'notas = [5, 6, 7, 8]\ninicio = slice(0, 3)\n# troque a fatia aqui\n',
                'notas = [5, 6, 7, 8]\ninicio = slice(0, 3)\nnotas[inicio] = [0]',
                'assert notas == [0, 8], "notas deve ficar [0, 8]"',
                "notas[inicio] = [0] — do lado direito vai uma lista.")]),
        # lição 6
        L("Desafio: campos fixos",
          "Sistemas antigos guardam dados em linhas de tamanho fixo: cada campo ocupa sempre as mesmas posições. Com slice, você descreve cada campo uma vez e lê quantas linhas quiser.",
          'NOME = slice(0, 10)\nCIDADE = slice(10, 20)\nIDADE = slice(20, 22)\nlinha = "Ana       Recife    31"\nprint(linha[NOME].strip())\nprint(linha[CIDADE].strip())\nprint(int(linha[IDADE]) + 1)',
          [OUT('CAMPOS = {"uf": slice(0, 2), "num": slice(2, None)}\ncod = "PE123"\nprint(cod[CAMPOS["num"]], cod[CAMPOS["uf"]])', ["PE 123", "PE123", "123PE"],
               "Primeiro o número (do índice 2 em diante), depois a UF."),
           MC("Que fatia pega os 3 últimos caracteres de um texto?", "slice(-3, None)",
              ["slice(3)", "slice(-3)", "slice(None, -3)"],
              "slice(-3) define só o FIM: pegaria tudo menos os 3 últimos."),
           CODE('Cada linha de produto tem o código nas posições 0 a 3 e o preço em centavos nas posições 4 a 8. Complete ler(linha) para devolver a tupla (codigo, preco_em_reais) usando os slices. Ex.: ler("CAFE01250") dá ("CAFE", 12.5).',
                'CODIGO = slice(0, 4)\nPRECO = slice(4, 9)\n\ndef ler(linha):\n    pass\n',
                'CODIGO = slice(0, 4)\nPRECO = slice(4, 9)\n\ndef ler(linha):\n    return linha[CODIGO], int(linha[PRECO]) / 100',
                'assert ler("CAFE01250") == ("CAFE", 12.5), "ler(CAFE01250) deve dar (CAFE, 12.5)"\nassert ler("LEIT00499") == ("LEIT", 4.99), "ler(LEIT00499) deve dar (LEIT, 4.99)"',
                "return linha[CODIGO], int(linha[PRECO]) / 100")]),
    ],

    # ================================================================ aiter
    "aiter": [
        # lição 2
        L("async for usa aiter",
          "Assim como o for chama iter() escondido, o async for chama aiter() por você. Ele só funciona dentro de async def. Nos exemplos, a função rodar() faz o que a lição 1 fazia: empurra a corrotina com send(None) até ela terminar.",
          RODAR + 'async def contar():\n    for i in range(1, 4):\n        yield i\n\nasync def main():\n    async for n in contar():\n        print("passo", n)\n\nrodar(main())',
          [OUT(RODAR + 'async def cores():\n    yield "azul"\n    yield "rosa"\n\nasync def main():\n    async for c in cores():\n        print(c.upper())\n\nrodar(main())',
               ["azul\nrosa", "AZUL", "Erro"], "O async for passa pelas duas cores, e cada uma sai em maiúsculas."),
           MC("O async for chama, por baixo dos panos…", "aiter() e depois anext() até acabar",
              ["iter() e next()", "len() e índices", "asyncio.run()"], "É o mesmo esquema do for, na versão assíncrona."),
           MC("Onde o async for pode ser usado?", "Dentro de uma função async def",
              ["Em qualquer lugar do programa", "Só dentro de classes", "Só dentro de um for comum"],
              "Fora de async def ele dá SyntaxError."),
           TYPE(RODAR + 'async def nums():\n    for n in [2, 4, 6]:\n        yield n\n\nasync def main():\n    total = 0\n    async for n in nums():\n        total += n\n    print(total)\n\nrodar(main())',
                "2 + 4 + 6.")]),
        # lição 3
        L("Classe assíncrona",
          "Uma classe vira iterável assíncrona quando tem __aiter__ (que devolve self) e async def __anext__, que devolve o próximo item ou levanta StopAsyncIteration no fim. aiter(objeto) chama o __aiter__.",
          RODAR + 'class Contagem:\n    def __init__(self, n):\n        self.n = n\n    def __aiter__(self):\n        return self\n    async def __anext__(self):\n        if self.n == 0:\n            raise StopAsyncIteration\n        self.n -= 1\n        return self.n + 1\n\nasync def main():\n    async for x in Contagem(3):\n        print(x)\n\nrodar(main())',
          [MC("Para avisar que acabou, __anext__ deve levantar…", "StopAsyncIteration",
              ["StopIteration", "ValueError", "Nada, basta devolver None"],
              "No mundo assíncrono, o fim é StopAsyncIteration."),
           MC("O que aiter(obj) chama no objeto?", "obj.__aiter__()",
              ["obj.__iter__()", "obj.__anext__()", "obj.__len__()"], "aiter ↔ __aiter__, como iter ↔ __iter__."),
           FILL("Complete: __anext__ precisa ser uma função assíncrona.",
                'class Fila:\n    def __aiter__(self):\n        return self\n    ___ def __anext__(self):\n        raise StopAsyncIteration',
                "async", ["await", "yield", "lambda"], "__anext__ é definida com async def."),
           OUT(RODAR + 'class Eco:\n    def __init__(self, texto):\n        self.texto = texto\n        self.i = 0\n    def __aiter__(self):\n        return self\n    async def __anext__(self):\n        if self.i >= len(self.texto):\n            raise StopAsyncIteration\n        self.i += 1\n        return self.texto[self.i - 1] * 2\n\nasync def main():\n    async for p in Eco("oi"):\n        print(p)\n\nrodar(main())',
               ["o\ni", "oioi", "oo ii"], "Cada letra sai repetida (* 2), uma por linha.")]),
        # lição 4
        L("Cuidados com aiter",
          "aiter só aceita iteráveis assíncronos: aiter([1, 2]) dá TypeError, porque lista é do mundo síncrono. O contrário também vale: um for comum num gerador async dá TypeError. E aiter em si não usa await; quem precisa de await é o anext.",
          'async def gen():\n    yield 1\n\ntry:\n    aiter([1, 2])\nexcept TypeError:\n    print("lista não é assíncrona")\ntry:\n    for x in gen():\n        pass\nexcept TypeError:\n    print("gerador async pede async for")',
          [MC("O que acontece em aiter([1, 2, 3])?", "TypeError, pois lista não é iterável assíncrona",
              ["Devolve um iterador assíncrono da lista", "Devolve 1", "Só funciona dentro de async def"],
              "Para listas, use iter(). aiter é para objetos com __aiter__."),
           OUT('async def gen():\n    yield 1\n\nit = aiter(gen())\nprint(aiter(it) is it)', ["False", "Erro", "1"],
               "Como no iter, aiter de algo que já é iterador assíncrono devolve ele mesmo."),
           MC("Qual linha dá SyntaxError fora de uma função async def?", "x = await anext(it)",
              ["it = aiter(gen())", "g = gen()", "print(type(it).__name__)"],
              "await só pode aparecer dentro de async def. aiter é uma função comum."),
           MC("Você esqueceu o async e escreveu for x in gerador_async(). O que acontece?", "TypeError: o objeto não é iterável",
              ["Funciona normalmente", "O laço roda zero vezes, sem erro", "Os itens saem em ordem inversa"],
              "Gerador assíncrono não tem __iter__, só __aiter__.")]),
        # lição 5
        L("Compreensões assíncronas",
          "Dentro de async def dá para montar listas com async for: [x async for x in gen()]. E aiter combina com anext: crie o iterador uma vez, pegue alguns itens e deixe o resto para um async for.",
          RODAR + 'async def precos():\n    for p in [10, 25, 40]:\n        yield p\n\nasync def main():\n    dobro = [p * 2 async for p in precos()]\n    print(dobro)\n    it = aiter(precos())\n    print("primeiro:", await anext(it))\n    async for p in it:\n        print("resto:", p)\n\nrodar(main())',
          [OUT(RODAR + 'async def nums():\n    for n in range(5):\n        yield n\n\nasync def main():\n    print([n async for n in nums() if n % 2 == 0])\n\nrodar(main())',
               ["[0, 1, 2, 3, 4]", "[1, 3]", "Erro"], "O if filtra só os pares: 0, 2 e 4."),
           TYPE(RODAR + 'async def letras():\n    for c in "abc":\n        yield c\n\nasync def main():\n    it = aiter(letras())\n    await anext(it)\n    print("".join([c async for c in it]))\n\nrodar(main())',
                "O a já saiu com anext; a compreensão pega o resto."),
           MC("Qual compreensão é válida dentro de async def?", "[x async for x in gen()]",
              ["[async x for x in gen()]", "[x for x async in gen()]", "async [x for x in gen()]"],
              "O async vai logo antes do for."),
           CODE("Crie async def coletar(gerador) que devolve uma lista com todos os itens de um gerador assíncrono. Use uma compreensão com async for.",
                'async def coletar(gerador):\n    return []\n',
                'async def coletar(gerador):\n    return [x async for x in gerador]',
                RODAR_T + 'async def tres():\n    for n in [1, 2, 3]:\n        yield n\n\nasync def nada():\n    for n in []:\n        yield n\n\nassert rodar(coletar(tres())) == [1, 2, 3], "coletar deve devolver [1, 2, 3]"\nassert rodar(coletar(nada())) == [], "Sem itens, deve devolver []"',
                "return [x async for x in gerador]")]),
        # lição 6
        L("Desafio: gerador assíncrono",
          "Hora de criar o seu: um gerador assíncrono é um async def com yield. Quem consome usa async for (que chama aiter) ou aiter com anext.",
          RODAR + 'async def contagem(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nasync def main():\n    async for x in contagem(3):\n        print(x, "...")\n    print("Já!")\n\nrodar(main())',
          [OUT(RODAR + 'async def eco(palavras):\n    for p in palavras:\n        yield p + "!"\n\nasync def main():\n    it = aiter(eco(["oi", "tchau"]))\n    print(await anext(it))\n\nrodar(main())',
               ["oi", "oi!\ntchau!", "Erro"], "Só um anext, então sai só o primeiro item: oi!"),
           MC("O que torna uma função um gerador assíncrono?", "Ser async def e ter yield",
              ["Ser def e ter return", "Ter await sem yield", "Ser chamada com aiter"],
              "async def sem yield é só uma corrotina; com yield vira gerador assíncrono."),
           CODE("Complete o gerador assíncrono regressiva(n) para entregar n, n-1, ... até 1. Ex.: regressiva(3) entrega 3, 2, 1.",
                'async def regressiva(n):\n    yield n  # complete aqui\n',
                'async def regressiva(n):\n    while n > 0:\n        yield n\n        n -= 1',
                RODAR_T + 'async def coletar(n):\n    return [x async for x in aiter(regressiva(n))]\n\nassert rodar(coletar(3)) == [3, 2, 1], "regressiva(3) deve entregar 3, 2, 1"\nassert rodar(coletar(1)) == [1], "regressiva(1) deve entregar só 1"',
                "Um while n > 0 com yield n e n -= 1.")]),
    ],

    # ================================================================ anext
    "anext": [
        # lição 2
        L("Padrão e fim da linha",
          'Como o next, anext aceita um padrão: await anext(it, "fim") devolve "fim" quando acaba. Sem padrão, o fim vira StopAsyncIteration, que você pode capturar com try/except.',
          RODAR + 'async def sabores():\n    yield "uva"\n\nasync def main():\n    it = aiter(sabores())\n    print(await anext(it, "acabou"))\n    print(await anext(it, "acabou"))\n    try:\n        await anext(it)\n    except StopAsyncIteration:\n        print("sem padrão: StopAsyncIteration")\n\nrodar(main())',
          [OUT(RODAR + 'async def gen():\n    yield 5\n\nasync def main():\n    it = aiter(gen())\n    a = await anext(it, 0)\n    b = await anext(it, 0)\n    print(a + b)\n\nrodar(main())',
               ["10", "0", "Erro"], "a recebe 5; b recebe o padrão 0, porque acabou. 5 + 0 = 5."),
           TYPE(RODAR + 'async def vazio():\n    for x in []:\n        yield x\n\nasync def main():\n    print(await anext(vazio(), "nada"))\n\nrodar(main())',
                "O gerador não entrega nada, então vem o padrão."),
           FILL("Complete para capturar o fim do iterador assíncrono.",
                RODAR + 'async def gen():\n    yield 1\n\nasync def main():\n    it = aiter(gen())\n    await anext(it)\n    try:\n        await anext(it)\n    except ___:\n        print("acabou")\n\nrodar(main())',
                "StopAsyncIteration", ["StopIteration", "TypeError", "IndexError"],
                "anext sinaliza o fim com StopAsyncIteration."),
           MC("O que await anext(it, None) devolve quando it já acabou?", "None",
              ["StopAsyncIteration", "O último item de novo", "Uma lista vazia"], "Com padrão não há erro: vem o padrão.")]),
        # lição 3
        L("Pegando aos poucos",
          "anext serve para pegar só alguns itens, quando você quiser. Também acha o primeiro item que combina, junto com uma expressão geradora assíncrona: (x async for x in gen() if condição).",
          RODAR + 'async def temperaturas():\n    for t in [18, 22, 31, 35]:\n        yield t\n\nasync def main():\n    quente = await anext((t async for t in temperaturas() if t > 30), None)\n    print("primeira acima de 30:", quente)\n\nrodar(main())',
          [OUT(RODAR + 'async def senhas():\n    for n in range(1, 4):\n        yield f"S{n}"\n\nasync def main():\n    it = aiter(senhas())\n    await anext(it)\n    print(await anext(it))\n\nrodar(main())',
               ["S1", "S3", "S1\nS2"], "O primeiro anext consome S1; o segundo pega S2."),
           TYPE(RODAR + 'async def nomes():\n    for n in ["ana", "bruno", "bia"]:\n        yield n\n\nasync def main():\n    b = await anext((n async for n in nomes() if n.startswith("b")), "?")\n    print(b)\n\nrodar(main())',
                "O primeiro nome que começa com b."),
           MC("Quando faz sentido usar anext em vez de async for?", "Para pegar só um item (ou poucos) na hora que você quiser",
              ["Sempre, porque async for não existe", "Para ordenar os itens", "Para transformar a lista em texto"],
              "async for percorre tudo; anext pega um de cada vez, sob seu controle."),
           CODE("Crie async def primeiro_par(gerador) que devolve o primeiro número par de um gerador assíncrono, ou None se não houver. Use anext com padrão.",
                'async def primeiro_par(gerador):\n    return None\n',
                'async def primeiro_par(gerador):\n    return await anext((n async for n in gerador if n % 2 == 0), None)',
                RODAR_T + 'async def gen(lista):\n    for x in lista:\n        yield x\n\nassert rodar(primeiro_par(gen([3, 8, 4]))) == 8, "Em 3, 8, 4 o primeiro par é 8"\nassert rodar(primeiro_par(gen([1, 5]))) is None, "Sem pares, deve devolver None"',
                "return await anext((n async for n in gerador if n % 2 == 0), None)")]),
        # lição 4
        L("Cuidados com anext",
          "Três armadilhas: sem await você recebe um objeto 'aguardável', não o item. anext só aceita iteradores assíncronos: anext(iter([1])) dá TypeError. E o padrão vai sem nome: anext(it, default=0) também dá TypeError.",
          RODAR + 'async def gen():\n    yield "a"\n\nasync def main():\n    it = aiter(gen())\n    sem_await = anext(it)\n    print(sem_await == "a")\n    print(await sem_await)\n\nrodar(main())',
          [MC("O que acontece em x = anext(it), sem await, dentro de async def?", "x recebe um objeto aguardável, não o item",
              ["x recebe o próximo item", "Dá SyntaxError", "O programa para"],
              "O item só chega quando você espera: await anext(it)."),
           OUT(RODAR + 'async def main():\n    try:\n        await anext(iter([1, 2]))\n    except TypeError:\n        print("iterador comum não serve")\n\nrodar(main())',
               ["1", "StopAsyncIteration", "[1, 2]"], "iter([1, 2]) é síncrono; anext recusa com TypeError."),
           MC("Qual linha está certa?", "await anext(it, 0)",
              ["await anext(it, default=0)", "anext(await it)", "await it.anext()"],
              "O padrão vai pela posição, e o await fica antes do anext."),
           OUT(RODAR + 'async def gen():\n    yield 1\n    yield 2\n\nasync def main():\n    print(await anext(gen()))\n    print(await anext(gen()))\n\nrodar(main())',
               ["1\n2", "2\n2", "Erro"], "Cada gen() cria um gerador novo, que começa do 1. Guarde o iterador numa variável.")]),
        # lição 5
        L("while e classes",
          "Dá para percorrer tudo só com anext: um while True que para quando vem o padrão. E anext funciona com qualquer objeto que tenha async def __anext__, inclusive classes suas.",
          RODAR + 'class Dado:\n    def __init__(self, faces):\n        self.faces = faces\n    def __aiter__(self):\n        return self\n    async def __anext__(self):\n        if not self.faces:\n            raise StopAsyncIteration\n        return self.faces.pop(0)\n\nasync def main():\n    d = Dado([6, 2, 5])\n    while True:\n        face = await anext(d, None)\n        if face is None:\n            break\n        print("tirou", face)\n\nrodar(main())',
          [OUT(RODAR + 'async def gen():\n    for x in "abc":\n        yield x\n\nasync def main():\n    it = aiter(gen())\n    texto = ""\n    while True:\n        c = await anext(it, "")\n        if c == "":\n            break\n        texto = c + texto\n    print(texto)\n\nrodar(main())',
               ["abc", "a", "c"], "Cada letra entra na FRENTE do texto, então ele sai invertido: cba."),
           TYPE(RODAR + 'class Moedas:\n    def __init__(self):\n        self.lista = [1, 5, 10]\n    def __aiter__(self):\n        return self\n    async def __anext__(self):\n        if not self.lista:\n            raise StopAsyncIteration\n        return self.lista.pop()\n\nasync def main():\n    m = Moedas()\n    print(await anext(m), await anext(m))\n\nrodar(main())',
                "pop() tira do fim da lista: primeiro 10, depois 5."),
           FILL('Complete para o while parar quando vier "fim".',
                RODAR + 'async def gen():\n    yield 1\n\nasync def main():\n    it = aiter(gen())\n    while True:\n        x = await anext(it, ___)\n        if x == "fim":\n            break\n        print(x)\n\nrodar(main())',
                '"fim"', ["None", "0", "break"], 'O padrão precisa ser o mesmo valor que o if confere: "fim".'),
           CODE("Crie async def somar(it) que soma todos os itens de um iterador assíncrono usando um while com await anext(it, None), parando quando vier None.",
                'async def somar(it):\n    total = 0\n    return total\n',
                'async def somar(it):\n    total = 0\n    while True:\n        n = await anext(it, None)\n        if n is None:\n            break\n        total += n\n    return total',
                RODAR_T + 'async def gen(lista):\n    for x in lista:\n        yield x\n\nassert rodar(somar(gen([1, 2, 3]))) == 6, "A soma de 1, 2 e 3 deve dar 6"\nassert rodar(somar(gen([]))) == 0, "Sem itens, a soma é 0"',
                "while True: n = await anext(it, None); se for None, break; senão total += n.")]),
        # lição 6
        L("Desafio: pedidos assíncronos",
          "Juntando tudo: aiter cria o iterador, await anext pega um item por vez e o padrão avisa quando acabou. Vamos atender pedidos que chegam de um gerador assíncrono.",
          RODAR + 'async def pedidos():\n    for p in ["pizza", "suco"]:\n        yield p\n\nasync def atender(it):\n    pedido = await anext(it, None)\n    if pedido is None:\n        return "Sem pedidos"\n    return f"Preparando {pedido}"\n\nasync def main():\n    it = aiter(pedidos())\n    for _ in range(3):\n        print(await atender(it))\n\nrodar(main())',
          [OUT(RODAR + 'async def gen():\n    for n in [4, 7]:\n        yield n\n\nasync def main():\n    it = aiter(gen())\n    a = await anext(it)\n    b = await anext(it)\n    c = await anext(it, a + b)\n    print(c)\n\nrodar(main())',
               ["4", "7", "Erro"], "O terceiro anext não tem item e devolve o padrão a + b = 11."),
           MC("Num programa normal (fora do navegador), como se roda a corrotina main()?", "import asyncio e asyncio.run(main())",
              ["Só chamar main()", "await main() no começo do arquivo", "anext(main())"],
              "asyncio.run cuida de tudo. Aqui usamos rodar() porque o app roda no navegador."),
           CODE('Crie async def atender(it) que pega o próximo pedido com anext e devolve "Preparando <pedido>", ou "Sem pedidos" quando o iterador acabou.',
                'async def atender(it):\n    return "Sem pedidos"\n',
                'async def atender(it):\n    pedido = await anext(it, None)\n    if pedido is None:\n        return "Sem pedidos"\n    return f"Preparando {pedido}"',
                RODAR_T + 'async def gen(lista):\n    for x in lista:\n        yield x\n\nit = aiter(gen(["bolo"]))\nassert rodar(atender(it)) == "Preparando bolo", "O primeiro deve dar Preparando bolo"\nassert rodar(atender(it)) == "Sem pedidos", "Depois que acabou, deve dar Sem pedidos"',
                "pedido = await anext(it, None); se for None, devolva Sem pedidos.")]),
    ],
}

BUGS = r'''
@fn_iter 1
nums = iter(10)
for n in nums:
    print(n)
>>> nums = iter(range(10))
!! Um número não é iterável. Use range(10) para ter de 0 a 9.

@fn_iter 4
notas = [7, 8, 9]
it = iter(notas)
print(sum(it))
print(len(list(it)))  # esperado: 3
>>> print(len(notas))  # esperado: 3
!! O sum já esvaziou o iterador. Conte a lista original.

@fn_iter 2
fila = ["a", "b", "fim", "c"]
for x in iter(lambda: fila.pop(0), "FIM"):
    print(x)
>>> for x in iter(lambda: fila.pop(0), "fim"):
!! O sentinela "FIM" nunca aparece; a lista esvazia e dá erro. O certo é "fim".

@fn_iter 2
fila = [3, 1, 0, 5]
for n in iter(fila.pop(0), 0):
    print(n)
>>> for n in iter(lambda: fila.pop(0), 0):
!! Com sentinela, iter precisa de uma função, não de um valor. Use lambda.

@fn_iter 4
linhas = ["nome", "Ana", "Bia"]
it = iter(linhas)
next(it)
print(len(list(linhas)))  # esperado: 2
>>> print(len(list(it)))  # esperado: 2
!! O cabeçalho saiu do iterador, não da lista. Use it.

@fn_iter 3
dados = ["a", 1, "b", 2]
it = iter(dados)
pares = zip(it, dados)
print(dict(pares))  # esperado: {'a': 1, 'b': 2}
>>> pares = zip(it, it)
!! Para formar pares, os dois lados do zip precisam ser o mesmo iterador.

@fn_next 2
cartas = ["A", "K", "Q"]
print(next(cartas))
>>> print(next(iter(cartas)))
!! Lista não é iterador. Crie um com iter() antes do next.

@fn_next 2
it = iter([])
print(next(it, default="vazio"))
>>> print(next(it, "vazio"))
!! next não aceita default=. O padrão vai pela posição.

@fn_next 2
nomes = ["Ana", "Bia"]
achado = next(n for n in nomes if n.startswith("C"))
print(achado)
>>> achado = next((n for n in nomes if n.startswith("C")), None)
!! Ninguém começa com C e não há padrão: dá StopIteration. Passe None como padrão.

@fn_next 3
dias = ["seg", "ter", "qua"]
it = iter(dias)
primeiro = next(iter(dias))
segundo = next(it)
print(segundo)  # esperado: ter
>>> primeiro = next(it)
!! iter(dias) cria um iterador novo. Use o mesmo it nas duas chamadas.

@fn_next 5
def senhas():
    for n in range(1, 4):
        yield n
g = senhas()
print(next(g), next(senhas()))  # esperado: 1 2
>>> print(next(g), next(g))  # esperado: 1 2
!! senhas() cria um gerador novo, que começa do 1. Use g de novo.

@fn_next 2
linhas = iter(["nota", "7", "9"])
cabecalho = linhas
total = sum(int(x) for x in linhas)
print(cabecalho, total)  # esperado: nota 16
>>> cabecalho = next(linhas)
!! Faltou tirar o cabeçalho com next; aí int("nota") dá erro.

@fn_slice 1
pulo = slice(None, None, 0)
print("abcdef"[pulo])  # esperado: ace
>>> pulo = slice(None, None, 2)
!! O passo não pode ser 0. Para pular de 2 em 2, use 2.

@fn_slice 2
placa = "ABC1D23"
numeros = slice(3)
print(placa[numeros])  # esperado: 1D23
>>> numeros = slice(3, None)
!! slice(3) é o FIM, não o início. Use slice(3, None).

@fn_slice 1
ANO = slice(0, 3)
data = "20261007"
print(data[ANO])  # esperado: 2026
>>> ANO = slice(0, 4)
!! O fim não entra na fatia. Para 4 dígitos, vá até 4.

@fn_slice 1
meio = slice(1:4)
print([1, 2, 3, 4, 5][meio])
>>> meio = slice(1, 4)
!! Dentro de slice() os valores vão separados por vírgula, não por dois-pontos.

@fn_slice 3
texto = "Pipoca"
fatia = slice(0, 4)
print(texto(fatia))
>>> print(texto[fatia])
!! Fatia se usa com colchetes, não com parênteses.

@fn_slice 3
notas = [5, 6, 7, 8]
inicio = slice(0, 2)
notas[inicio] = 0
print(notas)
>>> notas[inicio] = [0]
!! Para trocar uma fatia, o lado direito precisa ser uma lista.

@fn_aiter 4
async def notas():
    yield 7
async def main():
    for n in notas():
        print(n)
try: main().send(None)
except StopIteration: pass
>>> async for n in notas():
!! Gerador assíncrono pede async for, que chama aiter por você.

@fn_aiter 4
async def cores():
    yield "azul"
async def main():
    it = iter(cores())
    print(await anext(it))
try: main().send(None)
except StopIteration: pass
>>> it = aiter(cores())
!! Gerador assíncrono usa aiter, não iter.

@fn_aiter 3
class Vazio:
    def __aiter__(self):
        pass
    async def __anext__(self):
        raise StopAsyncIteration
print(aiter(Vazio()) is not None)
>>> return self
!! __aiter__ precisa devolver o iterador (self), senão aiter dá TypeError.

@fn_aiter 3
class Fila:
    def __aiter__(self): return self
    async def __anext__(self): raise StopIteration
async def main():
    async for x in Fila(): print(x)
try: main().send(None)
except StopIteration: print("fim")
>>> async def __anext__(self): raise StopAsyncIteration
!! No mundo assíncrono, o fim é StopAsyncIteration.

@fn_aiter 4
async def cores():
    yield "azul"
async def main():
    it = aiter(cores)
    print(await anext(it))
try: main().send(None)
except StopIteration: pass
>>> it = aiter(cores())
!! Faltaram os parênteses: chame cores() para criar o gerador.

@fn_aiter 4
async def nums():
    for n in range(3): yield n
async def main():
    print([n for n in nums()])
try: main().send(None)
except StopIteration: pass
>>> print([n async for n in nums()])
!! Na compreensão de um gerador assíncrono, use async for.

@fn_anext 5
async def gen():
    yield "oi"
async def main():
    it = aiter(gen())
    print(anext(it) == "oi")  # esperado: True
try: main().send(None)
except StopIteration: pass
>>> print(await anext(it) == "oi")  # esperado: True
!! Sem await, anext devolve um objeto aguardável, não o item.

@fn_anext 4
async def gen():
    yield 1
async def main():
    print(await anext(gen(), default=0))
try: main().send(None)
except StopIteration: pass
>>> print(await anext(gen(), 0))
!! anext não aceita default=. O padrão vai pela posição.

@fn_anext 5
async def gen():
    yield 1
async def main():
    it = aiter(gen())
    print(await next(it))
try: main().send(None)
except StopIteration: pass
>>> print(await anext(it))
!! Para iterador assíncrono, use anext, não next.

@fn_anext 5
async def gen():
    yield "a"
async def main():
    it = aiter(gen())
    print(await anext(it), await anext(it))  # esperado: a fim
try: main().send(None)
except StopIteration: pass
>>> print(await anext(it), await anext(it, "fim"))  # esperado: a fim
!! Só há um item; sem padrão, o segundo anext dá StopAsyncIteration.

@fn_anext 5
async def gen():
    for n in [1, 2]: yield n
async def main():
    it = aiter(gen())
    print(await anext(it), await anext(gen()))  # esperado: 1 2
try: main().send(None)
except StopIteration: pass
>>> print(await anext(it), await anext(it))  # esperado: 1 2
!! gen() cria um gerador novo, que começa do 1. Use o mesmo it.

@fn_anext 5
async def vazio():
    for x in []: yield x
async def main():
    try: await anext(vazio())
    except StopIteration: print("acabou")
try: main().send(None)
except StopIteration: pass
>>> except StopAsyncIteration: print("acabou")
!! anext avisa o fim com StopAsyncIteration, não StopIteration.
'''
