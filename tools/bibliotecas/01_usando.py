from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_intro", titulo="Usando bibliotecas",
               descricao="O que são módulos e bibliotecas, como importar e como explorar o que vem dentro.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("O que é uma biblioteca",
      "Um módulo é um arquivo de Python cheio de funções prontas, e uma biblioteca é um conjunto de módulos (quando vem em pastas, também se chama pacote). Em vez de escrever tudo do zero, você pede emprestado com import e usa com nome_do_modulo.funcao. Exemplo: o módulo math já sabe tirar raiz quadrada.",
      'import math\n\nprint(math.sqrt(81))\nprint(math.pi)',
      [OUT('import math\nprint(math.sqrt(25))', ["25", "5", "Erro"], "sqrt devolve a raiz quadrada sempre como número decimal: 5.0."),
       MC("Para que serve o import?", "Trazer um módulo pronto para usar no seu programa", ["Baixar arquivos da internet", "Criar uma variável nova", "Mostrar algo na tela"], "O import carrega um módulo; depois você usa o que tem dentro dele com o ponto."),
       FILL("Complete para usar a função sqrt do módulo math.", 'import math\nprint(math___sqrt(49))', ".", [",", ":", "_"], "O ponto liga o módulo à função: math.sqrt."),
       MC("O que acontece se você escrever print(sqrt(16)) sem nenhum import?", "Dá NameError: o Python não conhece sqrt", ["Mostra 4.0", "Mostra 4", "O Python importa o math sozinho"], "sqrt mora dentro do math. Sem import, o nome não existe.")]),
    # lição 2
    L("Padrão x externas (pip)",
      "A biblioteca padrão já vem com o Python: math, random, json, datetime... é só importar. As bibliotecas externas (como pandas e requests) ficam no PyPI, uma loja gratuita de pacotes, e são instaladas uma vez no terminal com pip install nome. Depois de instaladas, o import é igualzinho.",
      '# No TERMINAL (não no código), uma vez só:\n#   pip install requests\n\n# Módulos da biblioteca padrão já estão aí:\nimport statistics\nnotas = [7, 8, 9]\nprint(statistics.mean(notas))',
      [MC("Qual destas já vem com o Python, sem instalar nada?", "math", ["pandas", "requests", "numpy"], "math faz parte da biblioteca padrão. As outras vêm do PyPI."),
       MC("Onde você digita pip install pandas?", "No terminal (prompt de comando)", ["Dentro do arquivo .py, antes do import", "Dentro do print", "No navegador, no site do Python"], "pip é um programa do terminal. No código você só escreve import pandas."),
       MC("Você rodou import requests e apareceu ModuleNotFoundError. O que provavelmente aconteceu?", "A biblioteca externa ainda não foi instalada com pip", ["Faltaram os parênteses: import requests()", "O nome tem que ser em maiúsculas", "requests só funciona dentro de uma função"], "ModuleNotFoundError quer dizer que o Python não achou o módulo. Para externas, falta o pip install."),
       OUT('import statistics\nprint(statistics.median([3, 1, 9]))', ["1", "4.333333333333333", "9"], "median ordena os valores (1, 3, 9) e pega o do meio: 3.")]),
    # lição 3
    L("Jeitos de importar",
      "import math traz o módulo inteiro (use math.pi). from math import pi traz só pi, e você usa sem o prefixo. import math as m dá um apelido curto. from math import * despeja tudo de uma vez e não é recomendado: você não sabe de onde veio cada nome e pode apagar variáveis suas sem querer.",
      'import math\nfrom math import sqrt\nimport statistics as st\n\nprint(math.floor(2.7))\nprint(sqrt(9))\nprint(st.mean([2, 4]))',
      [OUT('from math import pi\nprint(round(pi, 2))', ["3.1", "3.141", "math.pi"], "from math import pi traz pi direto; round(pi, 2) dá 3.14."),
       FILL("Complete para dar o apelido st ao módulo statistics.", 'import statistics ___ st\nprint(st.mean([1, 2, 3]))', "as", ["to", "=", "like"], "import ... as ... cria um apelido."),
       MC("Por que evitar from math import *?", "Ele traz muitos nomes de uma vez e pode sobrescrever variáveis suas sem avisar", ["Ele deixa o programa sem acesso ao math", "Ele só funciona na biblioteca padrão", "Ele importa o módulo duas vezes"], "Com * você não sabe de onde veio cada nome. Prefira importar o que vai usar."),
       CODE("Importe só a função sqrt do math (com from) e mostre a raiz de 144.",
            "import math\n# troque o import acima e mostre sqrt(144) sem escrever math.\n",
            'from math import sqrt\nprint(sqrt(144))',
            'assert "sqrt" in globals(), "Use from math import sqrt"\nassert __stdout__.strip() == "12.0", "A saída deve ser 12.0"',
            'from math import sqrt\nprint(sqrt(144))')]),
    # lição 4
    L("Explorando um módulo",
      "Não sabe o que tem num módulo? dir(modulo) devolve a lista de nomes que ele guarda. help(modulo.funcao) mostra o manual, e modulo.funcao.__doc__ guarda esse texto. Cada módulo também sabe o próprio nome em __name__.",
      'import math\n\nnomes = dir(math)\nprint("sqrt" in nomes)\nprint("raiz" in nomes)\nprint(math.__name__)\nprint(math.sqrt.__doc__)',
      [OUT('import math\nprint("pi" in dir(math))', ["False", "pi", "3.141592653589793"], "dir(math) é uma lista de nomes, e \"pi\" está nela: True."),
       TYPE('import statistics as st\nprint(st.__name__)', "O apelido não muda o nome verdadeiro do módulo."),
       MC("Qual comando mostra o manual de uma função, explicando como usar?", "help(math.ceil)", ["dir(math.ceil)", "print(math.ceil)", "math.ceil.__name__"], "help mostra a documentação. dir lista nomes, e __name__ é só o nome."),
       CODE("Crie a variável tem_media com True ou False, dizendo se \"mean\" existe no módulo statistics. Use dir, não escreva True na mão.",
            "import statistics\ntem_media = None\nprint(tem_media)\n",
            'import statistics\ntem_media = "mean" in dir(statistics)\nprint(tem_media)',
            'assert tem_media is True, "tem_media deve ser True: mean existe no statistics"\nassert __stdout__.strip() == "True", "Mostre tem_media com print"',
            'tem_media = "mean" in dir(statistics)')]),
    # lição 5
    L("Seu próprio módulo",
      "Todo arquivo .py é um módulo! Se você salva funções em loja.py, outro arquivo na mesma pasta pode fazer import loja e usar loja.desconto(). Dentro do arquivo que está rodando, __name__ vale \"__main__\"; quando ele é importado, vale o nome do arquivo. Aqui simulamos um módulo com types.ModuleType.",
      'import types\n\n# imagine que isto é o arquivo loja.py\nloja = types.ModuleType("loja")\ndef desconto(preco):\n    return preco * 90 // 100\nloja.desconto = desconto\n\nprint(loja.__name__)\nprint(loja.desconto(200))\nprint(__name__)',
      [MC("Você criou o arquivo pets.py com a função latir(). Como usar em outro arquivo da mesma pasta?", "import pets e depois pets.latir()", ["import pets.py e depois latir()", "from pets.py import latir", "include pets"], "No import vai o nome do arquivo sem o .py."),
       TYPE('print(__name__)', "O arquivo que está rodando direto se chama \"__main__\"."),
       ORDER("Monte o módulo notas.py: a função media e um teste que só roda quando o arquivo é executado direto.", ["def media(lista):", "    return sum(lista) / len(lista)", 'if __name__ == "__main__":', "    print(media([6, 8, 10]))"], "Primeiro a função. O teste fica no if __name__, então não roda quando outro arquivo faz import notas."),
       MC("Para que serve if __name__ == \"__main__\": no fim de um módulo?", "Rodar aquele trecho só quando o arquivo é executado direto, não quando é importado", ["Deixar o módulo mais rápido", "Impedir que outros arquivos importem o módulo", "Criar a função main automaticamente"], "Quando o arquivo é importado, __name__ é o nome dele, então o bloco não roda.")]),
    # lição 6
    L("Desafio: kit de ferramentas",
      "Juntando tudo: importe só o que precisa, use apelidos curtos e consulte dir quando esquecer um nome. Bibliotecas prontas economizam muito trabalho, como calcular o boletim de uma turma.",
      'from statistics import mean\nimport math as m\n\nnotas = [6.5, 8.0, 9.5]\nmedia = mean(notas)\nprint(media)\nprint(m.ceil(media))',
      [OUT('import math as m\nprint(m.floor(7.9))', ["8", "7.9", "Erro: math não existe"], "Com o apelido, m.floor é o mesmo que math.floor: arredonda para baixo, 7."),
       OUT('from math import *\npi = 3\nprint(pi)', ["3.141592653589793", "Erro", "3.14"], "Sua variável pi sobrescreveu o pi do math. É o perigo do import *."),
       FILL("Complete para importar a função mean.", '___ statistics import mean\nprint(mean([4, 6]))', "from", ["import", "with", "use"], "from módulo import nome."),
       CODE("Crie a função media_arredondada(notas) que devolve a média das notas arredondada para CIMA. Use mean do statistics e ceil do math.",
            "def media_arredondada(notas):\n    return 0\n\nprint(media_arredondada([7, 8, 8]))\n",
            'from statistics import mean\nfrom math import ceil\n\ndef media_arredondada(notas):\n    return ceil(mean(notas))\n\nprint(media_arredondada([7, 8, 8]))',
            'assert media_arredondada([7, 8, 8]) == 8, "A média de 7, 8, 8 é 7.66..., para cima dá 8"\nassert media_arredondada([5, 6]) == 6, "A média de 5 e 6 é 5.5, para cima dá 6"\nassert media_arredondada([10, 10]) == 10, "A média de 10 e 10 é 10"',
            'from statistics import mean\nfrom math import ceil\n\ndef media_arredondada(notas):\n    return ceil(mean(notas))')]),
]

BUGS = r'''
@lib_intro 2
import math
print(math.squareroot(36))
>>> print(math.sqrt(36))
!! A função de raiz quadrada se chama sqrt.

@lib_intro 2
import math
print(Math.pi)
>>> print(math.pi)
!! O módulo foi importado como math, com m minúsculo.

@lib_intro 1
from math import floor
print(math.floor(4.8))
>>> import math
!! Com from math import floor, só floor existe. Para usar math.floor, importe o módulo.

@lib_intro 2
import statistics as st
print(statistics.mean([2, 4, 6]))
>>> print(st.mean([2, 4, 6]))
!! Com o apelido st, use st.mean.

@lib_intro 1
import math.sqrt
print(sqrt(49))
>>> from math import sqrt
!! sqrt é uma função, não um módulo. Para trazer só ela, use from math import sqrt.

@lib_intro 2
from math import *
e = 5
print(round(e, 2))  # esperado: 2.72
>>> nota = 5
!! A variável e apagou a constante e do math. É o perigo do import *: use outro nome.
'''
