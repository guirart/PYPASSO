from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_math", titulo="math",
               descricao="Contas avançadas: arredondar, raízes, pi, logaritmos, combinações e geometria.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Arredondando: floor e ceil",
      "math é o módulo de matemática da biblioteca padrão: basta import math. math.floor arredonda para baixo, math.ceil para cima e math.trunc corta as casas decimais. Já o round (que nem precisa de import) vai para o inteiro mais próximo (no empate, .5, ele escolhe o par: round(4.5) dá 4). Serve para contar caixas, páginas, parcelas...",
      'import math\n\nprint(math.floor(4.7))\nprint(math.ceil(4.2))\nprint(math.trunc(-4.7))\nprint(round(4.5), round(5.5))',
      [OUT('import math\nprint(math.ceil(2.1))', ["2", "2.1", "3.0"], "ceil sobe para o próximo inteiro: 3."),
       OUT('import math\nprint(math.floor(-2.5))', ["-2", "-2.5", "2"], "floor vai para baixo na reta numérica. Abaixo de -2.5 vem -3."),
       MC("São 23 alunos e cada carro leva 4. Quantos carros? Qual conta resolve?", "math.ceil(23 / 4)", ["math.floor(23 / 4)", "round(23 / 4)", "math.trunc(23 / 4)"], "23 / 4 dá 5.75. Sobrar aluno não pode, então arredonda para cima: 6 carros."),
       TYPE('import math\nprint(math.trunc(9.99))', "trunc só joga fora a parte decimal.")]),
    # lição 2
    L("Raízes e potências",
      "math.sqrt(x) tira a raiz quadrada e devolve float. math.isqrt(x) devolve só a parte inteira da raiz. Para potências, use ** (2 ** 3 é 8) ou math.pow, que sempre devolve float. É útil para áreas, distâncias e para saber se um número é quadrado perfeito.",
      'import math\n\nprint(math.sqrt(16))\nprint(math.isqrt(20))\nprint(2 ** 10)\nprint(math.pow(2, 10))',
      [OUT('import math\nprint(math.isqrt(50))', ["7.0710678118654755", "8", "25"], "A raiz de 50 é 7.07..., e isqrt fica só com o inteiro: 7."),
       TYPE('import math\nprint(math.pow(3, 2))', "math.pow sempre devolve float."),
       FILL("Complete para calcular o lado de um quadrado com área 64.", 'import math\nlado = math.___(64)\nprint(lado)', "sqrt", ["pow", "root", "square"], "O lado é a raiz quadrada da área: sqrt."),
       CODE("Crie a função eh_quadrado(n) que devolve True se n for quadrado perfeito (como 9, 16, 25) e False se não for. Dica: math.isqrt(n) ** 2 == n.",
            "import math\n\ndef eh_quadrado(n):\n    return False\n\nprint(eh_quadrado(16))\n",
            'import math\n\ndef eh_quadrado(n):\n    return math.isqrt(n) ** 2 == n\n\nprint(eh_quadrado(16))',
            'assert eh_quadrado(16) is True, "16 é 4 x 4: deve dar True"\nassert eh_quadrado(15) is False, "15 não é quadrado perfeito"\nassert eh_quadrado(1) is True, "1 é 1 x 1"\nassert eh_quadrado(50) is False, "50 não é quadrado perfeito"',
            'return math.isqrt(n) ** 2 == n')]),
    # lição 3
    L("Constantes: pi, e, inf, nan",
      "O math guarda números famosos: math.pi (3.14159...), math.e (2.71828...), math.inf (infinito) e math.nan (não é um número). Como floats têm pequenos erros (0.1 + 0.2 não dá 0.3 exato), compare com math.isclose em vez de ==.",
      'import math\n\nraio = 2\nprint(round(math.pi * raio ** 2, 2))\nprint(0.1 + 0.2 == 0.3)\nprint(math.isclose(0.1 + 0.2, 0.3))\nprint(math.inf > 10 ** 100)',
      [OUT('import math\nprint(round(math.pi, 3))', ["3.14", "3.141", "3.1416"], "round com 3 casas: 3.142 (o 5 seguinte arredonda para cima)."),
       OUT('import math\nprint(math.isclose(0.1 * 3, 0.3))', ["False", "0.30000000000000004", "Erro"], "0.1 * 3 dá 0.30000000000000004, mas isclose aceita essa diferença minúscula: True."),
       MC("Você quer começar a busca pelo menor preço com um valor maior que qualquer preço. Qual usar?", "menor = math.inf", ["menor = math.nan", "menor = 0", "menor = math.e"], "Qualquer preço é menor que infinito, então o primeiro já substitui."),
       TYPE('import math\nprint(math.nan == math.nan)', "nan não é igual a nada, nem a ele mesmo.")]),
    # lição 4
    L("Logaritmos e exponenciais",
      "math.log10(x) diz quantas vezes se multiplica 10 para chegar em x; math.log2 faz o mesmo com 2, e math.log(x) usa a base e. math.exp(x) é o caminho inverso: e elevado a x. Servem para juros compostos, crescimento de seguidores e para saber quantos dígitos um número tem.",
      'import math\n\nprint(math.log10(1000))\nprint(math.log2(8))\nprint(math.log(math.e))\nprint(math.log(81, 3))\nprint(math.exp(0))',
      [OUT('import math\nprint(math.log10(100))', ["10.0", "100.0", "1.0"], "10 x 10 = 100: são 2 multiplicações, então 2.0."),
       TYPE('import math\nprint(math.log2(1024))', "Dobrando 1 dez vezes você chega em 1024."),
       MC("Uma pasta começa com 1 arquivo e dobra todo dia. Qual conta diz em quantos dias chega a 64?", "math.log2(64)", ["math.sqrt(64)", "math.log10(64)", "math.exp(64)"], "Dobrar é potência de 2, e log2 desfaz a potência: 6 dias."),
       FILL("Complete para calcular log de 125 na base 5.", 'import math\nprint(math.log(125, ___))', "5", ["125", "10", "math.e"], "O segundo argumento de math.log é a base.")]),
    # lição 5
    L("Contagem: fatorial e combinações",
      "math.factorial(n) multiplica 1 x 2 x ... x n: é de quantos jeitos n pessoas fazem fila. math.comb(n, k) conta grupos de k sem importar a ordem (times, cartelas de loteria); math.perm(n, k) conta quando a ordem importa (pódio). math.gcd e math.lcm dão o MDC e o MMC.",
      'import math\n\nprint(math.factorial(4))\nprint(math.comb(5, 2))\nprint(math.perm(5, 2))\nprint(math.gcd(12, 18))\nprint(math.lcm(4, 6))',
      [OUT('import math\nprint(math.factorial(5))', ["15", "25", "60"], "5 x 4 x 3 x 2 x 1 = 120."),
       MC("De quantos jeitos dá para escolher 2 sabores de pizza entre 6, sem importar a ordem?", "math.comb(6, 2)", ["math.perm(6, 2)", "math.factorial(6)", "math.lcm(6, 2)"], "A ordem não importa (calabresa e queijo é o mesmo que queijo e calabresa): comb. Dá 15."),
       TYPE('import math\nprint(math.perm(4, 3))', "Pódio de 3 lugares com 4 corredores: 4 x 3 x 2."),
       CODE("Ônibus A passa a cada 12 minutos e o B a cada 20. Os dois saíram juntos agora. Guarde em juntos_de_novo quantos minutos faltam para saírem juntos de novo (use math) e mostre com print.",
            "import math\njuntos_de_novo = 12 * 20\nprint(juntos_de_novo)\n",
            'import math\njuntos_de_novo = math.lcm(12, 20)\nprint(juntos_de_novo)',
            'assert juntos_de_novo == 60, "Eles se encontram no MMC de 12 e 20: 60 minutos"\nassert __stdout__.strip() == "60", "Mostre juntos_de_novo com print"',
            'juntos_de_novo = math.lcm(12, 20)')]),
    # lição 6
    L("Desafio: geometria",
      "Para triângulos e mapas: math.hypot(a, b) dá a hipotenusa, math.dist(p, q) a distância entre dois pontos, e math.sin/math.cos trabalham com radianos (use math.radians para converter graus, e math.degrees para voltar).",
      'import math\n\nprint(math.hypot(3, 4))\nprint(math.dist((0, 0), (6, 8)))\nprint(round(math.sin(math.radians(30)), 2))\nprint(math.degrees(math.pi))',
      [OUT('import math\nprint(math.hypot(5, 12))', ["17.0", "13", "169.0"], "raiz de 5² + 12² = raiz de 169 = 13.0."),
       OUT('import math\nprint(round(math.cos(math.radians(60)), 2))', ["0.87", "60.0", "-0.95"], "cos de 60 graus é 0.5. Sem radians, o Python acharia que 60 está em radianos."),
       ORDER("Monte o programa que calcula a distância entre a casa (1, 2) e a escola (4, 6).", ["import math", "casa = (1, 2)", "escola = (4, 6)", "print(math.dist(casa, escola))"], "Import primeiro, depois os pontos, depois a conta. Dá 5.0."),
       CODE("Crie a função area_pizza(diametro) que devolve a área da pizza (pi x raio²) arredondada para 1 casa. Use math.pi.",
            "import math\n\ndef area_pizza(diametro):\n    return 3 * diametro\n\nprint(area_pizza(30))\n",
            'import math\n\ndef area_pizza(diametro):\n    raio = diametro / 2\n    return round(math.pi * raio ** 2, 1)\n\nprint(area_pizza(30))',
            'assert area_pizza(30) == 706.9, "Pizza de 30 cm: raio 15, área 706.9"\nassert area_pizza(2) == 3.1, "Diâmetro 2: raio 1, área 3.1"\nassert area_pizza(0) == 0, "Diâmetro 0 dá área 0"',
            'raio = diametro / 2\nreturn round(math.pi * raio ** 2, 1)')]),
]

BUGS = r'''
@lib_math 2
import math
print(math.sqroot(16))
>>> print(math.sqrt(16))
!! A raiz quadrada se chama sqrt.

@lib_math 3
import math
alunos = 23
print(math.floor(alunos / 4))  # esperado: 6
>>> print(math.ceil(alunos / 4))  # esperado: 6
!! Para caber todo mundo, arredonde para cima com ceil.

@lib_math 2
import math
print(round(math.PI, 2))
>>> print(round(math.pi, 2))
!! A constante é math.pi, com letras minúsculas.

@lib_math 2
import math
print(math.factorial(4.0))
>>> print(math.factorial(4))
!! factorial só aceita inteiros: use 4, não 4.0.

@lib_math 2
import math
print(round(math.sin(30), 2))  # esperado: 0.5
>>> print(round(math.sin(math.radians(30)), 2))  # esperado: 0.5
!! sin trabalha em radianos. Converta os graus com math.radians.

@lib_math 2
import math
print(math.comb(2, 6))  # esperado: 15
>>> print(math.comb(6, 2))  # esperado: 15
!! Em comb, primeiro vem o total (6 sabores), depois quantos escolher (2).
'''
