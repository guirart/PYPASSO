from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================ object
    "object": [
        # lição 2
        L("Um marcador único",
          "Cada object() é único: só é igual a ele mesmo. Por isso ele serve de marcador para saber se a pessoa passou um argumento, mesmo quando ela passa None. Compare marcadores com is.",
          'FALTA = object()\n\ndef pegar(dic, chave, padrao=FALTA):\n    if chave in dic:\n        return dic[chave]\n    if padrao is FALTA:\n        return "sem padrão"\n    return padrao\n\nprint(pegar({"a": 1}, "a"))\nprint(pegar({}, "b"))\nprint(pegar({}, "b", None))',
          [OUT('a = object()\nb = object()\nprint(a == b, a is a)', ["True True", "False False", "True False"], "Dois object() diferentes nunca são iguais, mas cada um é ele mesmo."),
           TYPE('m = object()\nlista = [1, m, 3]\nprint(lista.index(m))', "O marcador m está na posição 1."),
           MC("Por que usar object() como marcador em vez de None?", "Porque None pode ser um valor que a pessoa passou de propósito", ["Porque object() é mais rápido", "Porque None dá erro em funções", "Porque object() vale zero"], "Com um marcador próprio, dá para diferenciar \"não passou nada\" de \"passou None\"."),
           FILL("Complete para testar se nada foi passado.", 'VAZIO = object()\ndef f(x=VAZIO):\n    if x ___ VAZIO:\n        return "nada"\n    return x\nprint(f())', "is", ["in", "=", "is not"], "is confere se é exatamente o mesmo objeto.")]),
        # lição 3
        L("O que vem de object",
          "Toda classe herda de object vários métodos prontos, como __init__, __str__ e __eq__. O __eq__ herdado compara identidade: dois objetos só são iguais se forem o mesmo. Em __bases__ você vê de quem a classe herda.",
          'class Vazio:\n    pass\n\nprint(Vazio.__bases__)\nprint(hasattr(Vazio(), "__str__"))\nv = Vazio()\nprint(v == v, v == Vazio())',
          [OUT('class A: pass\nprint(A.__bases__)', ["()", "(<class 'A'>,)", "None"], "Sem escrever nada, a base é object."),
           OUT('class A: pass\nprint(A() == A())', ["True", "Erro", "None"], "O __eq__ de object compara identidade, e são dois objetos diferentes."),
           MC("Sua classe não tem __init__. De onde vem o __init__ usado ao criar o objeto?", "Da classe object", ["Do módulo builtins", "Ele é criado vazio pelo print", "Dá erro ao criar o objeto"], "object fornece um __init__ que não faz nada."),
           TYPE('class A: pass\nprint(A.__mro__[-1].__name__)', "O último da cadeia de heranças é sempre object.")]),
        # lição 4
        L("Pegadinhas do object",
          "Um object() puro não aceita atributos novos: ele não tem __dict__. E object() não recebe argumentos. Para guardar dados, crie sua própria classe, mesmo que vazia.",
          'o = object()\ntry:\n    o.nome = "Pipo"\nexcept AttributeError:\n    print("object() não aceita atributos novos")\n\nclass Caixa:\n    pass\n\nc = Caixa()\nc.nome = "Pipo"\nprint(c.nome)',
          [OUT('o = object()\ntry:\n    o.x = 1\n    print("ok")\nexcept AttributeError:\n    print("não deu")', ["ok", "1", "Erro"], "object() puro não guarda atributos."),
           OUT('try:\n    object(5)\nexcept TypeError as e:\n    print(type(e).__name__)', ["ValueError", "5", "AttributeError"], "object() não recebe argumentos: TypeError."),
           MC("Você quer um objeto simples para pendurar atributos. O que usar?", "Uma classe sua: class Caixa: pass", ["object()", 'object(nome="x")', "dir()"], "Classes que você cria têm __dict__ e aceitam atributos."),
           TYPE('print(hasattr(object(), "__dict__"))', "object() não tem __dict__, por isso não guarda atributos.")]),
        # lição 5
        L("A raiz de tudo",
          "Como tudo herda de object, isinstance(x, object) é sempre True. A cadeia de herança, em __mro__, sempre termina em object. Isso vale até para bool, que herda de int.",
          'for valor in [1, "a", None, len, int]:\n    print(isinstance(valor, object), end=" ")\nprint()\nprint(bool.__mro__)',
          [OUT('print(int.__mro__)', ["(<class 'int'>,)", "(<class 'object'>, <class 'int'>)", "<class 'object'>"], "Primeiro a própria classe, depois object."),
           TYPE('print(issubclass(type, object))', "Até type herda de object."),
           ORDER("Monte o programa: Gato herda de Animal, e o final mostra que Gato também é object.",
                 ['class Animal:', '    som = "..."', 'class Gato(Animal):', '    som = "miau"', 'print(issubclass(Gato, object))'],
                 "Animal herda de object sem escrever, então Gato também."),
           CODE("Crie SEM = object() e a função saudacao(nome=SEM). Sem argumento, ela devolve \"Oi, visitante\". Com qualquer argumento, até None, devolve f\"Oi, {nome}\".",
                'SEM = object()\n\ndef saudacao(nome=None):\n    if nome is None:\n        return "Oi, visitante"\n    return f"Oi, {nome}"\n',
                'SEM = object()\n\ndef saudacao(nome=SEM):\n    if nome is SEM:\n        return "Oi, visitante"\n    return f"Oi, {nome}"',
                'assert saudacao() == "Oi, visitante", "Sem argumento: Oi, visitante"\nassert saudacao("Ana") == "Oi, Ana", "saudacao(\\"Ana\\") deve dar Oi, Ana"\nassert saudacao(None) == "Oi, None", "Passar None é diferente de não passar nada: Oi, None"',
                "Use SEM como padrão e compare com is SEM.")]),
        # lição 6
        L("Desafio: trocando o herdado",
          "Você pode reescrever métodos que vêm de object. Com __str__ você decide o texto que o print mostra; com __eq__ você decide quando dois objetos são iguais.",
          'class Nota:\n    def __init__(self, valor):\n        self.valor = valor\n    def __str__(self):\n        return f"Nota {self.valor}"\n    def __eq__(self, outra):\n        return self.valor == outra.valor\n\nprint(Nota(9))\nprint(Nota(7) == Nota(7))',
          [OUT('class Pet:\n    def __str__(self):\n        return "Pet fofo"\nprint(Pet())', ["<Pet object>", "Pet", "None"], "O print usa o __str__ que você escreveu."),
           TYPE('class P:\n    def __init__(self, x):\n        self.x = x\n    def __eq__(self, o):\n        return self.x == o.x\nprint(P(2) == P(2))', "Agora o __eq__ compara o x, não a identidade."),
           MC("Se você não escrever __eq__, P(2) == P(2) dá…", "False, porque compara se é o mesmo objeto", ["True, porque os valores são iguais", "Erro", "None"], "O __eq__ herdado de object compara identidade."),
           CODE("Crie a classe Moeda(valor). str(Moeda(5)) deve dar \"R$ 5.00\", e Moeda(2) == Moeda(2) deve dar True.",
                'class Moeda:\n    def __init__(self, valor):\n        self.valor = valor\n',
                'class Moeda:\n    def __init__(self, valor):\n        self.valor = valor\n    def __str__(self):\n        return f"R$ {self.valor:.2f}"\n    def __eq__(self, outra):\n        return self.valor == outra.valor',
                'assert str(Moeda(5)) == "R$ 5.00", "str(Moeda(5)) deve ser R$ 5.00"\nassert str(Moeda(2.5)) == "R$ 2.50", "str(Moeda(2.5)) deve ser R$ 2.50"\nassert Moeda(2) == Moeda(2), "Moedas com o mesmo valor devem ser iguais"\nassert not (Moeda(2) == Moeda(3)), "Valores diferentes não são iguais"',
                "Reescreva __str__ (com :.2f) e __eq__ (comparando valor).")]),
    ],

    # ================================================================ getattr
    "getattr": [
        # lição 2
        L("O valor padrão",
          "O terceiro argumento só é usado quando o atributo NÃO existe. Se ele existe, vem o valor dele, mesmo que seja 0 ou None. Sem padrão, faltar o atributo dá AttributeError.",
          'class Produto:\n    nome = "Caneca"\n    preco = 25\n\np = Produto()\nprint(getattr(p, "preco", 0))\nprint(getattr(p, "estoque", 0))\nprint(getattr(p, "cor", None))',
          [OUT('class A:\n    x = 0\nprint(getattr(A(), "x", 10))', ["10", "None", "Erro"], "x existe e vale 0, então o padrão não é usado."),
           OUT('class A: pass\ntry:\n    getattr(A(), "y")\nexcept AttributeError:\n    print("sem y")', ["None", "y", "AttributeError: y"], "Sem padrão, faltar o atributo dá AttributeError, que foi tratado."),
           TYPE('class A: pass\nprint(getattr(A(), "cor", "azul"))', "cor não existe, então vem o padrão."),
           FILL("Complete para não dar erro se faltar a idade.", 'class Pet:\n    nome = "Rex"\nprint(getattr(Pet(), "idade"___))', ", 0", [", default=0", " or 0", ".get(0)"], "O padrão é o terceiro argumento, sem nome: getattr não aceita default=.")]),
        # lição 3
        L("Nome guardado em variável",
          "A grande vantagem do getattr é escolher o atributo na hora: o nome pode vir de uma lista, de uma escolha do jogador ou de um laço. Funciona também com métodos.",
          'class Heroi:\n    def __init__(self):\n        self.forca = 8\n        self.magia = 3\n        self.vida = 10\n\nh = Heroi()\nfor atributo in ["forca", "magia", "vida"]:\n    print(atributo, getattr(h, atributo))',
          [OUT('class C:\n    a = 1\n    b = 2\nprint([getattr(C, n) for n in "ab"])', ["['a', 'b']", "[1]", "3"], "Para cada letra, pega o atributo com esse nome."),
           TYPE('class Calc:\n    def soma(self, a, b):\n        return a + b\n    def mult(self, a, b):\n        return a * b\n\nop = "mult"\nprint(getattr(Calc(), op)(3, 4))', "op escolhe o método mult, chamado com 3 e 4."),
           MC("Por que escrever getattr(p, campo) em vez de p.campo?", "Porque o nome do atributo está guardado na variável campo", ["Porque getattr é mais rápido", "Porque p.campo não é Python válido", "Porque getattr copia o objeto"], "p.campo procuraria um atributo chamado literalmente campo."),
           CODE("Crie a função total(obj, campos) que soma os atributos do obj cujos nomes estão na lista campos.",
                'def total(obj, campos):\n    return 0\n',
                'def total(obj, campos):\n    soma = 0\n    for c in campos:\n        soma += getattr(obj, c)\n    return soma',
                'class N:\n    a = 7\n    b = 8\n    c = 5\nassert total(N(), ["a", "b"]) == 15, "total com a e b deve ser 15"\nassert total(N(), ["a", "b", "c"]) == 20, "total com a, b e c deve ser 20"\nassert total(N(), []) == 0, "Lista vazia dá 0"',
                "Percorra campos e some getattr(obj, c).")]),
        # lição 4
        L("Pegadinhas do getattr",
          "O nome precisa ser texto: getattr(p, nome) sem aspas procura uma VARIÁVEL nome. getattr não lê chaves de dicionário, e não segue pontos: \"a.b\" é tratado como um nome só.",
          'dados = {"nome": "Ana"}\nprint(getattr(dados, "nome", "não achei"))\nprint(dados.get("nome"))',
          [OUT('d = {"x": 1}\nprint(getattr(d, "x", "?"))', ["1", "x", "Erro"], "Chaves de dicionário não são atributos. Veio o padrão."),
           OUT('class A:\n    x = 5\ntry:\n    print(getattr(A(), x))\nexcept NameError:\n    print("NameError")', ["5", "x", "TypeError"], "Sem aspas, x é uma variável que não existe."),
           OUT('try:\n    getattr("oi", 5)\nexcept TypeError:\n    print("nome precisa ser texto")', ["oi", "5", "None"], "O nome do atributo tem de ser str."),
           MC('getattr(obj, "dono.nome") faz o quê?', "Procura um atributo chamado literalmente dono.nome", ["Pega obj.dono.nome", "Dá SyntaxError", "Devolve os atributos de dono"], "Para seguir o caminho, use getattr duas vezes.")]),
        # lição 5
        L("getattr com outras funções",
          "getattr combina bem com sorted (ordenar pelo campo escolhido), callable (saber se é método) e hasattr. Assim o mesmo código serve para vários atributos.",
          'class Aluno:\n    def __init__(self, nome, nota):\n        self.nome = nome\n        self.nota = nota\n\nturma = [Aluno("Caio", 7), Aluno("Ana", 9), Aluno("Bia", 8)]\ncampo = "nota"\nfor a in sorted(turma, key=lambda a: getattr(a, campo)):\n    print(a.nome, a.nota)',
          [OUT('class A:\n    def __init__(self, n):\n        self.nome = n\nlista = [A("Teo"), A("Ana"), A("Bia")]\ncampo = "nome"\nprint([a.nome for a in sorted(lista, key=lambda a: getattr(a, campo))])', ["['Teo', 'Ana', 'Bia']", "['Teo', 'Bia', 'Ana']", "['nome', 'nome', 'nome']"], "Ordena pelo atributo nome, em ordem alfabética."),
           TYPE('print(callable(getattr("abc", "upper")))', "upper é um método, então dá para chamar."),
           ORDER("Monte o programa que escolhe o método andar pelo nome e mostra andando.",
                 ['class Robo:', '    def andar(self):', '        return "andando"', 'acao = getattr(Robo(), "andar")', 'print(acao())'],
                 "Primeiro a classe, depois pega o método e chama."),
           FILL("Complete para mostrar Pipo.", 'print(getattr("pipo", "title")___)', "()", ["(self)", ".run()", "[]"], "getattr devolve o método; os parênteses o chamam.")]),
        # lição 6
        L("Desafio: seguindo caminhos",
          "Para ler algo como pedido.cliente.nome a partir do texto \"cliente.nome\", divida nos pontos e aplique getattr uma vez para cada parte.",
          'class Cliente:\n    nome = "Bia"\n\nclass Pedido:\n    cliente = Cliente()\n\nobj = Pedido()\nfor parte in "cliente.nome".split("."):\n    obj = getattr(obj, parte)\nprint(obj)',
          [OUT('class B:\n    v = 3\nclass A:\n    b = B()\nprint(getattr(getattr(A(), "b"), "v"))', ["b", "None", "Erro"], "O primeiro getattr pega b; o segundo pega v."),
           TYPE('print("dono.nome".split("."))', "split corta o texto em cada ponto."),
           MC("Qual é o problema de getattr(obj, \"a.b\")?", "Procura um nome com ponto, que não existe", ["Nenhum, funciona", "Pega só a", "Apaga o atributo b"], "getattr não entende pontos."),
           CODE("Crie a função ler(obj, caminho) que segue um caminho com pontos, como \"dono.nome\", e devolve o valor final.",
                'def ler(obj, caminho):\n    return getattr(obj, caminho)\n',
                'def ler(obj, caminho):\n    for parte in caminho.split("."):\n        obj = getattr(obj, parte)\n    return obj',
                'class Dono:\n    nome = "Ana"\nclass Pet:\n    dono = Dono()\n    idade = 3\nassert ler(Pet(), "idade") == 3, "ler(pet, \\"idade\\") deve dar 3"\nassert ler(Pet(), "dono.nome") == "Ana", "ler(pet, \\"dono.nome\\") deve dar Ana"',
                "Use split(\".\") e um for que troca obj a cada passo.")]),
    ],

    # ================================================================ setattr
    "setattr": [
        # lição 2
        L("Criar ou trocar",
          "Se o atributo não existe, setattr cria. Se já existe, troca o valor. Ele mesmo não devolve nada: o resultado é sempre None.",
          'class Pet:\n    pass\n\np = Pet()\nsetattr(p, "fome", 5)\nprint(p.fome)\nsetattr(p, "fome", 2)\nprint(p.fome)\nprint(setattr(p, "sono", 1))',
          [OUT('class A: pass\na = A()\nsetattr(a, "x", 1)\nsetattr(a, "x", a.x + 10)\nprint(a.x)', ["1", "10", "Erro"], "O segundo setattr troca 1 por 1 + 10."),
           TYPE('class A: pass\nprint(setattr(A(), "y", 3))', "setattr não devolve nada."),
           MC("O que setattr devolve?", "None", ["O objeto alterado", "O valor novo", "True se deu certo"], "Ele só altera o objeto."),
           FILL('Complete para que c.cor valha "azul".', 'class Carro: pass\nc = Carro()\nsetattr(c, ___, "azul")\nprint(c.cor)', '"cor"', ["cor", "c.cor", '"azul"'], "O nome vai entre aspas, como texto.")]),
        # lição 3
        L("Usos do dia a dia",
          "setattr brilha quando os nomes vêm de fora: um formulário, um arquivo de configuração, uma contagem. Usado na classe, o valor muda para todos os objetos dela.",
          'class Perfil:\n    pass\n\nformulario = {"nome": "Bia", "cidade": "Recife", "idade": 22}\np = Perfil()\nfor campo, valor in formulario.items():\n    setattr(p, campo, valor)\nprint(p.nome, p.cidade, p.idade)',
          [OUT('class Placar: pass\np = Placar()\nfor time in ["azul", "verde", "azul"]:\n    setattr(p, time, getattr(p, time, 0) + 1)\nprint(p.azul, p.verde)', ["1 1", "3 0", "Erro"], "Cada vez que o time aparece, soma 1. Azul aparece duas vezes."),
           OUT('class Loja:\n    aberta = False\na = Loja()\nb = Loja()\nsetattr(Loja, "aberta", True)\nprint(a.aberta, b.aberta)', ["False False", "True False", "Erro"], "Mudou na classe, então vale para os dois objetos."),
           MC("Você recebe um dicionário de configurações. Como passar tudo para atributos de c?", "for k, v in config.items(): setattr(c, k, v)", ["setattr(c, config)", "c = setattr(config)", "for k in config: setattr(c, k)"], "Um setattr para cada par chave e valor."),
           CODE("Crie a função preencher(obj, dados) que copia cada par do dicionário dados para atributos do obj e devolve o obj.",
                'def preencher(obj, dados):\n    return obj\n',
                'def preencher(obj, dados):\n    for chave, valor in dados.items():\n        setattr(obj, chave, valor)\n    return obj',
                'class Ficha: pass\nf = preencher(Ficha(), {"nome": "Teo", "nivel": 3})\nassert f.nome == "Teo", "f.nome deve ser Teo"\nassert f.nivel == 3, "f.nivel deve ser 3"',
                "Percorra dados.items() e use setattr(obj, chave, valor).")]),
        # lição 4
        L("Pegadinhas do setattr",
          "Números, textos e object() não aceitam atributos novos: dá AttributeError. O nome tem de ser texto; sem aspas, vale o conteúdo da variável. Nomes com espaço até funcionam, mas só dá para ler com getattr.",
          'try:\n    setattr(10, "dobro", 20)\nexcept AttributeError:\n    print("int não aceita atributos novos")\n\nclass Caixa:\n    pass\n\nc = Caixa()\nsetattr(c, "meu item", 1)\nprint(getattr(c, "meu item"))',
          [OUT('try:\n    setattr("oi", "x", 1)\n    print("ok")\nexcept AttributeError:\n    print("AttributeError")', ["ok", "TypeError", "x"], "Textos não aceitam atributos novos."),
           OUT('class A: pass\na = A()\nnome = "cor"\nsetattr(a, nome, "rosa")\nprint(hasattr(a, "nome"), a.cor)', ["True rosa", "True cor", "Erro"], "Sem aspas, vale o conteúdo da variável: o atributo criado foi cor."),
           MC('Depois de setattr(c, "meu item", 1), como ler o valor?', 'getattr(c, "meu item")', ["c.meu item", "c.meu_item", 'c["meu item"]'], "Com espaço no nome, o ponto não funciona."),
           TYPE('class A: pass\ntry:\n    setattr(A(), 1, "x")\nexcept TypeError as e:\n    print(type(e).__name__)', "O nome precisa ser str, não número.")]),
        # lição 5
        L("setattr com outras funções",
          "Junto com getattr, setattr lê e grava atributos pelo nome, como num interruptor. Com zip você casa uma lista de nomes com uma de valores, e vars mostra o resultado.",
          'class Luz:\n    def __init__(self):\n        self.sala = False\n        self.quarto = True\n\ncasa = Luz()\nfor comodo in ["sala", "quarto"]:\n    setattr(casa, comodo, not getattr(casa, comodo))\nprint(casa.sala, casa.quarto)',
          [OUT('class P: pass\np = P()\nfor n, v in zip(["x", "y"], [3, 4]):\n    setattr(p, n, v)\nprint(p.x + p.y)', ["34", "xy", "Erro"], "x vale 3 e y vale 4; a soma dá 7."),
           TYPE('class P: pass\np = P()\nsetattr(p, "a", 1)\nsetattr(p, "b", 2)\nprint(vars(p))', "vars mostra os atributos criados, na ordem."),
           ORDER("Monte o programa que cria o atributo nivel com valor 1 e mostra 1.",
                 ['class Jogador:', '    pass', 'j = Jogador()', 'setattr(j, "nivel", 1)', 'print(j.nivel)'],
                 "Classe, objeto, setattr e só então a leitura."),
           FILL("Complete para inverter o interruptor.", 'class C:\n    ligado = True\nc = C()\nsetattr(c, "ligado", ___ c.ligado)\nprint(c.ligado)', "not", ["!", "-", "~"], "Em Python, a negação é not.")]),
        # lição 6
        L("Desafio: subindo de nível",
          "Um padrão comum: ler o valor atual com getattr (com padrão 0) e gravar o novo com setattr. Assim o atributo nasce na primeira vez e cresce nas próximas.",
          'class Heroi:\n    pass\n\nh = Heroi()\nfor _ in range(3):\n    setattr(h, "xp", getattr(h, "xp", 0) + 10)\nprint(h.xp)',
          [OUT('class H: pass\nh = H()\nsetattr(h, "ouro", getattr(h, "ouro", 5) * 2)\nprint(h.ouro)', ["5", "2", "Erro"], "ouro não existia, então partiu de 5 e dobrou."),
           TYPE('class H: pass\nh = H()\nfor c in "aba":\n    setattr(h, c, getattr(h, c, 0) + 1)\nprint(h.a, h.b)', "a aparece duas vezes e b uma."),
           MC('Por que usar getattr(h, "xp", 0) antes do setattr?', "Para não dar erro na primeira vez, quando xp ainda não existe", ["Para apagar o xp antigo", "Porque setattr só aceita zero", "Para copiar o objeto"], "O padrão 0 serve de ponto de partida."),
           CODE("Crie a função aumentar(obj, campo, valor) que soma valor ao atributo campo do obj. Se o atributo não existir, ele começa em 0.",
                'def aumentar(obj, campo, valor):\n    setattr(obj, campo, valor)\n',
                'def aumentar(obj, campo, valor):\n    setattr(obj, campo, getattr(obj, campo, 0) + valor)',
                'class Conta: pass\nc = Conta()\naumentar(c, "saldo", 10)\nassert c.saldo == 10, "Começando do zero, o saldo deve ser 10"\naumentar(c, "saldo", 5)\nassert c.saldo == 15, "Depois de somar 5, o saldo deve ser 15"',
                "setattr(obj, campo, getattr(obj, campo, 0) + valor)")]),
    ],

    # ================================================================ delattr
    "delattr": [
        # lição 2
        L("Apagar não é zerar",
          "Trocar o valor por None mantém o atributo existindo. delattr some com ele: depois, ler dá AttributeError, e getattr com padrão devolve o padrão.",
          'class Jogador:\n    pass\n\nj = Jogador()\nj.bonus = 50\nj.bonus = None\nprint(hasattr(j, "bonus"))\ndelattr(j, "bonus")\nprint(hasattr(j, "bonus"))\nprint(getattr(j, "bonus", "sem bônus"))',
          [OUT('class A: pass\na = A()\na.x = 1\na.x = None\nprint(hasattr(a, "x"))', ["False", "None", "Erro"], "Com None o atributo ainda existe."),
           TYPE('class A: pass\na = A()\na.v = 9\ndelattr(a, "v")\nprint(getattr(a, "v", "apagado"))', "Depois de apagar, o getattr usa o padrão."),
           MC("Depois de delattr(p, \"nome\"), o que acontece com print(p.nome)?", "AttributeError", ["Mostra None", "Mostra um texto vazio", "Mostra nome"], "O atributo deixou de existir."),
           FILL("Complete para apagar o atributo senha.", 'class U: pass\nu = U()\nu.senha = "123"\n___(u, "senha")\nprint(hasattr(u, "senha"))', "delattr", ["del", "setattr", "remove"], "delattr recebe o objeto e o nome em texto.")]),
        # lição 3
        L("Limpando dados",
          "Um uso prático é tirar dados que não devem sair, como senhas, antes de mostrar ou salvar o objeto. Com uma lista de nomes, um for apaga todos.",
          'class Usuario:\n    def __init__(self):\n        self.nome = "Teo"\n        self.senha = "1234"\n        self.token = "abc"\n\nu = Usuario()\nfor campo in ["senha", "token"]:\n    delattr(u, campo)\nprint(vars(u))',
          [OUT('class F:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\n        self.c = 3\nf = F()\nfor n in "ac":\n    delattr(f, n)\nprint(vars(f))', ["{'a': 1, 'c': 3}", "{}", "{'b': 2, 'c': 3}"], "Apagou a e c; sobrou só b."),
           TYPE('class F: pass\nf = F()\nf.tmp = 1\nf.fixo = 2\ndelattr(f, "tmp")\nprint(len(vars(f)))', "Sobrou um atributo."),
           MC("Por que apagar a senha de um objeto antes de mostrá-lo?", "Para que o dado sensível não apareça", ["Para o programa ficar mais rápido", "Porque print não mostra textos", "Porque senhas dão erro"], "Menos dados expostos, menos risco."),
           CODE("Crie a função limpar(obj, campos) que apaga cada atributo da lista campos que existir no obj. Os que não existirem devem ser ignorados, sem erro.",
                'def limpar(obj, campos):\n    for c in campos:\n        delattr(obj, c)\n',
                'def limpar(obj, campos):\n    for c in campos:\n        if hasattr(obj, c):\n            delattr(obj, c)',
                'class U: pass\nu = U()\nu.nome = "Ana"\nu.senha = "1"\nlimpar(u, ["senha", "token"])\nassert not hasattr(u, "senha"), "senha deve ser apagada"\nassert u.nome == "Ana", "nome deve continuar"',
                "Teste com hasattr antes de chamar delattr.")]),
        # lição 4
        L("Pegadinhas do delattr",
          "Atributos da classe não podem ser apagados pelo objeto: dá AttributeError. Se o objeto tinha um atributo com o mesmo nome da classe, apagar o dele faz o da classe aparecer de novo. Apagar duas vezes também dá erro.",
          'class Gato:\n    som = "miau"\n\ng = Gato()\ng.som = "MIAU!"\nprint(g.som)\ndelattr(g, "som")\nprint(g.som)',
          [OUT('class A:\n    x = 1\ntry:\n    delattr(A(), "x")\n    print("apagou")\nexcept AttributeError:\n    print("AttributeError")', ["apagou", "1", "KeyError"], "x pertence à classe, não ao objeto."),
           OUT('class A:\n    cor = "azul"\na = A()\na.cor = "verde"\ndelattr(a, "cor")\nprint(a.cor)', ["verde", "None", "Erro"], "Sem o atributo do objeto, volta a valer o da classe."),
           OUT('class A: pass\na = A()\na.x = 1\ndelattr(a, "x")\ntry:\n    delattr(a, "x")\nexcept AttributeError:\n    print("já foi")', ["1", "x", "None"], "Na segunda vez, x não existe mais."),
           MC("Qual destes dá erro?", 'delattr("texto", "upper")', ['delattr(obj, "x") logo depois de obj.x = 1', 'del obj.x logo depois de obj.x = 1', 'hasattr(obj, "x")'], "Não dá para apagar métodos de str.")]),
        # lição 5
        L("delattr com outras funções",
          "Para apagar sem susto, combine com hasattr ou try/except. Ele também funciona na própria classe, e aí o atributo some para todos os objetos.",
          'class Config:\n    modo = "teste"\n\nc = Config()\nprint(hasattr(c, "modo"))\ndelattr(Config, "modo")\nprint(hasattr(c, "modo"))',
          [FILL("Complete para só apagar se existir.", 'class A: pass\na = A()\nif ___(a, "x"):\n    delattr(a, "x")\nprint("ok")', "hasattr", ["getattr", "delattr", "vars"], "hasattr devolve True ou False."),
           ORDER("Monte o programa que tenta apagar e avisa se não havia nada.",
                 ['class Caixa: pass', 'c = Caixa()', 'try:', '    delattr(c, "item")', 'except AttributeError:', '    print("nada para apagar")'],
                 "O delattr fica dentro do try."),
           OUT('class A:\n    x = 1\n    y = 2\ndelattr(A, "y")\nprint(hasattr(A(), "x"), hasattr(A(), "y"))', ["True True", "False True", "Erro"], "y foi apagado da classe."),
           TYPE('class P: pass\np = P()\np.a, p.b, p.c = 1, 2, 3\ndelattr(p, "b")\nprint(list(vars(p)))', "Sobraram a e c.")]),
        # lição 6
        L("Desafio: só o essencial",
          "Para apagar enquanto percorre os atributos, percorra uma CÓPIA: list(vars(obj)). Mexer num dicionário enquanto o percorre dá RuntimeError.",
          'class Ficha:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\n\nf = Ficha()\nfor nome in list(vars(f)):\n    delattr(f, nome)\nprint(vars(f))',
          [OUT('class F:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\nf = F()\ntry:\n    for n in vars(f):\n        delattr(f, n)\nexcept RuntimeError:\n    print("RuntimeError")', ["{}", "a", "KeyError"], "O dicionário mudou de tamanho durante o for."),
           MC("Por que usar list(vars(obj)) no for?", "Para percorrer uma cópia dos nomes enquanto apaga", ["Para ordenar os nomes", "Porque vars não funciona em for", "Para apagar mais rápido"], "Assim o dicionário original pode mudar sem problema."),
           TYPE('class P: pass\np = P()\np.x = 1\np.y = 2\nfor n in list(vars(p)):\n    if n != "x":\n        delattr(p, n)\nprint(vars(p))', "Só x ficou."),
           CODE("Crie a função manter(obj, campos) que apaga todos os atributos do obj que NÃO estão na lista campos.",
                'def manter(obj, campos):\n    pass\n',
                'def manter(obj, campos):\n    for nome in list(vars(obj)):\n        if nome not in campos:\n            delattr(obj, nome)',
                'class P: pass\np = P()\np.nome = "Bia"\np.idade = 20\np.senha = "x"\nmanter(p, ["nome", "idade"])\nassert vars(p) == {"nome": "Bia", "idade": 20}, "Devem sobrar só nome e idade"',
                "Percorra list(vars(obj)) e apague quem não estiver em campos.")]),
    ],

    # ================================================================ vars
    "vars": [
        # lição 2
        L("Objeto, classe e sem nada",
          "vars(objeto) mostra só os atributos do próprio objeto, não os da classe. vars(Classe) mostra o que foi definido na classe. E vars() sem nada, dentro de uma função, mostra as variáveis locais.",
          'class Pet:\n    especie = "gato"\n    def __init__(self, nome):\n        self.nome = nome\n\np = Pet("Mimi")\nprint(vars(p))\nprint("especie" in vars(p))\nprint("especie" in vars(Pet))',
          [OUT('def f():\n    a = 1\n    b = 2\n    return vars()\nprint(f())', ["{}", "['a', 'b']", "{'a': 1}"], "Sem argumento, vars mostra as variáveis locais da função."),
           OUT('class A:\n    x = 1\n    def __init__(self):\n        self.y = 2\nprint(vars(A()))', ["{'x': 1, 'y': 2}", "{'x': 1}", "{}"], "x é da classe; o objeto só tem y."),
           TYPE('class A:\n    cor = "azul"\nprint("cor" in vars(A))', "cor foi definido na classe."),
           MC("vars(p) inclui os atributos definidos na classe de p?", "Não, só os do próprio objeto", ["Sim, todos", "Só os métodos", "Só se forem números"], "Para ver tudo, inclusive o herdado, use dir.")]),
        # lição 3
        L("Usos do dia a dia",
          "vars ajuda a espiar um objeto rapidinho, a transformá-lo em dicionário (por exemplo, para salvar em JSON) e a comparar dois objetos pelos valores.",
          'class Produto:\n    def __init__(self, nome, preco):\n        self.nome = nome\n        self.preco = preco\n\na = Produto("Bola", 30)\nb = Produto("Bola", 30)\nprint(a == b)\nprint(vars(a) == vars(b))',
          [OUT('import json\nclass P:\n    def __init__(self):\n        self.nome = "Ana"\n        self.vip = True\nprint(json.dumps(vars(P())))', ["{'nome': 'Ana', 'vip': True}", '{"nome": "Ana", "vip": True}', "Erro"], "json.dumps usa aspas duplas e true minúsculo."),
           TYPE('class P:\n    def __init__(self):\n        self.a = 1\n        self.b = 2\n        self.c = 3\nprint(len(vars(P())))', "Três atributos."),
           MC("Dois objetos com os mesmos valores: o que dá True?", "vars(a) == vars(b)", ["a == b", "a is b", "id(a) == id(b)"], "Sem __eq__, a == b compara identidade; os dicionários comparam valores."),
           CODE("Crie a função como_texto(obj) que devolve os atributos no formato nome=valor, separados por vírgula e espaço. Ex.: \"nome=Ana, idade=20\".",
                'def como_texto(obj):\n    return ""\n',
                'def como_texto(obj):\n    return ", ".join(f"{k}={v}" for k, v in vars(obj).items())',
                'class P:\n    def __init__(self):\n        self.nome = "Ana"\n        self.idade = 20\nassert como_texto(P()) == "nome=Ana, idade=20", "Esperado: nome=Ana, idade=20"',
                'Use ", ".join com um f"{k}={v}" para cada item de vars(obj).')]),
        # lição 4
        L("Pegadinhas do vars",
          "vars devolve o dicionário de verdade do objeto: mudar ele muda o objeto! Para uma cópia, use dict(vars(obj)). E números, textos e listas não têm __dict__: vars neles dá TypeError.",
          'class Caixa:\n    def __init__(self):\n        self.itens = 3\n\nc = Caixa()\nd = vars(c)\nd["itens"] = 10\nprint(c.itens)\ntry:\n    vars(42)\nexcept TypeError:\n    print("42 não tem __dict__")',
          [OUT('class A:\n    def __init__(self):\n        self.x = 1\na = A()\nvars(a)["x"] = 5\nprint(a.x)', ["1", "Erro", "None"], "O dicionário de vars é o próprio __dict__ do objeto."),
           OUT('class A:\n    def __init__(self):\n        self.x = 1\na = A()\ncopia = dict(vars(a))\ncopia["x"] = 5\nprint(a.x)', ["5", "Erro", "None"], "dict() fez uma cópia; o objeto não mudou."),
           TYPE('try:\n    vars([1, 2])\nexcept TypeError as e:\n    print(type(e).__name__)', "Listas não têm __dict__."),
           MC('vars(p).nome funciona?', 'Não: vars devolve um dicionário, use vars(p)["nome"]', ["Sim, igual a p.nome", "Só se nome for texto", "Sim, mas devolve None"], "Dicionário se lê com colchetes.")]),
        # lição 5
        L("vars com outras funções",
          "Como vars devolve um dicionário, valem todas as ferramentas de dicionário: .items() num for, sum dos .values(), max com key, e por aí vai.",
          'class Notas:\n    def __init__(self):\n        self.mat = 8\n        self.port = 9\n        self.hist = 7\n\nn = Notas()\nfor materia, nota in vars(n).items():\n    print(f"{materia}: {nota}")\nprint("média:", sum(vars(n).values()) / len(vars(n)))',
          [OUT('class N:\n    def __init__(self):\n        self.a = 7\n        self.b = 9\nprint(sum(vars(N()).values()))', ["79", "2", "Erro"], "Soma os valores 7 e 9."),
           TYPE('class N:\n    def __init__(self):\n        self.mat = 8\n        self.port = 10\n        self.hist = 6\nd = vars(N())\nprint(max(d, key=d.get))', "max com key=d.get acha a chave de maior valor."),
           ORDER("Monte o programa que mostra cada atributo na forma nome -> valor.",
                 ['class P:', '    def __init__(self):', '        self.cor = "azul"', 'for k, v in vars(P()).items():', '    print(k, "->", v)'],
                 "Primeiro a classe, depois o for com .items()."),
           FILL("Complete para pegar só os nomes, em ordem alfabética.", 'class P:\n    def __init__(self):\n        self.b = 1\n        self.a = 2\nprint(___(vars(P())))', "sorted", ["list", "reversed", "vars"], "sorted de um dicionário devolve as chaves ordenadas.")]),
        # lição 6
        L("Desafio: o que mudou?",
          "Comparando os dicionários de vars de dois objetos, dá para descobrir quais atributos mudaram, como num histórico de edições.",
          'class Perfil:\n    def __init__(self, nome, cidade):\n        self.nome = nome\n        self.cidade = cidade\n\nantes = Perfil("Ana", "Recife")\ndepois = Perfil("Ana", "Natal")\nfor k in vars(antes):\n    if vars(antes)[k] != vars(depois)[k]:\n        print("mudou:", k)',
          [OUT('class P:\n    def __init__(self, a, b):\n        self.a = a\n        self.b = b\nx, y = P(1, 2), P(1, 3)\nprint([k for k in vars(x) if vars(x)[k] != vars(y)[k]])', ["['a']", "['a', 'b']", "[]"], "Só b é diferente."),
           TYPE('class P:\n    def __init__(self, v):\n        self.v = v\nprint(vars(P(1)) == vars(P(1)))', "Os dicionários têm os mesmos pares."),
           MC("Para listar os nomes em ordem alfabética, o que usar?", "sorted(vars(obj))", ["vars(obj).sort()", "sorted(obj)", "vars(sorted(obj))"], "sorted de um dicionário ordena as chaves."),
           CODE("Crie a função diferencas(a, b) que devolve a lista, em ordem alfabética, dos nomes de atributos cujos valores são diferentes entre a e b (os dois têm os mesmos atributos).",
                'def diferencas(a, b):\n    return []\n',
                'def diferencas(a, b):\n    return sorted(k for k in vars(a) if vars(a)[k] != vars(b)[k])',
                'class P:\n    def __init__(self, nome, cidade, idade):\n        self.nome = nome\n        self.cidade = cidade\n        self.idade = idade\nassert diferencas(P("Ana", "Recife", 20), P("Ana", "Natal", 21)) == ["cidade", "idade"], "Esperado: [\\"cidade\\", \\"idade\\"]"\nassert diferencas(P("Bia", "Rio", 5), P("Bia", "Rio", 5)) == [], "Iguais: lista vazia"',
                "Compare vars(a)[k] com vars(b)[k] e ordene com sorted.")]),
    ],

    # ================================================================ dir
    "dir": [
        # lição 2
        L("dir sem nada e a ordem",
          "dir() sem argumento lista os nomes que existem onde você está; dentro de uma função, são as variáveis locais. O resultado é sempre uma lista em ordem alfabética.",
          'nota = 9\naluno = "Bia"\nnomes = dir()\nprint("nota" in nomes, "aluno" in nomes)\nprint(type(dir([])).__name__)',
          [OUT('def f():\n    y = 1\n    x = 2\n    return dir()\nprint(f())', ["['y', 'x']", "{'x': 2, 'y': 1}", "[]"], "Os nomes locais, em ordem alfabética."),
           TYPE('print(dir([]) == sorted(dir([])))', "dir já devolve tudo em ordem."),
           MC("O que dir() devolve?", "Uma lista de nomes (textos)", ["Um dicionário nome -> valor", "Um texto com tudo junto", "Os valores das variáveis"], "Só os nomes; para os valores, use vars."),
           FILL("Complete para checar se a variável pontos existe aqui.", 'pontos = 3\nprint("pontos" ___ dir())', "in", ["is", "==", "of"], "in procura o nome dentro da lista.")]),
        # lição 3
        L("Explorando um tipo",
          "dir é ótimo para descobrir o que um tipo sabe fazer. Filtre os nomes com startswith para achar, por exemplo, todos os métodos de str que começam com is.",
          'publicos = [n for n in dir("texto") if not n.startswith("_")]\nprint(len(publicos) > 40)\nprint([n for n in publicos if n.startswith("is")][:3])',
          [OUT('print([n for n in dir({}) if n.startswith("p")])', ["['pop']", "['popitem']", "[]"], "Dicionários têm pop e popitem."),
           TYPE('print([m for m in dir([]) if m.startswith("c")])', "Os métodos de lista que começam com c."),
           MC('Como achar os métodos de str que terminam com "case"?', '[n for n in dir(str) if n.endswith("case")]', ['dir(str, "case")', 'dir(str).endswith("case")', 'str.dir("case")'], "Filtre a lista com endswith."),
           CODE("Crie a função metodos_com(obj, inicio) que devolve a lista dos nomes de dir(obj) que começam com o texto inicio.",
                'def metodos_com(obj, inicio):\n    return dir(obj)\n',
                'def metodos_com(obj, inicio):\n    return [n for n in dir(obj) if n.startswith(inicio)]',
                'assert metodos_com([], "re") == ["remove", "reverse"], "Para listas e \\"re\\": remove e reverse"\nassert metodos_com({}, "item") == ["items"], "Para dicionários e \\"item\\": items"',
                "Uma compreensão de lista com startswith.")]),
        # lição 4
        L("dir x vars",
          "dir mostra tudo que dá para acessar, inclusive o que vem da classe e de object. vars mostra só o que está guardado no próprio objeto. E dir funciona com qualquer coisa, até com números.",
          'class Pet:\n    especie = "cão"\n    def latir(self):\n        return "au"\n\np = Pet()\np.nome = "Rex"\nprint(vars(p))\nprint("especie" in dir(p), "latir" in dir(p), "nome" in dir(p))',
          [OUT('class A:\n    x = 1\na = A()\nprint("x" in dir(a), "x" in vars(a))', ["True True", "False False", "False True"], "x é da classe: dir vê, vars do objeto não."),
           OUT('class A:\n    def __init__(self):\n        self.v = 1\nprint("v" in dir(A), "v" in dir(A()))', ["True True", "True False", "Erro"], "v só nasce quando o objeto é criado."),
           TYPE('print("__init__" in dir(object()))', "Até um object() puro tem __init__."),
           MC("Qual funciona com o número 5?", "dir(5)", ["vars(5)", "As duas dão erro", "Nenhuma das duas existe"], "Inteiros não têm __dict__, mas dir lista o que eles têm.")]),
        # lição 5
        L("dir com outras funções",
          "Juntando dir, getattr e callable, você separa os métodos (que dá para chamar) dos dados de um objeto.",
          'class Robo:\n    nome = "R2"\n    bateria = 80\n    def andar(self):\n        pass\n\nr = Robo()\npublicos = [n for n in dir(r) if not n.startswith("_")]\nprint([n for n in publicos if callable(getattr(r, n))])\nprint([n for n in publicos if not callable(getattr(r, n))])',
          [OUT('class C:\n    a = 1\n    def b(self): pass\nprint([n for n in dir(C) if not n.startswith("_") and callable(getattr(C, n))])', ["['a']", "['a', 'b']", "[]"], "Só b é método."),
           TYPE('class C:\n    z = 1\n    a = 2\nprint([n for n in dir(C) if not n.startswith("_")])', "dir ordena: a vem antes de z."),
           ORDER("Monte o programa que mostra quantos nomes públicos a classe Gato tem.",
                 ['class Gato:', '    nome = "Mimi"', 'publicos = [n for n in dir(Gato) if not n.startswith("_")]', 'print(len(publicos))'],
                 "Primeiro a classe, depois o filtro e por fim o len."),
           FILL("Complete: os dois testes dão sempre a mesma resposta.", 'print(("upper" in dir("a")) == ___("a", "upper"))', "hasattr", ["getattr", "callable", "vars"], "Ter o nome em dir equivale a hasattr dar True.")]),
        # lição 6
        L("Desafio: raio-x do objeto",
          "Agora junte tudo: dir para os nomes, um filtro para tirar os internos (_), callable para tirar os métodos e getattr para pegar os valores.",
          'class Livro:\n    autor = "Machado"\n    def __init__(self):\n        self.titulo = "Dom Casmurro"\n    def ler(self):\n        return "lendo"\n\nl = Livro()\nfor n in dir(l):\n    if not n.startswith("_") and not callable(getattr(l, n)):\n        print(n, "=", getattr(l, n))',
          [OUT('class A:\n    b = 2\n    def __init__(self):\n        self.a = 1\nx = A()\nprint([getattr(x, n) for n in dir(x) if not n.startswith("_")])', ["[2, 1]", "['a', 'b']", "[1]"], "Nomes em ordem: a (1) e depois b (2)."),
           MC("Por que filtrar com not n.startswith(\"_\")?", "Para tirar os nomes internos, como __init__", ["Para tirar os métodos", "Porque dir dá erro com _", "Para ordenar a lista"], "Nomes com _ são de uso interno."),
           TYPE('class A:\n    def f(self): pass\nprint(callable(getattr(A(), "f")))', "f é um método."),
           CODE("Crie a função resumo(obj) que devolve um dicionário {nome: valor} com todos os atributos públicos (sem _ no início) do obj que NÃO são métodos.",
                'def resumo(obj):\n    return vars(obj)\n',
                'def resumo(obj):\n    d = {}\n    for n in dir(obj):\n        if not n.startswith("_") and not callable(getattr(obj, n)):\n            d[n] = getattr(obj, n)\n    return d',
                'class Pet:\n    especie = "gato"\n    def __init__(self):\n        self.nome = "Mimi"\n    def miar(self):\n        return "miau"\nassert resumo(Pet()) == {"especie": "gato", "nome": "Mimi"}, "Esperado: especie e nome, sem o método miar"',
                "dir para os nomes; filtre _ e callable; getattr para os valores.")]),
    ],
}

BUGS = r'''
@fn_object 3
class Caixa:
    pass
c = object()
c.item = "bola"
print(c.item)
>>> c = Caixa()
!! object() puro não aceita atributos. Use a sua classe.

@fn_object 3
FALTA = object()
def dobro(x=FALTA):
    if x == None:
        return 0
    return x * 2
print(dobro())  # esperado: 0
>>> if x is FALTA:
!! O padrão é o marcador FALTA, não None. Compare com is FALTA.

@fn_object 4
class Ponto:
    def __init__(self, x):
        self.x = x
print(Ponto(1) == Ponto(1))  # esperado: True
>>> print(vars(Ponto(1)) == vars(Ponto(1)))  # esperado: True
!! O == herdado de object compara identidade. Compare os atributos.

@fn_object 1
class Animal(object()):
    pass
print(issubclass(Animal, object))
>>> class Animal(object):
!! A herança é da classe object, sem parênteses de chamada.

@fn_object 3
marcador = object()
itens = [1, marcador, 3]
print(itens.index(object()))  # esperado: 1
>>> print(itens.index(marcador))  # esperado: 1
!! Cada object() é novo e único. Use o mesmo marcador.

@fn_object 3
class Gato:
    def __str__(self):
        print("Gato Mimi")
print(Gato())
>>> return "Gato Mimi"
!! __str__ precisa devolver o texto com return, não imprimir.

@fn_object 3
class Ave:
    pass
print(issubclass(object, Ave))  # esperado: True
>>> print(issubclass(Ave, object))  # esperado: True
!! A ordem é issubclass(filha, mãe). Ave é que herda de object.

@fn_getattr 4
class Pet:
    nome = "Rex"
p = Pet()
print(getattr(p, nome))
>>> print(getattr(p, "nome"))
!! O nome do atributo vai entre aspas, como texto.

@fn_getattr 3
class Pet:
    nome = "Rex"
print(getattr(Pet(), "idade"))  # esperado: 0
>>> print(getattr(Pet(), "idade", 0))  # esperado: 0
!! idade não existe. Passe o padrão 0 como terceiro argumento.

@fn_getattr 5
class Loja:
    def abrir(self):
        return "aberta"
acao = "abrir"
msg = getattr(Loja(), acao)
print(msg.upper())
>>> msg = getattr(Loja(), acao)()
!! getattr devolve o método. Faltou chamar com ().

@fn_getattr 2
dados = {"cor": "azul"}
print(getattr(dados, "cor", "nenhuma"))  # esperado: azul
>>> print(dados.get("cor", "nenhuma"))  # esperado: azul
!! Chaves de dicionário não são atributos. Use .get().

@fn_getattr 4
class Aluno:
    nota = 8
campo = "nota"
print(getattr(Aluno(), "campo", 0))  # esperado: 8
>>> print(getattr(Aluno(), campo, 0))  # esperado: 8
!! Com aspas, procura um atributo chamado campo. Use a variável.

@fn_getattr 5
class Carro:
    def __init__(self):
        self.velocidade = 60
c = Carro()
print(getattr(c, "velocidade", default=0))
>>> print(getattr(c, "velocidade", 0))
!! getattr não aceita default=. O padrão vai como terceiro argumento.

@fn_setattr 3
class Pet: pass
p = Pet()
setattr(p, nome, "Rex")
print(p.nome)
>>> setattr(p, "nome", "Rex")
!! O nome do atributo vai entre aspas.

@fn_setattr 3
class Pet: pass
p = Pet()
p = setattr(p, "nome", "Rex")
print(p.nome)
>>> setattr(p, "nome", "Rex")
!! setattr devolve None. Não guarde o resultado em p.

@fn_setattr 4
class Conta: pass
c = Conta()
setattr(c, "saldo", 100)
setattr(c, "saldo", 50)
print(c.saldo)  # esperado: 150
>>> setattr(c, "saldo", c.saldo + 50)
!! setattr troca o valor. Para somar, use o valor atual + 50.

@fn_setattr 3
class Perfil: pass
p = Perfil()
setattr(p, "Bia", "nome")
print(p.nome)
>>> setattr(p, "nome", "Bia")
!! A ordem é objeto, nome do atributo e valor.

@fn_setattr 3
class Config: pass
c = Config()
for chave, valor in {"tema": "escuro", "som": True}:
    setattr(c, chave, valor)
print(c.tema)
>>> for chave, valor in {"tema": "escuro", "som": True}.items():
!! Para pegar chave e valor juntos, use .items().

@fn_setattr 4
class Placar: pass
p = Placar()
for time in ["azul", "azul", "verde"]:
    setattr(p, time, getattr(p, time) + 1)
print(p.azul)
>>> setattr(p, time, getattr(p, time, 0) + 1)
!! Na primeira vez o atributo não existe. Use o padrão 0.

@fn_delattr 4
class A: pass
a = A()
a.x = 1
delattr(a, x)
print(hasattr(a, "x"))
>>> delattr(a, "x")
!! O nome do atributo vai entre aspas.

@fn_delattr 4
class Usuario: pass
u = Usuario()
u.senha = "123"
u.senha = None
print(hasattr(u, "senha"))  # esperado: False
>>> delattr(u, "senha")
!! Trocar por None não apaga. Use delattr.

@fn_delattr 4
class Gato:
    som = "miau"
g = Gato()
delattr(g, "som")
print(hasattr(g, "som"))
>>> delattr(Gato, "som")
!! som pertence à classe. Apague na classe, não no objeto.

@fn_delattr 5
class Item: pass
i = Item()
i.temp = 1
delattr(i, "temp")
delattr(i, "temp")
print("limpo")
>>> if hasattr(i, "temp"): delattr(i, "temp")
!! O atributo já foi apagado. Confira com hasattr antes.

@fn_delattr 6
class Ficha:
    def __init__(self):
        self.a = 1
        self.b = 2
f = Ficha()
for nome in vars(f):
    delattr(f, nome)
print(vars(f))
>>> for nome in list(vars(f)):
!! Não apague enquanto percorre o dicionário. Percorra uma cópia.

@fn_delattr 4
class Caixa: pass
c = Caixa()
c.item = "bola"
delattr(c.item)
print(hasattr(c, "item"))
>>> delattr(c, "item")
!! delattr recebe o objeto e o nome do atributo em texto.

@fn_vars 5
class Aluno:
    def __init__(self, nome):
        self.nome = nome
a = Aluno("Caio")
print(vars(Aluno)["nome"])
>>> print(vars(a)["nome"])
!! nome é do objeto, criado no __init__. Use vars(a).

@fn_vars 5
class Pet:
    def __init__(self, nome):
        self.nome = nome
p = Pet("Rex")
print(vars(p).nome)
>>> print(vars(p)["nome"])
!! vars devolve um dicionário. Leia com colchetes.

@fn_vars 5
class P:
    def __init__(self):
        self.x = 1
p = P()
copia = vars(p)
copia["x"] = 99
print(p.x)  # esperado: 1
>>> copia = dict(vars(p))
!! vars devolve o dicionário do próprio objeto. Faça uma cópia com dict().

@fn_vars 5
class Pet:
    especie = "gato"
    def __init__(self, nome):
        self.nome = nome
print("especie" in vars(Pet("Mimi")))  # esperado: True
>>> print("especie" in dir(Pet("Mimi")))  # esperado: True
!! vars só tem os atributos do objeto. especie é da classe; dir vê os dois.

@fn_vars 6
class Nota:
    def __init__(self):
        self.a = 7
        self.b = 9
n = Nota()
print(sum(vars(n)))  # esperado: 16
>>> print(sum(vars(n).values()))  # esperado: 16
!! Percorrer o dicionário dá as chaves (textos). Some os .values().

@fn_vars 5
class Carro:
    def __init__(self):
        self.cor = "azul"
c = Carro()
for nome, valor in vars(c):
    print(nome, valor)
>>> for nome, valor in vars(c).items():
!! Para pegar nome e valor juntos, use .items().

@fn_dir 2
nomes = dir("oi")
print("upper" in nomes())
>>> print("upper" in nomes)
!! nomes já é a lista. Não tem parênteses.

@fn_dir 1
metodos = [m for m in dir([]) if m.startswith("_")]
print(metodos[0])  # esperado: append
>>> metodos = [m for m in dir([]) if not m.startswith("_")]
!! Faltou o not: a ideia era tirar os nomes com _.

@fn_dir 1
print("upper()" in dir("a"))  # esperado: True
>>> print("upper" in dir("a"))  # esperado: True
!! dir lista só os nomes, sem parênteses.

@fn_dir 1
print(dir("a")["upper"])
>>> print("upper" in dir("a"))
!! dir devolve uma lista, não um dicionário. Use in.

@fn_dir 5
class Robo:
    nome = "R2"
    def andar(self):
        pass
publicos = [n for n in dir(Robo) if not n.startswith("_")]
print(publicos)  # esperado: ['andar']
>>> publicos = [n for n in dir(Robo) if not n.startswith("_") and callable(getattr(Robo, n))]
!! Para ficar só com métodos, filtre com callable.

@fn_dir 4
class Pet:
    def __init__(self):
        self.nome = "Rex"
print("Nome" in dir(Pet()))  # esperado: True
>>> print("nome" in dir(Pet()))  # esperado: True
!! Maiúsculas importam: o atributo é nome.

@fn_dir 4
class Pet:
    def __init__(self):
        self.nome = "Rex"
print("nome" in dir(Pet))  # esperado: True
>>> print("nome" in dir(Pet()))  # esperado: True
!! nome só existe no objeto criado. Use dir(Pet()).
'''
