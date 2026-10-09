# Trilha "Bibliotecas" do PyPasso

Uma unidade por biblioteca, com **6 lições**: cada lição ensina **uma funcionalidade** da
biblioteca (ex.: em `math`, uma lição para arredondar com floor/ceil, outra para raízes e
potências, outra para constantes...). Depois vem a Prova de fogo da unidade (bugs).

Público: iniciantes brasileiros que já sabem o básico de Python (variáveis, strings, listas,
dicionários, if, for, funções). Português do Brasil, frases curtas, "você", exemplos concretos e
divertidos (loja, notas da turma, jogos, receitas, pets, agenda...). Mostre para que a
funcionalidade serve na vida real.

## Arquivo: `tools/bibliotecas/NN_slug.py`

```python
from bt_helpers import OUT, TYPE, MC, FILL, ORDER, CODE, L

UNIDADE = dict(id="lib_math", titulo="math", descricao="Contas avançadas: raízes, arredondar, pi...",
               externa=False, grupo="Biblioteca padrão")   # grupo: "Biblioteca padrão" ou "Bibliotecas externas"

LICOES = [L(...), L(...), L(...), L(...), L(...), L(...)]   # exatamente 6

BUGS = r'''
@lib_math 2
import math
print(math.sqroot(16))
>>> print(math.sqrt(16))
!! A raiz quadrada se chama sqrt.
'''
```

Exemplo do estilo (lições e bugs aprovados): `tools/builtins_licoes/exemplo_print.py`.
Ferramentas: `tools/bt_helpers.py` (OUT, TYPE, MC, FILL, ORDER, CODE, L — leia as docstrings).

## Lições

`L(titulo, explica, exemplo, itens)`:
- `titulo`: a funcionalidade, curto (até ~30 caracteres). Ex.: "Arredondando: floor e ceil".
- `explica`: 1 a 3 frases que ensinam ANTES de cobrar: o que faz, para que serve, como se usa.
- `exemplo`: código curto que roda (com o `import`) e mostra a funcionalidade. A saída é calculada sozinha.
- `itens`: 4 exercícios variando OUT, TYPE, MC, FILL, ORDER e CODE.
- A lição 1 da unidade apresenta a biblioteca (o que é, como importar, para que serve) e a primeira funcionalidade.
- A lição 6 é um desafio que junta as funcionalidades.

Regras de exercícios:
- `OUT`: 3 distratores plausíveis e diferentes da resposta. `TYPE`: a saída tem UMA linha curta.
- `FILL`: exatamente uma lacuna `___`. `ORDER`: 3+ linhas, sem linhas repetidas.
- `CODE`: testes com `assert` e mensagem em português; `__stdout__` tem o que foi impresso; o
  código inicial NÃO pode passar. **Bibliotecas padrão: pelo menos 2 CODE, e a lição 6 tem CODE.**
  **Bibliotecas externas (numpy, pandas, matplotlib, requests): NENHUM CODE** — use OUT, TYPE, MC,
  FILL e ORDER (o app não instala pacotes dentro dos exercícios).

## Execução (tudo é conferido rodando Python 3.13; numpy 2.5, pandas 3.0, matplotlib 3.11 instalados)

- Saídas determinísticas: nada de data/hora atual, `random` sem `random.seed(...)` no próprio código,
  `id()`, `hash()` de texto, sets de textos impressos, endereços de memória.
- Não imprima mensagens de erro (`str(e)`): use `type(e).__name__`.
- Sem internet: em `requests`, ensine com MC/ORDER/FILL e com exemplos que não fazem requisição de
  verdade (ex.: montar a URL, `params`, ler um JSON em texto com `json.loads`, um objeto de resposta
  de mentirinha criado na hora). Nunca chame `requests.get` de verdade.
- Matplotlib: roda sem tela (backend Agg). Não mostre imagens; teste coisas como `len(ax.lines)`,
  `ax.get_title()`, rótulos, `type(fig).__name__`. Explique `plt.show()`/`savefig` nos cartões e MCs.
- pandas/numpy: prefira saídas pequenas e estáveis (uma linha: `print(df.shape)`, `print(s.sum())`,
  `print(arr.tolist())`). Para TYPE, a saída tem uma linha.
- Arquivos (`csv`, `json`, `pathlib`): cada execução roda numa pasta vazia; crie os arquivos no
  próprio código, com `encoding="utf-8"`.
- `input()` nunca.

## Bugs da Prova de fogo

5 ou 6 por unidade, sobre aquela biblioteca. `@<id> N` (N = linha do erro, começa em 1);
`>>> linha corrigida` (sem recuo herda o da linha errada); `!! explicação curta`. O código com
bug tem de dar erro ou resultado diferente; o corrigido tem de rodar; para erros de lógica use
`# esperado: X` na linha que imprime (X = última linha da saída corrigida).

## Conferir

```
python3 tools/validar_bibliotecas.py tools/bibliotecas/NN_slug.py
```
Repita até aparecer OK.
