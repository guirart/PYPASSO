PROJETO = dict(
    id="adivinha",
    titulo="Adivinhe o número",
    emoji="🎲",
    resumo="O computador sorteia um número de 1 a 100 e você tem 7 tentativas para descobrir qual é, com dicas de maior e menor.",
    requer="u5l1",
    demo_entrada="abc\n50\n25\n75\n12\n88\n37\n63\nn",
    passos=[
        # ---------------------------------------------------------------- 1
        dict(
            titulo="Comparando o palpite",
            explica=(
                "Todo jogo de adivinhar precisa responder uma pergunta: o palpite está certo, baixo ou alto? "
                "Vamos guardar essa lógica numa função, um bloquinho de código com nome que você cria com def. "
                "Ela recebe valores entre parênteses (os parâmetros) e devolve uma resposta com return. "
                "Assim dá para usar a mesma comparação quantas vezes quiser."
            ),
            tarefa=(
                "Complete a função comparar(palpite, secreto): ela deve devolver \"maior\" se o número secreto for maior "
                "que o palpite, \"menor\" se for menor e \"acertou\" se os dois forem iguais."
            ),
            starter='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    # TODO: se o palpite for menor que o secreto, devolva "maior" (o secreto é maior)
    # TODO: se o palpite for maior que o secreto, devolva "menor"
    # TODO: senão, devolva "acertou"
    return None
''',
            solucao='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"
''',
            tests='''assert comparar(10, 50) == "maior", "Com palpite 10 e secreto 50, o secreto é maior: devolva \\"maior\\"."
assert comparar(80, 50) == "menor", "Com palpite 80 e secreto 50, o secreto é menor: devolva \\"menor\\"."
assert comparar(50, 50) == "acertou", "Quando palpite e secreto são iguais, devolva \\"acertou\\"."
assert comparar(1, 100) == "maior", "comparar(1, 100) deveria dar \\"maior\\"."
assert comparar(100, 1) == "menor", "comparar(100, 1) deveria dar \\"menor\\"."
''',
            dica="Use if, elif e else comparando palpite com secreto, e escreva return \"...\" dentro de cada caso.",
        ),
        # ---------------------------------------------------------------- 2
        dict(
            titulo="Lendo o palpite com segurança",
            explica=(
                "O que a pessoa digita chega como texto, e às vezes vem errado: \"abc\", \"0\" ou \"500\". "
                "Se você usar int() direto num texto como \"abc\", o programa quebra. "
                "O método texto.isdigit() responde True quando o texto só tem algarismos, então dá para checar antes de converter. "
                "Quando o texto não serve, a função devolve None, o valor do Python que quer dizer \"nada\"."
            ),
            tarefa=(
                "Complete ler_numero(texto): tire os espaços com strip(), devolva None se o texto não for só algarismos "
                "ou se o número estiver fora de 1 a 100; caso contrário, devolva o número como int."
            ),
            starter='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    # TODO: tire os espaços das pontas com texto.strip()
    # TODO: se não for só algarismos (texto.isdigit()), devolva None
    # TODO: converta com int() e devolva None se ficar fora de 1 a 100
    # TODO: senão, devolva o número
    return None
''',
            solucao='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero
''',
            tests='''assert ler_numero("42") == 42, "ler_numero(\\"42\\") deveria devolver o número 42 (int, sem aspas)."
assert ler_numero(" 7 ") == 7, "Espaços nas pontas não podem atrapalhar: use texto.strip()."
assert ler_numero("100") == 100, "100 está dentro do intervalo, então deve ser aceito."
assert ler_numero("1") == 1, "1 está dentro do intervalo, então deve ser aceito."
assert ler_numero("abc") is None, "\\"abc\\" não é número: devolva None."
assert ler_numero("") is None, "Texto vazio não é número: devolva None."
assert ler_numero("-5") is None, "\\"-5\\" não passa no isdigit() e está fora de 1 a 100: devolva None."
assert ler_numero("0") is None, "0 está fora de 1 a 100: devolva None."
assert ler_numero("101") is None, "101 está fora de 1 a 100: devolva None."
''',
            dica="Faça as checagens em ordem: primeiro isdigit() (antes de int!), depois o intervalo com numero < 1 or numero > 100.",
        ),
        # ---------------------------------------------------------------- 3
        dict(
            titulo="O laço das tentativas",
            explica=(
                "Agora o coração do jogo: repetir a pergunta enquanto ainda houver tentativas. "
                "Um while com um contador resolve isso, e o continue pula para a próxima volta quando o texto não é um número válido (sem gastar tentativa). "
                "A função jogar recebe o número secreto como parâmetro, assim dá para testá-la sem depender de sorteio. "
                "Ela devolve True se a pessoa acertar e False se as tentativas acabarem."
            ),
            tarefa=(
                "Complete jogar(secreto): em cada volta leia um palpite com input(), use ler_numero e comparar, "
                "devolva True ao acertar, mostre a dica (\"O número secreto é maior/menor\") nos outros casos e devolva False quando acabarem as 7 tentativas."
            ),
            starter='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    # TODO: enquanto tentativas for menor que TENTATIVAS:
    # TODO:   leia o texto com input("Seu palpite: ") e converta com ler_numero
    # TODO:   se der None, avise "Digite um número inteiro de 1 a 100." e use continue
    # TODO:   some 1 em tentativas e guarde o resultado de comparar(palpite, secreto)
    # TODO:   se for "acertou", devolva True; senão, mostre a dica
    # TODO: depois do laço, devolva False
''',
            solucao='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            return True
        print("O número secreto é", resultado)
    return False
''',
            tests='''import io, contextlib

entradas = iter(["50", "30", "42"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    r = jogar(42)
assert r is True, "Com secreto 42 e palpites 50, 30, 42, jogar deveria devolver True (acertou no 3º)."
assert "menor" in saida.getvalue() and "maior" in saida.getvalue(), "Mostre a dica: \\"O número secreto é maior\\" ou \\"... menor\\"."

entradas = iter(["1"] * 7 + ["99"])
input = lambda p="": next(entradas)
with contextlib.redirect_stdout(io.StringIO()):
    r = jogar(99)
assert r is False, "Depois de 7 palpites errados, jogar deveria parar e devolver False (mesmo que o 8º palpite estivesse certo)."

entradas = iter(["abc", "500", "42"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    r = jogar(42)
assert r is True, "Palpites inválidos (\\"abc\\", \\"500\\") não podem quebrar o jogo: avise e use continue."
assert "1 a 100" in saida.getvalue(), "Quando o texto não serve, mostre \\"Digite um número inteiro de 1 a 100.\\""

entradas = iter(["abc"] * 3 + ["1"] * 6 + ["99"])
input = lambda p="": next(entradas)
with contextlib.redirect_stdout(io.StringIO()):
    r = jogar(99)
assert r is True, "Palpite inválido não deve gastar tentativa: some 1 em tentativas só depois do continue."
''',
            dica="Lembre de somar 1 em tentativas só depois de checar o None; senão o continue pula a soma (o que é bom) ou o laço nunca termina.",
        ),
        # ---------------------------------------------------------------- 4
        dict(
            titulo="Mensagens e tentativas restantes",
            explica=(
                "O jogo funciona, mas está mudo nas horas importantes. "
                "Vamos avisar quantas tentativas sobram depois de cada erro, comemorar quando a pessoa acerta e revelar o número quando ela perde. "
                "As f-strings deixam isso fácil: f\"Restam {restam} tentativas.\" troca {restam} pelo valor da variável."
            ),
            tarefa=(
                "Depois da dica, mostre \"Restam X tentativas.\"; ao acertar, mostre \"Acertou em X tentativa(s)!\" antes do return True; "
                "ao perder, mostre \"Suas tentativas acabaram! O número era X.\" antes do return False."
            ),
            starter='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            # TODO: mostre f"Acertou em {tentativas} tentativa(s)!"
            return True
        print("O número secreto é", resultado)
        # TODO: calcule restam = TENTATIVAS - tentativas e, se restam > 0, mostre f"Restam {restam} tentativas."
    # TODO: mostre f"Suas tentativas acabaram! O número era {secreto}."
    return False
''',
            solucao='''# Adivinhe o número, construído passo a passo.

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            print(f"Acertou em {tentativas} tentativa(s)!")
            return True
        print("O número secreto é", resultado)
        restam = TENTATIVAS - tentativas
        if restam > 0:
            print(f"Restam {restam} tentativas.")
    print(f"Suas tentativas acabaram! O número era {secreto}.")
    return False
''',
            tests='''import io, contextlib

entradas = iter(["50", "30", "42"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    r = jogar(42)
texto = saida.getvalue()
assert r is True, "jogar(42) com palpites 50, 30, 42 ainda precisa devolver True."
assert "Acertou em 3 tentativa(s)!" in texto, "Ao acertar no 3º palpite, mostre \\"Acertou em 3 tentativa(s)!\\" antes do return True."
assert "Restam 6 tentativas." in texto, "Depois do 1º erro, mostre \\"Restam 6 tentativas.\\" (TENTATIVAS - tentativas)."
assert "Restam 5 tentativas." in texto, "Depois do 2º erro, mostre \\"Restam 5 tentativas.\\""

entradas = iter(["1"] * 7)
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    r = jogar(77)
assert r is False, "Depois de 7 erros, jogar ainda precisa devolver False."
assert "Suas tentativas acabaram! O número era 77." in saida.getvalue(), "Ao perder, revele o número: \\"Suas tentativas acabaram! O número era 77.\\""
''',
            dica="O print da derrota fica depois do while, alinhado com o return False (fora do laço).",
        ),
        # ---------------------------------------------------------------- 5
        dict(
            titulo="Sorteio e a função main",
            explica=(
                "Falta sortear o número! Com import random você ganha acesso ao módulo random, e random.randint(1, 100) sorteia um inteiro de 1 a 100. "
                "Quem junta tudo é a função main, o ponto de partida do programa. "
                "Por fim, o bloco if __name__ == \"__main__\": main() quer dizer \"se este arquivo foi aberto para rodar, comece pela main\". "
                "Quando o arquivo é só importado (como nos testes), o jogo não começa sozinho."
            ),
            tarefa=(
                "Adicione import random no topo, crie main() que mostra \"Adivinhe o número de 1 a 100!\", sorteia secreto com random.randint(1, 100) e chama jogar(secreto), "
                "e termine o arquivo com o bloco if __name__ == \"__main__\": main()."
            ),
            starter='''# Adivinhe o número, construído passo a passo.
# TODO: importe o módulo random aqui

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            print(f"Acertou em {tentativas} tentativa(s)!")
            return True
        print("O número secreto é", resultado)
        restam = TENTATIVAS - tentativas
        if restam > 0:
            print(f"Restam {restam} tentativas.")
    print(f"Suas tentativas acabaram! O número era {secreto}.")
    return False


# TODO: crie def main(): que mostra "Adivinhe o número de 1 a 100!",
# TODO: sorteia secreto = random.randint(1, 100) e chama jogar(secreto)

# TODO: no fim do arquivo, escreva o bloco:  if __name__ == "__main__":  e, dentro dele, main()
''',
            solucao='''# Adivinhe o número, construído passo a passo.
import random

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            print(f"Acertou em {tentativas} tentativa(s)!")
            return True
        print("O número secreto é", resultado)
        restam = TENTATIVAS - tentativas
        if restam > 0:
            print(f"Restam {restam} tentativas.")
    print(f"Suas tentativas acabaram! O número era {secreto}.")
    return False


def main():
    print("Adivinhe o número de 1 a 100!")
    secreto = random.randint(1, 100)
    jogar(secreto)


if __name__ == "__main__":
    main()
''',
            tests='''import io, contextlib
import random as _random

assert __stdout__ == "", "Nada deve rodar quando o arquivo é importado: chame main() só dentro do bloco if __name__ == \\"__main__\\":"
assert "random" in globals(), "Faltou import random no topo do arquivo."

_original = _random.randint
_random.randint = lambda a, b: 42
try:
    entradas = iter(["42"])
    input = lambda p="": next(entradas)
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        main()
finally:
    _random.randint = _original
texto = saida.getvalue()
assert "Adivinhe o número de 1 a 100!" in texto, "main() deve começar mostrando \\"Adivinhe o número de 1 a 100!\\""
assert "Acertou em 1 tentativa(s)!" in texto, "main() deve sortear com random.randint(1, 100) e chamar jogar(secreto)."
''',
            dica="O bloco final não tem recuo: if __name__ == \"__main__\": numa linha e, embaixo, main() com 4 espaços.",
        ),
        # ---------------------------------------------------------------- 6
        dict(
            titulo="Jogar de novo e placar",
            explica=(
                "Uma partida só é pouco! Vamos colocar a main num while True que joga várias vezes. "
                "Como jogar devolve True ou False, dá para contar as vitórias num placar. "
                "No fim de cada partida, perguntamos se a pessoa quer jogar de novo; qualquer resposta diferente de \"s\" encerra com break."
            ),
            tarefa=(
                "Reescreva a main: conte vitorias e partidas, repita as partidas num while True, mostre \"Placar: X vitória(s) em Y partida(s).\" "
                "e pergunte \"Jogar de novo? (s/n) \"; se a resposta não for \"s\", saia do laço e mostre \"Valeu por jogar!\"."
            ),
            starter='''# Adivinhe o número, construído passo a passo.
import random

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            print(f"Acertou em {tentativas} tentativa(s)!")
            return True
        print("O número secreto é", resultado)
        restam = TENTATIVAS - tentativas
        if restam > 0:
            print(f"Restam {restam} tentativas.")
    print(f"Suas tentativas acabaram! O número era {secreto}.")
    return False


def main():
    print("Adivinhe o número de 1 a 100!")
    # TODO: crie vitorias = 0 e partidas = 0
    # TODO: coloque as duas linhas abaixo dentro de um while True:
    secreto = random.randint(1, 100)
    jogar(secreto)
    # TODO: se jogar(secreto) der True, some 1 em vitorias; some 1 em partidas sempre
    # TODO: mostre f"Placar: {vitorias} vitória(s) em {partidas} partida(s)."
    # TODO: pergunte input("Jogar de novo? (s/n) ") e use break se a resposta não for "s"
    # TODO: depois do laço, mostre "Valeu por jogar!"


if __name__ == "__main__":
    main()
''',
            solucao='''# Adivinhe o número, construído passo a passo.
import random

def comparar(palpite, secreto):
    if palpite < secreto:
        return "maior"
    elif palpite > secreto:
        return "menor"
    else:
        return "acertou"


def ler_numero(texto):
    texto = texto.strip()
    if not texto.isdigit():
        return None
    numero = int(texto)
    if numero < 1 or numero > 100:
        return None
    return numero


TENTATIVAS = 7


def jogar(secreto):
    tentativas = 0
    while tentativas < TENTATIVAS:
        texto = input("Seu palpite: ")
        palpite = ler_numero(texto)
        if palpite is None:
            print("Digite um número inteiro de 1 a 100.")
            continue
        tentativas = tentativas + 1
        resultado = comparar(palpite, secreto)
        if resultado == "acertou":
            print(f"Acertou em {tentativas} tentativa(s)!")
            return True
        print("O número secreto é", resultado)
        restam = TENTATIVAS - tentativas
        if restam > 0:
            print(f"Restam {restam} tentativas.")
    print(f"Suas tentativas acabaram! O número era {secreto}.")
    return False


def main():
    print("Adivinhe o número de 1 a 100!")
    vitorias = 0
    partidas = 0
    while True:
        secreto = random.randint(1, 100)
        if jogar(secreto):
            vitorias = vitorias + 1
        partidas = partidas + 1
        print(f"Placar: {vitorias} vitória(s) em {partidas} partida(s).")
        resposta = input("Jogar de novo? (s/n) ")
        if resposta.strip().lower() != "s":
            break
    print("Valeu por jogar!")


if __name__ == "__main__":
    main()
''',
            tests='''import io, contextlib
import random as _random

_original = _random.randint
_random.randint = lambda a, b: 42
try:
    entradas = iter(["42", "s", "42", "n"])
    input = lambda p="": next(entradas)
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        main()
    texto = saida.getvalue()
    assert "Placar: 1 vitória(s) em 1 partida(s)." in texto, "Depois da 1ª partida, mostre \\"Placar: 1 vitória(s) em 1 partida(s).\\""
    assert "Placar: 2 vitória(s) em 2 partida(s)." in texto, "Respondendo \\"s\\", o jogo deve recomeçar e o placar chegar a 2 vitória(s) em 2 partida(s)."
    assert "Valeu por jogar!" in texto, "Quando a resposta não for \\"s\\", saia do laço e mostre \\"Valeu por jogar!\\""

    entradas = iter(["1"] * 7 + ["n"])
    input = lambda p="": next(entradas)
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        main()
    assert "Placar: 0 vitória(s) em 1 partida(s)." in saida.getvalue(), "Derrota não conta vitória: o placar deveria ficar 0 vitória(s) em 1 partida(s)."
finally:
    _random.randint = _original
''',
            dica="Chame jogar(secreto) uma vez só, dentro do if: if jogar(secreto): já joga a partida e testa se ganhou.",
        ),
    ],
)
