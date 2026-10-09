PROJETO = dict(
    id="calculadora",
    titulo="Calculadora",
    emoji="🧮",
    resumo="Uma calculadora de terminal: você digita contas como 8 * 2 e ela responde, avisa divisão por zero e guarda o histórico.",
    requer="u6l0",
    demo_entrada="8 * 2\n10 / 4\n10 / 0\n7 - 10\n3 ^ 2\nabc\nhistorico\nsair",
    passos=[
        # ---------------------------------------------------------------- 1
        dict(
            titulo="As quatro operações",
            explica=(
                "Toda calculadora começa pelo básico: somar, subtrair, multiplicar e dividir. "
                "Cada operação vira uma função pequena que recebe dois números (a e b) e devolve o resultado com return. "
                "Funções curtas assim são fáceis de testar e de reaproveitar depois."
            ),
            tarefa="Complete as funções somar, subtrair, multiplicar e dividir, cada uma devolvendo a conta entre a e b.",
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    # TODO: devolva a soma de a e b
    pass


def subtrair(a, b):
    # TODO: devolva a menos b
    pass


def multiplicar(a, b):
    # TODO: devolva a vezes b
    pass


def dividir(a, b):
    # TODO: devolva a dividido por b
    pass
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    return a / b
''',
            tests='''assert somar(2, 3) == 5, "somar(2, 3) deveria devolver 5. Use return a + b."
assert subtrair(10, 4) == 6, "subtrair(10, 4) deveria devolver 6."
assert subtrair(4, 10) == -6, "subtrair(4, 10) deveria devolver -6 (a ordem importa: a - b)."
assert multiplicar(3, 7) == 21, "multiplicar(3, 7) deveria devolver 21."
assert dividir(10, 4) == 2.5, "dividir(10, 4) deveria devolver 2.5. Use / (barra simples)."
''',
            dica="Troque cada pass por um return com a conta. Na divisão use / e não //, para não perder as casas decimais.",
        ),
        # ---------------------------------------------------------------- 2
        dict(
            titulo="O despachante calcular",
            explica=(
                "Quem usa a calculadora escreve o operador como texto: \"+\", \"-\", \"*\" ou \"/\". "
                "A função calcular(a, op, b) olha o operador e chama a função certa, como um despachante. "
                "Se o operador for desconhecido, ela devolve None, o valor que quer dizer \"nada\"."
            ),
            tarefa=(
                "Complete calcular(a, op, b) com if/elif: para cada operador, devolva o resultado da função correspondente; "
                "para qualquer outro operador, devolva None."
            ),
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    return a / b


def calcular(a, op, b):
    # TODO: se op for "+", devolva somar(a, b)
    # TODO: faça o mesmo para "-", "*" e "/"
    # TODO: para qualquer outro operador, devolva None
    pass
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None
''',
            tests='''assert calcular(2, "+", 3) == 5, "calcular(2, \\"+\\", 3) deveria devolver 5."
assert calcular(9, "-", 4) == 5, "calcular(9, \\"-\\", 4) deveria devolver 5."
assert calcular(6, "*", 7) == 42, "calcular(6, \\"*\\", 7) deveria devolver 42."
assert calcular(9, "/", 2) == 4.5, "calcular(9, \\"/\\", 2) deveria devolver 4.5."
assert calcular(2, "^", 3) is None, "Operador desconhecido (como \\"^\\") deve devolver None."
assert calcular(2, "x", 3) is None, "Operador desconhecido (como \\"x\\") deve devolver None."
''',
            dica="Compare op com cada texto usando ==, por exemplo if op == \"+\": e devolva a chamada da função certa.",
        ),
        # ---------------------------------------------------------------- 3
        dict(
            titulo="Divisão por zero e respostas bonitas",
            explica=(
                "Dividir por zero não existe, e o Python reclama com um erro (ZeroDivisionError). "
                "Vamos proteger dividir: se b for 0, ela devolve None em vez de quebrar. "
                "Depois criamos responder(a, op, b), que transforma a conta num texto pronto para mostrar, como \"8 * 2 = 16\", "
                "ou numa mensagem amigável quando algo dá errado."
            ),
            tarefa=(
                "Faça dividir devolver None quando b for 0. Depois complete responder(a, op, b): devolva \"Operador desconhecido: X\" se op não for + - * /, "
                "\"Não dá para dividir por zero.\" se calcular devolver None, e senão f\"{a} {op} {b} = {resultado}\"."
            ),
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    # TODO: se b for 0, devolva None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    # TODO: se op não estiver em ["+", "-", "*", "/"], devolva f"Operador desconhecido: {op}"
    # TODO: guarde resultado = calcular(a, op, b)
    # TODO: se resultado for None, devolva "Não dá para dividir por zero."
    # TODO: senão, devolva f"{a} {op} {b} = {resultado}"
    pass
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"
''',
            tests='''r = None
try:
    r = dividir(5, 0)
except ZeroDivisionError:
    assert False, "dividir(5, 0) quebrou com ZeroDivisionError: teste if b == 0: return None antes de dividir."
assert r is None, "dividir(5, 0) deveria devolver None."
assert dividir(8, 2) == 4, "dividir(8, 2) ainda precisa devolver 4.0."
assert responder(8, "*", 2) == "8 * 2 = 16", "responder(8, \\"*\\", 2) deveria devolver \\"8 * 2 = 16\\"."
assert responder(7, "-", 10) == "7 - 10 = -3", "responder(7, \\"-\\", 10) deveria devolver \\"7 - 10 = -3\\"."
assert responder(10, "/", 4) == "10 / 4 = 2.5", "responder(10, \\"/\\", 4) deveria devolver \\"10 / 4 = 2.5\\"."
assert responder(10, "/", 0) == "Não dá para dividir por zero.", "Dividindo por zero, responder deve devolver \\"Não dá para dividir por zero.\\""
assert responder(3, "^", 2) == "Operador desconhecido: ^", "Com op \\"^\\", responder deve devolver \\"Operador desconhecido: ^\\""
''',
            dica="Teste o operador desconhecido primeiro, com not in; assim, quando calcular devolver None, só sobra o caso da divisão por zero.",
        ),
        # ---------------------------------------------------------------- 4
        dict(
            titulo="Entendendo o que foi digitado",
            explica=(
                "A pessoa vai escrever a conta numa linha só, como \"8 * 2\". "
                "O método texto.split() quebra o texto nos espaços e devolve uma lista: [\"8\", \"*\", \"2\"]. "
                "Antes de usar int(), conferimos com isdigit() se o pedaço só tem algarismos, para o programa não quebrar com algo como \"abc\". "
                "Nesta calculadora vamos trabalhar com números inteiros, sem sinal."
            ),
            tarefa=(
                "Complete ler_conta(texto): divida o texto com split(); se não vierem exatamente 3 partes, ou se o 1º ou o 3º pedaço não forem só algarismos, devolva None. "
                "Senão, devolva a lista [a, op, b] com a e b convertidos para int."
            ),
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    # TODO: se len(partes) for diferente de 3, devolva None
    # TODO: se partes[0] ou partes[2] não forem só algarismos (isdigit), devolva None
    # TODO: devolva [int(partes[0]), partes[1], int(partes[2])]
    return None
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    if len(partes) != 3:
        return None
    if not partes[0].isdigit() or not partes[2].isdigit():
        return None
    return [int(partes[0]), partes[1], int(partes[2])]
''',
            tests='''assert ler_conta("8 * 2") == [8, "*", 2], "ler_conta(\\"8 * 2\\") deveria devolver [8, \\"*\\", 2], com os números como int."
assert ler_conta("  10   /  4 ") == [10, "/", 4], "Espaços a mais não podem atrapalhar: split() sem argumentos já cuida disso."
assert ler_conta("3 ^ 2") == [3, "^", 2], "ler_conta só separa as partes; o operador desconhecido é problema do responder."
assert ler_conta("abc") is None, "\\"abc\\" não é uma conta: devolva None."
assert ler_conta("8 *") is None, "Com só 2 partes, devolva None."
assert ler_conta("1 + 2 + 3") is None, "Com mais de 3 partes, devolva None."
assert ler_conta("dois + 2") is None, "\\"dois\\" não é número: confira com isdigit() e devolva None."
assert ler_conta("2 + x") is None, "\\"x\\" não é número: devolva None."
''',
            dica="Lembre que os índices começam em 0: partes[0] é o primeiro número, partes[1] o operador e partes[2] o segundo número.",
        ),
        # ---------------------------------------------------------------- 5
        dict(
            titulo="O laço da calculadora e a main",
            explica=(
                "Agora juntamos tudo num laço: a main pergunta uma conta, mostra a resposta e repete até a pessoa digitar \"sair\". "
                "Se a conta vier num formato estranho, mostramos um exemplo e usamos continue para pedir de novo. "
                "No fim do arquivo entra o bloco if __name__ == \"__main__\": main(). Ele quer dizer \"se este arquivo foi aberto para rodar, comece pela main\"; "
                "quando o arquivo é só importado (como nos testes), nada começa sozinho."
            ),
            tarefa=(
                "Crie main(): num while True, leia texto = input(\"Conta (ou sair): \"); se for \"sair\", use break; se ler_conta der None, mostre "
                "\"Escreva assim: 8 * 2\" e use continue; senão, mostre responder(...). Depois do laço mostre \"Até mais!\" e adicione o bloco if __name__."
            ),
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    if len(partes) != 3:
        return None
    if not partes[0].isdigit() or not partes[2].isdigit():
        return None
    return [int(partes[0]), partes[1], int(partes[2])]


def main():
    print("Calculadora PyPasso! Digite contas como 8 * 2.")
    # TODO: while True:
    # TODO:   texto = input("Conta (ou sair): ").strip()
    # TODO:   se texto for "sair", use break
    # TODO:   conta = ler_conta(texto); se for None, mostre "Escreva assim: 8 * 2" e use continue
    # TODO:   mostre responder(conta[0], conta[1], conta[2])
    # TODO: depois do laço, mostre "Até mais!"

# TODO: no fim do arquivo:  if __name__ == "__main__":  e, dentro dele, main()
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    if len(partes) != 3:
        return None
    if not partes[0].isdigit() or not partes[2].isdigit():
        return None
    return [int(partes[0]), partes[1], int(partes[2])]


def main():
    print("Calculadora PyPasso! Digite contas como 8 * 2.")
    while True:
        texto = input("Conta (ou sair): ").strip()
        if texto == "sair":
            break
        conta = ler_conta(texto)
        if conta is None:
            print("Escreva assim: 8 * 2")
            continue
        print(responder(conta[0], conta[1], conta[2]))
    print("Até mais!")


if __name__ == "__main__":
    main()
''',
            tests='''import io, contextlib

assert __stdout__ == "", "Nada deve rodar quando o arquivo é importado: chame main() só dentro do bloco if __name__ == \\"__main__\\":"

entradas = iter(["8 * 2", "abc", "10 / 0", "sair", "1 + 1"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
texto = saida.getvalue()
assert "8 * 2 = 16" in texto, "Para \\"8 * 2\\", main deve mostrar \\"8 * 2 = 16\\" (use responder)."
assert "Escreva assim: 8 * 2" in texto, "Para \\"abc\\", main deve mostrar \\"Escreva assim: 8 * 2\\" e continuar."
assert "Não dá para dividir por zero." in texto, "Para \\"10 / 0\\", main deve mostrar a mensagem de divisão por zero."
assert "Até mais!" in texto, "Ao digitar \\"sair\\", saia do laço com break e mostre \\"Até mais!\\""
assert "1 + 1 = 2" not in texto, "Depois de \\"sair\\" a calculadora deve parar de pedir contas."
''',
            dica="O break fica dentro do if texto == \"sair\":, e o print(\"Até mais!\") fica fora do while, alinhado com ele.",
        ),
        # ---------------------------------------------------------------- 6
        dict(
            titulo="Histórico de contas",
            explica=(
                "Que tal lembrar das contas feitas? Uma lista vazia, historico = [], vai guardando cada resposta com append. "
                "Quando a pessoa digitar \"historico\", mostramos tudo, numerado, com um for. "
                "Se ainda não houver nada, avisamos com uma mensagem gentil."
            ),
            tarefa=(
                "Na main, crie historico = [] antes do laço e guarde cada resposta com append. Se o texto for \"historico\", "
                "mostre \"Nenhuma conta ainda.\" (lista vazia) ou cada conta como \"1. 8 * 2 = 16\", e use continue."
            ),
            starter='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    if len(partes) != 3:
        return None
    if not partes[0].isdigit() or not partes[2].isdigit():
        return None
    return [int(partes[0]), partes[1], int(partes[2])]


def main():
    print("Calculadora PyPasso! Digite contas como 8 * 2.")
    # TODO: crie a lista historico = []
    while True:
        texto = input("Conta (ou sair): ").strip()
        if texto == "sair":
            break
        # TODO: se texto for "historico":
        # TODO:   lista vazia? mostre "Nenhuma conta ainda."
        # TODO:   senão, mostre cada item numerado: f"{numero}. {item}"
        # TODO:   use continue
        conta = ler_conta(texto)
        if conta is None:
            print("Escreva assim: 8 * 2")
            continue
        print(responder(conta[0], conta[1], conta[2]))
        # TODO: guarde a resposta no historico (dica: guarde a resposta numa variável antes de mostrar)
    print("Até mais!")


if __name__ == "__main__":
    main()
''',
            solucao='''# Calculadora, construída passo a passo.

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        return None
    return a / b


def calcular(a, op, b):
    if op == "+":
        return somar(a, b)
    elif op == "-":
        return subtrair(a, b)
    elif op == "*":
        return multiplicar(a, b)
    elif op == "/":
        return dividir(a, b)
    else:
        return None


def responder(a, op, b):
    if op not in ["+", "-", "*", "/"]:
        return f"Operador desconhecido: {op}"
    resultado = calcular(a, op, b)
    if resultado is None:
        return "Não dá para dividir por zero."
    return f"{a} {op} {b} = {resultado}"


def ler_conta(texto):
    partes = texto.split()
    if len(partes) != 3:
        return None
    if not partes[0].isdigit() or not partes[2].isdigit():
        return None
    return [int(partes[0]), partes[1], int(partes[2])]


def main():
    print("Calculadora PyPasso! Digite contas como 8 * 2.")
    historico = []
    while True:
        texto = input("Conta (ou sair): ").strip()
        if texto == "sair":
            break
        if texto == "historico":
            if len(historico) == 0:
                print("Nenhuma conta ainda.")
            numero = 1
            for item in historico:
                print(f"{numero}. {item}")
                numero = numero + 1
            continue
        conta = ler_conta(texto)
        if conta is None:
            print("Escreva assim: 8 * 2")
            continue
        resposta = responder(conta[0], conta[1], conta[2])
        print(resposta)
        historico.append(resposta)
    print("Até mais!")


if __name__ == "__main__":
    main()
''',
            tests='''import io, contextlib

entradas = iter(["historico", "8 * 2", "10 / 4", "historico", "sair"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
texto = saida.getvalue()
assert "Nenhuma conta ainda." in texto, "Pedindo \\"historico\\" antes de qualquer conta, mostre \\"Nenhuma conta ainda.\\""
assert "1. 8 * 2 = 16" in texto, "No histórico, a 1ª conta deve aparecer como \\"1. 8 * 2 = 16\\"."
assert "2. 10 / 4 = 2.5" in texto, "No histórico, a 2ª conta deve aparecer como \\"2. 10 / 4 = 2.5\\"."
assert "Escreva assim" not in texto, "\\"historico\\" é um comando: trate-o antes do ler_conta e use continue."
assert "Até mais!" in texto, "\\"sair\\" ainda precisa encerrar com \\"Até mais!\\""
''',
            dica="Guarde o texto de responder numa variável (resposta), mostre com print e depois faça historico.append(resposta). Para numerar, use um contador que começa em 1.",
        ),
    ],
)
