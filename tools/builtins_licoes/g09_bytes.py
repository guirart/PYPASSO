from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    # ================================================================== bytes
    "bytes": [
        # lição 2 (a lição 1 já mostrou encode/decode e bytes([...]))
        L("Jeitos de criar bytes",
          'Além de encode, dá para escrever bytes direto com um b antes das aspas, criar n bytes zerados com bytes(n), passar um texto com a codificação, bytes("oi", "utf-8"), ou ler números hexadecimais com bytes.fromhex.',
          'print(b"Oi")\nprint(bytes(3))\nprint(bytes("pé", "utf-8"))\nprint(bytes.fromhex("4f 69"))',
          [OUT('print(bytes(2))', ["b'2'", "b'\\x02'", "b''"], "bytes(2) cria 2 bytes com valor zero, mostrados como \\x00."),
           TYPE('print(list(b"Py"))', "list mostra o número de cada byte: P é 80 e y é 121."),
           MC('O que acontece com bytes("oi"), sem dizer a codificação?', "Dá TypeError", ["Vira b'oi'", "Vira bytes vazio", "Vira [111, 105]"], 'Para transformar texto, bytes precisa da codificação: bytes("oi", "utf-8").'),
           FILL("Complete para transformar o texto em bytes.", 'b = bytes("café", ___)\nprint(len(b))', '"utf-8"', ['"bytes"', '4', 'utf-8'], 'A codificação vai como texto, entre aspas: "utf-8".'),
           OUT('print(bytes.fromhex("41 42 43"))', ["b'414243'", "[65, 66, 67]", "b'41 42 43'"], "41, 42 e 43 em hexadecimal são 65, 66 e 67: as letras A, B e C.")]),
        # lição 3
        L("Índices, fatias e busca",
          "Um índice em bytes devolve um número: o valor daquele byte. Já uma fatia devolve bytes. Também funcionam in, startswith, count e find, desde que você procure bytes (com b na frente).",
          'arquivo = b"PNG...imagem"\nprint(arquivo[0])\nprint(arquivo[0:3])\nprint(arquivo.startswith(b"PNG"))\nprint(b"ima" in arquivo)',
          [OUT('b = b"pato"\nprint(b[1])', ["a", "b'a'", "112"], "O índice devolve o número do byte: a é 97."),
           OUT('b = b"pato"\nprint(b[1:3])', ["at", "[97, 116]", "b'pat'"], "A fatia continua sendo bytes, por isso aparece o b'...'."),
           TYPE('print(b"banana".count(b"a"))', "Há três bytes a em banana."),
           CODE('Crie a função eh_png(dados) que devolve True se os bytes começam com b"PNG" e False se não.',
                "def eh_png(dados):\n    pass\n",
                'def eh_png(dados):\n    return dados.startswith(b"PNG")',
                'assert eh_png(b"PNG1234") is True, "eh_png(b\\"PNG1234\\") deve ser True"\nassert eh_png(b"GIF89a") is False, "eh_png(b\\"GIF89a\\") deve ser False"\nassert eh_png(b"xPNG") is False, "Só vale se COMEÇAR com PNG"',
                'return dados.startswith(b"PNG")')]),
        # lição 4
        L("Cuidados com bytes",
          'Bytes não mudam: dados[0] = 65 dá TypeError. Cada byte vai de 0 a 255; fora disso, ValueError. E bytes não se misturam com texto: b"a" + "b" dá erro e b"a" == "a" é False.',
          'dados = b"abc"\ntry:\n    dados[0] = 65\nexcept TypeError as e:\n    print("Erro:", type(e).__name__)\nprint(b"a" == "a")\nprint(b"a" + "b".encode())',
          [OUT('try:\n    bytes([10, 300])\n    print("ok")\nexcept ValueError:\n    print("fora da faixa")', ["ok", "b'\\n,'", "[10, 300]"], "300 passa de 255, o maior valor de um byte."),
           OUT('print(b"oi" == "oi")', ["True", "Erro", "b'oi'"], "Bytes e texto são tipos diferentes: nunca são iguais."),
           MC("Qual destas linhas dá erro?", 'b"total: " + "10"', ['b"total: " + b"10"', '"total: " + "10"', 'b"total: " + "10".encode()'], "Não dá para somar bytes com str. Transforme o texto com encode antes."),
           MC('Por que b"olá" dá SyntaxError?', "Bytes escritos com b só aceitam caracteres ASCII", ["Porque falta o encode", "Porque olá tem 3 letras", "Porque b só aceita números"], 'Para acentos, use "olá".encode("utf-8").'),
           FILL("Complete para voltar dos bytes para o texto.", 'texto = b"ol\\xc3\\xa1".___("utf-8")\nprint(texto)', "decode", ["encode", "bytes", "str"], "decode vai de bytes para texto; encode faz o caminho contrário.")]),
        # lição 5
        L("Bytes com outras funções",
          "Bytes combinam com funções que você já conhece: list mostra os números, sum e max fazem contas e len conta bytes. Métodos como split, join e upper também existem, só que trabalham com bytes.",
          'pacote = b"id=7;nome=Bia"\nprint(pacote.split(b";"))\nprint(max(b"abc"))\nprint(b"-".join([b"a", b"b", b"c"]))\nprint(pacote.upper())',
          [TYPE('print(sum(b"\\x01\\x02\\x03"))', "Os bytes valem 1, 2 e 3; a soma é 6."),
           OUT('print(b", ".join([b"sim", b"nao"]))', ["sim, nao", "b'sim', b'nao'", "[b'sim', b'nao']"], "join cola os pedaços e o resultado continua sendo bytes."),
           OUT('print(sorted(b"cab"))', ["b'abc'", "['a', 'b', 'c']", "b'cab'"], "sorted devolve uma lista com os números dos bytes em ordem."),
           ORDER("Monte o programa que mostra quantos bytes o texto ocupa em UTF-8.", ['texto = "maçã"', 'dados = texto.encode("utf-8")', 'print(len(dados))'], "Primeiro o texto, depois o encode, por fim o len dos bytes: 6.")]),
        # lição 6
        L("Desafio: soma de verificação",
          "Um checksum é um número calculado a partir dos bytes para conferir se uma mensagem chegou inteira. Um jeito simples: somar todos os bytes e pegar o resto da divisão por 256.",
          'msg = "Oi!".encode("utf-8")\nprint(list(msg))\nprint(sum(msg) % 256)',
          [TYPE('print(sum(b"AB") % 256)', "65 + 66 = 131, que já é menor que 256."),
           MC("Por que usar % 256 no checksum?", "Para o resultado caber em um byte (0 a 255)", ["Para deixar o número negativo", "Porque sum só aceita 256", "Para transformar em texto"], "O resto da divisão por 256 sempre fica entre 0 e 255."),
           CODE("Crie a função checksum(texto) que transforma o texto em bytes UTF-8, soma todos e devolve o resto da divisão por 256.",
                "def checksum(texto):\n    # transforme em bytes, some e use % 256\n    pass\n",
                'def checksum(texto):\n    return sum(texto.encode("utf-8")) % 256',
                'assert checksum("Oi!") == 217, "checksum(\\"Oi!\\") deve ser 217"\nassert checksum("") == 0, "Texto vazio deve dar 0"\nassert checksum("é") == 108, "Lembre do encode: é vira 2 bytes e o resultado é 108"',
                'return sum(texto.encode("utf-8")) % 256'),
           CODE("Crie a função so_ascii(texto) que devolve True se TODOS os bytes do texto em UTF-8 forem menores que 128.",
                "def so_ascii(texto):\n    pass\n",
                'def so_ascii(texto):\n    for b in texto.encode("utf-8"):\n        if b >= 128:\n            return False\n    return True',
                'assert so_ascii("gato") is True, "gato só tem letras ASCII"\nassert so_ascii("pão") is False, "ã ocupa bytes maiores que 127"\nassert so_ascii("") is True, "Texto vazio não tem nenhum byte proibido"',
                "Percorra os bytes do encode e devolva False no primeiro que for 128 ou mais.")]),
    ],
    # ================================================================== bytearray
    "bytearray": [
        # lição 2 (a lição 1 mostrou que bytearray muda: troca e append)
        L("Criando e convertendo",
          'bytearray aceita as mesmas entradas que bytes: um número (bytes zerados), uma lista de números, bytes ou texto com codificação. Para ter de volta bytes que não mudam, use bytes(ba).',
          'print(bytearray(2))\nprint(bytearray([72, 105]))\nba = bytearray("pão", "utf-8")\nprint(len(ba))\nprint(bytes(ba))',
          [OUT('print(bytearray(b"ok"))', ["b'ok'", "ok", "[111, 107]"], "O print mostra o tipo junto: bytearray(b'ok')."),
           TYPE('print(len(bytearray("ação", "utf-8")))', "ç e ã ocupam 2 bytes cada; a e o, 1 cada: 6."),
           MC("Como transformar o bytearray ba em bytes que não mudam?", "bytes(ba)", ["ba.freeze()", "str(ba)", "tuple(ba)"], "bytes(ba) faz uma cópia imutável."),
           FILL("Complete para criar 4 bytes zerados.", 'buffer = bytearray(___)\nprint(len(buffer))', "4", ["[4]", '"4"', 'b"4"'], "bytearray(4) cria 4 bytes zerados; [4] criaria um byte só, de valor 4.")]),
        # lição 3
        L("Mexendo como numa lista",
          "bytearray tem métodos de lista: append põe um byte no fim, extend põe vários, insert põe numa posição, pop tira o último e del apaga. Sempre com números de 0 a 255 (ou bytes, no extend).",
          'ba = bytearray(b"ola")\nba.append(33)\nba.extend(b"!!")\nba.insert(0, ord(">"))\nprint(ba.decode())\nba.pop()\ndel ba[0]\nprint(ba.decode())',
          [TYPE('ba = bytearray(b"abc")\nba.append(100)\nprint(ba.decode())', "100 é o byte da letra d."),
           OUT('ba = bytearray(b"pato")\nba.pop()\nprint(ba.decode())', ["pato", "ato", "o"], "pop tira o último byte."),
           OUT('ba = bytearray(b"ab")\nba.extend(b"cd")\nprint(len(ba))', ["3", "2", "Erro"], "extend adiciona os dois bytes de b\"cd\"."),
           CODE('Crie a função adicionar_ponto(ba) que coloca um ponto final (.) no fim do próprio bytearray ba.',
                "def adicionar_ponto(ba):\n    pass\n",
                'def adicionar_ponto(ba):\n    ba.append(ord("."))',
                'x = bytearray(b"Oi")\nadicionar_ponto(x)\nassert x == bytearray(b"Oi."), "Depois da função, x deve ser bytearray(b\\"Oi.\\")"',
                'ba.append(ord(".")) muda o próprio bytearray, sem precisar de return.')]),
        # lição 4
        L("Pegadinhas do bytearray",
          'append recebe UM número, não texto: ba.append("!") dá TypeError. ba[0] = b"x" também dá erro; use ord("x"). E como muda, bytearray não tem hash: não pode ser chave de dicionário.',
          'ba = bytearray(b"oi")\ntry:\n    ba.append("!")\nexcept TypeError as e:\n    print("append:", type(e).__name__)\nba.append(ord("!"))\nprint(ba.decode())\nprint(bytearray(b"oi!") == b"oi!")',
          [MC("Qual linha adiciona a letra A no fim de ba?", "ba.append(65)", ['ba.append("A")', 'ba.append(b"A")', 'ba + "A"'], "append quer um número de 0 a 255; 65 é o A."),
           OUT('ba = bytearray(b"x")\ntry:\n    ba[0] = 256\nexcept ValueError:\n    print("grande demais")', ["0", "bytearray(b'\\x00')", "x"], "256 passa do limite de um byte."),
           OUT('print(bytearray(b"ab") == b"ab")', ["False", "Erro", "bytearray(b'ab')"], "bytearray e bytes com o mesmo conteúdo são iguais."),
           OUT('try:\n    d = {bytearray(b"k"): 1}\n    print("ok")\nexcept TypeError:\n    print("sem hash")', ["ok", "{b'k': 1}", "1"], "Coisas que mudam não têm hash e não podem ser chave.")]),
        # lição 5
        L("Fatias e transformações",
          'Dá para trocar um pedaço inteiro com fatia: ba[0:2] = b"XY". O pedaço novo pode até ter outro tamanho. reverse() inverte no lugar, e métodos como upper() devolvem um bytearray novo.',
          'ba = bytearray(b"bom dia")\nba[4:7] = b"noite"\nprint(ba.decode())\nba.reverse()\nprint(ba.decode())\nprint(bytearray(b"oi").upper())',
          [TYPE('ba = bytearray(b"gato")\nba[0:2] = b"ra"\nprint(ba.decode())', "Os dois primeiros bytes viram r e a."),
           OUT('ba = bytearray(b"abc")\nba.reverse()\nprint(ba.decode())', ["abc", "None", "cab"], "reverse inverte o próprio bytearray."),
           OUT('ba = bytearray(b"oi")\nba[2:] = b" tudo bem"\nprint(len(ba))', ["2", "9", "Erro"], "A fatia no fim acrescenta 9 bytes aos 2 que já existiam: 11."),
           ORDER('Monte o programa que troca a primeira letra de "lata" por m e mostra o texto.', ['ba = bytearray("lata", "utf-8")', 'ba[0] = ord("m")', 'print(ba.decode())'], "Cria, altera e só depois mostra: mata.")]),
        # lição 6
        L("Desafio: esconder a senha",
          "Como bytearray muda no lugar, ele é ótimo para editar texto byte a byte, como esconder parte de uma senha com asteriscos.",
          'ba = bytearray(b"segredo")\nfor i in range(3):\n    ba[i] = ord("*")\nprint(ba.decode())',
          [OUT('ba = bytearray(b"1234")\nba[0] = ba[-1]\nprint(ba.decode())', ["1234", "1231", "Erro"], "O primeiro byte recebe o valor do último: 4."),
           MC("Por que usar bytearray em vez de bytes para editar?", "Porque bytearray pode ser alterado no lugar", ["Porque bytes não aceita números", "Porque bytearray é mais curto", "Porque bytes não tem len"], "bytes é imutável, como a tupla."),
           CODE("Crie a função mascarar(senha) que devolve um texto com todos os caracteres trocados por *, menos os 2 últimos. Ex.: \"12345678\" vira \"******78\".",
                "def mascarar(senha):\n    ba = bytearray(senha, \"utf-8\")\n    # troque os bytes aqui\n    return senha\n",
                'def mascarar(senha):\n    ba = bytearray(senha, "utf-8")\n    for i in range(len(ba) - 2):\n        ba[i] = ord("*")\n    return ba.decode()',
                'assert mascarar("12345678") == "******78", "mascarar(\\"12345678\\") deve dar ******78"\nassert mascarar("abc") == "*bc", "mascarar(\\"abc\\") deve dar *bc"\nassert mascarar("ok") == "ok", "Com 2 caracteres, nada é escondido"',
                "Troque os bytes de 0 até len(ba) - 2 por ord(\"*\") e devolva ba.decode()."),
           CODE("Crie a função trocar_espacos(ba) que troca, no próprio bytearray, cada espaço (byte 32) por _ (byte 95).",
                "def trocar_espacos(ba):\n    pass\n",
                'def trocar_espacos(ba):\n    for i in range(len(ba)):\n        if ba[i] == 32:\n            ba[i] = 95',
                'x = bytearray(b"bom dia pra voce")\ntrocar_espacos(x)\nassert x == b"bom_dia_pra_voce", "Os espaços devem virar _"\ny = bytearray(b"nada")\ntrocar_espacos(y)\nassert y == b"nada", "Sem espaços, nada muda"',
                "Percorra os índices e troque ba[i] quando ele valer 32.")]),
    ],
    # ================================================================== memoryview
    "memoryview": [
        # lição 2 (a lição 1 mostrou a ideia de janela e uma alteração)
        L("Lendo pela janela",
          "m[i] dá o número do byte, len(m) o tamanho, m.tolist() a lista de números e m.tobytes() uma cópia em bytes. m.readonly diz se dá para alterar. print(m) só mostra o endereço na memória, então converta antes.",
          'm = memoryview(b"Pipo")\nprint(m[0])\nprint(m.tolist())\nprint(m.tobytes())\nprint(m.readonly)',
          [OUT('m = memoryview(b"ab")\nprint(m.tolist())', ["['a', 'b']", "b'ab'", "[97]"], "tolist devolve os números dos bytes."),
           TYPE('m = memoryview(bytearray(b"ok"))\nprint(m.readonly)', "Sobre um bytearray, a janela pode alterar: readonly é False."),
           OUT('m = memoryview(b"pato")\nprint(m[1:3].tobytes())', ["b'pat'", "at", "[97, 116]"], "A fatia pega os bytes 1 e 2; tobytes mostra como bytes."),
           MC("Por que print(m) não mostra o conteúdo da memoryview?", "Ele mostra só onde a janela está na memória", ["Porque a memoryview está vazia", "Porque print não aceita memoryview", "Porque o conteúdo é secreto"], "Use m.tobytes() ou m.tolist() para ver os dados.")]),
        # lição 3
        L("Alterando sem copiar",
          "Com um bytearray por baixo, mudar pela janela muda o original. A fatia de uma memoryview também é janela, não cópia. Já a fatia de um bytearray é uma cópia nova, separada.",
          'dados = bytearray(b"abcdef")\ncopia = dados[0:3]\ncopia[0] = ord("X")\nprint(dados.decode())\njanela = memoryview(dados)[0:3]\njanela[0] = ord("X")\nprint(dados.decode())',
          [OUT('d = bytearray(b"gato")\nm = memoryview(d)\nm[0] = ord("p")\nprint(d.decode())', ["gato", "p", "Erro"], "A janela altera o próprio bytearray."),
           OUT('d = bytearray(b"gato")\nc = d[0:2]\nc[0] = ord("r")\nprint(d.decode())', ["rato", "ra", "Erro"], "A fatia do bytearray é uma cópia; o original não muda."),
           FILL("Complete para que a mudança apareça em dados.", 'dados = bytearray(b"sol")\nparte = ___(dados)[0:1]\nparte[0] = ord("S")\nprint(dados.decode())', "memoryview", ["bytes", "bytearray", "list"], "Só a memoryview olha para os mesmos bytes; as outras fazem cópia."),
           CODE("Crie a função zerar_inicio(dados, n) que, usando memoryview, coloca 0 nos n primeiros bytes do bytearray dados.",
                "def zerar_inicio(dados, n):\n    m = memoryview(dados)\n    # altere pela janela\n",
                'def zerar_inicio(dados, n):\n    m = memoryview(dados)\n    for i in range(n):\n        m[i] = 0',
                'd = bytearray([5, 6, 7, 8])\nzerar_inicio(d, 2)\nassert list(d) == [0, 0, 7, 8], "Os 2 primeiros devem virar 0: [0, 0, 7, 8]"\ne = bytearray([9, 9])\nzerar_inicio(e, 0)\nassert list(e) == [9, 9], "Com n = 0, nada muda"',
                "Percorra range(n) e faça m[i] = 0.")]),
        # lição 4
        L("Cuidados com a janela",
          'memoryview só aceita objetos de bytes: memoryview("texto") dá TypeError. Sobre bytes, a janela é só leitura. Ao trocar uma fatia, o pedaço novo precisa ter o mesmo tamanho. E com a janela aberta, o bytearray não pode crescer: chame release() antes.',
          'dados = bytearray(b"oi")\nm = memoryview(dados)\ntry:\n    dados.append(33)\nexcept BufferError as e:\n    print("Erro:", type(e).__name__)\nm.release()\ndados.append(33)\nprint(dados.decode())',
          [OUT('try:\n    memoryview("oi")\n    print("ok")\nexcept TypeError:\n    print("precisa de bytes")', ["ok", "oi", "b'oi'"], "Texto não é bytes; use \"oi\".encode() antes."),
           OUT('m = memoryview(b"abc")\ntry:\n    m[0] = 65\nexcept TypeError:\n    print("só leitura")\nprint(m.tobytes())', ["b'Abc'", "só leitura\nb'Abc'", "b'abc'"], "Sobre bytes a janela não altera nada: aparece o aviso e os bytes continuam iguais."),
           MC('Com d = bytearray(b"abcd") e m = memoryview(d), o que faz m[0:2] = b"XYZ"?', "Dá ValueError: os tamanhos não batem", ['d vira XYZcd', 'd vira XYcd', 'd vira XYZd'], "A janela não muda de tamanho: 2 posições recebem só 2 bytes."),
           MC("O que fazer antes de dar append num bytearray com uma memoryview aberta?", "Fechar a janela com m.release()", ["Nada, funciona direto", "Apagar o bytearray", "Converter m em lista"], "Enquanto a janela existe, o bytearray não pode mudar de tamanho.")]),
        # lição 5
        L("Janela com outras funções",
          "Uma memoryview funciona com len, sum, max, list e comparações com bytes. Para métodos de texto, como decode, converta antes com bytes(m). Com with memoryview(...) as m, a janela fecha sozinha no fim do bloco.",
          'dados = bytearray([10, 20, 30, 40])\nwith memoryview(dados) as m:\n    print(sum(m[1:3]))\n    print(max(m))\n    print(m == bytes([10, 20, 30, 40]))\ndados.append(50)\nprint(len(dados))',
          [TYPE('m = memoryview(bytes([3, 4, 5]))\nprint(sum(m))', "3 + 4 + 5 = 12."),
           OUT('m = memoryview(b"Oi")\nprint(bytes(m).decode())', ["b'Oi'", "Erro", "[79, 105]"], "bytes(m) copia para bytes, e aí o decode funciona."),
           OUT('m = memoryview(b"abc")\nprint(m[0:2] == b"ab")', ["False", "Erro", "b'ab'"], "A janela pode ser comparada com bytes."),
           ORDER("Monte o programa que mostra o tamanho pela janela e só depois aumenta o bytearray.", ['dados = bytearray(b"abc")', 'with memoryview(dados) as m:', '    print(len(m))', 'dados.append(100)', 'print(dados.decode())'], "O append vem depois do with, quando a janela já fechou.")]),
        # lição 6
        L("Desafio: editor de imagem",
          "Imagens em tons de cinza são bytes: 0 é preto e 255 é branco. Com memoryview você ajusta só um pedaço da imagem, sem copiar tudo.",
          'imagem = bytearray([0, 50, 100, 150, 200, 250])\nlinha = memoryview(imagem)[2:5]\nfor i in range(len(linha)):\n    linha[i] = 255 - linha[i]\nprint(list(imagem))',
          [OUT('img = bytearray([10, 20, 30])\nm = memoryview(img)\nm[1] = 255 - m[1]\nprint(list(img))', ["[10, 20, 30]", "[245, 235, 225]", "[10, 255, 30]"], "Só a posição 1 muda: 255 - 20 = 235."),
           MC("Por que usar memoryview em vez de fatiar o bytearray?", "Para alterar o pedaço sem criar uma cópia", ["Porque a fatia não funciona com números", "Para deixar a imagem só leitura", "Porque memoryview ordena os bytes"], "A fatia copia; a janela altera o original."),
           CODE("Crie a função clarear(img, inicio, fim) que, usando memoryview, soma 10 a cada byte de img entre inicio e fim (fim fora), sem passar de 255.",
                "def clarear(img, inicio, fim):\n    pass\n",
                'def clarear(img, inicio, fim):\n    m = memoryview(img)[inicio:fim]\n    for i in range(len(m)):\n        m[i] = min(m[i] + 10, 255)',
                'img = bytearray([0, 100, 250, 7])\nclarear(img, 1, 3)\nassert list(img) == [0, 110, 255, 7], "Esperado [0, 110, 255, 7]: 250 + 10 para em 255"\nb = bytearray([1, 2])\nclarear(b, 0, 2)\nassert list(b) == [11, 12], "Esperado [11, 12]"',
                "Pegue a janela memoryview(img)[inicio:fim] e use min(m[i] + 10, 255).")]),
    ],
    # ================================================================== hash
    "hash": [
        # lição 2 (a lição 1 mostrou o básico e o erro com lista)
        L("Quem tem hash?",
          "Têm hash os valores imutáveis: int, float, bool, str, bytes, None, frozenset e tuplas (se tudo dentro também tiver hash). Listas, dicionários, sets e bytearray não têm: hash() dá TypeError.",
          'for valor in [7, "oi", (1, 2), None, b"x"]:\n    hash(valor)\nprint("todos têm hash")\nfor valor in [[1], {"a": 1}, {1, 2}]:\n    try:\n        hash(valor)\n    except TypeError:\n        print(type(valor).__name__, "não tem hash")',
          [OUT('print(hash(True))', ["True", "0", "Erro"], "True vale 1, e o hash de um inteiro pequeno é ele mesmo."),
           MC("Qual destes NÃO tem hash?", "[1, 2]", ["(1, 2)", '"12"', "12"], "Listas mudam, por isso não têm hash."),
           OUT('try:\n    hash((1, [2]))\n    print("ok")\nexcept TypeError:\n    print("não tem hash")', ["ok", "(1, [2])", "1"], "A tupla tem uma lista dentro, então não tem hash."),
           TYPE('print(hash(frozenset([1, 2])) == hash(frozenset([2, 1])))', "São o mesmo conjunto, então têm o mesmo hash.")]),
        # lição 3
        L("Hash no dia a dia",
          "Você quase nunca chama hash() direto: dicionários e sets usam o hash por baixo para achar as coisas rápido. Por isso tuplas servem de chave, como coordenadas de um mapa, e listas não.",
          'mapa = {(0, 0): "casa", (2, 3): "tesouro"}\nprint(mapa[(2, 3)])\nvisitados = {(0, 0), (1, 0)}\nprint((1, 0) in visitados)',
          [OUT('notas = {("Ana", 1): 8, ("Ana", 2): 9}\nprint(notas[("Ana", 2)])', ["8", "('Ana', 2)", "Erro"], "A tupla (\"Ana\", 2) é a chave da nota 9."),
           TYPE('vistos = {(1, 2), (3, 4), (1, 2)}\nprint(len(vistos))', "Tuplas iguais têm o mesmo hash, e o set guarda só uma."),
           FILL("Complete para usar a posição como chave.", 'pos = ___\ntabuleiro = {pos: "rei"}\nprint(tabuleiro[(4, 0)])', "(4, 0)", ["[4, 0]", "{4, 0}", '"4, 0"'], "Só a tupla tem hash e é igual à chave procurada."),
           CODE("Crie a função contar_pares(pares) que recebe uma lista de listas como [[1, 2], [1, 2], [3, 4]] e devolve um dicionário com tuplas de chave contando cada par: {(1, 2): 2, (3, 4): 1}.",
                "def contar_pares(pares):\n    contagem = {}\n    # use tuple(par) como chave\n    return contagem\n",
                'def contar_pares(pares):\n    contagem = {}\n    for par in pares:\n        chave = tuple(par)\n        contagem[chave] = contagem.get(chave, 0) + 1\n    return contagem',
                'assert contar_pares([[1, 2], [1, 2], [3, 4]]) == {(1, 2): 2, (3, 4): 1}, "Esperado {(1, 2): 2, (3, 4): 1}"\nassert contar_pares([]) == {}, "Lista vazia deve dar {}"',
                "Lista não pode ser chave; tuple(par) pode.")]),
        # lição 4
        L("Pegadinhas do hash",
          "Valores iguais têm o mesmo hash, por isso 1, 1.0 e True viram a mesma chave. Mas hash igual não garante valor igual: hash(-1) e hash(-2) dão -2! E o hash de textos muda cada vez que o programa roda: nunca guarde esse número.",
          'print(hash(-1), hash(-2))\nd = {1: "um"}\nd[1.0] = "um vírgula zero"\nd[True] = "verdadeiro"\nprint(d)',
          [OUT('d = {1: "a"}\nd[True] = "b"\nprint(d)', ["{1: 'a', True: 'b'}", "{True: 'b'}", "{1: 'a'}"], "True == 1, então é a mesma chave: só o valor muda."),
           TYPE('print(hash(-1) == hash(-2))', "Uma coincidência famosa: os dois dão -2."),
           MC('Por que não guardar hash("senha") num arquivo para conferir depois?', "O hash de textos muda a cada execução", ["hash de texto sempre dá 0", "hash não funciona com textos", "Arquivos não aceitam números"], "O Python sorteia uma semente ao iniciar. Para senhas, use o módulo hashlib."),
           OUT('print(len({1, 1.0, True}))', ["3", "2", "Erro"], "Os três são iguais e têm o mesmo hash: o set guarda um só.")]),
        # lição 5
        L("Hash nas suas classes",
          "Por padrão, cada objeto de uma classe tem hash próprio e só é igual a ele mesmo. Se você criar __eq__, o Python tira o hash (vira None). Para usar em sets e dicts, crie também __hash__, devolvendo o hash de uma tupla com os atributos.",
          'class Ponto:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __eq__(self, outro):\n        return (self.x, self.y) == (outro.x, outro.y)\n    def __hash__(self):\n        return hash((self.x, self.y))\n\npontos = {Ponto(1, 2), Ponto(1, 2), Ponto(3, 4)}\nprint(len(pontos))',
          [OUT('class A:\n    pass\n\nprint(len({A(), A()}))', ["1", "0", "Erro"], "Sem __eq__, cada objeto é diferente dos outros."),
           OUT('class B:\n    def __eq__(self, o):\n        return True\n\nprint(B.__hash__ is None)', ["False", "Erro", "B"], "Criar __eq__ sem __hash__ deixa __hash__ como None."),
           FILL("Complete o __hash__ usando os atributos.", 'class Carta:\n    def __init__(self, valor, naipe):\n        self.valor, self.naipe = valor, naipe\n    def __eq__(self, o):\n        return (self.valor, self.naipe) == (o.valor, o.naipe)\n    def __hash__(self):\n        return ___\n\nprint(len({Carta(7, "ouros"), Carta(7, "ouros")}))', "hash((self.valor, self.naipe))", ["hash([self.valor, self.naipe])", "(self.valor, self.naipe)", "self.valor + self.naipe"], "__hash__ precisa devolver um número; a tupla dos atributos tem hash, a lista não."),
           MC("Se a == b é True, o que também precisa ser verdade?", "hash(a) == hash(b)", ["hash(a) != hash(b)", "hash(a) == 0", "Nada"], "Objetos iguais precisam ter o mesmo hash, senão dicts e sets se perdem.")]),
        # lição 6
        L("Desafio: sem repetidos",
          "Sets usam o hash para descartar repetidos, mas listas dentro de listas não têm hash. O truque: converter cada item para tupla antes de pôr no set.",
          'pedidos = [["café", 2], ["pão", 1], ["café", 2]]\nunicos = []\nvistos = set()\nfor p in pedidos:\n    chave = tuple(p)\n    if chave not in vistos:\n        vistos.add(chave)\n        unicos.append(p)\nprint(unicos)',
          [OUT('print(tuple(["a", 1]) in {("a", 1)})', ["False", "Erro", "('a', 1)"], "A lista vira tupla, que tem hash e está no set."),
           MC("Por que não dá para fazer set([[1, 2], [1, 2]])?", "As listas de dentro não têm hash", ["set não aceita números", "Porque há repetidos", "Dá sim: vira {[1, 2]}"], "Converta cada item com tuple() antes."),
           CODE("Crie a função sem_repetidos(itens) que recebe uma lista de listas e devolve uma nova lista sem os repetidos, na ordem em que apareceram.",
                "def sem_repetidos(itens):\n    return itens\n",
                'def sem_repetidos(itens):\n    vistos = set()\n    unicos = []\n    for item in itens:\n        chave = tuple(item)\n        if chave not in vistos:\n            vistos.add(chave)\n            unicos.append(item)\n    return unicos',
                'assert sem_repetidos([[1, 2], [3], [1, 2]]) == [[1, 2], [3]], "Esperado [[1, 2], [3]]"\nassert sem_repetidos([["b"], ["a"], ["b"], ["a"]]) == [["b"], ["a"]], "Mantenha a ordem da primeira aparição"',
                "Guarde tuple(item) num set de vistos e só adicione o item se ele ainda não foi visto."),
           CODE("Complete a classe Produto para que dois produtos com o mesmo codigo sejam iguais e tenham o mesmo hash (o nome não importa).",
                "class Produto:\n    def __init__(self, codigo, nome):\n        self.codigo = codigo\n        self.nome = nome\n",
                'class Produto:\n    def __init__(self, codigo, nome):\n        self.codigo = codigo\n        self.nome = nome\n    def __eq__(self, outro):\n        return self.codigo == outro.codigo\n    def __hash__(self):\n        return hash(self.codigo)',
                'assert Produto(1, "Café") == Produto(1, "Café forte"), "Mesmo código deve ser igual"\nassert Produto(1, "Café") != Produto(2, "Café"), "Códigos diferentes não são iguais"\nassert len({Produto(1, "a"), Produto(1, "b"), Produto(2, "c")}) == 2, "O set deve ficar com 2 produtos"',
                "Crie __eq__ comparando self.codigo e __hash__ devolvendo hash(self.codigo).")]),
    ],
}

BUGS = r'''
@fn_bytes 1
b = bytes("olá")
print(len(b))
>>> b = bytes("olá", "utf-8")
!! Para transformar texto em bytes, diga a codificação.

@fn_bytes 1
dados = b"gato"
dados[0] = ord("p")
print(dados.decode())
>>> dados = bytearray(b"gato")
!! bytes não muda. Para alterar byte a byte, use bytearray.

@fn_bytes 2
b = "café".encode("utf-8")
print(len("café"))  # esperado: 5
>>> print(len(b))  # esperado: 5
!! len do texto conta letras. Para contar bytes, use len(b).

@fn_bytes 2
msg = b"Oi"
print(msg + "!")
>>> print(msg + b"!")
!! Não dá para somar bytes com texto. Use b"!".

@fn_bytes 1
b = bytes([72, 105, 300])
print(b)
>>> b = bytes([72, 105, 33])
!! Cada byte vai de 0 a 255; 300 não cabe.

@fn_bytes 2
msg = b"Oi"
print(msg[0] == "O")  # esperado: True
>>> print(msg[0] == ord("O"))  # esperado: True
!! O índice em bytes devolve um número. Compare com ord("O").

@fn_bytes 1
texto = b"ol\xc3\xa1".decode("ascii")
print(texto)
>>> texto = b"ol\xc3\xa1".decode("utf-8")
!! Esses bytes estão em UTF-8; ASCII não entende o á.

@fn_bytearray 2
ba = bytearray(b"oi")
ba.append("!")
print(ba.decode())
>>> ba.append(ord("!"))
!! append recebe um número. Use ord("!").

@fn_bytearray 1
ba = bytearray("gato")
print(len(ba))
>>> ba = bytearray("gato", "utf-8")
!! Com texto, bytearray precisa da codificação.

@fn_bytearray 2
ba = bytearray(b"abc")
ba[0] = b"x"
print(ba.decode())
>>> ba[0] = ord("x")
!! Cada posição guarda um número, não bytes.

@fn_bytearray 1
buffer = bytearray([5])
print(len(buffer))  # esperado: 5
>>> buffer = bytearray(5)
!! [5] cria um byte de valor 5. bytearray(5) cria 5 bytes zerados.

@fn_bytearray 3
cache = {}
chave = bytearray(b"id1")
cache[chave] = 10
>>> cache[bytes(chave)] = 10
!! bytearray muda e não tem hash. Converta para bytes para usar como chave.

@fn_bytearray 2
ba = bytearray(b"ola")
ba.extend(33)
print(ba.decode())
>>> ba.append(33)
!! extend espera vários bytes. Para um só número, use append.

@fn_memoryview 1
m = memoryview(b"abc")
m[0] = 65
print(m.tobytes())
>>> m = memoryview(bytearray(b"abc"))
!! Sobre bytes a janela é só leitura. Use um bytearray por baixo.

@fn_memoryview 1
m = memoryview("texto")
print(len(m))
>>> m = memoryview(b"texto")
!! memoryview só aceita objetos de bytes, não texto.

@fn_memoryview 3
dados = bytearray(b"abcdef")
m = memoryview(dados)
m[0:2] = b"XYZ"
print(dados.decode())
>>> m[0:2] = b"XY"
!! A fatia tem 2 posições; o pedaço novo precisa ter 2 bytes.

@fn_memoryview 2
dados = bytearray(b"abcdef")
parte = dados[0:3]
parte[0] = ord("X")
print(dados.decode())  # esperado: Xbcdef
>>> parte = memoryview(dados)[0:3]
!! A fatia do bytearray é uma cópia. A memoryview altera o original.

@fn_memoryview 2
m = memoryview(b"Oi")
print(m.decode())
>>> print(bytes(m).decode())
!! memoryview não tem decode. Converta antes com bytes(m).

@fn_memoryview 2
m = memoryview(bytearray(b"abc"))
print(m[0] == "a")  # esperado: True
>>> print(m[0] == ord("a"))  # esperado: True
!! m[0] é um número. Compare com ord("a").

@fn_hash 2
coord = [1, 2]
visitados = {coord}
print(len(visitados))
>>> visitados = {tuple(coord)}
!! Lista não tem hash. Converta para tupla antes de pôr no set.

@fn_hash 2
precos = {}
precos[["arroz", "feijão"]] = 30
print(precos)
>>> precos[("arroz", "feijão")] = 30
!! Chave de dicionário precisa de hash: use tupla, não lista.

@fn_hash 1
time = {"ana", "bia"}
pontos = {time: 10}
print(pontos[time])
>>> time = frozenset({"ana", "bia"})
!! set não tem hash. frozenset é a versão imutável, que serve de chave.

@fn_hash 1
chave = ("ana", [8, 9])
notas = {chave: "aprovada"}
print(notas[("ana", (8, 9))])
>>> chave = ("ana", (8, 9))
!! Uma tupla com lista dentro não tem hash. Use tupla dentro de tupla.

@fn_hash 5
class Aluno:
    def __init__(self, ra):
        self.ra = ra
    def __hash__(self):
        return str(self.ra)
print(len({Aluno(1), Aluno(2)}))
>>> return hash(self.ra)
!! __hash__ precisa devolver um número inteiro, não texto.

@fn_hash 5
class Pedido:
    def __init__(self, itens):
        self.itens = itens
    def __hash__(self):
        return hash(self.itens)
p = Pedido(["pão", "leite"])
print(hash(p) == hash(Pedido(["pão", "leite"])))
>>> return hash(tuple(self.itens))
!! self.itens é lista e não tem hash. Converta para tupla.

@fn_hash 3
a = "Gato"
b = "gato"
print(hash(a) == hash(b))  # esperado: True
>>> print(hash(a.lower()) == hash(b.lower()))  # esperado: True
!! Maiúsculas mudam o hash. Para ignorar, compare tudo em minúsculas.
'''
