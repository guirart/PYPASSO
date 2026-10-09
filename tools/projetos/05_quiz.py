def c(s):
    return s.strip("\n") + "\n"


# ---------------------------------------------------------------- passo 1
PERGUNTAS_INICIO = r'''
PERGUNTAS = [
    {
        "pergunta": "Qual comando mostra um texto na tela?",
        "opcoes": ["input()", "print()", "show()"],
        "resposta": 2,
    },
    {
        "pergunta": "Qual é o resultado de 7 // 2?",
        "opcoes": ["3", "3.5", "4"],
        "resposta": 1,
    },
    {
        "pergunta": "Que símbolo começa um comentário em Python?",
        "opcoes": ["//", "#", "--"],
        "resposta": 2,
    },
'''

S1 = c(PERGUNTAS_INICIO + r'''
    {
        "pergunta": "Qual destes é uma lista?",
        "opcoes": ["(1, 2, 3)", "{1, 2, 3}", "[1, 2, 3]"],
        "resposta": 3,
    },
    {
        "pergunta": "O que len('pato') devolve?",
        "opcoes": ["4", "pato", "5"],
        "resposta": 1,
    },
    {
        "pergunta": "Qual palavra cria uma função?",
        "opcoes": ["func", "def", "function"],
        "resposta": 2,
    },
]
''')

ST1 = c(PERGUNTAS_INICIO + r'''
    # TODO: crie pelo menos mais 2 perguntas sobre Python, no mesmo formato
]
''')

T1 = r'''
assert type(PERGUNTAS) == list, "PERGUNTAS precisa ser uma lista."
assert len(PERGUNTAS) >= 5, f"Crie pelo menos 5 perguntas. Agora tem {len(PERGUNTAS)}."
for i, item in enumerate(PERGUNTAS, start=1):
    assert type(item) == dict, f"A pergunta {i} precisa ser um dicionário {{...}}."
    for chave in ("pergunta", "opcoes", "resposta"):
        assert chave in item, f"A pergunta {i} está sem a chave '{chave}'."
    assert len(item["opcoes"]) >= 2, f"A pergunta {i} precisa de pelo menos 2 opções."
    assert type(item["resposta"]) == int, f"Na pergunta {i}, 'resposta' deve ser um número (1, 2, 3...), sem aspas."
    assert 1 <= item["resposta"] <= len(item["opcoes"]), f"Na pergunta {i}, 'resposta' precisa ser o número de uma das opções (de 1 a {len(item['opcoes'])})."
'''

# ---------------------------------------------------------------- passo 2
S2 = S1 + c(r'''


def mostrar_pergunta(numero, item):
    print(f"Pergunta {numero}: {item['pergunta']}")
    n = 1
    for opcao in item["opcoes"]:
        print(f"  {n}) {opcao}")
        n += 1
''')

ST2 = S1 + c(r'''


def mostrar_pergunta(numero, item):
    # TODO: mostre "Pergunta {numero}: " seguido do texto da pergunta
    # TODO: mostre cada opção numerada, começando em 1, assim: "  1) print()"
    pass
''')

T2 = r'''
import io, contextlib
item = {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "22"], "resposta": 2}
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    mostrar_pergunta(5, item)
linhas = [l.strip() for l in saida.getvalue().strip().splitlines()]
assert len(linhas) == 4, f"Deveria mostrar 4 linhas (a pergunta e 3 opções), mas mostrou {len(linhas)}."
assert linhas[0] == "Pergunta 5: Quanto é 2 + 2?", f"A primeira linha deveria ser 'Pergunta 5: Quanto é 2 + 2?', veio {linhas[0]!r}."
assert linhas[1] == "1) 3", f"A primeira opção deveria aparecer como '1) 3', veio {linhas[1]!r}."
assert linhas[3] == "3) 22", f"A última opção deveria aparecer como '3) 22', veio {linhas[3]!r}. A contagem começa em 1."
'''

# ---------------------------------------------------------------- passo 3
S3 = S2 + c(r'''


def corrigir(item, digitado):
    return digitado.strip() == str(item["resposta"])
''')

ST3 = S2 + c(r'''


def corrigir(item, digitado):
    # TODO: digitado é um texto, como "2". Tire os espaços com strip()
    # TODO: devolva True se ele for igual à resposta certa (transforme o número em texto com str)
    return None
''')

T3 = r'''
item = {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "22"], "resposta": 2}
assert corrigir(item, "2") is True, "corrigir(item, '2') deveria dar True: a resposta certa é a opção 2."
assert corrigir(item, " 2 ") is True, "Espaços sobrando não podem atrapalhar: use strip()."
assert corrigir(item, "1") is False, "corrigir(item, '1') deveria dar False."
assert corrigir(item, "banana") is False, "Uma resposta que nem é número também é errada (False), sem dar erro."
'''

# ---------------------------------------------------------------- passo 4
S4 = S3 + c(r'''


def mensagem_final(acertos, total):
    porcentagem = acertos / total * 100
    texto = f"Você acertou {acertos} de {total}. "
    if porcentagem == 100:
        return texto + "Perfeito! Você é fera em Python!"
    elif porcentagem >= 70:
        return texto + "Mandou bem!"
    elif porcentagem >= 40:
        return texto + "Quase lá, continue treinando!"
    else:
        return texto + "Bora revisar as lições e tentar de novo!"
''')

ST4 = S3 + c(r'''


def mensagem_final(acertos, total):
    porcentagem = acertos / total * 100
    texto = f"Você acertou {acertos} de {total}. "
    # TODO: 100% -> texto + "Perfeito! Você é fera em Python!"
    # TODO: 70% ou mais -> texto + "Mandou bem!"
    # TODO: 40% ou mais -> texto + "Quase lá, continue treinando!"
    # TODO: menos que isso -> texto + "Bora revisar as lições e tentar de novo!"
    return None
''')

T4 = r'''
r = mensagem_final(10, 10)
assert r is not None, "mensagem_final ainda devolve None."
assert r.startswith("Você acertou 10 de 10."), f"A mensagem deve começar com 'Você acertou 10 de 10.', veio {r!r}."
assert "Perfeito" in r, "Com 10 de 10 (100%) a mensagem deve ter 'Perfeito'."
assert "Mandou bem" in mensagem_final(7, 10), "Com 7 de 10 (70%) a mensagem deve ter 'Mandou bem'."
assert "Mandou bem" in mensagem_final(4, 5), "Com 4 de 5 (80%) a mensagem deve ter 'Mandou bem'."
assert "Quase lá" in mensagem_final(2, 5), "Com 2 de 5 (40%) a mensagem deve ter 'Quase lá'."
assert "revisar" in mensagem_final(1, 5), "Com 1 de 5 (20%) a mensagem deve falar em 'revisar'."
assert "revisar" in mensagem_final(0, 3), "Com 0 acertos a mensagem deve falar em 'revisar'."
'''

# ---------------------------------------------------------------- passo 5
S5 = S4 + c(r'''


def fazer_quiz(perguntas):
    acertos = 0
    erradas = []
    numero = 1
    for item in perguntas:
        mostrar_pergunta(numero, item)
        digitado = input("Sua resposta: ")
        if corrigir(item, digitado):
            print("Certo! 🎉")
            acertos += 1
        else:
            print("Errado!")
            erradas.append(item)
        numero += 1
    return {"acertos": acertos, "erradas": erradas}
''')

ST5 = S4 + c(r'''


def fazer_quiz(perguntas):
    acertos = 0
    erradas = []
    numero = 1
    # TODO: para cada item em perguntas:
    # TODO:   mostre a pergunta com mostrar_pergunta e peça a resposta com input()
    # TODO:   se corrigir der True, mostre "Certo!" e some 1 em acertos
    # TODO:   senão, mostre "Errado!" e guarde o item em erradas
    # TODO:   some 1 em numero
    # TODO: devolva o dicionário {"acertos": acertos, "erradas": erradas}
    return None
''')

T5 = r'''
import io, contextlib
p1 = {"pergunta": "A?", "opcoes": ["x", "y"], "resposta": 1}
p2 = {"pergunta": "B?", "opcoes": ["x", "y"], "resposta": 2}
p3 = {"pergunta": "C?", "opcoes": ["x", "y", "z"], "resposta": 3}
entradas = iter(["1", "1", "3"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    r = fazer_quiz([p1, p2, p3])
txt = saida.getvalue()
assert type(r) == dict, f"fazer_quiz deve devolver um dicionário com 'acertos' e 'erradas'. Veio {r!r}."
assert r.get("acertos") == 2, f"Respondendo 1, 1, 3 a pessoa acerta 2 perguntas. Veio acertos = {r.get('acertos')!r}."
assert r.get("erradas") == [p2], "A lista 'erradas' deve ter só a pergunta B (a que foi respondida errado)."
assert "Pergunta 3: C?" in txt, "Use mostrar_pergunta(numero, item) e conte as perguntas a partir de 1."
assert "Certo" in txt and "Errado" in txt, "Diga 'Certo!' ou 'Errado!' depois de cada resposta."
'''

# ---------------------------------------------------------------- passo 6
S6 = S5 + c(r'''


def mostrar_resumo(erradas):
    if len(erradas) == 0:
        print("Nenhum erro! 🏆")
        return
    print("Revise estas:")
    for item in erradas:
        certa = item["opcoes"][item["resposta"] - 1]
        print(f"- {item['pergunta']} Resposta: {certa}")
''')

ST6 = S5 + c(r'''


def mostrar_resumo(erradas):
    # TODO: se erradas estiver vazia, mostre "Nenhum erro!" e pare a função com return
    # TODO: senão, mostre "Revise estas:" e, para cada item, a pergunta e o TEXTO da opção certa
    # TODO: lembre: a opção 1 está no índice 0 de item["opcoes"]
    pass
''')

T6 = r'''
import io, contextlib
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    mostrar_resumo([])
assert "Nenhum erro" in saida.getvalue(), "Com a lista vazia, mostre 'Nenhum erro!'."

p = {"pergunta": "Qual palavra cria uma função?", "opcoes": ["func", "def", "function"], "resposta": 2}
q = {"pergunta": "Que símbolo começa um comentário?", "opcoes": ["//", "#", "--"], "resposta": 2}
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    mostrar_resumo([p, q])
txt = saida.getvalue()
assert "Nenhum erro" not in txt, "Se tem perguntas erradas, não diga 'Nenhum erro!'."
assert "Qual palavra cria uma função?" in txt and "Que símbolo começa um comentário?" in txt, "Mostre o texto de cada pergunta errada."
assert "def" in txt and "#" in txt, "Mostre o texto da opção certa (para resposta 2, use item['opcoes'][1])."
assert "function" not in txt, "Mostre só a opção certa, não todas. Lembre: a opção 2 fica no índice 1."
'''

# ---------------------------------------------------------------- passo 7
MAIN = r'''


def main():
    print("=== QUIZ DE PYTHON ===")
    perguntas = PERGUNTAS.copy()
    random.shuffle(perguntas)
    resultado = fazer_quiz(perguntas)
    print(mensagem_final(resultado["acertos"], len(perguntas)))
    mostrar_resumo(resultado["erradas"])


if __name__ == "__main__":
    main()
'''

S7 = "import random\n\n" + S6 + c(MAIN)

ST7 = "import random\n\n" + S6 + c(r'''


def main():
    print("=== QUIZ DE PYTHON ===")
    # TODO: faça uma cópia de PERGUNTAS com .copy() e embaralhe a cópia com random.shuffle
    # TODO: chame fazer_quiz com a cópia e guarde o resultado
    # TODO: mostre mensagem_final(acertos, total) e depois mostrar_resumo(erradas)
    pass


if __name__ == "__main__":
    main()
''')

T7 = r'''
import io, contextlib
antes = PERGUNTAS.copy()
entradas = iter(["1"] * 50)
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
txt = saida.getvalue()
assert "Pergunta 1:" in txt, "main() precisa chamar fazer_quiz com as perguntas."
assert f"de {len(PERGUNTAS)}." in txt, "No fim, mostre mensagem_final(acertos, total), com o total de perguntas."
assert "Revise" in txt or "Nenhum erro" in txt, "Depois da nota, chame mostrar_resumo com as perguntas erradas."
assert PERGUNTAS == antes, "Embaralhe uma CÓPIA (PERGUNTAS.copy()), não a lista original."
'''

PROJETO = dict(
    id="quiz",
    titulo="Quiz de Python",
    emoji="❓",
    resumo="Um quiz de múltipla escolha sobre Python, com perguntas embaralhadas, nota no final e revisão do que você errou.",
    requer="u7l1",
    demo_entrada="\n".join(["2", "1", "2", "3", "1", "2", "1", "1", "1", "1"]),
    passos=[
        dict(
            titulo="Guardando as perguntas",
            explica="Cada pergunta do quiz tem três partes: o texto, as opções e qual opção é a certa. Um dicionário é perfeito "
                    "para isso, e uma lista de dicionários guarda o quiz inteiro. A 'resposta' é o número da opção certa, "
                    "contando a partir de 1, como a pessoa vai digitar.",
            tarefa="Crie pelo menos mais 2 perguntas sobre Python em PERGUNTAS, no mesmo formato das que já estão lá.",
            starter=ST1, solucao=S1, tests=T1,
            dica="Copie um dicionário inteiro, das chaves { até }, e troque o conteúdo. Não esqueça a vírgula entre um dicionário e outro.",
        ),
        dict(
            titulo="Mostrando uma pergunta",
            explica="Agora vamos mostrar uma pergunta na tela, com as opções numeradas. Para acessar uma parte do dicionário "
                    "usamos a chave: item['pergunta']. Dentro de uma f-string com aspas duplas, use aspas simples na chave.",
            tarefa="Complete mostrar_pergunta(numero, item) para mostrar 'Pergunta 1: ...' e, embaixo, cada opção como '  1) texto'.",
            starter=ST2, solucao=S2, tests=T2,
            dica="Crie um contador n = 1 antes do for das opções e some 1 nele a cada volta.",
        ),
        dict(
            titulo="Corrigindo a resposta",
            explica="O input() sempre devolve texto, mas a resposta certa está guardada como número. Para comparar, "
                    "transformamos o número em texto com str(). Assim, se a pessoa digitar 'banana', não dá erro: só fica errado.",
            tarefa="Complete corrigir(item, digitado) para devolver True quando o texto digitado for o número da opção certa.",
            starter=ST3, solucao=S3, tests=T3,
            dica="Uma comparação com == já é True ou False, então dá para devolver ela direto no return.",
        ),
        dict(
            titulo="A nota final",
            explica="No fim do quiz, uma mensagem conforme o desempenho deixa tudo mais divertido. Calculamos a porcentagem "
                    "de acertos e usamos if, elif e else para escolher o comentário. A ordem importa: teste do maior para o menor.",
            tarefa="Complete mensagem_final(acertos, total) com as quatro faixas indicadas nos TODOs.",
            starter=ST4, solucao=S4, tests=T4,
            dica="Comece com if porcentagem == 100, depois elif porcentagem >= 70, depois elif porcentagem >= 40 e, por último, else.",
        ),
        dict(
            titulo="Jogando o quiz",
            explica="Esta função faz o quiz de verdade: passa por todas as perguntas, pede a resposta e conta os acertos. "
                    "Ela também guarda as perguntas erradas numa lista, para revisar depois. Como são duas informações, "
                    "devolvemos as duas dentro de um dicionário.",
            tarefa="Complete fazer_quiz(perguntas) usando mostrar_pergunta, input() e corrigir, e devolva {'acertos': ..., 'erradas': ...}.",
            starter=ST5, solucao=S5, tests=T5,
            dica="Dentro do for: mostrar_pergunta(numero, item), digitado = input('Sua resposta: ') e um if corrigir(item, digitado):.",
        ),
        dict(
            titulo="Revisando os erros",
            explica="Errar faz parte de aprender! Vamos mostrar as perguntas erradas com a resposta certa. Como a opção 1 "
                    "fica no índice 0 da lista, a opção certa está em item['opcoes'][item['resposta'] - 1].",
            tarefa="Complete mostrar_resumo(erradas): 'Nenhum erro!' se a lista estiver vazia, senão cada pergunta com o texto da opção certa.",
            starter=ST6, solucao=S6, tests=T6,
            dica="Um return sozinho para a função na hora. Use isso logo depois de mostrar 'Nenhum erro!'.",
        ),
        dict(
            titulo="Embaralhando e começando",
            explica="Para o quiz não ser sempre igual, embaralhamos as perguntas com random.shuffle, do módulo random. "
                    "Embaralhamos uma cópia, para não bagunçar a lista original. O bloco if __name__ == \"__main__\": no fim "
                    "quer dizer 'rode main() só quando este arquivo for o programa principal': nos testes ele não roda, "
                    "mas roda quando você toca em Jogar no editor.",
            tarefa="Complete main(): embaralhe uma cópia de PERGUNTAS, rode fazer_quiz, mostre a mensagem final e o resumo dos erros.",
            starter=ST7, solucao=S7, tests=T7,
            dica="random.shuffle(lista) embaralha a lista ali mesmo e não devolve nada, então não escreva perguntas = random.shuffle(...).",
        ),
    ],
)
