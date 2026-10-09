from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L


def c(texto):
    """Tira a primeira quebra de linha e a última, para escrever código em blocos."""
    return texto.strip("\n")


LICOES = {
    # ================================================================ property
    "property": [
        # lição 2
        L("Setter: mudando com regras",
          "Uma property pode ter um setter: um método que roda quando você atribui um valor. Você cria com @nome.setter e guarda o valor de verdade num atributo com _ na frente, como self._idade.",
          c('''
class Pet:
    def __init__(self, idade):
        self._idade = idade

    @property
    def idade(self):
        return self._idade

    @idade.setter
    def idade(self, valor):
        if valor < 0:
            valor = 0
        self._idade = valor

p = Pet(3)
p.idade = -5
print(p.idade)
p.idade = 4
print(p.idade)
'''),
          [OUT(c('''
class Nota:
    def __init__(self):
        self._v = 0
    @property
    def v(self):
        return self._v
    @v.setter
    def v(self, x):
        self._v = min(x, 10)
n = Nota()
n.v = 15
print(n.v)
'''), ["15", "0", "Erro"], "O setter roda na atribuição e limita o valor a 10."),
           FILL("Complete o decorador do setter.", c('''
class Conta:
    @property
    def saldo(self):
        return self._saldo
    @___
    def saldo(self, valor):
        self._saldo = valor
'''), "saldo.setter", ["property.setter", "setter", "saldo.set"], "O setter usa o nome da property: @saldo.setter."),
           MC("Por que o valor real fica em self._idade, e não em self.idade?",
              "Porque self.idade = ... chamaria o próprio setter de novo, sem fim",
              ["Porque o _ deixa o código mais rápido", "Porque o Python exige _ em todo atributo", "Porque o _ apaga o valor antigo"],
              "self.idade é a property. O valor guardado precisa de outro nome, e o _ avisa que ele é interno."),
           TYPE(c('''
class Jogo:
    def __init__(self):
        self._nivel = 1
    @property
    def nivel(self):
        return self._nivel
    @nivel.setter
    def nivel(self, n):
        self._nivel = n
j = Jogo()
j.nivel = j.nivel + 2
print(j.nivel)
'''), "O getter lê 1, soma 2, e o setter guarda 3.")]),
        # lição 3
        L("Valores sempre atualizados",
          "Uma property calculada é refeita a cada acesso. Se os dados mudam, o resultado muda junto, sem você guardar nada a mais. Ótimo para totais, nomes completos e conversões.",
          c('''
class Carrinho:
    def __init__(self):
        self.precos = []

    @property
    def total(self):
        return sum(self.precos)

c = Carrinho()
c.precos.append(10)
print(c.total)
c.precos.append(5)
print(c.total)
'''),
          [OUT(c('''
class Pessoa:
    def __init__(self, nome, sobrenome):
        self.nome = nome
        self.sobrenome = sobrenome
    @property
    def completo(self):
        return f"{self.nome} {self.sobrenome}"
p = Pessoa("Ana", "Lima")
p.nome = "Bia"
print(p.completo)
'''), ["Ana Lima", "Bia", "Erro"], "A property é calculada na hora do acesso, já com o nome novo."),
           TYPE(c('''
class Temp:
    def __init__(self, c):
        self.c = c
    @property
    def f(self):
        return self.c * 9 / 5 + 32
print(Temp(100).f)
'''), "100 * 9 / 5 + 32 dá 212.0 (a divisão / gera float)."),
           MC("Qual a vantagem de total ser uma property, e não um atributo calculado uma vez no __init__?",
              "Ela recalcula a cada acesso, então nunca fica desatualizada",
              ["Ela ocupa menos memória sempre", "Ela deixa o valor imutável para sempre", "Ela roda só uma vez e guarda o resultado"],
              "Um atributo calculado no __init__ congela o valor; a property acompanha as mudanças."),
           CODE("Crie na classe Retangulo uma property perimetro que devolve 2 * (largura + altura).",
                c('''
class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    # crie a property perimetro aqui
''') + "\n",
                c('''
class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

    @property
    def perimetro(self):
        return 2 * (self.largura + self.altura)
'''),
                c('''
r = Retangulo(3, 4)
assert r.perimetro == 14, "Retangulo(3, 4).perimetro deve ser 14"
r.largura = 10
assert r.perimetro == 28, "Depois de mudar a largura para 10, o perímetro deve ser 28"
assert isinstance(Retangulo.__dict__.get("perimetro"), property), "perimetro precisa ser uma @property"
'''),
                "@property em cima de def perimetro(self), devolvendo 2 * (self.largura + self.altura).")]),
        # lição 4
        L("Pegadinhas da property",
          "Três erros clássicos: chamar com parênteses (q.area() tenta chamar o número), atribuir a uma property sem setter (AttributeError) e, no setter, escrever self.nome = valor em vez de self._nome = valor, o que chama o setter sem parar (RecursionError).",
          c('''
class Quadrado:
    def __init__(self, lado):
        self.lado = lado

    @property
    def area(self):
        return self.lado ** 2

q = Quadrado(3)
try:
    q.area = 50
except AttributeError as e:
    print("Sem setter:", type(e).__name__)
try:
    q.area()
except TypeError as e:
    print("Com parênteses:", type(e).__name__)
'''),
          [OUT(c('''
class Q:
    @property
    def x(self):
        return 5
try:
    print(Q().x())
except TypeError:
    print("TypeError")
'''), ["5", "x", "None"], "Q().x já vale 5; 5() tenta chamar um número e dá TypeError."),
           OUT(c('''
class P:
    @property
    def cor(self):
        return "azul"
p = P()
try:
    p.cor = "verde"
except AttributeError:
    print("não deu")
print(p.cor)
'''), ["verde", "azul", "não deu\nverde"], "Sem setter, a atribuição falha e a cor continua azul."),
           MC("No setter de saldo, o que acontece com self.saldo = valor?",
              "O setter chama a si mesmo sem parar e dá RecursionError",
              ["Funciona normalmente", "Cria um atributo comum e desliga a property", "Dá SyntaxError"],
              "Atribuir a self.saldo chama o setter de saldo de novo. Guarde em self._saldo."),
           FILL("Complete o setter sem cair em recursão.", c('''
class Pet:
    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, v):
        ___ = v.title()
'''), "self._nome", ["self.nome", "nome", "Pet.nome"], "O valor real fica em self._nome, que o getter lê.")]),
        # lição 5
        L("property() sem decorador",
          "O @property é um atalho. Dá para escrever preco = property(pegar, mudar) na classe, passando as funções. E, como properties parecem atributos, funcionam direitinho com getattr, max, sorted e listas.",
          c('''
class Produto:
    def __init__(self, preco):
        self._preco = preco

    def _pegar(self):
        return self._preco

    def _mudar(self, v):
        self._preco = max(v, 0)

    preco = property(_pegar, _mudar)

p = Produto(10)
p.preco = -3
print(p.preco)
p.preco = 8
print(getattr(p, "preco"))
'''),
          [OUT(c('''
class A:
    def _x(self):
        return 7
    x = property(_x)
print(A().x + 1)
'''), ["7", "Erro", "<property object>"], "property(_x) transforma _x num getter: A().x vale 7."),
           TYPE(c('''
class Item:
    def __init__(self, nome, qtd):
        self.nome, self.qtd = nome, qtd
    @property
    def esgotado(self):
        return self.qtd == 0
itens = [Item("pão", 0), Item("leite", 3), Item("ovo", 0)]
print([i.nome for i in itens if i.esgotado])
'''), "Só pão e ovo têm quantidade 0."),
           OUT(c('''
class Aluno:
    def __init__(self, nome, notas):
        self.nome, self.notas = nome, notas
    @property
    def media(self):
        return sum(self.notas) / len(self.notas)
turma = [Aluno("Ana", [8, 6]), Aluno("Caio", [9, 9]), Aluno("Bia", [5, 7])]
melhor = max(turma, key=lambda a: a.media)
print(melhor.nome, melhor.media)
'''), ["Caio 9", "Ana 7.0", "Bia 6.0"], "max usa a media de cada aluno; a de Caio é 9.0 (a divisão gera float)."),
           MC("O que property(pegar, mudar) faz?",
              "Cria uma property com pegar como getter e mudar como setter",
              ["Chama pegar e mudar na hora", "Cria dois atributos, pegar e mudar", "Dá erro: property só funciona com @"],
              "É o mesmo que usar @property e @nome.setter.")]),
        # lição 6
        L("Desafio: termômetro",
          "Junte getter, setter e cálculo: guarde a temperatura em _c, valide no setter e ofereça outra property que converte. Repare que o __init__ usa o próprio setter, então o valor inicial também é validado.",
          c('''
class Termometro:
    def __init__(self, c):
        self.celsius = c

    @property
    def celsius(self):
        return self._c

    @celsius.setter
    def celsius(self, v):
        self._c = max(v, -273)

    @property
    def fahrenheit(self):
        return self._c * 9 / 5 + 32

t = Termometro(-300)
print(t.celsius)
t.celsius = 25
print(t.fahrenheit)
'''),
          [OUT(c('''
class Senha:
    def __init__(self, s):
        self.texto = s
    @property
    def texto(self):
        return self._t
    @texto.setter
    def texto(self, s):
        self._t = s if len(s) >= 4 else "1234"
print(Senha("ab").texto)
'''), ["ab", "Erro", "None"], "O __init__ passa pelo setter, que troca senhas curtas por 1234."),
           ORDER("Monte a classe com getter e setter de vida.",
                 ["class Heroi:", "    @property", "    def vida(self):", "        return self._vida",
                  "    @vida.setter", "    def vida(self, v):", "        self._vida = max(0, v)"],
                 "Primeiro o getter com @property, depois o setter com @vida.setter."),
           MC("Por que o __init__ faz self.celsius = c (sem _)?",
              "Para que o valor inicial também passe pela validação do setter",
              ["Porque _c não pode ser usado no __init__", "Para criar uma segunda cópia do valor", "Porque o getter só funciona assim"],
              "self.celsius = c chama o setter, que guarda em _c já validado."),
           CODE('Crie a classe ContaBancaria com uma property saldo (guardada em self._saldo, que começa em 0). O setter não pode deixar o saldo negativo: valores menores que 0 viram 0. Crie também uma property em_reais que devolve f"R$ {self._saldo:.2f}".',
                c('''
class ContaBancaria:
    def __init__(self):
        self._saldo = 0

    # property saldo (getter e setter)

    # property em_reais
''') + "\n",
                c('''
class ContaBancaria:
    def __init__(self):
        self._saldo = 0

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, v):
        self._saldo = max(v, 0)

    @property
    def em_reais(self):
        return f"R$ {self._saldo:.2f}"
'''),
                c('''
c = ContaBancaria()
assert c.saldo == 0, "O saldo começa em 0"
c.saldo = 150.5
assert c.saldo == 150.5, "Depois de c.saldo = 150.5, o saldo deve ser 150.5"
c.saldo = -20
assert c.saldo == 0, "Um valor negativo deve virar 0"
c.saldo = 7
assert c.em_reais == "R$ 7.00", "em_reais deve devolver R$ 7.00 quando o saldo é 7"
'''),
                "Getter devolve self._saldo, o setter guarda max(v, 0) e em_reais formata com :.2f.")]),
    ],

    # ================================================================ staticmethod
    "staticmethod": [
        # lição 2
        L("Chamando de vários jeitos",
          "Você chama um staticmethod pela classe (Classe.f()) ou por um objeto (obj.f()). Dentro de outros métodos da classe, use self.f() ou Classe.f(): o nome sozinho não é encontrado.",
          c('''
class Conversor:
    @staticmethod
    def km_para_m(km):
        return km * 1000

    def mostrar(self, km):
        print(km, "km =", self.km_para_m(km), "m")

print(Conversor.km_para_m(2))
Conversor().mostrar(3)
'''),
          [OUT(c('''
class M:
    @staticmethod
    def triplo(n):
        return n * 3
    def calc(self):
        return M.triplo(2) + self.triplo(1)
print(M().calc())
'''), ["6", "Erro", "3"], "M.triplo(2) é 6 e self.triplo(1) é 3: total 9."),
           TYPE(c('''
class Texto:
    @staticmethod
    def grita(t):
        return t.upper() + "!"
print(Texto().grita("oi"))
'''), "Chamado por um objeto, funciona igual: OI!"),
           MC("Dentro de um método normal, como chamar o staticmethod limpar da mesma classe?",
              "self.limpar(...) ou NomeDaClasse.limpar(...)",
              ["limpar(...) sozinho", "super.limpar(...)", "staticmethod.limpar(...)"],
              "Sozinho, o nome limpar não existe fora da classe e dá NameError."),
           FILL("Complete para chamar o método estático pela classe.", c('''
class Dado:
    @staticmethod
    def faces():
        return 6
print(___.faces())
'''), "Dado", ["self", "cls", "staticmethod"], "Pela classe: Dado.faces(). self e cls não existem fora dos métodos.")]),
        # lição 3
        L("Utilitários organizados",
          "Use staticmethod para funções que têm a ver com a classe, mas não precisam de nenhum dado dela: validar uma senha, converter unidades, formatar preço. Fica tudo no mesmo lugar, com nome claro.",
          c('''
class Loja:
    @staticmethod
    def formatar(preco):
        return f"R$ {preco:.2f}"

    @staticmethod
    def preco_valido(preco):
        return preco > 0

print(Loja.formatar(9.5))
print(Loja.preco_valido(-2))
'''),
          [OUT(c('''
class Senha:
    @staticmethod
    def forte(s):
        return len(s) >= 8 and any(c.isdigit() for c in s)
print(Senha.forte("banana"), Senha.forte("banana123"))
'''), ["True True", "False False", "True False"], "banana é curta e sem número; banana123 tem 9 letras e números."),
           TYPE(c('''
class Nota:
    @staticmethod
    def conceito(n):
        return "A" if n >= 9 else "B" if n >= 7 else "C"
print(Nota.conceito(8))
'''), "8 não chega a 9, mas é pelo menos 7: B."),
           MC("Quando um staticmethod é uma boa escolha?",
              "Quando a função não usa self nem a classe, mas faz sentido ficar nela",
              ["Quando o método precisa mudar atributos do objeto", "Quando você quer criar objetos de outro jeito", "Sempre: ele é mais rápido que qualquer método"],
              "Para mexer no objeto, use método normal; para criar objetos, classmethod."),
           CODE("Crie a classe Calculadora com um staticmethod media(a, b, c) que devolve a média dos três números.",
                c('''
class Calculadora:
    def media(a, b, c):
        pass
''') + "\n",
                c('''
class Calculadora:
    @staticmethod
    def media(a, b, c):
        return (a + b + c) / 3
'''),
                c('''
assert Calculadora.media(6, 7, 8) == 7, "media(6, 7, 8) deve ser 7"
assert Calculadora().media(1, 2, 3) == 2, "Também deve funcionar por um objeto: media(1, 2, 3) == 2"
assert isinstance(Calculadora.__dict__["media"], staticmethod), "Use @staticmethod"
'''),
                "@staticmethod e return (a + b + c) / 3. Os parênteses garantem a soma antes da divisão.")]),
        # lição 4
        L("Pegadinhas do staticmethod",
          "Sem @staticmethod, chamar o método por um objeto passa o objeto como primeiro argumento e dá TypeError. E dentro de um staticmethod não existe self: ele não enxerga os atributos do objeto.",
          c('''
class Sem:
    def oi(nome):
        return "oi " + nome

class Com:
    @staticmethod
    def oi(nome):
        return "oi " + nome

print(Com().oi("Ana"))
try:
    Sem().oi("Ana")
except TypeError as e:
    print("Sem o decorador:", type(e).__name__)
'''),
          [OUT(c('''
class A:
    def dobro(n):
        return n * 2
print(A.dobro(4))
'''), ["Erro", "4", "None"], "Pela classe funciona: o Python não passa nada extra. O problema só aparece ao chamar por um objeto."),
           OUT(c('''
class B:
    def dobro(n):
        return n * 2
try:
    print(B().dobro(4))
except TypeError:
    print("TypeError")
'''), ["8", "4", "None"], "Pelo objeto, o Python passa o próprio objeto e mais o 4: dois argumentos para um parâmetro."),
           MC("Um staticmethod tenta usar self.nome. O que acontece?",
              "NameError: self não existe ali",
              ["Funciona, o Python cria self sozinho", "Ele recebe o objeto mesmo assim", "Devolve None"],
              "staticmethod não recebe self. Se precisa do objeto, use um método normal."),
           FILL("O método não usa self. Complete para ele funcionar também por um objeto.", c('''
class Relogio:
    ___
    def horas_em_min(h):
        return h * 60
print(Relogio().horas_em_min(2))
'''), "@staticmethod", ["@property", "staticmethod", "@self"], "Com @staticmethod, o objeto não é passado como primeiro argumento.")]),
        # lição 5
        L("Com map, sorted e filter",
          "Um staticmethod é uma função comum, então dá para passar Classe.metodo (sem parênteses) para map, filter ou para o key do sorted.",
          c('''
class Texto:
    @staticmethod
    def limpar(t):
        return t.strip().lower()

nomes = ["  Ana", "BIA ", " Caio "]
print(list(map(Texto.limpar, nomes)))
'''),
          [OUT(c('''
class Num:
    @staticmethod
    def par(n):
        return n % 2 == 0
print(list(filter(Num.par, [1, 2, 3, 4])))
'''), ["[1, 3]", "[False, True, False, True]", "2"], "filter mantém os números em que Num.par devolve True."),
           TYPE(c('''
class Ordem:
    @staticmethod
    def tamanho(p):
        return len(p)
print(sorted(["melancia", "uva", "kiwi"], key=Ordem.tamanho))
'''), "Ordena pelo tamanho: 3, 4 e 8 letras."),
           MC("Por que passamos Num.par, e não Num.par(), para o filter?",
              "Porque o filter precisa da função, não do resultado dela",
              ["Porque com parênteses fica mais lento", "Tanto faz, os dois funcionam", "Porque staticmethod não aceita parênteses"],
              "Num.par() tentaria rodar a função na hora, sem o número, e daria erro."),
           CODE("Na classe Precos, faça o staticmethod com_desconto(valor) devolver valor * 0.9. Depois troque a lista novos pelo resultado de aplicar o método a [100, 50, 20] com map.",
                c('''
class Precos:
    @staticmethod
    def com_desconto(valor):
        pass

novos = []
''') + "\n",
                c('''
class Precos:
    @staticmethod
    def com_desconto(valor):
        return valor * 0.9

novos = list(map(Precos.com_desconto, [100, 50, 20]))
'''),
                c('''
assert Precos.com_desconto(10) == 9, "com_desconto(10) deve ser 9.0"
assert novos == [90.0, 45.0, 18.0], "novos deve ser [90.0, 45.0, 18.0]"
'''),
                "return valor * 0.9 e novos = list(map(Precos.com_desconto, [100, 50, 20])).")]),
        # lição 6
        L("Desafio: caixa de ferramentas",
          "Uma classe pode juntar vários staticmethods, como uma caixa de ferramentas. Um pode até usar o outro, chamando pelo nome da classe.",
          c('''
class Medidas:
    @staticmethod
    def cm_para_m(cm):
        return cm / 100

    @staticmethod
    def imc(peso, altura_cm):
        m = Medidas.cm_para_m(altura_cm)
        return round(peso / m ** 2, 1)

print(Medidas.imc(70, 175))
'''),
          [OUT(c('''
class F:
    @staticmethod
    def a(x):
        return x + 1
    @staticmethod
    def b(x):
        return F.a(x) * 2
print(F.b(3))
'''), ["7", "6", "Erro"], "F.a(3) é 4, e 4 * 2 é 8."),
           ORDER("Monte a classe com um staticmethod e use-o.",
                 ["class Moeda:", "    @staticmethod", "    def real(v):", '        return f"R$ {v:.2f}"', "print(Moeda.real(3))"],
                 "O decorador vem logo antes do def, e a chamada fica fora da classe."),
           MC("Qual NÃO é um bom uso de staticmethod?",
              "Um método que muda self.pontos do jogador",
              ["Converter graus Celsius em Fahrenheit", "Verificar se um e-mail tem @", "Formatar um preço como texto"],
              "Mudar self.pontos precisa do objeto, então pede um método normal."),
           CODE('Crie a classe Validador com dois staticmethods: email_ok(t), que devolve True se o texto tem "@" e termina com ".com", e todos_ok(lista), que devolve True só se todos os e-mails passarem em email_ok (use all e Validador.email_ok).',
                c('''
class Validador:
    @staticmethod
    def email_ok(t):
        pass

    @staticmethod
    def todos_ok(lista):
        pass
''') + "\n",
                c('''
class Validador:
    @staticmethod
    def email_ok(t):
        return "@" in t and t.endswith(".com")

    @staticmethod
    def todos_ok(lista):
        return all(Validador.email_ok(e) for e in lista)
'''),
                c('''
assert Validador.email_ok("ana@pypasso.com") is True, "ana@pypasso.com é válido"
assert Validador.email_ok("ana.com") is False, "Sem @ não é válido"
assert Validador.email_ok("ana@site.org") is False, "Precisa terminar com .com"
assert Validador.todos_ok(["a@b.com", "c@d.com"]) is True, "Todos válidos: deve dar True"
assert Validador.todos_ok(["a@b.com", "errado"]) is False, "Com um inválido, deve dar False"
'''),
                'email_ok: "@" in t and t.endswith(".com"). todos_ok: all(Validador.email_ok(e) for e in lista).')]),
    ],

    # ================================================================ classmethod
    "classmethod": [
        # lição 2
        L("cls muda com a herança",
          "Quando uma classe filha chama um classmethod herdado, cls passa a ser a filha. Por isso return cls() cria o objeto do tipo certo, e cls.__name__ mostra o nome da filha.",
          c('''
class Animal:
    @classmethod
    def criar(cls):
        print("Criando", cls.__name__)
        return cls()

class Gato(Animal):
    pass

g = Gato.criar()
print(type(g).__name__)
'''),
          [OUT(c('''
class Veiculo:
    @classmethod
    def tipo(cls):
        return cls.__name__.lower()
class Moto(Veiculo):
    pass
print(Moto.tipo())
'''), ["veiculo", "Moto", "Erro"], "Chamado por Moto, cls é Moto, e lower() deixa minúsculo."),
           TYPE(c('''
class A:
    rodas = 4
    @classmethod
    def info(cls):
        return cls.rodas
class B(A):
    rodas = 2
print(A.info() + B.info())
'''), "Em A, cls.rodas é 4; em B, é 2. Soma: 6."),
           MC("Por que usar return cls() em vez de return Animal()?",
              "Assim as classes filhas criam objetos delas mesmas",
              ["Porque Animal() dá erro dentro da classe", "Porque cls() é mais rápido", "Não tem diferença nenhuma"],
              "Com Animal(), Gato.criar() devolveria um Animal, não um Gato."),
           FILL("Complete para o método funcionar também nas filhas.", c('''
class Forma:
    @classmethod
    def nova(cls):
        return ___()
class Bola(Forma):
    pass
print(type(Bola.nova()).__name__)
'''), "cls", ["Forma", "self", "super"], "cls() cria um objeto da classe que chamou: aqui, Bola.")]),
        # lição 3
        L("Construtores alternativos",
          "O uso mais comum: criar objetos a partir de outros formatos, como um texto, um dicionário ou valores prontos. O nome costuma começar com de_ ou descrever o modelo. No final, sempre return cls(...).",
          c('''
class Pizza:
    def __init__(self, sabores):
        self.sabores = sabores

    @classmethod
    def margherita(cls):
        return cls(["mussarela", "tomate", "manjericão"])

    @classmethod
    def de_texto(cls, texto):
        return cls(texto.split(", "))

print(Pizza.margherita().sabores)
print(Pizza.de_texto("calabresa, cebola").sabores)
'''),
          [OUT(c('''
class Hora:
    def __init__(self, h, m):
        self.h, self.m = h, m
    @classmethod
    def de_minutos(cls, total):
        return cls(total // 60, total % 60)
x = Hora.de_minutos(135)
print(x.h, x.m)
'''), ["135 0", "2.25 0", "15 2"], "135 // 60 é 2 e 135 % 60 é 15."),
           TYPE(c('''
class Ponto:
    def __init__(self, x, y):
        self.x, self.y = x, y
    @classmethod
    def de_dict(cls, d):
        return cls(d["x"], d["y"])
p = Ponto.de_dict({"x": 3, "y": 8})
print(p.x + p.y)
'''), "O dicionário vira Ponto(3, 8): 3 + 8."),
           MC("Qual destes é um bom construtor alternativo?",
              "Usuario.de_json(texto), que devolve cls(...)",
              ["Usuario.de_json(texto), que só imprime os dados", "Um método normal que muda self.nome", "Um staticmethod que devolve Usuario sempre fixo"],
              "Ele recebe a classe, monta os dados e devolve cls(...)."),
           CODE('Na classe Produto, crie o classmethod de_texto(cls, texto), que recebe algo como "café;12.5" e devolve um Produto com nome "café" e preco 12.5 (float).',
                c('''
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    @classmethod
    def de_texto(cls, texto):
        pass
''') + "\n",
                c('''
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    @classmethod
    def de_texto(cls, texto):
        nome, preco = texto.split(";")
        return cls(nome, float(preco))
'''),
                c('''
p = Produto.de_texto("café;12.5")
assert isinstance(p, Produto), "de_texto deve devolver um Produto (use return cls(...))"
assert p.nome == "café", "O nome deve ser café"
assert p.preco == 12.5, "O preço deve ser o número 12.5 (use float)"
'''),
                'nome, preco = texto.split(";") e return cls(nome, float(preco)).')]),
        # lição 4
        L("Pegadinhas do classmethod",
          "cls é a classe, não um objeto: atributos criados no __init__ (como self.nome) não existem em cls. E esquecer o return faz o construtor devolver None.",
          c('''
class Cliente:
    loja = "PyPasso"

    def __init__(self, nome):
        self.nome = nome

    @classmethod
    def info(cls):
        return cls.loja

    @classmethod
    def errado(cls):
        return cls.nome

print(Cliente.info())
try:
    Cliente.errado()
except AttributeError as e:
    print(type(e).__name__)
'''),
          [OUT(c('''
class C:
    @classmethod
    def novo(cls):
        cls()
print(C.novo())
'''), ["<C object>", "C", "Erro"], "O objeto é criado, mas sem return o método devolve None."),
           OUT(c('''
class Time:
    vitorias = 0
    @classmethod
    def venceu(cls):
        cls.vitorias += 1
a = Time()
b = Time()
Time.venceu()
a.venceu()
print(b.vitorias)
'''), ["1", "0", "Erro"], "Mesmo chamado por a, cls é Time. O contador é da classe, e todos os objetos veem 2."),
           MC("Dentro de um classmethod, cls.nome dá AttributeError quando…",
              "nome só é criado no __init__, como self.nome",
              ["nome é um atributo da classe", "a classe tem um método nome", "o parâmetro se chama cls"],
              "Atributos de objeto nascem no __init__; a classe em si não os tem."),
           FILL("Complete: o classmethod precisa receber a classe.", c('''
class Loja:
    nome = "Pipo Shop"
    @classmethod
    def titulo(___):
        return cls.nome.upper()
print(Loja.titulo())
'''), "cls", ["self", "nome", "Loja"], "O primeiro parâmetro recebe a classe; o corpo usa o nome cls.")]),
        # lição 5
        L("Contando e registrando",
          "classmethods combinam com atributos da classe: um contador de objetos, uma lista de registros, uma configuração compartilhada. Também dá para escrever nome = classmethod(funcao), sem o @.",
          c('''
class Jogador:
    criados = 0

    def __init__(self, nome):
        self.nome = nome
        Jogador.criados += 1

    @classmethod
    def quantos(cls):
        return f"{cls.criados} jogadores"

Jogador("Ana")
Jogador("Teo")
print(Jogador.quantos())
'''),
          [OUT(c('''
class Tarefa:
    lista = []
    def __init__(self, t):
        self.t = t
    @classmethod
    def adicionar(cls, t):
        obj = cls(t)
        cls.lista.append(obj)
        return obj
Tarefa.adicionar("lavar")
Tarefa.adicionar("estudar")
print([x.t for x in Tarefa.lista])
'''), ["['estudar']", "[]", "['lavar']"], "A lista é da classe e guarda as duas tarefas, na ordem."),
           TYPE(c('''
class Config:
    tema = "claro"
    @classmethod
    def trocar(cls):
        cls.tema = "escuro" if cls.tema == "claro" else "claro"
Config.trocar()
Config.trocar()
Config.trocar()
print(Config.tema)
'''), "Três trocas: escuro, claro, escuro."),
           OUT(c('''
class K:
    def _nome(cls):
        return cls.__name__ * 2
    nome = classmethod(_nome)
print(K.nome())
'''), ["K", "Erro", "_nome_nome"], "classmethod(_nome) faz cls ser K, e \"K\" * 2 é KK."),
           CODE("Na classe Pedido, o __init__ deve guardar self.numero = Pedido.proximo e depois somar 1 em Pedido.proximo. O classmethod total(cls) deve devolver quantos pedidos foram criados (cls.proximo - 1).",
                c('''
class Pedido:
    proximo = 1

    def __init__(self):
        pass

    @classmethod
    def total(cls):
        pass
''') + "\n",
                c('''
class Pedido:
    proximo = 1

    def __init__(self):
        self.numero = Pedido.proximo
        Pedido.proximo += 1

    @classmethod
    def total(cls):
        return cls.proximo - 1
'''),
                c('''
a = Pedido()
b = Pedido()
assert a.numero == 1 and b.numero == 2, "O primeiro pedido é o número 1 e o segundo, o 2"
assert Pedido.total() == 2, "Depois de criar 2 pedidos, total() deve ser 2"
'''),
                "O contador fica na classe (Pedido.proximo), e total lê cls.proximo - 1.")]),
        # lição 6
        L("Desafio: fábrica de personagens",
          "Juntando tudo: atributos de classe, cls e construtores alternativos. Um classmethod pode ler um dicionário de modelos guardado na classe e montar o objeto pronto.",
          c('''
class Personagem:
    modelos = {"mago": (60, 90), "guerreiro": (120, 10)}

    def __init__(self, vida, mana):
        self.vida, self.mana = vida, mana

    @classmethod
    def do_modelo(cls, nome):
        vida, mana = cls.modelos[nome]
        return cls(vida, mana)

m = Personagem.do_modelo("mago")
print(m.vida, m.mana)
'''),
          [OUT(c('''
class Cor:
    def __init__(self, r, g, b):
        self.rgb = (r, g, b)
    @classmethod
    def cinza(cls, n):
        return cls(n, n, n)
print(Cor.cinza(128).rgb)
'''), ["128", "[128, 128, 128]", "(128,)"], "cinza(128) vira Cor(128, 128, 128), e rgb é uma tupla."),
           ORDER("Monte a classe com um construtor de visitante.",
                 ["class Usuario:", "    def __init__(self, nome):", "        self.nome = nome", "    @classmethod",
                  "    def visitante(cls):", '        return cls("visitante")', "print(Usuario.visitante().nome)"],
                 "O @classmethod vem logo antes do def visitante(cls)."),
           MC("Qual a diferença entre staticmethod e classmethod?",
              "classmethod recebe a classe (cls); staticmethod não recebe nada automático",
              ["Nenhuma, são sinônimos", "staticmethod recebe self; classmethod não", "classmethod só funciona em classes filhas"],
              "Precisa da classe (para criar objetos ou ler atributos dela)? classmethod."),
           CODE('Na classe Data, crie dois classmethods: de_texto(cls, t), que aceita "25/12/2026", e de_iso(cls, t), que aceita "2026-12-25". Os dois devem devolver cls(dia, mes, ano) com números inteiros.',
                c('''
class Data:
    def __init__(self, dia, mes, ano):
        self.dia, self.mes, self.ano = dia, mes, ano

    # crie de_texto e de_iso aqui
''') + "\n",
                c('''
class Data:
    def __init__(self, dia, mes, ano):
        self.dia, self.mes, self.ano = dia, mes, ano

    @classmethod
    def de_texto(cls, t):
        d, m, a = map(int, t.split("/"))
        return cls(d, m, a)

    @classmethod
    def de_iso(cls, t):
        a, m, d = map(int, t.split("-"))
        return cls(d, m, a)
'''),
                c('''
x = Data.de_texto("25/12/2026")
assert (x.dia, x.mes, x.ano) == (25, 12, 2026), "de_texto('25/12/2026') deve dar dia 25, mês 12, ano 2026"
y = Data.de_iso("2026-03-07")
assert (y.dia, y.mes, y.ano) == (7, 3, 2026), "de_iso('2026-03-07') deve dar dia 7, mês 3, ano 2026"
class Feriado(Data):
    pass
assert isinstance(Feriado.de_texto("01/01/2027"), Feriado), "Use return cls(...) para funcionar nas classes filhas"
'''),
                "Divida o texto, converta com map(int, ...) e devolva cls(dia, mes, ano). No formato ISO, o ano vem primeiro.")]),
    ],

    # ================================================================ super
    "super": [
        # lição 2
        L("super em qualquer método",
          "super() não serve só para o __init__. Em qualquer método sobrescrito, super().metodo() pega o resultado da mãe para você completar, em vez de reescrever tudo.",
          c('''
class Produto:
    def __init__(self, nome):
        self.nome = nome

    def etiqueta(self):
        return f"Produto: {self.nome}"

class Bebida(Produto):
    def etiqueta(self):
        return super().etiqueta() + " (gelada)"

print(Bebida("suco").etiqueta())
'''),
          [OUT(c('''
class A:
    def falar(self):
        return "oi"
class B(A):
    def falar(self):
        return super().falar().upper() + "!"
print(B().falar())
'''), ["oi!", "OI", "oi"], "Pega oi da mãe, deixa maiúsculo e põe a exclamação."),
           TYPE(c('''
class Base:
    def bonus(self):
        return 10
class Vip(Base):
    def bonus(self):
        return super().bonus() * 3
print(Vip().bonus())
'''), "O bônus da mãe (10) vezes 3."),
           MC("Por que usar super().etiqueta() em vez de copiar o código da mãe?",
              "Se a mãe mudar, a filha acompanha sem você reescrever nada",
              ["Porque copiar código dá erro", "Porque super() deixa o método privado", "Porque assim a mãe deixa de existir"],
              "Reaproveitar evita código repetido e desatualizado."),
           FILL("Complete para somar 20 ao ataque da mãe.", c('''
class Inimigo:
    def ataque(self):
        return 5
class Chefe(Inimigo):
    def ataque(self):
        return ___.ataque() + 20
print(Chefe().ataque())
'''), "super()", ["super", "self", "Inimigo"], "super() com parênteses; self.ataque() chamaria o próprio método sem parar.")]),
        # lição 3
        L("Herança na prática",
          "Padrão comum: a filha recebe os mesmos dados da mãe e mais alguns. No __init__, ela passa para a mãe o que é dela, com super().__init__(...), e guarda o resto.",
          c('''
class Conta:
    def __init__(self, dono, saldo):
        self.dono = dono
        self.saldo = saldo

class Poupanca(Conta):
    def __init__(self, dono, saldo, juros):
        super().__init__(dono, saldo)
        self.juros = juros

    def render(self):
        self.saldo += self.saldo * self.juros

p = Poupanca("Ana", 100, 0.1)
p.render()
print(p.dono, p.saldo)
'''),
          [OUT(c('''
class Pet:
    def __init__(self, nome):
        self.nome = nome
        self.fome = 5
class Gato(Pet):
    def __init__(self, nome, cor):
        super().__init__(nome)
        self.cor = cor
g = Gato("Mia", "preto")
print(g.nome, g.cor, g.fome)
'''), ["Mia preto", "Erro", "preto Mia 5"], "O __init__ da mãe criou nome e fome; a filha criou cor."),
           TYPE(c('''
class Funcionario:
    def __init__(self, salario):
        self.salario = salario
    def pagamento(self):
        return self.salario
class Gerente(Funcionario):
    def pagamento(self):
        return super().pagamento() + 1000
print(Gerente(3000).pagamento())
'''), "Gerente usa o __init__ herdado; o pagamento é 3000 + 1000."),
           ORDER("Monte a filha que aproveita o __init__ da mãe.",
                 ["class Ave:", "    def __init__(self, nome):", "        self.nome = nome", "class Pinguim(Ave):",
                  "    def __init__(self):", '        super().__init__("Pingu")', "print(Pinguim().nome)"],
                 "A mãe vem antes da filha, e o super() fica dentro do __init__ da filha."),
           CODE("Crie o __init__ de Estagiario: ele recebe (nome, escola), chama super().__init__(nome, 1500) e guarda self.escola.",
                c('''
class Funcionario:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

class Estagiario(Funcionario):
    def __init__(self, nome, escola):
        self.escola = escola
''') + "\n",
                c('''
class Funcionario:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

class Estagiario(Funcionario):
    def __init__(self, nome, escola):
        super().__init__(nome, 1500)
        self.escola = escola
'''),
                c('''
e = Estagiario("Caio", "IFRJ")
assert e.escola == "IFRJ", "Guarde a escola em self.escola"
assert e.nome == "Caio", "O nome deve vir do __init__ da mãe (use super().__init__)"
assert e.salario == 1500, "O salário do estagiário deve ser 1500"
'''),
                "Coloque super().__init__(nome, 1500) no __init__ do Estagiario.")]),
        # lição 4
        L("Pegadinhas do super",
          "Erros comuns: escrever super sem parênteses (super.__init__), passar self de novo (super().__init__(self, nome)) e esquecer de chamar o __init__ da mãe. Lembre: super() já sabe quem é o self.",
          c('''
class Mae:
    def __init__(self, nome):
        self.nome = nome

class Filha(Mae):
    def __init__(self, nome):
        super().__init__(self, nome)

try:
    Filha("Lia")
except TypeError as e:
    print("Passou self duas vezes:", type(e).__name__)
'''),
          [OUT(c('''
class A:
    def __init__(self):
        self.x = 1
class B(A):
    def __init__(self):
        self.y = 2
b = B()
print(hasattr(b, "x"), hasattr(b, "y"))
'''), ["True True", "True False", "Erro"], "B não chamou super().__init__(), então o x da mãe nunca foi criado."),
           MC("O que está errado em super().__init__(self, nome)?",
              "O self vai duas vezes: super() já passa o objeto",
              ["Faltou o ponto antes de __init__", "super precisa do nome da mãe nos parênteses", "Nada, está certo"],
              "O certo é super().__init__(nome)."),
           OUT(c('''
class A:
    def oi(self):
        return "A"
class B(A):
    def oi(self):
        return "B"
class C(B):
    def oi(self):
        return super().oi()
print(C().oi())
'''), ["A", "C", "BA"], "super() em C pega a mãe mais próxima, que é B."),
           FILL("Complete a chamada ao __init__ da mãe.", c('''
class Loja:
    def __init__(self, nome):
        self.nome = nome
class Quiosque(Loja):
    def __init__(self, nome):
        ___.__init__(nome)
print(Quiosque("Pipo").nome)
'''), "super()", ["super", "self", "Loja"], "Sem os parênteses, super é só a classe super, e Loja.__init__(nome) ficaria sem o self.")]),
        # lição 5
        L("Três gerações e o MRO",
          "Com várias gerações, cada super() chama o próximo da fila. Essa fila se chama MRO (ordem de resolução de métodos), e você pode vê-la em Classe.__mro__. super() também funciona dentro de classmethods.",
          c('''
class A:
    def nome(self):
        return "A"

class B(A):
    def nome(self):
        return "B>" + super().nome()

class C(B):
    def nome(self):
        return "C>" + super().nome()

print(C().nome())
print([k.__name__ for k in C.__mro__])
'''),
          [OUT(c('''
class X:
    def __init__(self):
        self.passos = ["X"]
class Y(X):
    def __init__(self):
        super().__init__()
        self.passos.append("Y")
class Z(Y):
    def __init__(self):
        super().__init__()
        self.passos.append("Z")
print(Z().passos)
'''), ["['Z', 'Y', 'X']", "['Z']", "['X']"], "Cada um chama a mãe primeiro: X cria a lista, depois Y e Z acrescentam."),
           TYPE(c('''
class A:
    pass
class B(A):
    pass
print(len(B.__mro__))
'''), "A fila de B é B, A e object: 3 classes."),
           OUT(c('''
class Base:
    @classmethod
    def titulo(cls):
        return "base"
class Filha(Base):
    @classmethod
    def titulo(cls):
        return super().titulo() + "+filha"
print(Filha.titulo())
'''), ["filha", "base", "Erro"], "super() também funciona em classmethods: pega o titulo da mãe e completa."),
           CODE("Nivel1.pontos() devolve 10. Faça Nivel2 devolver os pontos da mãe + 5 e Nivel3 devolver os pontos da mãe vezes 2. Use super() nos dois.",
                c('''
class Nivel1:
    def pontos(self):
        return 10

class Nivel2(Nivel1):
    def pontos(self):
        return 0

class Nivel3(Nivel2):
    def pontos(self):
        return 0
''') + "\n",
                c('''
class Nivel1:
    def pontos(self):
        return 10

class Nivel2(Nivel1):
    def pontos(self):
        return super().pontos() + 5

class Nivel3(Nivel2):
    def pontos(self):
        return super().pontos() * 2
'''),
                c('''
assert Nivel2().pontos() == 15, "Nivel2 deve dar 10 + 5 = 15"
assert Nivel3().pontos() == 30, "Nivel3 deve dar 15 * 2 = 30"
'''),
                "Nivel2: super().pontos() + 5. Nivel3: super().pontos() * 2, que usa o resultado de Nivel2.")]),
        # lição 6
        L("Desafio: loja com herança",
          "Junte tudo: a filha aproveita o __init__ e os métodos da mãe com super() e só acrescenta o que muda.",
          c('''
class Item:
    def __init__(self, nome, preco):
        self.nome, self.preco = nome, preco

    def resumo(self):
        return f"{self.nome}: R$ {self.preco:.2f}"

class ItemPromo(Item):
    def __init__(self, nome, preco, desconto):
        super().__init__(nome, preco * (1 - desconto))
        self.desconto = desconto

    def resumo(self):
        return super().resumo() + f" ({self.desconto:.0%} off)"

print(ItemPromo("tênis", 200, 0.25).resumo())
'''),
          [OUT(c('''
class Msg:
    def texto(self):
        return "olá"
class MsgAlta(Msg):
    def texto(self):
        return super().texto().upper()
class MsgAltaFeliz(MsgAlta):
    def texto(self):
        return super().texto() + " :)"
print(MsgAltaFeliz().texto())
'''), ["olá :)", "OLÁ", "olá"], "A mãe direta já devolve OLÁ; a neta acrescenta o :)."),
           MC("Na filha, por que costumamos chamar super().__init__ antes de criar ou ajustar os próprios atributos?",
              "Porque a mãe prepara a base e a filha completa ou ajusta depois",
              ["Porque super() só pode ser a primeira linha do arquivo", "Porque depois do super() não dá para criar atributos", "Porque a ordem nunca importa"],
              "Se a filha mexer num atributo antes, o __init__ da mãe pode sobrescrevê-lo."),
           TYPE(c('''
class Conta:
    def __init__(self):
        self.saldo = 100
class ContaBonus(Conta):
    def __init__(self):
        super().__init__()
        self.saldo += 50
print(ContaBonus().saldo)
'''), "A mãe cria saldo = 100 e a filha soma 50."),
           CODE('Crie a classe Cachorro (filha de Animal) com __init__(self, nome, truque), usando super() para o nome e guardando self.truque. Crie também falar(self), que devolve o falar da mãe + f" e sabe {self.truque}".',
                c('''
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        return f"{self.nome} faz barulho"

class Cachorro(Animal):
    pass
''') + "\n",
                c('''
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        return f"{self.nome} faz barulho"

class Cachorro(Animal):
    def __init__(self, nome, truque):
        super().__init__(nome)
        self.truque = truque

    def falar(self):
        return super().falar() + f" e sabe {self.truque}"
'''),
                c('''
c = Cachorro("Rex", "sentar")
assert c.nome == "Rex", "O nome deve ser guardado pelo __init__ da mãe"
assert c.truque == "sentar", "Guarde o truque em self.truque"
assert c.falar() == "Rex faz barulho e sabe sentar", "falar() deve devolver: Rex faz barulho e sabe sentar"
'''),
                "super().__init__(nome) no __init__ e super().falar() + f\" e sabe {self.truque}\" no falar.")]),
    ],
}

BUGS = r'''
@fn_property 6
class Caixa:
    @property
    def total(self):
        return 10
c = Caixa()
print(c.total())
>>> print(c.total)
!! total é uma property: acesse sem parênteses.

@fn_property 5
class Conta:
    @property
    def saldo(self): return self._saldo
    @saldo.setter
    def saldo(self, v): self.saldo = v
c = Conta(); c.saldo = 5
print(c.saldo)
>>> def saldo(self, v): self._saldo = v
!! self.saldo chama o setter de novo, sem fim. Guarde em self._saldo.

@fn_property 4
class Temp:
    @property
    def c(self): return self._c
    @property
    def c(self, v): self._c = v
t = Temp(); t.c = 30
print(t.c)
>>> @c.setter
!! O setter usa @c.setter, não um segundo @property.

@fn_property 4
class Pedido:
    def __init__(self, itens): self.itens = itens
    @property
    def total(self): return len(self.itens)
p = Pedido([10, 20, 5])
print(p.total)  # esperado: 35
>>> def total(self): return sum(self.itens)
!! len conta os itens; o total é a soma dos preços.

@fn_property 6
class Circulo:
    def __init__(self, r): self.r = r
    @property
    def diametro(self): return self.r * 2
c = Circulo(3)
c.diametro = 10
print(c.r)  # esperado: 5
>>> c.r = 5
!! diametro não tem setter. Mude o raio, e o diâmetro acompanha.

@fn_property 4
class Pet:
    def __init__(self, n): self._n = n
    @property
    def nome(): return self._n.title()
print(Pet("rex").nome)
>>> def nome(self): return self._n.title()
!! A property também é um método: precisa receber self.

@fn_staticmethod 2
class Calc:
    @classmethod
    def dobro(n):
        return n * 2
print(Calc.dobro(4))
>>> @staticmethod
!! Com @classmethod, n recebe a classe e o 4 sobra. A função não usa a classe: é @staticmethod.

@fn_staticmethod 4
class Loja:
    taxa = 0.1
    @staticmethod
    def com_taxa(v): return v + v * self.taxa
print(Loja.com_taxa(100))
>>> def com_taxa(v): return v + v * Loja.taxa
!! Dentro de um staticmethod não existe self. Use o nome da classe.

@fn_staticmethod 2
class Conv:
    staticmethod
    def km_para_m(km): return km * 1000
print(Conv().km_para_m(2))
>>> @staticmethod
!! Faltou o @. Sem ele, staticmethod é só um nome solto e o método recebe o objeto.

@fn_staticmethod 4
class Util:
    @staticmethod
    def saudacao(): return "Olá!"
print(Util.saudacao)  # esperado: Olá!
>>> print(Util.saudacao())  # esperado: Olá!
!! Sem parênteses, você mostra a função em vez de chamá-la.

@fn_staticmethod 4
class Preco:
    @staticmethod
    def arred(v): return round(v, 2)
    def final(self, v): return arred(v * 1.1)
print(Preco().final(10))
>>> def final(self, v): return Preco.arred(v * 1.1)
!! Dentro da classe, chame pelo nome da classe ou por self: Preco.arred.

@fn_staticmethod 3
class Dado:
    @staticmethod
    def lados(self): return 6
print(Dado.lados())
>>> def lados(): return 6
!! staticmethod não recebe self. Tire o parâmetro que nunca chega.

@fn_classmethod 3
class Ponto:
    def __init__(self, x, y): self.x, self.y = x, y
    @staticmethod
    def origem(cls): return cls(0, 0)
p = Ponto.origem()
print(p.x, p.y)
>>> @classmethod
!! Para receber a classe em cls, o decorador é @classmethod.

@fn_classmethod 3
class Animal:
    @classmethod
    def novo(cls): return Animal()
class Gato(Animal): pass
print(type(Gato.novo()).__name__)  # esperado: Gato
>>> def novo(cls): return cls()
!! Animal() fixa o tipo. cls() cria um objeto da classe que chamou.

@fn_classmethod 4
class Data:
    def __init__(self, d, m): self.d, self.m = d, m
    @classmethod
    def de_texto(cls, t): cls(*map(int, t.split("/")))
x = Data.de_texto("07/10")
print(x.d)
>>> def de_texto(cls, t): return cls(*map(int, t.split("/")))
!! Faltou o return: o objeto é criado e jogado fora, e x vira None.

@fn_classmethod 3
class Jogador:
    total = 0
    def __init__(self): self.total += 1
    @classmethod
    def quantos(cls): return cls.total
Jogador(); Jogador()
print(Jogador.quantos())  # esperado: 2
>>> def __init__(self): Jogador.total += 1
!! self.total += 1 cria um atributo no objeto. O contador da classe fica em 0.

@fn_classmethod 4
class Produto:
    def __init__(self, nome, preco): self.nome, self.preco = nome, preco
    @classmethod
    def de_dict(cls, d): return cls(d["nome"])
p = Produto.de_dict({"nome": "pão", "preco": 1.5})
print(p.preco)
>>> def de_dict(cls, d): return cls(d["nome"], d["preco"])
!! cls(...) chama o __init__, que pede nome e preco.

@fn_classmethod 4
class Cor:
    @classmethod
    def padrao(cls): return cls.__name__ + " azul"
print(Cor.padrao(Cor))
>>> print(Cor.padrao())
!! O Python já passa a classe em cls. Não passe de novo.

@fn_super 4
class Animal:
    def __init__(self, nome): self.nome = nome
class Cao(Animal):
    def __init__(self, nome): super.__init__(nome)
print(Cao("Rex").nome)
>>> def __init__(self, nome): super().__init__(nome)
!! Faltaram os parênteses: é super(), não super.

@fn_super 4
class Conta:
    def __init__(self, dono): self.dono = dono
class Poupanca(Conta):
    def __init__(self, dono): super().__init__(self, dono)
print(Poupanca("Ana").dono)
>>> def __init__(self, dono): super().__init__(dono)
!! super() já passa o self. Mande só o dono.

@fn_super 5
class Pessoa:
    def __init__(self, nome): self.nome = nome
class Aluno(Pessoa):
    def __init__(self, nome, nota):
        super().__init__
        self.nota = nota
print(Aluno("Bia", 9).nome)
>>> super().__init__(nome)
!! Sem os parênteses e o nome, o __init__ da mãe não roda.

@fn_super 4
class Base:
    def desc(self): return "item"
class Livro(Base):
    def desc(self): return "livro " + self.desc()
print(Livro().desc())
>>> def desc(self): return "livro " + super().desc()
!! self.desc() chama o próprio método sem parar. A versão da mãe é super().desc().

@fn_super 4
class A:
    def preco(self): return 100
class B(A):
    def preco(self): super().preco() * 0.9
print(B().preco())  # esperado: 90.0
>>> def preco(self): return super().preco() * 0.9
!! Faltou o return: a conta é feita e o resultado se perde.

@fn_super 4
class Inimigo:
    def __init__(self, vida): self.vida = vida
class Chefe(Inimigo):
    def __init__(self): super().__init__()
print(Chefe().vida)  # esperado: 500
>>> def __init__(self): super().__init__(500)
!! O __init__ da mãe pede a vida. Passe 500 para ele.
'''
