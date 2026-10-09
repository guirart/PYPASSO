from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    "base3": [
        # lição 1
        L("Criando funções: def e return",
          "Com def você cria sua própria função: um nome, parâmetros entre parênteses e o bloco recuado. O return DEVOLVE um valor para quem chamou (print só mostra na tela). Sem return, a função devolve None. Um parâmetro pode ter valor padrão, usado quando ninguém passa nada.",
          'def dobro(n):\n    return n * 2\n\ndef saudar(nome, saudacao="Oi"):\n    print(f"{saudacao}, {nome}!")\n\nprint(dobro(5))\nsaudar("Ana")\nsaudar("Caio", "Olá")\nx = saudar("Bia")\nprint(x)',
          [OUT('def mostra(n):\n    print(n + 1)\n\nr = mostra(1)\nprint(r)',
               ["2\n2", "None", "2"],
               "mostra imprime 2, mas não tem return. Então r recebe None."),
           TYPE('def preco(valor, desconto=0):\n    return valor - desconto\n\nprint(preco(50), preco(50, 10))',
                "Na primeira chamada o desconto é o padrão 0; na segunda, 10."),
           FILL("Complete para a função DEVOLVER o triplo do número.",
                'def triplo(n):\n    ___ n * 3\n\nprint(triplo(4))',
                "return", ["print", "def", "give"],
                "return devolve o valor; aí o print de fora mostra 12."),
           CODE("Crie a função area(largura, altura) que DEVOLVE (com return) a largura vezes a altura.",
                "def area(largura, altura):\n    pass\n",
                "def area(largura, altura):\n    return largura * altura\n",
                'assert area(3, 4) == 12, "area(3, 4) deve devolver 12"\nassert area(5, 2) == 10, "area(5, 2) deve devolver 10"',
                "return largura * altura devolve o resultado para quem chamou.")]),
        # lição 2
        L("Funções de uma linha: lambda",
          "lambda cria uma função pequena numa linha só: lambda x: x * 2 recebe x e devolve x * 2. Funções também são valores: dá para guardar numa variável e até passar para outra função (sem os parênteses!). E com *nums a função aceita quantos valores quiser, que chegam juntos numa tupla.",
          'dobro = lambda x: x * 2\nprint(dobro(7))\n\ndef aplica(funcao, valor):\n    return funcao(valor)\n\nprint(aplica(len, "pipoca"))\nprint(aplica(dobro, 10))\n\ndef soma(*nums):\n    total = 0\n    for n in nums:\n        total = total + n\n    return total\n\nprint(soma(1, 2, 3, 4))',
          [FILL("Complete para criar uma função que devolve a metade.",
                'metade = ___ x: x / 2\nprint(metade(10))',
                "lambda", ["def", "return", "func"],
                "lambda x: x / 2 é uma função de uma linha que devolve x / 2."),
           TYPE('def aplica(f, texto):\n    return f(texto)\n\nprint(aplica(len, "banana"))',
                "aplica chama len(\"banana\"), que dá 6."),
           OUT('def conta(*itens):\n    return len(itens)\n\nprint(conta("a", "b", "c"))',
               ["1", "abc", "('a', 'b', 'c')"],
               "*itens junta os três valores numa tupla, e len dela é 3."),
           MC('Em aplica(len, "oi"), por que len vai sem parênteses?',
              "Porque estamos passando a própria função, sem chamá-la ainda",
              ["Porque len nunca precisa de parênteses", "É um erro de digitação", "Porque len só funciona com listas"],
              "len() chama a função; len sozinho é a função como valor.")]),
        # lição 3
        L("Erros e exceções",
          "Quando algo dá errado, o Python para e mostra o NOME do erro: TypeError (tipo errado), ValueError (valor inválido), NameError (nome não existe), IndexError (posição não existe), KeyError (chave não existe), ZeroDivisionError (divisão por zero). Com try/except você trata o erro sem o programa parar. Com except ... as e, type(e).__name__ dá o nome do erro. E raise cria um erro de propósito.",
          'try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print("Não dá para dividir por zero!")\n\nfrutas = ["maçã", "uva"]\ntry:\n    print(frutas[5])\nexcept IndexError as e:\n    print("Erro do tipo", type(e).__name__)\n\ndef sacar(saldo, valor):\n    if valor > saldo:\n        raise ValueError("saldo insuficiente")\n    return saldo - valor\n\nprint(sacar(100, 30))',
          [MC("Que erro aparece em print(nome) se a variável nome nunca foi criada?",
              "NameError", ["TypeError", "KeyError", "IndexError"],
              "NameError: o Python não conhece esse nome."),
           OUT('precos = {"pão": 2}\ntry:\n    print(precos["bolo"])\nexcept KeyError:\n    print("Produto não existe")\nprint("fim")',
               ["KeyError", "None\nfim", "fim"],
               "A chave \"bolo\" não existe: o except mostra a mensagem e o programa continua."),
           TYPE('try:\n    total = "5" + 3\nexcept TypeError as e:\n    print(type(e).__name__)',
                "Texto + número é TypeError; type(e).__name__ mostra esse nome."),
           ORDER("Monte a função que recusa idade negativa com raise.",
                 ['def idade_valida(idade):', '    if idade < 0:', '        raise ValueError("idade negativa")', '    return idade', 'print(idade_valida(20))'],
                 "O raise fica dentro do if; o return só acontece quando a idade é válida.")]),
        # lição 4
        L("Módulos: import",
          "Módulos são caixas de ferramentas prontas. import math traz o módulo inteiro, e você usa com ponto: math.sqrt (raiz quadrada), math.floor (arredonda para baixo), math.ceil (para cima). from math import pi traz só pi, sem precisar do math. na frente. O módulo random sorteia valores; random.seed(n) fixa o sorteio para ele se repetir igual.",
          'import math\nprint(math.sqrt(81))\nprint(math.floor(4.7))\n\nfrom math import pi\nprint(pi > 3)\n\nimport random\nrandom.seed(1)\ndado = random.randint(1, 6)\nprint(dado >= 1 and dado <= 6)',
          [OUT('import math\nprint(math.sqrt(16))',
               ["4", "16", "256"],
               "math.sqrt devolve um float: 4.0."),
           FILL("Complete para trazer só o pi do módulo math.",
                'from math ___ pi\nprint(pi > 3)',
                "import", ["get", "use", "include"],
                "from módulo import nome traz só aquele nome."),
           MC("O que acontece em print(math.sqrt(9)) sem import math antes?",
              "Dá NameError: math ainda não existe",
              ["Mostra 3.0", "Mostra 3", "O Python importa sozinho"],
              "Sem import, o nome math não foi criado."),
           TYPE('import math\nprint(math.ceil(2.1))',
                "math.ceil arredonda sempre para cima: 3.")]),
        # lição 5
        L("Arquivos: with open",
          'open(nome, "w", encoding="utf-8") abre um arquivo para escrever (e apaga o que tinha). O modo "a" acrescenta no final. Sem modo, abre só para ler, e .read() devolve o texto todo. Usando with, o arquivo é fechado sozinho no fim do bloco, mesmo se der erro.',
          'with open("lista.txt", "w", encoding="utf-8") as arq:\n    arq.write("arroz\\n")\n    arq.write("feijão\\n")\n\nwith open("lista.txt", "a", encoding="utf-8") as arq:\n    arq.write("café\\n")\n\nwith open("lista.txt", encoding="utf-8") as arq:\n    texto = arq.read()\nprint(texto)',
          [OUT('with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("oi")\nwith open("a.txt", "w", encoding="utf-8") as f:\n    f.write("tchau")\nwith open("a.txt", encoding="utf-8") as f:\n    print(f.read())',
               ["oitchau", "oi", "oi\ntchau"],
               'O modo "w" apaga o conteúdo antigo. Só sobra tchau.'),
           TYPE('with open("a.txt", "w", encoding="utf-8") as f:\n    f.write("oi")\nwith open("a.txt", "a", encoding="utf-8") as f:\n    f.write("tchau")\nwith open("a.txt", encoding="utf-8") as f:\n    print(f.read())',
                'O modo "a" acrescenta no final, sem quebra de linha: oitchau.'),
           MC("Por que usar with open(...)?",
              "Ele fecha o arquivo sozinho no fim do bloco, mesmo se der erro",
              ["Ele deixa o arquivo mais rápido", "Sem with não dá para abrir arquivo", "Ele apaga o arquivo no final"],
              "Arquivo esquecido aberto pode perder dados; o with garante o fechamento."),
           CODE('Escreva o texto Olá, arquivo! no arquivo saida.txt. Use with open no modo "w" e encoding="utf-8".',
                "# escreva no arquivo saida.txt\n",
                'with open("saida.txt", "w", encoding="utf-8") as f:\n    f.write("Olá, arquivo!")\n',
                'try:\n    with open("saida.txt", encoding="utf-8") as f:\n        conteudo = f.read()\nexcept FileNotFoundError:\n    conteudo = None\nassert conteudo is not None, "O arquivo saida.txt não foi criado"\nassert conteudo.strip() == "Olá, arquivo!", "O arquivo deve conter: Olá, arquivo!"',
                'with open("saida.txt", "w", encoding="utf-8") as f: f.write("Olá, arquivo!")')]),
        # lição 6
        L("Classes e objetos",
          "Uma classe é um molde; cada objeto criado com ela tem seus próprios dados. O __init__ roda ao criar o objeto, e self é o próprio objeto: self.nome = nome guarda um atributo. Métodos são funções da classe e sempre recebem self primeiro. Todo valor é objeto de uma classe: type(5) is int dá True.",
          'class Cachorro:\n    def __init__(self, nome, idade):\n        self.nome = nome\n        self.idade = idade\n\n    def latir(self):\n        print(f"{self.nome} diz: Au au!")\n\nrex = Cachorro("Rex", 3)\nbolt = Cachorro("Bolt", 5)\nrex.latir()\nprint(bolt.idade)\nprint(type(rex).__name__)\nprint(type(5) is int)',
          [OUT('class Conta:\n    def __init__(self, saldo):\n        self.saldo = saldo\n\n    def depositar(self, valor):\n        self.saldo = self.saldo + valor\n\nc = Conta(100)\nc.depositar(50)\nprint(c.saldo)',
               ["100", "50", "None"],
               "depositar soma 50 ao saldo guardado em self.saldo: 150."),
           FILL("Complete o primeiro parâmetro do __init__.",
                'class Gato:\n    def __init__(___, nome):\n        self.nome = nome\n\ng = Gato("Mia")\nprint(g.nome)',
                "self", ["this", "nome", "Gato"],
                "O primeiro parâmetro de um método é sempre self, o próprio objeto."),
           TYPE('print(type([1, 2]).__name__)',
                "Uma lista é um objeto da classe list."),
           CODE("Crie a classe Retangulo: o __init__(self, largura, altura) guarda os dois valores em self.largura e self.altura, e o método area(self) DEVOLVE largura vezes altura.",
                "class Retangulo:\n    def __init__(self, largura, altura):\n        pass\n\n    def area(self):\n        pass\n",
                "class Retangulo:\n    def __init__(self, largura, altura):\n        self.largura = largura\n        self.altura = altura\n\n    def area(self):\n        return self.largura * self.altura\n",
                'r = Retangulo(3, 4)\nassert getattr(r, "largura", None) == 3, "Guarde a largura em self.largura"\nassert getattr(r, "altura", None) == 4, "Guarde a altura em self.altura"\nassert r.area() == 12, "Retangulo(3, 4).area() deve devolver 12"\nassert Retangulo(5, 2).area() == 10, "Retangulo(5, 2).area() deve devolver 10"',
                "Guarde os valores em self no __init__ e use self.largura * self.altura no return.")]),
    ],
}

BUGS = r'''
@base3 2
def dobro(n):
    n * 2
print(dobro(4))  # esperado: 8
>>> return n * 2
!! Sem return, a função devolve None. Use return para devolver o valor.

@base3 2
class Gato:
    def miar():
        print("Miau")
g = Gato()
g.miar()
>>> def miar(self):
!! Todo método recebe self como primeiro parâmetro.

@base3 3
try:
    print(10 / 0)
except ValueError:
    print("Não dá para dividir por zero")
>>> except ZeroDivisionError:
!! Dividir por zero gera ZeroDivisionError, não ValueError.

@base3 2
import math
raiz = sqrt(49)
print(raiz)
>>> raiz = math.sqrt(49)
!! Com import math, as funções se usam com math. na frente.

@base3 1
with open("notas.txt", "r", encoding="utf-8") as f:
    f.write("10")
>>> with open("notas.txt", "w", encoding="utf-8") as f:
!! O modo "r" só lê. Para escrever, use "w".

@base3 3
class Pet:
    def __init__(self, nome):
        nome = nome
p = Pet("Rex")
print(p.nome)
>>> self.nome = nome
!! Para virar atributo do objeto, guarde em self.nome.
'''
