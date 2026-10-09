PROJETO = dict(
    id="tarefas",
    titulo="Lista de tarefas",
    emoji="✅",
    resumo="Um organizador de tarefas no terminal: adicione, liste, conclua e remova tarefas por um menu.",
    requer="u6l1",
    demo_entrada="1\nComprar pão\n1\nEstudar Python\n1\nRegar as plantas\n2\n3\n2\n4\n1\n3\n9\n2\nsair",
    passos=[
        # ---------------------------------------------------------------- 1
        dict(
            titulo="Adicionando tarefas",
            explica=(
                "Cada tarefa precisa de duas informações: o texto e se já foi feita. "
                "Vamos guardar cada uma como uma listinha de dois itens, [texto, feita], por exemplo [\"Comprar pão\", False]. "
                "Todas as tarefas ficam numa lista maior, então teremos uma lista de listas. "
                "A função adicionar recebe essa lista e o texto, e coloca a nova tarefa no fim com append."
            ),
            tarefa=(
                "Complete adicionar(tarefas, texto): tire os espaços das pontas; se o texto ficar vazio, devolva False sem adicionar nada; "
                "senão, adicione [texto, False] à lista e devolva True."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    # TODO: se texto for "", devolva False
    # TODO: adicione [texto, False] em tarefas com append e devolva True
    return None
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True
''',
            tests='''lista = []
r = adicionar(lista, "Comprar pão")
assert r is True, "Ao adicionar uma tarefa válida, devolva True."
assert lista == [["Comprar pão", False]], "Depois de adicionar, a lista deveria ser [[\\"Comprar pão\\", False]]."
adicionar(lista, "  Estudar Python  ")
assert lista[1] == ["Estudar Python", False], "Tire os espaços das pontas antes de guardar: \\"  Estudar Python  \\" vira \\"Estudar Python\\"."
r = adicionar(lista, "   ")
assert r is False, "Texto vazio (ou só espaços) deve devolver False."
assert len(lista) == 2, "Texto vazio não pode entrar na lista."
''',
            dica="Use tarefas.append([texto, False]): repare nos colchetes, você está colocando uma lista dentro da outra.",
        ),
        # ---------------------------------------------------------------- 2
        dict(
            titulo="Listando com números",
            explica=(
                "Para escolher uma tarefa depois, cada uma precisa de um número na tela. "
                "Vamos percorrer a lista com for e um contador que começa em 1 (gente conta a partir de 1, o Python a partir de 0). "
                "Tarefa feita aparece com [x] e pendente com [ ], como uma caixinha de marcar."
            ),
            tarefa=(
                "Complete listar(tarefas): se a lista estiver vazia, mostre \"Nenhuma tarefa ainda.\"; senão, mostre cada tarefa como "
                "\"1. [ ] Comprar pão\" ou \"2. [x] Estudar Python\"."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    # TODO: se len(tarefas) for 0, mostre "Nenhuma tarefa ainda."
    numero = 1
    for tarefa in tarefas:
        # TODO: a caixinha é "[x]" se tarefa[1] for True, senão "[ ]"
        # TODO: mostre f"{numero}. {caixa} {tarefa[0]}"
        numero = numero + 1
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1
''',
            tests='''import io, contextlib

saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    listar([])
assert "Nenhuma tarefa ainda." in saida.getvalue(), "Com a lista vazia, mostre \\"Nenhuma tarefa ainda.\\""

saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    listar([["Comprar pão", False], ["Estudar Python", True]])
texto = saida.getvalue()
assert "1. [ ] Comprar pão" in texto, "A 1ª tarefa (pendente) deveria aparecer como \\"1. [ ] Comprar pão\\"."
assert "2. [x] Estudar Python" in texto, "A 2ª tarefa (feita) deveria aparecer como \\"2. [x] Estudar Python\\"."
assert "Nenhuma tarefa" not in texto, "Só mostre \\"Nenhuma tarefa ainda.\\" quando a lista estiver vazia."
''',
            dica="tarefa[0] é o texto e tarefa[1] é True ou False. Use um if/else para escolher a caixinha antes do print.",
        ),
        # ---------------------------------------------------------------- 3
        dict(
            titulo="Concluindo uma tarefa",
            explica=(
                "Marcar como feita é trocar o False por True. "
                "Mas cuidado com a diferença de contagem: a tarefa número 1 da tela está na posição 0 da lista, então usamos tarefas[n - 1]. "
                "Também precisamos recusar números que não existem, como 0 ou 99, senão o Python dá IndexError."
            ),
            tarefa=(
                "Complete concluir(tarefas, n): se n for menor que 1 ou maior que len(tarefas), devolva False; "
                "senão, marque tarefas[n - 1][1] como True e devolva True."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    # TODO: se n < 1 ou n > len(tarefas), devolva False
    # TODO: marque tarefas[n - 1][1] = True e devolva True
    return None
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True
''',
            tests='''lista = [["Comprar pão", False], ["Estudar Python", False]]
r = concluir(lista, 2)
assert r is True, "concluir(lista, 2) com 2 tarefas deveria devolver True."
assert lista[1][1] is True, "A tarefa número 2 (posição 1 da lista) deveria ficar marcada como True."
assert lista[0][1] is False, "Só a tarefa escolhida muda: a número 1 deveria continuar False. Lembre do n - 1."
assert concluir(lista, 0) is False, "Não existe tarefa número 0: devolva False."
assert concluir(lista, 3) is False, "Com 2 tarefas, a número 3 não existe: devolva False."
assert concluir([], 1) is False, "Numa lista vazia, nenhuma tarefa existe: devolva False."
''',
            dica="Primeiro confira o intervalo com if n < 1 or n > len(tarefas):, e só depois mexa na lista.",
        ),
        # ---------------------------------------------------------------- 4
        dict(
            titulo="Removendo uma tarefa",
            explica=(
                "Para apagar uma tarefa da lista usamos pop, que tira o item de uma posição e ainda devolve o que foi tirado. "
                "Assim conseguimos dizer qual tarefa saiu, com o texto dela. "
                "Quando o número não existe, devolvemos None, o valor do Python que quer dizer \"nada\"; para testar isso, use is None."
            ),
            tarefa=(
                "Complete remover(tarefas, n): se o número não existir, devolva None; senão, tire a tarefa com tarefas.pop(n - 1) "
                "e devolva o texto dela."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    # TODO: se n < 1 ou n > len(tarefas), devolva None
    # TODO: tirada = tarefas.pop(n - 1)
    # TODO: devolva o texto da tarefa tirada (tirada[0])
    return None
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]
''',
            tests='''lista = [["Comprar pão", False], ["Estudar Python", True], ["Regar as plantas", False]]
r = remover(lista, 2)
assert r == "Estudar Python", "remover(lista, 2) deveria devolver o texto da tarefa tirada: \\"Estudar Python\\"."
assert len(lista) == 2, "Depois de remover, a lista deveria ter 2 tarefas."
assert lista[1][0] == "Regar as plantas", "A tarefa que vinha depois sobe uma posição; confira se você usou pop(n - 1)."
assert remover(lista, 0) is None, "Não existe tarefa número 0: devolva None."
assert remover(lista, 5) is None, "Com 2 tarefas, a número 5 não existe: devolva None."
assert len(lista) == 2, "Número inválido não pode apagar nada."
''',
            dica="pop(posição) devolve a tarefa inteira, [texto, feita]; o texto é o item [0] dela.",
        ),
        # ---------------------------------------------------------------- 5
        dict(
            titulo="Lendo o número da tarefa",
            explica=(
                "No menu, a pessoa vai digitar o número da tarefa, e isso chega como texto. "
                "O método isdigit() diz se o texto só tem algarismos, então dá para converter com int() sem medo de erro. "
                "Se não for número, devolvemos 0: como nenhuma tarefa tem número 0, concluir e remover já vão recusar sozinhos."
            ),
            tarefa=(
                "Complete ler_numero(texto): tire os espaços das pontas; se for só algarismos, devolva int(texto); senão, devolva 0."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    # TODO: tire os espaços das pontas com strip()
    # TODO: se texto.isdigit() for True, devolva int(texto)
    # TODO: senão, devolva 0
    return None
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return 0
''',
            tests='''assert ler_numero("3") == 3, "ler_numero(\\"3\\") deveria devolver o número 3 (int, sem aspas)."
assert ler_numero(" 12 ") == 12, "Espaços nas pontas não podem atrapalhar: use strip()."
assert ler_numero("abc") == 0, "\\"abc\\" não é número: devolva 0."
assert ler_numero("") == 0, "Texto vazio: devolva 0."
assert ler_numero("-1") == 0, "\\"-1\\" não passa no isdigit(): devolva 0."
assert concluir([["Teste", False]], ler_numero("xyz")) is False, "Com ler_numero devolvendo 0, concluir deve recusar sozinho."
''',
            dica="Confira com isdigit() antes de chamar int(); se chamar int(\"abc\") o programa quebra com ValueError.",
        ),
        # ---------------------------------------------------------------- 6
        dict(
            titulo="O menu",
            explica=(
                "Hora de juntar as peças num menu que se repete até a pessoa digitar \"sair\". "
                "Cada opção chama uma das funções que você já fez, e o resultado delas (True, False, None ou um texto) decide a mensagem. "
                "A função menu recebe a lista de tarefas como parâmetro, assim os testes podem conferir o que aconteceu com ela."
            ),
            tarefa=(
                "Complete menu(tarefas): num while True, leia a opção; \"sair\" encerra com break; \"1\" pede o texto e adiciona; \"2\" lista; "
                "\"3\" pede o número e conclui; \"4\" pede o número e remove; qualquer outra coisa mostra \"Opção inválida.\"."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return 0


def menu(tarefas):
    while True:
        print()
        print("1 adicionar | 2 listar | 3 concluir | 4 remover | sair")
        opcao = input("Escolha: ").strip()
        # TODO: "sair" -> break
        # TODO: "1" -> texto = input("Nova tarefa: "); se adicionar der True mostre "Tarefa adicionada!",
        # TODO:        senão "A tarefa não pode ficar vazia."
        # TODO: "2" -> listar(tarefas)
        # TODO: "3" -> n = ler_numero(input("Número da tarefa: ")); se concluir der True mostre "Tarefa concluída!",
        # TODO:        senão "Não achei essa tarefa."
        # TODO: "4" -> n = ler_numero(input("Número da tarefa: ")); removida = remover(tarefas, n);
        # TODO:        se removida for None mostre "Não achei essa tarefa.", senão f"Removida: {removida}"
        # TODO: qualquer outra opção -> "Opção inválida."
        break
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return 0


def menu(tarefas):
    while True:
        print()
        print("1 adicionar | 2 listar | 3 concluir | 4 remover | sair")
        opcao = input("Escolha: ").strip()
        if opcao == "sair":
            break
        elif opcao == "1":
            texto = input("Nova tarefa: ")
            if adicionar(tarefas, texto):
                print("Tarefa adicionada!")
            else:
                print("A tarefa não pode ficar vazia.")
        elif opcao == "2":
            listar(tarefas)
        elif opcao == "3":
            n = ler_numero(input("Número da tarefa: "))
            if concluir(tarefas, n):
                print("Tarefa concluída!")
            else:
                print("Não achei essa tarefa.")
        elif opcao == "4":
            n = ler_numero(input("Número da tarefa: "))
            removida = remover(tarefas, n)
            if removida is None:
                print("Não achei essa tarefa.")
            else:
                print(f"Removida: {removida}")
        else:
            print("Opção inválida.")
''',
            tests='''import io, contextlib

entradas = iter(["1", "Comprar pão", "1", "  ", "1", "Estudar", "3", "1", "3", "9",
                 "2", "4", "2", "4", "abc", "x", "sair", "1"])
input = lambda p="": next(entradas)
lista = []
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    menu(lista)
texto = saida.getvalue()
assert "Tarefa adicionada!" in texto, "Na opção \\"1\\", mostre \\"Tarefa adicionada!\\" quando adicionar der certo."
assert "A tarefa não pode ficar vazia." in texto, "Na opção \\"1\\" com texto vazio, mostre \\"A tarefa não pode ficar vazia.\\""
assert "Tarefa concluída!" in texto, "Na opção \\"3\\" com um número válido, mostre \\"Tarefa concluída!\\""
assert "1. [x] Comprar pão" in texto, "A opção \\"2\\" deve listar as tarefas (a 1ª já concluída: \\"1. [x] Comprar pão\\")."
assert "Removida: Estudar" in texto, "Na opção \\"4\\", mostre \\"Removida: \\" seguido do texto da tarefa."
assert texto.count("Não achei essa tarefa.") == 2, "Números que não existem (no concluir e no remover) devem mostrar \\"Não achei essa tarefa.\\""
assert "Opção inválida." in texto, "Uma opção desconhecida (como \\"x\\") deve mostrar \\"Opção inválida.\\""
assert lista == [["Comprar pão", True]], "No fim, a lista deveria ter só [\\"Comprar pão\\", True]. Confira cada opção."
assert next(entradas) == "1", "Depois de \\"sair\\" o menu deve parar de perguntar (use break)."
''',
            dica="Use uma corrente de if/elif/else comparando opcao com \"sair\", \"1\", \"2\", \"3\" e \"4\"; o else final pega o resto. Apague o break provisório do fim.",
        ),
        # ---------------------------------------------------------------- 7
        dict(
            titulo="A main e o resumo final",
            explica=(
                "Por último, a função main: ela dá boas-vindas, cria a lista vazia, chama o menu e, quando a pessoa sai, mostra um resumo. "
                "Para o resumo, contamos quantas tarefas têm feita igual a True. "
                "No fim do arquivo vem o bloco if __name__ == \"__main__\": main(), que quer dizer \"se este arquivo foi aberto para rodar, comece pela main\"; "
                "quando ele é só importado (como nos testes), nada começa sozinho."
            ),
            tarefa=(
                "Crie main(): mostre \"Bem-vindo à sua lista de tarefas!\", crie tarefas = [], chame menu(tarefas), conte as feitas e mostre "
                "f\"Você concluiu {feitas} de {len(tarefas)} tarefa(s). Até logo!\". Termine com o bloco if __name__ == \"__main__\": main()."
            ),
            starter='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return 0


def menu(tarefas):
    while True:
        print()
        print("1 adicionar | 2 listar | 3 concluir | 4 remover | sair")
        opcao = input("Escolha: ").strip()
        if opcao == "sair":
            break
        elif opcao == "1":
            texto = input("Nova tarefa: ")
            if adicionar(tarefas, texto):
                print("Tarefa adicionada!")
            else:
                print("A tarefa não pode ficar vazia.")
        elif opcao == "2":
            listar(tarefas)
        elif opcao == "3":
            n = ler_numero(input("Número da tarefa: "))
            if concluir(tarefas, n):
                print("Tarefa concluída!")
            else:
                print("Não achei essa tarefa.")
        elif opcao == "4":
            n = ler_numero(input("Número da tarefa: "))
            removida = remover(tarefas, n)
            if removida is None:
                print("Não achei essa tarefa.")
            else:
                print(f"Removida: {removida}")
        else:
            print("Opção inválida.")


# TODO: crie def main(): que mostra "Bem-vindo à sua lista de tarefas!",
# TODO: cria tarefas = [], chama menu(tarefas),
# TODO: conta as tarefas feitas (tarefa[1] é True) e mostra
# TODO: f"Você concluiu {feitas} de {len(tarefas)} tarefa(s). Até logo!"

# TODO: no fim do arquivo:  if __name__ == "__main__":  e, dentro dele, main()
''',
            solucao='''# Lista de tarefas, construída passo a passo.
# Cada tarefa é uma lista [texto, feita], por exemplo ["Comprar pão", False].

def adicionar(tarefas, texto):
    texto = texto.strip()
    if texto == "":
        return False
    tarefas.append([texto, False])
    return True


def listar(tarefas):
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda.")
    numero = 1
    for tarefa in tarefas:
        if tarefa[1]:
            caixa = "[x]"
        else:
            caixa = "[ ]"
        print(f"{numero}. {caixa} {tarefa[0]}")
        numero = numero + 1


def concluir(tarefas, n):
    if n < 1 or n > len(tarefas):
        return False
    tarefas[n - 1][1] = True
    return True


def remover(tarefas, n):
    if n < 1 or n > len(tarefas):
        return None
    tirada = tarefas.pop(n - 1)
    return tirada[0]


def ler_numero(texto):
    texto = texto.strip()
    if texto.isdigit():
        return int(texto)
    return 0


def menu(tarefas):
    while True:
        print()
        print("1 adicionar | 2 listar | 3 concluir | 4 remover | sair")
        opcao = input("Escolha: ").strip()
        if opcao == "sair":
            break
        elif opcao == "1":
            texto = input("Nova tarefa: ")
            if adicionar(tarefas, texto):
                print("Tarefa adicionada!")
            else:
                print("A tarefa não pode ficar vazia.")
        elif opcao == "2":
            listar(tarefas)
        elif opcao == "3":
            n = ler_numero(input("Número da tarefa: "))
            if concluir(tarefas, n):
                print("Tarefa concluída!")
            else:
                print("Não achei essa tarefa.")
        elif opcao == "4":
            n = ler_numero(input("Número da tarefa: "))
            removida = remover(tarefas, n)
            if removida is None:
                print("Não achei essa tarefa.")
            else:
                print(f"Removida: {removida}")
        else:
            print("Opção inválida.")


def main():
    print("Bem-vindo à sua lista de tarefas!")
    tarefas = []
    menu(tarefas)
    feitas = 0
    for tarefa in tarefas:
        if tarefa[1]:
            feitas = feitas + 1
    print(f"Você concluiu {feitas} de {len(tarefas)} tarefa(s). Até logo!")


if __name__ == "__main__":
    main()
''',
            tests='''import io, contextlib

assert __stdout__ == "", "Nada deve rodar quando o arquivo é importado: chame main() só dentro do bloco if __name__ == \\"__main__\\":"

entradas = iter(["1", "Comprar pão", "1", "Estudar", "1", "Regar", "3", "2", "sair"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
texto = saida.getvalue()
assert "Bem-vindo à sua lista de tarefas!" in texto, "main() deve começar mostrando \\"Bem-vindo à sua lista de tarefas!\\""
assert "Tarefa adicionada!" in texto, "main() deve chamar menu(tarefas) para o menu funcionar."
assert "Você concluiu 1 de 3 tarefa(s). Até logo!" in texto, "Com 3 tarefas e 1 concluída, o resumo deveria ser \\"Você concluiu 1 de 3 tarefa(s). Até logo!\\""

entradas = iter(["sair"])
input = lambda p="": next(entradas)
saida = io.StringIO()
with contextlib.redirect_stdout(saida):
    main()
assert "Você concluiu 0 de 0 tarefa(s). Até logo!" in saida.getvalue(), "Saindo direto, o resumo deveria ser \\"Você concluiu 0 de 0 tarefa(s). Até logo!\\""
''',
            dica="Para contar as feitas, comece com feitas = 0 e percorra a lista com for, somando 1 quando tarefa[1] for True.",
        ),
    ],
)
