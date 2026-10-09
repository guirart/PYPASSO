# Lições 2–6 das unidades de built-ins

Na trilha "71 built-ins" do PyPasso, **cada função embutida é uma unidade com 6 lições**
e uma Prova de fogo no final. A lição 1 de cada função já existe em
`tools/gerar_builtins.py` (blocos `B("nome", ...)`): é o básico. Os arquivos desta pasta
trazem as **lições 2 a 6** de um grupo de funções e os **bugs da Prova de fogo** de cada uma.

Público: iniciantes brasileiros (app estilo Duolingo). Português do Brasil, frases curtas,
"você", exemplos concretos e divertidos (jogos, lojas, notas, receitas, pets…).

## Arquivo

`tools/builtins_licoes/gNN_slug.py`:

```python
from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

LICOES = {
    "nome_da_funcao": [L(...), L(...), L(...), L(...), L(...)],   # exatamente 5 (lições 2..6)
    ...
}

BUGS = r'''
@fn_nome 2
codigo com bug
>>> linha corrigida
!! explicação curta
'''
```

Exemplo completo e aprovado: `tools/builtins_licoes/exemplo_print.py`.

## Lições (ordem sugerida)

2. Parâmetros e variações (o que muda com cada argumento).
3. Usos práticos do dia a dia.
4. Cuidados e pegadinhas (erros comuns, o que dá erro e por quê).
5. Combinando com outras funções/recursos.
6. Desafio (sempre com um exercício `CODE`).

Não repita o conteúdo da lição 1 — leia o bloco `B("nome", ...)` em `tools/gerar_builtins.py`
e avance a partir dele.

`L(titulo, explica, exemplo, itens, entrada="")`
- `titulo`: até ~30 caracteres, sem o nome da unidade repetido à toa.
- `explica`: 1 a 3 frases que ensinam o conceito ANTES de cobrar.
- `exemplo`: código curto que roda e mostra o conceito (a saída é calculada sozinha).
- `itens`: 4 exercícios (3 a 5), variando os tipos.

Exercícios (`bt_helpers.py`):
- `OUT(codigo, [3 errados], explicacao)`: "Qual é a saída?" — a resposta certa é calculada rodando.
  Distratores plausíveis e diferentes da resposta.
- `TYPE(codigo, explicacao)`: "Digite a saída" — a saída tem de ser UMA linha curta.
- `MC(pergunta, certo, [2 ou 3 errados], explicacao)`.
- `FILL(pergunta, codigo_com____, certo, [errados], explicacao)` — exatamente uma lacuna `___`.
- `ORDER(pergunta, [linhas na ordem certa], explicacao)` — 3+ linhas, sem linhas repetidas.
- `CODE(pergunta, codigo_inicial, solucao, testes, explicacao)` — `testes` são `assert`s com
  mensagem em português; `__stdout__` tem o que o programa imprimiu. O código inicial
  NÃO pode passar nos testes. Cada função precisa de pelo menos 2 `CODE` nas lições 2–6.

## Regras de execução (o conteúdo roda no CPython aqui e no Pyodide/navegador no app)

- Saídas precisam ser determinísticas: nada de `id()` cru, `hash()` de texto, sets de textos
  impressos (a ordem muda), datas/horas, `random` sem necessidade.
- Não imprima mensagens de erro do Python (`str(e)`) — mudam entre versões. Use `type(e).__name__`.
- `help()` imprime textos enormes: use `__doc__`. `dir()`/`globals()`/`locals()`: não imprima tudo,
  teste com `in`, `len` de algo pequeno, etc.
- `input()`: só nas lições de `input` em `OUT`/`TYPE`/exemplo, com `entrada="resposta1\nresposta2"`
  e um comentário `# a pessoa digita X`. Nunca em `CODE` (no app, input não funciona nos exercícios).
- `aiter`/`anext`: `asyncio.run` NÃO funciona no navegador. Rode a corrotina na mão, como a lição 1
  faz (`main().send(None)` dentro de `try/except StopIteration`), ou explique sem rodar.
- `breakpoint`: troque `sys.breakpointhook` por uma função que imprime, como a lição 1.
- `open`: pode criar arquivos (cada execução roda numa pasta vazia). Use `encoding="utf-8"`.
- Nada de rede, threads, `time.sleep`, laços infinitos.

## Bugs da Prova de fogo

Pelo menos **5 por função** (6 é melhor), sobre aquela função. Cada bloco:

```
@fn_len 2
nome = 12345
print(len(nome))
>>> print(len(str(nome)))
!! Números não têm tamanho. Converta para texto.
```

- `@fn_<nome> N`: N = número da linha com o erro (começa em 1). Para `__import__` use `@fn___import__`.
- Só UMA linha muda. A linha `>>>` sem recuo herda o recuo da linha errada; escreva o recuo se ele mudar.
- O código com bug tem de dar erro OU resultado diferente do corrigido. O corrigido tem de rodar.
- Para erros de lógica, ponha `# esperado: X` na linha que imprime; X = última linha da saída corrigida.
- Trechos de 2 a 7 linhas, realistas, do tipo que iniciante escreve.

## Conferir

```
python3 tools/validar_builtins.py tools/builtins_licoes/gNN_slug.py
```

Repita até aparecer `OK`. O validador roda tudo e aponta cada problema.
