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
    "input": [
        # lição 2 (a lição 1 já existe: input mostra a pergunta e devolve texto)
        L("Convertendo a resposta",
          "Como input sempre devolve texto, envolva-o com int() para ler inteiros ou float() para ler decimais. Assim a conversão acontece logo na leitura.",
          'idade = int(input("Idade: "))  # a pessoa digita 12\naltura = float(input("Altura: "))  # a pessoa digita 1.5\nprint(idade + 1)\nprint(altura * 2)',
          [OUT('n = int(input())  # a pessoa digita 5\nprint(n * 2)', ["55", "5", "Erro"], "Com int(), \"5\" vira 5, e 5 * 2 é 10.", entrada="5"),
           TYPE('p = float(input())  # a pessoa digita 2.5\nprint(p + 1)', "float(\"2.5\") é 2.5; somando 1 dá 3.5.", entrada="2.5"),
           FILL("Complete para transformar o texto digitado num número inteiro.", 'texto = "8"  # veio do input()\nqtd = ___(texto)\nprint(qtd + 2)', "int", ["str", "len", "input"], "int(\"8\") vira o número 8, e 8 + 2 dá 10."),
           MC("A pessoa digita 3.5 e o código faz int(input()). O que acontece?", "Dá ValueError", ["Devolve 3", "Devolve 4", "Devolve 3.5"], "int() não aceita texto com ponto. Para decimais, use float().")],
          entrada="12\n1.5"),
        # lição 3
        L("Várias perguntas",
          "Cada input lê uma resposta, na ordem em que aparece no programa. Guarde cada resposta numa variável e use todas depois.",
          'nome = input("Nome: ")  # a pessoa digita Caio\npet = input("Pet: ")  # a pessoa digita Rex\nprint(f"{nome} tem um pet chamado {pet}")',
          [OUT('a = input()  # a pessoa digita 3\nb = input()  # a pessoa digita 4\nprint(a + b)', ["7", "3 4", "Erro"], "Os dois são textos: \"3\" + \"4\" cola e dá 34.", entrada="3\n4"),
           TYPE('a = int(input())  # a pessoa digita 3\nb = int(input())  # a pessoa digita 4\nprint(a + b)', "Agora são números: 3 + 4 dá 7.", entrada="3\n4"),
           OUT('x = input()  # a pessoa digita bolo\ny = input()  # a pessoa digita suco\nprint(y, x)', ["bolo suco", "x y", "suco"], "A primeira resposta vai para x e a segunda para y; o print mostra y primeiro.", entrada="bolo\nsuco"),
           MC("Um programa tem 3 input(). Quantas vezes a pessoa aperta Enter?", "3", ["1", "Nenhuma", "Depende do print"], "Cada input espera uma resposta terminada com Enter.")],
          entrada="Caio\nRex"),
        # lição 4
        L("Cuidados com a resposta",
          "A pessoa pode digitar espaços a mais, letras maiúsculas ou só apertar Enter (aí vem o texto vazio \"\"). Use .strip() para tirar os espaços das pontas e .lower() para deixar tudo minúsculo antes de comparar.",
          'r = input("Continuar? ")  # a pessoa digita   SIM\nprint(r == "sim")\nprint(r.strip().lower() == "sim")',
          [OUT('r = input()  # a pessoa digita Sim\nprint(r == "sim")', ["True", "Sim", "Erro"], "Para o Python, S maiúsculo e s minúsculo são diferentes.", entrada="Sim"),
           TYPE('r = input()  # a pessoa só aperta Enter\nprint(len(r))', "Só Enter dá o texto vazio, que tem tamanho 0.", entrada="\n"),
           MC("A pessoa digita 3,5 e o código faz float(input()). O que acontece?", "Dá ValueError", ["Devolve 3.5", "Devolve 35.0", "Devolve 3.0"], "O Python usa ponto nos decimais. Troque a vírgula com .replace(\",\", \".\") antes."),
           CODE("Crie a função limpar(resposta) que devolve a resposta sem espaços nas pontas e em minúsculas. Ex.: limpar(\"  SIM \") devolve \"sim\".",
                "def limpar(resposta):\n    return resposta\n",
                'def limpar(resposta):\n    return resposta.strip().lower()',
                'assert limpar("  SIM ") == "sim", "Com  SIM  a função deveria devolver sim"\nassert limpar("Não") == "não", "Com Não a função deveria devolver não"',
                "strip() tira os espaços e lower() deixa minúsculo: return resposta.strip().lower()")],
          entrada="  SIM "),
        # lição 5
        L("Vários valores numa linha",
          "Quando a pessoa digita vários valores separados por espaço, .split() quebra o texto numa lista de pedaços. Depois é só converter cada pedaço com int().",
          'linha = input("Dois números: ")  # a pessoa digita 3 8\na, b = linha.split()\nprint(int(a) + int(b))',
          [OUT('partes = input().split()  # a pessoa digita 10 20 30\nprint(partes)', ["[10, 20, 30]", "10 20 30", "['10 20 30']"], "split() devolve uma lista de TEXTOS, por isso as aspas.", entrada="10 20 30"),
           TYPE('x, y = input().split()  # a pessoa digita 4 5\nprint(int(x) * int(y))', "Cada pedaço vira número, e 4 * 5 dá 20.", entrada="4 5"),
           OUT('nums = input().split(",")  # a pessoa digita 1,2,3\nprint(len(nums))', ["1", "5", "6"], "split(\",\") corta nas vírgulas: 3 pedaços.", entrada="1,2,3"),
           FILL("Complete para somar todos os números do texto.", 'linha = "2 4 6"  # veio do input()\nprint(sum(map(int, linha.___())))', "split", ["strip", "lower", "upper"], "split() separa os números, e map(int, ...) converte cada um.")],
          entrada="3 8"),
        # lição 6
        L("Desafio: cadastro rápido",
          "Juntando tudo: ler, limpar, separar e converter. Nos exercícios de código o input não funciona, então você vai escrever funções que recebem o texto que o input devolveria.",
          'linha = input("Nome e idade: ")  # a pessoa digita bia 15\nnome, idade = linha.split()\nidade = int(idade)\nprint(f"{nome.title()} faz {idade + 1} no ano que vem")',
          [OUT('r = input().strip()  # a pessoa digita   oi  \nprint(f"[{r}]")', ["[  oi  ]", "[oi  ]", "oi"], "strip() tira os espaços das duas pontas.", entrada="  oi  "),
           TYPE('a, b = input().split()  # a pessoa digita 7 2\nprint(int(a) // int(b), int(a) % int(b))', "7 // 2 dá 3 e o resto 7 % 2 dá 1.", entrada="7 2"),
           MC("Qual linha lê um preço como 9.90 do jeito certo?", 'preco = float(input("Preço: "))', ['preco = int(input("Preço: "))', 'preco = input(float("Preço: "))', 'preco = float(input)("Preço: ")'], "Primeiro o input lê o texto, depois o float converte."),
           CODE("Crie a função soma_linha(linha) que recebe um texto como \"3 4 5\" (do jeito que o input devolveria) e devolve a soma dos números (12).",
                "def soma_linha(linha):\n    return linha\n",
                'def soma_linha(linha):\n    return sum(int(p) for p in linha.split())',
                'assert soma_linha("3 4 5") == 12, "Com 3 4 5 a soma deveria dar 12"\nassert soma_linha(" 10 ") == 10, "Lembre de converter cada pedaço com int()"',
                "split() separa os pedaços e int() converte cada um antes de somar.")],
          entrada=" bia 15 "),
    ],
    "len": [
        # lição 2 (a lição 1 já existe: len com textos, listas e dicionários)
        L("len em cada tipo",
          "Em textos, len conta caracteres. Em listas e tuplas, conta itens. Em dicionários, conta as chaves. Uma lista dentro de outra conta como um item só.",
          'print(len(""))\nprint(len([[1, 2], [3]]))\nprint(len({"a": 1, "b": 2}))\nprint(len((7, 8, 9)))',
          [OUT('print(len([1, [2, 3], 4]))', ["4", "2", "1"], "A lista de dentro conta como um item: são 3."),
           TYPE('print(len({"pão": 2, "leite": 1, "ovo": 12}))', "len de dicionário conta as chaves: 3."),
           MC('Quanto vale len("")?', "0", ["1", "None", "Dá erro"], "O texto vazio não tem nenhum caractere."),
           OUT('print(len("a b"))', ["2", "1", "4"], "O espaço também é um caractere: são 3.")]),
        # lição 3
        L("len no dia a dia",
          "len ajuda a validar e a calcular: conferir o tamanho de uma senha, achar o último item (índice len - 1) e fazer médias com sum(lista) / len(lista).",
          'notas = [7, 9, 8]\nprint(sum(notas) / len(notas))\nprint(notas[len(notas) - 1])\nsenha = "gato"\nprint(len(senha) >= 6)',
          [TYPE('compras = ["arroz", "feijão", "café"]\nprint(compras[len(compras) - 1])', "len - 1 é o índice do último item."),
           OUT('gols = [2, 0, 4]\nprint(sum(gols) / len(gols))', ["2", "6", "3"], "6 / 3 dá 2.0, porque a divisão com / sempre dá float."),
           FILL("Complete para avisar se o nome tem mais de 10 letras.", 'nome = "Maximiliano"\nif ___(nome) > 10:\n    print("Nome comprido!")', "len", ["type", "print", "sum"], "len(nome) é 11, que é maior que 10."),
           CODE("Crie a função media(notas) que devolve a média da lista: a soma dividida pela quantidade de notas.",
                "def media(notas):\n    return sum(notas)\n",
                'def media(notas):\n    return sum(notas) / len(notas)',
                'assert media([8, 6, 10]) == 8, "media([8, 6, 10]) deveria dar 8"\nassert media([5]) == 5, "media([5]) deveria dar 5"',
                "return sum(notas) / len(notas)")]),
        # lição 4
        L("Pegadinhas do len",
          "len não funciona com números (int e float): dá TypeError. E o último índice é len - 1, porque os índices começam no 0; usar lista[len(lista)] dá IndexError.",
          'x = 2024\nprint(len(str(x)))\ncores = ["azul", "verde"]\nprint(cores[len(cores) - 1])',
          [MC("O que acontece com len(3.14)?", "TypeError", ["Devolve 4", "Devolve 3", "Devolve 1"], "float não tem tamanho. Para contar os caracteres, use len(str(3.14))."),
           OUT('try:\n    print([1, 2, 3][len([1, 2, 3])])\nexcept Exception as e:\n    print(type(e).__name__)', ["3", "TypeError", "None"], "len é 3, mas os índices vão de 0 a 2: o índice 3 não existe."),
           TYPE('print(len(str(-50)))', "\"-50\" tem 3 caracteres: o sinal também conta."),
           OUT('print(len("ação"))', ["6", "5", "3"], "Letras com acento contam como um caractere só: são 4.")]),
        # lição 5
        L("len com outras funções",
          "Combine len com outras ferramentas: len(texto.split()) conta palavras, len(set(lista)) conta itens sem repetição e range(len(lista)) percorre os índices.",
          'frase = "o rato roeu a roupa"\nprint(len(frase.split()))\nvotos = ["a", "b", "a", "a"]\nprint(len(set(votos)))\nfor i in range(len(votos)):\n    print(i, votos[i])',
          [TYPE('print(len("bom dia pra você".split()))', "split() separa a frase em 4 palavras."),
           OUT('print(len(set([1, 1, 2, 2, 2])))', ["5", "1", "3"], "O set tira as repetições: sobra {1, 2}."),
           ORDER("Monte o programa que mostra cada índice e o pet daquela posição.", ['pets = ["Rex", "Mia"]', 'for i in range(len(pets)):', '    print(i, pets[i])'], "range(len(pets)) gera os índices 0 e 1."),
           CODE("Crie a função conta_palavras(frase) que devolve quantas palavras a frase tem.",
                "def conta_palavras(frase):\n    return len(frase)\n",
                'def conta_palavras(frase):\n    return len(frase.split())',
                'assert conta_palavras("eu gosto de python") == 4, "Deveria contar 4 palavras"\nassert conta_palavras("oi") == 1, "A frase oi tem 1 palavra"',
                "len(frase) conta letras; len(frase.split()) conta palavras.")]),
        # lição 6
        L("Desafio: validador",
          "len é a base de muitas validações: tamanho mínimo, campos vazios e limites de caracteres, como num cadastro de site ou numa rede social.",
          'usuario = "ana_22"\nbio = ""\nprint(3 <= len(usuario) <= 15)\nprint(len(bio) == 0)',
          [OUT('post = "a" * 300\nprint(len(post) > 280)', ["False", "300", "280"], "300 é maior que 280, então dá True."),
           TYPE('print(len([]) + len("") + len({}))', "Tudo vazio: 0 + 0 + 0."),
           MC("Qual condição confere se a lista tarefas está vazia?", "len(tarefas) == 0", ["len(tarefas) == None", "tarefas.len() == 0", "len[tarefas] == 0"], "len vem antes, com parênteses: len(tarefas)."),
           CODE("Crie a função senha_ok(senha) que devolve True se a senha tiver pelo menos 8 caracteres e False se não tiver.",
                "def senha_ok(senha):\n    return True\n",
                'def senha_ok(senha):\n    return len(senha) >= 8',
                'assert senha_ok("abc") is False, "abc tem só 3 caracteres"\nassert senha_ok("12345678") is True, "8 caracteres já valem"\nassert senha_ok("supersegura") is True, "supersegura deveria passar"',
                "return len(senha) >= 8")]),
    ],
    "type": [
        # lição 2 (a lição 1 já existe: type de int, str, float e .__name__)
        L("Tipos das coleções",
          "type também revela coleções: list, tuple, dict e set. Atenção: {} vazio é dict, e (5) é só um número; a tupla de um item precisa da vírgula: (5,). O valor None é do tipo NoneType.",
          'print(type({}).__name__)\nprint(type((5)).__name__)\nprint(type((5,)).__name__)\nprint(type(None).__name__)',
          [OUT('print(type({1, 2}).__name__)', ["dict", "list", "tuple"], "Chaves com valores soltos (sem dois-pontos) formam um set."),
           TYPE('print(type({"a": 1}).__name__)', "Pares chave: valor formam um dicionário."),
           MC("Qual destes cria uma tupla de um item?", "(7,)", ["(7)", "[7]", "{7}"], "Sem a vírgula, (7) é só o número 7."),
           OUT('print(type(range(3)).__name__)', ["list", "tuple", "int"], "range tem um tipo só dele: range.")]),
        # lição 3
        L("Comparando tipos",
          "Dá para comparar o resultado de type com o tipo, escrito sem aspas: type(x) == int. Assim o programa decide o que fazer conforme o tipo do valor.",
          'x = 3.5\nif type(x) == float:\n    print("decimal")\nprint(type("oi") == str)\nprint(type(10) == float)',
          [TYPE('print(type([1, 2]) == list)', "[1, 2] é uma lista, então a comparação dá True."),
           OUT('v = "42"\nif type(v) == int:\n    print("número")\nelse:\n    print("texto")', ["número", "42", "Erro"], "\"42\" entre aspas é str, então cai no else."),
           FILL("Complete para conferir se nota é um número inteiro.", 'nota = 9\nprint(type(nota) == ___)', "int", ['"int"', "float", "number"], "Compare com o tipo int, sem aspas."),
           MC('O que type(5) == "int" devolve?', "False", ["True", "int", "Dá erro"], "Do lado direito há um texto, não o tipo int. Um tipo nunca é igual a um texto.")]),
        # lição 4
        L("Pegadinhas de tipo",
          "Alguns resultados surpreendem: True é bool (e não int), a divisão com / sempre dá float e um número entre aspas continua sendo str. Na dúvida, pergunte ao type.",
          'print(type(True).__name__)\nprint(type(6 / 2).__name__)\nprint(type(6 // 2).__name__)\nprint(type("6").__name__)',
          [OUT('print(type(1 == 1).__name__)', ["int", "str", "True"], "Uma comparação dá True ou False, que são do tipo bool."),
           TYPE('print(type(2 * 1.0).__name__)', "int vezes float dá float."),
           OUT('print(type(-0).__name__, type("-0").__name__)', ["int int", "str str", "float str"], "O primeiro é número; o segundo, entre aspas, é texto."),
           CODE("A função tipo_de(valor) deve devolver o NOME do tipo como texto. Ex.: tipo_de(3) devolve \"int\". Corrija-a.",
                "def tipo_de(valor):\n    return type(valor)\n",
                'def tipo_de(valor):\n    return type(valor).__name__',
                'assert tipo_de(3) == "int", "tipo_de(3) deveria devolver o texto int"\nassert tipo_de("a") == "str", "Para um texto, deveria devolver str"\nassert tipo_de(None) == "NoneType", "tipo_de(None) deveria devolver NoneType"',
                "type(valor).__name__ dá o nome do tipo como texto.")]),
        # lição 5
        L("type com outras funções",
          "type(x).__name__ fica ótimo dentro de f-strings para montar relatórios. E dá para usar type num laço para tratar de jeitos diferentes os valores de uma lista misturada.",
          'itens = [3, "pão", 2.5, True]\nfor x in itens:\n    print(f"{x} -> {type(x).__name__}")',
          [TYPE('print(f"{7} é {type(7).__name__}")', "A f-string monta a frase: 7 é int."),
           OUT('dados = [1, "a", 2, "b", 3]\ntotal = 0\nfor d in dados:\n    if type(d) == int:\n        total += d\nprint(total)', ["5", "3", "Erro"], "Só os int entram na soma: 1 + 2 + 3 dá 6."),
           ORDER("Monte o programa que converte o texto em número e mostra o novo tipo.", ['texto = "12"', 'numero = int(texto)', 'print(type(numero).__name__)'], "Primeiro o texto, depois a conversão e, por fim, o type."),
           MC("Qual é o resultado de type(type(5)).__name__?", "type", ["int", "str", "class"], "O próprio int é um tipo, e o tipo de qualquer tipo é type.")]),
        # lição 6
        L("Desafio: organizador",
          "Com type você inspeciona cada valor e decide o que fazer. Isso ajuda quando uma lista mistura números e textos, como dados vindos de uma planilha.",
          'linha = ["Ana", 9, "Caio", 7.5]\nnomes = []\nfor v in linha:\n    if type(v) == str:\n        nomes.append(v)\nprint(nomes)',
          [OUT('x = 5\nx = str(x)\nprint(type(x).__name__)', ["int", "5", "float"], "Depois de str(x), x virou texto: str."),
           TYPE('print(type([]) == type([1, 2, 3]))', "As duas são listas, então os tipos são iguais."),
           MC("Qual destas expressões dá True?", "type(3.0) == float", ["type(3) == float", 'type("3") == int', "type(None) == str"], "3.0 tem ponto, então é float."),
           CODE("Crie a função soma_numeros(lista) que soma só os itens do tipo int e ignora o resto. Ex.: soma_numeros([1, \"a\", 2]) devolve 3.",
                "def soma_numeros(lista):\n    total = 0\n    return total\n",
                'def soma_numeros(lista):\n    total = 0\n    for x in lista:\n        if type(x) == int:\n            total += x\n    return total',
                'assert soma_numeros([1, "a", 2]) == 3, "Deveria somar 1 + 2 = 3"\nassert soma_numeros(["x", "y"]) == 0, "Sem números, a soma é 0"\nassert soma_numeros([5, "5", 5]) == 10, "O texto 5 não entra na soma"',
                "Percorra a lista e some só quando type(x) == int.")]),
    ],
    "help": [
        # lição 2 (a lição 1 já existe: help no terminal e a docstring em __doc__)
        L("Docstrings de várias linhas",
          "A docstring pode ter várias linhas: a primeira resume o que a função faz e as outras dão detalhes. O texto inteiro fica em __doc__, que é o que help() mostra.",
          'def area(base, altura):\n    """Calcula a área do retângulo.\n\n    base e altura são números.\n    """\n    return base * altura\n\nprint(area.__doc__.splitlines()[0])',
          [OUT('def soma(a, b):\n    """Soma a e b."""\n    return a + b\n\nprint(soma.__doc__)', ["soma", "a + b", "None"], "__doc__ guarda o texto da docstring."),
           TYPE('def latir():\n    """Faz o cachorro latir.\n    Use com moderação."""\n\nprint(latir.__doc__.splitlines()[0])', "splitlines()[0] pega só a primeira linha."),
           MC("Quantas aspas abrem uma docstring?", 'Três: """', ['Uma: "', 'Duas: ""', "Nenhuma, é um # no começo"], "Docstrings usam aspas triplas, que aceitam várias linhas."),
           FILL("Complete para mostrar a docstring da função miar.", 'def miar():\n    """Faz miau."""\n\nprint(miar.___)', "__doc__", ["doc", "__help__", "help()"], "A docstring fica no atributo __doc__.")]),
        # lição 3
        L("Ajuda dos built-ins",
          "As funções do Python também têm docstring. No terminal, help(len) ou help(str.upper) mostra a ajuda; para sair da tela, aperte q. Num programa, o mesmo texto está em __doc__.",
          'print(type(len.__doc__).__name__)\nprint(len.__doc__ is not None)\nprint(str.upper.__doc__ is not None)',
          [MC("Para ver a ajuda do método upper dos textos, você digita…", "help(str.upper)", ["help(upper)", 'help("oi".upper())', "str.help(upper)"], "Indique o método pelo tipo, str.upper, sem os parênteses de chamada."),
           MC("A tela do help() abriu no terminal. Como você sai dela?", "Apertando q", ["Digitando exit()", "Fechando o computador", "Apertando a barra de espaço"], "q (de quit) fecha a tela de ajuda."),
           OUT('print(abs.__doc__ is None)', ["True", "None", "abs"], "abs tem documentação, então __doc__ não é None: False."),
           TYPE('print(type(print.__doc__).__name__)', "A documentação é um texto: str.")]),
        # lição 4
        L("Pegadinhas do help",
          "Sem docstring, __doc__ é None. Comentários com # não viram documentação, e a docstring precisa ser a primeira linha dentro da função. E passe a função sem chamá-la: help(len), não help(len()).",
          'def a():\n    # só um comentário\n    return 1\n\ndef b():\n    x = 1\n    """Isto não é docstring."""\n\nprint(a.__doc__)\nprint(b.__doc__)',
          [OUT('def f():\n    pass\n\nprint(f.__doc__)', ["pass", "f", "Erro"], "Sem docstring, __doc__ é None."),
           MC("Por que help(len()) dá erro?", "Porque len() chama a função sem argumentos", ["Porque len não tem ajuda", "Porque help só aceita textos", "Não dá erro"], "Passe a função em si, sem parênteses: help(len)."),
           OUT('def g():\n    print("oi")\n    """Diz oi."""\n\nprint(g.__doc__)', ["Diz oi.", "oi", "Erro"], "A docstring precisa ser a primeira coisa da função. Aqui ela veio depois, então __doc__ é None."),
           CODE("A função dobro está sem documentação. Troque o comentário pela docstring Devolve o dobro de n. (com o ponto), para que dobro.__doc__ seja esse texto.",
                "def dobro(n):\n    # Devolve o dobro de n.\n    return n * 2\n",
                'def dobro(n):\n    """Devolve o dobro de n."""\n    return n * 2',
                'assert dobro.__doc__ == "Devolve o dobro de n.", "A docstring deve ser exatamente: Devolve o dobro de n."\nassert dobro(4) == 8, "dobro(4) ainda deve dar 8"',
                'Troque o comentário por """Devolve o dobro de n.""".')]),
        # lição 5
        L("Documentando de verdade",
          "Docstrings também funcionam em classes. Junto com __name__ (o nome da função), dá para montar uma listinha de ajuda do seu próprio programa.",
          'def somar(a, b):\n    """Soma dois números."""\n    return a + b\n\ndef sair():\n    """Fecha o jogo."""\n\nfor f in [somar, sair]:\n    print(f"{f.__name__}: {f.__doc__}")',
          [TYPE('def pular():\n    """Faz o boneco pular."""\n\nprint(pular.__name__)', "__name__ guarda o nome da função."),
           OUT('class Gato:\n    """Um gato de estimação."""\n\nprint(Gato.__doc__)', ["Gato", "None", "class Gato"], "Classes também têm docstring."),
           OUT('def oi():\n    """  Oi!  """\n\nprint(f"[{oi.__doc__.strip()}]")', ["[  Oi!  ]", "[oi]", "Oi!"], "strip() tira os espaços das pontas."),
           CODE("Crie a função ajuda(f) que devolve o texto <nome>: <docstring>. Ex.: para uma função pular com a docstring Pula., devolve pular: Pula.",
                "def ajuda(f):\n    return f.__name__\n",
                'def ajuda(f):\n    return f"{f.__name__}: {f.__doc__}"',
                'def pular():\n    """Pula."""\nassert ajuda(pular) == "pular: Pula.", "Esperado: pular: Pula."',
                'return f"{f.__name__}: {f.__doc__}"')]),
        # lição 6
        L("Desafio: documente tudo",
          "Bons programas explicam a si mesmos. Escreva docstrings curtas que digam O QUE a função faz; assim qualquer pessoa entende o código usando help().",
          'def converter(reais):\n    """Converte reais em centavos."""\n    return reais * 100\n\nprint(converter.__doc__)\nprint(converter(2))',
          [MC("Qual é a melhor docstring para def area(l): return l * l?", '"""Calcula a área de um quadrado de lado l."""', ['"""Função."""', '"""return l * l"""', "# área"], "Uma boa docstring diz o que a função faz, em poucas palavras."),
           TYPE('def f():\n    """A\n    B"""\n\nprint(len(f.__doc__.splitlines()))', "A docstring ocupa 2 linhas."),
           OUT('def nada():\n    """Não faz nada."""\n\nprint(nada())', ["Não faz nada.", "nada", "Erro"], "Chamar a função roda o corpo, não mostra a docstring. Sem return, ela devolve None."),
           CODE("Crie a função area_retangulo(base, altura) que devolve base * altura e tem a docstring Calcula a área do retângulo.",
                "def area_retangulo(base, altura):\n    pass\n",
                'def area_retangulo(base, altura):\n    """Calcula a área do retângulo."""\n    return base * altura',
                'assert area_retangulo(3, 4) == 12, "area_retangulo(3, 4) deveria dar 12"\nassert area_retangulo.__doc__ == "Calcula a área do retângulo.", "A docstring deve ser: Calcula a área do retângulo."',
                "Docstring na primeira linha da função e depois return base * altura.")]),
    ],
    "id": [
        # lição 2 (a lição 1 já existe: id, mesmo objeto e o operador is)
        L("is e is not",
          "a is b é o jeito curto de perguntar se id(a) == id(b), ou seja, se é o mesmo objeto. O contrário é is not. Para conferir None, use sempre is None.",
          'a = [1, 2]\nb = a\nc = [1, 2]\nprint(a is b)\nprint(a is c)\nprint(a is not c)\nx = None\nprint(x is None)',
          [OUT('a = [5]\nb = [5]\nprint(a == b, a is b)', ["True True", "False False", "False True"], "Valores iguais (==), mas objetos diferentes (is)."),
           TYPE('r = None\nprint(r is None)', "r guarda None, então is None dá True."),
           FILL("Complete para conferir se a resposta ainda não foi preenchida.", 'resposta = None\nif resposta ___ None:\n    print("vazio")', "is", ["=", "in", "has"], "Compare com None usando is."),
           MC("a is b é o mesmo que…", "id(a) == id(b)", ["a == b", "type(a) == type(b)", "len(a) == len(b)"], "is compara a identidade, que é o que id mostra.")]),
        # lição 3
        L("Cópia ou o mesmo objeto?",
          "b = a não copia a lista: as duas variáveis passam a apontar para o mesmo objeto. Para ter uma cópia de verdade (com outro id), use a.copy(), list(a) ou a[:].",
          'a = [1, 2]\nb = a\nc = a.copy()\nb.append(3)\nprint(a)\nprint(c)\nprint(c is a)',
          [OUT('x = ["pão"]\ny = x\ny.append("leite")\nprint(len(x))', ["1", "0", "Erro"], "y é o mesmo objeto que x, então x também ganhou o leite."),
           OUT('x = ["pão"]\ny = x.copy()\ny.append("leite")\nprint(len(x))', ["2", "0", "Erro"], "copy() criou outra lista, então x continua com 1 item."),
           TYPE('a = [1, 2]\nb = list(a)\nprint(a is b)', "list(a) cria uma lista nova: é outro objeto."),
           CODE("A função backup(lista) deve devolver uma CÓPIA da lista (mesmos valores, outro objeto). Corrija-a.",
                "def backup(lista):\n    return lista\n",
                'def backup(lista):\n    return lista.copy()',
                'orig = [1, 2, 3]\nb = backup(orig)\nassert b == orig, "A cópia deve ter os mesmos valores"\nassert b is not orig, "A cópia deve ser outro objeto: use copy()"',
                "return lista.copy() (ou list(lista), ou lista[:]).")]),
        # lição 4
        L("Quando o id muda",
          "Mudar a lista por dentro (append, x[0] = ...) mantém o mesmo id. Já x = x + [2] cria um objeto novo. Textos e números não mudam por dentro: toda alteração gera um objeto novo.",
          'x = [1]\nantes = id(x)\nx.append(2)\nprint(id(x) == antes)\nx = x + [3]\nprint(id(x) == antes)',
          [OUT('n = [0]\nantes = id(n)\nn[0] = 99\nprint(id(n) == antes)', ["False", "99", "Erro"], "Trocar um item muda a lista por dentro; o objeto continua o mesmo."),
           TYPE('t = "oi"\nantes = id(t)\nt = t + "!"\nprint(id(t) == antes)', "Textos não mudam por dentro: t + \"!\" cria um texto novo."),
           MC("Qual operação mantém o mesmo objeto da lista nums?", "nums.append(4)", ["nums = nums + [4]", "nums = [4]", "nums = list(nums)"], "append altera a lista por dentro; as outras criam listas novas."),
           OUT('a = [1]\nb = a\na = a + [2]\nprint(b)', ["[1, 2]", "[2]", "Erro"], "a + [2] criou uma lista nova para a; b ficou com a antiga.")]),
        # lição 5
        L("Listas dentro de listas",
          "Cuidado com [[0] * 3] * 2: o * repete o MESMO objeto, então mudar uma linha muda todas. Para linhas independentes, use um for. E funções recebem o mesmo objeto: alterar a lista lá dentro altera a de fora.",
          'grade = [[0] * 3] * 2\nprint(grade[0] is grade[1])\ncerta = [[0] * 3 for _ in range(2)]\nprint(certa[0] is certa[1])',
          [OUT('g = [[0, 0]] * 2\ng[0][0] = 1\nprint(g)', ["[[1, 0], [0, 0]]", "[[0, 0], [0, 0]]", "Erro"], "As duas linhas são o mesmo objeto, então as duas mudam."),
           OUT('def adiciona(lista):\n    lista.append("novo")\n\nitens = []\nadiciona(itens)\nprint(itens)', ["[]", "novo", "None"], "A função recebeu o mesmo objeto, então itens mudou."),
           ORDER("Monte o programa que cria um tabuleiro 2x2 com linhas independentes e marca um X.", ['tab = [["-"] * 2 for _ in range(2)]', 'tab[0][0] = "X"', 'print(tab)'], "Com o for, cada linha é um objeto diferente."),
           CODE("Crie a função mesma_lista(a, b) que devolve True se a e b forem o MESMO objeto e False se não forem (mesmo com valores iguais).",
                "def mesma_lista(a, b):\n    return a == b\n",
                'def mesma_lista(a, b):\n    return a is b',
                'x = [1]\nassert mesma_lista(x, x) is True, "x e x são o mesmo objeto"\nassert mesma_lista(x, [1]) is False, "Valores iguais, mas objetos diferentes"',
                "return a is b (ou id(a) == id(b)).")]),
        # lição 6
        L("Desafio: sem surpresas",
          "Quando uma função não deve estragar a lista original, ela trabalha numa cópia ou monta uma lista nova. Assim quem chamou continua com os valores de antes.",
          'def com_bonus(notas):\n    novas = notas.copy()\n    novas.append(10)\n    return novas\n\nminhas = [7, 8]\nprint(com_bonus(minhas))\nprint(minhas)',
          [OUT('a = [1, 2]\nb = a[:]\nb[0] = 9\nprint(a[0])', ["9", "2", "Erro"], "a[:] cria uma cópia; mudar b não mexe em a."),
           TYPE('x = [3]\ny = x\nprint(id(x) == id(y), x is y)', "É o mesmo objeto: as duas comparações dão True."),
           MC("Por que se usa x is None em vez de x == None?", "Porque is confere se é exatamente o objeto None", ["Porque == dá erro com None", "Porque is é mais curto de digitar", "Não há diferença nenhuma"], "None é um objeto único; comparar a identidade com is é o jeito recomendado."),
           CODE("Crie a função sem_negativos(lista) que devolve uma NOVA lista só com os números maiores ou iguais a 0, sem alterar a lista original.",
                "def sem_negativos(lista):\n    for x in lista[:]:\n        if x < 0:\n            lista.remove(x)\n    return lista\n",
                'def sem_negativos(lista):\n    nova = []\n    for x in lista:\n        if x >= 0:\n            nova.append(x)\n    return nova',
                'orig = [3, -1, 0, -5, 2]\nr = sem_negativos(orig)\nassert r == [3, 0, 2], "Deveria devolver [3, 0, 2]"\nassert orig == [3, -1, 0, -5, 2], "A lista original não pode mudar"\nassert r is not orig, "Devolva uma lista nova"',
                "Crie nova = [] e vá colocando nela só os números >= 0.")]),
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
@fn_input 2
idade = "17"  # veio do input()
if idade >= 18:
    print("Pode entrar")
else:
    print("Ainda não")
>>> if int(idade) >= 18:
!! input devolve texto. Converta com int() antes de comparar com número.

@fn_input 3
a = "2"  # veio do input()
b = "3"  # veio do input()
print(a + b)  # esperado: 5
>>> print(int(a) + int(b))  # esperado: 5
!! Texto + texto cola: "2" + "3" dá 23. Converta para int antes de somar.

@fn_input 2
preco = "4.50"  # veio do input()
total = int(preco) * 2
print(total)
>>> total = float(preco) * 2
!! int() não aceita texto com ponto. Para decimais, use float().

@fn_input 2
resposta = "Sim "  # veio do input()
if resposta == "sim":
    print("ok")  # esperado: ok
else:
    print("não entendi")
>>> if resposta.strip().lower() == "sim":
!! A pessoa digitou com maiúscula e espaço. Use strip() e lower() antes de comparar.

@fn_input 2
dados = "3 4"  # veio do input()
a, b = dados
print(int(a) + int(b))
>>> a, b = dados.split()
!! Sem split(), o texto é desmontado letra por letra, espaço incluído. Use dados.split().

@fn_input 2
n = "3"  # veio do input()
for i in range(n):
    print("Olá!")
>>> for i in range(int(n)):
!! range precisa de um número inteiro, não de texto. Converta com int(n).

@fn_len 2
lista = [3, 5, 8]
print(lista[len(lista)])
>>> print(lista[len(lista) - 1])
!! Os índices começam no 0: o último é len(lista) - 1.

@fn_len 2
numero = 2024
print(len(numero))
>>> print(len(str(numero)))
!! Números não têm tamanho. Converta para texto com str() antes.

@fn_len 2
notas = [8, 6, 10]
media = sum(notas) / (len(notas) - 1)
print(media)  # esperado: 8.0
>>> media = sum(notas) / len(notas)
!! A média divide pela quantidade de notas, que é len(notas), sem tirar 1.

@fn_len 2
senha = "abc"
if len(senha) > 6:
    print("Senha curta")  # esperado: Senha curta
else:
    print("Senha boa")
>>> if len(senha) < 6:
!! A senha é curta quando tem MENOS de 6 caracteres: use <.

@fn_len 2
frase = "eu amo python"
print(len(frase))  # esperado: 3
>>> print(len(frase.split()))  # esperado: 3
!! len(frase) conta caracteres. Para contar palavras, use len(frase.split()).

@fn_len 2
pets = ["Rex", "Mia", "Bob"]
for i in range(len(pets) + 1):
    print(pets[i])
>>> for i in range(len(pets)):
!! range(len(pets)) já vai de 0 até o último índice. O + 1 passa do fim da lista.

@fn_type 2
x = 5
if type(x) == "int":
    print("inteiro")  # esperado: inteiro
else:
    print("outro")
>>> if type(x) == int:
!! Compare com o tipo int, sem aspas. "int" entre aspas é só um texto.

@fn_type 1
idade = "20"
print(type(idade) == int)  # esperado: True
>>> idade = 20
!! Entre aspas, 20 é texto (str). Sem aspas, é int.

@fn_type 1
print(type("oi").name)
>>> print(type("oi").__name__)
!! O nome do tipo fica em __name__, com dois sublinhados de cada lado.

@fn_type 1
print("Tipo: " + type(5))
>>> print("Tipo: " + type(5).__name__)
!! type devolve um tipo, não um texto. Use .__name__ para juntar com +.

@fn_type 1
nota = 10 / 2
if type(nota) == int:
    print("inteira")  # esperado: inteira
else:
    print("quebrada")
>>> nota = 10 // 2
!! A divisão com / sempre dá float. Para um resultado int, use //.

@fn_type 1
tupla = (5)
print(type(tupla).__name__)  # esperado: tuple
>>> tupla = (5,)
!! Sem a vírgula, (5) é só o número 5. A tupla de um item é (5,).

@fn_help 2
def dobro(n):
    # Devolve o dobro de n.
    return n * 2
print(dobro.__doc__)  # esperado: Devolve o dobro de n.
>>> """Devolve o dobro de n."""
!! Comentário com # não vira documentação. Use aspas triplas.

@fn_help 4
def oi():
    """Diz oi."""
    print("oi")
print(oi().__doc__)  # esperado: Diz oi.
>>> print(oi.__doc__)  # esperado: Diz oi.
!! oi() chama a função, que devolve None. Use oi, sem parênteses.

@fn_help 3
def miar():
    """Faz miau."""
print(miar.doc)
>>> print(miar.__doc__)
!! O atributo da docstring é __doc__, com dois sublinhados de cada lado.

@fn_help 4
def dobro(n):
    """Devolve o dobro de n."""
    return n * 2
print(Dobro.__doc__)
>>> print(dobro.__doc__)
!! A função se chama dobro, com d minúsculo.

@fn_help 2
def media(notas):
    """Calcula a média das notas.""
    return sum(notas) / len(notas)
print(media.__doc__)
>>> """Calcula a média das notas."""
!! A docstring abriu com três aspas e fechou com duas. Feche com três.

@fn_help 2
def media(notas):
"""Calcula a média das notas."""
    return sum(notas) / len(notas)
print(media.__doc__)
>>>     """Calcula a média das notas."""
!! A docstring fica dentro da função, com o mesmo recuo do resto do corpo.

@fn_id 2
original = [1, 2, 3]
copia = original
copia.append(4)
print(original)  # esperado: [1, 2, 3]
>>> copia = original.copy()
!! copia = original não copia: é o mesmo objeto. Use original.copy().

@fn_id 1
grade = [[0] * 2] * 2
grade[0][0] = 1
print(grade)  # esperado: [[1, 0], [0, 0]]
>>> grade = [[0] * 2 for _ in range(2)]
!! O * repete a MESMA linha. Use um for para criar linhas independentes.

@fn_id 2
resposta = None
if resposta is not None:
    print("vazio")  # esperado: vazio
>>> if resposta is None:
!! Para saber se está vazio, a pergunta é is None, não is not None.

@fn_id 3
a = [1, 2]
b = [1, 2]
print(a is b)  # esperado: True
>>> print(a == b)  # esperado: True
!! is compara se é o mesmo objeto. Para comparar os valores, use ==.

@fn_id 2
def zerar(lista):
    lista = []
nums = [1, 2]
zerar(nums)
print(nums)  # esperado: []
>>> lista.clear()
!! lista = [] cria outro objeto e não mexe no de fora. clear() esvazia a lista original.

@fn_id 3
a = [1]
b = a
print(id(a) = id(b))
>>> print(id(a) == id(b))
!! Para comparar, use ==. Um = sozinho é atribuição.
'''
