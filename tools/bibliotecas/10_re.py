from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_re", titulo="re (expressões regulares)",
               descricao="Encontre, extraia e limpe textos com padrões: números, e-mails, CPF, preços...",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Procurando: search e match",
      'A biblioteca re procura padrões dentro de textos: um número de pedido, um e-mail, uma palavra. Use import re. re.search(padrao, texto) procura em qualquer lugar e devolve um "achado" (Match) ou None; .group() mostra o trecho achado. re.match só olha o COMEÇO do texto. Escreva os padrões com r"..." (raw string), para a barra invertida \\ não virar código especial.',
      r'''import re
msg = "Seu pedido 4521 saiu para entrega"
achado = re.search("pedido", msg)
print(achado.group())
print(re.match("pedido", msg))
print(re.match("Seu", msg).group())''',
      [OUT('import re\nm = re.search("pix", "Pague com pix ou cartão")\nprint(m.group())',
           ["Pague com pix", "True", "None"], ".group() devolve só o trecho que combinou com o padrão."),
       OUT('import re\nprint(re.match("ana", "banana"))',
           ["ana", "banana", "Erro"], 'match só olha o começo. "banana" começa com "b", então não acha nada: None.'),
       MC('Por que escrevemos os padrões como r"\\d+" (com r antes)?',
          "Para a barra invertida \\ ser lida como está, sem virar escape",
          ["Para o padrão rodar mais rápido", "Porque o r significa regex e é obrigatório", "Para ignorar maiúsculas e minúsculas"],
          'Com r"..." o Python não mexe nas barras, e o re recebe o padrão exatamente como você escreveu.'),
       FILL("Complete para avisar quando a mensagem tiver a palavra urgente em qualquer lugar.",
            'import re\nmsg = "Responder hoje: urgente!"\nif re.___("urgente", msg):\n    print("Prioridade!")',
            "search", ["match", "find", "contains"],
            "search procura em qualquer lugar. match só olharia o começo, e a mensagem começa com Responder."),
       ]),
    # lição 2
    L("Classes e quantificadores",
      r'Padrões têm "coringas": \d é um dígito, \w é letra, número ou _, \s é espaço e . é qualquer caractere. Depois deles vêm os quantificadores: + (um ou mais), * (zero ou mais), ? (opcional) e {n} (exatamente n vezes). Assim você descreve formatos como CEP, placa ou telefone.',
      r'''import re
print(re.search(r"\d+", "Sala 2045, bloco B").group())
print(re.search(r"\d{5}-\d{3}", "CEP 01310-100").group())
print(re.search(r"https?", "site: http://loja.com").group())
print(re.search(r"\w+", "   olá mundo").group())''',
      [OUT(r'''import re
print(re.search(r"\d+", "Tenho 3 gatos e 12 peixes").group())''',
           ["12", "3 12", "312"], "search para no PRIMEIRO trecho que combina: o 3."),
       TYPE(r'''import re
print(re.search(r"\d{2}:\d{2}", "Sala 5, aula às 14:30").group())''',
            r"\d{2}:\d{2} pede dois dígitos, dois-pontos e mais dois dígitos. O 5 sozinho não serve."),
       MC("Qual padrão encontra tanto http quanto https?",
          r'r"https?"', [r'r"https+"', r'r"http\d"', r'r"(http)s"'],
          "O ? deixa o s opcional: pode aparecer uma vez ou nenhuma."),
       FILL("Complete para pegar a idade inteira (todos os dígitos seguidos).",
            r'''import re
print(re.search(r"\d___", "Tenho 35 anos").group())''',
            "+", ["?", "{1}", "s"],
            r"\d+ pega um ou mais dígitos: 35. Com ? ou {1}, viria só o 3."),
       ]),
    # lição 3
    L("Achando todos: findall",
      "re.findall(padrao, texto) devolve uma LISTA com todos os trechos que combinam, na ordem em que aparecem. Se não achar nada, devolve lista vazia. Ótimo para pegar todas as hashtags de um post ou todos os números de uma nota fiscal.",
      r'''import re
post = "Dia de praia #verão #férias #sol"
print(re.findall(r"#\w+", post))
nota = "Café 5, pão 3, bolo 12"
print(re.findall(r"\d+", nota))''',
      [OUT(r'''import re
print(re.findall(r"\d+", "1 maçã, 20 uvas"))''',
           ["[1, 20]", "['1', '2', '0']", "1 20"],
           "findall devolve textos (strings), e \\d+ junta os dígitos seguidos: '1' e '20'."),
       TYPE('import re\nprint(len(re.findall("a", "banana")))',
            "Há três letras a em banana."),
       MC("O que re.findall devolve quando não encontra nada?",
          "Uma lista vazia []", ["None", "Um erro", 'O texto vazio ""'],
          "findall sempre devolve lista. Por isso dá para usar len() ou um for sem medo."),
       CODE("Crie a função somar_numeros(texto) que devolve a soma de todos os números inteiros do texto. Ex.: somar_numeros(\"2 pizzas e 10 refris\") devolve 12.",
            "import re\n\ndef somar_numeros(texto):\n    pass\n",
            r'''import re

def somar_numeros(texto):
    return sum(int(n) for n in re.findall(r"\d+", texto))''',
            'assert somar_numeros("2 pizzas e 10 refris") == 12, "somar_numeros(\'2 pizzas e 10 refris\') deve ser 12"\n'
            'assert somar_numeros("100 e 250") == 350, "somar_numeros(\'100 e 250\') deve ser 350"\n'
            'assert somar_numeros("nada aqui") == 0, "Sem números, a soma deve ser 0"',
            "findall devolve textos: converta cada um com int() antes de somar."),
       ]),
    # lição 4
    L("Grupos e grupos com nome",
      "Parênteses ( ) marcam pedaços do padrão que você quer guardar. m.group(1) é o 1º grupo, m.group(2) o 2º, e m.group() é o trecho inteiro. Com (?P<nome>...) o grupo ganha um nome, e você pega com m.group(\"nome\"). Serve para separar dia, mês e ano de uma data ou o usuário de um e-mail.",
      r'''import re
m = re.search(r"(\d{2})/(\d{2})/(\d{4})", "Prova em 15/03/2026")
print(m.group(1), m.group(2), m.group(3))
m = re.search(r"(?P<usuario>\w+)@(?P<site>\w+)\.com", "fale com bia@loja.com")
print(m.group("usuario"), "-", m.group("site"))''',
      [OUT(r'''import re
m = re.search(r"(\w+) tem (\d+) anos", "Caio tem 9 anos")
print(m.group(2))''',
           ["Caio", "9 anos", "Caio tem 9 anos"], "O 2º par de parênteses guarda os dígitos: 9."),
       TYPE(r'''import re
m = re.search(r"(\d+)h(\d+)", "O filme começa às 19h30")
print(m.group(2))''',
            "O 2º grupo são os minutos, depois do h."),
       FILL("Complete para mostrar só o DDD (11).",
            r'''import re
m = re.search(r"DDD (?P<ddd>\d{2})", "DDD 11, número 98888-7777")
print(m.group(___))''',
            '"ddd"', ['"DDD"', '"?P<ddd>"', "0"],
            "O nome do grupo vai entre aspas, igualzinho ao que está em (?P<ddd>...)."),
       OUT(r'''import re
print(re.findall(r"(\w+)=(\d+)", "a=1 b=2"))''',
           ["['a=1', 'b=2']", "['a', '1', 'b', '2']", "[('a=1'), ('b=2')]"],
           "Com grupos, findall devolve só o que está nos grupos: uma tupla por achado."),
       ]),
    # lição 5
    L("Trocar e limpar: sub",
      r're.sub(padrao, troca, texto) troca TODOS os trechos achados. Use para limpar dados: \D é "qualquer coisa que NÃO é dígito", então re.sub(r"\D", "", cpf) deixa só os números. Na troca, \1, \2... repetem o que cada grupo achou, o que ajuda a formatar CPF e telefone.',
      r'''import re
cpf = "123.456.789-09"
print(re.sub(r"\D", "", cpf))
print(re.sub(r"\s+", " ", "muitos    espaços   aqui"))
print(re.sub(r"(\d{3})(\d{3})(\d{3})(\d{2})", r"\1.\2.\3-\4", "98765432100"))''',
      [OUT(r'''import re
print(re.sub(r"\d", "*", "senha123"))''',
           ["senha*", "***", "senha123"], r"Cada dígito é trocado por um *, então 123 vira ***."),
       TYPE(r'''import re
print(re.sub(r"\D", "", "(11) 4002-8922"))''',
            "Tudo que não é dígito (parênteses, espaço, traço) some."),
       MC(r'Em re.sub(r"(\d{2})(\d{4})", r"\1-\2", "119999"), o que o \1 significa?',
          "O que o primeiro grupo ( ) encontrou", ["O número 1", "A primeira letra do texto", "Repetir o padrão uma vez"],
          r"\1 copia o 1º grupo (11) e \2 o segundo (9999): o resultado é 11-9999."),
       CODE("Crie formatar_telefone(tel): ele recebe um celular com 11 dígitos, que pode vir com espaços, traços ou parênteses, e devolve no formato (11) 98765-4321.",
            "import re\n\ndef formatar_telefone(tel):\n    pass\n",
            r'''import re

def formatar_telefone(tel):
    numeros = re.sub(r"\D", "", tel)
    return re.sub(r"(\d{2})(\d{5})(\d{4})", r"(\1) \2-\3", numeros)''',
            'assert formatar_telefone("11987654321") == "(11) 98765-4321", "11987654321 deve virar (11) 98765-4321"\n'
            'assert formatar_telefone("21 99876-5432") == "(21) 99876-5432", "21 99876-5432 deve virar (21) 99876-5432"',
            r"Primeiro limpe com \D, depois use três grupos e monte com \1, \2 e \3."),
       ]),
    # lição 6
    L("Desafio: valores em R$",
      r'Juntando tudo: findall, grupos e quantificadores tiram dados de textos bagunçados, como um extrato. Atenção: símbolos como $ . + ( ) têm significado especial no padrão; para procurar o símbolo de verdade, ponha uma barra antes: \$ ou \.',
      r'''import re
extrato = "Mercado R$ 52,90; Uber R$ 18,50; Cinema R$ 30,00"
valores = re.findall(r"R\$ (\d+,\d{2})", extrato)
print(valores)
total = sum(float(v.replace(",", ".")) for v in valores)
print(f"Total: R$ {total:.2f}")''',
      [OUT(r'''import re
print(re.findall(r"\d+\.\d+", "pi vale 3.14 e e vale 2.71"))''',
           ["['3', '14', '2', '71']", "['3.14']", "[3.14, 2.71]"],
           r"\. é um ponto de verdade, então cada número decimal vem inteiro, como texto."),
       MC('Qual padrão encontra um preço como "R$ 9,99"?',
          r'r"R\$ \d+,\d{2}"', [r'r"R$ \d+,\d{2}"', r'r"R\$ \d,\d"', r'r"R\$ \w{2}"'],
          r"Sem a barra, $ significa fim do texto. E \d+ aceita reais com um ou mais dígitos."),
       ORDER("Monte o programa que mostra a lista de e-mails do texto.",
             ["import re",
              'texto = "Contato: ana@site.com ou caio@loja.com"',
              r'emails = re.findall(r"\w+@\w+\.com", texto)',
              "print(emails)"],
             "Importe, tenha o texto, procure com findall e só então mostre."),
       CODE("Crie total_gasto(texto) que soma todos os valores no formato R$ 12,50 do texto e devolve um float. Ex.: total_gasto(\"Pão R$ 8,00 e leite R$ 5,50\") devolve 13.5.",
            "import re\n\ndef total_gasto(texto):\n    pass\n",
            r'''import re

def total_gasto(texto):
    valores = re.findall(r"R\$ (\d+,\d{2})", texto)
    return sum(float(v.replace(",", ".")) for v in valores)''',
            'assert total_gasto("Pão R$ 8,00 e leite R$ 5,50") == 13.5, "Pão R$ 8,00 e leite R$ 5,50 deve dar 13.5"\n'
            'assert round(total_gasto("Luz R$ 120,35; água R$ 80,10; 3 boletos"), 2) == 200.45, "Deve somar só os valores em R$: 200.45"\n'
            'assert total_gasto("sem gastos hoje") == 0, "Sem valores, o total é 0"',
            r"Use um grupo para pegar só o número, troque a vírgula por ponto e converta com float()."),
       ]),
]

BUGS = r'''
@lib_re 3
import re
m = re.search(r"\d+", "sem números aqui")
print(m.group())
>>> print(m.group() if m else "nada encontrado")
!! Quando não acha nada, search devolve None, e None não tem .group(). Confira antes.

@lib_re 2
import re
m = re.match(r"\d+", "Pedido 42")
print(m.group())
>>> m = re.search(r"\d+", "Pedido 42")
!! match só olha o começo do texto, que é "Pedido". Para achar em qualquer lugar, use search.

@lib_re 3
import re
nums = re.findall(r"\d+", "3 bolos e 4 tortas")
total = sum(nums)
print(total)  # esperado: 7
>>> total = sum(int(n) for n in nums)
!! findall devolve textos. Converta cada um com int() antes de somar.

@lib_re 3
import re
m = re.search(r"(\d+) reais", "Custa 50 reais")
print(m.group(2))
>>> print(m.group(1))
!! O padrão só tem um par de parênteses, então só existe o grupo 1.

@lib_re 2
import re
print(re.findall(r"\d", "10 maçãs e 25 peras"))  # esperado: ['10', '25']
>>> print(re.findall(r"\d+", "10 maçãs e 25 peras"))  # esperado: ['10', '25']
!! \d pega um dígito só. Com \d+ os dígitos seguidos ficam juntos.

@lib_re 2
import re
print(re.findall(r"R$ (\d+)", "Total: R$ 50"))  # esperado: ['50']
>>> print(re.findall(r"R\$ (\d+)", "Total: R$ 50"))  # esperado: ['50']
!! No padrão, $ significa fim do texto. Para o cifrão de verdade, escreva \$.
'''
