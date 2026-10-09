from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_datetime", titulo="datetime",
               descricao="Datas e horas: prazos, aniversários, contagem de dias e o formato dd/mm/aaaa.",
               externa=False, grupo="Biblioteca padrão")

LICOES = [
    # lição 1
    L("Criando datas: date",
      "A biblioteca datetime cuida de datas e horas: vencimento de boleto, aniversário, prazo de entrega. Para uma data, use from datetime import date e escreva date(ano, mês, dia). Depois é só ler .year, .month e .day; .weekday() diz o dia da semana, contando 0 para segunda até 6 para domingo.",
      'from datetime import date\n\nniver = date(2026, 3, 15)\nprint(niver)\nprint(niver.year, niver.month, niver.day)\nprint(niver.weekday())',
      [OUT('from datetime import date\nd = date(2026, 7, 4)\nprint(d.month)', ["4", "2026", "julho"], ".month devolve o número do mês: 7."),
       TYPE('from datetime import date\nprint(date(2026, 1, 5))', "Ao imprimir uma data, o Python usa o formato ano-mês-dia, com dois dígitos no mês e no dia."),
       MC("Se d.weekday() devolve 0, que dia da semana é?", "Segunda-feira", ["Domingo", "Sábado", "Não existe dia 0"], "weekday conta a partir de segunda: 0 = segunda, 6 = domingo."),
       FILL("Complete para criar a data do Natal de 2026.", 'from datetime import date\nnatal = ___(2026, 12, 25)\nprint(natal)', "date", ["Date", "data", "day"], "A classe se chama date, tudo minúsculo.")]),
    # lição 2
    L("Data com hora: datetime e time",
      "Quando o horário importa (consulta médica, sessão de cinema), use datetime(ano, mês, dia, hora, minuto). Ele tem .hour e .minute, e .date() separa só a data. Para guardar só um horário, sem dia, existe time(hora, minuto).",
      'from datetime import datetime, time\n\nconsulta = datetime(2026, 3, 15, 14, 30)\nprint(consulta)\nprint(consulta.hour, consulta.minute)\nprint(consulta.date())\nprint(time(8, 5))',
      [OUT('from datetime import datetime\nfilme = datetime(2026, 5, 2, 21, 10)\nprint(filme.hour)', ["10", "2", "21:10"], ".hour devolve só a hora: 21."),
       TYPE('from datetime import time\nprint(time(7, 45))', "time mostra hora:minuto:segundo, com os segundos zerados."),
       OUT('from datetime import datetime\nd = datetime(2026, 8, 1, 9, 0)\nprint(d.date())', ["2026-08-01 09:00:00", "09:00:00", "01/08/2026"], ".date() descarta o horário e fica só com a data."),
       MC("Qual escolha combina com o horário de abertura de uma loja, que é o mesmo todo dia?", "time(9, 0)", ["date(9, 0)", "datetime(9, 0)", "timedelta(9, 0)"], "Um horário sem dia específico é um time.")]),
    # lição 3
    L("Somando dias: timedelta",
      "timedelta representa uma duração: dias, horas, minutos. Some um timedelta a uma data para descobrir prazos (\"30 dias depois da compra\"). E subtraindo uma data da outra você ganha um timedelta; o .days dá quantos dias há entre elas.",
      'from datetime import date, timedelta\n\ncompra = date(2026, 3, 15)\nprint(compra + timedelta(days=20))\n\nnatal = date(2026, 12, 25)\ninicio = date(2026, 12, 1)\nfalta = natal - inicio\nprint(falta.days)',
      [OUT('from datetime import date, timedelta\nprint(date(2026, 2, 28) + timedelta(days=1))', ["2026-02-29", "2026-02-28", "2026-03-00"], "2026 não é bissexto: depois de 28 de fevereiro vem 1º de março."),
       TYPE('from datetime import date\nprint((date(2026, 1, 31) - date(2026, 1, 1)).days)', "Do dia 1 ao dia 31 são 30 dias de diferença."),
       MC("O que date(2026, 5, 10) - date(2026, 5, 1) devolve?", "Um timedelta de 9 dias", ["O número 9", "A data 2026-00-09", "Um erro, não dá para subtrair datas"], "Diferença de datas é um timedelta; para ter o número, use .days."),
       CODE("Uma loja dá 7 dias para devolver um produto. Usando timedelta, guarde em prazo a data final para a compra feita em compra e mostre-a.",
            "from datetime import date, timedelta\n\ncompra = date(2026, 4, 28)\nprazo = compra\n",
            "from datetime import date, timedelta\n\ncompra = date(2026, 4, 28)\nprazo = compra + timedelta(days=7)\nprint(prazo)",
            'from datetime import date\nassert prazo == date(2026, 5, 5), "7 dias depois de 28/04/2026 é 05/05/2026"\nassert "2026-05-05" in __stdout__, "Mostre o prazo com print"',
            "prazo = compra + timedelta(days=7) já passa para o mês seguinte sozinho.")]),
    # lição 4
    L("Formato brasileiro: strftime",
      "Aqui no Brasil escrevemos 15/03/2026, não 2026-03-15. O método strftime transforma a data em texto do jeito que você quiser, usando códigos: %d é o dia, %m o mês, %Y o ano com 4 dígitos, %H a hora e %M os minutos.",
      'from datetime import date, datetime\n\nd = date(2026, 3, 15)\nprint(d.strftime("%d/%m/%Y"))\n\nconsulta = datetime(2026, 3, 15, 14, 30)\nprint(consulta.strftime("%d/%m/%Y às %H:%M"))',
      [OUT('from datetime import date\nprint(date(2026, 7, 4).strftime("%d/%m/%Y"))', ["07/04/2026", "2026/07/04", "4/7/2026"], "%d é o dia (04), %m o mês (07), com zero na frente."),
       TYPE('from datetime import date\nprint(date(2026, 11, 9).strftime("%d-%m-%y"))', "%y minúsculo mostra só os dois últimos dígitos do ano."),
       FILL("Complete para mostrar 25/12/2026.", 'from datetime import date\nprint(date(2026, 12, 25).strftime("%d/%m/___"))', "%Y", ["%y", "%A", "%M"], "%Y maiúsculo é o ano com 4 dígitos. %M seria minutos!"),
       CODE("Crie a função data_br(d) que DEVOLVE o texto da data no formato dia/mês/ano, por exemplo 05/01/2026.",
            "from datetime import date\n\ndef data_br(d):\n    return str(d)\n",
            'from datetime import date\n\ndef data_br(d):\n    return d.strftime("%d/%m/%Y")',
            'from datetime import date\nassert data_br(date(2026, 1, 5)) == "05/01/2026", "data_br(date(2026, 1, 5)) deve ser 05/01/2026"\nassert data_br(date(2026, 12, 25)) == "25/12/2026", "data_br(date(2026, 12, 25)) deve ser 25/12/2026"',
            'return d.strftime("%d/%m/%Y")')]),
    # lição 5
    L("Lendo texto: strptime",
      "O caminho contrário: quando a data chega como texto (digitada num formulário ou numa planilha), datetime.strptime(texto, formato) transforma em data de verdade. O formato precisa bater com o texto, usando os mesmos códigos do strftime.",
      'from datetime import datetime\n\ntexto = "25/12/2026"\nd = datetime.strptime(texto, "%d/%m/%Y")\nprint(d)\nprint(d.date())\nprint(d.month)',
      [OUT('from datetime import datetime\nd = datetime.strptime("03/08/2026", "%d/%m/%Y")\nprint(d.month)', ["3", "2026", "03"], "No formato brasileiro, o segundo número é o mês: 8."),
       MC('O que acontece com datetime.strptime("2026-12-25", "%d/%m/%Y")?', "Dá erro (ValueError), porque o texto não segue o formato", ["Devolve 25/12/2026", "Devolve None", "Troca o formato sozinho"], "O texto usa hífens e começa pelo ano; o formato pede barras e começa pelo dia."),
       TYPE('from datetime import datetime\nd = datetime.strptime("10/02/2026", "%d/%m/%Y")\nprint(d.year + 1)', "Depois de convertido, o ano vira número e dá para fazer conta."),
       ORDER("Monte o programa que lê a data digitada e mostra o dia.", ["from datetime import datetime", 'texto = "18/09/2026"', 'd = datetime.strptime(texto, "%d/%m/%Y")', "print(d.day)"], "Import, o texto, a conversão com strptime e só então o uso.")]),
    # lição 6
    L("Desafio: quantos dias faltam?",
      "Juntando tudo: ler a data em texto (strptime), subtrair (timedelta) e mostrar no formato brasileiro (strftime). Nos exercícios usamos sempre uma data fixa como \"hoje\", para o resultado não mudar. No seu programa de verdade, date.today() dá a data do dia.",
      'from datetime import date, datetime\n\nhoje = date(2026, 10, 7)\nferias = datetime.strptime("18/12/2026", "%d/%m/%Y").date()\nfalta = (ferias - hoje).days\nprint(f"Faltam {falta} dias para {ferias.strftime(\'%d/%m/%Y\')}")',
      [OUT('from datetime import date\nprint((date(2026, 3, 1) - date(2026, 2, 1)).days)', ["30", "31", "1"], "Fevereiro de 2026 tem 28 dias."),
       MC("Por que nos exercícios não usamos date.today()?", "Porque o resultado mudaria a cada dia que o programa rodasse", ["Porque date.today() não existe", "Porque date.today() só funciona no Windows", "Porque date.today() devolve um texto"], "Com uma data fixa, a resposta certa é sempre a mesma."),
       FILL("Complete para descobrir quantos dias faltam para o aniversário.", 'from datetime import date\nhoje = date(2026, 10, 7)\nniver = date(2026, 11, 2)\nprint((niver - hoje).___)', "days", ["day", "dias", "total"], ".days é o número de dias de um timedelta."),
       CODE("Crie a função idade(nascimento, hoje) que DEVOLVE a idade em anos completos. As duas são date. Cuidado: se o aniversário deste ano ainda não chegou, a pessoa ainda não fez aniversário!",
            "from datetime import date\n\ndef idade(nascimento, hoje):\n    return hoje.year - nascimento.year\n",
            "from datetime import date\n\ndef idade(nascimento, hoje):\n    anos = hoje.year - nascimento.year\n    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):\n        anos -= 1\n    return anos",
            'from datetime import date\nassert idade(date(2000, 5, 10), date(2026, 10, 7)) == 26, "Nascido em 10/05/2000, em 07/10/2026 já tem 26 anos"\nassert idade(date(2000, 12, 25), date(2026, 10, 7)) == 25, "Nascido em 25/12/2000, em 07/10/2026 ainda tem 25 anos"\nassert idade(date(2010, 10, 7), date(2026, 10, 7)) == 16, "No dia do aniversário a idade já conta"',
            "Subtraia os anos e, se (mês, dia) de hoje vier antes de (mês, dia) do nascimento, tire 1.")]),
]

BUGS = r'''
@lib_datetime 2
import datetime
d = datetime(2026, 3, 15)
print(d.year)
>>> d = datetime.datetime(2026, 3, 15)
!! Com import datetime, a classe fica dentro do módulo: datetime.datetime. Ou use from datetime import datetime.

@lib_datetime 2
from datetime import date
vencimento = date(2026, 2, 30)
print(vencimento)
>>> vencimento = date(2026, 2, 28)
!! Fevereiro não tem dia 30: a data não existe e dá ValueError. O último dia de fevereiro de 2026 é 28.

@lib_datetime 3
from datetime import date
d = date(2026, 3, 15)
print(d.strftime("%d/%M/%Y"))  # esperado: 15/03/2026
>>> print(d.strftime("%d/%m/%Y"))  # esperado: 15/03/2026
!! %M maiúsculo é minuto. O mês é %m minúsculo.

@lib_datetime 3
from datetime import date, timedelta
compra = date(2026, 4, 28)
print(compra + 7)
>>> print(compra + timedelta(days=7))
!! Não dá para somar número com data. Use timedelta(days=7).

@lib_datetime 4
from datetime import date
inicio = date(2026, 12, 1)
fim = date(2026, 12, 25)
print(fim - inicio)  # esperado: 24
>>> print((fim - inicio).days)  # esperado: 24
!! A subtração dá um timedelta ("24 days, 0:00:00"). Para ter só o número, use .days.

@lib_datetime 2
from datetime import datetime
d = datetime.strptime("25/12/2026", "%Y-%m-%d")
print(d.day)
>>> d = datetime.strptime("25/12/2026", "%d/%m/%Y")
!! O formato tem de bater com o texto: dia/mês/ano, com barras.
'''
