from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    "base1": [
        # lição 1
        L("Funções e valores",
          'Um valor é um dado, como o número 7 ou o texto "oi". Uma função é um comando pronto: você chama a função com parênteses e coloca os valores (argumentos) dentro, como print("Olá"). Algumas funções devolvem um resultado: len("abc") devolve 3, e você pode guardar esse resultado. Tudo depois de # é um comentário: o Python ignora.',
          '# print mostra valores na tela\nprint("Olá")\nprint(7, "gatos")\n\n# len devolve o tamanho do texto\nprint(len("abc"))',
          [OUT('print("Oi", "Ana")', ["OiAna", "Oi, Ana", '"Oi" "Ana"'], "Com vários argumentos, print coloca um espaço entre eles."),
           TYPE('print(len("pipoca"))', 'len devolve quantas letras tem "pipoca": 6. O print mostra esse resultado.'),
           MC("O que o Python faz com uma linha que começa com #?", "Ignora: é um comentário", ["Mostra a linha na tela", "Dá erro", "Repete a linha"], "Comentários são anotações para pessoas. O Python pula essa parte."),
           FILL('Complete para chamar a função print com o valor "Oi".', 'print___"Oi")', "(", ["[", "{", " "], "Funções são chamadas com parênteses: print(\"Oi\").")]),
        # lição 2
        L("Variáveis",
          'Uma variável é um nome que guarda um valor: nome = valor. Depois, é só usar o nome no lugar do valor. Você pode trocar o valor quando quiser. O nome não pode ter espaços nem começar com número: use _ para separar palavras, como nota_final.',
          'pet = "Rex"\nidade = 3\nprint(pet, idade)\nidade = 4  # mudou!\nprint(pet, idade)',
          [OUT('x = 5\nx = 8\nprint(x)', ["5", "5 8", "x"], "A variável guarda só o último valor: 8."),
           MC("Qual destes é um nome de variável válido?", "nota_final", ["nota final", "2nota", "nota-final"], "Sem espaços, sem começar com número. O - seria lido como conta de menos."),
           ORDER("Monte o programa: guarda 10 pontos, ganha mais 5 e mostra o total (15).", ["pontos = 10", "pontos = pontos + 5", "print(pontos)"], "Primeiro cria a variável, depois muda o valor, e só então mostra."),
           CODE('Crie a variável pet com o texto "Rex" e mostre ela com print.',
                "# crie a variável pet aqui\n",
                'pet = "Rex"\nprint(pet)',
                'assert pet == "Rex", "A variável pet deve guardar \\"Rex\\""\nassert __stdout__.strip() == "Rex", "O programa deve mostrar: Rex"',
                'pet = "Rex" e depois print(pet), sem aspas no nome da variável.')]),
        # lição 3
        L("Strings (textos)",
          'Texto entre aspas é uma string, e o tipo dela se chama str. Pode usar aspas duplas ou simples, tanto faz. Com + você junta textos e com * repete. Atenção: "10" com aspas é texto, não número! Uma f-string (f antes das aspas) coloca variáveis dentro do texto com {}.',
          'a = "Bom"\nb = \'dia\'\nprint(a + " " + b)\nprint("ha" * 3)\nprint("10" + "5")\nnome = "Bia"\nprint(f"Oi, {nome}!")',
          [OUT('print("ab" + "cd")', ["ab cd", "ab+cd", "Erro"], "O + cola os textos sem colocar espaço."),
           TYPE('print("la" * 3)', "O * repete o texto 3 vezes."),
           OUT('print("10" + "5")', ["15", "10 5", "Erro"], 'Com aspas são textos, então o + junta: "105".'),
           FILL("Complete para mostrar: Oi, Bia!", 'nome = "Bia"\nprint(___"Oi, {nome}!")', "f", ["s", "+", "str"], "O f antes das aspas faz o {nome} virar o valor da variável.")]),
        # lição 4
        L("Mexendo em strings",
          'Cada letra tem uma posição, começando do 0: texto[0] é a primeira e texto[-1] a última. texto[1:3] pega um pedaço (da posição 1 até antes da 3). "a" in texto responde True (sim) ou False (não). Um método é uma função que vem junto com o valor e é chamada com ponto: texto.upper(). Métodos de string devolvem uma string NOVA; a original não muda.',
          'texto = "  Python  "\nlimpo = texto.strip()\nprint(limpo)\nprint(limpo[0], limpo[-1], limpo[1:3])\nprint("th" in limpo)\nprint(limpo.upper(), limpo.lower())\nprint(limpo.replace("P", "J"))',
          [OUT('palavra = "Python"\nprint(palavra[0], palavra[-1])', ["P o", "y n", "Erro"], "[0] é a primeira letra e [-1] é a última."),
           TYPE('print("banana"[1:3])', "Posições 1 e 2 (a 3 fica de fora): a e n."),
           OUT('nome = "ana"\nnome.upper()\nprint(nome)', ["ANA", "Ana", "Erro"], "upper() devolve um texto novo, mas ninguém guardou. Para mudar: nome = nome.upper()."),
           FILL('Complete para trocar "gato" por "cão".', 'frase = "meu gato"\nprint(frase.___("gato", "cão"))', "replace", ["upper", "strip", "in"], "replace(velho, novo) devolve o texto com a troca."),
           MC('O que sai de print("ana" in "banana")?', "True", ["False", "ana", "Erro"], '"ana" aparece dentro de "banana" (b-ANA-na).')]),
        # lição 5
        L("Números",
          "int é número inteiro (5) e float é número com ponto (2.5). As contas: + - * /, // (divisão inteira), % (resto) e ** (potência). A divisão / sempre dá float, mesmo que seja exata. Cuidado: 5 + 5 é 10, mas \"5\" + \"5\" é \"55\".",
          'print(7 + 2, 7 - 2, 7 * 2)\nprint(7 / 2, 7 // 2, 7 % 2)\nprint(2 ** 3)\nprint(10 / 2)\nprint(5 + 5, "5" + "5")',
          [OUT('print(7 / 2)', ["3", "3.0", "4"], "A divisão / dá o resultado com ponto: 3.5."),
           TYPE('print(7 // 2, 7 % 2)', "7 dividido por 2 dá 3 inteiro e sobra 1."),
           OUT('print("5" + "5", 5 + 5)', ["10 10", "55 55", "Erro"], 'Com aspas é texto (junta: 55); sem aspas é número (soma: 10).'),
           MC("Qual é o resultado de 10 / 2?", "5.0", ["5", "2", "Erro"], "A divisão / sempre devolve float, então 5.0."),
           FILL("Complete para calcular 2 elevado a 3 (dá 8).", "print(2 ___ 3)", "**", ["*", "^", "//"], "** é potência. No Python, ^ não é potência.")]),
        # lição 6
        L("True, False e None",
          "Comparações respondem True (verdadeiro) ou False (falso); esse tipo se chama bool. Compare com == (igual), != (diferente), <, >, <= e >=. Atenção: = guarda, == compara! and exige as duas coisas, or aceita uma delas e not inverte. None quer dizer \"nada\": é o que print() devolve.",
          'idade = 15\nprint(idade >= 18)\nprint(idade == 15, idade != 15)\nprint(idade > 10 and idade < 20)\nprint(not True)\nresultado = print("oi")\nprint(resultado)',
          [OUT('print(3 > 2, 3 == 2)', ["False True", "True True", "3 > 2 3 == 2"], "3 é maior que 2 (True), mas não é igual a 2 (False)."),
           OUT('x = print("oi")\nprint(x)', ["oi", "None", "oi\noi"], 'O primeiro print mostra oi e devolve None, que vai para x.'),
           FILL("Complete para perguntar se 5 é igual a 5.", "print(5 ___ 5)", "==", ["=", "is"], "== compara. Um = só serve para guardar valor em variável."),
           MC("Qual é o resultado de True and False?", "False", ["True", "None"], "and só dá True quando os dois lados são True."),
           CODE('Calcule total = preco * quantidade, crie caro = total > 50 e mostre exatamente: Total: 60 | Caro: True',
                'preco = 20\nquantidade = 3\n# crie total e caro e mostre o resultado\n',
                'preco = 20\nquantidade = 3\ntotal = preco * quantidade\ncaro = total > 50\nprint(f"Total: {total} | Caro: {caro}")',
                'assert total == 60, "total deve ser preco * quantidade (60)"\nassert caro is True, "caro deve ser o resultado de total > 50"\nassert __stdout__.strip() == "Total: 60 | Caro: True", "A saída deve ser exatamente: Total: 60 | Caro: True"',
                'total = preco * quantidade; caro = total > 50; print(f"Total: {total} | Caro: {caro}")')]),
    ],
}

BUGS = r'''
@base1 1
print(Olá mundo)
>>> print("Olá mundo")
!! Texto precisa ficar entre aspas.

@base1 2
nome = "Ana"
Print(nome)
>>> print(nome)
!! O Python diferencia maiúsculas: a função é print, com p minúsculo.

@base1 2
idade = 30
print("Idade: " + idade)
>>> print(f"Idade: {idade}")
!! Texto + número dá erro. Use uma f-string.

@base1 2
nota = 10
print(nota = 10)  # esperado: True
>>> print(nota == 10)  # esperado: True
!! Um = guarda valor; para comparar use ==.

@base1 2
nome = "ana"
nome.upper()
print(nome)  # esperado: ANA
>>> nome = nome.upper()
!! upper() devolve um texto novo. Guarde o resultado na variável.

@base1 2
palavra = "Python"
print(palavra[1])  # esperado: P
>>> print(palavra[0])  # esperado: P
!! As posições começam do 0. A primeira letra é [0].
'''
