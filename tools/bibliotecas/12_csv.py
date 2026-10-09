from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_csv", titulo="csv",
               descricao="Leia e crie planilhas em texto (CSV): notas, vendas, listas de compras...",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("CSV e o writer",
      'CSV é uma planilha em forma de texto: cada linha é um registro e os valores são separados por vírgula. Excel e Google Planilhas abrem CSV. Com import csv, csv.writer(arquivo) cria um "escritor": writerow([...]) grava uma linha e writerows([[...], [...]]) grava várias. Abra o arquivo com newline="" e encoding="utf-8".',
      '''import csv
with open("notas.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.writer(f)
    escritor.writerow(["nome", "nota"])
    escritor.writerow(["Ana", 9])
    escritor.writerows([["Caio", 7], ["Bia", 10]])
with open("notas.csv", encoding="utf-8") as f:
    print(f.read())''',
      [OUT('import csv\nwith open("a.csv", "w", newline="", encoding="utf-8") as f:\n    csv.writer(f).writerow(["pão", 2, 0.5])\nwith open("a.csv", encoding="utf-8") as f:\n    print(f.read())',
           ["['pão', 2, 0.5]", "pão 2 0.5", "pão;2;0.5"],
           "writerow junta os valores com vírgula, sem colchetes nem aspas."),
       MC('Por que abrimos o arquivo com newline="" ao usar csv.writer?',
          "Para não aparecerem linhas em branco extras entre as linhas",
          ["Para o arquivo começar vazio", "Para os acentos funcionarem", "Para separar valores com ponto e vírgula"],
          'O csv cuida das quebras de linha sozinho. Sem newline="", no Windows surge uma linha vazia entre cada registro.'),
       FILL("Complete para gravar as duas linhas de uma vez.",
            'import csv\nwith open("estoque.csv", "w", newline="", encoding="utf-8") as f:\n    escritor = csv.writer(f)\n    escritor.___([["lápis", 30], ["caderno", 12]])',
            "writerows", ["writerow", "write", "rows"],
            "writerows (com s) recebe uma lista de linhas. writerow grava uma linha só."),
       CODE("Crie o arquivo compras.csv com 3 linhas: o cabeçalho item,qtd e depois arroz,2 e feijão,1.",
            'import csv\n\n# crie compras.csv aqui\n',
            'import csv\n\nwith open("compras.csv", "w", newline="", encoding="utf-8") as f:\n    escritor = csv.writer(f)\n    escritor.writerow(["item", "qtd"])\n    escritor.writerow(["arroz", 2])\n    escritor.writerow(["feijão", 1])',
            'import os\n'
            'assert os.path.exists("compras.csv"), "O arquivo compras.csv não foi criado"\n'
            'with open("compras.csv", encoding="utf-8") as f:\n'
            '    linhas = f.read().splitlines()\n'
            'assert linhas == ["item,qtd", "arroz,2", "feijão,1"], f"O arquivo deve ter item,qtd / arroz,2 / feijão,1 (veio {linhas})"',
            'Abra com "w", newline="" e encoding="utf-8", crie o writer e use writerow para cada linha.'),
       ]),
    # lição 2
    L("Lendo: csv.reader",
      'csv.reader(arquivo) lê o CSV e devolve cada linha como uma LISTA de textos. A primeira linha costuma ser o cabeçalho: next(leitor) pula ela. Atenção: tudo vem como texto, então use int() ou float() para fazer contas. Dica: csv.reader também aceita uma lista de linhas, como texto.splitlines().',
      '''import csv
with open("pets.csv", "w", newline="", encoding="utf-8") as f:
    f.write("nome,especie,idade\\nRex,cachorro,3\\nMia,gato,5\\n")
with open("pets.csv", newline="", encoding="utf-8") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    for linha in leitor:
        print(linha)''',
      [OUT('import csv\nleitor = csv.reader(["uva,7,kg"])\nprint(next(leitor))',
           ["['uva', 7, 'kg']", "uva,7,kg", "['uva,7,kg']"],
           "Cada linha vira uma lista, e o 7 vem como texto: '7'."),
       TYPE('import csv\nlinha = next(csv.reader(["Ana,8"]))\nprint(int(linha[1]) + 2)',
            "linha[1] é o texto '8'; com int() vira 8 e somado a 2 dá 10."),
       MC("Lendo com csv.reader a linha Teo,12, de que tipo é o 12?",
          "str (texto)", ["int (número inteiro)", "float (decimal)", "Depende do Excel"],
          "O csv não adivinha tipos: tudo vem como texto. Converta quando precisar."),
       ORDER("Monte o programa que mostra só os nomes, pulando o cabeçalho.",
             ["import csv",
              'texto = "nome,idade\\nRex,3\\nMia,5"',
              "leitor = csv.reader(texto.splitlines())",
              "cabecalho = next(leitor)",
              "for linha in leitor:",
              "    print(linha[0])"],
             "Crie o leitor, pule o cabeçalho com next e depois percorra o resto."),
       ]),
    # lição 3
    L("Linhas como dicionário: DictReader",
      'csv.DictReader usa o cabeçalho como chaves: cada linha vira um dicionário. Em vez de lembrar que a nota é a coluna 1, você escreve aluno["nota"]. O cabeçalho é lido sozinho, não precisa de next.',
      '''import csv
with open("alunos.csv", "w", newline="", encoding="utf-8") as f:
    f.write("nome,nota\\nAna,9\\nTeo,6\\n")
with open("alunos.csv", newline="", encoding="utf-8") as f:
    for aluno in csv.DictReader(f):
        print(aluno["nome"], "tirou", aluno["nota"])''',
      [OUT('import csv\nfor d in csv.DictReader(["nome,idade", "Bia,12"]):\n    print(d["idade"])',
           ["Bia", "idade", "{'nome': 'Bia', 'idade': '12'}"],
           'A chave "idade" vem do cabeçalho, e o valor da linha da Bia é 12.'),
       TYPE('import csv\nprint(next(csv.DictReader(["a,b", "1,2"])))',
            "A primeira linha de dados vira um dicionário com as chaves do cabeçalho."),
       MC("De onde o DictReader tira as chaves de cada dicionário?",
          "Da primeira linha do arquivo (o cabeçalho)",
          ["Ele numera as colunas: 0, 1, 2...", "Você precisa passar sempre fieldnames", "Do nome do arquivo"],
          "Por padrão, a primeira linha vira as chaves. Por isso o cabeçalho não aparece como dado."),
       CODE("Use csv.DictReader para mostrar o nome dos alunos aprovados (nota 7 ou mais), um por linha.",
            'import csv\n\ntexto = "nome,nota\\nAna,9\\nCaio,5\\nBia,7"\n# use csv.DictReader(texto.splitlines())\n',
            'import csv\n\ntexto = "nome,nota\\nAna,9\\nCaio,5\\nBia,7"\nfor aluno in csv.DictReader(texto.splitlines()):\n    if int(aluno["nota"]) >= 7:\n        print(aluno["nome"])',
            'assert __stdout__.split() == ["Ana", "Bia"], "Devem aparecer só Ana e Bia, um por linha"',
            'A nota vem como texto: compare int(aluno["nota"]) >= 7.'),
       ]),
    # lição 4
    L("Gravando dicionários: DictWriter",
      'csv.DictWriter(arquivo, fieldnames=[...]) grava dicionários. fieldnames diz quais colunas existem e em que ordem. writeheader() grava o cabeçalho e writerow({...}) grava uma linha. Perfeito quando seus dados já estão em dicionários, como uma lista de contatos.',
      '''import csv
contatos = [{"nome": "Ana", "tel": "9999-1111"}, {"nome": "Caio", "tel": "9888-2222"}]
with open("contatos.csv", "w", newline="", encoding="utf-8") as f:
    escritor = csv.DictWriter(f, fieldnames=["nome", "tel"])
    escritor.writeheader()
    escritor.writerows(contatos)
with open("contatos.csv", encoding="utf-8") as f:
    print(f.read())''',
      [FILL("Complete para gravar a linha de cabeçalho nome,nota.",
            'import csv\nwith open("t.csv", "w", newline="", encoding="utf-8") as f:\n    escritor = csv.DictWriter(f, fieldnames=["nome", "nota"])\n    escritor.___()\n    escritor.writerow({"nome": "Ana", "nota": 9})',
            "writeheader", ["writerow", "header", "writefields"],
            "writeheader() escreve os fieldnames como primeira linha."),
       OUT('import csv\nwith open("p.csv", "w", newline="", encoding="utf-8") as f:\n    w = csv.DictWriter(f, fieldnames=["preco", "item"])\n    w.writerow({"item": "bolo", "preco": 20})\nwith open("p.csv", encoding="utf-8") as f:\n    print(f.read())',
           ["bolo,20", "item,preco\nbolo,20", "{'item': 'bolo', 'preco': 20}"],
           "A ordem das colunas vem de fieldnames (preco, item), não do dicionário. E sem writeheader não há cabeçalho."),
       MC("Para que serve fieldnames no DictWriter?",
          "Dizer quais colunas existem e em que ordem",
          ["Dar nome ao arquivo", "Escolher o separador", "Ordenar as linhas pelo nome"],
          "Sem fieldnames o DictWriter não sabe montar as colunas e dá erro."),
       ORDER("Monte o programa que grava um pet no arquivo pets.csv com cabeçalho.",
             ["import csv",
              'with open("pets.csv", "w", newline="", encoding="utf-8") as f:',
              '    escritor = csv.DictWriter(f, fieldnames=["nome", "especie"])',
              "    escritor.writeheader()",
              '    escritor.writerow({"nome": "Rex", "especie": "cachorro"})'],
             "Abra o arquivo, crie o DictWriter, grave o cabeçalho e depois os dados."),
       ]),
    # lição 5
    L("Ponto e vírgula e aspas",
      'No Brasil, o Excel costuma salvar CSV com ponto e vírgula (;), porque a vírgula já é usada nos decimais (18,90). Para isso, passe delimiter=";" ao reader e ao writer. E se um valor tiver o próprio separador dentro, o csv põe esse valor entre aspas automaticamente (isso se chama quoting), e na leitura as aspas somem.',
      '''import csv
linhas = ["produto;preço", "Café;18,90"]
for linha in csv.reader(linhas, delimiter=";"):
    print(linha)
with open("itens.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow(["Café, 500g", 18.9])
with open("itens.csv", encoding="utf-8") as f:
    print(f.read())''',
      [OUT('import csv\nprint(next(csv.reader(["a;b;c"])))',
           ["['a', 'b', 'c']", "a b c", "['a;', 'b;', 'c']"],
           'Sem delimiter=";", o reader procura vírgulas. Como não há nenhuma, a linha inteira vira um valor só.'),
       TYPE('import csv\nprint(next(csv.reader([\'"Silva, Ana",30\'])))',
            "As aspas protegem a vírgula do nome: são 2 valores, e as aspas somem."),
       MC("Por que muitas planilhas brasileiras usam ; em vez de , no CSV?",
          "Porque a vírgula já separa os decimais, como em 18,90",
          ["Porque o Python não lê vírgulas", "Porque ; ocupa menos espaço", "Porque é obrigatório por lei"],
          "Com ; dá para escrever 18,90 sem confundir com uma nova coluna."),
       FILL("Complete para ler uma planilha exportada do Excel brasileiro.",
            'import csv\nlinha = next(csv.reader(["Bia;9,5"], ___=";"))\nprint(linha)',
            "delimiter", ["sep", "separator", "split"],
            'O parâmetro se chama delimiter. (sep é do print, não do csv.)'),
       ]),
    # lição 6
    L("Desafio: somando as vendas",
      'Juntando tudo: ler uma planilha de vendas no padrão brasileiro (com ; e vírgula decimal) com DictReader, converter os valores e somar. Para "18,90" virar número: valor.replace(",", ".") e depois float().',
      '''import csv
with open("vendas.csv", "w", newline="", encoding="utf-8") as f:
    f.write("produto;valor\\nbolo;35,00\\ncafé;7,50\\nsuco;9,90\\n")
total = 0
with open("vendas.csv", newline="", encoding="utf-8") as f:
    for venda in csv.DictReader(f, delimiter=";"):
        total += float(venda["valor"].replace(",", "."))
print(f"Total vendido: R$ {total:.2f}")''',
      [OUT('print(float("12,50".replace(",", ".")) * 2)',
           ["24,0", "Erro", "12.5"],
           '"12,50" vira "12.50", depois o número 12.5, e vezes 2 dá 25.0.'),
       MC("Ao ler 'valor' de uma planilha brasileira, o que acontece com float(\"7,50\")?",
          "Dá ValueError: o Python só entende ponto decimal",
          ["Vira 7.5 normalmente", "Vira 750", "Vira 7"],
          "Troque a vírgula pelo ponto antes de converter."),
       ORDER("Monte o programa que mostra a quantidade total de itens.",
             ["import csv",
              'linhas = ["item;qtd", "lápis;3", "caneta;2"]',
              "total = 0",
              'for l in csv.DictReader(linhas, delimiter=";"):',
              '    total += int(l["qtd"])',
              "print(total)"],
             "O total começa em 0 antes do laço e só é mostrado depois dele."),
       CODE('Crie total_vendas(arquivo): ela lê um CSV separado por ; com as colunas produto;valor (valores como 35,00) e devolve a soma dos valores como float.',
            "import csv\n\ndef total_vendas(arquivo):\n    pass\n",
            'import csv\n\ndef total_vendas(arquivo):\n    total = 0\n    with open(arquivo, newline="", encoding="utf-8") as f:\n        for venda in csv.DictReader(f, delimiter=";"):\n            total += float(venda["valor"].replace(",", "."))\n    return total',
            'with open("loja.csv", "w", encoding="utf-8") as f:\n'
            '    f.write("produto;valor\\nbolo;35,00\\ncafé;7,50\\n")\n'
            'assert total_vendas("loja.csv") == 42.5, "loja.csv tem 35,00 + 7,50: deve dar 42.5"\n'
            'with open("vazia.csv", "w", encoding="utf-8") as f:\n'
            '    f.write("produto;valor\\n")\n'
            'assert total_vendas("vazia.csv") == 0, "Sem vendas, o total deve ser 0"',
            'Use DictReader com delimiter=";" e converta cada valor com replace e float.'),
       ]),
]

BUGS = r'''
@lib_csv 6
import csv
linhas = ["item,qtd", "lápis,3", "caneta,2"]
leitor = csv.DictReader(linhas)
total = 0
for l in leitor:
    total += l["qtd"]
print(total)
>>> total += int(l["qtd"])
!! O csv lê tudo como texto. Converta com int() antes de somar.

@lib_csv 2
import csv
linha = next(csv.reader(["Ana;9"]))
print(linha[1])
>>> linha = next(csv.reader(["Ana;9"], delimiter=";"))
!! O separador é ponto e vírgula. Sem delimiter=";", a linha vira um valor só.

@lib_csv 3
import csv
linhas = ["nome,nota", "Ana,9", "Bia,8"]
leitor = csv.reader(linhas)
for l in leitor:
    print(int(l[1]))
>>> leitor = csv.reader(linhas[1:])
!! A primeira linha é o cabeçalho, e "nota" não vira número. Pule essa linha.

@lib_csv 3
import csv
with open("a.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f)
    w.writeheader()
    w.writerow({"nome": "Rex"})
>>> w = csv.DictWriter(f, fieldnames=["nome"])
!! O DictWriter precisa de fieldnames para saber quais colunas gravar.

@lib_csv 3
import csv
with open("n.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerow("Ana")
with open("n.csv", encoding="utf-8") as f:
    print(f.read())  # esperado: Ana
>>> csv.writer(f).writerow(["Ana"])
!! writerow espera uma lista. Um texto solto vira uma coluna por letra: A,n,a.

@lib_csv 2
import csv
linhas = ["nome, nota", "Ana, 9"]
for l in csv.DictReader(linhas):
    print(l["nota"])
>>> linhas = ["nome,nota", "Ana,9"]
!! O espaço depois da vírgula faz parte do nome da coluna: a chave virou " nota".
'''
