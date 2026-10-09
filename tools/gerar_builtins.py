"""Trilha "71 funções embutidas" do PyPasso.

Cada função vira uma lição: cartão de conceito + exercícios. As respostas certas
dos exercícios de saída NÃO são escritas à mão: o script roda o código e usa o
resultado. Rode:  python3 tools/gerar_builtins.py
"""
import builtins, contextlib, io, json, os, random, sys, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "..", "src", "content", "builtins.json")

OFICIAIS = """abs aiter all anext any ascii bin bool breakpoint bytearray bytes callable chr classmethod compile complex
delattr dict dir divmod enumerate eval exec filter float format frozenset getattr globals hasattr hash help hex id
input int isinstance issubclass iter len list locals map max memoryview min next object oct open ord pow print
property range repr reversed round set setattr slice sorted staticmethod str sum super tuple type vars zip __import__""".split()

# ------------------------------------------------------------ helpers de autoria
def OUT(code, errados, e, entrada=""):
    return {"k": "out", "c": code, "_wrong": errados, "e": e, "_in": entrada}
def TYPE(code, e, entrada=""):
    return {"k": "type", "c": code, "e": e, "_in": entrada}
def MC(q, certo, errados, e):
    return {"k": "mc", "q": q, "o": [certo, *errados], "e": e}
def FILL(q, code, certo, errados, e):
    return {"k": "fill", "q": q, "c": code, "b": [certo, *errados], "a": [certo], "e": e}

def B(nome, sig, resumo, explica, exemplo, itens, cuidado=None, entrada=""):
    return dict(nome=nome, sig=sig, resumo=resumo, explica=explica, exemplo=exemplo, itens=itens, cuidado=cuidado, entrada=entrada)

UNITS = []
def U(titulo, desc, *lessons):
    UNITS.append((titulo, desc, list(lessons)))

# ============================================================ 1
U("Primeiros built-ins", "print, input, len, type, help e id",
  B("print", "print(*valores, sep=' ', end='\\n')", "Mostra valores na tela.",
    "Mostra tudo o que você passar, separado por espaço, e pula uma linha no fim. sep troca o separador e end troca o final.",
    'print("Olá", "Python")\nprint(1, 2, 3, sep=" - ")\nprint("sem pular", end="! ")\nprint("fim")',
    [OUT('print("a", "b", sep="")', ["a b", "a,b", "a\nb"], "sep=\"\" junta os valores sem nada no meio."),
     TYPE('print(3, 4, sep="+", end="=7")', "O separador vira + e o final vira =7."),
     MC("O que print() devolve?", "None", ["O texto mostrado", "True", "O número de caracteres"], "print só mostra; o valor devolvido é None.")]),
  B("input", "input(pergunta='')", "Lê o que a pessoa digita.",
    "Mostra a pergunta e espera a pessoa digitar e apertar Enter. O resultado é sempre texto (str).",
    'nome = input("Seu nome: ")\nprint("Oi,", nome)', entrada="Ana",
    itens=[OUT('n = input("Número: ")  # a pessoa digita 5\nprint(n * 2)', ["10", "Erro", "n2"], "input devolve texto: \"5\" * 2 repete o texto.", entrada="5"),
     MC("Para fazer contas com o que foi digitado, você deve…", "converter com int() ou float()", ["usar print()", "nada, já é número", "usar len()"], "input sempre devolve str."),
     TYPE('x = input()  # a pessoa digita 42\nprint(type(x).__name__)', "Mesmo digitando 42, o tipo é str.", entrada="42")]),
  B("len", "len(coleção)", "Conta quantos itens algo tem.",
    "Funciona com strings, listas, tuplas, dicionários, conjuntos e ranges.",
    'print(len("Python"))\nprint(len([1, 2, 3]))\nprint(len({"a": 1}))',
    [TYPE('print(len("olá mundo"))', "O espaço também conta."),
     OUT('print(len(range(2, 10)))', ["10", "9", "7"], "range(2, 10) vai de 2 a 9: 8 números."),
     MC("O que len(42) faz?", "Dá TypeError", ["Devolve 2", "Devolve 42", "Devolve 1"], "Números não têm tamanho.")]),
  B("type", "type(valor)", "Diz o tipo de um valor.",
    "Mostra a classe do valor: int, float, str, list… Ótimo para entender erros.",
    'print(type(10))\nprint(type("10"))\nprint(type(10.0))',
    [OUT('print(type([]).__name__)', ["array", "tuple", "None"], "[] é uma lista."),
     TYPE('print(type(3 / 1).__name__)', "A divisão com / sempre dá float."),
     MC("Qual destes é do tipo bool?", "True", ['"True"', "1", "None"], "\"True\" entre aspas é str.")]),
  B("help", "help(algo)", "Mostra a documentação de algo.",
    "Use no terminal (>>>) para ler a ajuda oficial de uma função, método ou módulo. Funções que você cria mostram o texto entre três aspas logo abaixo do def (a docstring).",
    'def dobro(n):\n    """Devolve o dobro de n."""\n    return n * 2\n\nprint(dobro.__doc__)',
    [OUT('def oi():\n    """Diz oi."""\n\nprint(oi.__doc__)', ["oi", "None", "def oi"], "A docstring fica em __doc__."),
     MC("Onde help() é mais útil?", "No terminal >>> para consultar uma função", ["Para corrigir erros sozinho", "Para mostrar gráficos", "Para salvar arquivos"], "help mostra a documentação."),
     FILL("Complete para ver a ajuda de len no terminal.", '___(len)', "help", ["print", "type", "dir"], "help(len) mostra a documentação de len.")]),
  B("id", "id(objeto)", "Número de identidade de um objeto.",
    "Cada objeto na memória tem um id único enquanto existe. Duas variáveis com o mesmo id apontam para o mesmo objeto.",
    'a = [1, 2]\nb = a\nc = [1, 2]\nprint(id(a) == id(b))\nprint(id(a) == id(c))',
    [OUT('x = [0]\ny = x\ny.append(1)\nprint(x)', ["[0]", "[1]", "Erro"], "x e y são o mesmo objeto (mesmo id)."),
     MC("a == b é True, mas id(a) == id(b) é False. Isso significa…", "Valores iguais, objetos diferentes", ["Erro no Python", "São o mesmo objeto", "Um deles é None"], "== compara valores; id compara identidade."),
     TYPE('a = [1]\nb = a\nprint(a is b)', "is compara identidade, como id(a) == id(b).")]),
)
# ============================================================ 2
U("Conversões de tipo", "int, float, str, bool, complex e repr",
  B("int", "int(valor, base=10)", "Converte para número inteiro.",
    "Converte textos com algarismos e corta a parte decimal de floats (sem arredondar). Com base, lê números em outras bases.",
    'print(int("42") + 1)\nprint(int(3.99))\nprint(int("ff", 16))',
    [TYPE('print(int(-2.7))', "int corta a parte decimal em direção ao zero."),
     OUT('print(int("101", 2))', ["101", "2", "1"], "\"101\" em base 2 é 5."),
     MC('O que int("3.5") faz?', "Dá ValueError", ["Devolve 3", "Devolve 4", "Devolve 3.5"], "Texto com ponto não vira int direto; use int(float(\"3.5\")).")]),
  B("float", "float(valor)", "Converte para número decimal.",
    "Converte textos e inteiros. Aceita \"inf\" e \"nan\". Use ponto como separador decimal.",
    'print(float("2.5") * 2)\nprint(float(3))\nprint(float("1e3"))',
    [TYPE('print(float("  7 "))', "Espaços nas pontas são ignorados."),
     OUT('print(0.1 + 0.2 == 0.3)', ["True", "Erro", "0.3"], "Floats têm pequenas imprecisões: 0.1 + 0.2 dá 0.30000000000000004."),
     MC('float("3,5") dá…', "ValueError", ["3.5", "35.0", "3.0"], "O Python usa ponto; troque a vírgula com replace.")]),
  B("str", "str(valor)", "Converte em texto.",
    "Qualquer valor vira texto. Útil para juntar números com strings usando +.",
    'idade = 30\nprint("Tenho " + str(idade) + " anos")\nprint(str([1, 2]))',
    [OUT('print(str(10) + str(5))', ["15", "10 5", "Erro"], "Textos com + são colados: \"10\" + \"5\"."),
     TYPE('print(len(str(12345)))', "\"12345\" tem 5 caracteres."),
     MC("Qual jeito é mais simples para montar \"Idade: 30\"?", 'f"Idade: {idade}"', ['"Idade: " + idade', "print(Idade, idade)", "str(Idade: idade)"], "f-strings convertem sozinhas.")]),
  B("bool", "bool(valor)", "Converte em True ou False.",
    "0, 0.0, \"\", [], {}, set() e None são False. Todo o resto é True.",
    'print(bool(0), bool(1))\nprint(bool(""), bool(" "))\nprint(bool([]), bool([0]))',
    [OUT('print(bool("False"))', ["False", "Erro", "None"], "É um texto com conteúdo, então é True."),
     TYPE('print(bool(None) or bool(0.0))', "Os dois são falsos."),
     MC("Qual destes é True?", "bool([0])", ["bool(0)", "bool('')", "bool({})"], "Uma lista com um item (mesmo 0) não está vazia.")]),
  B("complex", "complex(real, imaginário=0)", "Cria um número complexo.",
    "Números complexos têm parte real e imaginária. Em Python a parte imaginária usa j. Aparecem em engenharia e matemática.",
    'z = complex(3, 4)\nprint(z)\nprint(z.real, z.imag)\nprint(abs(z))',
    [OUT('print(complex(1, 1) * 2)', ["(2+1j)", "2", "Erro"], "As duas partes são multiplicadas."),
     TYPE('print((2 + 3j).imag)', "imag é a parte imaginária, como float."),
     MC("Qual letra marca a parte imaginária em Python?", "j", ["i", "k", "x"], "Python usa j, como na engenharia.")]),
  B("repr", "repr(valor)", "Mostra o valor como ele é escrito no código.",
    "Strings aparecem com aspas e caracteres especiais visíveis, como \\n. Ótimo para enxergar espaços escondidos.",
    'texto = "oi\\n"\nprint(texto)\nprint(repr(texto))',
    [OUT('print(repr("  a "))', ["a", "'a'", "  a "], "repr mostra as aspas e os espaços."),
     TYPE('print(len(repr("ab")))', "repr(\"ab\") é 'ab', com 4 caracteres."),
     MC("Para que repr() mais ajuda?", "Ver espaços e \\n escondidos no texto", ["Arredondar números", "Ler arquivos", "Ordenar listas"], "repr mostra o texto exatamente como é.")]),
)
# ============================================================ 3
U("Contas embutidas", "abs, round, pow, divmod, sum, min e max",
  B("abs", "abs(número)", "Valor absoluto: tira o sinal.",
    "Transforma negativos em positivos. Ótimo para medir distâncias e diferenças.",
    'print(abs(-5))\nprint(abs(5))\nprint(abs(3 - 10))',
    [TYPE('print(abs(-2.5) + abs(2.5))', "Os dois viram 2.5."),
     OUT('print(abs(-0))', ["-0", "Erro", "None"], "Zero não tem sinal."),
     MC("Para saber a distância entre a e b, use…", "abs(a - b)", ["a - b", "max(a, b)", "round(a - b)"], "abs ignora quem é maior.")]),
  B("round", "round(número, casas=None)", "Arredonda.",
    "Sem casas, devolve um inteiro. Com casas, mantém aquela quantidade de decimais. Empates vão para o par mais próximo.",
    'print(round(3.14159, 2))\nprint(round(7.6))\nprint(round(2.5), round(3.5))',
    [OUT('print(round(4.5))', ["5", "4.5", "Erro"], "Empate: vai para o par, 4."),
     TYPE('print(round(1234.5678, 1))', "Uma casa decimal."),
     MC("round(1250, -2) dá…", "1200", ["1300", "1250", "12.5"], "Casas negativas arredondam dezenas, centenas…; o empate vai para o par (12).")]),
  B("pow", "pow(base, expoente, módulo=None)", "Potência.",
    "pow(a, b) é o mesmo que a ** b. Com o terceiro argumento, calcula o resto da divisão da potência de forma rápida.",
    'print(pow(2, 5))\nprint(pow(9, 0.5))\nprint(pow(2, 10, 1000))',
    [TYPE('print(pow(3, 3))', "3 × 3 × 3."),
     OUT('print(pow(2, -1))', ["-2", "Erro", "0"], "Expoente negativo dá o inverso: 1/2."),
     FILL("Complete para calcular 5 ao cubo.", 'print(5 ___ 3)', "**", ["*", "^", "//"], "Em Python ^ não é potência; é **.")]),
  B("divmod", "divmod(a, b)", "Divisão inteira e resto juntos.",
    "Devolve a tupla (a // b, a % b).",
    'print(divmod(17, 5))\nhoras, minutos = divmod(135, 60)\nprint(horas, "h", minutos, "min")',
    [OUT('print(divmod(10, 3))', ["(3, 3)", "3.33", "(1, 3)"], "10 // 3 é 3 e 10 % 3 é 1."),
     TYPE('q, r = divmod(29, 7)\nprint(q * 10 + r)', "q = 4, r = 1."),
     MC("Para converter 200 segundos em minutos e segundos, use…", "divmod(200, 60)", ["round(200 / 60)", "pow(200, 60)", "abs(200 - 60)"], "Dá (3, 20).")]),
  B("sum", "sum(números, início=0)", "Soma os itens.",
    "Soma listas, tuplas, conjuntos e geradores de números. O segundo argumento é o valor inicial.",
    'print(sum([1, 2, 3]))\nprint(sum(range(101)))\nprint(sum([1, 2], 10))',
    [TYPE('print(sum(n * n for n in range(4)))', "0 + 1 + 4 + 9."),
     OUT('print(sum([]))', ["Erro", "None", "[]"], "Soma de nada é 0."),
     MC('sum(["a", "b"]) dá…', "TypeError (use \"\".join)", ['"ab"', '"a b"', "2"], "sum é para números.")]),
  B("min", "min(itens, key=None, default=…)", "O menor valor.",
    "Aceita vários argumentos ou uma coleção. key define o critério; default evita erro com coleção vazia.",
    'print(min(5, 2, 8))\nprint(min(["uva", "abacaxi", "kiwi"], key=len))\nprint(min([], default="vazio"))',
    [OUT('print(min("python"))', ["p", "y", "n"], "Com texto, compara letra a letra: h vem antes."),
     TYPE('print(min([3, -1, 2], key=abs))', "Pelo valor absoluto, -1 é o menor."),
     MC("min([]) sem default faz o quê?", "Dá ValueError", ["Devolve 0", "Devolve None", "Devolve []"], "Coleção vazia não tem menor valor.")]),
  B("max", "max(itens, key=None, default=…)", "O maior valor.",
    "Igual ao min, mas devolve o maior.",
    'print(max(5, 2, 8))\nnotas = {"Ana": 9, "Bia": 10}\nprint(max(notas, key=notas.get))',
    [TYPE('print(max(["b", "a", "c"]))', "Ordem alfabética: c é o maior."),
     OUT('print(max([1, 5], [2, 0]))', ["[1, 5]", "5", "Erro"], "Listas são comparadas item a item: 2 > 1."),
     MC('Para achar a palavra mais longa da lista p, use…', "max(p, key=len)", ["max(len(p))", "len(max(p))", "max(p)"], "key=len compara pelo tamanho.")]),
)
# ============================================================ 4
U("Coleções embutidas", "list, tuple, dict, set, frozenset e range",
  B("list", "list(coleção)", "Cria uma lista.",
    "Transforma strings, tuplas, conjuntos e ranges em lista, que pode ser alterada.",
    'print(list("abc"))\nprint(list(range(3)))\nprint(list((1, 2)))',
    [OUT('print(list("oi!"))', ["['oi!']", "['o', 'i']", "oi!"], "Cada caractere vira um item."),
     TYPE('print(len(list({1, 1, 2})))', "O conjunto já tinha tirado o repetido."),
     MC("list() sem argumentos devolve…", "[]", ["None", "Erro", "[None]"], "Uma lista vazia.")]),
  B("tuple", "tuple(coleção)", "Cria uma tupla (imutável).",
    "Como uma lista que não pode mudar. Útil para dados fixos e para devolver vários valores.",
    't = tuple([1, 2, 3])\nprint(t)\nprint(t[0])\nx, y = (10, 20)\nprint(x + y)',
    [OUT('print(type((5)).__name__)', ["tuple", "list", "str"], "Sem vírgula, (5) é só o número 5."),
     TYPE('print(len(tuple("abc")))', "Três caracteres, três itens."),
     MC("O que acontece em t[0] = 9 se t é tupla?", "TypeError", ["Troca o item", "Cria uma lista", "Nada"], "Tuplas são imutáveis.")]),
  B("dict", "dict(pares) ou dict(chave=valor)", "Cria um dicionário.",
    "Aceita argumentos nomeados, listas de pares ou zip de duas listas.",
    'print(dict(nome="Ana", idade=20))\nprint(dict([("a", 1), ("b", 2)]))\nprint(dict(zip(["x", "y"], [1, 2])))',
    [OUT('print(dict(a=1, b=2)["b"])', ["1", "b", "Erro"], "Busca pela chave b."),
     TYPE('print(len(dict(a=1, a2=2, b=3)))', "Três chaves diferentes."),
     MC('dict(zip(["a", "b"], [1, 2])) é…', '{"a": 1, "b": 2}', ['[("a", 1), ("b", 2)]', '{"a": "b"}', "Erro"], "zip pareia; dict transforma os pares.")]),
  B("set", "set(coleção)", "Cria um conjunto sem repetidos.",
    "Remove duplicados e permite operações de conjunto: | união, & interseção, - diferença.",
    'print(set([3, 1, 3, 2]))\nprint(len(set("banana")))\nprint({1, 2} & {2, 3})',
    [TYPE('print(len(set([1, 1, 1, 2])))', "Sobram 1 e 2."),
     OUT('print(sorted(set("aabbc")))', ["['a', 'a', 'b', 'b', 'c']", "aabbc", "{'a', 'b', 'c'}"], "set remove repetidos; sorted devolve lista ordenada."),
     MC("Como criar um conjunto vazio?", "set()", ["{}", "[]", "()"], "{} é um dicionário vazio.")]),
  B("frozenset", "frozenset(coleção)", "Conjunto que não pode mudar.",
    "Igual ao set, mas imutável. Por isso pode ser chave de dicionário ou item de outro conjunto.",
    'f = frozenset([1, 2, 2])\nprint(f)\nprint(2 in f)\nd = {frozenset(["a", "b"]): "par"}\nprint(d[frozenset(["b", "a"])])',
    [OUT('print(frozenset("aab") == {"a", "b"})', ["False", "Erro", "None"], "Comparado com set, vale o conteúdo."),
     MC("frozenset tem o método add()?", "Não, é imutável", ["Sim", "Só para números", "Só com 1 item"], "Para mudar, crie outro."),
     TYPE('print(len(frozenset([1, 2, 3, 3])))', "Repetidos somem.")]),
  B("range", "range(início, fim, passo)", "Sequência de números.",
    "Vai do início até antes do fim, pulando de passo em passo. Não ocupa memória com todos os números.",
    'print(list(range(5)))\nprint(list(range(1, 10, 3)))\nprint(list(range(5, 0, -2)))',
    [OUT('print(list(range(3, 6)))', ["[3, 4, 5, 6]", "[4, 5, 6]", "[3, 6]"], "O fim não entra."),
     TYPE('print(sum(range(0, 10, 2)))', "0 + 2 + 4 + 6 + 8."),
     MC("Como contar de 10 até 1?", "range(10, 0, -1)", ["range(1, 10)", "range(10, 1)", "range(-10)"], "Passo negativo conta para trás.")]),
)
# ============================================================ 5
U("Ordenar e percorrer", "sorted, reversed, enumerate, zip, map e filter",
  B("sorted", "sorted(coleção, key=None, reverse=False)", "Devolve uma cópia ordenada.",
    "Funciona com qualquer coleção e não altera a original. key escolhe o critério; reverse inverte.",
    'n = [3, 1, 2]\nprint(sorted(n))\nprint(n)\nprint(sorted(["Bia", "ana"], key=str.lower))',
    [OUT('print(sorted("cba"))', ["cba", "abc", "['c', 'b', 'a']"], "Ordena os caracteres e devolve lista."),
     TYPE('print(sorted([5, 1, 4], reverse=True)[0])', "Do maior para o menor."),
     MC("Qual a diferença entre sorted(l) e l.sort()?", "sorted cria uma lista nova; sort altera a lista", ["Nenhuma", "sort é mais lento", "sorted só funciona com números"], "sort devolve None.")]),
  B("reversed", "reversed(sequência)", "Percorre de trás para frente.",
    "Devolve um iterador. Use list() para ver como lista, ou use direto num for.",
    'print(list(reversed([1, 2, 3])))\nfor letra in reversed("abc"):\n    print(letra)',
    [OUT('print("".join(reversed("pipo")))', ["pipo", "Erro", "['o', 'p', 'i', 'p']"], "Junta as letras invertidas."),
     TYPE('print(list(reversed(range(3)))[0])', "O primeiro da lista invertida é o último original."),
     MC("reversed(lista) altera a lista?", "Não, só percorre ao contrário", ["Sim", "Só se for número", "Apaga a lista"], "Para alterar, use lista.reverse().")]),
  B("enumerate", "enumerate(coleção, start=0)", "Percorre com o índice.",
    "Entrega pares (índice, item). start define o primeiro número.",
    'for i, cor in enumerate(["azul", "verde"]):\n    print(i, cor)\nprint(list(enumerate("ab", start=1)))',
    [OUT('for i, x in enumerate("oi", 1):\n    print(i, end="")', ["01", "oi", "12oi"], "start=1: os índices são 1 e 2."),
     TYPE('print(list(enumerate([7]))[0][0])', "O primeiro índice é 0."),
     MC("Em vez de for i in range(len(l)), prefira…", "for i, item in enumerate(l)", ["for item in range(l)", "while i < l", "for i in l.len()"], "Mais legível e já traz o item.")]),
  B("zip", "zip(a, b, …, strict=False)", "Percorre coleções em paralelo.",
    "Junta o 1º com o 1º, o 2º com o 2º… Para na menor coleção.",
    'nomes = ["Ana", "Bia"]\nidades = [20, 31]\nfor n, i in zip(nomes, idades):\n    print(n, i)',
    [OUT('print(list(zip("ab", [1, 2, 3])))', ["[('a', 1), ('b', 2), (None, 3)]", "Erro", "[('ab', 1)]"], "Para na coleção menor."),
     TYPE('print(len(list(zip(range(5), range(3)))))', "A menor tem 3 itens."),
     MC("dict(zip(chaves, valores)) serve para…", "Criar um dicionário a partir de duas listas", ["Ordenar listas", "Somar listas", "Comparar listas"], "zip pareia; dict monta.")]),
  B("map", "map(função, coleção)", "Aplica uma função em cada item.",
    "Devolve um iterador com os resultados. Use list() para ver.",
    'print(list(map(int, ["1", "2", "3"])))\nprint(list(map(len, ["oi", "olá"])))\nprint(list(map(lambda x: x * 10, [1, 2])))',
    [OUT('print(list(map(str.upper, ["a", "b"])))', ["['a', 'b']", "AB", "Erro"], "upper em cada item."),
     TYPE('print(sum(map(int, "123")))', "Cada caractere vira int: 1 + 2 + 3."),
     MC("Qual compreensão equivale a list(map(f, l))?", "[f(x) for x in l]", ["[l(x) for x in f]", "[x for x in l if f]", "f(l)"], "Aplica f em cada item.")]),
  B("filter", "filter(função, coleção)", "Fica só com os itens aprovados.",
    "Mantém os itens em que a função devolve verdadeiro. Com None, tira os valores falsos.",
    'pares = filter(lambda n: n % 2 == 0, range(10))\nprint(list(pares))\nprint(list(filter(None, [0, 1, "", "a"])))',
    [OUT('print(list(filter(str.isdigit, ["1", "a", "2"])))', ["['a']", "['1', 'a', '2']", "[1, 2]"], "Só os textos que são dígitos."),
     TYPE('print(len(list(filter(lambda x: x > 2, [1, 3, 5]))))', "3 e 5 passam."),
     MC("filter(None, lista) remove…", "Os valores falsos (0, '', None…)", ["Os None apenas", "Nada", "Os números"], "None faz o filter usar o próprio valor como teste.")]),
)
# ============================================================ 6
U("Perguntas de True ou False", "all, any, callable, isinstance, issubclass e hasattr",
  B("all", "all(coleção)", "Todos são verdadeiros?",
    "True se nenhum item for falso. Coleção vazia dá True.",
    'notas = [7, 8, 9]\nprint(all(n >= 6 for n in notas))\nprint(all([1, 0, 1]))\nprint(all([]))',
    [OUT('print(all(["a", "b", ""]))', ["True", "Erro", "None"], "A string vazia é falsa."),
     TYPE('print(all(c.isalpha() for c in "Pipo"))', "Todas são letras."),
     MC("all([]) é…", "True", ["False", "None", "Erro"], "Não há nenhum item falso.")]),
  B("any", "any(coleção)", "Algum é verdadeiro?",
    "True se pelo menos um item for verdadeiro. Coleção vazia dá False.",
    'senha = "abc7"\nprint(any(c.isdigit() for c in senha))\nprint(any([0, "", None]))',
    [OUT('print(any([0, 0, 1]))', ["False", "1", "Erro"], "O 1 é verdadeiro."),
     TYPE('print(any(x > 10 for x in [3, 7, 12]))', "12 > 10."),
     MC("any([]) é…", "False", ["True", "None", "Erro"], "Não existe nenhum item verdadeiro.")]),
  B("callable", "callable(objeto)", "Dá para chamar com ()?",
    "True para funções, métodos e classes. False para números, strings e listas.",
    'def f():\n    pass\n\nprint(callable(f))\nprint(callable(print))\nprint(callable(42))',
    [OUT('print(callable("texto".upper))', ["False", "Erro", "TEXTO"], "Um método é chamável."),
     TYPE('print(callable(int))', "Classes também são chamáveis: int(\"5\")."),
     MC('Qual destes NÃO é chamável?', '"oi"', ["len", "str", "lambda: 1"], "Uma string não é função.")]),
  B("isinstance", "isinstance(objeto, tipo)", "É deste tipo?",
    "Responde True ou False. Aceita uma tupla de tipos e considera herança.",
    'print(isinstance(3, int))\nprint(isinstance(3.0, (int, float)))\nprint(isinstance("3", int))',
    [OUT('print(isinstance(True, int))', ["False", "Erro", "None"], "bool é subclasse de int."),
     TYPE('print(isinstance([], (list, tuple)))', "[] é list."),
     MC("Por que preferir isinstance a type(x) == int?", "Porque considera herança e aceita vários tipos", ["Porque é mais curto", "Porque type não existe", "Não há diferença"], "isinstance é a forma idiomática.")]),
  B("issubclass", "issubclass(classe, outra)", "Esta classe herda daquela?",
    "Compara classes (não objetos). Toda classe é subclasse de si mesma e de object.",
    'class Animal:\n    pass\n\nclass Gato(Animal):\n    pass\n\nprint(issubclass(Gato, Animal))\nprint(issubclass(Animal, Gato))\nprint(issubclass(bool, int))',
    [OUT('class A: pass\nclass B(A): pass\nclass C(B): pass\nprint(issubclass(C, A))', ["False", "Erro", "None"], "Herança passa de geração em geração."),
     TYPE('print(issubclass(int, object))', "Tudo em Python herda de object."),
     MC("issubclass(Gato(), Animal) dá…", "TypeError: precisa da classe, não do objeto", ["True", "False", "None"], "Para objetos, use isinstance.")]),
  B("hasattr", "hasattr(objeto, 'nome')", "Tem este atributo ou método?",
    "Responde se o objeto possui algo com aquele nome.",
    'print(hasattr("texto", "upper"))\nprint(hasattr([1, 2], "append"))\nprint(hasattr(42, "append"))',
    [OUT('print(hasattr({}, "keys"))', ["False", "Erro", "keys"], "Dicionários têm keys()."),
     TYPE('print(hasattr("x", "push"))', "Strings não têm push."),
     MC("O nome do atributo em hasattr vai como…", "Texto entre aspas", ["Variável sem aspas", "Número", "Lista"], 'hasattr(obj, "nome").')]),
)
# ============================================================ 7
U("Caracteres e bases", "chr, ord, bin, oct, hex, ascii e format",
  B("ord", "ord(caractere)", "Código numérico de um caractere.",
    "Cada caractere tem um número no padrão Unicode. ord mostra esse número.",
    'print(ord("A"))\nprint(ord("a"))\nprint(ord("é"))',
    [TYPE('print(ord("B") - ord("A"))', "B vem logo depois de A."),
     OUT('print(ord("0"))', ["0", "Erro", "1"], "O caractere \"0\" tem código 48."),
     MC('ord("ab") dá…', "TypeError: espera um único caractere", ["195", "97", "[97, 98]"], "ord recebe exatamente 1 caractere.")]),
  B("chr", "chr(código)", "Caractere a partir do código.",
    "O contrário do ord: transforma o número Unicode no caractere.",
    'print(chr(65))\nprint(chr(97 + 2))\nprint(chr(128013))',
    [TYPE('print(chr(ord("a") + 1))', "A letra seguinte a a."),
     OUT('print("".join(chr(c) for c in [80, 121]))', ["80121", "Erro", "['P', 'y']"], "80 é P e 121 é y."),
     MC("chr e ord são…", "Funções inversas", ["Iguais", "Só para números", "Para arquivos"], "chr(ord(x)) == x.")]),
  B("bin", "bin(inteiro)", "Número em binário (texto).",
    "Mostra o número na base 2, com o prefixo 0b.",
    'print(bin(5))\nprint(bin(255))\nprint(bin(5)[2:])',
    [OUT('print(bin(8))', ["0b100", "8", "0b1001"], "8 = 1000 em binário."),
     TYPE('print(int("0b111", 2))', "111 em binário é 7."),
     MC("O que o prefixo 0b indica?", "Que o número está em binário", ["Que é negativo", "Que é texto", "Que é decimal"], "0b = binário, 0o = octal, 0x = hexadecimal.")]),
  B("oct", "oct(inteiro)", "Número em octal (texto).",
    "Mostra o número na base 8, com o prefixo 0o. Aparece em permissões de arquivos no Linux.",
    'print(oct(8))\nprint(oct(64))\nprint(0o17)',
    [OUT('print(oct(9))', ["0o9", "9", "0o10"], "9 = 1×8 + 1."),
     TYPE('print(0o10)', "Literal octal: 10 na base 8 é 8."),
     MC("Qual é o prefixo de octal?", "0o", ["0x", "0b", "0c"], "o de octal.")]),
  B("hex", "hex(inteiro)", "Número em hexadecimal (texto).",
    "Base 16, com algarismos 0-9 e a-f e prefixo 0x. Muito usado em cores e memória.",
    'print(hex(255))\nprint(hex(16))\nprint(int("ff", 16))',
    [OUT('print(hex(10))', ["0x10", "10", "0xA0"], "10 em hexadecimal é a."),
     TYPE('print(0x1f)', "1×16 + 15."),
     MC("Na cor #FF0000, FF em decimal é…", "255", ["16", "100", "15"], "F = 15; FF = 15×16 + 15.")]),
  B("ascii", "ascii(objeto)", "Como repr, mas só com caracteres ASCII.",
    "Acentos e emojis viram códigos de escape como \\xe9. Útil para registrar textos com segurança.",
    'print(ascii("olá"))\nprint(ascii("Pipo"))\nprint(repr("olá"))',
    [OUT('print(ascii("ç"))', ["'ç'", "c", "Erro"], "ç vira o escape \\xe7."),
     TYPE('print(ascii("abc") == repr("abc"))', "Sem acentos, os dois são iguais."),
     MC("ascii() é parecido com…", "repr()", ["str()", "len()", "ord()"], "Mostra com aspas, mas escapa o que não é ASCII.")]),
  B("format", "format(valor, especificação)", "Formata um valor como texto.",
    "Usa a mesma mini-linguagem das f-strings: casas decimais, alinhamento, separador de milhar, porcentagem…",
    'print(format(3.14159, ".2f"))\nprint(format(1234567, ","))\nprint(format(0.25, ".0%"))\nprint(format("oi", ">6") + "|")',
    [OUT('print(format(7, "03d"))', ["7", "703", "3d7"], "3 dígitos, completando com zeros."),
     TYPE('print(format(2.5, ".1f"))', "Uma casa decimal."),
     MC('f"{x:.2f}" equivale a…', 'format(x, ".2f")', ['round(x, 2)', 'str(x)[:4]', 'format(".2f", x)'], "f-strings usam format por baixo.")]),
)
# ============================================================ 8
U("Iteradores", "iter, next, slice, aiter e anext",
  B("iter", "iter(coleção)", "Cria um iterador.",
    "Um iterador entrega os itens um de cada vez, lembrando onde parou. O for usa iter por baixo dos panos.",
    'it = iter([10, 20, 30])\nprint(next(it))\nprint(next(it))\nprint(list(it))',
    [OUT('it = iter("ab")\nnext(it)\nprint(list(it))', ["['a', 'b']", "[]", "a"], "O primeiro já foi consumido."),
     TYPE('it = iter([1, 2, 3])\nnext(it)\nnext(it)\nprint(next(it))', "O terceiro item."),
     MC("O que o for faz por baixo dos panos?", "Chama iter() e depois next() até acabar", ["Usa len() e índices", "Copia a lista", "Ordena a lista"], "Por isso o for funciona com qualquer iterável.")]),
  B("next", "next(iterador, padrão)", "Pega o próximo item.",
    "Quando o iterador acaba, dá StopIteration, a não ser que você passe um valor padrão.",
    'it = iter([1])\nprint(next(it))\nprint(next(it, "acabou"))',
    [OUT('print(next(iter("xyz")))', ["xyz", "z", "['x']"], "O primeiro caractere."),
     TYPE('pares = (n for n in range(10) if n % 2 == 0 and n > 4)\nprint(next(pares))', "O primeiro par maior que 4."),
     MC("next(it) num iterador vazio, sem padrão, dá…", "StopIteration", ["None", "0", "IndexError"], "É assim que o for sabe que acabou.")]),
  B("slice", "slice(início, fim, passo)", "Um objeto de fatia.",
    "lista[1:4] é o mesmo que lista[slice(1, 4)]. Útil para guardar uma fatia numa variável e reutilizar.",
    'primeiros = slice(0, 3)\nprint("python"[primeiros])\nprint([1, 2, 3, 4, 5][slice(None, None, 2)])',
    [OUT('s = slice(1, None)\nprint("abcd"[s])', ["abcd", "a", "bc"], "Do índice 1 até o fim."),
     TYPE('print("abcdef"[slice(None, None, -1)][0])', "Passo -1 inverte; o primeiro passa a ser f."),
     MC('texto[2:5] equivale a…', "texto[slice(2, 5)]", ["texto[range(2, 5)]", "texto.slice(2, 5)", "slice(texto, 2, 5)"], "A sintaxe [:] cria um slice.")]),
  B("aiter", "aiter(iterável_assíncrono)", "Iterador de uma coleção assíncrona.",
    "É o iter() do mundo assíncrono (async/await). Usado com async for e geradores async def. Você vai ver isso ao trabalhar com tarefas que esperam rede ou arquivos.",
    'async def contar():\n    for i in range(3):\n        yield i\n\nasync def main():\n    it = aiter(contar())\n    print(await anext(it))\n    print(await anext(it))\n\n# Num programa normal: import asyncio; asyncio.run(main())\n# Aqui rodamos a função assíncrona "na mão", que funciona em qualquer lugar:\ntry:\n    main().send(None)\nexcept StopIteration:\n    pass',
    [MC("aiter() é a versão assíncrona de…", "iter()", ["len()", "print()", "range()"], "aiter/anext ↔ iter/next."),
     MC("Em que tipo de função se usa await anext(...)?", "Numa função async def", ["Em qualquer função", "Só em classes", "Só no terminal"], "await só funciona dentro de async def."),
     MC("Um gerador assíncrono é criado com…", "async def e yield", ["def e return", "lambda", "class"], "async def + yield = gerador assíncrono.")]),
  B("anext", "await anext(iterador_assíncrono, padrão)", "Próximo item de um iterador assíncrono.",
    "É o next() do mundo assíncrono. Precisa de await. Como o next, aceita um valor padrão para quando acabar.",
    'async def letras():\n    yield "a"\n\nasync def main():\n    it = aiter(letras())\n    print(await anext(it))\n    print(await anext(it, "fim"))\n\n# Num programa normal: import asyncio; asyncio.run(main())\ntry:\n    main().send(None)\nexcept StopIteration:\n    pass',
    [MC("anext precisa de…", "await", ["return", "yield", "lambda"], "Ele devolve algo que precisa ser esperado."),
     MC("Quando o iterador assíncrono acaba e não há padrão, anext dá…", "StopAsyncIteration", ["StopIteration", "None", "0"], "É o StopIteration do mundo async."),
     MC("Qual par é equivalente no mundo síncrono?", "iter() e next()", ["list() e len()", "open() e read()", "map() e filter()"], "aiter/anext espelham iter/next.")]),
)
# ============================================================ 9
U("Bytes e memória", "bytes, bytearray, memoryview e hash",
  B("bytes", "bytes(valor, encoding)", "Sequência de bytes (imutável).",
    "Bytes são números de 0 a 255. Textos viram bytes com encode e voltam com decode. Arquivos e redes trabalham com bytes.",
    'b = "olá".encode("utf-8")\nprint(b)\nprint(len(b))\nprint(b.decode("utf-8"))\nprint(bytes([80, 121]))',
    [OUT('print(len("é".encode("utf-8")))', ["1", "0", "Erro"], "Em UTF-8, é ocupa 2 bytes."),
     TYPE('print(bytes([65, 66]).decode())', "65 é A e 66 é B."),
     MC("Como transformar o texto t em bytes?", 't.encode("utf-8")', ['bytes(t)', 't.decode()', 'str(t, "bytes")'], "encode vai de texto para bytes; decode volta.")]),
  B("bytearray", "bytearray(valor)", "Bytes que podem mudar.",
    "Igual a bytes, mas mutável: dá para trocar, adicionar e remover bytes.",
    'ba = bytearray(b"gato")\nba[0] = ord("p")\nprint(ba)\nba.append(33)\nprint(ba.decode())',
    [OUT('b = bytearray(3)\nprint(list(b))', ["[3]", "[]", "Erro"], "bytearray(3) cria 3 bytes zerados."),
     TYPE('b = bytearray(b"ab")\nb[1] = 99\nprint(b.decode())', "99 é c."),
     MC("A diferença entre bytes e bytearray é…", "bytearray pode ser alterado", ["bytes é maior", "bytearray só guarda texto", "Nenhuma"], "Como tupla vs lista.")]),
  B("memoryview", "memoryview(bytes_ou_bytearray)", "Janela para a memória sem copiar.",
    "Permite ler e alterar pedaços de bytes grandes sem fazer cópias. Útil com imagens, áudio e dados binários.",
    'dados = bytearray(b"abcdef")\njanela = memoryview(dados)[2:4]\nprint(bytes(janela))\njanela[0] = ord("X")\nprint(dados)',
    [OUT('m = memoryview(b"pipo")\nprint(m[0])', ["p", "b'p'", "Erro"], "Cada posição é um número (o byte)."),
     MC("Para que memoryview serve?", "Acessar pedaços de bytes sem copiar", ["Medir a memória do computador", "Liberar memória", "Guardar senhas"], "Economiza cópias em dados grandes."),
     TYPE('print(len(memoryview(b"abc")))', "Três bytes.")]),
  B("hash", "hash(objeto)", "Número de impressão digital.",
    "Objetos imutáveis (números, strings, tuplas) têm hash. É o que permite usá-los como chave de dicionário e em conjuntos. O valor de strings muda entre execuções.",
    'print(hash(1) == hash(1.0))\nprint(hash((1, 2)) == hash((1, 2)))\ntry:\n    hash([1, 2])\nexcept TypeError as e:\n    print("lista:", e)',
    [OUT('print(hash(10))', ["1", "0", "Erro"], "O hash de um inteiro pequeno é o próprio número."),
     MC("Por que uma lista não pode ser chave de dicionário?", "Porque é mutável e não tem hash", ["Porque é grande", "Porque tem colchetes", "Pode sim"], "Use uma tupla no lugar."),
     TYPE('print(hash("a") == hash("a"))', "O mesmo valor sempre tem o mesmo hash na mesma execução.")]),
)
# ============================================================ 10
U("Objetos e atributos", "object, getattr, setattr, delattr, vars e dir",
  B("object", "object()", "A classe mãe de todas.",
    "Toda classe herda de object, mesmo sem escrever. object() cria um objeto vazio e único, às vezes usado como marcador.",
    'class Ponto:\n    pass\n\nprint(issubclass(Ponto, object))\nmarcador = object()\nprint(marcador == object())',
    [OUT('print(isinstance("texto", object))', ["False", "Erro", "None"], "Tudo é object."),
     MC("Escrever class A(object): e class A: é…", "A mesma coisa no Python 3", ["Diferente", "Erro", "Só funciona com object"], "object é a base implícita."),
     TYPE('print(type(object()).__name__)', "O tipo é object.")]),
  B("getattr", "getattr(objeto, 'nome', padrão)", "Pega um atributo pelo nome.",
    "Útil quando o nome do atributo está numa variável. Com padrão, não dá erro se não existir.",
    'class Gato:\n    nome = "Mimi"\n\ng = Gato()\nprint(getattr(g, "nome"))\nprint(getattr(g, "idade", "?"))\nprint(getattr("oi", "upper")())',
    [OUT('print(getattr([1, 2], "count")(2))', ["2", "0", "Erro"], "getattr pegou o método count, que foi chamado com 2."),
     TYPE('campo = "real"\nprint(getattr(3 + 4j, campo))', "A parte real de 3+4j."),
     MC('getattr(obj, "x") equivale a…', "obj.x", ['obj["x"]', "obj(x)", "x.obj"], "Mas com o nome vindo de um texto.")]),
  B("setattr", "setattr(objeto, 'nome', valor)", "Define um atributo pelo nome.",
    "O contrário do getattr: cria ou muda um atributo usando o nome em texto.",
    'class Config:\n    pass\n\nc = Config()\nfor chave, valor in {"tema": "escuro", "som": True}.items():\n    setattr(c, chave, valor)\nprint(c.tema, c.som)',
    [OUT('class A: pass\na = A()\nsetattr(a, "x", 5)\nprint(a.x * 2)', ["5", "Erro", "x5"], "a.x passou a valer 5."),
     MC('setattr(p, "idade", 30) equivale a…', "p.idade = 30", ['p["idade"] = 30', "p.setattr(30)", 'idade = p.30'], "Atribuição por nome."),
     TYPE('class A: pass\na = A()\nsetattr(a, "nome", "Pipo")\nprint(a.nome)', "O atributo foi criado.")]),
  B("delattr", "delattr(objeto, 'nome')", "Apaga um atributo pelo nome.",
    "É o mesmo que del objeto.nome, mas com o nome em texto.",
    'class A:\n    pass\n\na = A()\na.x = 1\ndelattr(a, "x")\nprint(hasattr(a, "x"))',
    [OUT('class A: pass\na = A()\na.v = 1\ndel a.v\nprint(hasattr(a, "v"))', ["True", "1", "Erro"], "del apagou o atributo."),
     MC('delattr(obj, "x") equivale a…', "del obj.x", ["obj.x = None", "obj.pop(x)", "obj.x.delete()"], "Remove de verdade, não só zera."),
     MC("Apagar um atributo que não existe dá…", "AttributeError", ["Nada", "KeyError", "None"], "Teste com hasattr antes.")]),
  B("vars", "vars(objeto)", "Os atributos de um objeto como dicionário.",
    "Mostra o __dict__ do objeto: nome → valor de cada atributo criado nele.",
    'class Pessoa:\n    def __init__(self, nome, idade):\n        self.nome = nome\n        self.idade = idade\n\nprint(vars(Pessoa("Ana", 20)))',
    [OUT('class A:\n    def __init__(self):\n        self.x = 1\nprint(list(vars(A())))', ["['x', 1]", "[1]", "{'x': 1}"], "list de um dicionário pega as chaves."),
     TYPE('class B: pass\nprint(len(vars(B())))', "Sem atributos criados, o dicionário está vazio."),
     MC("vars(obj) é o mesmo que…", "obj.__dict__", ["dir(obj)", "type(obj)", "obj.vars()"], "dir lista tudo, inclusive métodos herdados.")]),
  B("dir", "dir(objeto)", "Lista o que um objeto tem.",
    "Mostra nomes de atributos e métodos, incluindo os herdados. Os que começam com _ são internos.",
    'metodos = [m for m in dir([]) if not m.startswith("_")]\nprint(metodos)',
    [OUT('print("upper" in dir("x"))', ["False", "upper", "Erro"], "Strings têm upper."),
     MC("Para descobrir o que dá para fazer com uma lista, use…", "dir([])", ["len([])", "type([])", "list.dir"], "dir lista os métodos."),
     TYPE('print(len([m for m in dir(5) if m == "real"]))', "Inteiros têm o atributo real.")]),
)
# ============================================================ 11
U("Classes avançadas", "property, staticmethod, classmethod e super",
  B("property", "@property", "Método que se usa como atributo.",
    "Com @property, você calcula ou valida um valor, mas acessa como atributo, sem parênteses.",
    'class Retangulo:\n    def __init__(self, l, a):\n        self.l, self.a = l, a\n\n    @property\n    def area(self):\n        return self.l * self.a\n\nr = Retangulo(3, 4)\nprint(r.area)',
    [OUT('class C:\n    @property\n    def dobro(self):\n        return 21 * 2\nprint(C().dobro)', ["21", "Erro", "<bound method>"], "Acessa sem parênteses e o método roda."),
     MC("Com @property, como você acessa area?", "r.area", ["r.area()", "r[area]", "area(r)"], "Parece atributo."),
     TYPE('class T:\n    @property\n    def nome(self):\n        return "pipo".title()\nprint(T().nome)', "O método roda ao acessar.")]),
  B("staticmethod", "@staticmethod", "Função dentro da classe, sem self.",
    "Um método estático não recebe self nem a classe. É uma função comum guardada na classe por organização.",
    'class Matematica:\n    @staticmethod\n    def dobro(n):\n        return n * 2\n\nprint(Matematica.dobro(5))\nprint(Matematica().dobro(1))',
    [OUT('class U:\n    @staticmethod\n    def oi():\n        return "oi"\nprint(U.oi())', ["Erro: falta self", "U", "None"], "Métodos estáticos não precisam de self."),
     MC("Um staticmethod recebe self?", "Não", ["Sim", "Só o primeiro", "Recebe a classe"], "É uma função comum dentro da classe."),
     TYPE('class K:\n    @staticmethod\n    def soma(a, b):\n        return a + b\nprint(K.soma(2, 3))', "Chamado direto pela classe.")]),
  B("classmethod", "@classmethod", "Método que recebe a classe (cls).",
    "Em vez de self, recebe cls, a própria classe. Muito usado para criar objetos de outros jeitos (construtores alternativos).",
    'class Data:\n    def __init__(self, d, m):\n        self.d, self.m = d, m\n\n    @classmethod\n    def de_texto(cls, texto):\n        d, m = map(int, texto.split("/"))\n        return cls(d, m)\n\nx = Data.de_texto("07/10")\nprint(x.d, x.m)',
    [OUT('class A:\n    n = 0\n    @classmethod\n    def criar(cls):\n        cls.n += 1\n        return cls()\nA.criar(); A.criar()\nprint(A.n)', ["0", "1", "Erro"], "cls é a própria classe A, e n é compartilhado."),
     MC("O primeiro parâmetro de um classmethod se chama, por convenção…", "cls", ["self", "this", "class"], "cls aponta para a classe."),
     TYPE('class P:\n    @classmethod\n    def nome(cls):\n        return cls.__name__\nprint(P.nome())', "cls.__name__ é o nome da classe.")]),
  B("super", "super().metodo()", "Chama o método da classe mãe.",
    "Dentro de uma classe filha, super() acessa a versão da mãe. Muito usado no __init__ para aproveitar o que a mãe já faz.",
    'class Animal:\n    def __init__(self, nome):\n        self.nome = nome\n\nclass Cachorro(Animal):\n    def __init__(self, nome, raca):\n        super().__init__(nome)\n        self.raca = raca\n\nc = Cachorro("Rex", "vira-lata")\nprint(c.nome, c.raca)',
    [OUT('class A:\n    def oi(self):\n        return "A"\nclass B(A):\n    def oi(self):\n        return "B" + super().oi()\nprint(B().oi())', ["B", "A", "AB"], "B chama o oi da mãe e junta."),
     MC("Esquecer super().__init__(...) na filha causa…", "A filha não ganha os atributos que a mãe criaria", ["Nada", "Erro de sintaxe", "A mãe é apagada"], "O __init__ da mãe não roda."),
     TYPE('class A:\n    def v(self):\n        return 1\nclass B(A):\n    def v(self):\n        return super().v() + 1\nprint(B().v())', "1 da mãe + 1.")]),
)
# ============================================================ 12
U("Código que roda código", "eval, exec, compile, globals, locals, __import__, breakpoint e open",
  B("eval", "eval(expressão)", "Calcula uma expressão escrita em texto.",
    "Recebe um texto com uma expressão Python e devolve o resultado. Nunca use com texto vindo de usuários: ele pode rodar qualquer coisa.",
    'print(eval("2 + 3 * 4"))\nx = 10\nprint(eval("x * 2"))',
    [OUT('print(eval("len(\'abc\') + 1"))', ["len('abc') + 1", "Erro", "abc1"], "A expressão é calculada."),
     TYPE('print(eval("10 // 3"))', "Divisão inteira."),
     MC("Por que é perigoso usar eval com o que o usuário digita?", "Ele pode executar qualquer código", ["Ele é lento", "Só aceita números", "Apaga variáveis sempre"], "Para converter números, use int ou float.")]),
  B("exec", "exec(código)", "Roda um trecho de código escrito em texto.",
    "Diferente do eval, executa comandos (atribuições, laços, def…) e devolve None. Também é perigoso com textos de fora.",
    'codigo = "for i in range(3):\\n    print(i)"\nexec(codigo)\nexec("y = 5")\nprint(y)',
    [OUT('print(exec("1 + 1"))', ["2", "Erro", "1 + 1"], "exec não devolve resultado: None."),
     MC("Qual a diferença entre eval e exec?", "eval devolve o valor de uma expressão; exec roda comandos", ["Nenhuma", "exec é mais seguro", "eval roda laços"], "exec devolve None."),
     TYPE('ns = {}\nexec("a = 2 ** 5", ns)\nprint(ns["a"])', "exec guardou a variável no dicionário ns.")]),
  B("compile", "compile(código, nome, modo)", "Prepara código em texto para rodar depois.",
    "Transforma o texto em código pronto (objeto code), nos modos \"eval\", \"exec\" ou \"single\". Útil para rodar o mesmo trecho muitas vezes. É o que o terminal do PyPasso usa por dentro.",
    'expr = compile("x * 2", "<conta>", "eval")\nfor x in range(3):\n    print(eval(expr))',
    [OUT('c = compile("print(\'oi\')", "<t>", "exec")\nexec(c)', ["print('oi')", "Erro", "None"], "O código compilado roda com exec."),
     MC("Qual modo usar para uma expressão como \"a + b\"?", '"eval"', ['"exec"', '"run"', '"calc"'], "eval para expressões; exec para comandos."),
     MC('compile("x = ", "<t>", "exec") dá…', "SyntaxError", ["None", "Um código vazio", "x"], "compile já verifica a sintaxe.")]),
  B("globals", "globals()", "Dicionário com as variáveis globais.",
    "Mostra tudo o que foi criado no nível de cima do arquivo: variáveis, funções, imports.",
    'nivel = "global"\nprint("nivel" in globals())\nprint(globals()["nivel"])',
    [OUT('vidas = 5\nprint(globals()["vidas"] + 1)', ["5", "Erro", "vidas1"], "globals() dá acesso à variável pelo nome."),
     MC("globals() devolve…", "Um dicionário nome → valor", ["Uma lista de nomes", "O número de variáveis", "None"], "É o dicionário do módulo."),
     TYPE('def f():\n    pass\nprint(callable(globals()["f"]))', "A função f está no dicionário global.")]),
  B("locals", "locals()", "Dicionário com as variáveis locais.",
    "Dentro de uma função, mostra as variáveis daquela função naquele momento.",
    'def f(a):\n    b = a * 2\n    print(locals())\n\nf(3)',
    [OUT('def g(x):\n    y = 1\n    return sorted(locals())\nprint(g(0))', ["['y']", "['x']", "{'x': 0, 'y': 1}"], "As chaves são x e y."),
     TYPE('def h():\n    return len(locals())\nprint(h())', "Sem variáveis locais."),
     MC("Fora de qualquer função, locals() é…", "O mesmo que globals()", ["Vazio", "Erro", "None"], "No nível de cima, local e global coincidem.")]),
  B("__import__", "__import__('nome')", "Importa um módulo pelo nome em texto.",
    "É o que o comando import usa por baixo. No dia a dia prefira import ou importlib.import_module; __import__ aparece em códigos que escolhem o módulo em tempo de execução.",
    'm = __import__("math")\nprint(m.sqrt(16))\nnome = "random"\nr = __import__(nome)\nprint(r.__name__)',
    [OUT('print(__import__("math").floor(2.9))', ["2.9", "3", "Erro"], "floor arredonda para baixo."),
     MC("No dia a dia, o melhor jeito de importar é…", "import math", ['__import__("math")', 'exec("import math")', 'open("math")'], "__import__ é para casos especiais."),
     TYPE('print(__import__("string").digits)', "string.digits são os algarismos.")]),
  B("breakpoint", "breakpoint()", "Pausa o programa para investigar.",
    "Num computador, abre o depurador (pdb) naquela linha para você inspecionar variáveis. O comportamento pode ser trocado; aqui trocamos por uma mensagem para ver o efeito.",
    'import sys\nsys.breakpointhook = lambda: print("(pausa: aqui você inspecionaria as variáveis)")\nx = 42\nbreakpoint()\nprint("continuou com x =", x)',
    [MC("Para que serve breakpoint()?", "Pausar o programa e investigar as variáveis", ["Encerrar o programa", "Dividir a tela", "Quebrar a linha"], "Abre o depurador pdb."),
     MC("No depurador pdb, o comando para continuar é…", "c (continue)", ["q (quit)", "exit()", "print"], "n vai para a próxima linha; c continua; q sai."),
     OUT('import sys\nsys.breakpointhook = lambda: print("pausa")\nbreakpoint()\nprint("fim")', ["fim", "pausa", "Erro"], "O gancho trocado mostra pausa e o programa segue.")]),
  B("open", "open(arquivo, modo, encoding)", "Abre um arquivo.",
    "Modos: \"r\" lê, \"w\" escreve do zero, \"a\" acrescenta, \"b\" binário. Use dentro de with para fechar sozinho.",
    'with open("diario.txt", "w", encoding="utf-8") as f:\n    f.write("Hoje aprendi open()!\\n")\nwith open("diario.txt", encoding="utf-8") as f:\n    print(f.read().strip())',
    [OUT('with open("t.txt", "w") as f:\n    f.write("12345")\nprint(len(open("t.txt").read()))', ["12345", "1", "0"], "O arquivo tem 5 caracteres."),
     TYPE('with open("a.txt", "w") as f:\n    f.write("x")\nwith open("a.txt", "a") as f:\n    f.write("y")\nprint(open("a.txt").read())', "\"a\" acrescentou depois do x."),
     MC('O modo "w" faz o quê com o conteúdo antigo?', "Apaga tudo e começa do zero", ["Acrescenta no fim", "Só lê", "Dá erro"], 'Para acrescentar, use "a".')]),
)

# ============================================================ unidades extras (combinações)
sys.path.insert(0, AQUI)
from builtins_extras import EXTRAS
UNITS.extend(EXTRAS)

# ============================================================ validação e geração
import builtins as _b
def run(src, entrada=""):
    buf = io.StringIO()
    respostas = iter(entrada.splitlines())
    def fake_input(prompt=""):
        return next(respostas)  # sem eco: nos exercícios, o que foi digitado aparece num comentário
    old_in, old_hook = _b.input, sys.breakpointhook
    _b.input = fake_input
    random.seed(0)
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(src, "<ex>", "exec"), {"__name__": "__main__"})
    finally:
        _b.input = old_in; sys.breakpointhook = old_hook
    return buf.getvalue().rstrip("\n")

def run_err(src, entrada=""):
    try:
        return run(src, entrada), None
    except Exception as ex:
        return None, ex

os.chdir(tempfile.mkdtemp())
HOSTS = ["ana", "caio", "bia", "teo"]
problems, nomes = [], []
course = {"units": []}
biblio = []
for ui, (titulo, desc, lessons) in enumerate(UNITS):
    unit = {"id": f"b{ui}", "title": titulo, "description": desc, "lessons": []}
    for li, L in enumerate(lessons):
        combo = L.get("combo", False)
        nome = L["titulo"] if combo else L["nome"]
        if not combo: nomes.append(nome)
        lid = f"b{ui}l{li}"
        saida, ex = run_err(L["exemplo"], L["entrada"])
        if ex: problems.append((nome, "exemplo do cartão", f"{type(ex).__name__}: {ex}")); saida = ""
        exs = [{"k": "learn", "id": f"{lid}c0", "host": "pipo", "q": f"{nome}: {L['resumo']}" if combo else f"{nome}(): {L['resumo']}",
                "body": L["explica"] + (f"\n\nCuidado: {L['cuidado']}" if L["cuidado"] else ""), "c": L["exemplo"], "out": saida + (f"\n(respostas digitadas: {', '.join(L['entrada'].splitlines())})" if L["entrada"] else ""), "e": ""}]
        for ei, it in enumerate(L["itens"]):
            it = dict(it)
            k = it["k"]
            q = "Qual é a saída?" if k == "out" else "Digite a saída." if k == "type" else it.get("q")
            if k in ("out", "type"):
                o, ex = run_err(it["c"], it.pop("_in"))
                if ex:
                    problems.append((nome, "exercício com erro", it["c"], f"{type(ex).__name__}: {ex}")); continue
                if k == "out":
                    errados = it.pop("_wrong")
                    if o in errados: problems.append((nome, "distrator igual à resposta", o))
                    it["o"] = [o, *errados]
                    if len(set(it["o"])) != 4: problems.append((nome, "opções repetidas", it["o"]))
                else:
                    if "\n" in o or o != o.strip() or not o: problems.append((nome, "resposta de digitar ruim", repr(o)))
                    it["a"] = [o]
                if it["c"] and "entrada" in L and it.get("_in"): pass
            elif k == "fill":
                src = it["c"].replace("___", it["a"][0])
                o, ex = run_err(src) if nome not in ("help",) else ("", None)
                if ex and not isinstance(ex, NameError): problems.append((nome, "lacuna não roda", src, ex))
            elif k == "order":
                o, ex = run_err("\n".join(it["l"]))
                if ex: problems.append((nome, "ordem não roda", ex))
                q = it["q"]
            elif k == "code":
                sol = it.pop("_sol")
                for src, deve_passar in ((sol, True), (it["starter"], False)):
                    try:
                        o = run(src); ns_ok = True
                        g = {"__name__": "__main__"}
                        with contextlib.redirect_stdout(io.StringIO()):
                            exec(compile(src, "<sol>", "exec"), g)
                        g["__stdout__"] = o
                        exec(it["tests"], g)
                        passou = True
                    except Exception as e2:
                        passou = False; err = e2
                    if passou != deve_passar:
                        problems.append((nome, "código", "solução falhou" if deve_passar else "o código inicial já passa", src, None if passou else err))
                q = it["q"]
            if k == "mc" and len(set(it["o"])) != len(it["o"]): problems.append((nome, "mc repetido", it["o"]))
            it.update(q=q, id=f"{lid}e{ei}", host=HOSTS[(ui + li + ei) % 4])
            exs.append(it)
        unit["lessons"].append({"id": lid, "title": nome if combo else f"{nome}()", "exercises": exs})
        if combo: continue
        biblio.append({"nome": nome, "sig": L["sig"], "resumo": L["resumo"], "explica": L["explica"], "exemplo": L["exemplo"],
                       "saida": saida, "entrada": L["entrada"], "cuidado": L["cuidado"], "licao": lid})
    course["units"].append(unit)

faltam = set(OFICIAIS) - set(nomes); extras = set(nomes) - set(OFICIAIS)
if faltam or extras or len(nomes) != 71: problems.append(("lista oficial", "faltam", sorted(faltam), "extras", sorted(extras), len(nomes)))
for n in nomes:
    if not hasattr(builtins, n): problems.append((n, "não é built-in"))
if problems:
    for p in problems: print("PROBLEMA:", p)
    raise SystemExit(1)
# ============================================================ uma unidade por função
# Cada função vira a unidade fn_<nome>: a lição 1 é a de cima ("o básico") e as lições
# 2 a 6 vêm de tools/builtins_licoes/gNN_*.py (conferidas por validar_builtins.py).
from validar_builtins import GRUPOS, validar
import glob
resumo = {b["nome"]: b["resumo"] for b in biblio}
extras_licoes = {}
for caminho in sorted(glob.glob(os.path.join(AQUI, "builtins_licoes", "g[0-9][0-9]_*.py"))):
    unidades, _bugs, probs = validar(caminho)
    if probs:
        for p_ in probs: print("PROBLEMA:", os.path.basename(caminho), *p_)
        raise SystemExit(1)
    extras_licoes.update(unidades)
novas, legado = [], {}
n_grupos = len(GRUPOS)
for u in course["units"][:n_grupos]:
    for l in u["lessons"]:
        nome = l["title"][:-2]
        fid = f"fn_{nome}"
        l0 = json.loads(json.dumps(l).replace(f'"{l["id"]}', f'"{fid}_l0'))
        l0["title"] = f"Conhecendo {nome}()"
        legado[l["id"]] = f"{fid}_l0"  # progresso antigo (b0l0…) passa para a lição 1 da função
        if nome not in extras_licoes:
            print("PROBLEMA: faltam as lições 2–6 de", nome); raise SystemExit(1)
        novas.append({"id": fid, "title": f"{nome}()", "description": resumo[nome], "group": u["title"],
                      "lessons": [l0, *extras_licoes[nome]]})
for b in biblio:
    b["licao"] = f"fn_{b['nome']}_l0"
# Unidades de base (antes das funções): ensinam strings, números, coleções, if/for,
# def, erros, arquivos e classes, que a trilha usa desde o print.
from validar_builtins import BASE
base = []
for key, (titulo, desc) in BASE.items():
    unidades, _b, probs = validar(os.path.join(AQUI, "builtins_licoes", f"{key}.py"))
    if probs:
        for p_ in probs: print("PROBLEMA:", key, *p_)
        raise SystemExit(1)
    base.append({"id": key, "title": titulo, "description": desc, "group": "Antes dos built-ins", "lessons": unidades[key]})
course["units"] = base + novas + course["units"][n_grupos:]
course["builtinsLibrary"] = biblio
course["legacyIds"] = legado
json.dump(course, open(SAIDA, "w"), ensure_ascii=False, indent=1)
from conferir_ordem import conferir
_ordem = conferir()
if _ordem:
    for p_ in _ordem: print("PROBLEMA de ordem (conceito usado antes de ser ensinado):", *p_)
    raise SystemExit(1)
n_ex = sum(1 for u in course["units"] for l in u["lessons"] for e in l["exercises"] if e["k"] != "learn")
n_l = sum(len(u["lessons"]) for u in course["units"])
print(f"OK: {len(nomes)} funções embutidas, {len(course['units'])} unidades, {n_l} lições, {n_ex} exercícios")
