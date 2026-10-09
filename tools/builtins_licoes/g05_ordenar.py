from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ sorted
    "sorted": [
        # lição 2
        L("Critérios com key",
          "key recebe uma função que é aplicada em cada item só na hora de comparar: key=len ordena pelo tamanho. Uma lambda é uma função de uma linha: lambda x: x[1] devolve o segundo elemento de x. E reverse=True vira a ordem de cabeça para baixo.",
          'frutas = ["kiwi", "banana", "uva"]\nprint(sorted(frutas, key=len))\nprint(sorted(frutas, key=len, reverse=True))\nnotas = [("Ana", 8), ("Bia", 10), ("Caio", 6)]\nprint(sorted(notas, key=lambda x: x[1]))',
          [OUT('print(sorted(["ccc", "a", "bb"], key=len))', ["['ccc', 'bb', 'a']", "['a', 'ccc', 'bb']", "[1, 2, 3]"], "key=len compara os tamanhos (3, 1, 2), mas a lista guarda as palavras."),
           TYPE('print(sorted([3, -5, 1], key=abs))', "key=abs compara 3, 5 e 1, sem o sinal. O -5 fica por último."),
           MC("Para ordenar do maior para o menor, use…", "reverse=True", ["key=-1", "reverse=False", "sorted(lista, 1)"], "reverse=True inverte a ordem final."),
           FILL("Complete para ordenar as palavras pelo tamanho.", 'palavras = ["sol", "lua", "estrela"]\nprint(sorted(palavras, key=___))', "len", ["len()", "size", "str"], "Passe a função len sem parênteses: o sorted chama ela para cada item.")]),
        # lição 3
        L("Rankings e dicionários",
          "sorted em um dicionário devolve as chaves em ordem. Para ordenar pelos valores, use d.items() com key=lambda par: par[1]. Depois, fatiar com [:3] pega o pódio.",
          'pontos = {"Ana": 30, "Bia": 50, "Caio": 40}\nprint(sorted(pontos))\nranking = sorted(pontos.items(), key=lambda par: par[1], reverse=True)\nprint(ranking)\nprint(ranking[0][0], "venceu")',
          [OUT('estoque = {"uva": 5, "maçã": 2, "banana": 9}\nprint(sorted(estoque))', ["['uva', 'maçã', 'banana']", "[2, 5, 9]", "['banana', 'uva', 'maçã']"], "Percorrer um dicionário entrega as chaves, e elas saem em ordem alfabética."),
           TYPE('tempos = [12.5, 9.8, 11.2, 10.4]\nprint(sorted(tempos)[:2])', "Ordena do menor para o maior e pega os dois primeiros."),
           MC("O que sorted(d.items(), key=lambda p: p[1]) ordena?", "Os pares (chave, valor), pelo valor", ["Só as chaves", "Os pares, pela chave", "Só os valores"], "items() dá pares, e p[1] é o valor de cada par."),
           CODE("Crie a função top3(notas) que recebe uma lista de números e devolve uma lista com as 3 maiores, da maior para a menor.",
                "def top3(notas):\n    return notas\n",
                "def top3(notas):\n    return sorted(notas, reverse=True)[:3]",
                'assert top3([5, 9, 7, 10, 3]) == [10, 9, 7], "top3([5, 9, 7, 10, 3]) deve devolver [10, 9, 7]"\nassert top3([1, 2]) == [2, 1], "Com só 2 notas, devolva as 2, da maior para a menor"',
                "sorted(notas, reverse=True) ordena do maior para o menor e [:3] pega as três primeiras.")]),
        # lição 4
        L("Pegadinhas do sorted",
          "Maiúsculas vêm antes de minúsculas, e textos com números são comparados letra a letra: \"10\" vem antes de \"9\". Misturar números e textos dá TypeError. E lembre: lista.sort() devolve None.",
          'print(sorted(["banana", "Uva", "abacaxi"]))\nprint(sorted(["10", "9", "100"]))\nprint(sorted(["10", "9", "100"], key=int))\ntry:\n    sorted([3, "a"])\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('print(sorted(["b", "C", "a"]))', ["['a', 'b', 'C']", "['C', 'b', 'a']", "['a', 'C', 'b']"], "Toda maiúscula vem antes de qualquer minúscula."),
           OUT('n = [3, 1, 2]\nr = n.sort()\nprint(r)', ["[1, 2, 3]", "[3, 1, 2]", "Erro"], "sort() altera a própria lista e devolve None."),
           TYPE('print(sorted(["20", "3", "100"]))', "São textos: compara o primeiro caractere. \"1\" < \"2\" < \"3\"."),
           MC('O que acontece em sorted([2, "1", 3])?', "Dá TypeError", ['Devolve ["1", 2, 3]', "Devolve [2, 3]", "Converte tudo para texto"], "Python não sabe dizer se um número é menor que um texto.")]),
        # lição 5
        L("Combinando com sorted",
          "sorted(set(lista)) tira os repetidos e ordena de uma vez. \", \".join(sorted(...)) monta um texto em ordem. Para desempatar, a key pode devolver uma tupla: compara o primeiro valor e, se empatar, o segundo.",
          'cores = ["azul", "rosa", "azul", "verde"]\nprint(sorted(set(cores)))\nprint(", ".join(sorted(cores)))\nalunos = [("Bia", 8), ("Ana", 9), ("Caio", 8)]\nprint(sorted(alunos, key=lambda a: (-a[1], a[0])))',
          [TYPE('print(sorted(set([3, 1, 3, 2, 1])))', "set tira os repetidos e sorted devolve uma lista em ordem."),
           OUT('print("-".join(sorted("pato")))', ["p-a-t-o", "aopt", "t-p-o-a"], "sorted separa e ordena as letras; join junta com hífen."),
           OUT('print(sorted([(2, "b"), (1, "z"), (2, "a")]))', ["[(1, 'z'), (2, 'b'), (2, 'a')]", "[(2, 'a'), (2, 'b'), (1, 'z')]", "Erro"], "Tuplas comparam o 1º item; se empatar, o 2º."),
           ORDER("Monte o programa que mostra os nomes sem repetição, em ordem, separados por vírgula.",
                 ['nomes = ["Leo", "Ana", "Leo"]', 'unicos = sorted(set(nomes))', 'print(", ".join(unicos))'],
                 "Primeiro a lista, depois tira repetidos e ordena, e por fim junta.")]),
        # lição 6
        L("Desafio: classificação",
          "Hora de montar a tabela de um campeonato: mais pontos primeiro e, no empate, ordem alfabética. O sinal de menos em -pontos faz o maior vir antes.",
          'times = {"Leões": 7, "Corvos": 9, "Tigres": 7}\ntabela = sorted(times.items(), key=lambda t: (-t[1], t[0]))\nfor nome, pts in tabela:\n    print(nome, pts)',
          [OUT('print(sorted([4, 1, 3], key=lambda n: -n))', ["[1, 3, 4]", "[-4, -3, -1]", "[4, 1, 3]"], "A key só compara: -4 é o menor, então o 4 vem primeiro. Os itens não mudam."),
           TYPE('print(sorted(["oi", "a", "olá"], key=len)[-1])', "O mais comprido fica no fim, e [-1] pega o último."),
           MC("Qual key ordena palavras pela última letra?", "key=lambda p: p[-1]", ["key=lambda p: p[0]", "key=len", "key=p[-1]"], "p[-1] é a última letra de cada palavra p."),
           CODE("Crie classificar(times) que recebe um dicionário {time: pontos} e devolve a lista de NOMES do mais pontuado para o menos. No empate, use a ordem alfabética.",
                "def classificar(times):\n    return sorted(times)\n",
                "def classificar(times):\n    return sorted(times, key=lambda t: (-times[t], t))",
                'assert classificar({"Lobos": 3, "Ursos": 9, "Gatos": 6}) == ["Ursos", "Gatos", "Lobos"], "Quem tem mais pontos vem primeiro"\nassert classificar({"Zebras": 5, "Antas": 5, "Corujas": 1}) == ["Antas", "Zebras", "Corujas"], "No empate, use a ordem alfabética"',
                "sorted(times, key=lambda t: (-times[t], t)) ordena pelos pontos (do maior) e desempata pelo nome.")]),
    ],

    # ================================================================ reversed
    "reversed": [
        # lição 2
        L("O que dá para inverter",
          "reversed funciona com sequências que têm ordem: listas, textos, tuplas e range. Um set não tem ordem, então dá TypeError. O resultado é um iterador: transforme com list(), tuple() ou \"\".join().",
          'print(list(reversed((1, 2, 3))))\nprint(list(reversed(range(1, 6))))\nprint("".join(reversed("amor")))\ntry:\n    reversed({1, 2})\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('print(tuple(reversed("abc")))', ["('abc',)", "cba", "['c', 'b', 'a']"], "tuple() transforma o iterador numa tupla de letras."),
           TYPE('print(list(reversed(range(2, 9, 3))))', "range(2, 9, 3) é 2, 5, 8. Invertido: 8, 5, 2."),
           MC("Qual destes dá erro com reversed?", "Um set, como {1, 2, 3}", ["Uma lista", "Um texto", "Um range"], "Set não tem ordem, então não existe 'de trás para frente'."),
           FILL("Complete para mostrar o texto invertido: odnum", 'print(___.join(reversed("mundo")))', '""', ['" "', "str", "list"], "Juntando com texto vazio, as letras ficam coladas.")]),
        # lição 3
        L("Usos do dia a dia",
          "reversed é ótimo para contagens regressivas, para ver os itens mais recentes primeiro e para conferir palíndromos: palavras que se leem igual nos dois sentidos.",
          'for n in reversed(range(1, 4)):\n    print(n)\nprint("Já!")\nhistorico = ["login", "compra", "logout"]\nprint(list(reversed(historico)))\npalavra = "arara"\nprint(palavra == "".join(reversed(palavra)))',
          [OUT('for n in reversed(range(3)):\n    print(n, end="")', ["012", "321", "3210"], "range(3) é 0, 1, 2. Invertido: 2, 1, 0."),
           TYPE('p = "ovo"\nprint(p == "".join(reversed(p)))', "ovo de trás para frente continua ovo."),
           MC("Uma lista msgs guarda mensagens da mais antiga para a mais nova. Como percorrer da mais nova para a mais antiga?", "for m in reversed(msgs):", ["for m in msgs:", "for m in sorted(msgs):", "for m in msgs.reversed():"], "reversed começa do último item, que é o mais novo."),
           CODE("Crie eh_palindromo(texto) que devolve True se o texto for igual de trás para frente, ignorando maiúsculas.",
                "def eh_palindromo(texto):\n    return False\n",
                'def eh_palindromo(texto):\n    t = texto.lower()\n    return t == "".join(reversed(t))',
                'assert eh_palindromo("Ana") is True, "Ana é palíndromo (ignore as maiúsculas)"\nassert eh_palindromo("radar") is True, "radar é palíndromo"\nassert eh_palindromo("pipo") is False, "pipo não é palíndromo"',
                'Deixe tudo minúsculo com lower() e compare com "".join(reversed(t)).')]),
        # lição 4
        L("Pegadinhas do reversed",
          "reversed devolve um iterador, e iterador só pode ser percorrido UMA vez: na segunda, vem vazio. Ele não muda a lista original; para inverter a própria lista, use lista.reverse(). E reversed(l)[0] dá TypeError, porque iterador não tem índice.",
          'nums = [1, 2, 3]\nr = reversed(nums)\nprint(list(r))\nprint(list(r))\nprint(nums)\nnums.reverse()\nprint(nums)',
          [OUT('r = reversed("ab")\nprint(list(r), list(r))', ["['b', 'a'] ['b', 'a']", "['a', 'b'] []", "Erro"], "O primeiro list() gasta o iterador; o segundo recebe nada."),
           OUT('l = [1, 2, 3]\nreversed(l)\nprint(l)', ["[3, 2, 1]", "None", "Erro"], "reversed não altera a lista, e o resultado foi jogado fora."),
           MC("Qual é o jeito certo de pegar o primeiro item da versão invertida de l?", "list(reversed(l))[0]", ["reversed(l)[0]", "reversed(l, 0)", "reversed(l).first"], "Converta para lista antes de usar índice."),
           TYPE('l = [5, 6, 7]\nprint(l.reverse())', "reverse() altera a lista e devolve None.")]),
        # lição 5
        L("Combinando com reversed",
          "reversed(sorted(l)) dá a ordem decrescente. zip(l, reversed(l)) pareia o primeiro com o último. A fatia l[::-1] também inverte, mas cria uma cópia inteira na hora.",
          'notas = [6, 9, 7]\nprint(list(reversed(sorted(notas))))\nprint(notas[::-1])\nfor a, b in zip("abc", reversed("abc")):\n    print(a, b)',
          [OUT('print(list(zip([1, 2, 3], reversed([1, 2, 3]))))', ["[(1, 1), (2, 2), (3, 3)]", "[(3, 1), (2, 2), (1, 3)]", "[1, 3, 2, 2, 3, 1]"], "O 1º da lista anda junto com o último, e assim por diante."),
           TYPE('print(list(reversed(sorted([3, 9, 1])))[0])', "Ordena (1, 3, 9) e inverte: o primeiro é o maior."),
           FILL("Complete para mostrar [3, 2, 1].", 'print(list(___([1, 2, 3])))', "reversed", ["sorted", "reverse", "list"], "reversed percorre de trás para frente; sorted deixaria igual."),
           CODE("Crie ultimos(lista, n) que devolve uma lista com os n últimos itens, do último para trás.",
                "def ultimos(lista, n):\n    return lista[:n]\n",
                "def ultimos(lista, n):\n    return list(reversed(lista))[:n]",
                'assert ultimos(["a", "b", "c", "d"], 2) == ["d", "c"], "ultimos([\'a\', \'b\', \'c\', \'d\'], 2) deve devolver [\'d\', \'c\']"\nassert ultimos([1, 2, 3], 3) == [3, 2, 1], "ultimos([1, 2, 3], 3) deve devolver [3, 2, 1]"',
                "list(reversed(lista)) inverte, e [:n] pega os n primeiros da versão invertida.")]),
        # lição 6
        L("Desafio: espelho",
          "Inverter letras e palavras é clássico em jogos de palavras. Para inverter a ORDEM das palavras, separe com split(), use reversed e junte de novo com \" \".join().",
          'frase = "eu gosto de python"\nprint(" ".join(reversed(frase.split())))\nprint("".join(reversed(frase)))',
          [OUT('print(" ".join(reversed("a b c".split())))', ["a b c", "cba", "c  b  a"], "split dá ['a', 'b', 'c']; invertido e juntado com espaço: c b a."),
           MC('O que " ".join(reversed("bom dia".split())) devolve?', '"dia bom"', ['"aid mob"', '"mob aid"', '["dia", "bom"]'], "Inverte a ordem das palavras, não as letras."),
           TYPE('print("".join(reversed(str(1234))))', "str() vira texto, aí dá para inverter os dígitos."),
           CODE('Crie inverter_palavras(frase) que devolve a frase com cada palavra escrita de trás para frente, mas mantendo a ordem das palavras. Ex.: "oi pipo" vira "io opip".',
                'def inverter_palavras(frase):\n    return "".join(reversed(frase))\n',
                'def inverter_palavras(frase):\n    novas = []\n    for p in frase.split():\n        novas.append("".join(reversed(p)))\n    return " ".join(novas)',
                'assert inverter_palavras("oi pipo") == "io opip", "inverter_palavras(\'oi pipo\') deve devolver \'io opip\'"\nassert inverter_palavras("bom dia") == "mob aid", "inverter_palavras(\'bom dia\') deve devolver \'mob aid\'"',
                'Separe com split(), inverta cada palavra com "".join(reversed(p)) e junte tudo com " ".join().')]),
    ],

    # ================================================================ enumerate
    "enumerate": [
        # lição 2
        L("Começando de outro número",
          "Por padrão a contagem começa em 0. Com start=1, ou só um segundo argumento como enumerate(l, 1), ela começa onde você quiser. O start só muda o número, não os itens.",
          'tarefas = ["lavar", "estudar", "jogar"]\nfor n, t in enumerate(tarefas, start=1):\n    print(f"{n}. {t}")\nprint(list(enumerate("xy", 10)))',
          [OUT('print(list(enumerate(["a", "b"], 5)))', ["[(0, 'a'), (1, 'b')]", "[(5, 'a'), (5, 'b')]", "[('a', 5), ('b', 6)]"], "Começa no 5 e vai somando 1: 5 e 6."),
           TYPE('for i, c in enumerate("abc", start=1):\n    pass\nprint(i)', "Depois do laço, i guarda o último número: 3."),
           FILL("Complete para numerar a partir de 1.", 'for n, nome in enumerate(["Ana", "Bia"], ___):\n    print(n, nome)', "start=1", ["begin=1", "first=1", "1, 2"], "O parâmetro se chama start."),
           MC("Em enumerate(l, start=1), o primeiro item da lista…", "continua sendo l[0], só ganha o número 1", ["é pulado", "vira l[1]", "aparece duas vezes"], "start muda só a contagem, nenhum item é pulado.")]),
        # lição 3
        L("Menus e posições",
          "enumerate brilha em menus, rankings e quando você precisa saber ONDE está um item. Dentro do laço, guarde o índice quando o item for o que você procura.",
          'menu = ["Pizza", "Suco", "Bolo"]\nfor n, item in enumerate(menu, 1):\n    print(f"[{n}] {item}")\nnotas = [7, 10, 8, 10]\nposicoes = []\nfor i, nota in enumerate(notas):\n    if nota == 10:\n        posicoes.append(i)\nprint(posicoes)',
          [OUT('for i, x in enumerate([4, 0, 4]):\n    if x == 4:\n        print(i, end="")', ["44", "13", "4"], "O 4 aparece nos índices 0 e 2."),
           TYPE('podio = ["Ana", "Bia", "Caio"]\nfor pos, nome in enumerate(podio, 1):\n    if nome == "Bia":\n        print(f"{pos}º lugar")', "Contando a partir de 1, Bia é a segunda."),
           ORDER("Monte o programa que mostra um menu numerado a partir de 1.",
                 ['opcoes = ["Jogar", "Sair"]', 'for n, op in enumerate(opcoes, 1):', '    print(n, op)'],
                 "A lista vem antes do laço, e o print fica dentro dele."),
           CODE("Crie posicoes(lista, alvo) que devolve uma lista com todos os índices onde alvo aparece.",
                "def posicoes(lista, alvo):\n    return []\n",
                "def posicoes(lista, alvo):\n    achados = []\n    for i, item in enumerate(lista):\n        if item == alvo:\n            achados.append(i)\n    return achados",
                'assert posicoes(["a", "b", "a"], "a") == [0, 2], "posicoes([\'a\', \'b\', \'a\'], \'a\') deve devolver [0, 2]"\nassert posicoes([1, 2, 3], 9) == [], "Se o alvo não aparece, devolva []"',
                "Percorra com enumerate e guarde o i sempre que item == alvo.")]),
        # lição 4
        L("Pegadinhas do enumerate",
          "A ordem é (índice, item): trocar os nomes das variáveis troca tudo. Com uma variável só, cada volta recebe a tupla inteira. E mudar a variável do item não muda a lista: para isso, use lista[i] = ...",
          'frutas = ["uva", "kiwi"]\nfor par in enumerate(frutas):\n    print(par)\nfor i, f in enumerate(frutas):\n    frutas[i] = f.upper()\nprint(frutas)',
          [OUT('for item, i in enumerate(["x", "y"]):\n    print(item, end="")', ["xy", "x0y1", "0x1y"], "O primeiro nome recebe sempre o índice, mesmo se chamado de item."),
           OUT('for p in enumerate("ok"):\n    print(p[1], end="")', ["01", "(0, 'o')(1, 'k')", "Erro"], "p é a tupla (índice, letra); p[1] é a letra."),
           OUT('n = [1, 2]\nfor i, x in enumerate(n):\n    x = x * 10\nprint(n)', ["[10, 20]", "[0, 10]", "Erro"], "Mudar x não mexe na lista."),
           MC("Em for i, item in enumerate(l), como dobrar cada número DENTRO da lista?", "l[i] = item * 2", ["item = item * 2", "i = item * 2", "enumerate(l) * 2"], "Só com o índice dá para trocar o item na lista.")]),
        # lição 5
        L("Combinando com enumerate",
          "dict(enumerate(l)) cria um dicionário índice → item. enumerate(zip(a, b)) numera pares; para desempacotar, use parênteses: for i, (x, y) in ...",
          'print(dict(enumerate(["zero", "um"])))\nnomes = ["Ana", "Bia"]\nidades = [20, 31]\nfor i, (n, idade) in enumerate(zip(nomes, idades), 1):\n    print(i, n, idade)',
          [TYPE('print(dict(enumerate("ab", 1)))', "Os números viram chaves e as letras, valores."),
           OUT('d = {"pão": 3, "leite": 5}\nprint(list(enumerate(d)))', ["[(0, 3), (1, 5)]", "[('pão', 3), ('leite', 5)]", "[(0, 'pão', 3), (1, 'leite', 5)]"], "Percorrer um dicionário entrega só as chaves."),
           FILL("Complete para desempacotar o índice e o par.", 'for i, ___ in enumerate(zip("ab", [1, 2])):\n    print(i, letra, num)', "(letra, num)", ["letra, num", "[letra]", "letra"], "Cada volta entrega (i, (letra, num)): o par precisa de parênteses."),
           CODE('Crie numerar(linhas) que recebe uma lista de textos e devolve uma NOVA lista com cada texto precedido do número da linha, começando em 1, assim: "1: oi".',
                "def numerar(linhas):\n    return linhas\n",
                'def numerar(linhas):\n    novas = []\n    for n, t in enumerate(linhas, 1):\n        novas.append(f"{n}: {t}")\n    return novas',
                'assert numerar(["oi", "tchau"]) == ["1: oi", "2: tchau"], "numerar([\'oi\', \'tchau\']) deve devolver [\'1: oi\', \'2: tchau\']"\nassert numerar([]) == [], "Lista vazia devolve lista vazia"',
                'Use enumerate(linhas, 1) e monte cada texto com f"{n}: {t}".')]),
        # lição 6
        L("Desafio: onde está o menor?",
          "Às vezes você precisa do valor E da posição. Percorra com enumerate guardando o índice do melhor até agora: compare os itens, mas guarde o índice.",
          'temps = [22, 31, 27]\nmaior_i = 0\nfor i, t in enumerate(temps):\n    if t > temps[maior_i]:\n        maior_i = i\nprint("Dia mais quente:", maior_i + 1)',
          [OUT('print(list(enumerate([])))', ["[(0,)]", "None", "Erro"], "Sem itens, não há pares: lista vazia."),
           MC("max(enumerate(notas), key=lambda p: p[1]) devolve…", "O par (índice, nota) com a maior nota", ["Só a maior nota", "O maior índice", "Erro"], "max compara pelas notas, mas devolve o par inteiro."),
           TYPE('l = [3, 8, 5]\nprint(max(enumerate(l), key=lambda p: p[1])[0])', "O maior é 8, que está no índice 1."),
           CODE("Crie indice_do_menor(lista) que devolve o ÍNDICE do menor número da lista (no empate, o primeiro). Use enumerate.",
                "def indice_do_menor(lista):\n    return min(lista)\n",
                "def indice_do_menor(lista):\n    melhor = 0\n    for i, x in enumerate(lista):\n        if x < lista[melhor]:\n            melhor = i\n    return melhor",
                'assert indice_do_menor([5, 2, 8]) == 1, "Em [5, 2, 8] o menor (2) está no índice 1"\nassert indice_do_menor([4, 1, 1]) == 1, "No empate, devolva o primeiro índice"\nassert indice_do_menor([0, 3]) == 0, "Em [0, 3] o menor está no índice 0"',
                "Comece com melhor = 0 e troque quando achar um x menor que lista[melhor].")]),
    ],

    # ================================================================ zip
    "zip": [
        # lição 2
        L("Três listas e strict",
          "zip aceita quantas coleções você quiser: cada volta entrega uma tupla com um item de cada. Com tamanhos diferentes, ele para na menor sem avisar. Com strict=True, ele dá ValueError nesse caso.",
          'nomes = ["Ana", "Bia"]\nidades = [20, 31]\ncidades = ["Rio", "Recife"]\nfor trio in zip(nomes, idades, cidades):\n    print(trio)\ntry:\n    list(zip([1, 2], [3], strict=True))\nexcept ValueError as e:\n    print(type(e).__name__)',
          [OUT('print(list(zip("ab", "cd", "ef")))', ["['ace', 'bdf']", "[('a', 'b'), ('c', 'd'), ('e', 'f')]", "Erro"], "Cada tupla tem um item de cada texto: a, c, e e depois b, d, f."),
           TYPE('print(list(zip([1, 2, 3], "xy")))', "Para no 2º par, porque \"xy\" só tem 2 letras."),
           MC("O que strict=True faz no zip?", "Dá erro se os tamanhos forem diferentes", ["Ordena os itens", "Completa com None", "Aceita só listas"], "Ajuda a não perder dados sem perceber."),
           FILL("Complete para dar erro se as listas tiverem tamanhos diferentes.", 'a = [1, 2]\nb = [3, 4]\nprint(list(zip(a, b, ___)))', "strict=True", ["strict=False", "check=True", "safe=True"], "strict=True confere os tamanhos.")]),
        # lição 3
        L("Dicionários e contas",
          "dict(zip(chaves, valores)) monta um dicionário. Num for, zip ajuda a fazer contas item a item, como preço × quantidade. E zip(l, l[1:]) pareia cada item com o seguinte.",
          'produtos = ["pão", "leite"]\nprecos = [1.5, 4.0]\nqtds = [4, 2]\nprint(dict(zip(produtos, precos)))\ntotal = 0\nfor p, q in zip(precos, qtds):\n    total += p * q\nprint(total)\nl = [1, 4, 9]\nprint(list(zip(l, l[1:])))',
          [TYPE('print(dict(zip(["a", "b"], [1, 2])))', "A primeira lista vira as chaves, a segunda, os valores."),
           OUT('l = [10, 13, 20]\nprint([b - a for a, b in zip(l, l[1:])])', ["[10, 13, 20]", "[3, 7, 20]", "[13, 20]"], "Pares (10, 13) e (13, 20): as diferenças são 3 e 7."),
           MC("Para somar preço × quantidade de cada produto, qual laço usar?", "for p, q in zip(precos, qtds):", ["for p in precos and qtds:", "for p, q in precos, qtds:", "for p, q in zip(precos * qtds):"], "zip anda nas duas listas juntas."),
           CODE("Crie total_compra(precos, qtds) que devolve o total da compra: a soma de preço × quantidade de cada item.",
                "def total_compra(precos, qtds):\n    return sum(precos)\n",
                "def total_compra(precos, qtds):\n    total = 0\n    for p, q in zip(precos, qtds):\n        total += p * q\n    return total",
                'assert total_compra([2, 5], [3, 1]) == 11, "total_compra([2, 5], [3, 1]) deve dar 11 (2×3 + 5×1)"\nassert total_compra([10], [0]) == 0, "Quantidade 0 não soma nada"',
                "Percorra com zip(precos, qtds) e some p * q em cada volta.")]),
        # lição 4
        L("Pegadinhas do zip",
          "zip devolve um iterador: depois de usado uma vez, fica vazio. Ele também corta a sobra da coleção maior em silêncio, o que pode esconder dados perdidos. E dá para desfazer um zip com zip(*pares).",
          'z = zip([1, 2], ["a", "b"])\nprint(list(z))\nprint(list(z))\npares = [("Ana", 8), ("Bia", 9)]\nnomes, notas = zip(*pares)\nprint(nomes)\nprint(notas)',
          [OUT('z = zip("ab", "cd")\nprint(len(list(z)), len(list(z)))', ["2 2", "4 0", "Erro"], "O primeiro list() gasta o zip; o segundo fica vazio."),
           OUT('nomes = ["Ana", "Bia", "Caio"]\nnotas = [9, 7]\nprint(dict(zip(nomes, notas)))', ["{'Ana': 9, 'Bia': 7, 'Caio': None}", "Erro", "{'Ana': 9, 'Bia': 7, 'Caio': 0}"], "Caio fica de fora: zip para na menor, sem avisar."),
           TYPE('a, b = zip(("x", 1), ("y", 2))\nprint(a)', "zip junta os primeiros itens de cada tupla: x e y."),
           MC("Por que print(zip([1], [2])) não mostra os pares?", "zip devolve um iterador; use list() para ver", ["Porque dá erro", "Porque falta strict=True", "Porque zip só funciona dentro de for"], "O iterador só entrega os pares quando alguém pede.")]),
        # lição 5
        L("Combinando com zip",
          "zip combina com sum, max e sorted. sum(a * b for a, b in zip(x, y)) soma os produtos. max(zip(pontos, nomes)) acha o par com mais pontos, porque tuplas comparam o primeiro item.",
          'nomes = ["Ana", "Bia", "Caio"]\npontos = [30, 50, 40]\nprint(max(zip(pontos, nomes)))\nprint(sorted(zip(pontos, nomes), reverse=True))\nnotas = [8, 6]\npesos = [2, 3]\nprint(sum(n * p for n, p in zip(notas, pesos)) / sum(pesos))',
          [TYPE('print(max(zip([3, 9, 5], "abc")))', "O maior primeiro item é 9, que anda com a letra b."),
           OUT('print(sorted(zip([2, 1], ["b", "a"])))', ["[(2, 'b'), (1, 'a')]", "[(1, 'b'), (2, 'a')]", "[1, 2, 'a', 'b']"], "Ordena os pares pelo número, e cada letra vai junto."),
           OUT('print(sum(a * b for a, b in zip([1, 2], [3, 4])))', ["10", "21", "[3, 8]"], "1×3 + 2×4 = 3 + 8."),
           ORDER("Monte o programa que mostra quem fez mais pontos.",
                 ['pontos = [7, 9]', 'pares = zip(pontos, ["Ana", "Bia"])', 'melhor = max(pares)', 'print(melhor[1])'],
                 "Crie os pares com o número primeiro, ache o maior e mostre o nome.")]),
        # lição 6
        L("Desafio: gabarito",
          "Corrigir uma prova de múltipla escolha é perfeito para zip: compare a resposta do aluno com o gabarito, questão por questão, e conte os acertos.",
          'gabarito = ["a", "c", "b"]\naluno = ["a", "b", "b"]\nacertos = 0\nfor g, r in zip(gabarito, aluno):\n    if g == r:\n        acertos += 1\nprint(acertos, "acertos")',
          [OUT('print(sum(a == b for a, b in zip("abc", "abd")))', ["3", "1", "Erro"], "a e b batem, c e d não. True conta como 1."),
           TYPE('print([a + b for a, b in zip("pa", "ão")])', "Junta p com ã e a com o."),
           MC("Qual destas monta um dicionário questão → resposta, com questões 1, 2 e 3?", "dict(zip(range(1, 4), respostas))", ["dict(respostas, range(1, 4))", "zip(dict(respostas))", "dict(range(1, 4) + respostas)"], "zip pareia número e resposta; dict monta."),
           CODE("Crie corrigir(gabarito, respostas) que devolve a nota: quantas respostas são iguais ao gabarito, na mesma posição.",
                "def corrigir(gabarito, respostas):\n    return 0\n",
                "def corrigir(gabarito, respostas):\n    acertos = 0\n    for g, r in zip(gabarito, respostas):\n        if g == r:\n            acertos += 1\n    return acertos",
                'assert corrigir(["a", "b", "c"], ["a", "c", "c"]) == 2, "Com gabarito a, b, c e respostas a, c, c a nota é 2"\nassert corrigir(["d"], ["d"]) == 1, "Uma resposta certa vale 1"',
                "Percorra com zip(gabarito, respostas) e conte quando g == r.")]),
    ],

    # ================================================================ map
    "map": [
        # lição 2
        L("Que funções usar",
          "map aceita qualquer função que receba um valor: funções prontas (int, str, round), métodos como str.strip, funções suas criadas com def ou uma lambda. Passe a função SEM parênteses: o map chama ela por você.",
          'def dobro(n):\n    return n * 2\n\nprint(list(map(dobro, [1, 2, 3])))\nprint(list(map(str.strip, [" oi ", "tchau  "])))\nprint(list(map(round, [1.4, 2.6])))',
          [OUT('print(list(map(str, [1, 2])))', ["[1, 2]", "'12'", "Erro"], "Cada número vira texto, e a lista mostra as aspas."),
           TYPE('def ao_quadrado(x):\n    return x * x\n\nprint(list(map(ao_quadrado, [2, 3])))', "2 × 2 e 3 × 3."),
           FILL("Complete para tirar os espaços das pontas de cada nome.", 'nomes = ["  Ana", "Bia  "]\nprint(list(map(___, nomes)))', "str.strip", ["str.strip()", "strip", "nomes.strip"], "Passe o método sem parênteses: str.strip."),
           MC("Em map(f, lista), a função f é chamada…", "Uma vez para cada item", ["Uma vez para a lista toda", "Só no primeiro item", "Duas vezes por item"], "map aplica f em cada item, um por um.")]),
        # lição 3
        L("Duas listas e textos",
          "Com duas coleções, map passa um item de cada para a função, que precisa receber dois valores. Um uso clássico: transformar \"3 7 2\" em números com map(int, texto.split()).",
          'linha = "3 7 2"\nnumeros = list(map(int, linha.split()))\nprint(numeros, sum(numeros))\nprint(list(map(lambda a, b: a + b, [1, 2], [10, 20])))\na, b = map(int, "8 5".split())\nprint(a - b)',
          [TYPE('print(sum(map(int, "4 5 6".split())))', "Cada pedaço vira número: 4 + 5 + 6."),
           OUT('print(list(map(pow, [2, 3], [3, 2])))', ["[6, 6]", "[9, 8]", "[2, 3, 3, 2]"], "pow(2, 3) = 8 e pow(3, 2) = 9."),
           MC('Qual linha transforma "10 20" nos números x = 10 e y = 20?', 'x, y = map(int, "10 20".split())', ['x, y = int("10 20")', 'x, y = map("10 20", int)', 'x, y = "10 20".split()'], "split separa e map(int, …) converte cada pedaço. Só split daria textos."),
           CODE("Crie precos_com_desconto(precos) que devolve uma lista com cada preço com 10% de desconto (preço * 0.9), arredondado com round(…, 2). Use map.",
                "def precos_com_desconto(precos):\n    return precos\n",
                "def desconto(p):\n    return round(p * 0.9, 2)\n\ndef precos_com_desconto(precos):\n    return list(map(desconto, precos))",
                'assert precos_com_desconto([10, 50]) == [9.0, 45.0], "precos_com_desconto([10, 50]) deve devolver [9.0, 45.0]"\nassert precos_com_desconto([19.9]) == [17.91], "19.9 com desconto e arredondado vira 17.91"',
                "Crie uma função que faz round(p * 0.9, 2) e use list(map(essa_funcao, precos)).")]),
        # lição 4
        L("Pegadinhas do map",
          "map(len(), lista) dá erro: com parênteses você CHAMA a função na hora. map também é preguiçoso: devolve um iterador que só calcula quando você pede e que acaba depois de percorrido uma vez. Por isso print(map(...)) não mostra os valores.",
          'm = map(len, ["oi", "olá"])\nprint(list(m))\nprint(list(m))\ntry:\n    map(len(), ["oi"])\nexcept TypeError as e:\n    print(type(e).__name__)',
          [OUT('m = map(abs, [-1, -2])\nprint(sum(m), sum(m))', ["3 3", "-3 0", "Erro"], "O primeiro sum gasta o map; o segundo soma nada."),
           MC("Por que map(len(), nomes) dá erro?", "len() é chamado na hora, sem nada para medir", ["Porque len não funciona com textos", "Porque falta list()", "Porque map só aceita lambda"], "Passe len sem parênteses."),
           TYPE('print(list(map(lambda x: x + 1, range(3))))', "0, 1 e 2, cada um mais 1."),
           OUT('nums = [1, 2]\nmap(lambda x: x * 10, nums)\nprint(nums)', ["[10, 20]", "None", "Erro"], "map não altera a lista original, e o resultado foi jogado fora.")]),
        # lição 5
        L("Combinando com map",
          "map combina com sum, max e join. \"-\".join(map(str, numeros)) junta números num texto, já que join só aceita textos. A compreensão [f(x) for x in l] faz o mesmo que list(map(f, l)): use a que ficar mais clara.",
          'nums = [3, 1, 4]\nprint("-".join(map(str, nums)))\nprint(max(map(len, ["sol", "estrela", "lua"])))\nprint(sum(map(lambda n: n * n, nums)))',
          [TYPE('print("".join(map(str, [2, 0, 2, 6])))', "Cada número vira texto e eles são colados."),
           OUT('print(max(map(len, ["pé", "mão", "olho"])))', ["olho", "3", "mão"], "max recebe os tamanhos 2, 3 e 4, então devolve o número 4."),
           FILL("Complete para mostrar 1+2+3", 'print("+".join(map(___, [1, 2, 3])))', "str", ["int", "list", "len"], "join só junta textos, então converta com str."),
           CODE("Crie soma_digitos(n) que devolve a soma dos dígitos de um inteiro positivo. Ex.: soma_digitos(472) devolve 13. Dica: str(n) e map(int, ...).",
                "def soma_digitos(n):\n    return n\n",
                "def soma_digitos(n):\n    return sum(map(int, str(n)))",
                'assert soma_digitos(472) == 13, "soma_digitos(472) deve dar 13 (4 + 7 + 2)"\nassert soma_digitos(5) == 5, "soma_digitos(5) deve dar 5"',
                "str(n) separa os dígitos, map(int, ...) converte cada um e sum soma.")]),
        # lição 6
        L("Desafio: conversor",
          "Converter várias medidas de uma vez é a cara do map: crie uma função de conversão e aplique em toda a lista.",
          'def para_fahrenheit(c):\n    return c * 9 / 5 + 32\n\ncelsius = [0, 25, 100]\nprint(list(map(para_fahrenheit, celsius)))',
          [OUT('print(list(map(lambda c: c * 1000, [1, 2.5])))', ["[1000, 2500]", "[1000, 2.5]", "[1, 2.5, 1000]"], "2.5 é decimal, então 2.5 × 1000 dá 2500.0."),
           MC("Qual destas NÃO faz o mesmo que list(map(str.upper, l))?", "l.upper()", ["[s.upper() for s in l]", "[str.upper(s) for s in l]"], "Lista não tem upper(): é preciso aplicar em cada texto."),
           TYPE('print(list(map(lambda n: n % 2 == 0, [1, 2])))', "A função devolve True ou False para cada número."),
           CODE('Crie iniciais(nomes) que devolve um texto com a primeira letra de cada nome, em maiúscula. Ex.: iniciais(["ana", "bruno"]) devolve "AB".',
                'def iniciais(nomes):\n    return ""\n',
                'def iniciais(nomes):\n    return "".join(map(lambda n: n[0].upper(), nomes))',
                'assert iniciais(["ana", "bruno"]) == "AB", "iniciais([\'ana\', \'bruno\']) deve devolver \'AB\'"\nassert iniciais(["Caio", "dani", "Eva"]) == "CDE", "iniciais([\'Caio\', \'dani\', \'Eva\']) deve devolver \'CDE\'"',
                'map(lambda n: n[0].upper(), nomes) pega a inicial de cada nome, e "".join junta tudo.')]),
    ],

    # ================================================================ filter
    "filter": [
        # lição 2
        L("Funções que dizem sim",
          "A função do filter recebe um item e responde verdadeiro ou falso. Pode ser uma função sua com def, um método como str.isupper ou uma lambda. Os itens aprovados saem na mesma ordem em que estavam.",
          'def maior_de_idade(idade):\n    return idade >= 18\n\nidades = [12, 30, 17, 45]\nprint(list(filter(maior_de_idade, idades)))\nprint(list(filter(str.isupper, ["A", "b", "C"])))',
          [OUT('print(list(filter(lambda x: x < 0, [3, -1, 0, -7])))', ["[3, 0]", "[-7, -1]", "[-1, 0, -7]"], "Passam só os negativos, na ordem original. O 0 não é menor que 0."),
           TYPE('def curta(p):\n    return len(p) <= 3\n\nprint(list(filter(curta, ["sol", "nuvem", "mar"])))', "sol e mar têm 3 letras; nuvem tem 5."),
           FILL("Complete para ficar só com os textos feitos de letras.", 'print(list(filter(___, ["a1", "pipo", "42"])))', "str.isalpha", ["str.isdigit", "str.isalpha()", "isalpha"], "str.isalpha, sem parênteses, testa cada texto."),
           MC("filter(f, lista) muda a ordem dos itens que passam?", "Não, eles saem na ordem original", ["Sim, ordena do menor ao maior", "Sim, inverte", "Depende da função"], "filter só escolhe; quem ordena é o sorted.")]),
        # lição 3
        L("Filtrando no dia a dia",
          "Use filter para separar alunos aprovados, produtos em estoque ou palavras de certo tamanho. Com dicionários, a função olha um campo, como lambda p: p[\"qtd\"] > 0.",
          'produtos = [\n    {"nome": "caneta", "qtd": 3},\n    {"nome": "lápis", "qtd": 0},\n    {"nome": "borracha", "qtd": 5},\n]\ntem = filter(lambda p: p["qtd"] > 0, produtos)\nfor p in tem:\n    print(p["nome"])',
          [TYPE('notas = [5.5, 7, 9, 4]\nprint(list(filter(lambda n: n >= 6, notas)))', "Só 7 e 9 são 6 ou mais."),
           OUT('pets = {"Rex": "cão", "Mia": "gato", "Bob": "cão"}\nprint(list(filter(lambda n: pets[n] == "cão", pets)))', ["['cão', 'cão']", "['Mia']", "[('Rex', 'cão'), ('Bob', 'cão')]"], "filter percorre as chaves (nomes) e guarda as dos cães."),
           MC("Para manter só os e-mails que têm @, qual função usar no filter?", 'lambda e: "@" in e', ['lambda e: e == "@"', 'lambda e: e.remove("@")', '"@" in e'], "A função precisa receber o e-mail e devolver True ou False."),
           CODE("Crie aprovados(notas) que recebe um dicionário {aluno: nota} e devolve a lista dos alunos com nota 7 ou mais, na ordem do dicionário. Use filter.",
                "def aprovados(notas):\n    return list(notas)\n",
                "def aprovados(notas):\n    return list(filter(lambda a: notas[a] >= 7, notas))",
                'assert aprovados({"Ana": 8, "Bia": 5, "Caio": 7}) == ["Ana", "Caio"], "Ana (8) e Caio (7) passam; Bia (5) não"\nassert aprovados({"Leo": 3}) == [], "Se ninguém passa, devolva []"',
                "filter(lambda a: notas[a] >= 7, notas) percorre os nomes e olha a nota de cada um.")]),
        # lição 4
        L("Pegadinhas do filter",
          "filter MANTÉM os itens aprovados (não remove). Se a sua função esquecer o return, ela devolve None, que é falso, e nada passa. filter(None, l) tira o 0 também, não só o None. E, como o map, filter devolve um iterador que acaba depois de usado.",
          'def par(n):\n    n % 2 == 0\n\nprint(list(filter(par, [1, 2, 4])))\nprint(list(filter(None, [0, 5, None, 3])))\nf = filter(None, [1, 2])\nprint(list(f), list(f))',
          [OUT('print(list(filter(None, [0, 1, 2, None])))', ["[0, 1, 2]", "[None]", "[0, 1, 2, None]"], "0 e None são falsos, então os dois saem."),
           OUT('def grande(x):\n    if x > 10:\n        return True\n\nprint(list(filter(grande, [5, 20])))', ["[5]", "[]", "Erro"], "Para o 5 a função devolve None, que é falso. O 20 passa."),
           TYPE('f = filter(lambda x: x > 1, [1, 2, 3])\nprint(len(list(f)) + len(list(f)))', "O primeiro list() tem 2 itens; o segundo, nenhum."),
           MC("Quero tirar os números negativos da lista. Qual função passo ao filter?", "lambda n: n >= 0", ["lambda n: n < 0", "lambda n: -n", "lambda n: remove(n)"], "A função diz quem FICA: os que são 0 ou mais.")]),
        # lição 5
        L("Combinando com filter",
          "sum(filter(...)) soma só os aprovados, len(list(filter(...))) conta quantos passaram, e map(f, filter(g, l)) primeiro filtra e depois transforma. A compreensão [x for x in l if g(x)] faz o mesmo que list(filter(g, l)).",
          'nums = [1, 2, 3, 4, 5, 6]\npares = filter(lambda n: n % 2 == 0, nums)\nprint(sum(pares))\nprint(list(map(lambda n: n * n, filter(lambda n: n > 3, nums))))\nprint(sorted(filter(str.isalpha, ["b", "2", "a"])))',
          [TYPE('print(sum(filter(lambda x: x > 5, [3, 6, 10])))', "Passam 6 e 10."),
           OUT('print(len(list(filter(str.isdigit, "a1b22"))))', ["2", "5", "['1', '2', '2']"], "filter percorre as letras: 1, 2 e 2 são dígitos."),
           OUT('print(list(map(str.upper, filter(lambda p: len(p) > 2, ["oi", "pipo", "olá"]))))', ["['OI']", "['oi', 'PIPO', 'OLÁ']", "['pipo', 'olá']"], "Primeiro filtra (sai oi), depois deixa em maiúsculas."),
           CODE("Crie soma_dos_pares(numeros) que devolve a soma apenas dos números pares. Use filter.",
                "def soma_dos_pares(numeros):\n    return sum(numeros)\n",
                "def soma_dos_pares(numeros):\n    return sum(filter(lambda n: n % 2 == 0, numeros))",
                'assert soma_dos_pares([1, 2, 3, 4]) == 6, "soma_dos_pares([1, 2, 3, 4]) deve dar 6 (2 + 4)"\nassert soma_dos_pares([1, 3]) == 0, "Sem pares, a soma é 0"',
                "sum(filter(lambda n: n % 2 == 0, numeros)) soma só os pares.")]),
        # lição 6
        L("Desafio: senhas fortes",
          "Juntando tudo: crie uma função de teste com várias regras e use filter para separar o que passa. Aqui, senha forte tem 8 ou mais caracteres e pelo menos um dígito.",
          'def forte(s):\n    digitos = list(filter(str.isdigit, s))\n    return len(s) >= 8 and len(digitos) > 0\n\nsenhas = ["abc", "abacaxi123", "senhalonga", "pipo2026"]\nprint(list(filter(forte, senhas)))',
          [OUT('print("".join(filter(str.isalpha, "p1p0 r0x")))', ["pipo rox", "p1p0r0x", "10 0"], "Ficam só as letras: p, p, r, x. O espaço e os dígitos saem."),
           MC('O que filter(str.isdigit, "a1b2") percorre?', "Cada caractere do texto", ["O texto inteiro de uma vez", "Só os números", "As palavras do texto"], "Percorrer um texto entrega uma letra por vez."),
           TYPE('print(list(filter(lambda s: s.startswith("p"), ["pão", "uva", "pera"])))', "Só ficam as palavras que começam com p."),
           CODE("Crie senhas_fortes(senhas) que devolve uma lista só com as senhas que têm 8 ou mais caracteres E pelo menos um dígito. Use filter.",
                "def senhas_fortes(senhas):\n    return senhas\n",
                "def forte(s):\n    tem_digito = len(list(filter(str.isdigit, s))) > 0\n    return len(s) >= 8 and tem_digito\n\ndef senhas_fortes(senhas):\n    return list(filter(forte, senhas))",
                'assert senhas_fortes(["abc1", "abacaxi123", "senhalonga", "pipo2026"]) == ["abacaxi123", "pipo2026"], "Só abacaxi123 e pipo2026 têm 8+ caracteres e um dígito"\nassert senhas_fortes([]) == [], "Lista vazia devolve lista vazia"',
                "Crie uma função forte(s) com as duas regras e use list(filter(forte, senhas)).")]),
    ],
}

BUGS = r'''
@fn_sorted 2
notas = [7, 3, 9]
notas = notas.sort()
print(notas)  # esperado: [3, 7, 9]
>>> notas = sorted(notas)
!! sort() devolve None. Use sorted() para receber a lista ordenada.

@fn_sorted 2
nomes = ["Bia", "ana", "Caio"]
print(sorted(nomes))  # esperado: ['ana', 'Bia', 'Caio']
>>> print(sorted(nomes, key=str.lower))  # esperado: ['ana', 'Bia', 'Caio']
!! Maiúsculas vêm antes das minúsculas. key=str.lower ignora essa diferença.

@fn_sorted 2
pontos = [40, 90, 70]
top = sorted(pontos)[0]
print(top)  # esperado: 90
>>> top = sorted(pontos, reverse=True)[0]
!! Sem reverse=True, o primeiro item é o menor.

@fn_sorted 2
palavras = ["sol", "oi", "girassol"]
print(sorted(palavras, key=len()))
>>> print(sorted(palavras, key=len))
!! Passe a função sem parênteses: key=len.

@fn_sorted 2
idades = {"Ana": 30, "Leo": 12, "Caio": 25}
mais_novo = sorted(idades.items())[0]
print(mais_novo[0])  # esperado: Leo
>>> mais_novo = sorted(idades.items(), key=lambda p: p[1])[0]
!! Sem key, os pares são ordenados pelo nome. Ordene pela idade, p[1].

@fn_sorted 2
codigos = ["10", "9", "100"]
print(sorted(codigos))  # esperado: ['9', '10', '100']
>>> print(sorted(codigos, key=int))  # esperado: ['9', '10', '100']
!! Textos são comparados letra a letra. key=int compara como números.

@fn_reversed 2
nums = [1, 2, 3]
print(reversed(nums)[0])
>>> print(list(reversed(nums))[0])
!! reversed devolve um iterador, que não tem índice. Converta com list().

@fn_reversed 2
letras = list(reversed("roma"))
print(letras)  # esperado: amor
>>> print("".join(letras))  # esperado: amor
!! A lista mostra as letras separadas. Use "".join() para colar.

@fn_reversed 1
cores = {"azul", "verde"}
for c in reversed(cores):
    print(c)
>>> cores = ["azul", "verde"]
!! Set não tem ordem, então não dá para inverter. Use uma lista.

@fn_reversed 2
nums = [4, 5, 6]
r = reversed(nums)
print(list(r))
print(len(list(r)))  # esperado: 3
>>> r = list(reversed(nums))
!! O iterador acaba depois do primeiro uso. Guarde como lista.

@fn_reversed 2
lista = [3, 1, 2]
lista = lista.reverse()
print(lista)  # esperado: [2, 1, 3]
>>> lista = list(reversed(lista))
!! reverse() altera a lista e devolve None.

@fn_reversed 1
contagem = list(reversed(range(1, 3)))
print(contagem)  # esperado: [3, 2, 1]
>>> contagem = list(reversed(range(1, 4)))
!! O fim do range não entra. Para incluir o 3, use range(1, 4).

@fn_enumerate 2
frutas = ["uva", "kiwi"]
for fruta, i in enumerate(frutas):
    print(i, fruta)  # esperado: 1 kiwi
>>> for i, fruta in enumerate(frutas):
!! enumerate entrega (índice, item), nessa ordem.

@fn_enumerate 2
menu = ["Pizza", "Suco"]
for n, item in enumerate(menu):
    print(f"{n}. {item}")  # esperado: 2. Suco
>>> for n, item in enumerate(menu, 1):
!! Para contar a partir de 1, passe start=1.

@fn_enumerate 3
nomes = ["Ana", "Bia"]
idades = [20, 31]
for nome, idade in enumerate(nomes, idades):
    print(nome, idade)
>>> for nome, idade in zip(nomes, idades):
!! enumerate não junta duas listas. Para andar nas duas, use zip.

@fn_enumerate 3
notas = [5, 8]
for i, n in enumerate(notas):
    n = n + 1
print(notas)  # esperado: [6, 9]
>>> notas[i] = n + 1
!! Mudar n não muda a lista. Use o índice: notas[i].

@fn_enumerate 2
cores = ["azul", "rosa"]
for i, cor in enumerate(len(cores)):
    print(i, cor)
>>> for i, cor in enumerate(cores):
!! enumerate precisa da lista, não do tamanho dela.

@fn_enumerate 2
letras = "abc"
for i in enumerate(letras):
    print(i + 1)
>>> for i, letra in enumerate(letras):
!! Com uma variável só, i é a tupla (índice, letra). Desempacote em duas.

@fn_zip 3
nomes = ["Ana", "Bia"]
notas = [8, 9]
for nome, nota in zip(nomes):
    print(nome, nota)
>>> for nome, nota in zip(nomes, notas):
!! Faltou passar a segunda lista para o zip.

@fn_zip 3
chaves = ["a", "b"]
valores = [1, 2]
d = zip(chaves, valores)
print(d["a"])
>>> d = dict(zip(chaves, valores))
!! zip só faz os pares. Para usar d["a"], transforme em dicionário.

@fn_zip 2
produtos = ["pão", "leite", "café"]
precos = [2, 5]
tabela = dict(zip(produtos, precos))
print(len(tabela))  # esperado: 3
>>> precos = [2, 5, 9]
!! Faltou o preço do café, e o zip cortou ele sem avisar.

@fn_zip 3
a = [1, 2]
b = [3, 4]
pares = zip(a, b)
print(list(pares))
print(len(list(pares)))  # esperado: 2
>>> pares = list(zip(a, b))
!! O zip acaba depois do primeiro uso. Guarde como lista.

@fn_zip 3
precos = [10, 4]
qtds = [2, 3]
total = sum(zip(precos, qtds))
print(total)  # esperado: 32
>>> total = sum(p * q for p, q in zip(precos, qtds))
!! zip dá pares, e não dá para somar pares. Multiplique cada par antes.

@fn_zip 3
nomes = ["Zeca", "Bia"]
pontos = [7, 9]
melhor = max(zip(nomes, pontos))
print(melhor[0])  # esperado: Bia
>>> melhor = max(zip(nomes, pontos), key=lambda p: p[1])
!! Sem key, max compara os nomes primeiro. Compare pelos pontos.

@fn_map 2
textos = ["1", "2", "3"]
nums = map(int(), textos)
print(list(nums))
>>> nums = map(int, textos)
!! Passe int sem parênteses: o map chama a função para você.

@fn_map 2
nums = [1, 2, 3]
dobros = map(lambda n: n * 2, nums)
print(dobros[0])
>>> dobros = list(map(lambda n: n * 2, nums))
!! map devolve um iterador, que não tem índice. Converta com list().

@fn_map 2
idades = "18 25 30".split()
print(sum(idades))
>>> print(sum(map(int, idades)))
!! split devolve textos. Converta com map(int, ...) antes de somar.

@fn_map 2
nums = [3, 1, 2]
print("-".join(map(int, nums)))
>>> print("-".join(map(str, nums)))
!! join só junta textos. Converta com str, não com int.

@fn_map 2
def dobro(n):
    n * 2

print(list(map(dobro, [1, 2])))  # esperado: [2, 4]
>>> return n * 2
!! Sem return, a função devolve None para cada item.

@fn_map 1
m = map(len, ["oi", "olá"])
print(max(m))
print(min(m))
>>> m = list(map(len, ["oi", "olá"]))
!! O map acaba depois do max. Guarde como lista para usar de novo.

@fn_filter 2
nums = [1, 2, 3, 4]
pares = filter(nums, lambda n: n % 2 == 0)
print(list(pares))
>>> pares = filter(lambda n: n % 2 == 0, nums)
!! A função vem primeiro e a coleção depois.

@fn_filter 2
def positivo(n):
    n > 0

print(list(filter(positivo, [-1, 2, 5])))  # esperado: [2, 5]
>>> return n > 0
!! Sem return, a função devolve None, que é falso, e nada passa.

@fn_filter 2
notas = [4, 7, 9]
aprovadas = filter(lambda n: n < 6, notas)
print(list(aprovadas))  # esperado: [7, 9]
>>> aprovadas = filter(lambda n: n >= 6, notas)
!! filter mantém quem passa no teste. O teste tem de ser n >= 6.

@fn_filter 2
valores = [0, None, 7, None]
print(list(filter(None, valores)))  # esperado: [0, 7]
>>> print(list(filter(lambda v: v is not None, valores)))  # esperado: [0, 7]
!! filter(None, ...) tira o 0 também. Teste só o None.

@fn_filter 2
palavras = ["OI", "tchau", "SOS"]
gritos = filter(str.isupper(), palavras)
print(list(gritos))
>>> gritos = filter(str.isupper, palavras)
!! Passe o método sem parênteses: str.isupper.

@fn_filter 3
nums = [5, 12, 30]
grandes = filter(lambda n: n > 10, nums)
print(len(grandes))
>>> print(len(list(grandes)))
!! filter devolve um iterador, que não tem len. Converta com list().
'''
