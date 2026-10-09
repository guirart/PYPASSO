from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_pathlib", titulo="os e pathlib",
               descricao="Pastas e arquivos: criar, listar, conferir, apagar e organizar.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Caminhos com Path",
      "O módulo pathlib ajuda seu programa a mexer com pastas e arquivos do computador. Ele já vem com o Python: é só escrever from pathlib import Path. Um Path é um caminho, e a barra / junta pedaços dele; depois você pega partes com .name (nome completo), .stem (nome sem extensão), .suffix (extensão) e .parent (a pasta de cima).",
      'from pathlib import Path\n\nfoto = Path("ferias") / "praia.jpg"\nprint(foto)\nprint(foto.name)\nprint(foto.stem)\nprint(foto.suffix)\nprint(foto.parent)',
      [OUT('from pathlib import Path\n\np = Path("fotos") / "aniversario.png"\nprint(p.suffix)',
           ["png", "aniversario", "aniversario.png"],
           ".suffix devolve a extensão COM o ponto: .png."),
       TYPE('from pathlib import Path\n\nprint(Path("musicas/rock/hino.mp3").stem)',
            ".stem é o nome do arquivo sem a pasta e sem a extensão."),
       MC('O que a barra / faz em Path("docs") / "contrato.pdf"?',
          "Junta os pedaços num caminho só: docs/contrato.pdf",
          ["Divide um número pelo outro", "Dá erro, pois não dá para dividir texto", "Cria a pasta docs no computador"],
          "Com Path, a barra é o jeito de juntar pastas e arquivos. Ela só monta o caminho; não cria nada."),
       FILL("Complete para mostrar a pasta onde o arquivo está: docs",
            'from pathlib import Path\n\narq = Path("docs/contrato.pdf")\nprint(arq.___)',
            "parent", ["name", "stem", "suffix"],
            ".parent é a pasta de cima. .name daria contrato.pdf.")]),
    # lição 2
    L("Criando pastas e arquivos",
      "pasta.mkdir() cria uma pasta. Com exist_ok=True ele não reclama se a pasta já existe, e com parents=True cria também as pastas do meio. Para arquivos de texto, write_text grava (substituindo o que havia) e read_text lê tudo de volta. Ótimo para salvar anotações, listas e configurações.",
      'from pathlib import Path\n\npasta = Path("receitas/doces")\npasta.mkdir(parents=True, exist_ok=True)\narq = pasta / "bolo.txt"\narq.write_text("3 ovos\\n2 xícaras de farinha", encoding="utf-8")\nprint(arq.read_text(encoding="utf-8"))',
      [OUT('from pathlib import Path\n\na = Path("recado.txt")\na.write_text("Olá", encoding="utf-8")\na.write_text("Tchau", encoding="utf-8")\nprint(a.read_text(encoding="utf-8"))',
           ["OláTchau", "Olá", "Olá\nTchau"],
           "write_text substitui o conteúdo inteiro do arquivo. Sobrou só Tchau."),
       MC('Para que serve parents=True em Path("2026/janeiro").mkdir(parents=True)?',
          "Cria também a pasta 2026, se ela ainda não existir",
          ["Cria a pasta dentro da pasta do usuário", "Evita erro se janeiro já existir", "Apaga as pastas antigas antes"],
          "Sem parents=True, criar 2026/janeiro dá erro se 2026 ainda não existe. Quem evita erro de pasta existente é exist_ok=True."),
       FILL("Complete para o programa poder rodar duas vezes sem erro.",
            'from pathlib import Path\n\nfor vez in range(2):\n    Path("backup").mkdir(___=True)',
            "exist_ok", ["parents", "force", "replace"],
            "exist_ok=True diz: se a pasta já existe, tudo bem, siga em frente."),
       CODE('Crie a pasta diario e, dentro dela, o arquivo dia1.txt com o texto Hoje aprendi pathlib. Depois mostre o conteúdo do arquivo com print.',
            'from pathlib import Path\n\n# crie a pasta, grave o arquivo e mostre o conteúdo\n',
            'from pathlib import Path\n\npasta = Path("diario")\npasta.mkdir(exist_ok=True)\narq = pasta / "dia1.txt"\narq.write_text("Hoje aprendi pathlib", encoding="utf-8")\nprint(arq.read_text(encoding="utf-8"))',
            'from pathlib import Path as _P\nassert _P("diario").is_dir(), "Crie a pasta diario"\nassert _P("diario/dia1.txt").is_file(), "Crie o arquivo dia1.txt dentro de diario"\nassert _P("diario/dia1.txt").read_text(encoding="utf-8") == "Hoje aprendi pathlib", "O arquivo deve conter: Hoje aprendi pathlib"\nassert __stdout__.strip() == "Hoje aprendi pathlib", "Mostre o conteúdo do arquivo com print"',
            'Use mkdir(exist_ok=True), depois write_text e read_text com encoding="utf-8".')]),
    # lição 3
    L("Listando: iterdir e glob",
      "pasta.iterdir() percorre tudo o que está dentro da pasta. pasta.glob(\"*.jpg\") pega só o que combina com o padrão (o * vale qualquer nome), e rglob faz o mesmo procurando também nas subpastas. A ordem pode variar de computador para computador, por isso use sorted para listar.",
      'from pathlib import Path\n\nfotos = Path("fotos")\nfotos.mkdir()\nfor nome in ["gato.jpg", "cachorro.jpg", "lista.txt"]:\n    (fotos / nome).write_text("", encoding="utf-8")\n\nfor item in sorted(fotos.iterdir()):\n    print(item.name)\nprint("Só fotos:", sorted(p.name for p in fotos.glob("*.jpg")))',
      [OUT('from pathlib import Path\n\np = Path("docs")\np.mkdir()\nfor nome in ["a.txt", "b.csv", "c.txt"]:\n    (p / nome).write_text("", encoding="utf-8")\nprint(len(list(p.glob("*.txt"))))',
           ["3", "1", "0"],
           "O padrão *.txt pega só os arquivos que terminam em .txt: a.txt e c.txt."),
       TYPE('from pathlib import Path\n\np = Path("jogo")\np.mkdir()\n(p / "save2.dat").write_text("", encoding="utf-8")\n(p / "save1.dat").write_text("", encoding="utf-8")\nprint(sorted(x.name for x in p.iterdir()))',
            "sorted devolve uma lista em ordem alfabética dos nomes."),
       MC("Qual a diferença entre glob(\"*.mp3\") e rglob(\"*.mp3\")?",
          "rglob procura também dentro das subpastas",
          ["rglob só acha o primeiro arquivo", "glob apaga os arquivos encontrados", "Nenhuma, são a mesma coisa"],
          "O r vem de recursivo: rglob entra em todas as subpastas."),
       CODE("Mostre, um por linha e em ordem alfabética, só o NOME dos arquivos .txt da pasta notas (sem o caminho).",
            'from pathlib import Path\n\nnotas = Path("notas")\nnotas.mkdir(exist_ok=True)\nfor nome in ["prova.txt", "aula.txt", "foto.png", "resumo.txt"]:\n    (notas / nome).write_text("", encoding="utf-8")\n\n# mostre os nomes dos .txt aqui\n',
            'from pathlib import Path\n\nnotas = Path("notas")\nnotas.mkdir(exist_ok=True)\nfor nome in ["prova.txt", "aula.txt", "foto.png", "resumo.txt"]:\n    (notas / nome).write_text("", encoding="utf-8")\n\nfor arq in sorted(notas.glob("*.txt")):\n    print(arq.name)',
            'linhas = __stdout__.strip().splitlines()\nassert linhas == ["aula.txt", "prova.txt", "resumo.txt"], "Esperado: aula.txt, prova.txt e resumo.txt, um por linha, em ordem"',
            'for arq in sorted(notas.glob("*.txt")): print(arq.name)')]),
    # lição 4
    L("Conferir e apagar",
      "Antes de ler ou apagar, confira: exists() diz se o caminho existe, is_file() se é um arquivo e is_dir() se é uma pasta. Para apagar um arquivo use unlink(); com missing_ok=True ele não dá erro se o arquivo já sumiu. Pastas vazias se apagam com rmdir().",
      'from pathlib import Path\n\nlista = Path("compras.txt")\nprint(lista.exists())\nlista.write_text("pão, leite", encoding="utf-8")\nprint(lista.exists(), lista.is_file(), lista.is_dir())\nlista.unlink()\nprint(lista.exists())',
      [OUT('from pathlib import Path\n\nPath("musicas").mkdir()\nprint(Path("musicas").is_file(), Path("musicas").is_dir())',
           ["True False", "True True", "False False"],
           "musicas é uma pasta: is_file() dá False e is_dir() dá True."),
       TYPE('from pathlib import Path\n\np = Path("rascunho.txt")\np.write_text("ideia", encoding="utf-8")\np.unlink()\nprint(p.exists())',
            "Depois do unlink() o arquivo não existe mais."),
       MC("O que acontece com Path(\"fantasma.txt\").unlink() se o arquivo não existe?",
          "Dá FileNotFoundError",
          ["Nada, ele ignora", "Cria o arquivo e apaga em seguida", "Apaga a pasta inteira"],
          "Sem missing_ok=True, apagar algo que não existe dá FileNotFoundError."),
       ORDER("Monte o programa que cria config.txt só se ele ainda não existir e depois mostra o conteúdo.",
             ['from pathlib import Path',
              'config = Path("config.txt")',
              'if not config.exists():',
              '    config.write_text("tema=escuro", encoding="utf-8")',
              'print(config.read_text(encoding="utf-8"))'],
             "Primeiro o import, depois o caminho, a conferência com exists() e por fim a leitura.")]),
    # lição 5
    L("O módulo os",
      "O módulo os é mais antigo e você vai vê-lo em muito código por aí. os.getcwd() diz em que pasta o programa está rodando, os.path.join junta caminhos (como a / do Path) e os.environ.get lê variáveis de ambiente, com um valor padrão se ela não existir, muito usado para guardar senhas e chaves fora do código.",
      'import os\nfrom pathlib import Path\n\nprint(os.path.join("fotos", "praia.jpg"))\nprint(Path("fotos") / "praia.jpg")\nprint(os.environ.get("PYPASSO_TEMA", "claro"))\nos.makedirs("a/b", exist_ok=True)\nprint(sorted(os.listdir(".")))',
      [OUT('import os\n\nprint(os.path.join("casa", "quarto", "foto.png"))',
           ["casaquartofoto.png", "casa quarto foto.png", "('casa', 'quarto', 'foto.png')"],
           "os.path.join coloca a barra de pasta entre os pedaços."),
       MC("O que os.getcwd() devolve?",
          "O caminho da pasta onde o programa está rodando agora",
          ["A lista de arquivos da pasta", "O nome do arquivo .py", "A pasta onde o Python foi instalado"],
          "cwd quer dizer current working directory: a pasta de trabalho atual. É dela que partem caminhos como \"notas.txt\"."),
       FILL("Complete para que as duas linhas mostrem o mesmo caminho.",
            'import os\nfrom pathlib import Path\n\nprint(os.path.join("loja", "precos.csv"))\nprint(Path("loja") ___ "precos.csv")',
            "/", ["+", ",", "&"],
            "No pathlib, a barra / faz o papel do os.path.join."),
       CODE('Leia a variável de ambiente IDIOMA_APP usando "pt" como padrão (ela não existe aqui) e mostre: Idioma: pt',
            'import os\n\nidioma = os.environ["IDIOMA_APP"]\nprint(f"Idioma: {idioma}")\n',
            'import os\n\nidioma = os.environ.get("IDIOMA_APP", "pt")\nprint(f"Idioma: {idioma}")',
            'assert __stdout__.strip() == "Idioma: pt", "A saída deve ser: Idioma: pt"',
            'os.environ["X"] dá KeyError se X não existe; os.environ.get("IDIOMA_APP", "pt") devolve o padrão.')]),
    # lição 6
    L("Desafio: organizar por extensão",
      "Juntando tudo: listar arquivos, ler a extensão com .suffix, criar pastas com mkdir e mover com rename. Assim você arruma uma pasta de Downloads bagunçada em segundos.",
      'from pathlib import Path\n\nbagunca = Path("downloads")\nbagunca.mkdir()\nfor nome in ["foto.jpg", "nota.txt", "selfie.jpg"]:\n    (bagunca / nome).write_text("", encoding="utf-8")\n\nfor arq in sorted(bagunca.iterdir()):\n    destino = Path("organizado") / arq.suffix[1:]\n    destino.mkdir(parents=True, exist_ok=True)\n    arq.rename(destino / arq.name)\n\nfor p in sorted(Path("organizado").rglob("*")):\n    if p.is_file():\n        print(p)',
      [OUT('from pathlib import Path\n\nprint(Path("relatorio.final.pdf").suffix)',
           [".final.pdf", ".final", "pdf"],
           ".suffix pega só a última extensão: .pdf."),
       MC('Para o arquivo foto.jpg, o que vale arq.suffix[1:]?',
          "jpg",
          [".jpg", "foto", "j"],
          "suffix é .jpg e [1:] corta o primeiro caractere, o ponto. Fica um bom nome de pasta."),
       ORDER("Monte o programa que garante a pasta origem e move cada arquivo dela para uma pasta com o nome da extensão.",
             ['from pathlib import Path',
              'Path("origem").mkdir(exist_ok=True)',
              'for arq in sorted(Path("origem").iterdir()):',
              '    pasta = Path("por_tipo") / arq.suffix[1:]',
              '    pasta.mkdir(parents=True, exist_ok=True)',
              '    arq.rename(pasta / arq.name)'],
             "Para cada arquivo: descobre a pasta, cria a pasta e só então move o arquivo."),
       CODE('Crie a função contar_por_extensao(pasta) que devolve um dicionário com quantos arquivos há de cada extensão. Ex.: {".txt": 2, ".jpg": 1}',
            'from pathlib import Path\n\ndef contar_por_extensao(pasta):\n    contagem = {}\n    return contagem\n',
            'from pathlib import Path\n\ndef contar_por_extensao(pasta):\n    contagem = {}\n    for arq in pasta.iterdir():\n        if arq.is_file():\n            contagem[arq.suffix] = contagem.get(arq.suffix, 0) + 1\n    return contagem\n',
            'from pathlib import Path as _P\n_p = _P("teste_contagem")\n_p.mkdir(exist_ok=True)\nfor _n in ["a.txt", "b.txt", "c.jpg"]:\n    (_p / _n).write_text("", encoding="utf-8")\nassert contar_por_extensao(_p) == {".txt": 2, ".jpg": 1}, "Para a.txt, b.txt e c.jpg o resultado deve ser {\'.txt\': 2, \'.jpg\': 1}"\n_v = _P("vazia_contagem")\n_v.mkdir(exist_ok=True)\nassert contar_por_extensao(_v) == {}, "Uma pasta vazia deve dar {}"',
            'Percorra pasta.iterdir() e some 1 em contagem[arq.suffix] com contagem.get(arq.suffix, 0) + 1.')]),
]

BUGS = r'''
@lib_pathlib 3
from pathlib import Path

foto = Path("fotos") + "praia.jpg"
print(foto.name)
>>> foto = Path("fotos") / "praia.jpg"
!! Com Path, os pedaços do caminho se juntam com /, não com +.

@lib_pathlib 3
from pathlib import Path

Path("2026/janeiro").mkdir(exist_ok=True)
print(Path("2026/janeiro").is_dir())
>>> Path("2026/janeiro").mkdir(parents=True, exist_ok=True)
!! A pasta 2026 ainda não existe. parents=True cria as pastas do meio.

@lib_pathlib 4
from pathlib import Path

musica = Path("hino.mp3")
print(musica.suffix == "mp3")  # esperado: True
>>> print(musica.suffix == ".mp3")  # esperado: True
!! .suffix vem com o ponto: ".mp3".

@lib_pathlib 3
from pathlib import Path

print(Path("bolo.txt").name)  # esperado: bolo
>>> print(Path("bolo.txt").stem)  # esperado: bolo
!! .name traz a extensão junto. O nome sem extensão é .stem.

@lib_pathlib 5
from pathlib import Path

pasta = Path("jogos")
pasta.mkdir()
for arq in pasta.iterdir:
    print(arq.name)
print("fim")
>>> for arq in pasta.iterdir():
!! iterdir é um método: faltaram os parênteses.

@lib_pathlib 4
from pathlib import Path

temp = Path("temporario.txt")
temp.unlink()
print("limpo")
>>> temp.unlink(missing_ok=True)
!! O arquivo não existe. missing_ok=True evita o FileNotFoundError.

@lib_pathlib 3
import os

tema = os.environ["TEMA_DO_APP"]
print(tema)
>>> tema = os.environ.get("TEMA_DO_APP", "claro")
!! A variável não existe, então os.environ[...] dá KeyError. Use .get com um padrão.
'''
