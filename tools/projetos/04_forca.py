def c(s):
    return s.strip("\n") + "\n"


# ---------------------------------------------------------------- passo 1
S1 = c(r'''
import random

PALAVRAS = ["python", "banana", "teclado", "girafa", "janela", "abacaxi"]


def sortear_palavra(lista):
    return random.choice(lista)
''')

ST1 = c(r'''
import random

# TODO: coloque pelo menos 5 palavras (em minúsculas e sem acento) nesta lista
PALAVRAS = ["python"]


def sortear_palavra(lista):
    # TODO: devolva uma palavra sorteada da lista com random.choice
    return None
''')

T1 = r'''
assert len(PALAVRAS) >= 5, "A lista PALAVRAS precisa ter pelo menos 5 palavras."
for p in PALAVRAS:
    assert p == p.lower(), f"Use só letras minúsculas: '{p}' tem maiúsculas."
    assert p.isalpha(), f"A palavra '{p}' tem algo que não é letra (espaço, número, hífen...)."
    for letra in p:
        assert letra in "abcdefghijklmnopqrstuvwxyz", f"Tire o acento de '{p}': o jogo só aceita letras de a até z."
assert sortear_palavra(["gato"]) == "gato", "sortear_palavra(['gato']) deveria devolver 'gato'. Use return random.choice(lista)."
assert sortear_palavra(PALAVRAS) in PALAVRAS, "A palavra sorteada precisa vir da lista recebida."
'''

# ---------------------------------------------------------------- passo 2
S2 = S1 + c(r'''


def mascarar(palavra, letras_certas):
    partes = []
    for letra in palavra:
        if letra in letras_certas:
            partes.append(letra)
        else:
            partes.append("_")
    return " ".join(partes)
''')

ST2 = S1 + c(r'''


def mascarar(palavra, letras_certas):
    partes = []
    # TODO: para cada letra da palavra, coloque a letra em partes se ela está em letras_certas, senão coloque "_"
    # TODO: devolva as partes juntas, separadas por espaço
    return None
''')

T2 = r'''
r = mascarar("python", ["p", "t", "o"])
assert r == "p _ t _ o _", f"mascarar('python', ['p','t','o']) deveria dar 'p _ t _ o _', mas deu {r!r}."
r = mascarar("gato", [])
assert r == "_ _ _ _", f"Sem nenhuma letra certa, 'gato' vira '_ _ _ _'. Veio {r!r}."
r = mascarar("banana", ["a"])
assert r == "_ a _ a _ a", f"A letra 'a' aparece 3 vezes em 'banana': deveria dar '_ a _ a _ a', veio {r!r}."
r = mascarar("sol", ["s", "o", "l", "x"])
assert r == "s o l", f"Com todas as letras certas, mostre a palavra inteira: 's o l'. Veio {r!r}."
'''

# ---------------------------------------------------------------- passo 3
S3 = S2 + c(r'''


def validar_letra(chute, usadas):
    if len(chute) != 1:
        return "Digite só uma letra."
    if chute not in "abcdefghijklmnopqrstuvwxyz":
        return "Isso não é uma letra de a até z."
    if chute in usadas:
        return "Você já tentou essa letra!"
    return ""
''')

ST3 = S2 + c(r'''


def validar_letra(chute, usadas):
    # TODO: se chute não tiver exatamente 1 caractere, devolva "Digite só uma letra."
    # TODO: se chute não estiver em "abcdefghijklmnopqrstuvwxyz", devolva "Isso não é uma letra de a até z."
    # TODO: se chute já estiver em usadas, devolva "Você já tentou essa letra!"
    # TODO: se passou por tudo, devolva "" (texto vazio = letra válida)
    return None
''')

T3 = r'''
assert validar_letra("a", []) == "", "Uma letra nova e válida deve devolver '' (texto vazio)."
assert validar_letra("z", ["a", "b"]) == "", "'z' ainda não foi usada: deveria devolver ''."
r = validar_letra("ab", [])
assert r == "Digite só uma letra.", f"Para 'ab' (duas letras) devolva 'Digite só uma letra.'. Veio {r!r}."
r = validar_letra("", [])
assert r == "Digite só uma letra.", f"Texto vazio também não é uma letra: devolva 'Digite só uma letra.'. Veio {r!r}."
r = validar_letra("7", [])
assert r == "Isso não é uma letra de a até z.", f"'7' não é letra. Veio {r!r}."
r = validar_letra("A", [])
assert r == "Isso não é uma letra de a até z.", f"'A' maiúsculo não está em 'abc...z'. Veio {r!r}."
r = validar_letra("e", ["a", "e"])
assert r == "Você já tentou essa letra!", f"'e' já está em usadas. Veio {r!r}."
'''

# ---------------------------------------------------------------- passo 4
S4 = S3 + c(r'''


def contar_erros(palavra, usadas):
    erros = 0
    for letra in usadas:
        if letra not in palavra:
            erros += 1
    return erros


def acertou_tudo(palavra, usadas):
    for letra in palavra:
        if letra not in usadas:
            return False
    return True
''')

ST4 = S3 + c(r'''


def contar_erros(palavra, usadas):
    erros = 0
    # TODO: para cada letra em usadas que NÃO está na palavra, some 1 em erros
    return None


def acertou_tudo(palavra, usadas):
    # TODO: se alguma letra da palavra não está em usadas, devolva False
    # TODO: se todas estão, devolva True
    return None
''')

T4 = r'''
assert contar_erros("gato", []) == 0, "Sem letras usadas, são 0 erros."
assert contar_erros("gato", ["g", "a"]) == 0, "'g' e 'a' estão em 'gato': 0 erros."
r = contar_erros("gato", ["g", "x", "a", "z"])
assert r == 2, f"'x' e 'z' não estão em 'gato': deveriam ser 2 erros, veio {r!r}."
assert acertou_tudo("gato", ["o", "t", "a", "g"]) is True, "Todas as letras de 'gato' foram usadas: devolva True."
assert acertou_tudo("gato", ["g", "a", "t"]) is False, "Falta o 'o' de 'gato': devolva False."
assert acertou_tudo("banana", ["b", "a", "n", "x"]) is True, "Letras repetidas contam uma vez só: 'banana' com b, a, n está completa."
'''

# ---------------------------------------------------------------- passo 5
FORCA_CODE = r'''

MAX_ERROS = 6

# Um desenho para cada número de erros (0 a 6). O \\ vira uma barra invertida só.
FORCA = [
    "  +---+\n  |   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n=========",
]
'''

S5 = S4 + c(FORCA_CODE + r'''

def desenhar_forca(erros):
    if erros > MAX_ERROS:
        erros = MAX_ERROS
    return FORCA[erros]
''')

ST5 = S4 + c(FORCA_CODE + r'''

def desenhar_forca(erros):
    # TODO: se erros passar de MAX_ERROS, use MAX_ERROS
    # TODO: devolva o desenho da posição erros da lista FORCA
    return None
''')

T5 = r'''
assert MAX_ERROS == 6, "MAX_ERROS deve continuar valendo 6."
assert len(FORCA) == 7, "FORCA precisa ter 7 desenhos (de 0 a 6 erros)."
d0 = desenhar_forca(0)
assert d0 is not None, "desenhar_forca ainda devolve None. Use return FORCA[erros]."
assert "O" not in d0, "Com 0 erros a forca ainda está vazia (sem cabeça)."
assert desenhar_forca(1) == FORCA[1], "desenhar_forca(1) deve devolver FORCA[1]."
assert desenhar_forca(6) == FORCA[6], "desenhar_forca(6) deve devolver o boneco completo, FORCA[6]."
assert desenhar_forca(9) == FORCA[6], "Mais de 6 erros: mostre o último desenho (FORCA[6]) em vez de dar erro."
'''

# ---------------------------------------------------------------- passo 6
JOGAR = r'''


def jogar(palavra):
    usadas = []
    while contar_erros(palavra, usadas) < MAX_ERROS and not acertou_tudo(palavra, usadas):
        print(desenhar_forca(contar_erros(palavra, usadas)))
        print("Palavra:", mascarar(palavra, usadas))
        chute = input("Uma letra: ").strip().lower()
        problema = validar_letra(chute, usadas)
        if problema != "":
            print(problema)
            continue
        usadas.append(chute)
        if chute in palavra:
            print("Boa! Tem", chute)
        else:
            print("Não tem", chute)
    if acertou_tudo(palavra, usadas):
        print("Palavra:", mascarar(palavra, usadas))
        print("Você venceu! A palavra era", palavra)
        return True
    print(desenhar_forca(MAX_ERROS))
    print("Você perdeu! A palavra era", palavra)
    return False
'''

S6 = S5 + c(JOGAR)

ST6 = S5 + c(r'''


def jogar(palavra):
    usadas = []
    # TODO: repita enquanto os erros forem menores que MAX_ERROS e a palavra não estiver completa:
    # TODO:   mostre a forca e a palavra mascarada
    # TODO:   peça uma letra com input(), use .strip().lower() e valide com validar_letra
    # TODO:   se tiver problema, mostre a mensagem e use continue
    # TODO:   senão, guarde a letra em usadas e diga se ela está ou não na palavra
    # TODO: no fim, se acertou tudo, mostre "Você venceu!" e devolva True
    # TODO: senão, mostre a forca completa, "Você perdeu!" e devolva False
    return None
''')

T6 = r'''
import io, contextlib

def _joga(palavra, letras):
    global input
    entradas = iter(letras)
    input = lambda p="": next(entradas)
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        r = jogar(palavra)
    return r, saida.getvalue()

r, txt = _joga("gato", ["g", "a", "t", "o"])
assert r is True, f"Digitando g, a, t, o a palavra 'gato' está completa: jogar deve devolver True. Veio {r!r}."
assert "venceu" in txt, "Quando acerta tudo, mostre uma mensagem com 'venceu'."

r, txt = _joga("gato", ["x", "y", "z", "w", "k", "j"])
assert r is False, "Com 6 letras erradas, jogar deve devolver False."
assert "perdeu" in txt, "Quando erra 6 vezes, mostre uma mensagem com 'perdeu'."
assert "gato" in txt, "Ao perder, conte qual era a palavra."

r, txt = _joga("sol", ["S", "s", "ab", "7", "o", " L "])
assert r is True, "Letras maiúsculas e com espaços devem virar minúsculas (strip e lower), e letras repetidas ou inválidas não contam."
assert "já tentou" in txt, "Ao repetir uma letra, mostre a mensagem de validar_letra."

r, txt = _joga("ovo", ["x", "x", "x", "x", "x", "o", "v"])
assert r is True, "Repetir uma letra errada não pode contar como erro de novo (use continue antes de guardar a letra)."
'''

# ---------------------------------------------------------------- passo 7
MAIN = r'''


def main():
    print("=== JOGO DA FORCA ===")
    palavra = sortear_palavra(PALAVRAS)
    print("A palavra tem", len(palavra), "letras.")
    jogar(palavra)


if __name__ == "__main__":
    main()
'''

S7 = S6 + c(MAIN)

ST7 = S6 + c(r'''


def main():
    # TODO: mostre o título do jogo
    # TODO: sorteie uma palavra de PALAVRAS com sortear_palavra
    # TODO: diga quantas letras ela tem (len) e chame jogar(palavra)
    pass


if __name__ == "__main__":
    main()
''')

T7 = r'''
import io, contextlib
PALAVRAS = ["sol"]
entradas = iter(["s", "o", "l"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
txt = saida.getvalue()
assert txt.strip() != "", "main() ainda não mostra nada. Mostre o título e chame jogar(palavra)."
assert "3" in txt, "Diga quantas letras a palavra sorteada tem (use len)."
assert "venceu" in txt, "main() precisa chamar jogar(palavra) com a palavra sorteada de PALAVRAS."
'''

PROJETO = dict(
    id="forca",
    titulo="Jogo da forca",
    emoji="🪢",
    resumo="O computador sorteia uma palavra secreta e você tenta descobrir letra por letra antes que o boneco seja enforcado.",
    requer="u8l1",
    demo_entrada="\n".join("aeoirsntlcmdupbgvfhjqxzkwy"),
    passos=[
        dict(
            titulo="A lista de palavras",
            explica="Todo jogo da forca começa com uma palavra secreta. Vamos guardar várias palavras numa lista e deixar o "
                    "computador sortear uma. Para sortear, usamos o módulo random, que já vem com o Python: "
                    "random.choice(lista) devolve um item qualquer da lista.",
            tarefa="Coloque pelo menos 5 palavras (minúsculas, sem acento) em PALAVRAS e faça sortear_palavra devolver random.choice(lista).",
            starter=ST1, solucao=S1, tests=T1,
            dica="Não precisa de laço: uma linha com return random.choice(lista) resolve. E troque 'ç' e acentos: 'macã' vira 'maca'.",
        ),
        dict(
            titulo="Escondendo a palavra",
            explica="O jogador não pode ver a palavra, só os tracinhos. A função mascarar mostra cada letra que já foi "
                    "acertada e um '_' no lugar das outras. No fim, ' '.join(partes) junta a lista num texto com um espaço "
                    "entre os pedaços, para os tracinhos não grudarem.",
            tarefa="Complete mascarar(palavra, letras_certas) para que mascarar('python', ['p','t','o']) devolva 'p _ t _ o _'.",
            starter=ST2, solucao=S2, tests=T2,
            dica="Use for letra in palavra: e, dentro, um if letra in letras_certas para decidir entre partes.append(letra) e partes.append('_').",
        ),
        dict(
            titulo="Conferindo a letra digitada",
            explica="Gente digita de tudo: duas letras, números, a mesma letra de novo... Antes de aceitar o chute, vamos "
                    "conferir. Se algo estiver errado, a função devolve a mensagem de aviso; se estiver tudo certo, devolve "
                    "um texto vazio.",
            tarefa="Complete validar_letra(chute, usadas) seguindo os TODOs, na ordem: tamanho, se é letra, se já foi usada.",
            starter=ST3, solucao=S3, tests=T3,
            dica="len(chute) != 1 pega o tamanho errado. O operador in funciona com textos: 'b' in 'abc' é True.",
        ),
        dict(
            titulo="Contando erros e acertos",
            explica="Para saber se o jogo acabou, precisamos de duas respostas: quantas letras erradas já foram tentadas e "
                    "se todas as letras da palavra já apareceram. Vamos guardar todas as letras tentadas numa lista só, "
                    "usadas, e calcular o resto a partir dela.",
            tarefa="Complete contar_erros (quantas letras de usadas não estão na palavra) e acertou_tudo (True se toda letra da palavra está em usadas).",
            starter=ST4, solucao=S4, tests=T4,
            dica="Em acertou_tudo, um return False dentro do for sai na hora que achar uma letra faltando. Se o for terminar, é porque não faltou nenhuma.",
        ),
        dict(
            titulo="Desenhando a forca",
            explica="Agora a parte divertida: um desenho para cada erro! A lista FORCA já tem os 7 desenhos prontos, do "
                    "vazio (0 erros) ao boneco completo (6 erros). O \\n dentro do texto é uma quebra de linha. Sua função só "
                    "precisa escolher o desenho certo pela posição.",
            tarefa="Complete desenhar_forca(erros) para devolver FORCA[erros], sem passar do último desenho.",
            starter=ST5, solucao=S5, tests=T5,
            dica="Primeiro um if que troca erros por MAX_ERROS quando ele é maior. Depois é só acessar a lista pelo índice.",
        ),
        dict(
            titulo="A rodada do jogo",
            explica="Hora de juntar as peças! A função jogar repete a mesma coisa enquanto o jogo não acaba: mostra a forca, "
                    "mostra os tracinhos, pede uma letra e confere. O continue pula para a próxima volta do laço sem guardar "
                    "uma letra inválida. Quando o while termina, ou a pessoa ganhou, ou o boneco foi enforcado.",
            tarefa="Complete jogar(palavra) seguindo os TODOs: ela devolve True se a pessoa venceu e False se perdeu.",
            starter=ST6, solucao=S6, tests=T6,
            dica="A condição do while pode usar as suas funções: contar_erros(palavra, usadas) < MAX_ERROS and not acertou_tudo(palavra, usadas).",
        ),
        dict(
            titulo="Começando o jogo",
            explica="Falta só a função main, que liga tudo: sorteia a palavra e chama jogar. Repare no bloco "
                    "if __name__ == \"__main__\": no final. Ele quer dizer 'rode main() só quando este arquivo for o "
                    "programa principal'. Nos testes o arquivo é só importado, então o jogo não começa sozinho; quando "
                    "você toca em Jogar no editor, ele roda de verdade.",
            tarefa="Complete main(): mostre um título, sorteie a palavra com sortear_palavra(PALAVRAS), diga quantas letras ela tem e chame jogar(palavra).",
            starter=ST7, solucao=S7, tests=T7,
            dica="print('A palavra tem', len(palavra), 'letras.') mostra o tamanho. Depois é só chamar jogar(palavra).",
        ),
    ],
)
