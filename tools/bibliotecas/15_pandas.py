from bt_helpers import OUT, TYPE, MC, FILL, ORDER, L

UNIDADE = dict(id="lib_pandas", titulo="pandas", descricao="Planilhas dentro do Python: tabelas, filtros, grupos e arquivos CSV.",
               externa=True, grupo="Bibliotecas externas")

LICOES = [
    L("O que é pandas e a Series",
      "pandas é a biblioteca para trabalhar com tabelas, como uma planilha dentro do Python. Você instala com pip install pandas e importa com import pandas as pd. A peça mais simples é a Series: uma coluna de valores com rótulos (o índice). Ela já sabe somar, tirar média e achar o maior.",
      'import pandas as pd\n\nvendas = pd.Series([120, 80, 95], index=["seg", "ter", "qua"])\nprint(vendas)\nprint(vendas["ter"])\nprint(vendas.sum())\nprint(vendas.max())',
      [MC("Qual é o jeito de costume de importar o pandas?", "import pandas as pd", ["import pandas as pa", "from pandas import *", "import pd"], "O apelido pd é usado em praticamente todo tutorial e projeto."),
       TYPE('import pandas as pd\ngastos = pd.Series([30, 45, 25])\nprint(gastos.sum())', "sum soma todos os valores da Series: 30 + 45 + 25."),
       OUT('import pandas as pd\ns = pd.Series([7, 9, 5], index=["Ana", "Bia", "Caio"])\nprint(s["Bia"])', ["7", "1", "Erro"], "Com índice de nomes, s[\"Bia\"] pega o valor com esse rótulo."),
       FILL("Complete para criar uma Series com as notas.", 'import pandas as pd\nnotas = pd.___([8, 6, 10])\nprint(notas.mean())', "Series", ["series", "List", "Column"], "Series começa com S maiúsculo: pd.Series(lista).")]),
    L("DataFrame: a tabela",
      "O DataFrame é a tabela completa, com várias colunas. O jeito mais fácil de criar é com um dicionário: cada chave vira o nome de uma coluna e cada lista vira os valores. Depois, .shape diz (linhas, colunas), .columns lista os nomes das colunas e .head(n) mostra só as primeiras n linhas.",
      'import pandas as pd\n\nturma = pd.DataFrame({\n    "aluno": ["Ana", "Bia", "Caio", "Davi"],\n    "nota": [8, 6, 9, 5],\n})\nprint(turma)\nprint(turma.shape)\nprint(list(turma.columns))\nprint(len(turma.head(2)))',
      [TYPE('import pandas as pd\ndf = pd.DataFrame({"produto": ["café", "pão", "leite"], "preco": [12, 1, 5]})\nprint(df.shape)', "3 linhas (produtos) e 2 colunas (produto e preco)."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"nome": ["Rex", "Mia"], "idade": [3, 5], "peso": [20, 4]})\nprint(list(df.columns))', ["['Rex', 'Mia']", "[3, 5]", "['nome', 'idade']"], "As chaves do dicionário viram os nomes das colunas, na mesma ordem."),
       MC("Num DataFrame com 1000 vendas, o que df.head() mostra?", "As 5 primeiras linhas", ["A primeira linha", "Os nomes das colunas", "As 5 maiores vendas"], "Sem número, head mostra 5 linhas. É ótimo para dar uma espiada numa tabela grande."),
       FILL("Complete para criar a tabela a partir do dicionário.", 'import pandas as pd\ndados = {"cidade": ["Recife", "Natal"], "temp": [30, 29]}\ndf = pd.___(dados)\nprint(df.shape)', "DataFrame", ["Dataframe", "Table", "Series"], "O nome é DataFrame, com D e F maiúsculos.")]),
    L("Selecionando e filtrando",
      "df[\"coluna\"] pega uma coluna (uma Series). df.loc[rótulo, \"coluna\"] busca pelo rótulo da linha, e df.iloc[posição] pela posição, contando do 0. Para filtrar, crie uma condição com a coluna e coloque dentro dos colchetes: df[df[\"nota\"] >= 7] fica só com quem passou.",
      'import pandas as pd\n\nturma = pd.DataFrame({"aluno": ["Ana", "Bia", "Caio", "Davi"], "nota": [8, 6, 9, 5]})\nprint(turma["nota"].tolist())\nprint(turma.loc[2, "aluno"])\nprint(turma.iloc[0]["aluno"])\naprovados = turma[turma["nota"] >= 7]\nprint(aprovados["aluno"].tolist())',
      [TYPE('import pandas as pd\ndf = pd.DataFrame({"aluno": ["Ana", "Bia", "Caio"], "nota": [8, 4, 7]})\nprint(df[df["nota"] >= 7]["aluno"].tolist())', "Só ficam as linhas com nota 7 ou mais: Ana (8) e Caio (7)."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"pet": ["Rex", "Mia", "Tom"], "idade": [3, 5, 2]})\nprint(df.iloc[1]["pet"])', ["Rex", "Tom", "5"], "iloc conta posições a partir do 0, então iloc[1] é a segunda linha."),
       MC("Qual linha fica só com as vendas acima de 100 reais?", 'df[df["valor"] > 100]', ['df["valor"] > 100', 'df[valor > 100]', 'df.filter("valor" > 100)'], "A condição sozinha gera só True/False; ela precisa ir dentro de df[...]. E o nome da coluna vai entre aspas."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"produto": ["café", "pão", "leite"], "estoque": [0, 12, 3]})\nprint(len(df[df["estoque"] == 0]))', ["0", "3", "café"], "Só uma linha tem estoque igual a 0, então o filtro tem tamanho 1.")]),
    L("Novas colunas e contas",
      "Criar uma coluna é como criar uma chave de dicionário: df[\"total\"] = df[\"preco\"] * df[\"qtd\"]. A conta é feita linha por linha, sem precisar de for. Você também pode usar contas com números, como aplicar 10% de desconto em todos os preços.",
      'import pandas as pd\n\nvendas = pd.DataFrame({"produto": ["café", "pão", "bolo"], "preco": [12.0, 1.5, 30.0], "qtd": [2, 10, 1]})\nvendas["total"] = vendas["preco"] * vendas["qtd"]\nprint(vendas["total"].tolist())\nprint(vendas["total"].sum())\nprint(list(vendas.columns))',
      [TYPE('import pandas as pd\ndf = pd.DataFrame({"preco": [10, 20], "qtd": [3, 2]})\ndf["total"] = df["preco"] * df["qtd"]\nprint(df["total"].tolist())', "Linha por linha: 10 * 3 e 20 * 2."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"a": [1, 2]})\ndf["b"] = df["a"] + 10\nprint(df.shape)', ["(2, 1)", "(3, 2)", "(2, 11)"], "A nova coluna b entra na tabela: continuam 2 linhas, agora com 2 colunas."),
       FILL("Complete para aplicar 10% de desconto em todos os preços.", 'import pandas as pd\ndf = pd.DataFrame({"preco": [100, 50]})\ndf["com_desconto"] = df["preco"] ___ 0.9\nprint(df["com_desconto"].tolist())', "*", ["-", "+", "/"], "Pagar 90% do preço é multiplicar por 0.9."),
       MC("Para criar a coluna media com a média de p1 e p2, qual é o código certo?", 'df["media"] = (df["p1"] + df["p2"]) / 2', ['df["media"] = df["p1"] + df["p2"] / 2', 'df.media = mean(p1, p2)', 'df["media"] = (p1 + p2) / 2'], "Os parênteses garantem que a soma acontece antes da divisão, e cada coluna é lida com df[\"nome\"].")]),
    L("Agrupando: groupby",
      "groupby junta as linhas que têm o mesmo valor numa coluna e calcula algo para cada grupo, como uma tabela dinâmica de planilha. df.groupby(\"vendedor\")[\"valor\"].sum() dá o total de cada vendedor. Também existem .mean(), .count() e .agg([\"sum\", \"mean\"]) para várias contas de uma vez.",
      'import pandas as pd\n\nvendas = pd.DataFrame({\n    "vendedor": ["Ana", "Bia", "Ana", "Bia", "Ana"],\n    "valor": [100, 80, 50, 120, 30],\n})\ntotais = vendas.groupby("vendedor")["valor"].sum()\nprint(totais)\nprint(totais.to_dict())\nprint(vendas.groupby("vendedor")["valor"].mean().round(1).to_dict())',
      [TYPE('import pandas as pd\ndf = pd.DataFrame({"time": ["A", "B", "A"], "gols": [2, 1, 3]})\nprint(df.groupby("time")["gols"].sum().to_dict())', "O time A tem 2 + 3 gols e o time B tem 1."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"turma": ["1A", "1B", "1A", "1B"], "nota": [8, 6, 6, 10]})\nprint(df.groupby("turma")["nota"].mean().to_dict())', ["{'1A': 14, '1B': 16}", "{'1A': 7.5, '1B': 7.5}", "{'1A': 8, '1B': 6}"], "Média de cada turma: 1A = (8 + 6) / 2 e 1B = (6 + 10) / 2."),
       MC("Numa planilha de gastos com as colunas categoria e valor, como saber quanto foi gasto em cada categoria?", 'df.groupby("categoria")["valor"].sum()', ['df["valor"].sum()', 'df.groupby("valor")["categoria"].sum()', 'df.sort_values("categoria")'], "Agrupe pela categoria e some a coluna valor dentro de cada grupo."),
       ORDER("Monte o programa que mostra quantas vendas cada vendedor fez.",
             ["import pandas as pd", 'df = pd.DataFrame({"vendedor": ["Ana", "Bia", "Ana"], "valor": [10, 20, 30]})', 'contagem = df.groupby("vendedor")["valor"].count()', "print(contagem.to_dict())"],
             "import, depois a tabela, o agrupamento e por fim o print.")]),
    L("Desafio: CSV e ordenação",
      "Na vida real os dados chegam em arquivos. df.to_csv(\"arquivo.csv\", index=False) salva a tabela e pd.read_csv(\"arquivo.csv\") lê de volta. Depois, sort_values(\"coluna\", ascending=False) ordena do maior para o menor e value_counts() conta quantas vezes cada valor aparece. Juntando tudo, você faz um relatório de vendas em poucas linhas.",
      'import pandas as pd\n\nvendas = pd.DataFrame({"produto": ["café", "pão", "café", "bolo"], "valor": [24, 15, 12, 30]})\nvendas.to_csv("vendas.csv", index=False)\n\ndf = pd.read_csv("vendas.csv")\nprint(df.shape)\nprint(df.sort_values("valor", ascending=False)["produto"].tolist())\nprint(df["produto"].value_counts().to_dict())',
      [TYPE('import pandas as pd\nwith open("notas.csv", "w", encoding="utf-8") as f:\n    f.write("aluno,nota\\nAna,8\\nBia,6\\nCaio,9\\n")\ndf = pd.read_csv("notas.csv")\nprint(df.shape)', "A primeira linha do arquivo é o cabeçalho; sobram 3 linhas de dados e 2 colunas."),
       OUT('import pandas as pd\ndf = pd.DataFrame({"aluno": ["Ana", "Bia", "Caio"], "nota": [8, 6, 9]})\nprint(df.sort_values("nota")["aluno"].tolist())', ["['Caio', 'Ana', 'Bia']", "['Ana', 'Bia', 'Caio']", "[6, 8, 9]"], "Sem ascending=False, sort_values ordena do menor para o maior: 6, 8, 9."),
       MC("Para que serve index=False em df.to_csv(\"vendas.csv\", index=False)?", "Para não gravar a coluna de números do índice no arquivo", ["Para não gravar a linha de cabeçalho", "Para salvar sem apagar o arquivo antigo", "Para ordenar as linhas antes de salvar"], "Sem index=False, o CSV ganha uma coluna extra com 0, 1, 2..."),
       ORDER("Monte o programa: salvar as vendas em CSV, ler de volta e mostrar o produto mais vendido.",
             ["import pandas as pd", 'df = pd.DataFrame({"produto": ["café", "pão", "café"]})', 'df.to_csv("v.csv", index=False)', 'lido = pd.read_csv("v.csv")', 'print(lido["produto"].value_counts().idxmax())'],
             "Primeiro cria e salva, depois lê; value_counts conta e idxmax pega o produto que mais aparece.")]),
]

BUGS = r'''
@lib_pandas 2
import pandas as pd
df = pd.dataframe({"nota": [7, 8]})
print(df.shape)
>>> df = pd.DataFrame({"nota": [7, 8]})
!! O nome é DataFrame, com D e F maiúsculos.

@lib_pandas 3
import pandas as pd
df = pd.DataFrame({"aluno": ["Ana", "Bia"], "nota": [8, 5]})
print(df["Nota"].tolist())
>>> print(df["nota"].tolist())
!! O nome da coluna é nota, com n minúsculo. Nomes de colunas diferenciam maiúsculas.

@lib_pandas 3
import pandas as pd
df = pd.DataFrame({"aluno": ["Ana", "Bia", "Caio"], "nota": [8, 5, 9]})
aprovados = df["nota"] >= 7
print(len(aprovados))  # esperado: 2
>>> aprovados = df[df["nota"] >= 7]
!! A condição sozinha é só uma coluna de True/False. Coloque-a dentro de df[...] para filtrar.

@lib_pandas 3
import pandas as pd
df = pd.DataFrame({"pet": ["Rex", "Mia", "Tom"]})
print(df.iloc[3]["pet"])  # esperado: Tom
>>> print(df.iloc[2]["pet"])  # esperado: Tom
!! iloc começa no 0: a terceira linha é a posição 2.

@lib_pandas 3
import pandas as pd
df = pd.DataFrame({"vendedor": ["Ana", "Bia", "Ana"], "valor": [10, 20, 30]})
print(df.groupby("valor")["vendedor"].count().to_dict())  # esperado: {'Ana': 40, 'Bia': 20}
>>> print(df.groupby("vendedor")["valor"].sum().to_dict())  # esperado: {'Ana': 40, 'Bia': 20}
!! As colunas estavam trocadas e count só conta linhas: agrupe por vendedor e use sum na coluna valor.

@lib_pandas 3
import pandas as pd
df = pd.DataFrame({"produto": ["café", "pão", "bolo"], "valor": [24, 15, 30]})
print(df.sort_values("valor")["produto"].tolist()[0])  # esperado: bolo
>>> print(df.sort_values("valor", ascending=False)["produto"].tolist()[0])  # esperado: bolo
!! Para o maior aparecer primeiro, use ascending=False.
'''
