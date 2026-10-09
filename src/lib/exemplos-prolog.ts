/**
 * Programas de exemplo do Laboratório Prolog. São originais, no espírito dos exemplos do SWISH (swish.swi-prolog.org):
 * fatos e ciúmes, listas, filmes, sistema especialista, rainhas, cavaleiros e patifes.
 */
export type ExemploProlog = { id: string; nome: string; descricao: string; programa: string; consulta: string; esperado: string };

export const EXEMPLOS_PROLOG: ExemploProlog[] = [
  {
    id: 'ciumes', nome: 'Gosta e ciúmes', descricao: 'Fatos, regra com variável compartilhada e X \\= Y.',
    programa: `% quem gosta de quem
gosta(maria, joao).
gosta(joao, maria).
gosta(ana, joao).
gosta(pedro, ana).

% X tem ciúmes de Y se os dois gostam da mesma pessoa
ciumento(X, Y) :-
    gosta(X, Z),
    gosta(Y, Z),
    X \\= Y.
`,
    consulta: 'ciumento(X, Y).', esperado: 'X = maria, Y = ana',
  },
  {
    id: 'familia', nome: 'Família', descricao: 'Regras que usam outras regras: avô, irmãos, ancestral (recursão).',
    programa: `pai(jose, ana).
pai(jose, paulo).
pai(paulo, rita).
pai(ana, lia).
mae(clara, ana).
mae(clara, paulo).

progenitor(X, Y) :- pai(X, Y).
progenitor(X, Y) :- mae(X, Y).

avo(X, Z) :- progenitor(X, Y), progenitor(Y, Z).
irmao(X, Y) :- progenitor(P, X), progenitor(P, Y), X \\= Y.

ancestral(X, Y) :- progenitor(X, Y).
ancestral(X, Y) :- progenitor(X, Z), ancestral(Z, Y).
`,
    consulta: 'ancestral(jose, Quem).', esperado: 'Quem = ana',
  },
  {
    id: 'listas', nome: 'Listas', descricao: 'Recursão sobre [Cabeça|Cauda], append, reverse e length.',
    programa: `membro(X, [X|_]).
membro(X, [_|T]) :- membro(X, T).

tamanho([], 0).
tamanho([_|T], N) :- tamanho(T, M), N is M + 1.

soma([], 0).
soma([H|T], S) :- soma(T, R), S is R + H.
`,
    consulta: 'soma([1,2,3,4], S), tamanho([a,b,c], N).', esperado: 'S = 10, N = 3',
  },
  {
    id: 'filmes', nome: 'Filmes', descricao: 'Uma pequena base de dados com findall, consultas e contas.',
    programa: `filme(matrix, 1999, ficcao).
filme(titanic, 1997, drama).
filme(alien, 1979, ficcao).
filme(casablanca, 1942, drama).
filme(avatar, 2009, ficcao).

antigo(F) :- filme(F, Ano, _), Ano < 1980.
do_genero(G, Lista) :- findall(F, filme(F, _, G), Lista).
`,
    consulta: 'do_genero(ficcao, L).', esperado: 'L = [matrix,alien,avatar]',
  },
  {
    id: 'animais', nome: 'Sistema especialista', descricao: 'Regras que identificam um animal a partir de características.',
    programa: `% características observadas
tem(bicho, penas).
tem(bicho, bico).
nao_voa(bicho).

animal(ave)       :- tem(bicho, penas), tem(bicho, bico).
animal(mamifero)  :- tem(bicho, pelos), tem(bicho, leite).
animal(reptil)    :- tem(bicho, escamas).

especie(pinguim)  :- animal(ave), nao_voa(bicho).
especie(pardal)   :- animal(ave), \\+ nao_voa(bicho).
`,
    consulta: 'especie(E).', esperado: 'E = pinguim',
  },
  {
    id: 'rainhas', nome: 'Rainhas', descricao: 'Coloque N rainhas num tabuleiro sem ataques (tentativa e erro com backtracking).',
    programa: `rainhas(N, Qs) :-
    numlist(1, N, Ns),
    permutation(Ns, Qs),
    seguro(Qs).

seguro([]).
seguro([Q|Qs]) :- sem_ataque(Q, Qs, 1), seguro(Qs).

sem_ataque(_, [], _).
sem_ataque(Q, [Q1|Qs], D) :-
    Q =\\= Q1 + D,
    Q =\\= Q1 - D,
    D1 is D + 1,
    sem_ataque(Q, Qs, D1).
`,
    consulta: 'rainhas(6, Qs).', esperado: 'Qs = [2,4,6,1,3,5]',
  },
  {
    id: 'patifes', nome: 'Cavaleiros e patifes', descricao: 'Quebra-cabeça: cavaleiros sempre dizem a verdade e patifes sempre mentem.',
    programa: `% cavaleiro diz a verdade; patife mente
tipo(cavaleiro).
tipo(patife).

afirma(cavaleiro, F) :- call(F).
afirma(patife, F)    :- \\+ call(F).

% A diz: "B é patife".   B diz: "A e eu somos do mesmo tipo".
solucao(A, B) :-
    tipo(A), tipo(B),
    afirma(A, B = patife),
    afirma(B, A = B).
`,
    consulta: 'solucao(A, B).', esperado: 'A = cavaleiro, B = patife',
  },
  {
    id: 'contador', nome: 'assert e retract', descricao: 'Mudando a base de conhecimento durante a consulta.',
    programa: `:- dynamic contador/1.
contador(0).

incrementa :-
    retract(contador(N)),
    M is N + 1,
    assert(contador(M)).
`,
    consulta: 'incrementa, incrementa, contador(X).', esperado: 'X = 2',
  },
  {
    id: 'fatorial', nome: 'Fatorial e Fibonacci', descricao: 'Recursão com contas (is) e comparações.',
    programa: `fatorial(0, 1).
fatorial(N, F) :-
    N > 0,
    M is N - 1,
    fatorial(M, G),
    F is N * G.

fib(0, 0).
fib(1, 1).
fib(N, F) :-
    N > 1,
    A is N - 1, B is N - 2,
    fib(A, FA), fib(B, FB),
    F is FA + FB.
`,
    consulta: 'fatorial(6, F), fib(12, X).', esperado: 'F = 720, X = 144',
  },
];
