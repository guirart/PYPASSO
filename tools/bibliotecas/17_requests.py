from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_requests", titulo="Requests (internet)",
               descricao="Conversar com sites e APIs: pedir dados, ler JSON e tratar erros.",
               externa=True, grupo="Bibliotecas externas")

# Nada aqui usa a internet de verdade: montamos os pedidos sem enviar
# (requests.Request(...).prepare()) e criamos respostas de mentirinha.

LICOES = [
    # lição 1
    L("Pedidos e status_code",
      "Quando um app mostra a previsão do tempo, ele faz uma requisição HTTP: pede dados a um servidor e recebe uma resposta. Um endereço que devolve dados para programas se chama API. A biblioteca requests faz esses pedidos (instale com pip install requests): resposta = requests.get(url) busca a página, e resposta.status_code conta como foi: 200 é sucesso, 404 é não encontrado, 500 é erro no servidor. resposta.ok é True quando o código é menor que 400.",
      'import requests\n\n# na vida real: resposta = requests.get("https://api.exemplo.com/piadas")\npedido = requests.Request("GET", "https://api.exemplo.com/piadas").prepare()\nprint(pedido.method, pedido.url)\n\n# uma resposta de mentirinha, só para ver o status\nresposta = requests.Response()\nresposta.status_code = 200\nprint(resposta.status_code, resposta.ok)',
      [MC("Como instalar a requests no seu computador?",
          "pip install requests (no terminal)",
          ["Ela já vem com o Python", "pip install request", "import requests --install"],
          "requests é externa: instale com pip. Repare no s no final do nome."),
       MC("Você pediu https://api.exemplo.com/pets/999 e veio status_code 404. O que isso quer dizer?",
          "O que você pediu não foi encontrado",
          ["Deu tudo certo", "O servidor quebrou", "Sua internet caiu"],
          "404 é o famoso \"não encontrado\". Tudo certo seria 200 e erro do servidor seria 500."),
       OUT('import requests\n\nr = requests.Response()\nr.status_code = 404\nprint(r.ok)',
           ["True", "404", "None"],
           "ok só é True para códigos abaixo de 400. 404 é erro, então False."),
       FILL("Complete para conferir se o pedido deu certo.",
            'import requests\n\nresposta = requests.Response()\nresposta.status_code = 200\nif resposta.___ == 200:\n    print("Deu certo!")',
            "status_code", ["status", "code", "ok"],
            "O número do resultado fica em status_code.")]),
    # lição 2
    L("params: montando a URL",
      "Muitas APIs recebem opções no fim da URL, depois do ?, como ?cidade=Recife&dias=3. Em vez de escrever isso na mão, passe um dicionário em params: a requests monta a URL e cuida de espaços e acentos. Na vida real: requests.get(url, params={...}). Aqui usamos Request(...).prepare().url para ver a URL final sem enviar nada.",
      'import requests\n\nopcoes = {"ingrediente": "frango", "porcoes": 4}\npedido = requests.Request("GET", "https://api.exemplo.com/receitas", params=opcoes).prepare()\nprint(pedido.url)',
      [OUT('import requests\n\np = requests.Request("GET", "https://api.exemplo.com/busca", params={"q": "gato preto"}).prepare()\nprint(p.url)',
           ["https://api.exemplo.com/busca?q=gato preto", "https://api.exemplo.com/busca?gato+preto", "https://api.exemplo.com/busca/q/gato+preto"],
           "O espaço não pode ir na URL; a requests troca por +. Cada opção vira nome=valor."),
       TYPE('import requests\n\np = requests.Request("GET", "https://api.exemplo.com/fotos", params={"pagina": 2}).prepare()\nprint(p.url)',
            "A opção vai depois do ?, no formato nome=valor."),
       MC("Por que usar params={...} em vez de colar o texto na URL?",
          "A requests junta tudo com ? e & e trata espaços e acentos para você",
          ["Porque URLs com ? não funcionam", "Porque params deixa o pedido mais rápido", "Porque sem params a resposta não vem em JSON"],
          "Montar na mão é fácil de errar (um & a menos, um espaço). Com params o dicionário vira URL certinha."),
       FILL("Complete para pedir a previsão de Recife.",
            'import requests\n\np = requests.Request("GET", "https://api.exemplo.com/clima", ___={"cidade": "Recife"}).prepare()\nprint(p.url)',
            "params", ["dados", "query", "args"],
            "As opções da URL vão em params.")]),
    # lição 3
    L("Lendo respostas em JSON",
      "As APIs quase sempre respondem em JSON, um texto que parece um dicionário do Python. resposta.json() transforma esse texto em dicionários e listas que você já sabe usar. Por baixo, é o mesmo que json.loads(resposta.text). Aqui criamos uma resposta de mentirinha para treinar.",
      'import json\n\nclass RespostaFalsa:\n    status_code = 200\n    text = \'{"cidade": "Recife", "temp": 31, "chuva": false}\'\n    def json(self):\n        return json.loads(self.text)\n\nr = RespostaFalsa()\ndados = r.json()\nprint(dados["cidade"], dados["temp"])\nprint(dados["chuva"])',
      [OUT('import json\n\ntexto = \'{"nome": "Rex", "idade": 3}\'\ndados = json.loads(texto)\nprint(dados["idade"] + 1)',
           ["31", "Rex", "\"3\"1"],
           "json.loads transforma o 3 do texto num número de verdade. 3 + 1 dá 4."),
       TYPE('import json\n\nclass RespostaFalsa:\n    text = \'{"piadas": ["A", "B", "C"]}\'\n    def json(self):\n        return json.loads(self.text)\n\nr = RespostaFalsa()\nprint(len(r.json()["piadas"]))',
            "r.json() dá um dicionário; a chave piadas guarda uma lista com 3 itens."),
       MC("O que resposta.json() devolve?",
          "Dicionários e listas do Python, prontos para usar",
          ["Um texto que você ainda precisa recortar", "Um arquivo .json salvo no computador", "O status_code da resposta"],
          "O texto JSON vira estruturas do Python: você acessa com dados[\"chave\"]."),
       ORDER("Monte o programa que lê o JSON e mostra cada pet, um por linha.",
             ['import json',
              'texto = \'{"pets": ["Rex", "Mia"]}\'',
              'dados = json.loads(texto)',
              'for pet in dados["pets"]:',
              '    print(pet)'],
             "Primeiro o import, depois o texto, a conversão e só então o laço.")]),
    # lição 4
    L("Enviando dados: POST",
      "GET busca dados; POST envia dados, como num cadastro ou num pedido de pizza. Com requests.post(url, json=dados) o dicionário vira JSON e segue no corpo do pedido. headers são informações extras, como a chave da sua conta em Authorization. Aqui montamos o pedido sem enviar para ver como ele fica.",
      'import requests\n\npet = {"nome": "Rex", "idade": 3}\npedido = requests.Request("POST", "https://api.exemplo.com/pets", json=pet,\n                          headers={"Authorization": "Bearer minha-chave"}).prepare()\nprint(pedido.method)\nprint(pedido.body.decode())\nprint(pedido.headers["Content-Type"])\nprint(pedido.headers["Authorization"])',
      [OUT('import requests\n\np = requests.Request("POST", "https://api.exemplo.com/pedidos", json={"pizza": "calabresa"}).prepare()\nprint(p.method)',
           ["GET", "JSON", "pedidos"],
           "O método é o que você escolheu: POST, para enviar dados."),
       MC("Você quer CADASTRAR um novo usuário numa API. Qual método costuma usar?",
          "POST, enviando os dados com json=",
          ["GET, colocando a senha em params", "GET, sem nada", "status_code"],
          "GET é para buscar. Para criar ou enviar algo, use POST. E senha na URL fica exposta!"),
       FILL("Complete para enviar o dicionário como JSON.",
            'import requests\n\ndados = {"nome": "Bia", "nota": 9}\np = requests.Request("POST", "https://api.exemplo.com/notas", ___=dados).prepare()\nprint(p.body.decode())',
            "json", ["body", "dict", "texto"],
            "json= transforma o dicionário em texto JSON e já avisa o servidor."),
       TYPE('import requests\n\np = requests.Request("POST", "https://api.exemplo.com/pets", json={"nome": "Mia"}).prepare()\nprint(p.headers["Content-Type"])',
            "Com json=, a requests avisa no cabeçalho Content-Type que o corpo é JSON.")]),
    # lição 5
    L("Tempo limite e erros",
      "A internet falha: o site cai, demora ou responde 404. Sempre passe timeout=5 (segundos) em requests.get para não esperar para sempre. resposta.raise_for_status() levanta um HTTPError se o status for de erro, e você trata com try/except. requests.RequestException pega qualquer erro da requests (Timeout, ConnectionError, HTTPError...).",
      'import requests\n\n# na vida real: r = requests.get(url, timeout=5)\nr = requests.Response()\nr.status_code = 404\ntry:\n    r.raise_for_status()\n    print("Tudo certo")\nexcept requests.HTTPError as erro:\n    print("Falhou:", type(erro).__name__)\nprint(issubclass(requests.Timeout, requests.RequestException))',
      [OUT('import requests\n\nr = requests.Response()\nr.status_code = 200\nr.raise_for_status()\nprint("seguiu")',
           ["HTTPError", "200", "True"],
           "Com status 200 não há erro, então raise_for_status() não faz nada e o programa segue."),
       TYPE('import requests\n\nr = requests.Response()\nr.status_code = 500\ntry:\n    r.raise_for_status()\nexcept requests.RequestException as e:\n    print(type(e).__name__)',
            "Status 500 é erro do servidor: raise_for_status levanta HTTPError."),
       MC("Para que serve timeout=5 em requests.get(url, timeout=5)?",
          "Desistir depois de 5 segundos se o servidor não responder",
          ["Repetir o pedido 5 vezes", "Esperar 5 segundos antes de pedir", "Baixar só 5 resultados"],
          "Sem timeout, um servidor travado deixa seu programa esperando para sempre."),
       ORDER("Monte o programa que avisa o usuário quando o servidor está fora do ar.",
             ['import requests',
              'r = requests.Response()',
              'r.status_code = 503',
              'try:',
              '    r.raise_for_status()',
              'except requests.RequestException:',
              '    print("Tente de novo mais tarde")'],
             "Cria a resposta, define o status e testa dentro do try; o except trata o erro.")]),
    # lição 6
    L("Desafio: app do clima",
      "Juntando tudo: montar a URL com params, conferir se deu certo com ok e ler o JSON. A função abaixo recebe uma resposta (de mentirinha) e devolve uma frase pronta para mostrar no app.",
      'import json\nimport requests\n\nclass RespostaFalsa:\n    def __init__(self, status, texto):\n        self.status_code = status\n        self.ok = status < 400\n        self.text = texto\n    def json(self):\n        return json.loads(self.text)\n\ndef resumo_clima(r):\n    if not r.ok:\n        return f"Erro {r.status_code}"\n    d = r.json()\n    return f"{d[\'cidade\']}: {d[\'temp\']}°C"\n\nurl = requests.Request("GET", "https://api.exemplo.com/clima", params={"cidade": "Recife"}).prepare().url\nprint(url)\nprint(resumo_clima(RespostaFalsa(200, \'{"cidade": "Recife", "temp": 31}\')))\nprint(resumo_clima(RespostaFalsa(404, "")))',
      [OUT('import json\n\nclass RespostaFalsa:\n    def __init__(self, status, texto):\n        self.status_code = status\n        self.ok = status < 400\n        self.text = texto\n    def json(self):\n        return json.loads(self.text)\n\ndef resumo(r):\n    if not r.ok:\n        return f"Erro {r.status_code}"\n    return r.json()["cidade"]\n\nprint(resumo(RespostaFalsa(500, "")))',
           ["Recife", "Erro 404", "JSONDecodeError"],
           "500 não é ok, então a função devolve a mensagem de erro antes de tentar ler o JSON."),
       MC("Por que conferir r.ok ANTES de chamar r.json()?",
          "Se deu erro, a resposta pode nem ter o JSON esperado",
          ["Porque r.json() apaga o status_code", "Porque r.ok deixa o JSON mais rápido", "Não precisa, r.json() nunca falha"],
          "Uma página de erro costuma vir vazia ou em HTML. Ler como JSON daria erro."),
       FILL("Complete para tratar a resposta só quando deu certo.",
            'import requests\n\nr = requests.Response()\nr.status_code = 201\nif r.___:\n    print("Cadastro feito!")',
            "ok", ["json", "erro", "text"],
            "r.ok é True para códigos menores que 400, como 200 e 201."),
       TYPE('import json\n\ntexto = \'{"cidade": "Natal", "dias": [30, 31, 29]}\'\nd = json.loads(texto)\nprint(f"{d[\'cidade\']}: máxima {max(d[\'dias\'])}°C")',
            "max pega o maior valor da lista dias: 31.")]),
]

BUGS = r'''
@lib_requests 1
import request

p = requests.Request("GET", "https://api.exemplo.com/pets").prepare()
print(p.method)
>>> import requests
!! O nome da biblioteca é requests, com s no final.

@lib_requests 6
import requests

r = requests.Response()
r.status_code = 200

if r.status_code = 200:
    print("Deu certo!")
>>> if r.status_code == 200:
!! Para comparar use ==. Um = só serve para guardar valor.

@lib_requests 5
import requests

r = requests.Response()
r.status_code = 200
if r.status_code == "200":
    print("ok")
else:
    print("erro")  # esperado: ok
>>> if r.status_code == 200:
!! status_code é um número. 200 e "200" são coisas diferentes.

@lib_requests 9
import json

class RespostaFalsa:
    text = '{"temp": 28}'
    def json(self):
        return json.loads(self.text)

r = RespostaFalsa()
dados = r.json
print(dados["temp"])
>>> dados = r.json()
!! json é um método: faltaram os parênteses para chamar.

@lib_requests 4
import json

dados = json.loads('{"cidade": "Recife", "temp": 31}')
print(dados["Cidade"])
>>> print(dados["cidade"])
!! As chaves do JSON diferenciam maiúsculas: a chave é "cidade".

@lib_requests 3
import json

texto = "{'nome': 'Rex'}"
print(json.loads(texto)["nome"])
>>> texto = '{"nome": "Rex"}'
!! No JSON os textos usam aspas duplas. Aspas simples dão JSONDecodeError.

@lib_requests 3
import requests

p = requests.Request("GET", "https://api.exemplo.com/busca", param={"q": "bolo"}).prepare()
print(p.url)
>>> p = requests.Request("GET", "https://api.exemplo.com/busca", params={"q": "bolo"}).prepare()
!! O nome do parâmetro é params, no plural.
'''
