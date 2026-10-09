# Projetos guiados — formato

Cada arquivo `NN_id.py` define `PROJETO = dict(...)`:

```python
PROJETO = dict(
    id="adivinha",                 # único, só letras minúsculas e _
    titulo="Adivinhe o número",
    emoji="🎲",
    resumo="Um jogo em que o computador sorteia um número e você tenta adivinhar.",
    requer="u5l1",                 # lição da trilha "Python do zero" que libera o projeto
    passos=[
        dict(
            titulo="Sorteando o número",
            explica="Texto curto (2 a 5 frases) dizendo o que este passo constrói e por quê.",
            tarefa="O que a pessoa precisa fazer, em uma ou duas frases diretas.",
            starter="código inicial (inclui a solução de referência do passo anterior + # TODO)",
            solucao="código completo que passa nos testes",
            tests="asserts com mensagem em português (o que falhou e como arrumar)",
            dica="uma dica sem entregar a resposta",
        ),
        ...
    ],
)
```

Regras (conferidas por `tools/validar_projetos.py`, que usa o MESMO Python do app):

- 5 a 7 passos. Cada passo constrói uma parte; o `starter` do passo N começa da `solucao` do passo N-1
  (o validador confere que a solução anterior aparece no começo do starter, ignorando linhas `# TODO`).
- O código roda como **módulo importado** (`__name__ == "projeto"`), então o jogo de verdade fica em
  `def main():` chamado por `if __name__ == "__main__": main()`. Esse bloco NÃO roda nos testes; ele roda
  quando a pessoa toca em "Jogar no editor". Ensine isso no passo em que o bloco aparece.
- Nada de `input()` fora de funções. Para testar uma função que usa `input()`, os testes trocam o input:
  `entradas = iter(["5", "3"]); input = lambda p="": next(entradas)` (os testes rodam no mesmo namespace
  do código) e capturam a saída com `io.StringIO` + `contextlib.redirect_stdout`.
- `__stdout__` tem o que o código imprimiu ao ser carregado.
- A `solucao` passa nos testes; o `starter` NÃO passa. Mensagens de assert ajudam um iniciante.
- Use só o que a trilha já ensinou até a lição `requer` (e o que o próprio projeto explica).
- `random`: nos testes, nunca dependa do número sorteado; passe o valor como parâmetro.
- `demo_entrada` (no PROJETO, opcional mas recomendado): respostas do `input()`, uma por linha, que fazem o jogo
  final terminar sozinho QUALQUER que seja o sorteio (ex.: limite de tentativas, opção "sair"). O validador roda o
  jogo com elas e mostra a saída; o app usa como respostas de exemplo no editor.
- Português do Brasil, tom simpático do PyPasso, explicações curtas.
