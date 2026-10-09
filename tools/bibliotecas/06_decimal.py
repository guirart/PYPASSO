from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_decimal", titulo="decimal e fractions",
               descricao="Contas exatas com dinheiro e frações: adeus 0.30000000000000004.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Por que 0.1 + 0.2 ≠ 0.3?",
      "O computador guarda números com vírgula (float) em binário, e alguns, como 0.1, não cabem certinho: sobra um errinho minúsculo. Para jogos tudo bem, mas para dinheiro não! A biblioteca decimal resolve isso: from decimal import Decimal e os números passam a ser exatos, do jeito que fazemos no papel.",
      'from decimal import Decimal\n\nprint(0.1 + 0.2)\nprint(0.1 + 0.2 == 0.3)\nprint(Decimal("0.1") + Decimal("0.2"))\nprint(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))',
      [OUT('print(0.1 + 0.2 == 0.3)', ["True", "0.3", "Erro"], "Com float, a soma dá 0.30000000000000004, que é diferente de 0.3."),
       TYPE('from decimal import Decimal\nprint(Decimal("0.1") * 3)', "Com Decimal a conta é exata, como no papel."),
       MC("Em qual situação o Decimal é mais importante?", "Calcular o saldo de uma conta bancária", ["Mover um personagem num jogo", "Medir a temperatura de um sensor", "Desenhar um gráfico"], "Com dinheiro, até um centavo perdido importa. Nos outros casos um errinho mínimo não faz diferença."),
       OUT('from decimal import Decimal\nprint(Decimal("19.90") * 3)', ["59.699999999999996", "59.7", "60"], "Decimal é exato e mantém as duas casas: 59.70.")]),
    # lição 2
    L("Decimal a partir de texto",
      "Crie o Decimal a partir de um texto, entre aspas: Decimal(\"0.1\"). Se você passar um float, Decimal(0.1), o errinho do float já vem junto! Números inteiros podem ir sem aspas. E não misture Decimal com float na mesma conta: o Python dá erro.",
      'from decimal import Decimal\n\nprint(Decimal("0.1"))\nprint(Decimal(0.1))\nprint(Decimal("2.50") + 1)',
      [OUT('from decimal import Decimal\nprint(Decimal("3.50") * 2)', ["7.0", "7", "3.503.50"], "Decimal mantém as casas decimais: 7.00."),
       MC('O que acontece com Decimal("10") + 0.5?', "Dá erro (TypeError)", ["Dá 10.5", "Dá 10", "Dá 10.50"], "Decimal não se mistura com float. Use Decimal(\"0.5\")."),
       FILL("Complete para criar o preço exato de R$ 4,99.", 'from decimal import Decimal\npreco = Decimal(___)\nprint(preco)', '"4.99"', ["4.99", '"4,99"', "4,99"], 'Use texto com ponto: "4.99". Sem aspas vira float; com vírgula o Decimal não entende.'),
       TYPE('from decimal import Decimal\nprint(Decimal("1.10") + Decimal("2.205"))', "A soma fica com o maior número de casas: 3.305.")]),
    # lição 3
    L("Centavos: quantize",
      "Para arredondar dinheiro em centavos, use quantize(Decimal(\"0.01\")): o 0.01 diz \"quero 2 casas\". Escolha o modo de arredondar com rounding=ROUND_HALF_UP, o arredondamento da escola (5 sobe). Sem ele, o padrão é o arredondamento bancário, que leva o 5 para o número par.",
      'from decimal import Decimal, ROUND_HALF_UP\n\nvalor = Decimal("2.675")\nprint(valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))\nprint(valor.quantize(Decimal("0.01")))\nprint(round(2.675, 2))',
      [OUT('from decimal import Decimal, ROUND_HALF_UP\nprint(Decimal("9.999").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))', ["9.99", "10", "9.999"], "9.999 arredonda para 10.00, mantendo duas casas."),
       TYPE('from decimal import Decimal, ROUND_HALF_UP\nprint(Decimal("12.345").quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))', "Decimal(\"0.1\") pede só uma casa decimal: 12.3 (o 4 não sobe)."),
       MC('Em quantize(Decimal("0.01")), o que o 0.01 indica?', "Quantas casas decimais o resultado terá", ["Quanto será somado ao valor", "O valor mínimo aceito", "A porcentagem de desconto"], "0.01 tem duas casas, então o resultado fica com duas casas."),
       CODE("Crie a função centavos(valor) que recebe um Decimal e DEVOLVE o valor arredondado para 2 casas, com ROUND_HALF_UP.",
            "from decimal import Decimal, ROUND_HALF_UP\n\ndef centavos(valor):\n    return valor\n",
            'from decimal import Decimal, ROUND_HALF_UP\n\ndef centavos(valor):\n    return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)',
            'from decimal import Decimal\nassert centavos(Decimal("2.675")) == Decimal("2.68"), "2.675 arredondado deve dar 2.68"\nassert str(centavos(Decimal("10"))) == "10.00", "10 deve virar 10.00, com duas casas"\nassert str(centavos(Decimal("0.125"))) == "0.13", "0.125 deve dar 0.13 (5 sobe)"',
            'return valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)')]),
    # lição 4
    L("Precisão: getcontext",
      "Em divisões que não acabam, como 1 / 7, o Decimal guarda 28 algarismos por padrão. Com getcontext().prec você muda essa precisão (a quantidade de algarismos significativos, não de casas decimais). A mudança vale para as contas seguintes, então volte ao 28 quando terminar.",
      'from decimal import Decimal, getcontext\n\nprint(Decimal(1) / Decimal(7))\ngetcontext().prec = 4\nprint(Decimal(1) / Decimal(7))\ngetcontext().prec = 28',
      [TYPE('from decimal import getcontext\nprint(getcontext().prec)', "A precisão padrão do Decimal é 28 algarismos."),
       OUT('from decimal import Decimal, getcontext\ngetcontext().prec = 3\nprint(Decimal(2) / Decimal(3))\ngetcontext().prec = 28', ["0.666", "0.67", "0.6666666666666666666666666667"], "3 algarismos significativos, com arredondamento: 0.667."),
       MC("getcontext().prec = 5 quer dizer…", "5 algarismos significativos nas contas", ["5 casas depois do ponto", "Números até 5", "5 contas por vez"], "prec conta algarismos significativos: 1/7 vira 0.14286."),
       ORDER("Monte o programa que mostra 10/3 com 6 algarismos e depois volta ao padrão.", ["from decimal import Decimal, getcontext", "getcontext().prec = 6", "print(Decimal(10) / Decimal(3))", "getcontext().prec = 28"], "Primeiro muda a precisão, faz a conta e depois volta ao padrão.")]),
    # lição 5
    L("Frações exatas: Fraction",
      "A biblioteca fractions guarda frações de verdade, como 1/3, sem virar 0.333... Use from fractions import Fraction e escreva Fraction(1, 3). Ela simplifica sozinha (6/8 vira 3/4) e é ótima para receitas, música e probabilidade. .numerator e .denominator mostram as partes.",
      'from fractions import Fraction\n\nprint(Fraction(1, 3) + Fraction(1, 6))\nprint(Fraction(6, 8))\nprint(Fraction(1, 3) * 3)\nprint(float(Fraction(1, 4)))',
      [OUT('from fractions import Fraction\nprint(Fraction(1, 2) + Fraction(1, 4))', ["2/6", "0.75", "1/6"], "1/2 é 2/4, e 2/4 + 1/4 = 3/4."),
       TYPE('from fractions import Fraction\nprint(Fraction(10, 4))', "Fraction simplifica sozinha: 10/4 vira 5/2."),
       FILL("A receita pede 3/4 de xícara de açúcar e você vai fazer metade. Complete a conta.", 'from fractions import Fraction\nacucar = Fraction(3, 4) * Fraction(1, ___)\nprint(acucar)', "2", ["4", "3", "1"], "Metade é vezes 1/2: 3/4 × 1/2 = 3/8."),
       MC("O que Fraction(3, 4).denominator devolve?", "4", ["3", "0.75", "3/4"], "O denominador é o número de baixo da fração.")]),
    # lição 6
    L("Desafio: dividindo a conta",
      "No restaurante: a conta mais 10% de serviço, dividida entre os amigos. Com Decimal a partir de texto e quantize com ROUND_HALF_UP, ninguém paga um centavo a mais ou a menos por erro de float.",
      'from decimal import Decimal, ROUND_HALF_UP\n\nconta = Decimal("150.00")\ncom_servico = conta * Decimal("1.10")\npor_pessoa = (com_servico / 4).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)\nprint(f"Total: R$ {com_servico}")\nprint(f"Cada um: R$ {por_pessoa}")',
      [OUT('from decimal import Decimal, ROUND_HALF_UP\nprint((Decimal("100.00") / 3).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))', ["33.3333", "33.34", "33"], "100 / 3 = 33.333..., arredondado para centavos: 33.33."),
       MC("Por que criamos Decimal(\"1.10\") e não Decimal(1.10) para os 10% de serviço?", "Porque o float 1.10 já carrega um errinho que o Decimal copiaria", ["Porque Decimal não aceita números com ponto", "Porque com aspas a conta fica mais rápida", "Tanto faz, os dois dão o mesmo valor"], "Decimal(1.10) vira 1.100000000000000088817841970012523233890533447265625."),
       ORDER("Monte o cálculo da gorjeta de 10% de uma conta de R$ 87,35.", ["from decimal import Decimal, ROUND_HALF_UP", 'conta = Decimal("87.35")', 'gorjeta = conta * Decimal("0.10")', 'print(gorjeta.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))'], "Import, valor, conta e só no fim o arredondamento para centavos."),
       CODE("Crie a função dividir_conta(total, pessoas) que recebe o total como TEXTO (ex.: \"150.00\"), soma 10% de serviço, divide pelo número de pessoas e DEVOLVE um Decimal arredondado em centavos com ROUND_HALF_UP.",
            "from decimal import Decimal, ROUND_HALF_UP\n\ndef dividir_conta(total, pessoas):\n    return float(total) * 1.1 / pessoas\n",
            'from decimal import Decimal, ROUND_HALF_UP\n\ndef dividir_conta(total, pessoas):\n    com_servico = Decimal(total) * Decimal("1.10")\n    return (com_servico / pessoas).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)',
            'from decimal import Decimal\nr = dividir_conta("150.00", 4)\nassert isinstance(r, Decimal), "A função deve devolver um Decimal"\nassert str(r) == "41.25", "150.00 + 10% dividido por 4 dá 41.25"\nassert str(dividir_conta("100.00", 3)) == "36.67", "100.00 + 10% dividido por 3 dá 36.67"\nassert str(dividir_conta("50", 2)) == "27.50", "50 + 10% dividido por 2 dá 27.50"',
            'Decimal(total) * Decimal("1.10"), divida por pessoas e termine com .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP).')]),
]

BUGS = r'''
@lib_decimal 2
from decimal import Decimal
total = Decimal(0.1) + Decimal(0.2)
print(total)  # esperado: 0.3
>>> total = Decimal("0.1") + Decimal("0.2")
!! Decimal(0.1) copia o errinho do float. Crie a partir de texto: Decimal("0.1").

@lib_decimal 2
import decimal
preco = Decimal("4.99")
print(preco)
>>> preco = decimal.Decimal("4.99")
!! Com import decimal, o Decimal fica dentro do módulo: decimal.Decimal. Ou use from decimal import Decimal.

@lib_decimal 2
from decimal import Decimal
preco = Decimal("10,50")
print(preco * 2)
>>> preco = Decimal("10.50")
!! O Decimal usa ponto, não vírgula: "10.50". Com vírgula dá InvalidOperation.

@lib_decimal 3
from decimal import Decimal
saldo = Decimal("10.00")
saldo = saldo + 0.5
print(saldo)
>>> saldo = saldo + Decimal("0.50")
!! Decimal não se mistura com float. Transforme o 0.5 em Decimal também.

@lib_decimal 3
from decimal import Decimal, ROUND_HALF_UP
valor = Decimal("2.665")
print(valor.quantize(Decimal("0.01")))  # esperado: 2.67
>>> print(valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))  # esperado: 2.67
!! Sem rounding, o 5 vai para o par (2.66). Para o arredondamento da escola, use ROUND_HALF_UP.

@lib_decimal 2
from fractions import Fraction
terco = Fraction(1 / 3)
print(terco * 3)  # esperado: 1
>>> terco = Fraction(1, 3)
!! 1 / 3 vira um float aproximado antes de chegar na Fraction. Passe numerador e denominador separados: Fraction(1, 3).
'''
