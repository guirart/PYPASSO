def c(s):
    return s.strip("\n") + "\n"


# ---------------------------------------------------------------- passo 1
S1 = c(r'''
class Personagem:
    def __init__(self, nome, vida, ataque):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

    def esta_vivo(self):
        return self.vida > 0
''')

ST1 = c(r'''
class Personagem:
    def __init__(self, nome, vida, ataque):
        # TODO: guarde nome, vida e ataque em self
        pass

    def esta_vivo(self):
        # TODO: devolva True se a vida for maior que 0
        return None
''')

T1 = r'''
p = Personagem("Lia", 30, 5)
assert getattr(p, "nome", None) == "Lia", "Guarde o nome em self.nome."
assert getattr(p, "vida", None) == 30, "Guarde a vida em self.vida."
assert getattr(p, "ataque", None) == 5, "Guarde o ataque em self.ataque."
assert p.esta_vivo() is True, "Com 30 de vida, esta_vivo() deve devolver True."
p.vida = 0
assert p.esta_vivo() is False, "Com 0 de vida, esta_vivo() deve devolver False."
'''

# ---------------------------------------------------------------- passo 2
PERSONAGEM = r'''
class Personagem:
    def __init__(self, nome, vida, ataque):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

    def __str__(self):
        return f"{self.nome} (vida: {self.vida})"

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

    def atacar(self, alvo):
        alvo.receber_dano(self.ataque)
        return self.ataque
'''

S2 = c(PERSONAGEM)

ST2 = c(r'''
class Personagem:
    def __init__(self, nome, vida, ataque):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

    def __str__(self):
        # TODO: devolva um texto como "Lia (vida: 30)"
        return ""

    def esta_vivo(self):
        return self.vida > 0

    def receber_dano(self, dano):
        # TODO: tire o dano da vida, sem deixar a vida ficar negativa
        pass

    def atacar(self, alvo):
        # TODO: faça o alvo receber_dano(self.ataque) e devolva o dano causado
        return None
''')

T2 = r'''
a = Personagem("Lia", 30, 5)
b = Personagem("Rato", 8, 2)
assert str(a) == "Lia (vida: 30)", f"str(personagem) deveria dar 'Lia (vida: 30)', veio {str(a)!r}."
b.receber_dano(3)
assert b.vida == 5, f"Com 8 de vida e 3 de dano, sobram 5. Veio {b.vida}."
b.receber_dano(20)
assert b.vida == 0, f"A vida não pode ficar negativa: depois de um dano grande ela deve ser 0. Veio {b.vida}."
c = Personagem("Gato", 10, 1)
r = a.atacar(c)
assert r == 5, f"atacar deve devolver o dano causado (o ataque de quem bate). Veio {r!r}."
assert c.vida == 5, f"Lia tem ataque 5: o Gato devia ficar com 10 - 5 = 5 de vida. Ficou com {c.vida}."
assert a.vida == 30, "Quem ataca não perde vida."
'''

# ---------------------------------------------------------------- passo 3
HEROI = r'''


class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, pocoes=3):
        super().__init__(nome, vida, ataque)
        self.vida_max = vida
        self.pocoes = pocoes

    def __str__(self):
        return super().__str__() + f" | poções: {self.pocoes}"

    def beber_pocao(self):
        if self.pocoes == 0:
            return False
        self.pocoes -= 1
        self.vida += 10
        if self.vida > self.vida_max:
            self.vida = self.vida_max
        return True
'''

S3 = S2 + c(HEROI)

ST3 = S2 + c(r'''


class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, pocoes=3):
        # TODO: chame super().__init__(nome, vida, ataque)
        # TODO: guarde a vida inicial em self.vida_max e as poções em self.pocoes
        pass

    def __str__(self):
        # TODO: use super().__str__() e acrescente " | poções: 3" (com o número de poções)
        return ""

    def beber_pocao(self):
        # TODO: sem poções, devolva False
        # TODO: senão, gaste 1 poção, some 10 na vida (sem passar de vida_max) e devolva True
        return None
''')

T3 = r'''
h = Heroi("Lia", 30, 5)
assert getattr(h, "nome", None) == "Lia" and getattr(h, "vida", None) == 30, "Chame super().__init__(nome, vida, ataque) para guardar nome, vida e ataque."
assert getattr(h, "pocoes", None) == 3, "Sem dizer nada, o herói começa com 3 poções (pocoes=3)."
assert getattr(h, "vida_max", None) == 30, "Guarde a vida inicial em self.vida_max."
assert isinstance(h, Personagem), "Heroi precisa herdar de Personagem: class Heroi(Personagem):"
assert str(h) == "Lia (vida: 30) | poções: 3", f"str(heroi) deveria dar 'Lia (vida: 30) | poções: 3', veio {str(h)!r}."
h.vida = 12
assert h.beber_pocao() is True, "Com poções sobrando, beber_pocao() devolve True."
assert h.vida == 22 and h.pocoes == 2, f"A poção cura 10 e gasta 1: esperava vida 22 e 2 poções, veio vida {h.vida} e {h.pocoes} poções."
h.beber_pocao()
assert h.vida == 30, f"A vida não pode passar de vida_max (30). Veio {h.vida}."
h.beber_pocao()
assert h.pocoes == 0, "Depois de 3 poções, não sobra nenhuma."
assert h.beber_pocao() is False, "Sem poções, beber_pocao() devolve False."
assert Heroi("Zé", 20, 4, 1).pocoes == 1, "Heroi('Zé', 20, 4, 1) deve começar com 1 poção."
'''

# ---------------------------------------------------------------- passo 4
HEROI4 = r'''


class Heroi(Personagem):
    def __init__(self, nome, vida, ataque, pocoes=3):
        super().__init__(nome, vida, ataque)
        self.vida_max = vida
        self.pocoes = pocoes
        self.especial = True

    def __str__(self):
        return super().__str__() + f" | poções: {self.pocoes}"

    def beber_pocao(self):
        if self.pocoes == 0:
            return False
        self.pocoes -= 1
        self.vida += 10
        if self.vida > self.vida_max:
            self.vida = self.vida_max
        return True
'''

ESPECIAL = r'''
    def golpe_especial(self, alvo):
        if not self.especial:
            return 0
        self.especial = False
        dano = self.ataque * 2
        alvo.receber_dano(dano)
        return dano
'''

MONSTRO = r'''


class Monstro(Personagem):
    def __init__(self, nome, vida, ataque, recompensa=5):
        super().__init__(nome, vida, ataque)
        self.recompensa = recompensa

    def __str__(self):
        return "👹 " + super().__str__()
'''

S4 = S2 + c(HEROI4 + "\n" + ESPECIAL + MONSTRO)

ST4 = S2 + c(HEROI4 + r'''
    def golpe_especial(self, alvo):
        # TODO: se self.especial for False, devolva 0 (já foi usado)
        # TODO: senão, marque self.especial = False, cause o dobro do ataque no alvo e devolva o dano
        return None


class Monstro(Personagem):
    def __init__(self, nome, vida, ataque, recompensa=5):
        # TODO: chame super().__init__ e guarde a recompensa em self.recompensa
        pass

    def __str__(self):
        # TODO: devolva "👹 " + o texto do __str__ de Personagem
        return ""
''')

T4 = r'''
h = Heroi("Lia", 30, 5)
m = Monstro("Goblin", 25, 4, 10)
assert getattr(h, "especial", None) is True, "O herói começa com o golpe especial disponível: self.especial = True."
r = h.golpe_especial(m)
assert r == 10, f"O golpe especial causa o dobro do ataque (5 * 2 = 10). Veio {r!r}."
assert m.vida == 15, f"O Goblin tinha 25 de vida e levou 10: devia ficar com 15. Ficou com {m.vida}."
assert h.golpe_especial(m) == 0, "O golpe especial só pode ser usado uma vez: na segunda vez devolva 0."
assert m.vida == 15, "Quando o golpe especial já foi usado, o monstro não pode levar dano."
assert isinstance(m, Personagem), "Monstro precisa herdar de Personagem: class Monstro(Personagem):"
assert getattr(m, "recompensa", None) == 10, "Guarde a recompensa em self.recompensa."
assert Monstro("Slime", 10, 2).recompensa == 5, "Sem dizer nada, a recompensa é 5."
assert str(m) == "👹 Goblin (vida: 15)", f"str(monstro) deveria dar '👹 Goblin (vida: 15)', veio {str(m)!r}."
'''

# ---------------------------------------------------------------- passo 5
LUTAR = r'''


def lutar(heroi, monstro, escolhas):
    for escolha in escolhas:
        if escolha == "1":
            dano = heroi.atacar(monstro)
            print(f"{heroi.nome} ataca e causa {dano} de dano!")
        elif escolha == "2":
            dano = heroi.golpe_especial(monstro)
            if dano == 0:
                print("Você já usou o golpe especial!")
                continue
            print(f"GOLPE ESPECIAL! {dano} de dano!")
        elif escolha == "3":
            if not heroi.beber_pocao():
                print("Acabaram as poções!")
                continue
            print(f"Glub glub... {heroi.nome} agora tem {heroi.vida} de vida.")
        elif escolha == "4":
            print(f"{heroi.nome} fugiu!")
            return "fugiu"
        else:
            print("Opção inválida.")
            continue
        if not monstro.esta_vivo():
            print(f"{monstro.nome} foi derrotado!")
            return "venceu"
        dano = monstro.atacar(heroi)
        print(f"{monstro.nome} ataca e causa {dano} de dano!")
        if not heroi.esta_vivo():
            print(f"{heroi.nome} caiu...")
            return "perdeu"
    return "continua"
'''

S5 = S4 + c(LUTAR)

ST5 = S4 + c(r'''


def lutar(heroi, monstro, escolhas):
    for escolha in escolhas:
        # TODO: "1" -> heroi.atacar(monstro)
        # TODO: "2" -> heroi.golpe_especial(monstro); se der 0, avise e use continue
        # TODO: "3" -> heroi.beber_pocao(); se der False, avise e use continue
        # TODO: "4" -> mostre que fugiu e devolva "fugiu"
        # TODO: outra coisa -> "Opção inválida." e continue
        # TODO: se o monstro não está vivo, devolva "venceu"
        # TODO: senão, o monstro ataca o herói; se o herói não está vivo, devolva "perdeu"
        pass
    return None
''')

T5 = r'''
import io, contextlib

def _luta(heroi, monstro, escolhas):
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        r = lutar(heroi, monstro, escolhas)
    return r, saida.getvalue()

h = Heroi("Lia", 30, 5)
m = Monstro("Slime", 12, 3)
r, txt = _luta(h, m, ["1", "1", "1"])
assert r == "venceu", f"Lia (ataque 5) derrota o Slime (vida 12) em 3 ataques: devolva 'venceu'. Veio {r!r}."
assert h.vida == 24, f"O Slime atacou 2 vezes (3 de dano cada), então Lia fica com 24. Ficou com {h.vida}. O monstro não ataca depois de derrotado."

r, txt = _luta(Heroi("Lia", 30, 5), Monstro("Ogro", 50, 3), ["1"])
assert r == "continua", f"Se as escolhas acabam e ninguém caiu, devolva 'continua'. Veio {r!r}."

r, txt = _luta(Heroi("Lia", 30, 5), Monstro("Ogro", 50, 3), ["4", "1"])
assert r == "fugiu", "A escolha '4' foge na hora: devolva 'fugiu'."

r, txt = _luta(Heroi("Zé", 5, 1), Monstro("Dragão", 100, 10), ["1"])
assert r == "perdeu", "Se o herói fica sem vida, devolva 'perdeu'."

h = Heroi("Lia", 30, 5)
m = Monstro("Ogro", 50, 3)
r, txt = _luta(h, m, ["2", "2", "9"])
assert m.vida == 40, f"O golpe especial (10 de dano) só funciona uma vez: o Ogro devia ficar com 40. Ficou com {m.vida}."
assert h.vida == 27, "Quando a escolha não funciona (especial repetido ou opção inválida), o monstro não ataca: use continue."
assert "inválida" in txt, "Para uma opção que não existe, mostre 'Opção inválida.'."

h = Heroi("Lia", 30, 5, 1)
h.vida = 10
r, txt = _luta(h, Monstro("Ogro", 50, 3), ["3", "3"])
assert h.pocoes == 0 and h.vida == 17, f"Bebeu 1 poção (10 -> 20), levou 3 de dano (17) e depois não tinha mais poção. Veio vida {h.vida}."
'''

# ---------------------------------------------------------------- passo 6
MAIN = r'''


def main():
    print("=== AVENTURA RPG ===")
    nome = input("Qual é o nome do herói? ")
    heroi = Heroi(nome, 40, 6)
    monstros = [Monstro("Slime", 15, 3, 5), Monstro("Goblin", 25, 5, 10), Monstro("Dragãozinho", 35, 7, 20)]
    random.shuffle(monstros)
    ouro = 0
    for monstro in monstros:
        print(f"\nUm {monstro.nome} apareceu!")
        resultado = "continua"
        while resultado == "continua":
            print(heroi)
            print(monstro)
            escolha = input("1-atacar 2-especial 3-poção 4-fugir: ")
            resultado = lutar(heroi, monstro, [escolha])
        if resultado == "perdeu":
            print("Fim de jogo... tente de novo!")
            return
        if resultado == "venceu":
            ouro += monstro.recompensa
            print(f"Você ganhou {monstro.recompensa} moedas!")
    print(f"Aventura concluída! {heroi.nome} juntou {ouro} moedas.")


if __name__ == "__main__":
    main()
'''

S6 = "import random\n\n" + S5 + c(MAIN)

ST6 = "import random\n\n" + S5 + c(r'''


def main():
    print("=== AVENTURA RPG ===")
    # TODO: pergunte o nome com input() e crie heroi = Heroi(nome, 40, 6)
    # TODO: crie uma lista com 3 monstros e embaralhe com random.shuffle
    # TODO: para cada monstro: enquanto o resultado for "continua", mostre heroi e monstro,
    # TODO:   peça a escolha com input() e chame lutar(heroi, monstro, [escolha])
    # TODO: se perdeu, mostre "Fim de jogo..." e pare com return; se venceu, some a recompensa em ouro
    # TODO: no fim, mostre quantas moedas o herói juntou
    pass


if __name__ == "__main__":
    main()
''')

T6 = r'''
import io, contextlib

def _joga(respostas):
    global input
    entradas = iter(respostas)
    input = lambda p="": next(entradas)
    saida = io.StringIO()
    with contextlib.redirect_stdout(saida):
        main()
    return saida.getvalue()

txt = _joga(["Lia"] + ["1"] * 60)
assert "Lia" in txt, "Crie o herói com o nome digitado e mostre ele (print(heroi)) a cada rodada."
assert "apareceu" in txt or "👹" in txt, "Mostre o monstro de cada luta."
assert "moedas" in txt or "Fim de jogo" in txt, "No fim, mostre as moedas juntadas (ou 'Fim de jogo...' se perder)."

txt = _joga(["Zé"] + ["4"] * 3)
assert "fugiu" in txt, "Com a escolha '4' o herói foge de cada monstro."
assert "0 moedas" in txt, "Fugindo de todos, o herói termina com 0 moedas."

txt = _joga(["Bia"] + ["3"] * 3 + ["9"] * 5 + ["1"] * 60)
assert "Fim de jogo" in txt or "moedas" in txt, "O laço precisa continuar enquanto o resultado for 'continua'."
'''

PROJETO = dict(
    id="rpg",
    titulo="Aventura RPG de texto",
    emoji="⚔️",
    resumo="Crie um herói, enfrente monstros em batalhas por turnos e use golpes especiais e poções para sobreviver.",
    requer="u11l1",
    demo_entrada="\n".join(["Lia", "2", "3"] + ["1"] * 40),
    passos=[
        dict(
            titulo="A classe Personagem",
            explica="Num RPG, herói e monstros têm coisas em comum: nome, vida e força de ataque. Por isso começamos com uma "
                    "classe Personagem, o molde de todos eles. O __init__ guarda os dados em self, e o método esta_vivo "
                    "responde se o personagem ainda está de pé.",
            tarefa="Complete o __init__ guardando nome, vida e ataque em self, e faça esta_vivo() devolver True quando a vida for maior que 0.",
            starter=ST1, solucao=S1, tests=T1,
            dica="self.nome = nome guarda o nome dentro do objeto. Faça igual para vida e ataque.",
        ),
        dict(
            titulo="Bater e apanhar",
            explica="Agora os personagens vão se enfrentar! receber_dano tira vida, mas sem deixar ficar negativa. atacar faz o "
                    "alvo receber o dano e devolve quanto foi, para podermos mostrar na tela. E o __str__ decide o que aparece "
                    "quando fazemos print(personagem).",
            tarefa="Complete __str__ (formato 'Lia (vida: 30)'), receber_dano e atacar.",
            starter=ST2, solucao=S2, tests=T2,
            dica="Em atacar, o alvo é outro Personagem, então ele também tem o método receber_dano: alvo.receber_dano(self.ataque).",
        ),
        dict(
            titulo="O herói e suas poções",
            explica="O herói é um Personagem com algo a mais: poções de cura. Com herança, class Heroi(Personagem), ele ganha "
                    "tudo da classe mãe, e o super().__init__ aproveita o __init__ dela. Guardamos também a vida inicial, "
                    "para a poção não curar além do máximo.",
            tarefa="Complete Heroi: o __init__ com super(), o __str__ que acrescenta as poções e beber_pocao (cura 10, gasta 1 poção).",
            starter=ST3, solucao=S3, tests=T3,
            dica="No __str__, super().__str__() devolve 'Lia (vida: 30)'. É só somar o pedaço das poções com +.",
        ),
        dict(
            titulo="Golpe especial e monstros",
            explica="Todo herói merece um golpe especial: ele causa o dobro do dano, mas só pode ser usado uma vez, então "
                    "guardamos um True/False em self.especial. Do outro lado, criamos a classe Monstro, que também herda de "
                    "Personagem e guarda quantas moedas ele vale.",
            tarefa="Complete golpe_especial no Heroi e a classe Monstro (com recompensa e um __str__ que começa com '👹 ').",
            starter=ST4, solucao=S4, tests=T4,
            dica="Em golpe_especial, confira self.especial primeiro. Se ainda pode usar, troque para False antes de devolver o dano.",
        ),
        dict(
            titulo="A batalha por turnos",
            explica="A função lutar recebe uma lista de escolhas e executa um turno para cada uma: o herói age e, se o "
                    "monstro sobreviver, ele contra-ataca. Assim dá para testar uma luta inteira sem sorteio e sem input(). "
                    "No jogo de verdade, vamos mandar uma escolha por vez, a que a pessoa digitou.",
            tarefa="Complete lutar(heroi, monstro, escolhas) para devolver 'venceu', 'perdeu', 'fugiu' ou, se as escolhas acabarem, 'continua'.",
            starter=ST5, solucao=S5, tests=T5,
            dica="O continue pula o contra-ataque do monstro quando a escolha não deu certo. O return 'continua' fica fora do for, no fim.",
        ),
        dict(
            titulo="A aventura completa",
            explica="Agora o main monta a aventura: cria o herói, embaralha os monstros com random.shuffle e chama lutar com "
                    "uma escolha de cada vez, até a luta acabar. O bloco if __name__ == \"__main__\": no fim quer dizer 'rode "
                    "main() só quando este arquivo for o programa principal': nos testes ele não roda, mas roda quando você "
                    "toca em Jogar no editor.",
            tarefa="Complete main() seguindo os TODOs: um while repete a luta enquanto o resultado for 'continua'.",
            starter=ST6, solucao=S6, tests=T6,
            dica="Comece com resultado = 'continua' antes do while, e dentro dele faça resultado = lutar(heroi, monstro, [escolha]).",
        ),
    ],
)
