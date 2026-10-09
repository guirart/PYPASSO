from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    "base2": [
        # lição 1
        L("Listas",
          "Uma lista guarda vários valores em ordem, entre colchetes [ ]. O primeiro item é o [0] e o último é o [-1]. Métodos como .append mudam a própria lista e devolvem None.",
          'frutas = ["maçã", "banana", "uva"]\nprint(frutas[0])\nprint(frutas[-1])\nfrutas.append("manga")\nfrutas[1] = "kiwi"\nprint(frutas)\nprint(len(frutas))\nprint("uva" in frutas)\nprint([1, "dois", 3.5, True])',
          [OUT('notas = [7, 9, 5]\nprint(notas[1])', ["7", "5", "[9]"], "A contagem começa em 0, então [1] é o segundo item."),
           FILL("Complete para mostrar a última cor da lista.", 'cores = ["azul", "verde", "rosa"]\nprint(cores[___])', "-1", ["0", "3", "1"], "O índice -1 pega o último item, seja qual for o tamanho da lista."),
           OUT('nums = [1, 2]\nr = nums.append(3)\nprint(r)', ["[1, 2, 3]", "3", "[3]"], ".append muda a lista nums, mas devolve None. Por isso r é None."),
           CODE('A lista compras tem "arroz" e "feijão". Adicione "café" no final e troque "arroz" por "macarrão".',
                'compras = ["arroz", "feijão"]\n# adicione e troque aqui\n\nprint(compras)\n',
                'compras = ["arroz", "feijão"]\ncompras.append("café")\ncompras[0] = "macarrão"\nprint(compras)',
                'assert compras == ["macarrão", "feijão", "café"], "A lista deve ficar: [\'macarrão\', \'feijão\', \'café\']"',
                'compras.append("café") põe no final e compras[0] = "macarrão" troca o primeiro item.')]),
        # lição 2
        L("Tuplas e conjuntos",
          "Uma tupla, entre ( ), é como uma lista que não pode mudar. Dá para separar seus valores em variáveis: a, b = (1, 2). Um conjunto, entre { }, não guarda repetidos e ganha itens com .add. A função sorted(...) devolve uma lista em ordem.",
          'ponto = (3, 7)\nprint(ponto[0])\nx, y = ponto\nprint(x + y)\ndados = {6, 2, 6, 4, 2}\nprint(len(dados))\ndados.add(9)\nprint(sorted(dados))\ncores = {"azul", "verde", "azul"}\nprint(sorted(cores))',
          [OUT('a, b = (10, 20)\nprint(b, a)', ["10 20", "(20, 10)", "20, 10"], "a recebe 10 e b recebe 20. O print mostra b primeiro."),
           MC("O que acontece com t = (1, 2) e depois t[0] = 5?", "Dá erro: tuplas não podem mudar", ["t vira (5, 2)", "t vira (5, 1, 2)", "Nada acontece"], "Tuplas são fixas. Para mudar itens, use uma lista."),
           TYPE('n = {1, 2, 2, 3, 3, 3}\nprint(len(n))', "O conjunto guarda só 1, 2 e 3: os repetidos somem."),
           OUT('s = {5, 1}\ns.add(3)\ns.add(1)\nprint(sorted(s))', ["[5, 1, 3, 1]", "[1, 1, 3, 5]", "[5, 1, 3]"], "O 1 já estava lá, então não entra de novo. sorted devolve a lista em ordem.")]),
        # lição 3
        L("Dicionários",
          "Um dicionário liga chaves a valores: {\"chave\": valor}. Você lê com d[\"chave\"] e adiciona ou troca com d[\"chave\"] = valor. .get(chave, padrão) não dá erro se a chave faltar, e in confere as chaves.",
          'idades = {"Ana": 30, "Caio": 25}\nprint(idades["Ana"])\nidades["Bia"] = 19\nidades["Caio"] = 26\nprint(idades)\nprint(idades.get("Teo", 0))\nprint("Bia" in idades)\nprint(list(idades.items()))',
          [OUT('precos = {"pão": 1, "leite": 5}\nprint(precos["leite"])', ["1", "leite", "{'leite': 5}"], "precos[\"leite\"] devolve o valor ligado à chave \"leite\"."),
           FILL("Complete para mostrar 0 quando o item não existe no estoque.", 'estoque = {"lápis": 10}\nprint(estoque.get("borracha", ___))', "0", ["10", "None", '"borracha"'], "O segundo valor do .get é o que volta quando a chave não existe."),
           TYPE('d = {"a": 1}\nprint(1 in d)', "in procura nas CHAVES. A chave é \"a\"; o 1 é só o valor."),
           ORDER("Monte o programa que cria o pet, adiciona a idade e mostra a idade.", ['pet = {"nome": "Rex"}', 'pet["idade"] = 3', 'print(pet["idade"])'], "Primeiro crie, depois adicione a chave, e só então leia: ler antes dá KeyError.")]),
        # lição 4
        L("Decisões: if, elif, else",
          "if testa uma condição e termina com dois-pontos; o bloco de dentro tem 4 espaços de recuo. elif testa outra condição, e else pega o resto. 0, \"\", [] e None contam como falso.",
          'nota = 7\nif nota >= 9:\n    print("Excelente")\nelif nota >= 6:\n    print("Aprovado")\nelse:\n    print("Reprovado")\nlista = []\nif not lista:\n    print("Lista vazia")',
          [OUT('t = 30\nif t > 25:\n    print("calor")\nelse:\n    print("frio")', ["frio", "calor\nfrio", "True"], "30 > 25 é verdade, então só o bloco do if roda."),
           OUT('x = 0\nif x:\n    print("sim")\nelse:\n    print("não")', ["sim", "0", "False"], "O número 0 conta como falso, então vai para o else."),
           MC("O que falta em: if idade >= 18", "Dois-pontos (:) no final", ["Parênteses na condição", "A palavra then", "Ponto e vírgula"], "Toda linha de if, elif e else termina com dois-pontos."),
           TYPE('idade = 20\ningresso = True\nif idade >= 18:\n    if ingresso:\n        print("entra")\n    else:\n        print("compra")\nelse:\n    print("volta")', "Os dois testes são verdadeiros: o if de dentro mostra entra."),
           CODE('A variável pontos vale 75. Crie a variável medalha: "ouro" se pontos >= 90, "prata" se pontos >= 70, e "bronze" nos outros casos.',
                'pontos = 75\n# crie medalha com if, elif e else\n',
                'pontos = 75\nif pontos >= 90:\n    medalha = "ouro"\nelif pontos >= 70:\n    medalha = "prata"\nelse:\n    medalha = "bronze"',
                'assert medalha == "prata", "Com 75 pontos, medalha deve ser \\"prata\\""',
                'if pontos >= 90: ... elif pontos >= 70: ... else: ... — cada bloco cria medalha.')]),
        # lição 5
        L("Repetindo: while e for",
          "while repete enquanto a condição for verdadeira, então mude o contador para ele parar. for passa por cada item de uma lista, texto ou dicionário (as chaves). range(3) dá 0, 1, 2 e range(2, 5) dá 2, 3, 4. break sai do laço na hora.",
          'n = 1\nwhile n <= 3:\n    print("volta", n)\n    n = n + 1\nfor fruta in ["maçã", "uva"]:\n    print(fruta)\nfor i in range(2):\n    print(i)\nfor letra in "oba":\n    if letra == "b":\n        break\n    print(letra)',
          [TYPE('total = 0\nfor n in [2, 3, 5]:\n    total = total + n\nprint(total)', "O laço soma 2, depois 3, depois 5: total é 10."),
           OUT('for i in range(2, 5):\n    print(i)', ["2\n3\n4\n5", "0\n1\n2\n3\n4", "2 3 4"], "range(2, 5) começa no 2 e para ANTES do 5."),
           OUT('for letra in "python":\n    if letra == "h":\n        break\n    print(letra)', ["p\ny\nt\nh", "python", "h"], "Ao chegar no h, o break sai do laço antes de mostrar."),
           ORDER("Monte o programa que mostra 1, 2 e 3 com while e depois para.", ['n = 1', 'while n <= 3:', '    print(n)', '    n = n + 1'], "Sem o n = n + 1 dentro do laço, ele nunca terminaria.")]),
        # lição 6
        L("Juntando tudo",
          "Uma compreensão de lista cria uma lista nova numa linha só: [x * 2 for x in nums]. Com if no final, ela só guarda os itens que passam no teste.",
          'nums = [1, 2, 3, 4]\ndobros = [x * 2 for x in nums]\nprint(dobros)\npares = [x for x in nums if x % 2 == 0]\nprint(pares)',
          [OUT('print([x + 1 for x in [1, 2, 3]])', ["[1, 2, 3]", "[2, 3, 4, 5]", "6"], "Cada item ganha 1: 2, 3 e 4."),
           FILL("Complete para guardar só as notas maiores ou iguais a 6.", 'notas = [4, 8, 6, 9]\naprovados = [n for n in notas ___ n >= 6]\nprint(aprovados)', "if", ["for", "and", "elif"], "O if no final filtra: só entra quem passa no teste."),
           TYPE('palavras = ["sol", "lua"]\nprint([p.upper() for p in palavras])', "Cada palavra vira maiúscula, numa lista nova."),
           CODE("A lista notas tem as notas da turma. Usando for e if, conte quantas notas são maiores ou iguais a 7 e guarde em aprovados.",
                'notas = [8, 5, 7, 10, 6, 9]\naprovados = 0\n# use for e if para contar\n\nprint(aprovados)\n',
                'notas = [8, 5, 7, 10, 6, 9]\naprovados = 0\nfor n in notas:\n    if n >= 7:\n        aprovados = aprovados + 1\nprint(aprovados)',
                'assert aprovados == 4, "São 4 notas maiores ou iguais a 7"\nassert __stdout__.strip() == "4", "O programa deve mostrar 4"',
                'for n in notas: if n >= 7: aprovados = aprovados + 1')]),
    ],
}

BUGS = r'''
@base2 2
nomes = ["Ana", "Caio", "Bia"]
print(nomes[3])
>>> print(nomes[2])
!! A contagem começa em 0: o último dos 3 nomes é o [2].

@base2 2
idade = 20
if idade >= 18
    print("maior de idade")
>>> if idade >= 18:
!! Faltou o dois-pontos no final do if.

@base2 2
for n in [1, 2, 3]:
print(n)
>>>     print(n)
!! O que fica dentro do for precisa de 4 espaços de recuo.

@base2 2
precos = {"pão": 1, "café": 5}
print(precos["leite"])
>>> print(precos.get("leite", 0))
!! A chave "leite" não existe. Use .get com um valor padrão.

@base2 4
n = 1
while n <= 3:
    print(n)
    n + 1
>>> n = n + 1
!! n + 1 só calcula; precisa guardar em n, senão o laço nunca para.

@base2 2
lista = [3, 1]
lista = lista.append(2)
print(len(lista))
>>> lista.append(2)
!! .append muda a lista e devolve None. Não guarde o resultado.

'''
