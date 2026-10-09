from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_json", titulo="json",
               descricao="Transforme dicionários e listas em texto (e de volta): APIs, configurações, saves de jogo.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("JSON: dados como texto",
      "JSON é um jeito de escrever dicionários e listas como TEXTO, para salvar em arquivo ou mandar pela internet. Quase todo app e site usa: respostas de APIs, configurações, saves de jogo. Com import json, a função json.dumps(dados) transforma um dicionário ou lista em texto JSON.",
      '''import json
aluno = {"nome": "Ana", "nota": 9.5, "aprovada": True}
texto = json.dumps(aluno)
print(texto)
print(type(texto).__name__)''',
      [OUT('import json\nprint(json.dumps({"a": 1}))',
           ["{'a': 1}", "{a: 1}", '{"a":1}'],
           "JSON sempre usa aspas duplas, e dumps põe um espaço depois dos dois-pontos."),
       MC("Para que o JSON serve no dia a dia?",
          "Guardar e trocar dados entre programas em forma de texto",
          ["Deixar o Python mais rápido", "Desenhar gráficos", "Criar janelas e botões"],
          "Um app de clima, por exemplo, recebe a previsão do servidor em JSON."),
       TYPE('import json\nprint(json.dumps([1, "dois", 3]))',
            "Listas viram listas em JSON, e o texto fica com aspas duplas."),
       FILL("Complete para transformar o dicionário do pet em texto JSON.",
            'import json\npet = {"nome": "Rex", "idade": 3}\ntexto = json.___(pet)\nprint(texto)',
            "dumps", ["loads", "str", "text"],
            "dumps = dump string: transforma dados do Python em texto JSON."),
       ]),
    # lição 2
    L("dumps caprichado",
      "json.dumps tem opções úteis: indent=2 quebra as linhas e recua, deixando fácil de ler; ensure_ascii=False mantém os acentos (sem ela, ã vira \\u00e3); sort_keys=True coloca as chaves em ordem alfabética.",
      '''import json
receita = {"prato": "pão de queijo", "porções": 20}
print(json.dumps(receita))
print(json.dumps(receita, ensure_ascii=False))
print(json.dumps(receita, indent=2, ensure_ascii=False))''',
      [OUT('import json\nprint(json.dumps({"cidade": "Maceió"}))',
           ['{"cidade": "Maceió"}', "{'cidade': 'Maceió'}", '{"cidade": "Macei"}'],
           "Sem ensure_ascii=False, o ó vira um código \\u00f3."),
       TYPE('import json\nprint(json.dumps({"b": 2, "a": 1}, sort_keys=True))',
            "sort_keys=True ordena as chaves: a vem antes de b."),
       MC("O que indent=4 faz em json.dumps?",
          "Põe cada item numa linha, recuado com 4 espaços",
          ["Mostra só os 4 primeiros itens", "Arredonda números para 4 casas", "Repete o texto 4 vezes"],
          "indent deixa o JSON bonito para pessoas lerem, como num arquivo de configuração."),
       FILL("Complete para mostrar o nome com acento: {\"nome\": \"João\"}",
            'import json\nprint(json.dumps({"nome": "João"}, ___=False))',
            "ensure_ascii", ["acentos", "ascii", "utf8"],
            "ensure_ascii=False deixa os acentos como estão."),
       ]),
    # lição 3
    L("De texto para Python: loads",
      "json.loads(texto) faz o caminho de volta: lê um texto JSON e devolve dicionários e listas do Python. É o que você faz com a resposta de uma API. Depois disso, é só usar colchetes como em qualquer dicionário.",
      '''import json
resposta = '{"cidade": "Recife", "temp": 31, "chuva": false}'
dados = json.loads(resposta)
print(dados["cidade"], dados["temp"])
print(type(dados).__name__)
print(dados["chuva"])''',
      [OUT('import json\ndados = json.loads("[10, 20, 30]")\nprint(dados[1])',
           ["10", "[10, 20, 30]", "Erro"],
           "loads devolve uma lista de verdade; a posição 1 é o 20."),
       TYPE('import json\nd = json.loads(\'{"nome": "Teo", "idade": 8}\')\nprint(d["idade"] + 1)',
            "A idade vem como número, então dá para somar: 9."),
       MC("Qual a diferença entre json.dumps e json.loads?",
          "dumps: Python → texto JSON. loads: texto JSON → Python",
          ["São iguais, só muda o nome", "dumps lê arquivos e loads escreve arquivos", "dumps: texto → Python. loads: Python → texto"],
          "O s no final vem de string: as duas trabalham com texto."),
       CODE("A variável texto tem um JSON com as notas da turma. Use json.loads e mostre a média com uma casa decimal, assim: Média: 8.0",
            'import json\n\ntexto = \'{"turma": "6A", "notas": [7, 9, 8]}\'\n# transforme o texto e calcule a média\n',
            'import json\n\ntexto = \'{"turma": "6A", "notas": [7, 9, 8]}\'\ndados = json.loads(texto)\nnotas = dados["notas"]\nprint(f"Média: {sum(notas) / len(notas):.1f}")',
            'assert __stdout__.strip() == "Média: 8.0", "A saída deve ser exatamente: Média: 8.0"',
            'Depois do loads, dados["notas"] é uma lista comum: some e divida pelo len.'),
       ]),
    # lição 4
    L("Arquivos: dump e load",
      'Sem o s no final, json.dump(dados, arquivo) escreve direto num arquivo, e json.load(arquivo) lê dele. Abra o arquivo com open(..., encoding="utf-8"): "w" para escrever e sem "w" para ler. Assim seu programa lembra das coisas depois de fechar, como o save de um jogo.',
      '''import json
save = {"jogador": "Bia", "fase": 3, "itens": ["espada", "poção"]}
with open("save.json", "w", encoding="utf-8") as f:
    json.dump(save, f, ensure_ascii=False, indent=2)
with open("save.json", encoding="utf-8") as f:
    carregado = json.load(f)
print(carregado["fase"], carregado["itens"])''',
      [MC("Qual a diferença entre json.dump e json.dumps?",
          "dump escreve num arquivo; dumps devolve um texto",
          ["dump é mais novo e dumps está velho", "dump só aceita listas", "Nenhuma, são a mesma função"],
          "Lembre: com s = string (texto). Sem s = arquivo."),
       FILL("Complete para ler a configuração do arquivo.",
            'import json\nwith open("config.json", "w", encoding="utf-8") as f:\n    json.dump({"tema": "escuro"}, f)\nwith open("config.json", encoding="utf-8") as f:\n    config = json.___(f)\nprint(config["tema"])',
            "load", ["loads", "read", "open"],
            "load lê do arquivo. loads só aceita texto, não o arquivo f."),
       ORDER("Monte o programa que salva a lista de tarefas em tarefas.json.",
             ["import json",
              'tarefas = ["estudar", "passear com o Rex"]',
              'with open("tarefas.json", "w", encoding="utf-8") as f:',
              "    json.dump(tarefas, f, ensure_ascii=False)"],
             'Importe, crie os dados, abra com "w" e só então faça o dump dentro do with.'),
       CODE('Salve o dicionário agenda no arquivo agenda.json usando json.dump (abra com encoding="utf-8").',
            'import json\n\nagenda = {"Ana": "9999-1111", "Caio": "9888-2222"}\n# salve em agenda.json\n',
            'import json\n\nagenda = {"Ana": "9999-1111", "Caio": "9888-2222"}\nwith open("agenda.json", "w", encoding="utf-8") as f:\n    json.dump(agenda, f)',
            'import json, os\n'
            'assert os.path.exists("agenda.json"), "O arquivo agenda.json não foi criado"\n'
            'with open("agenda.json", encoding="utf-8") as f:\n'
            '    assert json.load(f) == agenda, "O arquivo deve ter exatamente o dicionário agenda"',
            'Use with open("agenda.json", "w", encoding="utf-8") as f: e, dentro, json.dump(agenda, f).'),
       ]),
    # lição 5
    L("Tipos e erros",
      "JSON tem nomes próprios: True vira true, False vira false, None vira null, e tuplas viram listas. As chaves de um objeto JSON são sempre textos. Se o texto não for JSON válido (por exemplo, com aspas simples), loads dá o erro json.JSONDecodeError, que você trata com try/except.",
      '''import json
print(json.dumps({"ok": True, "erro": None, "ponto": (3, 4)}))
print(json.loads("[true, null]"))
try:
    json.loads("{'nome': 'Ana'}")
except json.JSONDecodeError as e:
    print("JSON inválido:", type(e).__name__)''',
      [OUT('import json\nprint(json.dumps([True, False, None]))',
           ["[True, False, None]", '["true", "false", "null"]', "[true, false, None]"],
           "Em JSON: true, false e null, tudo minúsculo e sem aspas."),
       TYPE('import json\nprint(json.loads(json.dumps((1, 2))))',
            "A tupla vira lista no JSON e volta como lista: [1, 2]."),
       MC("Por que json.loads(\"{'a': 1}\") dá erro?",
          "JSON exige aspas duplas nos textos",
          ["Falta o import do dict", "O número 1 deveria estar entre aspas", "loads só aceita listas"],
          "Aspas simples são coisa do Python. No JSON, só aspas duplas."),
       FILL("Complete para tratar um JSON quebrado.",
            'import json\ntry:\n    json.loads("{nome: Ana}")\nexcept json.___ as e:\n    print(type(e).__name__)',
            "JSONDecodeError", ["JSONError", "DecodeError", "SyntaxError"],
            "json.JSONDecodeError é o erro de texto que não é JSON válido."),
       ]),
    # lição 6
    L("Desafio: pedido do delivery",
      "Juntando tudo: um app de delivery recebe o pedido em JSON, o programa lê com loads, faz as contas com dicionários e listas e devolve o resumo em JSON com dumps.",
      '''import json
pedido = '{"cliente": "Caio", "itens": [{"nome": "pizza", "preco": 45.0, "qtd": 1}, {"nome": "refri", "preco": 8.5, "qtd": 2}]}'
dados = json.loads(pedido)
total = sum(i["preco"] * i["qtd"] for i in dados["itens"])
resumo = {"cliente": dados["cliente"], "total": total}
print(json.dumps(resumo))''',
      [OUT('import json\nd = json.loads(\'{"a": [1, {"b": 2}]}\')\nprint(d["a"][1]["b"])',
           ["1", "{'b': 2}", "Erro"],
           'd["a"] é a lista, [1] é o dicionário {"b": 2} e ["b"] é o 2.'),
       MC("Um app de clima recebe a resposta '{\"temp\": 28}' como texto. Qual o primeiro passo para pegar a temperatura?",
          "dados = json.loads(resposta)",
          ['resposta["temp"]', "json.dumps(resposta)", "json.load(resposta)"],
          "Primeiro transforme o texto em dicionário com loads; depois use dados[\"temp\"]."),
       ORDER("Monte o programa que lê o JSON, soma 1 à fase e mostra o novo JSON.",
             ["import json",
              "save = json.loads('{\"fase\": 1}')",
              'save["fase"] = save["fase"] + 1',
              "print(json.dumps(save))"],
             "loads → mexe no dicionário → dumps."),
       CODE('Crie adicionar_tarefa(texto_json, tarefa): texto_json é um JSON como {"tarefas": ["lavar louça"]}. A função coloca a nova tarefa no fim da lista e DEVOLVE o novo texto JSON.',
            "import json\n\ndef adicionar_tarefa(texto_json, tarefa):\n    pass\n",
            'import json\n\ndef adicionar_tarefa(texto_json, tarefa):\n    dados = json.loads(texto_json)\n    dados["tarefas"].append(tarefa)\n    return json.dumps(dados)',
            'import json\n'
            'r = adicionar_tarefa(\'{"tarefas": ["lavar louça"]}\', "estudar")\n'
            'assert isinstance(r, str), "A função deve devolver um texto JSON (use json.dumps)"\n'
            'assert json.loads(r) == {"tarefas": ["lavar louça", "estudar"]}, "A nova tarefa deve ir para o fim da lista"\n'
            'assert json.loads(adicionar_tarefa(\'{"tarefas": []}\', "dormir"))["tarefas"] == ["dormir"], "Com a lista vazia, deve ficar só a nova tarefa"',
            "loads para virar dicionário, append na lista e dumps para voltar a ser texto."),
       ]),
]

BUGS = r'''
@lib_json 3
import json
pet = {"nome": "Rex"}
texto = json.loads(pet)
print(texto)
>>> texto = json.dumps(pet)
!! Para transformar o dicionário em texto, use dumps. loads faz o contrário.

@lib_json 2
import json
dados = json.loads("{'nome': 'Bia'}")
print(dados["nome"])
>>> dados = json.loads('{"nome": "Bia"}')
!! JSON só aceita aspas duplas nos textos.

@lib_json 4
import json
save = {"fase": 2}
with open("save.json", "w", encoding="utf-8") as f:
    json.dumps(save, f)
>>> json.dump(save, f)
!! Para escrever no arquivo, use dump (sem s). dumps só devolve texto.

@lib_json 4
import json
with open("c.json", "w", encoding="utf-8") as f:
    json.dump({"x": 1}, f)
with open("c.json", "w", encoding="utf-8") as f:
    print(json.load(f))
>>> with open("c.json", encoding="utf-8") as f:
!! Com "w" o arquivo abre só para escrever (e é apagado). Para ler, tire o "w".

@lib_json 2
import json
print(json.dumps({"fruta": "maçã"}))  # esperado: {"fruta": "maçã"}
>>> print(json.dumps({"fruta": "maçã"}, ensure_ascii=False))  # esperado: {"fruta": "maçã"}
!! Sem ensure_ascii=False, os acentos viram códigos como \u00e7.

@lib_json 3
import json
d = json.loads(json.dumps({1: "ouro"}))
print(d[1])
>>> print(d["1"])
!! No JSON as chaves são sempre texto: a chave 1 voltou como "1".
'''
