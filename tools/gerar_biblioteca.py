"""Biblioteca de funções do PyPasso. As saídas dos exemplos são geradas rodando Python.

Para adicionar uma função: escreva uma chamada e(...) na categoria certa e rode
    python3 tools/gerar_biblioteca.py
O script roda cada exemplo, confere as referências e grava src/content/library.json."""
import contextlib, io, json, os, tempfile, random
SAIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "content", "library.json")

CATS = [
    ("basico", "Básico", "print, input, len, type e conversões"),
    ("numeros", "Números", "contas, arredondar, mínimo e máximo"),
    ("texto", "Textos (str)", "métodos de string"),
    ("listas", "Listas", "adicionar, remover, ordenar"),
    ("dicionarios", "Dicionários", "chave e valor"),
    ("conjuntos", "Conjuntos e tuplas", "set, tuple e operações"),
    ("lacos", "Laços e iteração", "range, enumerate, zip, map, filter"),
    ("arquivos", "Arquivos", "open, read, write"),
    ("erros", "Erros", "try, except, raise e os erros comuns"),
    ("modulos", "Módulos", "math, random, datetime"),
    ("palavras", "Palavras-chave", "if, for, while, def, class…"),
    ("embutidas", "Mais funções embutidas", "as outras built-ins: chr, ord, hex, getattr, super…"),
]
E = []
def e(id, nome, cat, sig, resumo, explica, params, retorna, exemplo, cuidado=None, rel=(), tags="", entrada=""):
    E.append(dict(id=id, nome=nome, cat=cat, sig=sig, resumo=resumo, explica=explica,
                  params=[{"nome": a, "desc": b} for a, b in params], retorna=retorna,
                  exemplo=exemplo, cuidado=cuidado, rel=list(rel), tags=tags, entrada=entrada))

# ---------------------------------------------------------------- Básico
e("print", "print()", "basico", "print(*valores, sep=' ', end='\\n')", "Mostra valores na tela.",
  "Escreve na saída tudo que você passar, separado por espaço. No fim, pula uma linha. Dá para trocar o separador com sep e o final com end.",
  [("valores", "Um ou mais valores para mostrar, separados por vírgula."), ("sep", "O que vai entre os valores (padrão: espaço)."), ("end", "O que vai no fim (padrão: quebra de linha).")],
  "None (só mostra; não devolve nada útil).",
  'print("Olá", "mundo")\nprint("a", "b", "c", sep="-")\nprint("sem pular", end=" | ")\nprint("linha")',
  "print mostra, mas não devolve o valor. Para usar o resultado depois, guarde numa variável em vez de imprimir.", ["input", "fstring", "repr"], "mostrar exibir saida escrever tela")
e("input", "input()", "basico", "input(pergunta='')", "Lê o que a pessoa digita.",
  "Mostra a pergunta e espera a pessoa digitar e apertar Enter. Devolve sempre o texto digitado, mesmo que seja um número.",
  [("pergunta", "Texto mostrado antes da pessoa digitar (opcional).")], "str: o texto digitado.",
  'nome = input("Seu nome: ")\nidade = int(input("Sua idade: "))\nprint(f"{nome} faz {idade + 1} ano que vem")',
  "input() sempre devolve texto. Para fazer contas, converta com int() ou float(). Na aba Código, as respostas vão na caixa Entrada.", ["int", "float", "print"], "ler teclado digitar entrada perguntar",
  entrada="Ana\n20")
e("len", "len()", "basico", "len(coleção)", "Conta quantos itens algo tem.",
  "Devolve o tamanho de uma string (quantidade de caracteres), lista, tupla, dicionário (quantidade de chaves) ou conjunto.",
  [("coleção", "String, lista, tupla, dicionário, conjunto…")], "int: a quantidade de itens.",
  'print(len("Python"))\nprint(len([10, 20, 30]))\nprint(len({"a": 1, "b": 2}))\nprint(len(""))',
  "Números não têm tamanho: len(42) dá TypeError. Espaços contam como caracteres.", ["range", "str.count"], "tamanho quantidade contar comprimento")
e("type", "type()", "basico", "type(valor)", "Diz o tipo de um valor.",
  "Útil para descobrir se algo é texto, número inteiro, decimal, lista… Ajuda muito a entender erros de tipo.",
  [("valor", "Qualquer valor ou variável.")], "O tipo do valor (por exemplo <class 'int'>).",
  'print(type(42))\nprint(type(3.5))\nprint(type("oi"))\nprint(type([1, 2]))',
  "Para testar o tipo dentro de um if, prefira isinstance(valor, int).", ["isinstance", "int", "str"], "tipo classe descobrir")
e("isinstance", "isinstance()", "basico", "isinstance(valor, tipo)", "Testa se um valor é de um tipo.",
  "Responde True ou False. Aceita uma tupla de tipos para testar vários de uma vez.",
  [("valor", "O que você quer testar."), ("tipo", "Um tipo (int, str, list…) ou uma tupla de tipos.")], "bool.",
  'print(isinstance(5, int))\nprint(isinstance("5", int))\nprint(isinstance(2.5, (int, float)))',
  None, ["type"], "tipo verificar checar")
e("int", "int()", "basico", "int(valor)", "Converte para número inteiro.",
  "Transforma textos como \"42\" em 42 e corta a parte decimal de números como 3.9 (vira 3, sem arredondar).",
  [("valor", "Texto com algarismos ou número decimal.")], "int.",
  'print(int("42") + 1)\nprint(int(3.9))\nprint(int("-7"))',
  "int(\"3.5\") e int(\"abc\") dão ValueError. Para textos com ponto, use float() primeiro.", ["float", "str", "round", "input"], "converter inteiro numero")
e("float", "float()", "basico", "float(valor)", "Converte para número decimal.",
  "Transforma textos como \"3.5\" em 3.5. Use ponto, não vírgula.",
  [("valor", "Texto ou número.")], "float.",
  'print(float("3.5") * 2)\nprint(float(7))',
  "float(\"3,5\") dá ValueError: o separador decimal do Python é o ponto. Troque com texto.replace(\",\", \".\").", ["int", "round"], "decimal converter ponto flutuante")
e("str", "str()", "basico", "str(valor)", "Converte qualquer valor em texto.",
  "Útil para juntar números com textos usando +.",
  [("valor", "Qualquer valor.")], "str.",
  'idade = 30\nprint("Idade: " + str(idade))\nprint(str(3.5) + "!")',
  "Muitas vezes uma f-string é mais simples: f\"Idade: {idade}\".", ["fstring", "int"], "texto converter string")
e("bool", "bool()", "basico", "bool(valor)", "Diz se um valor conta como verdadeiro.",
  "0, texto vazio, lista vazia e None contam como False. Todo o resto é True. É isso que o if usa por baixo dos panos.",
  [("valor", "Qualquer valor.")], "True ou False.",
  'print(bool(0))\nprint(bool(""))\nprint(bool([]))\nprint(bool("0"))\nprint(bool(42))',
  "bool(\"False\") é True: é um texto com conteúdo.", ["if"], "verdadeiro falso booleano")
e("repr", "repr()", "basico", "repr(valor)", "Mostra o valor como ele é escrito no código.",
  "Strings aparecem entre aspas e com \\n visível. Ótimo para enxergar espaços escondidos.",
  [("valor", "Qualquer valor.")], "str.",
  'texto = "  oi\\n"\nprint(texto)\nprint(repr(texto))',
  None, ["print", "str.strip"], "depurar espacos aspas")
e("help", "help()", "basico", "help(algo)", "Mostra a documentação oficial de algo.",
  "Funciona com funções, métodos e módulos. Teste no >>> do terminal da aba Código.",
  [("algo", "Uma função, método, tipo ou módulo.")], "None (mostra o texto de ajuda).",
  'def dobro(n):\n    """Devolve o dobro de n."""\n    return n * 2\n\nprint(dobro.__doc__)',
  "No terminal, digite help(len) ou help(str.split).", ["dir"], "ajuda documentacao")
e("dir", "dir()", "basico", "dir(valor)", "Lista o que um valor sabe fazer.",
  "Mostra os métodos e atributos disponíveis. Os nomes com __ dos dois lados são internos.",
  [("valor", "Qualquer valor ou tipo.")], "list de nomes.",
  'metodos = [m for m in dir("texto") if not m.startswith("_")]\nprint(metodos[:6])',
  None, ["help", "type"], "metodos listar atributos")

# ---------------------------------------------------------------- Números
e("operadores", "+ - * / // % **", "numeros", "a + b, a - b, a * b, a / b, a // b, a % b, a ** b", "As contas básicas.",
  "/ é a divisão comum e sempre dá decimal. // é a divisão inteira (sem a parte decimal). % é o resto da divisão. ** é potência.",
  [], "O resultado da conta.",
  'print(7 / 2)\nprint(7 // 2)\nprint(7 % 2)\nprint(2 ** 10)',
  "Dividir por zero dá ZeroDivisionError. Para saber se n é par: n % 2 == 0.", ["divmod", "round", "abs"], "conta soma divisao resto potencia matematica")
e("round", "round()", "numeros", "round(número, casas=0)", "Arredonda um número.",
  "Sem o segundo argumento, devolve um inteiro. Com ele, mantém aquela quantidade de casas decimais.",
  [("número", "O valor a arredondar."), ("casas", "Quantas casas decimais manter (opcional).")], "int ou float.",
  'print(round(3.14159, 2))\nprint(round(2.7))\nprint(round(1234.5678, -2))',
  "Nos empates o Python arredonda para o par mais próximo: round(2.5) é 2 e round(3.5) é 4.", ["int", "math.floor"], "arredondar casas decimais")
e("abs", "abs()", "numeros", "abs(número)", "Valor absoluto (tira o sinal).",
  "Transforma negativos em positivos. Útil para medir distâncias e diferenças.",
  [("número", "Qualquer número.")], "O número sem sinal.",
  'print(abs(-7))\nprint(abs(3.5))\nprint(abs(10 - 25))',
  None, ["operadores"], "modulo positivo distancia")
e("min", "min()", "numeros", "min(itens) ou min(a, b, …)", "O menor valor.",
  "Aceita vários argumentos ou uma lista. Com textos, compara em ordem alfabética.",
  [("itens", "Uma coleção ou vários valores."), ("key", "Função que diz o que comparar (opcional).")], "O menor item.",
  'print(min(4, 9, 2))\nprint(min([3.5, 1.2, 8]))\nprint(min(["pera", "uva", "abacaxi"], key=len))',
  "min([]) dá ValueError: lista vazia não tem menor valor.", ["max", "sorted"], "menor minimo")
e("max", "max()", "numeros", "max(itens) ou max(a, b, …)", "O maior valor.",
  "Igual ao min, mas devolve o maior. Com key, você escolhe o critério.",
  [("itens", "Uma coleção ou vários valores."), ("key", "Função que diz o que comparar (opcional).")], "O maior item.",
  'print(max(4, 9, 2))\nnotas = {"Ana": 9, "Caio": 7}\nprint(max(notas, key=notas.get))',
  None, ["min", "sorted"], "maior maximo")
e("sum", "sum()", "numeros", "sum(números, início=0)", "Soma todos os números de uma coleção.",
  "Funciona com listas, tuplas, conjuntos e geradores de números.",
  [("números", "Coleção de números."), ("início", "Valor inicial da soma (opcional).")], "A soma.",
  'print(sum([10, 20, 30]))\nprint(sum(range(1, 101)))\nnotas = [7, 8, 9]\nprint(sum(notas) / len(notas))',
  "sum não junta textos; para isso use \"\".join(lista).", ["len", "str.join"], "somar total media")
e("divmod", "divmod()", "numeros", "divmod(a, b)", "Divisão inteira e resto de uma vez.",
  "Devolve a tupla (a // b, a % b). Muito usado para converter segundos em minutos e segundos.",
  [("a", "Dividendo."), ("b", "Divisor.")], "tuple (quociente, resto).",
  'minutos, segundos = divmod(135, 60)\nprint(minutos, "min", segundos, "s")',
  None, ["operadores"], "quociente resto tempo")
e("pow", "pow()", "numeros", "pow(base, expoente)", "Potência (o mesmo que **).",
  "pow(2, 3) é o mesmo que 2 ** 3.",
  [("base", "O número."), ("expoente", "A potência.")], "O resultado.",
  'print(pow(2, 3))\nprint(pow(9, 0.5))',
  None, ["operadores", "math.sqrt"], "potencia elevado")

# ---------------------------------------------------------------- Textos
S = "texto"
def m(id, nome, sig, resumo, explica, params, retorna, exemplo, cuidado=None, rel=(), tags=""):
    e("str." + id, nome, S, sig, resumo, explica, params, retorna, exemplo, cuidado, [r if r in ("fstring", "len", "repr", "print", "int", "float", "in", "fatias", "str") else "str." + r for r in rel], tags)

e("fstring", 'f"…{valor}…"', S, 'f"texto {expressão}"', "Monta textos com valores dentro.",
  "Coloque f antes das aspas e escreva variáveis ou contas entre chaves. Depois de dois-pontos dá para formatar: casas decimais, alinhamento…",
  [], "str.",
  'nome, preco = "Bia", 4.5\nprint(f"Oi, {nome}! Total: R$ {preco * 2:.2f}")\nprint(f"{nome:>6}|")',
  "Sem o f antes das aspas, as chaves aparecem literalmente: \"Oi, {nome}\".", ["str", "print"], "formatar fstring interpolar")
m("upper", ".upper()", "texto.upper()", "Tudo em MAIÚSCULAS.", "Devolve uma nova string com todas as letras maiúsculas.", [], "str.",
  'print("python".upper())', "Strings não mudam: s.upper() sozinho não altera s. Guarde o resultado: s = s.upper().", ["lower", "title"], "maiuscula caixa alta")
m("lower", ".lower()", "texto.lower()", "Tudo em minúsculas.", "Ótimo para comparar respostas sem ligar para maiúsculas.", [], "str.",
  'resposta = "SiM"\nprint(resposta.lower() == "sim")', None, ["upper", "casefold"], "minuscula comparar")
m("title", ".title()", "texto.title()", "Maiúscula no começo de cada palavra.", "Útil para nomes e títulos.", [], "str.",
  'print("ana maria silva".title())', "Apóstrofos confundem o title: \"d'água\".title() vira \"D'Água\".", ["capitalize", "upper"], "nome titulo")
m("capitalize", ".capitalize()", "texto.capitalize()", "Só a primeira letra maiúscula.", "A primeira letra vira maiúscula e todo o resto vira minúsculo.", [], "str.",
  'print("pYTHON é LEGAL".capitalize())', None, ["title"], "primeira letra frase")
m("swapcase", ".swapcase()", "texto.swapcase()", "Inverte maiúsculas e minúsculas.", "O que era maiúsculo vira minúsculo e vice-versa.", [], "str.",
  'print("Olá Mundo".swapcase())', None, ["upper", "lower"], "inverter caixa")
m("strip", ".strip()", "texto.strip(caracteres=None)", "Tira espaços das pontas.", "Remove espaços, \\n e \\t do começo e do fim. Passando caracteres, remove esses das pontas.",
  [("caracteres", "Quais caracteres remover (opcional). É um conjunto, não uma palavra.")], "str.",
  'print(repr("  oi  ".strip()))\nprint("***oba***".strip("*"))', "\"banana\".strip(\"an\") vira \"b\": remove as letras a e n das pontas, não a palavra \"an\".", ["lstrip", "rstrip"], "espacos limpar remover pontas")
m("lstrip", ".lstrip()", "texto.lstrip(caracteres=None)", "Tira espaços só da esquerda.", "Igual ao strip, mas mexe só no começo (left).",
  [("caracteres", "Quais caracteres remover (opcional).")], "str.", 'print(repr("  oi  ".lstrip()))\nprint("00042".lstrip("0"))', None, ["strip", "rstrip"], "esquerda inicio")
m("rstrip", ".rstrip()", "texto.rstrip(caracteres=None)", "Tira espaços só da direita.", "Igual ao strip, mas mexe só no fim (right). Muito usado para tirar o \\n de linhas lidas de arquivos.",
  [("caracteres", "Quais caracteres remover (opcional).")], "str.", 'print(repr("  oi  ".rstrip()))\nprint(repr("linha\\n".rstrip("\\n")))', None, ["strip", "lstrip"], "direita fim")
m("center", ".center()", "texto.center(largura, preenchimento=' ')", "Centraliza num tamanho fixo.", "Completa os dois lados até a largura pedida.",
  [("largura", "Tamanho final."), ("preenchimento", "Caractere usado para completar (opcional).")], "str.", 'print("menu".center(12, "*"))', "Se a largura for menor que o texto, ele volta sem mudanças.", ["ljust", "rjust", "fstring"], "centralizar alinhar")
m("ljust", ".ljust()", "texto.ljust(largura, preenchimento=' ')", "Alinha à esquerda num tamanho fixo.", "Completa à direita. Bom para montar tabelas.",
  [("largura", "Tamanho final."), ("preenchimento", "Caractere de preenchimento (opcional).")], "str.", 'for item, preco in [("pão", 2), ("café", 7)]:\n    print(item.ljust(8, ".") + str(preco))', None, ["rjust", "center"], "alinhar esquerda tabela")
m("rjust", ".rjust()", "texto.rjust(largura, preenchimento=' ')", "Alinha à direita num tamanho fixo.", "Completa à esquerda.",
  [("largura", "Tamanho final."), ("preenchimento", "Caractere de preenchimento (opcional).")], "str.", 'print("7".rjust(3, "0"))\nprint("fim".rjust(8) + "|")', None, ["ljust", "zfill"], "alinhar direita")
m("zfill", ".zfill()", "texto.zfill(largura)", "Completa com zeros à esquerda.", "Ideal para códigos e números de pedido. Respeita o sinal de menos.",
  [("largura", "Tamanho final.")], "str.", 'print("42".zfill(5))\nprint(str(7).zfill(3))', "Só funciona em texto: converta números com str() antes.", ["rjust"], "zeros codigo")
m("split", ".split()", "texto.split(sep=None, maxsplit=-1)", "Quebra o texto numa lista.", "Sem argumentos, quebra nos espaços (e ignora espaços repetidos). Com sep, quebra naquele separador.",
  [("sep", "Onde quebrar (opcional)."), ("maxsplit", "Quantas quebras no máximo (opcional).")], "list de str.",
  'print("um  dois três".split())\nprint("a,b,c".split(","))\nprint("a-b-c".split("-", 1))', None, ["join", "rsplit", "splitlines", "partition"], "quebrar dividir separar palavras")
m("rsplit", ".rsplit()", "texto.rsplit(sep=None, maxsplit=-1)", "Quebra começando pela direita.", "Só faz diferença quando há maxsplit.",
  [("sep", "Onde quebrar."), ("maxsplit", "Quantas quebras no máximo.")], "list de str.", 'print("foto.final.png".rsplit(".", 1))', None, ["split"], "direita extensao")
m("splitlines", ".splitlines()", "texto.splitlines()", "Quebra o texto em linhas.", "Separa em cada quebra de linha.", [], "list de str.",
  'poema = "linha 1\\nlinha 2\\nlinha 3"\nprint(poema.splitlines())', None, ["split"], "linhas quebrar")
m("join", ".join()", "separador.join(lista)", "Junta uma lista num texto só.", "O separador vai entre os itens. É o contrário do split.",
  [("lista", "Coleção de strings.")], "str.", 'print(" ".join(["Python", "é", "legal"]))\nprint("-".join("abc"))\nprint(", ".join([str(n) for n in [1, 2, 3]]))',
  "Todos os itens precisam ser texto: \"-\".join([1, 2]) dá TypeError.", ["split"], "juntar unir concatenar lista")
m("replace", ".replace()", "texto.replace(velho, novo, quantas=-1)", "Troca um trecho por outro.", "Troca todas as ocorrências, ou só as primeiras se você passar quantas.",
  [("velho", "O que procurar."), ("novo", "O que colocar no lugar."), ("quantas", "Limite de trocas (opcional).")], "str.",
  'print("banana".replace("a", "o"))\nprint("banana".replace("a", "o", 1))\nprint("3,5".replace(",", "."))', None, ["find", "strip"], "trocar substituir")
m("find", ".find()", "texto.find(trecho)", "Posição de um trecho (ou -1).", "Devolve o índice onde o trecho começa. Se não achar, devolve -1 em vez de dar erro.",
  [("trecho", "O que procurar.")], "int.", 'print("banana".find("na"))\nprint("banana".find("x"))', None, ["index", "count", "in"], "procurar posicao buscar")
m("index", ".index()", "texto.index(trecho)", "Posição de um trecho (ou erro).", "Igual ao find, mas dá ValueError se não achar. Também existe em listas.",
  [("trecho", "O que procurar.")], "int.", 'print("banana".index("n"))', "\"banana\".index(\"x\") dá ValueError. Use find ou teste com in antes.", ["find"], "posicao procurar")
m("count", ".count()", "texto.count(trecho)", "Conta quantas vezes um trecho aparece.", "Conta ocorrências que não se sobrepõem.",
  [("trecho", "O que contar.")], "int.", 'print("banana".count("a"))\nprint("o rato roeu".count("o"))', None, ["find", "len"], "contar ocorrencias")
m("startswith", ".startswith()", "texto.startswith(prefixo)", "Começa com…?", "Responde True ou False. Aceita uma tupla com várias opções.",
  [("prefixo", "Texto (ou tupla de textos) para testar no começo.")], "bool.", 'print("Python".startswith("Py"))\nprint("doc.txt".startswith(("img", "doc")))', None, ["endswith"], "comeca prefixo inicio")
m("endswith", ".endswith()", "texto.endswith(sufixo)", "Termina com…?", "Ótimo para testar extensões de arquivo e domínios de e-mail.",
  [("sufixo", "Texto (ou tupla de textos) para testar no fim.")], "bool.", 'arquivo = "foto.PNG"\nprint(arquivo.lower().endswith((".png", ".jpg")))', None, ["startswith"], "termina extensao sufixo")
m("isdigit", ".isdigit()", "texto.isdigit()", "Só tem algarismos?", "True se todos os caracteres forem de 0 a 9 (e o texto não for vazio).", [], "bool.",
  'print("2024".isdigit())\nprint("-5".isdigit())\nprint("3.5".isdigit())', "Sinal de menos e ponto não são algarismos.", ["isalpha", "isalnum", "int"], "numero digito validar")
m("isalpha", ".isalpha()", "texto.isalpha()", "Só tem letras?", "Letras com acento contam. Espaço não conta.", [], "bool.",
  'print("Ação".isalpha())\nprint("Ana Lu".isalpha())', None, ["isdigit", "isalnum"], "letras validar")
m("isalnum", ".isalnum()", "texto.isalnum()", "Só letras e algarismos?", "True se não houver espaços nem símbolos.", [], "bool.",
  'print("abc123".isalnum())\nprint("abc 123".isalnum())', None, ["isalpha", "isdigit"], "alfanumerico validar")
m("isspace", ".isspace()", "texto.isspace()", "Só tem espaços?", "Útil para detectar respostas em branco.", [], "bool.",
  'print("   ".isspace())\nprint("".isspace())', "Texto vazio dá False. Para pegar vazio e só espaços juntos: not texto.strip().", ["strip"], "branco vazio espacos")
m("partition", ".partition()", "texto.partition(sep)", "Divide em 3 partes na primeira ocorrência.", "Devolve (antes, separador, depois). Se não achar, devolve (texto, '', '').",
  [("sep", "O separador.")], "tuple de 3 str.", 'chave, _, valor = "cor=azul".partition("=")\nprint(chave, valor)', None, ["split"], "dividir chave valor")
m("casefold", ".casefold()", "texto.casefold()", "Minúsculas para comparar.", "Parecido com lower(), mas mais forte para comparações em vários idiomas.", [], "str.",
  'print("Straße".casefold() == "strasse")', None, ["lower"], "comparar minuscula")
e("in", "in", S, "item in coleção", "Testa se algo está dentro de outra coisa.",
  "Funciona com strings (trecho dentro do texto), listas, tuplas, conjuntos e dicionários (procura nas chaves). not in faz o contrário.",
  [], "bool.", 'print("py" in "python")\nprint(3 in [1, 2, 3])\nprint("nome" in {"nome": "Ana"})\nprint("x" not in "abc")',
  "Em dicionários, in procura nas chaves, não nos valores.", ["str.find", "list.index"], "contem pertence existe")
e("fatias", "texto[início:fim:passo]", S, "seq[início:fim:passo]", "Pega um pedaço de string, lista ou tupla.",
  "O início entra e o fim não. Índices negativos contam do fim. Passo -1 inverte.",
  [("início", "Onde começa (padrão: 0)."), ("fim", "Onde para, sem incluir (padrão: até o fim)."), ("passo", "De quanto em quanto (padrão: 1).")], "Um pedaço do mesmo tipo.",
  's = "python"\nprint(s[0])\nprint(s[-1])\nprint(s[1:4])\nprint(s[::-1])',
  "Índice fora do tamanho dá IndexError, mas fatias fora do tamanho não dão erro.", ["len"], "indice fatia slice pedaco inverter")

# ---------------------------------------------------------------- Listas
LI = "listas"
def lm(id, nome, sig, resumo, explica, params, retorna, exemplo, cuidado=None, rel=(), tags=""):
    e("list." + id, nome, LI, sig, resumo, explica, params, retorna, exemplo, cuidado, [r if "." in r or r in ("sorted", "reversed", "len", "in", "sum", "fatias", "compreensao", "map", "filter") else "list." + r for r in rel], tags)

lm("append", ".append()", "lista.append(item)", "Coloca um item no fim.", "Altera a própria lista.", [("item", "O que adicionar.")], "None.",
   'frutas = ["maçã"]\nfrutas.append("uva")\nprint(frutas)', "Não faça lista = lista.append(x): append devolve None e você perde a lista.", ["extend", "insert"], "adicionar inserir final")
lm("extend", ".extend()", "lista.extend(outra)", "Junta outra coleção no fim.", "Coloca cada item da outra coleção, um por um.", [("outra", "Lista, tupla, string…")], "None.",
   'a = [1, 2]\na.extend([3, 4])\nprint(a)\nb = [1, 2]\nb.append([3, 4])\nprint(b)', "append coloca a lista inteira como um item só; extend coloca os itens.", ["append"], "juntar concatenar")
lm("insert", ".insert()", "lista.insert(posição, item)", "Coloca um item numa posição.", "Os itens dali em diante andam uma casa.", [("posição", "Índice onde inserir."), ("item", "O que inserir.")], "None.",
   'letras = ["a", "c"]\nletras.insert(1, "b")\nprint(letras)', None, ["append"], "inserir posicao")
lm("remove", ".remove()", "lista.remove(valor)", "Remove a primeira ocorrência de um valor.", "Procura pelo valor, não pela posição.", [("valor", "O que remover.")], "None.",
   'nums = [3, 1, 3]\nnums.remove(3)\nprint(nums)', "Se o valor não existir, dá ValueError. Teste com in antes.", ["pop", "clear"], "remover apagar excluir")
lm("pop", ".pop()", "lista.pop(posição=-1)", "Remove e devolve um item.", "Sem argumento, tira o último. Com uma posição, tira aquele.", [("posição", "Índice a remover (opcional).")], "O item removido.",
   'pilha = [1, 2, 3]\nultimo = pilha.pop()\nprimeiro = pilha.pop(0)\nprint(ultimo, primeiro, pilha)', "pop() em lista vazia dá IndexError.", ["remove"], "remover ultimo pilha")
lm("clear", ".clear()", "lista.clear()", "Esvazia a lista.", "Remove todos os itens.", [], "None.", 'nums = [1, 2, 3]\nnums.clear()\nprint(nums)', None, ["remove"], "limpar esvaziar")
lm("index", ".index()", "lista.index(valor)", "Posição de um valor.", "Devolve o índice da primeira ocorrência.", [("valor", "O que procurar.")], "int.",
   'cores = ["azul", "verde", "azul"]\nprint(cores.index("verde"))', "Dá ValueError se não achar.", ["count", "in"], "posicao procurar")
lm("count", ".count()", "lista.count(valor)", "Conta quantas vezes um valor aparece.", "", [("valor", "O que contar.")], "int.",
   'votos = ["sim", "não", "sim"]\nprint(votos.count("sim"))', None, ["index"], "contar")
lm("sort", ".sort()", "lista.sort(reverse=False, key=None)", "Ordena a própria lista.", "Altera a lista no lugar. reverse=True ordena do maior para o menor; key escolhe o critério.",
   [("reverse", "True para ordem decrescente."), ("key", "Função que diz como comparar.")], "None.",
   'nums = [3, 1, 2]\nnums.sort()\nprint(nums)\nnomes = ["Bia", "ana", "Caio"]\nnomes.sort(key=str.lower)\nprint(nomes)', "sort devolve None: não faça lista = lista.sort(). Para uma cópia ordenada, use sorted().", ["sorted", "reverse"], "ordenar classificar")
e("sorted", "sorted()", LI, "sorted(coleção, reverse=False, key=None)", "Devolve uma cópia ordenada.",
  "Funciona com qualquer coleção e não mexe na original.",
  [("coleção", "Lista, tupla, string, conjunto…"), ("reverse", "True para decrescente."), ("key", "Critério de ordenação.")], "list nova.",
  'notas = [7, 10, 5]\nprint(sorted(notas))\nprint(sorted(notas, reverse=True))\nprint(notas)\nprint(sorted(["pera", "uva", "abacaxi"], key=len))',
  None, ["list.sort", "reversed"], "ordenar copia")
lm("reverse", ".reverse()", "lista.reverse()", "Inverte a própria lista.", "", [], "None.", 'nums = [1, 2, 3]\nnums.reverse()\nprint(nums)', None, ["reversed", "sort"], "inverter")
e("reversed", "reversed()", LI, "reversed(sequência)", "Percorre de trás para frente.",
  "Devolve um iterador; use list() para ver como lista ou use direto num for.", [("sequência", "Lista, tupla, string ou range.")], "Um iterador.",
  'for n in reversed([1, 2, 3]):\n    print(n)\nprint(list(reversed("abc")))', None, ["list.reverse", "fatias"], "inverter tras")
lm("copy", ".copy()", "lista.copy()", "Faz uma cópia da lista.", "Mudanças na cópia não afetam a original.", [], "list nova.",
   'a = [1, 2]\nb = a\nc = a.copy()\na.append(3)\nprint(b)\nprint(c)', "b = a NÃO copia: as duas variáveis apontam para a mesma lista.", ["fatias"], "copiar clonar")
e("compreensao", "[x for x in …]", LI, "[expressão for item in coleção if condição]", "Cria uma lista nova numa linha.",
  "Percorre a coleção, opcionalmente filtra com if e transforma cada item.", [], "list nova.",
  'quadrados = [n * n for n in range(5)]\npares = [n for n in range(10) if n % 2 == 0]\nprint(quadrados)\nprint(pares)', "Se ficar difícil de ler, use um for normal.", ["map", "filter", "for"], "compreensao list comprehension")
e("list", "list()", LI, "list(coleção)", "Cria uma lista.",
  "Transforma strings, tuplas, conjuntos e ranges em lista.", [("coleção", "Qualquer coleção (opcional).")], "list.",
  'print(list("abc"))\nprint(list(range(4)))\nprint(list())', None, ["tuple", "set"], "criar converter lista")

# ---------------------------------------------------------------- Dicionários
D = "dicionarios"
def dm(id, nome, sig, resumo, explica, params, retorna, exemplo, cuidado=None, rel=(), tags=""):
    e("dict." + id, nome, D, sig, resumo, explica, params, retorna, exemplo, cuidado, [r if r in ("dict", "in", "for") else "dict." + r for r in rel], tags)

e("dict", "dict() e {}", D, '{chave: valor, …}', "Guarda pares chave → valor.",
  "Busca rápida pela chave. As chaves precisam ser imutáveis (str, int, tupla). Atribuir a uma chave cria ou atualiza.", [], "dict.",
  'aluno = {"nome": "Ana", "idade": 20}\naluno["idade"] = 21\naluno["curso"] = "Python"\nprint(aluno)\nprint(aluno["nome"])',
  "Buscar uma chave que não existe com [ ] dá KeyError. Use .get().", ["dict.get", "dict.items", "in"], "dicionario chave valor mapa")
dm("get", ".get()", "dic.get(chave, padrão=None)", "Busca uma chave sem dar erro.", "Se a chave não existir, devolve None ou o padrão que você passar.",
   [("chave", "O que buscar."), ("padrão", "Valor devolvido se não achar (opcional).")], "O valor, ou o padrão.",
   'estoque = {"maçã": 3}\nprint(estoque.get("uva"))\nprint(estoque.get("uva", 0))\ncont = {}\nfor letra in "aba":\n    cont[letra] = cont.get(letra, 0) + 1\nprint(cont)', None, ["dict", "setdefault"], "buscar padrao contar")
dm("keys", ".keys()", "dic.keys()", "As chaves do dicionário.", "Um for direto no dicionário já percorre as chaves.", [], "Uma visão das chaves.",
   'd = {"a": 1, "b": 2}\nprint(list(d.keys()))', None, ["values", "items"], "chaves")
dm("values", ".values()", "dic.values()", "Os valores do dicionário.", "Ótimo para somar ou achar o maior valor.", [], "Uma visão dos valores.",
   'precos = {"pão": 2, "café": 7}\nprint(sum(precos.values()))', None, ["keys", "items"], "valores")
dm("items", ".items()", "dic.items()", "Pares (chave, valor).", "O jeito mais comum de percorrer um dicionário.", [], "Uma visão dos pares.",
   'notas = {"Ana": 9, "Caio": 7}\nfor nome, nota in notas.items():\n    print(nome, nota)', None, ["keys", "values"], "percorrer pares")
dm("update", ".update()", "dic.update(outro)", "Junta outro dicionário.", "Chaves repetidas ficam com o valor novo.", [("outro", "Outro dicionário.")], "None.",
   'config = {"tema": "claro", "som": True}\nconfig.update({"tema": "escuro"})\nprint(config)', None, ["dict"], "juntar atualizar mesclar")
dm("pop", ".pop()", "dic.pop(chave, padrão)", "Remove e devolve uma chave.", "", [("chave", "Qual remover."), ("padrão", "Devolvido se a chave não existir (opcional).")], "O valor removido.",
   'd = {"a": 1, "b": 2}\nprint(d.pop("a"))\nprint(d)\nprint(d.pop("z", "não tinha"))', "Sem padrão, chave inexistente dá KeyError.", ["get"], "remover apagar")
dm("setdefault", ".setdefault()", "dic.setdefault(chave, padrão)", "Pega a chave ou cria com um padrão.", "Se a chave não existe, cria com o padrão e devolve.",
   [("chave", "A chave."), ("padrão", "Valor inicial se não existir.")], "O valor.",
   'grupos = {}\nfor nome in ["Ana", "Alice", "Bia"]:\n    grupos.setdefault(nome[0], []).append(nome)\nprint(grupos)', None, ["get"], "agrupar padrao")

# ---------------------------------------------------------------- Conjuntos e tuplas
C = "conjuntos"
e("set", "set()", C, "set(coleção) ou {1, 2, 3}", "Coleção sem repetição.",
  "Ótimo para remover duplicados e testar se algo pertence muito rápido. Não tem ordem nem índice.", [("coleção", "Qualquer coleção (opcional).")], "set.",
  'print(set([1, 2, 2, 3, 3]))\nprint(len(set("banana")))', "{} cria um dicionário vazio! Conjunto vazio é set().", ["set.add", "set.ops"], "conjunto unico duplicados")
e("set.add", ".add()", C, "conjunto.add(item)", "Adiciona um item ao conjunto.", "Se já existir, nada muda.", [("item", "O que adicionar.")], "None.",
  'vistos = set()\nfor n in [1, 2, 1]:\n    vistos.add(n)\nprint(vistos)', None, ["set", "set.discard"], "adicionar")
e("set.discard", ".discard()", C, "conjunto.discard(item)", "Remove um item, se existir.", "Diferente de remove(), não dá erro quando o item não está lá.", [("item", "O que remover.")], "None.",
  's = {1, 2, 3}\ns.discard(2)\ns.discard(9)\nprint(s)', None, ["set.add"], "remover")
e("set.ops", "| & - ^", C, "a | b, a & b, a - b, a ^ b", "União, interseção e diferença.",
  "| junta tudo, & fica com o que está nos dois, - tira do primeiro o que está no segundo, ^ fica com o que está em só um deles.", [], "set novo.",
  'a = {1, 2, 3}\nb = {3, 4}\nprint(a | b)\nprint(a & b)\nprint(a - b)\nprint(a ^ b)', None, ["set"], "uniao intersecao diferenca")
e("tuple", "tuple() e ( )", C, "(a, b, c)", "Sequência que não pode mudar.",
  "Parecida com lista, mas imutável. Muito usada para devolver vários valores de uma função e para desempacotar.", [], "tuple.",
  'ponto = (3, 4)\nx, y = ponto\nprint(x + y)\nprint(ponto[0])\nunico = (5,)\nprint(type(unico))', "Tupla de um item precisa da vírgula: (5,). Sem ela, (5) é só o número 5.", ["list", "desempacotar"], "tupla imutavel")
e("desempacotar", "a, b = …", C, "a, b = sequência", "Separa uma sequência em variáveis.",
  "Cada variável recebe um item. Com * uma variável pega o resto. Também serve para trocar valores.", [], "—",
  'nome, idade = ["Ana", 20]\nprimeiro, *resto = [1, 2, 3, 4]\nprint(nome, idade, primeiro, resto)\na, b = 1, 2\na, b = b, a\nprint(a, b)', "A quantidade de variáveis precisa bater com a de itens (a não ser usando *).", ["tuple", "enumerate"], "desempacotar trocar unpack")

# ---------------------------------------------------------------- Laços e iteração
LA = "lacos"
e("range", "range()", LA, "range(fim) / range(início, fim, passo)", "Sequência de números.",
  "Gera do início até antes do fim. Muito usado no for.", [("início", "Primeiro número (padrão 0)."), ("fim", "Para antes deste."), ("passo", "De quanto em quanto (padrão 1).")], "Um range.",
  'print(list(range(5)))\nprint(list(range(2, 10, 3)))\nprint(list(range(5, 0, -1)))', "O fim nunca entra: range(1, 5) vai até 4.", ["for", "enumerate", "len"], "sequencia numeros contar")
e("enumerate", "enumerate()", LA, "enumerate(coleção, start=0)", "Percorre com o número da posição.",
  "Dá o índice e o item juntos, sem precisar de range(len(…)).", [("coleção", "O que percorrer."), ("start", "Número inicial (padrão 0).")], "Pares (índice, item).",
  'for i, fruta in enumerate(["maçã", "uva"], start=1):\n    print(i, fruta)', None, ["range", "zip"], "indice posicao numerar")
e("zip", "zip()", LA, "zip(a, b, …)", "Percorre várias coleções juntas.",
  "Junta o 1º com o 1º, o 2º com o 2º… Para quando a menor acaba.", [("a, b", "Duas ou mais coleções.")], "Tuplas com um item de cada.",
  'nomes = ["Ana", "Caio"]\nnotas = [9, 7]\nfor nome, nota in zip(nomes, notas):\n    print(nome, nota)\nprint(dict(zip(nomes, notas)))', "Itens sobrando na coleção maior são ignorados.", ["enumerate", "dict"], "juntar paralelo parear")
e("map", "map()", LA, "map(função, coleção)", "Aplica uma função a cada item.",
  "Devolve um iterador; use list() para ver o resultado.", [("função", "O que fazer com cada item."), ("coleção", "Os itens.")], "Um iterador.",
  'numeros = list(map(int, ["1", "2", "3"]))\nprint(numeros)\nprint(list(map(str.upper, ["a", "b"])))', "Uma compreensão de lista costuma ser mais legível: [int(x) for x in itens].", ["filter", "compreensao", "lambda"], "aplicar transformar")
e("filter", "filter()", LA, "filter(função, coleção)", "Fica só com os itens aprovados.",
  "Mantém os itens em que a função devolve True.", [("função", "Teste que devolve True ou False."), ("coleção", "Os itens.")], "Um iterador.",
  'idades = [12, 20, 17, 30]\nprint(list(filter(lambda i: i >= 18, idades)))', None, ["map", "compreensao"], "filtrar selecionar")
e("any", "any()", LA, "any(coleção)", "Algum é verdadeiro?", "True se pelo menos um item for verdadeiro.", [("coleção", "Valores ou testes.")], "bool.",
  'senha = "abc7"\nprint(any(c.isdigit() for c in senha))\nprint(any([]))', None, ["all"], "algum existe")
e("all", "all()", LA, "all(coleção)", "Todos são verdadeiros?", "True se todos os itens forem verdadeiros (e também para coleção vazia).", [("coleção", "Valores ou testes.")], "bool.",
  'notas = [7, 8, 9]\nprint(all(n >= 6 for n in notas))\nprint(all([]))', "all([]) é True: não há nenhum item falso.", ["any"], "todos")
e("for", "for", LA, "for item in coleção:", "Repete para cada item.",
  "A cada volta, a variável recebe o próximo item. break sai do laço; continue pula para a próxima volta.", [], "—",
  'for letra in "oi":\n    print(letra)\nfor n in range(10):\n    if n == 3:\n        break\n    print(n)', None, ["while", "range", "enumerate"], "repetir laco loop percorrer")
e("while", "while", LA, "while condição:", "Repete enquanto a condição for verdadeira.",
  "Algo dentro do laço precisa mudar a condição, senão ele nunca termina.", [], "—",
  'contador = 3\nwhile contador > 0:\n    print(contador)\n    contador -= 1\nprint("Já!")', "while True sem break é um laço infinito.", ["for"], "repetir enquanto laco loop")

# ---------------------------------------------------------------- Arquivos
A = "arquivos"
e("open", "open()", A, "open(nome, modo='r', encoding=None)", "Abre um arquivo.",
  "Use dentro de with para o arquivo fechar sozinho. Modos: \"r\" lê, \"w\" escreve apagando o que havia, \"a\" acrescenta no fim.",
  [("nome", "Caminho do arquivo."), ("modo", "\"r\", \"w\" ou \"a\" (e outros)."), ("encoding", "Use \"utf-8\" para acentos.")], "Um objeto arquivo.",
  'with open("nota.txt", "w", encoding="utf-8") as f:\n    f.write("Olá, arquivo!")\nwith open("nota.txt", encoding="utf-8") as f:\n    print(f.read())',
  "Abrir para leitura um arquivo que não existe dá FileNotFoundError.", ["file.read", "file.write", "with"], "arquivo abrir ler escrever")
e("file.read", ".read() / .readlines()", A, "f.read() / f.readlines()", "Lê o conteúdo do arquivo.",
  "read() traz tudo como um texto só. readlines() traz uma lista de linhas. Um for no arquivo lê linha por linha.", [], "str ou list.",
  'with open("lista.txt", "w") as f:\n    f.write("pão\\nleite\\n")\nwith open("lista.txt") as f:\n    for linha in f:\n        print(linha.strip())',
  "Cada linha lida vem com \\n no fim: use strip() ou rstrip(\"\\n\").", ["open", "str.strip"], "ler linhas")
e("file.write", ".write()", A, "f.write(texto)", "Escreve texto no arquivo.",
  "Não pula linha sozinho: coloque \\n quando quiser.", [("texto", "O que escrever (precisa ser str).")], "int: quantos caracteres foram escritos.",
  'with open("saida.txt", "w") as f:\n    for i in range(3):\n        f.write(f"linha {i}\\n")\nprint(open("saida.txt").read())', "write só aceita texto: converta números com str().", ["open"], "escrever gravar salvar")
e("with", "with", A, "with algo as nome:", "Usa um recurso e fecha sozinho no fim.",
  "O jeito certo de abrir arquivos: quando o bloco termina, o arquivo é fechado, mesmo se der erro.", [], "—",
  'with open("x.txt", "w") as f:\n    f.write("oi")\nprint(f.closed)', None, ["open"], "fechar contexto")

# ---------------------------------------------------------------- Erros
ER = "erros"
e("try", "try / except", ER, "try: … except Tipo: …", "Trata erros sem parar o programa.",
  "O código arriscado fica no try. Se acontecer o erro indicado, roda o except. else roda se não houve erro; finally roda sempre.", [], "—",
  'for texto in ["10", "abc"]:\n    try:\n        n = int(texto)\n    except ValueError:\n        print(texto, "não é número")\n    else:\n        print("dobro:", n * 2)',
  "Evite except sozinho: ele esconde qualquer erro, até os que você não esperava.", ["raise", "erros.comuns"], "tratar excecao erro")
e("raise", "raise", ER, "raise TipoDeErro(\"mensagem\")", "Dispara um erro de propósito.",
  "Use quando algo não faz sentido no seu programa, para avisar quem chamou a função.", [], "—",
  'def sacar(saldo, valor):\n    if valor > saldo:\n        raise ValueError("saldo insuficiente")\n    return saldo - valor\n\ntry:\n    sacar(50, 80)\nexcept ValueError as erro:\n    print("Erro:", erro)', None, ["try"], "lancar erro excecao")
e("erros.comuns", "Erros comuns", ER, "NameError, TypeError, ValueError, IndexError, KeyError…", "O que cada erro significa.",
  "NameError: nome que não existe. TypeError: tipos que não combinam. ValueError: valor inválido. IndexError: posição fora da lista. KeyError: chave que não existe. ZeroDivisionError: divisão por zero. SyntaxError: algo escrito errado. IndentationError: recuo errado.",
  [], "—",
  'testes = ["nome_que_nao_existe", "1 + \'a\'", "int(\'x\')", "[1][5]", "{}[\'k\']", "1 / 0"]\nfor t in testes:\n    try:\n        eval(t)\n    except Exception as erro:\n        print(type(erro).__name__)',
  "Leia a última linha da mensagem de erro: ela diz o tipo e o motivo. A linha indicada mostra onde o Python parou.", ["try"], "erro mensagem traceback")
e("assert", "assert", ER, "assert condição, \"mensagem\"", "Confere se algo é verdade.",
  "Se a condição for falsa, dá AssertionError com a mensagem. Muito usado em testes, como os dos desafios do PyPasso.", [], "—",
  'def dobro(n):\n    return n * 2\n\nassert dobro(3) == 6, "dobro(3) deveria ser 6"\nprint("Teste passou!")', None, ["raise"], "testar conferir verificar")

# ---------------------------------------------------------------- Módulos
MO = "modulos"
e("import", "import", MO, "import módulo / from módulo import nome", "Traz funções de um módulo.",
  "O Python vem com muitos módulos prontos (math, random, datetime…). Também dá para importar seus próprios arquivos da aba Código.", [], "—",
  'import math\nfrom random import choice\nprint(math.pi)\nprint(choice(["só uma opção"]))', None, ["math.sqrt", "random.randint"], "importar modulo biblioteca")
e("math.sqrt", "math.sqrt()", MO, "math.sqrt(número)", "Raiz quadrada.", "Precisa de import math.", [("número", "Número não negativo.")], "float.",
  'import math\nprint(math.sqrt(16))\nprint(math.sqrt(2))', "Raiz de negativo dá ValueError.", ["pow", "import"], "raiz quadrada")
e("math.floor", "math.floor() / math.ceil()", MO, "math.floor(x) / math.ceil(x)", "Arredonda para baixo / para cima.",
  "floor vai sempre para o inteiro de baixo; ceil sempre para o de cima.", [("x", "Um número.")], "int.",
  'import math\nprint(math.floor(3.7), math.ceil(3.2))\nprint(math.floor(-3.5))', None, ["round", "int"], "arredondar baixo cima piso teto")
e("math.pi", "math.pi", MO, "math.pi", "O número π.", "Constante com o valor de pi. Também existe math.e.", [], "float.",
  'import math\nraio = 2\nprint(round(math.pi * raio ** 2, 2))', None, ["math.sqrt"], "pi circulo")
e("random.randint", "random.randint()", MO, "random.randint(a, b)", "Sorteia um inteiro entre a e b.",
  "Os dois limites podem sair. Use random.seed() para sortear sempre a mesma sequência (útil em testes).", [("a", "Menor valor."), ("b", "Maior valor (incluído).")], "int.",
  'import random\nrandom.seed(42)\nprint(random.randint(1, 6))\nprint(random.randint(1, 6))', None, ["random.choice", "random.shuffle"], "sortear aleatorio dado")
e("random.choice", "random.choice()", MO, "random.choice(sequência)", "Sorteia um item.", "Escolhe um item de uma lista, tupla ou string.", [("sequência", "Onde sortear.")], "Um item.",
  'import random\nrandom.seed(1)\nprint(random.choice(["pedra", "papel", "tesoura"]))', "Lista vazia dá IndexError.", ["random.randint", "random.shuffle"], "sortear escolher")
e("random.shuffle", "random.shuffle()", MO, "random.shuffle(lista)", "Embaralha a lista.", "Mexe na própria lista e devolve None.", [("lista", "A lista a embaralhar.")], "None.",
  'import random\nrandom.seed(3)\ncartas = [1, 2, 3, 4, 5]\nrandom.shuffle(cartas)\nprint(cartas)', "Não faça lista = random.shuffle(lista): você ficaria com None.", ["random.choice"], "embaralhar misturar")
e("datetime", "datetime.date", MO, "date(ano, mês, dia)", "Trabalha com datas.",
  "date.today() dá a data de hoje. Subtrair datas dá a diferença em dias. strftime formata a data como texto.", [], "date.",
  'from datetime import date\ninicio = date(2026, 1, 1)\nfim = date(2026, 10, 7)\nprint((fim - inicio).days, "dias")\nprint(fim.strftime("%d/%m/%Y"))', None, ["import"], "data dia mes ano calendario")

# ---------------------------------------------------------------- Palavras-chave
P = "palavras"
e("if", "if / elif / else", P, "if condição: … elif outra: … else: …", "Toma decisões.",
  "Roda só o primeiro bloco cuja condição for verdadeira. A linha termina com dois-pontos e o bloco vai recuado com 4 espaços.", [], "—",
  'nota = 6\nif nota >= 7:\n    print("aprovado")\nelif nota >= 5:\n    print("recuperação")\nelse:\n    print("reprovado")',
  "Para comparar use ==. Um = sozinho guarda valor e dá erro dentro do if.", ["bool", "and"], "condicao decisao se senao")
e("and", "and / or / not", P, "a and b, a or b, not a", "Combina condições.",
  "and: as duas precisam ser verdadeiras. or: basta uma. not: inverte.", [], "bool (ou um dos valores).",
  'idade, tem_ingresso = 20, True\nprint(idade >= 18 and tem_ingresso)\nprint(idade < 12 or idade > 60)\nprint(not tem_ingresso)',
  "x == 1 or 2 é sempre verdadeiro. Escreva x == 1 or x == 2, ou x in (1, 2).", ["if"], "e ou nao logica")
e("def", "def / return", P, "def nome(parâmetros): … return valor", "Cria uma função.",
  "Uma função é um bloco com nome que você chama quando quiser. Parâmetros recebem valores; return devolve o resultado.", [], "—",
  'def area(base, altura=1):\n    return base * altura\n\nprint(area(3, 4))\nprint(area(5))',
  "Sem return, a função devolve None. print dentro da função mostra, mas não devolve.", ["lambda", "assert"], "funcao criar retornar parametro")
e("lambda", "lambda", P, "lambda parâmetros: expressão", "Função pequena de uma linha.",
  "Muito usada como argumento de sorted, map e filter.", [], "Uma função.",
  'dobro = lambda n: n * 2\nprint(dobro(5))\npessoas = [("Ana", 30), ("Bia", 25)]\nprint(sorted(pessoas, key=lambda p: p[1]))', None, ["def", "sorted", "map"], "funcao anonima")
e("class", "class", P, "class Nome: def __init__(self, …): …", "Cria um molde de objetos.",
  "__init__ roda ao criar o objeto; self é o próprio objeto. Métodos são funções dentro da classe.", [], "—",
  'class Cachorro:\n    def __init__(self, nome):\n        self.nome = nome\n\n    def latir(self):\n        return f"{self.nome}: au au!"\n\nrex = Cachorro("Rex")\nprint(rex.latir())', "Esquecer o self como primeiro parâmetro dos métodos dá TypeError.", ["def"], "classe objeto metodo orientacao")
e("none", "None", P, "None", "O valor que representa \"nada\".",
  "Funções sem return devolvem None. Compare com is None, não com ==.", [], "—",
  'def nada():\n    pass\n\nr = nada()\nprint(r)\nprint(r is None)', None, ["def"], "nulo nada vazio")
e("pass", "pass / break / continue", P, "pass, break, continue", "Controle de blocos e laços.",
  "pass não faz nada (ocupa um bloco vazio). break sai do laço. continue pula para a próxima volta.", [], "—",
  'for n in range(6):\n    if n == 1:\n        continue\n    if n == 4:\n        break\n    print(n)', None, ["for", "while"], "pular sair vazio")
e("global", "global", P, "global nome", "Usa a variável de fora dentro da função.",
  "Sem global, atribuir dentro da função cria uma variável local. Prefira passar valores como parâmetro e devolver com return.", [], "—",
  'pontos = 0\n\ndef marcar():\n    global pontos\n    pontos += 10\n\nmarcar()\nprint(pontos)', "Usar global demais deixa o código difícil de entender.", ["def"], "escopo variavel")

# ---------------------------------------------------------------- validação
import builtins
def run(src, entrada=""):
    buf = io.StringIO()
    respostas = iter(entrada.splitlines())
    def fake_input(prompt=""):  # igual ao terminal do app: mostra a pergunta e a resposta
        v = next(respostas); buf.write(str(prompt) + v + "\n"); return v
    old = builtins.input; builtins.input = fake_input
    random.seed(0)
    try:
        with contextlib.redirect_stdout(buf):
            exec(src, {"__name__": "__main__"})
    finally:
        builtins.input = old
    return buf.getvalue().rstrip("\n")

os.chdir(tempfile.mkdtemp())
ids = {x["id"] for x in E}
problems = []
for x in E:
    try:
        x["saida"] = run(x["exemplo"], x["entrada"])
    except Exception as ex:
        problems.append((x["id"], f"{type(ex).__name__}: {ex}"))
    for r in x["rel"]:
        if r not in ids: problems.append((x["id"], "relacionado inexistente", r))
    if x["cat"] not in {c[0] for c in CATS}: problems.append((x["id"], "categoria", x["cat"]))
if len(ids) != len(E): problems.append(("ids repetidos",))
if problems:
    for p in problems: print("PROBLEMA:", p)
    raise SystemExit(1)
# ---------------------------------------------------------------- as 71 built-ins
# Cada built-in ganha um link para a sua lição na trilha "71 funções embutidas".
# As que ainda não tinham página aqui ganham uma, a partir do conteúdo da lição.
BI = json.load(open(os.path.join(os.path.dirname(SAIDA), "builtins.json")))["builtinsLibrary"]
por_id = {x["id"]: x for x in E}
for b in BI:
    alvo = por_id.get(b["nome"])
    if alvo:
        alvo["licao"] = b["licao"]; alvo["builtin"] = True
        continue
    E.append(dict(id=b["nome"], nome=b["nome"] + "()", cat="embutidas", sig=b["sig"], resumo=b["resumo"], explica=b["explica"],
                  params=[], retorna="", exemplo=b["exemplo"], cuidado=b["cuidado"], rel=[], tags="built-in embutida",
                  entrada=b["entrada"], saida=b["saida"], licao=b["licao"], builtin=True))
for x in E:
    x.setdefault("licao", None); x.setdefault("builtin", False)
ids = {x["id"] for x in E}
print("built-ins com página:", sum(1 for x in E if x["builtin"]))

lib = {"categorias": [{"id": a, "nome": b, "desc": c} for a, b, c in CATS], "funcoes": E}
json.dump(lib, open(SAIDA, "w"), ensure_ascii=False, indent=1)
from collections import Counter
cnt = Counter(x["cat"] for x in E)
print("OK:", len(E), "entradas |", ", ".join(f"{b}: {cnt[a]}" for a, b, _ in CATS))
print("\nExemplo — str.center:\n" + next(x for x in E if x["id"] == "str.center")["saida"])
print("\nExemplo — erros.comuns:\n" + next(x for x in E if x["id"] == "erros.comuns")["saida"])
